"""
    DigiCloud load balancer Service.
"""
import ipaddress
from ..utils import is_tty
from .base import Lister, ShowOne, Command
from .. import schemas
from ..error_handlers import CLIError
from rich.prompt import Confirm


################################################
# Load Balancer                                #
################################################
class ListLoadBalancer(Lister):
    """List load balancers"""
    schema = schemas.LoadBalancerList(many=True)

    def get_data(self, parsed_args):
        load_balancer_list = self.app.session.get('/load-balancers')
        return load_balancer_list


class ShowLoadBalancer(ShowOne):
    """Show load balancer details."""
    schema = schemas.LoadBalancerDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/load-balancers/%s' % parsed_args.load_balancer
        load_balancer = self.app.session.get(uri)
        return load_balancer


class DeleteLoadBalancer(Command):
    """Delete load balancer."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )

        return parser

    def take_action(self, parsed_args):
        self.confirm_deletion(parsed_args)
        uri = '/load-balancers/%s' % parsed_args.load_balancer
        self.app.session.delete(uri)

    def confirm_deletion(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            user_response = Confirm.ask(
                "You're about to delete loadbalancer [red bold]{}[/red bold]. "
                "Are you sure?".format(
                    parsed_args.load_balancer
                ), default=False
            )
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write(
                "Unable to perform 'loadbalancer delete' operation in non-interactive mode,"
                " without '--i-am-sure' switch\n")
            return False


class UpdateLoadBalancer(ShowOne):
    """Update load balancer."""
    schema = schemas.LoadBalancerDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--name',
            metavar='<Name>',
            help='New name for load balancer.'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Load balancer description.',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/load-balancers/%s' % parsed_args.load_balancer
        payload = {}
        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.description:
            payload['description'] = parsed_args.description

        if not payload:
            raise CLIError([dict(
                msg="At least one of "
                    " --name or"
                    " --description is necessary"
            )])
        load_balancer = self.app.session.patch(uri, payload)
        return load_balancer


class CreateLoadBalancer(ShowOne):
    """Create Load Balancer"""
    schema = schemas.LoadBalancerDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<Name>',
            help='New name for load balancer.',
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Load balancer description.',
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.name,
        }
        if parsed_args.description:
            payload['description'] = parsed_args.description
        load_balancer = self.app.session.post('/load-balancers', payload)
        return load_balancer


################################################
# Backend                                      #
################################################


class CreateBackend(ShowOne):
    """Create Load balancer Backend.

    Each backend may contain multiple backend members.
    """
    schema = schemas.BackendDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--algorithm',
            metavar='<algorithm>',
            help='Backend algorithm one of "round_robin" or "source_ip"',
            choices=['round_robin', 'source_ip'],
            required=True
        )
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            'algorithm': parsed_args.algorithm,
        }
        uri = '/load-balancers/%s/backends' % parsed_args.load_balancer
        backend = self.app.session.post(uri, payload)
        return backend


class DeleteBackend(Command):
    """Delete a LoadBalancer backend."""
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--backend-id',
            metavar='<backend_id>',
            required=True,
            help='The backend identifier to be deleted.',
        )
        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )

        return parser

    def take_action(self, parsed_args):
        self.confirm_deletion(parsed_args)
        uri = '/load-balancers/%s/backends/%s' % (
            parsed_args.load_balancer,
            parsed_args.backend_id,
        )
        self.app.session.delete(uri)

    def confirm_deletion(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            user_response = Confirm.ask(
                "You're about to delete backend "
                " [red bold]{}[/red bold] "
                "including the members and the health check. "
                "Are you sure?".format(
                    parsed_args.backend_id
                ), default=False
            )
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write(
                "Unable to perform 'backend delete' operation in non-interactive mode,"
                " without '--i-am-sure' switch\n")
            return False


class ListBackend(Lister):
    """Lists a load balancer backends."""
    schema = schemas.BackendDetail(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/load-balancers/%s/backends' % parsed_args.load_balancer
        backends = self.app.session.get(uri)
        return backends


################################################
# Frontend                                     #
################################################


class CreateFrontend(ShowOne):
    """Create Load balancer Frontend."""
    schema = schemas.FrontendDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='The TCP port which frontend listens to.',
            type=int,
            required=True,
        )
        parser.add_argument(
            '--timeout-client-data',
            metavar='<timeout_client_data>',
            help='Client inactivity timeout in milliseconds.',
            type=int,
            required=False,
        )
        parser.add_argument(
            '--timeout-tcp-inspect',
            metavar='<timeout_tcp_inspect>',
            help='Time, in milliseconds, '
                 'to wait for additional TCP packets for content inspection.',
            type=int,
            required=False,
        )
        parser.add_argument(
            '--timeout-member-connect',
            metavar='<timeout_member_connect>',
            help='Backend member connection timeout in milliseconds.',
            type=int,
            required=False,
        )
        parser.add_argument(
            '--timeout_member_data',
            metavar='<timeout_member_data>',
            help='Backend member inactivity timeout in milliseconds.',
            type=int,
            required=False,
        )
        parser.add_argument(
            '--connection-limit',
            metavar='<connection_limit>',
            help='The maximum number of connections permitted for this Frontend.'
                 'Value "-1" represents infinite connections.',
            type=int,
            required=True,
        )
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--default-backend',
            metavar='<default_backend>',
            required=False,
            help='default backend which the frontend will forward requests to.',
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            'port': parsed_args.port,
            'default_backend_id': parsed_args.default_backend,
            "connection_limit": parsed_args.connection_limit,
        }
        if parsed_args.timeout_client_data:
            payload["timeout_client_data"] = parsed_args.timeout_client_data
        if parsed_args.timeout_tcp_inspect:
            payload["timeout_tcp_inspect"] = parsed_args.timeout_tcp_inspect
        if parsed_args.timeout_member_connect:
            payload["timeout_member_connect"] = parsed_args.timeout_member_connect
        if parsed_args.timeout_member_data:
            payload["timeout_member_data"] = parsed_args.timeout_member_data

        uri = '/load-balancers/%s/frontends' % parsed_args.load_balancer
        frontend = self.app.session.post(uri, payload)
        return frontend


class SetFrontendDefaultBackend(ShowOne):
    """Set a new default backend for the specified frontend."""
    schema = schemas.FrontendDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--frontend-id',
            metavar='<frontend_id>',
            required=True,
            help='The frontend identifier to be updated.',
        )
        parser.add_argument(
            '--default-backend',
            metavar='<default_backend>',
            required=True,
            help='default backend which the frontend will forward requests to.',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/load-balancers/{}/frontends/{}'.format(
            parsed_args.load_balancer, parsed_args.frontend_id
        )
        payload = {"default_backend_id": parsed_args.default_backend}
        frontend = self.app.session.patch(uri, payload)
        return frontend


class DeleteFrontendDefaultBackend(ShowOne):
    """Delete default backend for the specified frontend."""
    schema = schemas.FrontendDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--frontend-id',
            metavar='<frontend_id>',
            required=True,
            help='The frontend identifier to be updated.',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/load-balancers/{}/frontends/{}'.format(
            parsed_args.load_balancer, parsed_args.frontend_id
        )
        payload = {"default_backend_id": None}
        frontend = self.app.session.patch(uri, payload)
        return frontend


class DeleteFrontend(Command):
    """Delete a LoadBalancer frontend."""
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--frontend-id',
            metavar='<frontend_id>',
            required=True,
            help='The frontend identifier to be deleted.',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/load-balancers/%s/frontends/%s' % (
            parsed_args.load_balancer,
            parsed_args.frontend_id,
        )
        self.app.session.delete(uri)


class ListFrontend(Lister):
    """Lists a load balancer frontends."""
    schema = schemas.FrontendDetail(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/load-balancers/%s/frontends' % parsed_args.load_balancer
        frontends = self.app.session.get(uri)
        return frontends

################################################
# Health Check                                 #
################################################


class ListHealthCheck(Lister):
    """Lists backend Health check."""
    schema = schemas.HealthCheckDetail(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--backend-id',
            metavar='<backend_id>',
            required=True,
            help='The backend identifier.',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/load-balancers/%s/backends/%s/health-checks' % (
            parsed_args.load_balancer,
            parsed_args.backend_id,
        )
        health_checks = self.app.session.get(uri)
        return health_checks


class DeleteHealthCheck(Command):
    """Delete Health Check."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--backend-id',
            metavar='<backend_id>',
            required=True,
            help='The backend identifier.',
        )
        parser.add_argument(
            '--health-check-id',
            metavar='<health_check_id>',
            required=True,
            help='The health check identifier to be deleted.',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/load-balancers/%s/backends/%s/health-checks/%s' % (
            parsed_args.load_balancer,
            parsed_args.backend_id,
            parsed_args.health_check_id,
        )
        self.app.session.delete(uri)


