from contextlib import suppress
import json
import os
import pathlib
from pathlib import Path, PurePath
from string import Template
from typing import Any, Callable, Optional, Dict, Union

import yaml
from click import ClickException

from hashboard.utils.resource import Resource
from hashboard.utils.validate_config import is_valid_glean_config_file


VALID_FILE_EXTENSIONS = set([".json", ".yml", ".yaml"])


def build_spec_from_local(
    path: str,
    project_id: str,
    targets: Optional[set] = None,
    dbt_manifest_path: Optional[PurePath] = None,
) -> dict:
    # Maps parent_directory -> filename -> file contents
    inline_files = []
    dbt_manifest = None

    if dbt_manifest_path:
        try:
            with open(Path(dbt_manifest_path), "r") as f:
                dbt_manifest = f.read()
        except Exception as e:
            raise ClickException(f"Could not read dbt manifest file: {e}")

    for root, subdirs, filenames in os.walk(path):
        for filename in filenames:
            if pathlib.Path(filename).suffix not in VALID_FILE_EXTENSIONS:
                continue
            if targets:
                if filename not in targets:
                    continue
            with open(os.path.join(root, filename), "r") as f:
                raw_contents = f.read()

                # Check that the file is a valid config file. Otherwise, ignore it.
                if not is_valid_glean_config_file(filename, raw_contents):
                    continue

                # Right now, changing the filepath of a config file changes its generated ID.
                # So, we set parentDirectory here to mimic the format that the server uses
                # when pulling from a git repo.
                path_suffix = f"/{path}" if path else ""
                parent_directory = root.replace(
                    path, f"/tmp/repos/{project_id}{path_suffix}"
                )
                try:
                    file_contents = Template(raw_contents).substitute(**os.environ)
                except KeyError as e:
                    raise ClickException(
                        f"No value found for environment variable substitution in {filename}: {str(e)}"
                    )

                inline_files.append(
                    {
                        "parentDirectory": parent_directory,
                        "filename": filename,
                        "fileContents": file_contents,
                    }
                )
    return {"inlineConfigFiles": inline_files, "dbtManifest": dbt_manifest}


def local_resources(root: Union[str, os.PathLike]) -> Dict[PurePath, Resource]:
    """
    Recursively searches root for files that represent Hashboard resources.
    """
    root = Path(root)

    def parse_yaml(raw: str) -> Optional[Dict[str, Any]]:
        with suppress(yaml.YAMLError):
            return yaml.safe_load(raw)

    def parse_json(raw: str) -> Optional[Dict[str, Any]]:
        with suppress(json.JSONDecodeError):
            return json.loads(raw)

    PARSERS: Dict[str, Callable[[str], Optional[Dict[str, Any]]]] = {
        ".yml": parse_yaml,
        ".yaml": parse_yaml,
        ".json": parse_json,
    }

    resources: Dict[PurePath, Resource] = {}

    for path in root.rglob("*"):
        if (not path.is_file()) or (path.suffix not in VALID_FILE_EXTENSIONS):
            continue

        with open(path, "r") as f:
            raw_contents = f.read()

            # parse the file as a dictionary
            parser = PARSERS[path.suffix]
            raw = parser(raw_contents)
            if raw is None or not isinstance(raw, dict):
                continue

            # parse the dictionary as a Hashboard Resource
            resource: Optional[Resource] = Resource.from_dict(raw)
            if resource is not None:
                resources[PurePath(path.relative_to(root))] = resource

    return resources
