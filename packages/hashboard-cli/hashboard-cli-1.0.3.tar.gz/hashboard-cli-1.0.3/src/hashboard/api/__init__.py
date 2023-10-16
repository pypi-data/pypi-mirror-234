import click
from click import ClickException
import json
import os
from pathlib import PurePath
from requests import Session
from typing import List, Optional, Dict

from hashboard.constants import FILE_SIZE_LIMIT_MB, HASHBOARD_BASE_URI
from hashboard.credentials import CliCredentials
from hashboard.filesystem import build_spec_from_local
from hashboard import VERSION
from hashboard.utils.resource import Resource


def login(session: Session, credentials: CliCredentials):
    """Authenticates the session with the provided credentials.

    :return The user's project ID, if successfully logged in.
    :raises ClickException if the login is not successful.
    """
    r = session.post(
        HASHBOARD_BASE_URI + "/auth/login-cli",
        data={
            "accessKeyId": credentials.access_key_id,
            "accessKeyToken": credentials.access_key_token,
        },
        headers={"Glean-CLI-Version": VERSION},
    )
    # TODO(dse): Show custom error message from server, if present.
    if r.status_code >= 500:
        raise ClickException("Unexpected error initiating your Hashboard session.")
    elif r.status_code >= 400:
        raise ClickException("Your access key is invalid.")
    if not r.ok:
        raise ClickException("Unexpected error initiating your Hashboard session.")

    click.echo()
    click.echo("Successfully logged in to " + click.style(r.text, bold=True))
    click.echo("Project id: " + credentials.project_id)
    click.echo("Access key id: " + credentials.access_key_id)

    return credentials.project_id


def create_build_from_git_revision(
    session: Session,
    project_id: str,
    git_revision: Optional[str],
    git_path: Optional[str],
    deploy: bool,
    allow_dangerous_empty_build: bool = False,
    dbt_manifest_path: Optional[PurePath] = None,
):
    """Creates a build based on a git revision and returns the result."""
    build_spec = {
        "configFilesFromGit": {
            "revision": git_revision,
            "path": git_path,
            "dbtManifestPath": dbt_manifest_path,
        }
    }
    return _create_build(
        session, project_id, build_spec, deploy, allow_dangerous_empty_build
    )


def create_build_from_local_files(
    session: Session,
    project_id: str,
    path: str,
    deploy: bool,
    targets: Optional[set],
    allow_dangerous_empty_build: bool = False,
    dbt_manifest_path: Optional[PurePath] = None,
):
    """Creates a build using local files and returns the result."""
    build_spec = build_spec_from_local(path, project_id, targets, dbt_manifest_path)
    return _create_build(
        session, project_id, build_spec, deploy, allow_dangerous_empty_build
    )


def get_datasources(s: Session, project_id: str) -> dict:
    """Queries and formats datasources"""
    query = _get_data_connections(s, project_id)
    data_sources = {d["name"]: d["id"] for d in query["data"]["dataConnections"]}
    return data_sources


def clear_model_cache(s: Session, model_id: str) -> str:
    """Clears the cache for the specified model"""
    return _graphql_query(
        s,
        """
        mutation UpdateModelFreshnessKey($id: String!) {
            updateModelFreshnessKey(id: $id)
        }
        """,
        {"id": model_id},
    )


class PullResourceResponse(dict):
    configs: List[Resource]
    errors: List[str]


def pull_resource(
    s: Session,
    project_id: str,
    resource_type: Optional[str],
    resource_id: Optional[str],
    resource_alias: Optional[str],
    dataops_only: Optional[bool],
) -> PullResourceResponse:
    """Pulls the DataOps config for the given resource, or all resources in the project if none is specified."""
    res = _graphql_query(
        s,
        """
        query PullResource($projectId: String!, $resourceType: String, $resourceId: String, $resourceAlias: String, $dataOpsOnly: Boolean) {
            pullResource(
                projectId: $projectId,
                resourceType: $resourceType,
                resourceId: $resourceId,
                resourceAlias: $resourceAlias,
                dataOpsOnly: $dataOpsOnly
            ) { configs, errors }
        }
        """,
        {
            "projectId": project_id,
            "resourceType": resource_type,
            "resourceId": resource_id,
            "resourceAlias": resource_alias,
            "dataOpsOnly": dataops_only,
        },
    )["data"]["pullResource"]
    res["configs"] = [
        Resource.from_dict(json.loads(string)) for string in res["configs"]
    ]
    return res


def _parse_table_data(table_data: dict) -> Dict[str, Dict[str, str]]:
    """Formats table names for output, and returns tables names and schemas"""
    tables = table_data["data"]["getAvailableGleanDbTables"]
    tables_by_name = {}
    for table in tables:
        name = (
            table["schema"] + "." + table["name"] if table["schema"] else table["name"]
        )
        tables_by_name[name] = {"schema": table["schema"], "name": table["name"]}
    return tables_by_name


