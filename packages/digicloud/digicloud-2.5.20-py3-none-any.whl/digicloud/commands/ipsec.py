"""
    DigiCloud IpSec Service.
"""
from rich.prompt import Confirm

from .base import Lister, ShowOne, Command
from ..cli import parseractions
from digicloud import schemas
from ..utils import is_tty


class ListIpSec(Lister):
    """List ipsecs."""
    schema = schemas.IPSecPolicySchema(many=True)

    def get_data(self, parsed_args):
        objects = self.app.session.get('/ipsec-policies')
        return objects


class ShowIpSec(ShowOne):
    """Show ipsec details."""
    schema = schemas.IPSecPolicySchema()

    def get_parser(self, prog_name):
        parser = super(ShowIpSec, self).get_parser(prog_name)
        parser.add_argument(
            'ipsec',
            metavar='<ipsec>',
            help='IpSec name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/ipsec-policies/%s' % parsed_args.ipsec
        data = self.app.session.get(uri)
        return data


class DeleteIpSec(Command):
    """Delete ipsec."""

    def get_parser(self, prog_name):
        parser = super(DeleteIpSec, self).get_parser(prog_name)
        parser.add_argument(
            'ipsec',
            metavar='<ipsec>',
            help='IpSec name or ID'
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
        uri = '/ipsec-policies/%s' % parsed_args.ipsec
        self.app.session.delete(uri)

    def confirm(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            ipsec = self.app.session.get('/ipsec-policies/%s' % parsed_args.ipsec)
            user_response = Confirm.ask(
                "You're about to delete a ipsec named "
                "[red bold]{} Are you sure?".format(
                    ipsec['name'],
                ))
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write("Unable to perform 'delete ipsec' operation in non-interactive mode,"
                                  " without '--i-am-sure' switch\n")
            return False


class CreateIpSec(ShowOne):
    """Create IpSec."""
    schema = schemas.IPSecPolicySchema()

    def get_parser(self, prog_name):
        parser = super(CreateIpSec, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='IpSec name'
        )

        parser.add_argument(
            '--auth-algorithm',
            metavar='<auth_algorithm>',
            choices=['sha1', 'sha256', 'sha384', 'sha512'],
            default='sha1',
            help='IpSec auth_algorithm'
        )

        parser.add_argument(
            '--encapsulation-mode',
            metavar='<encapsulation_mode>',
            choices=['tunnel', 'transport'],
            default='tunnel',
            help='IpSec encapsulation mode'
        )

        parser.add_argument(
            '--encryption-algorithm',
            metavar='<encryption_algorithm>',
            choices=['3des', 'aes-128', 'aes-192', 'aes-256'],
            default='aes-128',
            help='IpSec encryption algorithm'
        )

        parser.add_argument(
            '--pfs',
            metavar='<pfs>',
            choices=['group2', 'group5', 'group14'],
            default='group5',
            help='IpSec pfs'
        )

        parser.add_argument(
            '--transform-protocol',
            metavar='<transform_protocol>',
            choices=['esp', 'ah', 'ah-esp'],
            default='esp',
            help='IpSec transform protocol'
        )

        parser.add_argument(
            '--lifetime',
            metavar='units=<units>,value=<value>',
            dest='lifetime',
            action=parseractions.MultiKeyValueAction,
            required_keys=['units', 'value'],
            default=[{'units':'seconds', 'value':'3600'}],
            help='determine lifetime, e.g --lifetime units=seconds,value=3600'
        )

        return parser

    def get_data(self, parsed_args):
        lifetime = parsed_args.lifetime[0]
        lifetime['value'] = int(lifetime['value'])
        payload = {
            'name': parsed_args.name,
            'auth_algorithm': parsed_args.auth_algorithm,
            'encapsulation_mode': parsed_args.encapsulation_mode,
            'encryption_algorithm': parsed_args.encryption_algorithm,
            'pfs': parsed_args.pfs,
            'transform_protocol': parsed_args.transform_protocol,
            'lifetime': lifetime,
        }
        payload = self.schema.load(payload)
        data = self.app.session.post('/ipsec-policies', payload)
        return data
