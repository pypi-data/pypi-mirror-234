"""Helper functions for the CLI API Wrapper"""
import os
import shutil
from click import Argument, Command, Context, Option
from contextlib import redirect_stdout, suppress
from flask_restx import Api, Model, Resource, fields
from flask_restx.reqparse import RequestParser
from io import StringIO
from requests.exceptions import JSONDecodeError
from typing import Callable, Dict, Optional, Tuple, Union
from urllib.parse import urljoin

from regscale.core.app.api import Api as CliApi
from regscale.core.app.application import Application
from regscale.utils.string import remove_ansi_escape_sequences


def execute_click_command_in_context(command: Command, params: dict = None) -> str:
    """Execute a click command
    :param Command command: a click.Command for performing the logic
    :param dict params: an optional dictionary of parameter key values to pass
    :returns: a string of the command output
    """
    with Context(command) as ctx:
        # redirect stdout to a string to capture command output
        output_stream = StringIO()
        with redirect_stdout(output_stream):
            with suppress(SystemExit):
                if params:
                    # run command, params are key values of the request JSON
                    ctx.invoke(command, **params)
                else:
                    # no params, so don't use them
                    ctx.invoke(command)
            # retrieve the output, remove ansi escape sequences to not color
            # also remove trailing returns
            output = remove_ansi_escape_sequences(text=output_stream.getvalue().strip())
    return output


# pylint: disable=duplicate-code
def create_view_func(command: Command) -> Union[Callable, Resource]:
    """Create a factory function for returning a CommandResource object for use in an API.
    :param Command command: a click.Command for performing the logic
    :returns: a Resource instance
    """
    parser = RequestParser()
    for param in command.params:
        parser.add_argument(param.human_readable_name, type=param.type, location="json")

    # define a CommandResource class to return (get or post depending upon if params are expected)
    if command.params and all([param.required for param in command.params]):

        class CommandResource(Resource):
            """Allow for the use of this view function using flask_restx."""

            def options(self) -> dict:
                """Return the allowed methods and any parameters expected"""
                methods = "GET, OPTIONS" if not command.params else "POST, OPTIONS"
                return {
                    "Allowed methods": methods,
                    "Parameters": [
                        param.human_readable_name for param in command.params
                    ],
                }

            def post(self) -> Tuple[Dict[str, str], int]:
                """Return output with params in a POST request"""
                if not command.params:
                    return {
                        "message": "Invalid method. This endpoint does not accept parameters, "
                        "use GET method instead"
                    }, 405
                args = parser.parse_args()
                params = {k: v for k, v in args.items() if v is not None}
                output = execute_click_command_in_context(command, params)
                return {"input": f"regscale {command.name}", "output": output}, 200

    elif command.params:

        class CommandResource(Resource):
            """Allow for the use of this view function using flask_restx."""

            def options(self) -> dict:
                """Return the allowed methods and any parameters expected"""
                methods = "GET, OPTIONS" if not command.params else "POST, OPTIONS"
                return {
                    "Allowed methods": methods,
                    "Parameters": [
                        param.human_readable_name for param in command.params
                    ],
                }

            def post(self) -> Tuple[Dict[str, str], int]:
                """Return output with params in a POST request"""
                if not command.params:
                    return {
                        "message": "Invalid method. This endpoint does not accept parameters, "
                        "use GET method instead"
                    }, 405
                args = parser.parse_args()
                params = {k: v for k, v in args.items() if v is not None}
                output = execute_click_command_in_context(command, params)
                return {"input": f"regscale {command.name}", "output": output}, 200

            def get(self) -> Tuple[Dict[str, str], int]:
                """Return output if get command is invoked."""
                if command.params:
                    return {
                        "message": "Invalid method. This endpoint expects parameters "
                        "use POST method for this endpoint with the following parameters: "
                        f"{','.join([p.human_readable_name for p in command.params])}",
                    }, 405
                output = execute_click_command_in_context(command)
                return {"input": f"regscale {command.name}", "output": output}, 200

    else:

        class CommandResource(Resource):
            """Allow for the use of this view function using flask_restx."""

            def options(self) -> dict:
                """Return the allowed methods and any parameters expected"""
                methods = "GET, OPTIONS" if not command.params else "POST, OPTIONS"
                return {
                    "Allowed methods": methods,
                    "Parameters": [
                        param.human_readable_name for param in command.params
                    ],
                }

            def get(self) -> Tuple[Dict[str, str], int]:
                """Return output if get command is invoked."""
                if command.params:
                    return {
                        "message": "Invalid method. This endpoint expects parameters "
                        "use POST method for this endpoint with the following parameters: "
                        f"{','.join([p.human_readable_name for p in command.params])}",
                    }, 405
                output = execute_click_command_in_context(command)
                return {"input": f"regscale {command.name}", "output": output}, 200

    return CommandResource


# pylint: enable=duplicate-code


def _get_field_type(param: Union[Option, Argument]) -> fields.Raw:
    """Retrieve the field type from a click.Option or click.Argument
    :param param: a click.Option or click.Argument
    :returns: a flask_restx.fields type
    """
    if param.type == int:
        return fields.Integer
    if param.type == float:
        return fields.Float
    if param.type == bool:
        return fields.Boolean
    return fields.String


