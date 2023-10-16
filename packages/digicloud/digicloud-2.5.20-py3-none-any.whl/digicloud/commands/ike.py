"""
    DigiCloud IKE Service.
"""
from rich.prompt import Confirm

from .base import Lister, ShowOne, Command
from ..cli import parseractions
from digicloud import schemas
from ..utils import is_tty


class ListIKE(Lister):
    """List ikes."""
    schema = schemas.IKEPolicySchema(many=True)

    def get_data(self, parsed_args):
        objects = self.app.session.get('/ike-policies')
        return objects


class ShowIKE(ShowOne):
    """Show ike details."""
    schema = schemas.IKEPolicySchema()

    def get_parser(self, prog_name):
        parser = super(ShowIKE, self).get_parser(prog_name)
        parser.add_argument(
            'ike',
            metavar='<ike>',
            help='IKE name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/ike-policies/%s' % parsed_args.ike
        data = self.app.session.get(uri)
        return data


class DeleteIKE(Command):

    def get_parser(self, prog_name):
        parser = super(DeleteIKE, self).get_parser(prog_name)
        parser.add_argument(
            'ike',
            metavar='<ike>',
            help='IKE name or ID'
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
        uri = '/ike-policies/%s' % parsed_args.ike
        self.app.session.delete(uri)

    def confirm(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            ike = self.app.session.get('/ike-policies/%s' % parsed_args.ike)
            user_response = Confirm.ask(
                "You're about to delete a ike named "
                "[red bold]{} Are you sure?".format(
                    ike['name'],
                ))
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write("Unable to perform 'delete ike' operation in non-interactive mode,"
                                  " without '--i-am-sure' switch\n")
            return False


class CreateIKE(ShowOne):
    """Create IKE."""
    schema = schemas.IKEPolicySchema()

    def get_parser(self, prog_name):
        parser = super(CreateIKE, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='IKE name'
        )

        parser.add_argument(
            '--auth-algorithm',
            metavar='<auth_algorithm>',
            choices=['sha1', 'sha256', 'sha384', 'sha512'],
            default='sha1',
            help='IKE auth_algorithm'
        )

        parser.add_argument(
            '--encryption-algorithm',
            metavar='<encryption_algorithm>',
            choices=['3des', 'aes-128', 'aes-192', 'aes-256'],
            default='aes-128',
            help='IKE encryption algorithm'
        )

        parser.add_argument(
            '--pfs',
            metavar='<pfs>',
            choices=['group2', 'group5', 'group14'],
            default='group5',
            help='IKE pfs'
        )

        parser.add_argument(
            '--ike-version',
            metavar='<ike_version>',
            choices=['v1', 'v2', ],
            default='v1',
            help='IKE version'
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
            'ike_version': parsed_args.ike_version,
            'encryption_algorithm': parsed_args.encryption_algorithm,
            'pfs': parsed_args.pfs,
            'ike_version': parsed_args.ike_version,
            'lifetime': lifetime,
        }
        payload = self.schema.load(payload)
        data = self.app.session.post('/ike-policies', payload)
        return data
