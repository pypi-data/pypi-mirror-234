import abc

from cliff.lister import Lister as CliffLister
from cliff.show import ShowOne as CliffShowOne
from cliff.command import Command as CliffCommand
from requests import HTTPError
from rich.console import Console

from ..error_handlers import CLIError
from ..utils import tabulate


class ErrorHandlingMixin:
    def run(self, parsed_args):
        try:
            return super(ErrorHandlingMixin, self).run(parsed_args)
        except Exception as exp:
            cli_error = self.on_exception(parsed_args, exp)
            self.represent_error(cli_error)
            return cli_error.return_code

    def on_exception(self, parsed_args, exp):
        try:
            if isinstance(exp, CLIError):
                return exp
            if isinstance(exp, HTTPError):
                result = self._handle_http_error(parsed_args, exp.response)
                if result:
                    return result
            return self.app.error_handler.handle(exp)
        except Exception:
            raise exp

    def represent_error(self, cli_error: CLIError):
        c = self.app.console
        assert isinstance(c, Console)
        c.print("Unable to run your command: ", style="red")
        for error in cli_error.errors:
            c.print("\t* {}".format(error['msg']))
            if 'hint' in error:
                c.print("\t  Hint: {}".format(error['hint']), style='yellow')

    def _handle_http_error(self, parsed_args, response):
        error_handler = getattr(self, "_on_{}".format(response.status_code), None)
        if callable(error_handler):
            return error_handler(parsed_args, response)


class SchemaMixin:
    schema = None

    def get_data(self, parsed_args):
        raise NotImplementedError()

    def take_action(self, parsed_args):
        data = self.get_data(parsed_args)
        if self.schema:
            return tabulate(self.schema.dump(data))
        return tabulate(data)


class Lister(ErrorHandlingMixin, SchemaMixin, CliffLister):

    @property
    def formatter_namespace(self):
        return 'digicloud.formatters.list'

    @property
    def formatter_default(self):
        return "rich"

    @abc.abstractmethod
    def get_data(self, parsed_args):
        raise NotImplementedError()


class ShowOne(ErrorHandlingMixin, SchemaMixin, CliffShowOne):
    @property
    def formatter_namespace(self):
        return 'digicloud.formatters.details'

    @property
    def formatter_default(self):
        return "rich"

    @abc.abstractmethod
    def get_data(self, parsed_args):
        raise NotImplementedError()


class Command(ErrorHandlingMixin, CliffCommand):
    pass
