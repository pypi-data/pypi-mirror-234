from biolib.typing_utils import TypedDict


class ExperimentDict(TypedDict):
    created_at: str
    job_count: int
    job_running_count: int
    name: str
    uuid: str
