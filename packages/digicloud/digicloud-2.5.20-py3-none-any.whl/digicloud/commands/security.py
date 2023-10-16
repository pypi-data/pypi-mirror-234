"""
    DigiCloud Security Service.
"""

from .base import Lister, ShowOne, Command
from .. import schemas


class ListFirewall(Lister):
    """List Firewalls."""
    schema = schemas.FirewallList(many=True)

    def get_data(self, parsed_args):
        data = self.app.session.get('/security-groups')

        return data


class ShowFirewall(ShowOne):
    """Show Firewall details."""
    schema = schemas.FirewallDetails()

    def get_parser(self, prog_name):
        parser = super(ShowFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'firewall',
            metavar='<firewall>',
            help='firewall name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/security-groups/%s' % parsed_args.firewall
        data = self.app.session.get(uri)

        return data


class CreateFirewall(ShowOne):
    """Create Firewall."""
    schema = schemas.FirewallDetails()

    def get_parser(self, prog_name):
        parser = super(CreateFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Firewall name'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            default="",
            required=False,
            help='Firewall description'
        )

        return parser

    def get_data(self, parsed_args):
        payload = {'name': parsed_args.name, 'description': parsed_args.description}
        data = self.app.session.post('/security-groups', payload)

        return data


class DeleteFirewall(Command):
    """Delete Firewall."""

    def get_parser(self, prog_name):
        parser = super(DeleteFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'firewall',
            metavar='<firewall>',
            help='Firewall name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/security-groups/%s' % parsed_args.firewall
        self.app.session.delete(uri)


class UpdateFirewall(Command):
    """Update Firewall."""

    def get_parser(self, prog_name):
        parser = super(UpdateFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'firewall',
            metavar='<firewall>',
            help='Firewall name or ID'
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            required=False,
            help='Firewall name'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            required=False,
            help='Firewall description'
        )
        return parser

    def take_action(self, parsed_args):
        uri = f'/security-groups/{parsed_args.firewall}'
        payload = {}
        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.description:
            payload['description'] = parsed_args.description
        self.app.session.patch(uri, payload)


class ListFirewallRule(Lister):
    """List Firewall Rules."""
    schema = schemas.FirewallRuleList(many=True)

    def get_parser(self, prog_name):
        parser = super(ListFirewallRule, self).get_parser(prog_name)
        parser.add_argument(
            'firewall',
            metavar='<firewall>',
            help='Firewall rule ID',
        )
        return parser

    def get_data(self, parsed_args):
        data = self.app.session.get(
            '/security-groups/{}/rules'.format(parsed_args.firewall)
        )
        return data


class ShowFirewallRule(ShowOne):
    """Show Firewall rule details."""
    schema = schemas.FirewallRuleDetails()

    def get_parser(self, prog_name):
        parser = super(ShowFirewallRule, self).get_parser(prog_name)
        parser.add_argument(
            'firewall_rule',
            metavar='<firewall_rule>',
            help='Firewall rule ID',
        )
        parser.add_argument(
            '--firewall',
            required=True,
            metavar='<firewall>',
            help='Firewall name or ID'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/security-groups/{}/rules/{}'.format(
            parsed_args.firewall,
            parsed_args.firewall_rule
        )
        data = self.app.session.get(uri)
        return data


class CreateFirewallRule(ShowOne):
    """Create Firewall Rule."""
    schema = schemas.FirewallRuleDetails()

    def get_parser(self, prog_name):
        parser = super(CreateFirewallRule, self).get_parser(prog_name)
        parser.add_argument(
            'firewall',
            metavar='<firewall>',
            help='Firewall name or ID'
        )
        parser.add_argument(
            '--direction',
            required=True,
            metavar='<direction>',
            help='Direction'
        )
        parser.add_argument(
            '--ethertype',
            default='IPv4',
            metavar='<ethertype>',
            help='IP version',
            choices=['IPv4', 'IPv6']
        )
        parser.add_argument(
            '--port-range-min',
            metavar='<port_range_min>',
            help='Minimum of port range'
        )
        parser.add_argument(
            '--port-range-max',
            metavar='<port_range_max>',
            help='Maximum of port range'
        )
        parser.add_argument(
            '--protocol',
            required=True,
            metavar='<protocol>',
            help="Protocol"
        )
        parser.add_argument(
            '--remote-ip-prefix',
            required=False,
            metavar='<remote_ip_prefix>',
            help='remote IP prefix matched by this Firewall rule'
        )
        return parser

    def get_data(self, parsed_args):
        args = [
            'direction', 'ethertype', 'port_range_min',
            'port_range_max', 'protocol', 'remote_ip_prefix',
        ]
        payload = {arg: getattr(parsed_args, arg) for arg in args
                   if getattr(parsed_args, arg) is not None}
        uri = '/security-groups/%s/rules' % parsed_args.firewall
        data = self.app.session.post(uri, payload)

        return data


class DeleteFirewallRule(Command):
    """Delete Firewall Rule."""

    def get_parser(self, prog_name):
        parser = super(DeleteFirewallRule, self).get_parser(prog_name)
        parser.add_argument(
            'firewall_rule',
            metavar='<firewall_rule>',
            help='Firewall rule ID'
        )
        parser.add_argument(
            '--firewall',
            required=True,
            metavar='<firewall>',
            help='Firewall name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/security-groups/{}/rules/{}'.format(parsed_args.firewall,
                                                    parsed_args.firewall_rule)
        self.app.session.delete(uri)