class CreateHealthCheck(ShowOne):
    """Create Health Check"""
    schema = schemas.HealthCheckDetail()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--backend-id',
            metavar='<backend_id>',
            required=True,
            help='The backend identifier.',
        )
        parser.add_argument(
            '--name',
            metavar='<Name>',
            help='Human readable name.',
            required=True,
        )
        parser.add_argument(
            '--delay',
            metavar='<delay>',
            help='Health Check delay.',
            type=int,
            required=True,
        )
        parser.add_argument(
            '--timeout',
            metavar='<timeout>',
            help='Health Check timeout.',
            type=int,
            required=True
        )
        parser.add_argument(
            '--max-retries',
            metavar='<max-retries>',
            help='Health Check max retries.',
            type=int,
            required=True,
        )
        parser.add_argument(
            '--max-retries-down',
            metavar='<max-retries-down>',
            help='The number of allowed check failures before '
                 'changing the operating status of the member to ERROR. '
                 'A valid value is from 1 to 10.',
            type=int,
            required=True,
        )
        return parser

    def _check_arg_validity(self, parsed_args):
        rules = [
            (
                parsed_args.delay < parsed_args.timeout,
                "timeout must be lower than and equal to delay",
            ),
        ]
        errors = []
        for is_invalid, err_msg in rules:
            if is_invalid:
                errors.append(dict(msg=err_msg))
        if errors:
            raise CLIError(errors)

    def get_data(self, parsed_args):
        self._check_arg_validity(parsed_args)
        uri = '/load-balancers/%s/backends/%s/health-checks' % (
            parsed_args.load_balancer,
            parsed_args.backend_id,
        )
        payload = {
            'name': parsed_args.name,
            'delay': parsed_args.delay,
            'timeout': parsed_args.timeout,
            'max_retries': parsed_args.max_retries,
            'max_retries_down': parsed_args.max_retries_down,
        }
        health_check = self.app.session.post(uri, payload)
        return health_check


