from digicloud.commands.base import Command
from digicloud.error_handlers import CLIError


class InstanceOperationMixin:
    new_state = None

    def get_parser(self, prog_name):
        parser = super(InstanceOperationMixin, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        return parser

    def _on_409(self, parsed_args, response):
        instance = self.app.session.get('/instances/%s' % parsed_args.instance)
        return CLIError([
            dict(
                msg="Your instance status is {}, and your requested operation "
                    "is not possible at the moment.".format(instance['status']),
                hint="Check your instance current status by "
                     "[blue bold]digicloud instance show {}[/blue bold]".format(
                    instance['name']
                )
            )
        ]
        )

    def take_action(self, parsed_args):
        uri = '/instances/%s/state-transitions' % parsed_args.instance
        self.app.session.post(uri, payload=dict(new_state=self.new_state))


class StartInstance(InstanceOperationMixin, Command):
    """Start instance."""
    new_state = "ACTIVE"


class StopInstance(InstanceOperationMixin, Command):
    """Stop instance."""
    new_state = "SHUTOFF"


class SuspendInstance(InstanceOperationMixin, Command):
    """Suspend instance."""
    new_state = "SUSPENDED"


class ResumeInstance(InstanceOperationMixin, Command):
    """Resume instance."""
    new_state = "ACTIVE"


class RebootInstance(InstanceOperationMixin, Command):
    """Reboot instance."""

    def get_parser(self, prog_name):
        parser = super(RebootInstance, self).get_parser(prog_name)
        parser.add_argument(
            '--type',
            default='SOFT',
            metavar='<type>',
            help='either `SOFT` for a software-level reboot, or `HARD` for a virtual '
                 'power cycle hard reboot',
            choices=['SOFT', 'HARD']
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/state-transitions' % parsed_args.instance
        self.app.session.post(uri, payload=dict(new_state="REBOOT",
                                                params={"reboot_type": parsed_args.type}))
