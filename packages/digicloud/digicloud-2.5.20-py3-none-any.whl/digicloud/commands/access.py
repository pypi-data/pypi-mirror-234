"""
    DigiCloud Access Service.
"""

from .base import Lister, ShowOne, Command
from .. import schemas


class ListPublicIp(Lister):
    """List public Ips."""
    schema = schemas.PublicIPList(many=True)

    def get_data(self, parsed_args):
        uri = '/public-ips'
        return self.app.session.get(uri)


class ShowPublicIp(ShowOne):
    """Show public Ip details."""
    schema = schemas.PublicIPDetails()

    def get_parser(self, prog_name):
        parser = super(ShowPublicIp, self).get_parser(prog_name)
        parser.add_argument(
            'public_ip',
            metavar='<public_ip>',
            help=('Public IP ID'),
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/public-ips/%s' % parsed_args.public_ip
        return self.app.session.get(uri)


class CreatePublicIp(ShowOne):
    """Create Public Ip."""
    schema = schemas.PublicIPDetails()

    def get_data(self, parsed_args):
        return self.app.session.post('/public-ips', {})


class DeletePublicIp(Command):
    """Delete Public Ip."""

    def get_parser(self, prog_name):
        parser = super(DeletePublicIp, self).get_parser(prog_name)
        parser.add_argument(
            'public_ip',
            metavar='<public_ip>',
            help=('Public IP ID')
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/public-ips/%s' % parsed_args.public_ip
        self.app.session.delete(uri)


class AssociatePublicIp(ShowOne):
    """Associate Public Ip."""
    schema = schemas.PublicIPDetails()

    def get_parser(self, prog_name):
        parser = super(AssociatePublicIp, self).get_parser(prog_name)
        parser.add_argument(
            'public_ip_id',
            metavar='<public_ip_id>',
            help='Public IP ID'
        )
        parser.add_argument(
            '--interface-id',
            metavar='<interface_id>',
            required=True,
            help='Interface ID'
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            'interface_id': parsed_args.interface_id,
        }
        uri = '/public-ips/%s/associate' % parsed_args.public_ip_id
        return self.app.session.post(uri, payload)


class RevokePublicIp(ShowOne):
    """Revoke Public Ip."""
    schema = schemas.PublicIPDetails()

    def get_parser(self, prog_name):
        parser = super(RevokePublicIp, self).get_parser(prog_name)
        parser.add_argument(
            'public_ip_id',
            metavar='<public_ip_id>',
            help='Public IP ID'
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/public-ips/%s/revoke' % parsed_args.public_ip_id
        return self.app.session.post(uri, {})