def _create_build(
    session, project_id, build_spec, deploy, allow_dangerous_empty_build=False
):
    return _graphql_query(
        session,
        """
        mutation CreateBuild($projectId: String!, $buildSpec: BuildSpecInput!, $deploy: Boolean!, $allowEmptyBuild: Boolean) {
            createBuild( projectId: $projectId, buildSpec: $buildSpec, deploy: $deploy, allowEmptyBuild: $allowEmptyBuild) {
                id,
                resources {
                    added { modelBundles { model { name } }, savedViews { name }, dashboards { name }, colorPalettes { name }, homepageLaunchpads { id }, metrics { name } }
                    changed { modelBundles { model { name } }, savedViews { name }, dashboards { name }, colorPalettes { name }, homepageLaunchpads { id }, metrics { name }}
                    unchanged { modelBundles { model { name } }, savedViews { name }, dashboards { name }, colorPalettes { name }, homepageLaunchpads { id }, metrics { name } }
                    deleted { modelBundles { model { name } }, savedViews { name }, dashboards { name }, colorPalettes { name }, homepageLaunchpads { id }, metrics { name } }
                },
                warnings,
                errors
            }
        }
        """,
        {
            "projectId": project_id,
            "buildSpec": build_spec,
            "deploy": deploy,
            "allowEmptyBuild": allow_dangerous_empty_build,
        },
    )


def _get_data_connections(session: Session, project_id: str) -> dict:
    query = _graphql_query(
        session,
        """
        query dataConnections($projectId: String!){
            dataConnections(projectId: $projectId){
                id,
                name
            }
        }
        """,
        {"projectId": project_id},
    )
    return query


def _get_table_data(session: Session, datasource_id: str) -> dict:
    query = _graphql_query(
        session,
        """
        query getAvailableGleanDbTables($datasourceId: String!){
            getAvailableGleanDbTables (datasourceId: $datasourceId){
                name,
                schema
            }
        }
        """,
        {"datasourceId": datasource_id},
    )
    return query


def get_tables(s: Session, datasource_id: str) -> Dict[str, Dict[str, str]]:
    """Queries and formats table from datasource"""
    query = _get_table_data(s, datasource_id)
    tables = _parse_table_data(query)
    return tables


preview_uri = lambda build_results, query_name="createBuild": click.style(
    f"{HASHBOARD_BASE_URI}/app/?build={build_results['data'][query_name]['id']}",
    underline=True,
)

build_details_uri = lambda build_results, query_name="createBuild": click.style(
    f"{HASHBOARD_BASE_URI}/app/p/builds/{build_results['data'][query_name]['id']}",
    underline=True,
)

preview_model_uri = (
    lambda model_id, build_results, query_name="modelPreviewBuildFromGleanDb": f"{HASHBOARD_BASE_URI}/app/m/{model_id}?build={build_results['data'][query_name]['id']}"
)


def _graphql_query(session: Session, query: str, variables: dict):
    r = session.post(
        HASHBOARD_BASE_URI + "/graphql/",
        json={"query": query, "variables": variables},
        headers={"Glean-CLI-Version": VERSION},
    )
    if r.status_code == 504:
        raise ClickException(
            f"The Hashboard CLI client has timed out but your request is still running on our server. Please check your project's build page in a few minutes to see build results: {HASHBOARD_BASE_URI}/app/p/data-ops"
        )
    elif r.status_code != 200:
        raise ClickException("Unexpected error received from the Hashboard server.")

    results = r.json()
    graphql_exceptions = results.get("errors")
    if (
        graphql_exceptions
        and isinstance(graphql_exceptions[0], dict)
        and graphql_exceptions[0].get("message")
    ):
        error = graphql_exceptions[0]["message"]

        # Must match error message in server code at glean/services/data_ops/build_management.py line #543 (as of 7/5/23).
        if (
            error
            == "No Glean config files were found, and empty builds were not enabled, so the build was aborted."
            or error
            == "No Hashboard config files were found, and empty builds were not enabled, so the build was aborted."
        ):
            error += "\n\tTo enable empty builds, use the --allow-dangerous-empty-build flag.\n\tWARNING: This will remove all data-ops managed resources, and any resources that depend on them, from your project."
            from hashboard.cli import _echo_build_errors_and_exit

            _echo_build_errors_and_exit([error])

        raise ClickException(
            f"Unexpected error received from the Hashboard server:\n  {error}"
        )

    return results


def upload_files_to_hashboard(session: Session, project_id: str, path: str) -> str:
    return _post_file(session, project_id, path)


def _is_over_filesize_limit(file_path: str) -> bool:
    size_in_bytes = os.path.getsize(file_path)
    size_in_mb = size_in_bytes / (1024 * 1024)

    return size_in_mb > FILE_SIZE_LIMIT_MB


def _post_file(session: Session, project_id: str, file_path: str) -> str:
    if _is_over_filesize_limit(file_path):
        raise ClickException(
            f"File exceeds upload limit of {FILE_SIZE_LIMIT_MB} megabytes"
        )

    r = session.post(
        HASHBOARD_BASE_URI + "/upload/data-file",
        data={"projectId": project_id},
        files={"file": open(file_path, "rb")},
        headers={"Glean-CLI-Version": VERSION},
    )

    results = r.json()
    file_errors = results.get("error")
    if file_errors:
        raise ClickException(f"Error uploading file\n  {file_errors}")

    uploaded_filename = results.get("filename")

    if uploaded_filename:
        return uploaded_filename
    else:
        raise ClickException(f"Error uploading file\n  Unexpected result from server")


def export_query(
    session: Session, endpoint: str, data: dict, additional_headers: dict = {}
):
    """POST request to export controllers"""
    r = session.post(
        HASHBOARD_BASE_URI + f"/export/{endpoint}",
        data=json.dumps(data),
        headers={"Glean-CLI-Version": VERSION, **additional_headers},
    )
    if r.status_code != 200:
        raise ClickException("Unexpected error received from the Hashboard server.")
    return r.text
