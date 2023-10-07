from bodosdk.exc import (
    ConflictException,
    ResourceNotFound,
    ServiceUnavailable,
    UnknownError,
    ValidationError,
)


# throws appropriate error with accurate message if the api response code contains a error code
# simply returns if the api response code is success(200/201)
def handle_job_run_api_error(resp):
    status_code = resp.status_code
    if str(status_code).startswith("2"):
        return
    print_message = False
    error_message = None
    if "message" in resp.json():
        print_message = True
        error_message = resp.json()["message"]
        error_message += f" status code: {str(status_code)}"

    if str(status_code).startswith("5"):
        raise ServiceUnavailable(
            error_message
            if print_message
            else f"Could not Complete Request: {str(status_code)}"
        )
    if status_code == 404:
        raise ResourceNotFound(
            error_message
            if print_message
            else f"Resource Not Found: {str(status_code)}"
        )
    if status_code == 409:
        raise ConflictException(
            error_message
            if print_message
            else f"Unable to validate request: {str(status_code)}"
        )

    if status_code == 400:
        raise ValidationError(
            error_message
            if print_message
            else f"Unable to validate request: {str(status_code)}"
        )
    # if none of these work
    raise UnknownError(
        error_message
        if print_message
        else f"Encountered Unexpected Error: {str(status_code)}"
    )
