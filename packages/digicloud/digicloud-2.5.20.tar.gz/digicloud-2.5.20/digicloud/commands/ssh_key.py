"""
    DigiCloud Compute Instance Service.
"""
import os

from .base import ShowOne, Lister, Command
from .. import schemas
from ..error_handlers import CLIError


class CreateSSHKey(ShowOne):
    """Create new public or private key for server ssh access."""
    schema = schemas.SSHKeyDetails()

    def get_parser(self, prog_name):
        parser = super(CreateSSHKey, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='New public or private key name'
        )
        parser.add_argument(
            '--public-key',
            metavar='<file>',
            required=True,
            help='Filename for public key to add. If not used,'
                 ' creates a private key.'
        )
        return parser

    def get_data(self, parsed_args):
        key_path = os.path.expanduser(parsed_args.public_key)
        with open(key_path) as file_:
            public_key = file_.read()

        payload = {
            'name': parsed_args.name,
            'public_key': public_key or '',
        }

        data = self.app.session.post('/ssh-keys', payload)

        return data

    def on_exception(self, parsed_args, exp):
        if isinstance(exp, FileNotFoundError):
            return CLIError([
                dict(
                    msg="Unable to find your public key file",
                    hint="File doesn't exist, it might be a typo in the file path"
                )
            ])
        if isinstance(exp, PermissionError):
            return CLIError([
                dict(
                    msg="Unable to access your public key file",
                    hint="You public key file has a restrictive permission"
                )
            ])
        return super(CreateSSHKey, self).on_exception(parsed_args, exp)


class ListSSHKey(Lister):
    """List ssh_keys."""
    schema = schemas.SSHKeyList(many=True)

    def get_data(self, parsed_args):
        data = self.app.session.get('/ssh-keys')

        return data


class ShowSSHKey(ShowOne):
    """Show ssh_key detail"""
    schema = schemas.SSHKeyDetails()

    def get_parser(self, prog_name):
        parser = super(ShowSSHKey, self).get_parser(prog_name)
        parser.add_argument(
            'ssh_key',
            metavar='<ssh_key>',
            help=('SSH key Name'),
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/ssh-keys/%s' % parsed_args.ssh_key
        data = self.app.session.get(uri)

        return data


class DeleteSSHKey(Command):
    """Delete SSHKey."""

    def get_parser(self, prog_name):
        parser = super(DeleteSSHKey, self).get_parser(prog_name)
        parser.add_argument(
            'ssh_key',
            metavar='<ssh_key>',
            help=('SSH Key Name')
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/ssh-keys/%s' % parsed_args.ssh_key
        self.app.session.delete(uri)
