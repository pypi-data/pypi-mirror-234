"""
    DigiCloud Volume Service.
"""
from rich.prompt import Confirm

from .base import Lister, ShowOne, Command
from digicloud import schemas
from ..error_handlers import CLIError
from ..utils import is_tty


def prepare_volume_details_output(session, volume_details):
    # TODO: Refactor required ( cry for help level)
    if volume_details.get('attached_to'):
        attachment_info = volume_details['attached_to'][0]
        volume_details['attachment_info'] = volume_details['attached_to'][0]
        data = session.get('/instances/%s' % attachment_info['instance_id'])
        attachment_info['instance'] = data['name']
    else:
        attachment_info = {}
    volume_details['attachment_info'] = attachment_info
    return volume_details


class ListVolume(Lister):
    """List volumes."""
    schema = schemas.VolumeList(many=True)

    def get_data(self, parsed_args):
        volumes = self.app.session.get('/volumes')
        for volume in volumes:
            volume_instances = []
            for attachment in volume.get('attached_to', []):
                instance_name = attachment['instance_id']
                volume_instances.append(instance_name)
            volume["attached_to"] = ', '.join(volume_instances)
        return volumes


class ShowVolume(ShowOne):
    """Show volume details."""
    schema = schemas.VolumeDetails()

    def get_parser(self, prog_name):
        parser = super(ShowVolume, self).get_parser(prog_name)
        parser.add_argument(
            'volume',
            metavar='<volume>',
            help='Volume name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/volumes/%s' % parsed_args.volume
        data = self.app.session.get(uri)
        data = prepare_volume_details_output(self.app.session, data)
        return data


class DeleteVolume(Command):
    """Delete volume."""

    def get_parser(self, prog_name):
        parser = super(DeleteVolume, self).get_parser(prog_name)
        parser.add_argument(
            'volume',
            metavar='<volume>',
            help='Volume name or ID'
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
        uri = '/volumes/%s' % parsed_args.volume
        self.app.session.delete(uri)

    def confirm(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            volume = self.app.session.get('/volumes/%s' % parsed_args.volume)
            user_response = Confirm.ask(
                "You're about to delete a volume named "
                "[red bold]{} with {}GB size[/red bold]. "
                "Are you sure?".format(
                    volume['name'],
                    volume['size']
                ))
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write("Unable to perform 'delete volume' operation in non-interactive mode,"
                                  " without '--i-am-sure' switch\n")
            return False


class CreateVolume(ShowOne):
    """Create Volume."""
    schema = schemas.VolumeDetails()

    def get_parser(self, prog_name):
        parser = super(CreateVolume, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Volume name'
        )
        parser.add_argument(
            '--size',
            required=True,
            metavar='<size>',
            help='Volume size'
        )

        parser.add_argument(
            '--type',
            required=True,
            metavar='<type>',
            help='Volume type, could be SSD or ULTRA_DISK',
            choices=['SSD', 'ULTRA_DISK'],
            type=lambda value: str(value).upper().replace("-", "_"),
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Volume description'
        )

        return parser

    def get_data(self, parsed_args):
        volume_type = parsed_args.type.upper()
        payload = {
            'name': parsed_args.name,
            'size': parsed_args.size,
            'volume_type': volume_type
        }
        if parsed_args.description:
            payload['description'] = parsed_args.description

        data = self.app.session.post('/volumes', payload)
        data = prepare_volume_details_output(self.app.session, data)

        return data


class UpdateVolume(ShowOne):
    """Update volume."""
    schema = schemas.VolumeDetails()

    def get_parser(self, prog_name):
        parser = super(UpdateVolume, self).get_parser(prog_name)
        parser.add_argument(
            'volume',
            metavar='<volume>',
            help=('Volume name or ID'),
        )
        parser.add_argument(
            '--name',
            required=False,
            metavar='<name>',
            help='new name for the volume, must be unique',
        )
        parser.add_argument(
            '--description',
            required=False,
            metavar='<description>',
            help='Volume description'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/volumes/%s' % parsed_args.volume
        payload = {}
        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.description:
            payload['description'] = parsed_args.description
        if not payload:
            raise CLIError([dict(
                msg="At least one of --name or --description is necessary"
            )])
        data = self.app.session.patch(uri, payload)
        data = prepare_volume_details_output(self.app.session, data)

        return data


class AttachVolume(ShowOne):
    """Attach instance volume."""
    schema = schemas.InstanceVolume()

    def get_parser(self, prog_name):
        parser = super(AttachVolume, self).get_parser(prog_name)
        parser.add_argument(
            'volume',
            metavar='<volume>',
            help='Volume name or ID'
        )
        parser.add_argument(
            '--instance',
            required=True,
            metavar='<instance>',
            help='Instance name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s/volumes' % parsed_args.instance
        payload = {'id': parsed_args.volume}

        data = self.app.session.post(uri, payload)

        return data


class DetachVolume(Command):
    """Detach instance volume."""

    def get_parser(self, prog_name):
        parser = super(DetachVolume, self).get_parser(prog_name)
        parser.add_argument(
            'volume',
            metavar='<volume>',
            help='Volume name or ID'
        )
        parser.add_argument(
            '--instance',
            required=True,
            metavar='<instance>',
            help='Instance name or ID'
        )

        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/volumes/%s' % (parsed_args.instance, parsed_args.volume)
        self.app.session.delete(uri)
