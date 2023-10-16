from os import path

from rich.markdown import Markdown

import digicloud
from digicloud.commands.base import Command
from digicloud.documentations import DocumentationContainer


class Explain(Command):
    """Digicloud manual for different topics"""

    def get_parser(self, prog_name):
        parser = super(Explain, self).get_parser(prog_name)
        parser.add_argument(
            'topic',
            metavar='<topic>',
            nargs="?",
            default=None,
            help='Topic to explain'
        )
        return parser

    def take_action(self, parsed_args):
        documentation = DocumentationContainer(
            path.join(path.dirname(digicloud.__file__), 'documentations')
        )
        if parsed_args.topic is None:
            self._display_list_of_topics(documentation.list())
            return
        try:

            self.app.console.print(
                Markdown(documentation.get(parsed_args.topic))
            )
        except FileNotFoundError:
            self.app.console.print(
                (
                    "[red bold]There is not documentation "
                    "available for '{}'.[/red bold]"
                ).format(
                    parsed_args.topic
                )
            )
            self._display_list_of_topics(documentation.list())

    def _display_list_of_topics(self, topics):
        self.app.console.print(
            "[green bold]The following "
            "topics are available:[/green bold]"
        )
        for topic in topics:
            self.app.console.print("* {}".format(topic))
