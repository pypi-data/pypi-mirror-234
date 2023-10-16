import logging
import signal
import sys
import time
import uuid
from urllib.parse import urlparse

from rich.console import Console

from digicloud.sentry import initialize_sentry
from digicloud.utils import get_latest_version_number, compare_versions, is_tty
from digicloud.managers import ConfigManager, Session

logger = logging.getLogger(__name__)

__all__ = [
    'ConfigMiddleware',
    'SignalHandlerMiddleware',
    'VersionCheckMiddleware',
    'SessionMiddleware',
    'RichMiddleware',
    'SentryMiddleware',
]


class BaseMiddleware:
    def __init__(self, app):
        self.app = app

    def before(self, cmd):
        """
        This hook provide control to access the app and the command object
        before command execution
        """

    def after(self, cmd, result, err):
        """
        This hook provide control to access the app, command, result,
        and error if available after command execution
        """


class SignalHandlerMiddleware(BaseMiddleware):
    def before(self, cmd):
        signal.signal(signal.SIGINT, self.interrupt_handler)
        logger.debug("Signal handler registered")

    def interrupt_handler(self, sig, frame):
        print('\nOperation canceled!!')
        sys.exit(130)


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, app):
        self.config = None
        super(ConfigMiddleware, self).__init__(app)

    def before(self, cmd):
        self.config = self.app.config = ConfigManager(self.app.LOG)
        self.config['options'] = {}

    def after(self, cmd, result, err):
        self.config.save()
        logger.debug("Configuration saved")


class VersionCheckMiddleware(BaseMiddleware):

    def __init__(self, app):
        self.session = None
        super(VersionCheckMiddleware, self).__init__(app)

    def before(self, cmd):
        self._check_version()

    def _set_last_run(self):
        self.app.config['last_version_check_time'] = int(time.time())

    def _get_last_run(self):
        now = int(time.time())
        if 'last_version_check_time' in self.app.config:
            return now - int(self.app.config['last_version_check_time'])
        return 0

    def _check_version(self):
        try:
            latest_version = get_latest_version_number('digicloud')
            current_version = self.app.current_version
            diff = compare_versions(latest_version, current_version)
            if diff['major']:
                self._important_version_change(current_version, latest_version)
            if diff['minor'] or diff['patch']:
                self._regular_version_change(current_version, latest_version)
        except Exception as exp:
            if getattr(self.app.options, "debug", False):
                raise exp

    def _important_version_change(self, current_version, latest_version):
        self.app.console.print(
            "[red bold]You current version is {} which is no longer "
            "work properly due to recent changes.\n[/red bold]"
            "Please update to latest version via "
            "[blue bold]pip install digicloud -U[blue bold]".format(
                current_version
            )
        )
        sys.exit(1)

    def _regular_version_change(self, current_version, latest_version):
        last_run = self._get_last_run()
        should_warn = (last_run == 0 or last_run > 3600) and is_tty()
        if should_warn:
            self.app.console.print(
                "[red bold]A new Digicloud "
                "version ({}) is available.[red bold]".format(
                    latest_version
                )
            )
        self._set_last_run()


class SessionMiddleware(BaseMiddleware):
    def __init__(self, app):
        self.session = getattr(app, 'session', None)
        super(SessionMiddleware, self).__init__(app)

    def before(self, cmd):
        config = self.app.config
        base_url = config['BASE_URL']
        session = config.get('SESSION', Session(base_url))
        session.user_agent = "PYTHON-CLI_{}".format(self.app.current_version)
        self.app.session = self.session = session
        session.setup(config)

    def after(self, cmd, result, err):
        self.app.config['SESSION'] = self.session


class RichMiddleware(BaseMiddleware):
    def before(self, cmd):
        self.app.console = Console()


class SentryMiddleware(BaseMiddleware):

    def before(self, cmd):
        if "client_id" not in self.app.config:
            self.app.console.print(
                "[yellow bold]"
                "Digicloud will collect errors and related context anonymously.\n"
                "[/yellow bold]"
                "To disable it you can easily run: "
                "[blue bold]digicloud config --set collect_error_info=0[/blue bold]"
                ""
            )
            self.app.config['client_id'] = uuid.uuid4().hex
        client_id = self.app.config['client_id']
        base_url = self.app.config['BASE_URL']
        region = self.app.config['AUTH_HEADERS'].get('Digicloud-Region', "")
        namespace = self.app.config['AUTH_HEADERS'].get('Digicloud-Namespace', "")
        initialize_sentry(
            self.app.current_version,
            urlparse(base_url).netloc,
            region=region,
            namespace=namespace,
            client_id=client_id
        )
