# pylint: disable=unsubscriptable-object
import threading
import time
import subprocess
from statistics import mean
from typing import List

from docker.models.containers import Container  # type: ignore

from biolib.biolib_logging import logger_no_user_data
from biolib.compute_node.cloud_utils import CloudUtils
from biolib.compute_node.webserver.webserver_types import ComputeNodeInfo


class UtilizationReporterThread(threading.Thread):
    def __init__(self,  container: Container, job_uuid: str, job_access_token: str, compute_node_info: ComputeNodeInfo):
        threading.Thread.__init__(self, daemon=True)
        self._container_object = container
        self._job_uuid = job_uuid
        self._job_auth_token = job_access_token
        self._compute_node_info = compute_node_info

        self._sample_duration_milliseconds = 1000
        self._samples_between_writes = 60  # 1 minute between writes

        self._has_gpu = False
        self._metrics: List[dict] = []

    @staticmethod
    def _get_gpu_utilization():
        cmd = "nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader"
        utilization = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
        utilization = utilization.decode("utf-8").strip().split("\n")
        utilization_for_each_gpu = [int(x.replace(" %", "")) for x in utilization]
        utilization_for_first_gpu = utilization_for_each_gpu[0]
        return utilization_for_first_gpu

    def _write_utilization_metrics_to_backend(self):
        # Calculate the average and max of all the samples since last write
        average_metrics = {key: mean(d[key] for d in self._metrics) for key in self._metrics[0]}
        max_metrics = {key: max(d[key] for d in self._metrics) for key in self._metrics[0]}

        response = CloudUtils.write_utilization_metric_sample(
            job_auth_token=self._job_auth_token,
            compute_node_auth_token=self._compute_node_info['auth_token'],
            data={
                'average_cpu_usage_in_percent': average_metrics['cpu'],
                'average_memory_usage_in_percent': average_metrics['memory'],
                'average_gpu_usage_in_percent': average_metrics['gpu'],
                'max_cpu_usage_in_percent': max_metrics['cpu'],
                'max_memory_usage_in_percent': max_metrics['memory'],
                'max_gpu_usage_in_percent': max_metrics['gpu'],
                'job': self._job_uuid,
                'sample_duration_in_milliseconds': self._sample_duration_milliseconds
            }
        )

        logger_no_user_data.info("Writing utilization metrics to backend...")
        if not response.ok:
            logger_no_user_data.warning(f"Could no post metrics due to f'{response.text}")

        self._metrics = []

    @property
    def _container(self):
        try:
            self._container_object.update()
            return self._container_object
        except BaseException:
            return None

    def run(self) -> None:
        # Determine if the app has access to GPU
        try:
            self._get_gpu_utilization()
            self._has_gpu = True
        except BaseException:
            self._has_gpu = False

        prev_cpu_usage = None
        prev_cpu_system_usage = None

        samples_since_last_write = 0

        while self._container and self._container.status not in ('exited',):
            try:
                stats = self._container.stats(stream=False)
                if not prev_cpu_usage or not prev_cpu_system_usage:
                    prev_cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
                    prev_cpu_system_usage = stats['cpu_stats']['system_cpu_usage']
                    continue

                # Calculate CPU usage
                cpu_usage_delta_ns = stats['cpu_stats']['cpu_usage']['total_usage'] - prev_cpu_usage
                cpu_system_usage_delta_ns = stats['cpu_stats']['system_cpu_usage'] - prev_cpu_system_usage
                cpu_usage_in_percent = round((cpu_usage_delta_ns / cpu_system_usage_delta_ns) * 100, 2)

                # Set previous usage
                prev_cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
                prev_cpu_system_usage = stats['cpu_stats']['system_cpu_usage']

                # Calculate Memory usage
                memory_usage_in_percent = round(
                    stats['memory_stats']['usage'] / stats['memory_stats']['limit'] * 100,
                    2
                )

                # Set metrics
                sample_metrics = {
                    'cpu': cpu_usage_in_percent,
                    'memory': memory_usage_in_percent
                }

                # GPU usage
                if self._has_gpu:
                    sample_metrics['gpu'] = self._get_gpu_utilization()

                self._metrics.append(sample_metrics)

            except BaseException as error:
                logger_no_user_data.warning(f'Could not retrieve utilization metrics due to: {error}')
                logger_no_user_data.warning(f'Stats data which failed: {stats}...')

            samples_since_last_write += 1
            if samples_since_last_write == self._samples_between_writes:
                self._write_utilization_metrics_to_backend()
                samples_since_last_write = 0

            time.sleep(self._sample_duration_milliseconds / 1000)

        # Write the remaining samples after container has exited
        if self._metrics:
            self._write_utilization_metrics_to_backend()