################################################
# Backend Member                               #
################################################

class ListBackendMember(Lister):
    """Lists backend members."""
    schema = schemas.BackendMemberDetail(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--backend-id',
            metavar='<backend_id>',
            required=True,
            help='The backend identifier.',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/load-balancers/%s/backends/%s/members' % (
            parsed_args.load_balancer,
            parsed_args.backend_id,
        )
        members = self.app.session.get(uri)
        return members


class DeleteBackendMember(Command):
    """Delete backend member."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--backend-id',
            metavar='<backend_id>',
            required=True,
            help='The backend identifier.',
        )
        parser.add_argument(
            '--member-id',
            metavar='<member_id>',
            help='The member identifier to be deleted.',
            required=True
        )
        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )
        return parser

    def take_action(self, parsed_args):
        self.confirm_deletion(parsed_args)
        uri = '/load-balancers/%s/backends/%s/members/%s' % (
            parsed_args.load_balancer,
            parsed_args.backend_id,
            parsed_args.member_id,
        )
        self.app.session.delete(uri)

    def confirm_deletion(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            user_response = Confirm.ask(
                "You're about to delete backend member"
                " [red bold]{}[/red bold] . "
                "Are you sure?".format(
                    parsed_args.member_id
                ), default=False
            )
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write(
                "Unable to perform 'backend member delete' operation in non-interactive mode,"
                " without '--i-am-sure' switch\n")
            return False


class AddBackendMember(Lister):
    """Add Backend member"""
    schema = schemas.BackendMemberDetail(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'load_balancer',
            metavar='<load-balancer>',
            help='Load Balancer name or ID',
        )
        parser.add_argument(
            '--backend-id',
            metavar='<backend_id>',
            required=True,
            help='The backend identifier.',
        )
        parser.add_argument(
            '--ip-address',
            metavar='<ip-address>',
            help='Backend member ip address.',
            required=True,
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Backend member port.',
            type=int,
            required=True,
        )
        return parser

    def _check_ip_address(self, value):
        try:
            ipaddress.IPv4Address(value)
            return False
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            return True

    def _check_arg_validity(self, parsed_args):
        rules = [
            (
                parsed_args.port and (parsed_args.port < 1 or parsed_args.port > 65535),
                "port should be in range 1 - 65535",
            ),
            (
                self._check_ip_address(parsed_args.ip_address),
                "Not a valid ipv4 address"
            )
        ]
        errors = []
        for is_invalid, err_msg in rules:
            if is_invalid:
                errors.append(dict(msg=err_msg))
        if errors:
            raise CLIError(errors)

    def get_data(self, parsed_args):
        self._check_arg_validity(parsed_args)
        uri = '/load-balancers/%s/backends/%s/members' % (
            parsed_args.load_balancer,
            parsed_args.backend_id,
        )
        payload = [{
            'ip_address': parsed_args.ip_address,
            'port': parsed_args.port,
        }]
        backend_member = self.app.session.post(uri, payload)
        return backend_member
