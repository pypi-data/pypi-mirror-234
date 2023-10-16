"""
    Digicloud Namespace Management.
"""

from .base import Lister, ShowOne, Command
from .. import schemas
from ..error_handlers import CLIError


def get_namespace(name_or_id, session):
    candidates = []
    for namespace in session.get('/namespaces'):
        if name_or_id == namespace['id'] or name_or_id == namespace['name']:
            candidates.append(namespace)
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        raise CLIError([dict(
            msg="You are a member of multiple namespaces named '{}'".format(name_or_id),
            hint="You should check list of your namespaces and repeat this command with"
                 " namespace id instead of name."
        )])
    raise CLIError([dict(
        msg="You're not a member of a namespace with this name or ID",
        hint="It might be because you leave "
             "the namespace (or someone removed you)."
             " you can see list of your namespaces by "
             "[blue bold]digicloud namespace list[/blue bold]"
    )])


class CreateNamespace(ShowOne):
    """Create Namespace."""
    schema = schemas.NamespaceDetails()

    def get_parser(self, prog_name):
        parser = super(CreateNamespace, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Name of namespace'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Description of namespace'
        )
        return parser

    def get_data(self, parsed_args):
        return self.app.session.post('/namespaces', {
            'name': parsed_args.name,
            'description': parsed_args.description,
        })


class ListNamespace(Lister):
    """List namespaces"""
    schema = schemas.NamespaceList(many=True)

    def get_data(self, parsed_args):
        return self.app.session.get('/namespaces')


class ShowNamespace(ShowOne):
    """Show server details."""
    schema = schemas.NamespaceDetails()

    def get_parser(self, prog_name):
        parser = super(ShowNamespace, self).get_parser(prog_name)
        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )
        return parser

    def get_data(self, parsed_args):
        return get_namespace(parsed_args.namespace, self.app.session)


class ListNamespaceMember(Lister):
    """List namespace members and invitations."""
    schema = schemas.NamespaceMemberList(many=True)

    def get_parser(self, prog_name):
        parser = super(ListNamespaceMember, self).get_parser(prog_name)
        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )
        return parser

    def get_data(self, parsed_args):
        namespace = get_namespace(parsed_args.namespace, self.app.session)
        members = self.app.session.get("/namespaces/{id}/members".format(id=namespace['id']))
        invitations = self.app.session.get("/namespaces/{id}/invitations".format(id=namespace['id']))
        return members + invitations


class InviteMember(Command):
    """Add Member to Namespace."""

    def get_parser(self, prog_name):
        parser = super(InviteMember, self).get_parser(prog_name)
        parser.add_argument(
            '--email',
            metavar='<user_email>',
            required=True,
            help='E-mail Address to send the invitation'
        )

        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )
        return parser

    def take_action(self, parsed_args):
        namespace = get_namespace(parsed_args.namespace, self.app.session)
        uri = '/invitations'
        payload = {
            'email': parsed_args.email,
            'namespace': namespace['id']
        }
        self.app.session.post(uri, payload)
        self.app.console.print(
            "[green bold]An invitation has been sent to {}[/green bold]".format(
                parsed_args.email
            )
        )


class DeleteNamespaceMember(Command):
    """Delete Member from Namespace."""

    def get_parser(self, prog_name):
        parser = super(DeleteNamespaceMember, self).get_parser(prog_name)
        parser.add_argument(
            '--user-id',
            metavar='<user_id>',
            required=True,
            help='ID of user'
        )
        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )

        return parser

    def take_action(self, parsed_args):
        namespace = get_namespace(parsed_args.namespace, self.app.session)
        uri = '/namespaces/{}/members/{}'.format(
            namespace["id"],
            parsed_args.user_id
        )
        self.app.session.delete(uri)


class LeaveNamespace(Command):
    """Leave a namespace """

    def get_parser(self, prog_name):
        parser = super(LeaveNamespace, self).get_parser(prog_name)
        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )

        return parser

    def take_action(self, parsed_args):
        current_user = self.app.config['USER']['id']
        namespace = get_namespace(parsed_args.namespace, self.app.session)
        uri = '/namespaces/%s/members/%s' % (namespace['id'], current_user)
        self.app.session.delete(uri)


class DeleteNamespace(Command):
    """Delete Namespace."""

    def get_parser(self, prog_name):
        parser = super(DeleteNamespace, self).get_parser(prog_name)
        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )
        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )

        return parser

    def take_action(self, parsed_args):
        self.app.console.print("Delete namespace feature is not currently available")


class SelectNamespace(ShowOne):
    """Select Namespace."""
    schema = schemas.NamespaceDetails()

    def get_parser(self, prog_name):
        parser = super(SelectNamespace, self).get_parser(prog_name)
        parser.add_argument(
            'namespace',
            metavar='<NAMESPACE ID>',
            help='Select namespace as default',
        )
        return parser

    def get_data(self, parsed_args):
        namespace = get_namespace(parsed_args.namespace, self.app.session)
        uid = self.app.config['USER']['id']
        url = '/users/%s' % uid
        payload = {'default_namespace': namespace['id']}
        self.app.session.patch(url, payload)
        self.app.config['AUTH_HEADERS']['Digicloud-Namespace'] = namespace['id']
        return namespace


class CurrentNamespace(ShowOne):
    """Display current namespace."""
    schema = schemas.NamespaceDetails()

    def get_parser(self, prog_name):
        parser = super(CurrentNamespace, self).get_parser(prog_name)

        return parser

    def get_data(self, parsed_args):
        if self.app.config.get('AUTH_HEADERS') is None:
            raise CLIError([
                dict(
                    msg="You need to login first",
                    hint="you can login by [blue bold]digicloud account login[/blue bold]"
                )
            ])

        namespace_id = self.app.config['AUTH_HEADERS']['Digicloud-Namespace']
        namespace = self.app.session.get('/namespaces/%s' % namespace_id)
        return namespace


class AcceptInvitation(ShowOne):
    """Accept an invitation to join a namespace"""
    schema = schemas.UserInvitation()

    def get_parser(self, prog_name):
        parser = super(AcceptInvitation, self).get_parser(prog_name)
        parser.add_argument(
            'invitation',
            metavar='<invitation>',
            help='Invitation ID to accept or reject'
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/invitations/%s' % parsed_args.invitation
        payload = {
            'status': "accepted"
        }
        return self.app.session.patch(uri, payload)


class ListQuota(Lister):
    """List your namespace quota"""
    schema = schemas.NamespaceQuota(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'namespace',
            metavar='<NAMESPACE>',
            help='Namespace name or id',
        )
        return parser

    def get_data(self, parsed_args):
        namespace = get_namespace(parsed_args.namespace, self.app.session)
        uri = '/quotas/{}'.format(namespace["id"])
        data = self.app.session.get(uri)
        return data


class ListUserInvitations(Lister):
    """Lists all user invitations"""
    schema = schemas.UserInvitation(many=True)

    def get_data(self, parsed_args):
        uri = '/invitations'
        return self.app.session.get(uri)
