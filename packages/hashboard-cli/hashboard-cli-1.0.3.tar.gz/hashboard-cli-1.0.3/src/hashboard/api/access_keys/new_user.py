from urllib.parse import urlencode
import click
from dataclasses import fields

from hashboard.api.access_keys.browser_auth import (
    QueryParamsHandler,
    auth_and_handle_query_params,
)
from hashboard.api.access_keys.utils import (
    AccessKeyInfo,
    confirm_credentials_filepath,
    echo_horizontal_rule,
    save_access_key,
)
from hashboard.constants import HASHBOARD_BASE_URI
from hashboard.utils.cli import parse_str_bool


def create_account_and_access_key(
    credentials_filepath: str, user_full_name: str, project_name: str
):
    """Creates a new account and project and saves a new access key.
    For authentication, opens a browser page that pushes them through
    our sign up flow.

    Args:
        credentials_filepath (str): Filepath to save access key to.
        user_full_name (str): Full name of the new user.
        project_name (str): Name of the new project.
    """
    confirm_credentials_filepath(credentials_filepath)
    access_key_info = _get_new_account_access_key_info(user_full_name, project_name)
    if access_key_info:
        save_access_key(credentials_filepath, access_key_info)
        echo_horizontal_rule()
        click.echo()
        click.echo(
            f"👋 Welcome {access_key_info.user_full_name}! We created a new Glean project for you."
        )
        click.echo()
        click.echo(
            f"{click.style('Go to the following link to set up a database connection:', bold=True)} {HASHBOARD_BASE_URI}/app/mb"
        )
        click.echo()


def _get_new_account_access_key_info(
    user_full_name: str, project_name: str
) -> AccessKeyInfo:
    # If the user attempted signup with an existing user, this
    # holds that user's email.
    attempted_signup_with_existing_user = None

    # Whether our request errored while finishing authentication.
    request_error = False

    # Access key info received from Glean's app server.
    access_key_info = None

    def qp_handler(query_params: dict) -> str:
        nonlocal attempted_signup_with_existing_user
        nonlocal request_error
        nonlocal access_key_info

        attempted_signup_with_existing_user = query_params.get(
            "attempted_signup_with_existing_user"
        )
        if attempted_signup_with_existing_user:
            query_params_dict = {"userEmail": attempted_signup_with_existing_user}
            return f"{HASHBOARD_BASE_URI}/cliAuthConfirmation/error/attemptedSignupWithExistingUser?{urlencode(query_params_dict)}"

        if any(
            map(
                lambda field: query_params.get(field.name, None) is None,
                fields(AccessKeyInfo),
            )
        ):
            request_error = True
            return f"{HASHBOARD_BASE_URI}/cliAuthConfirmation/error"

        access_key_info = AccessKeyInfo(**query_params)
        return f"{HASHBOARD_BASE_URI}/cliAuthConfirmation/success/newUser?userFullName={access_key_info.user_full_name}"

    _signup_and_handle_query_params(qp_handler, user_full_name, project_name)

    # If encountered error while handling request, raise an exception.
    if request_error:
        raise click.ClickException(
            "Unknown error while finishing authentication. Please try again."
        )

    if attempted_signup_with_existing_user:
        click.echo(f"{attempted_signup_with_existing_user} already has a Glean user.")
        click.echo(
            f"To create a new account, re-run `glean signup` with a different email."
        )
        click.echo()
        click.echo(
            f"If you'd like to create an access key for your existing Glean account, run `glean token` instead."
        )
        return

    return access_key_info


def _signup_and_handle_query_params(
    handle_get_query_params: QueryParamsHandler, user_full_name: str, project_name: str
):
    base_url = f"{HASHBOARD_BASE_URI}/cliAuthConfirmation/entry/newUser"
    query_params_dict = {
        "cli-auth-user-full-name": user_full_name,
        "cli-auth-project-name": project_name,
    }
    auth_and_handle_query_params(handle_get_query_params, base_url, query_params_dict)
