"""
    Main app components definition.
"""
import sys

from cmd2 import Cmd2ArgparseError
from pkg_resources import get_distribution
from cliff.commandmanager import CommandManager
from sentry_sdk import capture_message

from digicloud.cli.app import BaseApp
from digicloud.error_handlers import ErrorHandler
from .middlewares import (
    ConfigMiddleware,
    SessionMiddleware,
    SignalHandlerMiddleware,
    VersionCheckMiddleware,
    RichMiddleware,
    SentryMiddleware
)


class DigicloudApp(BaseApp):
    def __init__(self):
        command_manager = CommandManager('digicloud.cli')
        self.current_version = get_distribution('digicloud').version
        super(DigicloudApp, self).__init__(
            description="Digicloud CLI",
            version=self.current_version,
            command_manager=command_manager,
            deferred_help=True
        )
        self.middlewares = [
            SignalHandlerMiddleware(self),
            ConfigMiddleware(self),
            SessionMiddleware(self),
            RichMiddleware(self),
            VersionCheckMiddleware(self),
            SentryMiddleware(self),
        ]
        self.error_handler = ErrorHandler(self)

    def clean_up(self, cmd, result, err):
        super(DigicloudApp, self).clean_up(cmd, result, err)
        if isinstance(err, Cmd2ArgparseError):
            capture_message('invalid-command: {}'.format(' '.join(sys.argv[1:])))


def main(argv=None):
    """Initialize main ``cliff.app.App`` instance and run.

    Cliff look for this function as a console script entry point.
    """
    if not argv:
        argv = sys.argv[1:]
    if len(argv) == 0:  # Disable interactive mode
        argv = ['--help']  # display --help instead of interactive mode
    return DigicloudApp().run(argv)


if __name__ == '__main__':
    sys.exit(main())
