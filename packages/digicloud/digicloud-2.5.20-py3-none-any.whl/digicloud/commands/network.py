"""
    DigiCloud Network Service.
"""

from .base import Lister, ShowOne, Command
from .. import schemas
from ..error_handlers import CLIError


def enrich_network_details(session, *networks):
    subnets = {
        subnet['id']: subnet
        for subnet in session.get('/subnets')
    }
    for network_details in networks:
        network_details['subnets'] = [
            {
                "name": subnets[subnet_id]['name'],
                "cidr": subnets[subnet_id]['cidr'],
                "gateway": subnets[subnet_id]['gateway_ip'],
            }
            for subnet_id in network_details['subnets']
        ]


class ListNetwork(Lister):
    """List networks"""
    schema = schemas.NetworkList(many=True)

    def get_data(self, parsed_args):
        networks = self.app.session.get('/networks')
        enrich_network_details(self.app.session, *networks)
        return networks


class ShowNetwork(ShowOne):
    """Show network details."""
    schema = schemas.NetworkDetail()

    def get_parser(self, prog_name):
        parser = super(ShowNetwork, self).get_parser(prog_name)
        parser.add_argument(
            'network',
            metavar='<network>',
            help='Network name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/networks/%s' % parsed_args.network
        network = self.app.session.get(uri)
        enrich_network_details(self.app.session, network)
        return network


class DeleteNetwork(Command):
    """Delete network."""

    def get_parser(self, prog_name):
        parser = super(DeleteNetwork, self).get_parser(prog_name)
        parser.add_argument(
            'network',
            metavar='<network>',
            help='Network name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/networks/%s' % parsed_args.network
        self.app.session.delete(uri)


class UpdateNetwork(ShowOne):
    """Update network."""
    schema = schemas.NetworkDetail()

    def get_parser(self, prog_name):
        parser = super(UpdateNetwork, self).get_parser(prog_name)
        parser.add_argument(
            'network',
            metavar='<network>',
            help='Network ID',
        )
        parser.add_argument(
            '--name',
            metavar='<Name>',
            help='New name for network.'
        )
        parser.add_argument(
            '--description',
            metavar='<Description>',
            help='Description fro network.'
        )
        parser.add_argument(
            '--admin-state',
            metavar='<admin_state>',
            help='New admin state.',
            choices=("UP", "DOWN"),
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/networks/%s' % parsed_args.network
        payload = {}
        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.description:
            payload['description'] = parsed_args.description
        if parsed_args.admin_state:
            payload['admin_state'] = parsed_args.admin_state
        if not payload:
            raise CLIError([dict(
                msg="At least one of --name or --admin-state is necessary"
            )])
        network = self.app.session.patch(uri, payload)
        enrich_network_details(self.app.session, network)
        return network


class CreateNetwork(ShowOne):
    """Create Network"""
    schema = schemas.NetworkDetail()

    def get_parser(self, prog_name):
        parser = super(CreateNetwork, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Network name'
        )
        parser.add_argument(
            '--description',
            metavar='<Description>',
            help='Network description'
        )
        parser.add_argument(
            '--admin-state',
            metavar='<AdminState>',
            choices=("UP", "DOWN"),
            default='UP',
            help='Set admin state, could be "UP" or "DOWN", (default UP).'
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.name,
            'admin_state': parsed_args.admin_state
        }
        if parsed_args.description:
            payload['description'] = parsed_args.description
        network = self.app.session.post('/networks', payload)
        return network
