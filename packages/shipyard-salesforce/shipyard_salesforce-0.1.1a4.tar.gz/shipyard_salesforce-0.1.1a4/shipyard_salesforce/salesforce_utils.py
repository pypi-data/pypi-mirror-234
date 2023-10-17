import json

from typing import Optional
from requests import Response
from shipyard_templates import Crm, ExitCodeException


def handle_request_errors(response: Response) -> None:
    """
    Method for handling errors from the Salesforce API
    Can find error codes here: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/errorcodes.htm

    :param response: Response object from the Salesforce API
    :raises: ExitCodeException
    """
    try:
        response_details = response.json()
    except json.decoder.JSONDecodeError:
        response_details = {}

    if type(response_details) == list:
        response_details = response_details[0]  # TODO: Handle multiple errors

    if response.status_code in {401, 403}:
        raise ExitCodeException(
            response_details.get("error_description", "Invalid credentials"),
            Crm.EXIT_CODE_INVALID_CREDENTIALS,
        )
    elif response.status_code == 300:
        raise ExitCodeException(
            response_details.get("error_description", "Multiple IDs found"),
            Crm.EXIT_CODE_MULTIPLE_RECORDS_FOUND,
        )
    elif response.status_code == 304:
        raise ExitCodeException(
            response_details.get("error_description", "Not Modified"),
            Crm.EXIT_CODE_NOT_MODIFIED,
        )
    elif response.status_code in {400, 404, 405, 414, 428, 431}:
        raise ExitCodeException(
            response_details.get("error_description", "Bad Request"),
            Crm.EXIT_CODE_BAD_REQUEST,
        )
    elif response.status_code in {409, 412}:
        # The request could not be completed due to a conflict with the current state of the resource.
        raise ExitCodeException(
            response_details.get("error_description", "Conflict"),
            Crm.EXIT_CODE_CONFLICT,
        )

    elif response.status_code in {410}:
        raise ExitCodeException(
            response_details.get("error_description", "Not Found"),
            Crm.EXIT_CODE_RESOURCE_NOT_FOUND,
        )
    elif response.status_code in {500, 502, 503}:
        raise ExitCodeException(
            response_details.get("message", "Service unavailable"),
            Crm.EXIT_CODE_SERVICE_UNAVAILABLE,
        )
    else:
        raise ExitCodeException(response.text, Crm.EXIT_CODE_UNKNOWN_ERROR)


def validate_client_init(
    access_token: Optional[str] = None,
    consumer_key: Optional[str] = None,
    consumer_secret: Optional[str] = None,
    domain: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    security_token: Optional[str] = None,
) -> None:
    """
    Validates that the client is initialized with the correct combination arguments

    :param access_token: Access token for the Salesforce API
    :param consumer_key: Consumer key for the Salesforce API
    :param consumer_secret: Consumer secret for the Salesforce API
    :param domain: Domain for the Salesforce API
    :param username: Username for the Salesforce API
    :param password: Password for the Salesforce API
    :param security_token: Security token for the Salesforce API
    :return: None

    :raises ExitCodeException: If the client is not initialized with the correct combination of arguments
    """
    if access_token:
        print("Access token provided. Attempting to authenticate with access token.")
        return

    missing_args = []

    if not consumer_key:
        missing_args.append("consumer_key")
    if not consumer_secret:
        missing_args.append("consumer_secret")
    if not domain:
        missing_args.append("domain")
    if not username:
        missing_args.append("username")
    if not password:
        missing_args.append("password")

    if missing_args:
        raise ExitCodeException(
            f"Missing required arguments: {', '.join(missing_args)}",
            Crm.EXIT_CODE_INVALID_INPUT,
        )
