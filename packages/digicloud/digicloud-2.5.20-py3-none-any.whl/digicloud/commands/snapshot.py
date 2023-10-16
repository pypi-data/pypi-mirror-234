from rich.prompt import Confirm

from digicloud import schemas
from .base import Lister, ShowOne, Command
from ..utils import is_tty


class CreateSnapshot(ShowOne):
    """Create snapshot."""
    schema = schemas.SnapshotDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Snapshot name',
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Snapshot description',
            required=False,
        )
        parser.add_argument(
            '--instance',
            required=True,
            metavar='<instance>',
            help='Instance name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        self.app.console.print(
            "[yellow bold]"
            "WARNING: If your instance has any volume larger than 100G,"
            " you won't be able to create an instance from this snapshot."
            " Please contact support for help.\n"
            "[/yellow bold]"
        )
        uri = '/snapshots'
        payload = {
            'name': parsed_args.name,
            'instance': parsed_args.instance,
        }
        if parsed_args.description:
            payload['description'] = parsed_args.description
        data = self.app.session.post(uri, payload)
        return data


class ListSnapshot(Lister):
    """List snapshots."""
    schema = schemas.SnapshotList(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        return parser

    def get_data(self, parsed_args):
        uri = '/snapshots'
        data = self.app.session.get(uri)
        return data


class ShowSnapshot(ShowOne):
    """Show snapshot details."""
    schema = schemas.SnapshotDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'snapshot',
            metavar='<snapshot>',
            help='Snapshot name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/snapshots/%s' % parsed_args.snapshot
        data = self.app.session.get(uri)
        return data


class DeleteSnapshot(Command):
    """Delete snapshot."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'snapshot',
            metavar='<snapshot>',
            help='snapshot name or ID'
        )
        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )
        return parser

    def take_action(self, parsed_args):
        if not self.confirm(parsed_args):
            return
        uri = '/snapshots/%s' % parsed_args.snapshot
        self.app.session.delete(uri)

    def confirm(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            snapshot = self.app.session.get(
                '/snapshots/%s' % parsed_args.snapshot
            )
            user_response = Confirm.ask(
                "You're about to delete a snapshot named "
                "[red bold]{}[/red bold]. "
                "Are you sure?".format(
                    snapshot['name'],
                ))
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write(
                "Unable to perform 'delete snapshot' operation in "
                "non-interactive mode, without '--i-am-sure' switch\n"
            )
            return False


class UpdateSnapshot(ShowOne):
    """Update snapshot name or description."""
    schema = schemas.SnapshotDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'snapshot',
            metavar='<snapshot>',
            help='Snapshot name or ID',
        )
        parser.add_argument(
            '--description',
            metavar='<new_description>',
            help='Snapshot new description',
            required=False,
        )
        parser.add_argument(
            '--name',
            metavar='<new_name>',
            help='Snapshot new name',
            required=False,
        )
        return parser

    def get_data(self, parsed_args):
        uri = f'/snapshots/{parsed_args.snapshot}'

        payload = {}
        if parsed_args.name:
            payload["name"] = parsed_args.name

        if parsed_args.description:
            payload["description"] = parsed_args.description

        data = self.app.session.patch(uri, payload)
        return data
