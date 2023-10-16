"""
        DigiCloud Compute Server Group Service 
"""
'''
    Create Server group
    Delete Server group
    Show Server group
    List Server groups
'''
from rich.prompt import Confirm

from digicloud import schemas
from .base import Lister, ShowOne, Command
from ..cli import parseractions
from ..error_handlers import CLIError
from ..utils import is_tty

class CreateServerGroup(ShowOne):
    schema = schemas.ServerGroupDetails()

    def get_parser(self, prog_name):
        parser = super(CreateServerGroup, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help="Server group name"
        )

        parser.add_argument(
            '--policy',
            metavar='<policy>',
            required=True,
            choices=['AFFINITY', 'ANTI_AFFINITY', 'SOFT_AFFINITY', 'SOFT_ANTI_AFFINITY'],
            help=('Server group policy')
        )

        parser.add_argument(
            '--rules',
            metavar='max_server_per_host=<max_server_per_host>',
            dest="rules",
            action=parseractions.MultiKeyValueAction,
            required_keys=['max_server_per_host'],
            default=[],
            help=('Use this property to specify rules. Now only max_server_per_host is allowed'
                  'to be used alongside with anti_affinity policy') 
        )
        return parser

    def _check_arg_validity(self, parsed_args):
        rules = [
            (
                len(parsed_args.rules) and parsed_args.policy.lower() != 'anti_affinity',
                'rules can only be used with anti_affinity policy',
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
        
        payload = {
            'name': parsed_args.name,
            'policy': parsed_args.policy
        }

        if parsed_args.rules:
            payload['rules'] = {
                'max_server_per_host': parsed_args.rules[0]['max_server_per_host'],
            }
        data = self.app.session.post('/server-groups', payload)
        return data


class ShowServerGroup(ShowOne):
    schema =  schemas.ServerGroupDetails()

    def get_parser(self, prog_name):
        parser = super(ShowServerGroup, self).get_parser(prog_name)
        parser.add_argument(
            'server_group',
            metavar="<server_group>",
            help='Server group name or ID', 
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/server-groups/%s' % parsed_args.server_group
        data = self.app.session.get(uri)
        return data


class ListServerGroups(Lister):
    schema = schemas.ServerGroupDetails(many=True)

    def get_parser(self, prog_name):
        parser = super(ListServerGroups, self).get_parser(prog_name)
        parser.add_argument(
            '--policy',
            metavar='<policy>',
            choices=['AFFINITY', 'ANTI_AFFINITY', 'SOFT_AFFINITY', 'SOFT_ANTI_AFFINITY'],
            help=('Server group policy')
        )

        return parser

    def get_data(self, parsed_args):
        query_params = {}
        if parsed_args.policy:
            query_params['policy'] = parsed_args.policy

        data = self.app.session.get('/server-groups', params=query_params)
        return data


class DeleteServerGroup(Command):
    def get_parser(self, prog_name):
        parser = super(DeleteServerGroup, self).get_parser(prog_name)
        parser.add_argument(
            'server_group',
            metavar='<server_group>',
            help='Servre group name or ID',
        )
        
        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true',
        )

        return parser

    def take_action(self, parsed_args):
        if not self.confirm_server_group_deletion(parsed_args):
            return 

        uri = '/server-groups/%s' % parsed_args.server_group
        self.app.session.delete(uri)

    def confirm_server_group_deletion(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            serv_group = self.app.session.get('/server-groups/%s' % parsed_args.server_group)
            user_response = Confirm.ask(
                "You're about to delete the server group named [red bold]{}[/red bold]. "
                "Are you sure?".format(
                    serv_group['name']
                ), default=False
            )
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write(
                "Unable to perform 'server group delete' operation in non-interactive mode,"
                " without '--i-am-sure' switch\n")
            return False