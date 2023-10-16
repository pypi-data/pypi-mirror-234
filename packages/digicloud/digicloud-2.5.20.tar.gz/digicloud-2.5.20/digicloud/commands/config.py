"""
    Authentication to digicloud API.
"""

from digicloud.commands.base import Command
from ..cli import parseractions
from ..error_handlers import CLIError


class Config(Command):
    """Managing Digicloud configurations"""

    def get_parser(self, prog_name):
        parser = super(Config, self).get_parser(prog_name)

        parser.add_argument(
            '--set',
            metavar='collect_error_info=<collect_error_info>',
            dest='configs',
            action=parseractions.MultiKeyValueAction,
            optional_keys=['collect_error_info', ],
            help='Set CLI configuration, for example --set collect_error_info=1/0'
        )

        return parser

    def take_action(self, parsed_args):
        if parsed_args.configs is None:
            self.show_configs()
            return
        if len(parsed_args.configs) > 1:
            raise CLIError([dict(msg="You only need to specify --set once")])
        app_config = self.app.config
        if not app_config.get('options'):
            app_config['options'] = {}
        options = app_config['options']
        for key, value in parsed_args.configs[0].items():
            self.app.console.print(
                "Setting [bold blue]%s[/bold blue] to [bold green]%s[/bold green] " % (
                    key, value
                )
            )
            options[key] = value
        app_config.save()

    def show_configs(self):
        app_config = self.app.config
        if not app_config.get('options'):
            app_config['options'] = {}
        options = app_config['options']
        if not options:
            self.app.console.print("You haven't set any configuration parameter")
            return
        for key, value in options.items():
            self.app.console.print(
                "[bold blue]%s[/bold blue]: [bold green]%s[/bold green]" % (
                    key, value
                )
            )
