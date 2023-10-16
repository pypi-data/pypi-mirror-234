import json

from biolib import api


def set_main_result_prefix(result_prefix: str) -> None:
    try:
        with open('/biolib/secrets/biolib_system_secret', mode='r') as system_secrets_file:
            system_secrets = json.loads(system_secrets_file.read())
    except Exception:  # pylint: disable=broad-except
        raise Exception('Unable to load the BioLib runtime system secret') from None

    if not system_secrets['version'].startswith('1.'):
        raise Exception(f"Unexpected system secret version {system_secrets['version']} expected 1.x.x")

    api.client.patch(
        data={'result_name_prefix': result_prefix},
        headers={'Job-Auth-Token': system_secrets['job_auth_token']},
        path=f"/jobs/{system_secrets['job_uuid']}/main_result/",
    )
