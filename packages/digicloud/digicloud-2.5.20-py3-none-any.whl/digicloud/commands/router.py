"""
    DigiCloud Router Service.
"""

from digicloud import schemas
from .base import Lister, ShowOne, Command
from ..error_handlers import CLIError


def enrich_router_interface_details(session, *routers):
    subnets = {
        subnet['id']: subnet['name']
        for subnet in session.get('/subnets')
    }
    networks = {
        network['id']: network['name']
        for network in session.get('/networks')
    }

    for router in routers:
        router['network_name'] = networks.get(router['network_id'], "N/A")
        router['subnet_name'] = subnets.get(router['subnet_id'], "N/A")


class ListRouter(Lister):
    """List Routers."""
    schema = schemas.RouterList(many=True)

    def get_data(self, parsed_args):
        data = self.app.session.get('/routers')

        return data


class ShowRouter(ShowOne):
    """Show Router details."""
    schema = schemas.RouterDetails(many=False)

    def get_parser(self, prog_name):
        parser = super(ShowRouter, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/routers/%s' % parsed_args.router
        data = self.app.session.get(uri)

        return data


class DeleteRouter(Command):
    """Delete router."""

    def get_parser(self, prog_name):
        parser = super(DeleteRouter, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/routers/%s' % parsed_args.router
        self.app.session.delete(uri)


class CreateRouter(ShowOne):
    """Create Router."""
    schema = schemas.RouterDetails(many=False)

    def get_parser(self, prog_name):
        parser = super(CreateRouter, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Router name'
        )
        parser.add_argument(
            '--admin-state',
            metavar='<AdminState>',
            choices=['UP', 'DOWN'],
            type=str.upper,
            help='Set admin state, could be "UP" or "DOWN", default "UP"',
            default='UP',
        )

        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.name,
            'admin_state': parsed_args.admin_state,
        }
        data = self.app.session.post('/routers', payload)
        return data


class ListRouterInterface(Lister):
    """List all router interfaces"""
    schema = schemas.RouterInterfaceList(many=True)

    def get_parser(self, prog_name):
        parser = super(ListRouterInterface, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        return parser

    def get_data(self, parsed_args):
        uri = f'/routers/{parsed_args.router}/interfaces'
        interfaces = self.app.session.get(uri)
        enrich_router_interface_details(self.app.session, *interfaces)
        return interfaces


class ShowRouterInterface(ShowOne):
    """Show router interface."""
    schema = schemas.RouterInterfaceDetails(many=False)

    def get_parser(self, prog_name):
        parser = super(ShowRouterInterface, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        parser.add_argument(
            '--interface-id',
            required=True,
            metavar='<interface_id>',
            help='Interface ID'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/routers/%s/interfaces/%s' % (parsed_args.router, parsed_args.interface_id)
        interface = self.app.session.get(uri)
        enrich_router_interface_details(self.app.session, interface)
        return interface


class AddRouterInterface(ShowOne):
    """Add router interface."""
    schema = schemas.RouterInterfaceDetails(many=False)

    def get_parser(self, prog_name):
        parser = super(AddRouterInterface, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        parser.add_argument(
            '--subnet',
            required=True,
            metavar='<subnet>',
            help='SubnetList name or ID'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/routers/%s/interfaces' % parsed_args.router
        payload = {'subnet': parsed_args.subnet}
        interface = self.app.session.post(uri, payload)
        enrich_router_interface_details(self.app.session, interface)
        return interface


class RemoveRouterInterface(Command):
    """Remove router interface."""
    def get_parser(self, prog_name):
        parser = super(RemoveRouterInterface, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        parser.add_argument(
            '--interface-id',
            required=True,
            metavar='<interface_id>',
            help='Interface ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/routers/%s/interfaces/%s' % (parsed_args.router, parsed_args.interface_id)
        self.app.session.delete(uri)


class AddRouterExternal(ShowOne):
    """Add external network to router."""
    schema = schemas.RouterDetails(many=False)

    def get_parser(self, prog_name):
        parser = super(AddRouterExternal, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/routers/%s' % parsed_args.router
        payload = {'has_gateway': True}
        data = self.app.session.patch(uri, payload)
        return data


class RemoveRouterExternal(ShowOne):
    """Remove external network from router."""
    schema = schemas.RouterDetails(many=False)

    def get_parser(self, prog_name):
        parser = super(RemoveRouterExternal, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/routers/%s' % parsed_args.router
        payload = {'has_gateway': False}
        data = self.app.session.patch(uri, payload)
        return data


class UpdateRouter(ShowOne):
    _description = "Update Router"
    schema = schemas.RouterDetails(many=False)

    def get_parser(self, prog_name):
        parser = super(UpdateRouter, self).get_parser(prog_name)
        group = parser.add_mutually_exclusive_group()
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='New name for the router'
        )
        parser.add_argument(
            '--admin-state',
            metavar='<AdminState>',
            choices=['UP', 'DOWN'],
            type=str.upper,
            help='Set admin state, could be "UP" or "DOWN"'
        )

        group.add_argument(
            '--disable-gateway',
            help='Disconnect router from external network',
            action='store_true'

        )
        group.add_argument(
            '--enable-gateway',
            help='Connect router to external network',
            action='store_true'
        )
        return parser

    def get_data(self, parsed_args):
        payload = {}
        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.disable_gateway:
            payload['has_gateway'] = False
        if parsed_args.enable_gateway:
            payload['has_gateway'] = True
        if parsed_args.admin_state:
            payload['admin_state'] = parsed_args.admin_state
        if len(payload) == 0:
            raise CLIError([dict(
                msg="You need to at least provide one of "
                    "--name, --admin-state, --enable-gateway or --disable-gateway"
            )])
        uri = '/routers/%s' % parsed_args.router
        data = self.app.session.patch(uri, payload)
        return data


class ListRouterStatic(Lister):
    """List router static routes."""

    def get_parser(self, prog_name):
        parser = super(ListRouterStatic, self).get_parser(prog_name)
        parser.add_argument(
            'router_id',
            metavar='<router_id>',
            help='Router ID'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/routers/%s/static-routes' % parsed_args.router_id
        data = self.app.session.get(uri)
        return data


class AddRouterStatic(Lister):
    """Add router static routes."""
    def get_parser(self, prog_name):
        parser = super(AddRouterStatic, self).get_parser(prog_name)
        parser.add_argument(
            'router_id',
            metavar='<router_id>',
            help='Router ID'
        )
        parser.add_argument(
            '--destination',
            metavar='<Network>',
            required=True,
            help='Destination network.'
        )
        parser.add_argument(
            '--nexthop',
            metavar='<IP address>',
            required=True,
            help='Next hop IP address.'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/routers/%s/static-routes' % parsed_args.router_id
        payload = {
            "destination": parsed_args.destination,
            "nexthop": parsed_args.nexthop,

        }
        data = self.app.session.post(uri, payload)
        return data


class DeleteRouterStatic(Lister):
    """Delete static routes."""
    def get_parser(self, prog_name):
        parser = super(DeleteRouterStatic, self).get_parser(prog_name)
        parser.add_argument(
            'router_id',
            metavar='<router_id>',
            help='Router ID'
        )
        parser.add_argument(
            '--destination',
            metavar='<Network>',
            required=True,
            help='Destination network.'
        )
        parser.add_argument(
            '--nexthop',
            metavar='<IP address>',
            required=True,
            help='Next hop IP address.'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/routers/%s/static-routes' % parsed_args.router_id
        payload = {
            "destination": parsed_args.destination,
            "nexthop": parsed_args.nexthop,

        }
        data = self.app.session.delete(uri, payload)
        return data
