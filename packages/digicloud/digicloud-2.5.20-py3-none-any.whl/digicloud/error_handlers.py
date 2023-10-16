from requests import HTTPError
from sentry_sdk import capture_exception

from .schemas import ErrorSchema
from .utils import convert_camel_to_snake


class CLIError(Exception):
    def __init__(self, errors, return_code=1):
        self.errors = errors
        self.return_code = return_code


class ErrorHandler:
    def __init__(self, app):
        self.app = app

    def handle(self, exception):
        if getattr(self.app.options, 'debug', False):
            raise exception
        try:
            if isinstance(exception, HTTPError):
                result = self._handle_error_code(exception.response)
                if result:
                    return result
            capture_exception(exception)
            return self.get_unexpected_error()
        except Exception as exp:
            capture_exception(exp)
            return self.get_unexpected_error()

    def _handle_error_code(self, response):
        error = ErrorSchema().load(response.json())
        handler_method = getattr(self, "_on_{}".format(
            convert_camel_to_snake(error["error_code"])
        ), self._on_not_supported_error_code)
        return handler_method(error)

    def _on_not_found(self, error):
        return CLIError([dict(
            msg=error["message"],
            hint="It might be a typo in your object name or ID",
        )])

    def _on_no_unique_match(self, error):
        return CLIError([dict(
            msg=error["message"],
        )])

    def _on_bad_request(self, error):
        return CLIError([dict(
            msg=error["message"],
        )])

    def _on_invalid_json(self, error):
        return CLIError([dict(
            msg=error["message"],
        )])

    def _on_conflict(self, error):
        return CLIError([dict(
            msg=error["message"],
        )])

    def _on_quota_exceeded(self, error):
        cli_errors = []
        for rule in error["rules"]:
            if rule["used"].lower() != "none":
                message = "{message} {description} is {quota} but you used {used}.".format(
                        message=error['message'],
                        description=rule['description'],
                        quota=rule['quota'],
                        used=rule['used'],
                    )
            else:
                message = "{message} {description} is {quota}.".format(
                        message=error['message'],
                        description=rule['description'],
                        quota=rule['quota'],
                    )
            cli_errors.append(
                dict(
                    msg=message,
                    hint="Request more quota.",
                )
            )
        return CLIError(cli_errors)

    def _on_unauthorized(self, error):
        return CLIError([dict(
            msg=error["message"],
            hint="You can login to you account via `digicloud account login`"
                 " or go to https://digicloud.ir for registration",
        )])

    def _on_forbidden(self, error):
        return CLIError([dict(
            msg=error["message"],
            hint="You might not have required permission",
        )])

    def _on_not_supported_error_code(self, error):
        return CLIError([dict(
            msg=error["message"],
        )])

    def _on_validation_error(self, error):
        return CLIError([dict(
            msg="{message} {key}: {value}".format(
                message=error['message'],
                key=key,
                value=value,
            ),
        ) for key, value in error["errors"].items()])

    def _on_missing_http_header(self, error):
        return CLIError([dict(
            msg=error["message"],
        )])

    def _on_invalid_http_header(self, error):
        return CLIError([dict(
            msg=error["message"],
        )])

    def _on_too_many_request(self, error):
        return CLIError([dict(
            msg=error["message"],
        )])

    def _on_method_not_allowed(self, error):
        return CLIError([dict(
            msg=error["message"],
        )])

    def get_unexpected_error(self):
        return CLIError([
            dict(
                msg="An unexpected error happened while running your command.",
                hint="Please run your command with --debug and send the output "
                     "to us via support@digicloud.ir",
            )
        ])
