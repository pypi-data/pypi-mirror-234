from click import ClickException
import json
import yaml

parse_failure_message = (
    lambda filename, e: f"\n Could not parse file {filename}. \n Errors found in this file: \n ---- \n {e}"
)


def _is_valid_yaml_config_file(contents: str, filename: str) -> bool:
    try:
        data = yaml.safe_load(contents)
        return isinstance(data, dict) and (data.get("glean") is not None or data.get("hbVersion") is not None)
    except yaml.YAMLError as e:
        raise ClickException(parse_failure_message(filename, e))


def _is_valid_json_config_file(contents: str, filename: str) -> bool:
    try:
        data = json.loads(contents)
        return isinstance(data, dict) and (data.get("glean") is not None or data.get("hbVersion") is not None)
    except json.decoder.JSONDecodeError as e:
        raise ClickException(parse_failure_message(filename, e))


def is_valid_glean_config_file(filename: str, contents: str) -> bool:
    if filename.endswith(".yml") or filename.endswith(".yaml"):
        return _is_valid_yaml_config_file(contents, filename)

    if filename.endswith(".json"):
        return _is_valid_json_config_file(contents, filename)

    return False