def generate_parameters_model(api_instance: Api, command: Command) -> Model:
    """Generate a Flask_restx parameter model
    :param Api api_instance: the flask_restx.Api instance
    :param Command command: a click.Command to retrieve a Model from
    :returns: a flask_restx.Model of the parameters
    """
    parameters = {}
    for param in command.params:
        field_type = _get_field_type(param)
        parameters[param.name] = field_type(
            required=param.required, description=param.help
        )
    return api_instance.model(
        f"{command.name.title().replace('_', '')}Parameters", parameters
    )


def get_site_info():
    """Get site info
    :returns: Dictionary of site information to pass into pages
    """
    app = Application()
    site_info = {"domain": os.getenv("REGSCALE_DOMAIN", app.config["domain"])}

    return site_info


def get_catgalogues():
    """Get catalogues information
    :returns: List of tuples of catalogs in RegScale instance
    :rtype: List[Tuple[int, str]]
    """
    cli_app = Application()
    api = CliApi(cli_app)
    try:
        response = api.get(f"{cli_app.config['domain']}/api/catalogues/getlist")
        catalog_data = response.json()
        regscale_catalogues = [
            (catalog["id"], f'{catalog["title"][:45]} (#{catalog["id"]})')
            for catalog in catalog_data
        ]
    except (JSONDecodeError, KeyError, AttributeError, TypeError):
        regscale_catalogues = [
            (1, "Please Login to RegScale to retrieve Catalogues."),
        ]
    return regscale_catalogues


def get_ssps():
    """Get Security Plans from RegScale instance
    :returns: List of tuples of catalogs in RegScale instance
    :rtype: List[Tuple[int, str]]
    """
    cli_app = Application()
    api = CliApi(cli_app)
    body = """
            query {
                securityPlans(take: 50, skip: 0) {
                items {
                    id
                    systemName
                },
                pageInfo {
                    hasNextPage
                }
                ,totalCount}
            }
        """
    try:
        response = api.graph(query=body)
        ssp_data = response["securityPlans"]["items"]
        regscale_ssps = [
            (ssp["id"], f'{ssp["systemName"][:45]} (#{ssp["id"]})') for ssp in ssp_data
        ]
    except (JSONDecodeError, KeyError, AttributeError, TypeError):
        regscale_ssps = [
            (1, "Please Login to RegScale to retrieve SSPs."),
        ]
    return regscale_ssps


def get_ssp_name(ssp_id: Union[str, int]) -> str:
    """Get Security Plans from RegScale instance
    :param Union[str, int] ssp_id: ID of SSP to retrieve name for
    :returns: Name of the SSP from RegScale
    :rtype: str
    """
    cli_app = Application()
    api = CliApi(cli_app)
    body = f"""
            query {{
                securityPlans(take: 50, skip: 0, where: {{id: {{eq: {ssp_id}}}}}) {{
                items {{
                    id
                    systemName
                }},
                pageInfo {{
                    hasNextPage
                }}
                ,totalCount}}
            }}
            """
    try:
        response = api.graph(query=body)
        ssp_name = response["securityPlans"]["items"][0]["systemName"]
    except (JSONDecodeError, KeyError, AttributeError, TypeError):
        ssp_name = f"RegScale SSP# {ssp_id}"
    return ssp_name


def delete_all_items_in_directory(
    dir_path: str, keep_ext: Optional[str] = None
) -> None:
    """
    Recursively delete all files and directories in the given directory
    :param str dir_path: The directory whose contents are to be deleted
    :param str keep_ext: The file extension to keep (g.g., '.ckl') If None, all files will be deleted
    :return: None
    """
    # Check if the directory exists
    if not os.path.exists(dir_path):
        print(f"The directory {dir_path} does not exist.")
        return

    # Iterate through all the items in the directory
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)

        # If item is a directory, recursively call this function
        if os.path.isdir(item_path):
            delete_all_items_in_directory(item_path, keep_ext)

            # Remove the directory only if it's empty
            if not os.listdir(item_path):
                os.rmdir(item_path)

        else:
            # If keep_ext is None, remove all files
            if keep_ext is None:
                os.remove(item_path)
            else:
                # Otherwise, get the file extension and check if it should be kept
                _, ext = os.path.splitext(item_path)
                if ext != keep_ext:
                    os.remove(item_path)


def get_profiles():
    """Get catalogues information
    :returns: List of tuples of catalogs in RegScale instance
    :rtype: List[Tuple[int, str]]
    """
    cli_app = Application()
    api = CliApi(cli_app)
    response = api.get(urljoin(cli_app.config["domain"], "/api/profiles/getlist"))
    try:
        profiles = response.json()
        regscale_profiles = [
            (profile["id"], f'{profile["name"][:45]} (#{profile["id"]})')
            for profile in profiles
        ]
    except (JSONDecodeError, KeyError, AttributeError, TypeError):
        regscale_profiles = [
            (1, "Please Login to RegScale to retrieve Profiles."),
        ]
    return regscale_profiles
