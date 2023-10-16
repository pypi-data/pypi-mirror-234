"""
    DigiCloud Compute Instance Service.
"""
from rich.prompt import Confirm

from digicloud import schemas
from .base import Lister, ShowOne, Command
from ..cli import parseractions
from ..error_handlers import CLIError
from ..utils import is_tty


class ListInstance(Lister):
    """List instances."""
    schema = schemas.InstanceList(many=True)

    def get_parser(self, prog_name):
        parser = super(ListInstance, self).get_parser(prog_name)
        parser.add_argument(
            '--simple',
            help='Advanced instances',
            default=None,
            action='store_true'
        )

        parser.add_argument(
            '--advanced',
            help='Simple instances',
            default=None,
            action='store_true'
        )

        parser.add_argument(
            '--id',
            nargs='+',
            help='list of instance IDs to filter, e.g --id 1 2 3 ',
            required=False
        )

        return parser

    def get_data(self, parsed_args):
        args = (parsed_args.simple, parsed_args.advanced)
        if all(args):
            raise CLIError(
                [dict(msg="You need to specify one of --simple or --advanced")])

        query_params = {}
        if parsed_args.simple:
            query_params['type'] = 'simple'
        elif parsed_args.advanced:
            query_params['type'] = 'advanced'

        data = self.app.session.get('/instances', params=query_params)
        return data


class CreateInstance(ShowOne):
    """Create instance."""
    schema = schemas.InstanceDetails()

    def get_parser(self, prog_name):
        parser = super(CreateInstance, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Instance name'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Instance description'
        )
        parser.add_argument(
            '--instance-type',
            required=True,
            metavar='<instance_type>',
            help='InstanceType name or ID'
        )
        parser.add_argument(
            '--root-volume-size',
            required=False,
            type=int,
            metavar='<root_volume_size>',
            help=('Optionally you can set the size of root volume, otherwise root volume '
                  'will be created according to the instance type')
        )

        parser.add_argument(
            '--root-volume-type',
            required=False,
            metavar='<root_volume_type>',
            choices=['SSD', 'ULTRA_DISK'],
            type=lambda value: str(value).upper().replace("-", "_"),
            help=(
                'Optionally you can set the type of root volume, '
                'could be SSD or ULTRA_DISK case insensitive, the default is SSD'
            )
        )

        parser.add_argument(
            '--image',
            required=False,
            metavar='<image>',
            help='Image name or ID'
        )
        parser.add_argument(
            '--snapshot',
            required=False,
            metavar='<snapshot>',
            help='Snapshot name or ID'
        )
        parser.add_argument(
            '--network',
            required=False,
            metavar='<network>',
            help='Network name or ID'
        )
        parser.add_argument(
            '--ssh-key',
            metavar='<ssh_key>',
            help='SSH key name'
        )

        parser.add_argument(
            '--firewall',
            metavar='<firewall>',
            default=[],
            action='append',
            help='Firewall name or ID'
        )
        parser.add_argument(
            '--simple',
            help='Create a instance quickly',
            default=None,
            action='store_true'
        )
        parser.add_argument(
            '--with-public-ip',
            help='Create and associate a Public IP automatically',
            default=None,
            action='store_true'
        )

        parser.add_argument(
            '--public-ip',
            required=False,
            metavar='<public_ip>',
            help='Public IP name or ID to use after instance creation'
        )

        parser.add_argument(
            '--additional-volume',
            metavar='size=<size>,type=<type>',
            dest='additional_volumes',
            action=parseractions.MultiKeyValueAction,
            required_keys=['size', 'type'],
            default=[],
            help='Create and attach additional volume automatically, e.g --additional-volume size=500,type=SSD'
        )

        parser.add_argument(
            '--advanced',
            help='Create a instance with more configuration parameters',
            default=None,
            action='store_true'
        )

        parser.add_argument(
            '--count',
            metavar='<count>',
            type=int,
            help='Create multiple instance at once',
            default=1,
            required=False
        )

        parser.add_argument(
            '--server-group',
            nargs=1,
            dest='server_groups',
            help='list of server groups',
            required=False
        )

        return parser

    def _check_arg_validity(self, parsed_args):
        min_windows_root_vol_size = 20
        rules = [
            (
                all((parsed_args.advanced, parsed_args.simple)),
                "--advanced and --simple must not be used together",
            ),
            (
                parsed_args.simple and parsed_args.network is not None,
                "--simple and --network must not be used together",
            ),
            (
                parsed_args.simple and parsed_args.firewall,
                "--simple and --firewall must not be used together",
            ),
            (
                parsed_args.advanced and parsed_args.network is None,
                "--advanced requires --network to be present",
            ),
            (
                not parsed_args.simple and parsed_args.network is None,
                "--network is mandatory in advanced mode",
            ),
            (
                parsed_args.with_public_ip and parsed_args.public_ip is not None,
                "--with-public-ip and --public-ip must not be used together",
            ),
            # Creating multiple instance conditions:
            (
                parsed_args.with_public_ip and parsed_args.count > 1,
                "--with-public-ip and --count must not be used together",
            ),
            (
                parsed_args.public_ip and parsed_args.count > 1,
                "--public-ip and --count must not be used together",
            ),
            (
                any([
                    str(volume['type']).upper() not in ('SSD', 'ULTRA_DISK')
                    for volume in parsed_args.additional_volumes
                ]),
                "additional volume type must be either 'SSD' or 'ULTRA_DISK'"
            ),
            (
                parsed_args.image and parsed_args.snapshot,
                "--image and --snapshot must not be used together",
            ),
            (
                parsed_args.image is None and parsed_args.snapshot is None,
                "one of the --image and --snapshot arguments must be used",
            ),
            (
                parsed_args.count and parsed_args.count <= 0,
                "--count must be greater than 0",
            ),
            (
                parsed_args.image
                    and parsed_args.image.lower().startswith('windows')
                    and parsed_args.root_volume_size 
                    and parsed_args.root_volume_size is not None
                    and parsed_args.root_volume_size < min_windows_root_vol_size,
                "Minimum required root volume size for Windows images is 20 Gigabytes"
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
        if parsed_args.count and parsed_args.count > 1:
            return self.create_instance_group(parsed_args)

        payload = {
            'name': parsed_args.name,
            'instance_type': parsed_args.instance_type,
            'type': 'simple' if parsed_args.simple else 'advanced',
        }
        if parsed_args.image:
            payload['image'] = parsed_args.image
        if parsed_args.snapshot:
            payload['snapshot'] = parsed_args.snapshot
        if parsed_args.network:
            payload['network'] = parsed_args.network
        if parsed_args.ssh_key:
            payload['ssh_key_name'] = parsed_args.ssh_key
        if parsed_args.firewall:
            payload['security_groups'] = parsed_args.firewall
        if parsed_args.server_groups:
            payload['server_groups'] = parsed_args.server_groups
        if parsed_args.additional_volumes:
            payload['additional_volumes'] = [
                {
                    "size": additional_volume['size'],
                    "volume_type": additional_volume['type'],
                } for additional_volume in parsed_args.additional_volumes
            ]
        if parsed_args.with_public_ip:
            payload['has_public_ip'] = parsed_args.with_public_ip
        if parsed_args.public_ip:
            payload['public_ip'] = parsed_args.public_ip
        if parsed_args.description:
            payload['description'] = parsed_args.description

        if parsed_args.root_volume_type:
            payload['root_volume_type'] = parsed_args.root_volume_type

        if parsed_args.root_volume_size:
            payload['root_volume_size'] = parsed_args.root_volume_size

        data = self.app.session.post('/instances', payload)
        return data

    def create_instance_group(self, parsed_args):
        self.schema = schemas.InstanceGroupDetails(many=False)
        payload = {
            'name': parsed_args.name,
            "count": parsed_args.count,
            "template": {
                'instance_type': parsed_args.instance_type,
                'type': 'simple' if parsed_args.simple else 'advanced',
            },
        }
        if parsed_args.image:
            payload['template']['image'] = parsed_args.image
        if parsed_args.snapshot:
            payload['template']['snapshot'] = parsed_args.snapshot
        if parsed_args.network:
            payload['template']['network'] = parsed_args.network
        if parsed_args.ssh_key:
            payload['template']['ssh_key_name'] = parsed_args.ssh_key
        if parsed_args.firewall:
            payload['template']['security_groups'] = parsed_args.firewall
        if parsed_args.description:
            payload['description'] = parsed_args.description
        if parsed_args.root_volume_type:
            payload['template']['root_volume_type'] = parsed_args.root_volume_type
        if parsed_args.root_volume_size:
            payload['template']['root_volume_size'] = parsed_args.root_volume_size
        if parsed_args.additional_volumes:
            payload['template']['additional_volumes'] = [
                {
                    "size": additional_volume['size'],
                    "volume_type": additional_volume['type'],
                } for additional_volume in parsed_args.additional_volumes
            ]

        data = self.app.session.post('/instance-groups', payload)
        command = "[bold blue]digicloud instance list --id %s[/bold blue]" % " ".join(
            data['instance_ids']
        )
        self.app.console.print(f"Check you new instances via `%s`" % command)
        return data


class ShowInstance(ShowOne):
    """Show instance details."""
    schema = schemas.InstanceDetails()

    def get_parser(self, prog_name):
        parser = super(ShowInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s' % parsed_args.instance
        data = self.app.session.get(uri)
        return data


class DeleteInstance(Command):
    """Delete a instance."""

    def get_parser(self, prog_name):
        parser = super(DeleteInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )

        parser.add_argument(
            '--delete-volumes',
            help='Delete additional volumes attached to instance',
            default=None,
            action='store_true'
        )

        parser.add_argument(
            '--delete-root-volume',
            help='Use this switch to also delete root volume',
            default=None,
            action='store_true'
        )

        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )

        return parser

    def take_action(self, parsed_args):
        snapshot_check_uri = '/instances/%s/snapshots' % parsed_args.instance
        instance_snapshot = self.app.session.get(snapshot_check_uri)
        if instance_snapshot:
            self.app.stdout.write(
                "NOTE: You have snapshot on this instance so you can't delete its volumes\n"
            )
            return

        if not self.confirm_instance_deletion(parsed_args):
            return
        uri = '/instances/%s' % parsed_args.instance

        additional_volumes_ids = self._get_additional_volumes_ids(parsed_args.instance)
        if self.confirm_root_volume_deletion(parsed_args):
            uri += self._format_query_param(uri, "delete_root_volume=true")
        if additional_volumes_ids and self.confirm_additional_volume_deletion(parsed_args):
            uri += self._format_query_param(uri, "delete_additional_volumes=true")

        self.app.session.delete(uri)

    def _has_query_param(self, uri: str):
        return '?' in uri

    def _format_query_param(self, uri, new_query_param: str):
        new_query_param = new_query_param.strip()
        return f"&{new_query_param}" if self._has_query_param(uri) else f"?{new_query_param}"


    def confirm_instance_deletion(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            instance = self.app.session.get('/instances/%s' % parsed_args.instance)
            user_response = Confirm.ask(
                "You're about to delete the instance named [red bold]{}[/red bold]. "
                "Are you sure?".format(
                    instance['name']
                ), default=False
            )
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write(
                "Unable to perform 'instance delete' operation in non-interactive mode,"
                " without '--i-am-sure' switch\n")
            return False

    def confirm_root_volume_deletion(self, parsed_args):
        return self._volume_deletion_confirmation(
                parsed_args.delete_root_volume,
                "Would you like to also delete the root volume of this instance?"
        )

    def confirm_additional_volume_deletion(self, parsed_args):
        return self._volume_deletion_confirmation(
                parsed_args.delete_volumes,
                "Would you like to also delete the additional volumes attached to this instance?"
        )

    def _volume_deletion_confirmation(self, already_confirmed, msg):
        if already_confirmed:
            return True
        if is_tty():
            return Confirm.ask(
                msg,
                default=False
            )
        return False

    def _get_additional_volumes_ids(self, instance_name):
        uri = '/instances/%s/volumes' % instance_name
        non_root_volumes_id = [vol['id'] for vol in self.app.session.get(uri) if vol['is_root'] == False]
        return non_root_volumes_id

class ListInstanceVolume(Lister):
    """List instance volume(s)."""
    schema = schemas.InstanceVolume(many=True)

    def get_parser(self, prog_name):
        parser = super(ListInstanceVolume, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        # TODO: Could use a little bit of cache maybe
        # TODO: Duplicate logic
        volumes = {
            v['id']: v for v in self.app.session.get('/volumes')
        }
        instance_info = self.app.session.get('/instances/%s' % parsed_args.instance)
        uri = '/instances/%s/volumes' % instance_info['id']
        instance_volumes = self.app.session.get(uri)
        return [
            {
                "instance": instance_info['name'],
                "volume": volumes[volume['id']]['name'],
                **volume
            }
            for volume in instance_volumes

        ]


class ShowInstanceVolume(ShowOne):
    """Show instance volume details."""
    schema = schemas.InstanceVolume(many=False)

    def get_parser(self, prog_name):
        parser = super(ShowInstanceVolume, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        parser.add_argument(
            '--volume',
            required=True,
            metavar='<volume>',
            help='Volume name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        # TODO: Could use a little bit of cache maybe
        # TODO: Duplicate logic
        volumes = {
            v['id']: v for v in self.app.session.get('/volumes')
        }
        instance_info = self.app.session.get('/instances/%s' % parsed_args.instance)
        uri = '/instances/%s/volumes/%s' % (parsed_args.instance, parsed_args.volume)
        instance_volume = self.app.session.get(uri)
        return {
            "instance": instance_info['name'],
            "volume": volumes[instance_volume['id']]['name'],
            **instance_volume
        }


class AttachInstanceVolume(ShowOne):
    """Attach instance volume."""
    schema = schemas.InstanceVolume(many=False)

    def get_parser(self, prog_name):
        parser = super(AttachInstanceVolume, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--volume',
            required=True,
            metavar='<volume>',
            help='Volume name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s/volumes' % parsed_args.instance
        payload = {'id': parsed_args.volume}

        data = self.app.session.post(uri, payload)

        return data


class DetachInstanceVolume(Command):
    """Detach instance volume."""

    def get_parser(self, prog_name):
        parser = super(DetachInstanceVolume, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--volume',
            required=True,
            metavar='<volume>',
            help='Volume name or ID'
        )

        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/volumes/%s' % (parsed_args.instance, parsed_args.volume)
        self.app.session.delete(uri)


class ListInstanceInterface(Lister):
    """List instance interface(s)."""
    schema = schemas.ListInstanceInterface(many=True)

    def get_parser(self, prog_name):
        parser = super(ListInstanceInterface, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s/interfaces' % parsed_args.instance
        data = self.app.session.get(uri)

        return data


class AttachInterface(ShowOne):
    """Attach interface."""
    schema = schemas.InstanceInterface(many=False)

    def get_parser(self, prog_name):
        parser = super(AttachInterface, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--network',
            required=True,
            metavar='<network>',
            help='Network name or ID',

        )
        return parser

    def get_data(self, parsed_args):
        payload = {'net': parsed_args.network}
        uri = '/instances/%s/interfaces' % parsed_args.instance
        data = self.app.session.post(uri, payload)
        return data


class DetachInterface(Command):
    """Detach interface."""

    def get_parser(self, prog_name):
        parser = super(DetachInterface, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--interface-id',
            required=True,
            metavar='<interface>',
            help='Interface ID',

        )

        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/interfaces/%s' % (
            parsed_args.instance, parsed_args.interface_id)
        self.app.session.delete(uri)


class UpdateInstance(ShowOne):
    """Update instance name, description or even resize it to another instance-type"""
    schema = schemas.InstanceDetails()

    def get_parser(self, prog_name):
        parser = super(UpdateInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance ID or name',
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            required=False,
            help='Instance new name, must be unique',
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            required=False,
            help='Instance description',
        )
        parser.add_argument(
            '--instance-type',
            metavar='<instance_type>',
            required=False,
            help='New instance type you want to use for this instance',
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s' % parsed_args.instance
        payload = {}
        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.description:
            payload['description'] = parsed_args.description
        if parsed_args.instance_type:
            payload['instance_type'] = parsed_args.instance_type
            self.app.console.print(
                "Resizing your instance might cause additional charges",
                style='bold yellow'
            )
        if not payload:
            raise CLIError([
                dict(
                    msg="At least one of --name or --description or "
                        "--instance-type must be provided"
                )
            ]
            )
        data = self.app.session.patch(uri, payload)

        return data

    def _on_400(self, parsed_args, response):
        error_msg = response.json()['message']
        if 'stop your instance' in error_msg:
            return CLIError([
                dict(
                    msg=error_msg,
                    hint="You can stop your instance by running: "
                         "[bold blue]digicloud instance stop {}[/bold blue]".format(
                        parsed_args.instance
                    )
                )
            ])

    def _on_404(self, parsed_args, response):
        return CLIError([
            dict(
                msg="Please check your instance name and try again!",
                hint="You can list your instances by running: "
                     "[bold blue]digicloud instance list [/bold blue]"
            )
        ])


class ResizeInstance(ShowOne):
    """Resize your instance"""
    schema = schemas.InstanceDetails()

    def get_parser(self, prog_name):
        parser = super(ResizeInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance ID or name',
        )
        parser.add_argument(
            '--instance-type',
            metavar='<instance_type>',
            required=True,
            help='The instance type you want to use for this instance',
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s' % parsed_args.instance
        payload = {}
        if parsed_args.instance_type:
            payload['instance_type'] = parsed_args.instance_type
            self.app.console.print(
                "Resizing your instance might cause additional charges",
                style='bold yellow'
            )
        return self.app.session.patch(uri, payload)

    def _on_400(self, parsed_args, response):
        error_msg = response.json()['message']
        if 'stop your instance' in error_msg:
            return CLIError([
                dict(
                    msg=error_msg,
                    hint="You can stop your instance by running: "
                         "[bold blue]digicloud instance stop {}[/bold blue]".format(
                        parsed_args.instance
                    )
                )
            ])


class ListFirewall(Lister):
    """List Instance Firewalls"""
    schema = schemas.FirewallList(many=True)

    def get_parser(self, prog_name):
        parser = super(ListFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s/security-groups' % parsed_args.instance
        data = self.app.session.get(uri)
        return data


class AddFirewall(Command):
    """Add Firewall to instance"""

    def get_parser(self, prog_name):
        parser = super(AddFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--firewall',
            required=True,
            metavar='<firewall>',
            help='Firewall name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        payload = {'security_group_ref': parsed_args.firewall}
        uri = '/instances/%s/security-groups' % parsed_args.instance
        self.app.session.post(uri, payload)


class RemoveFirewall(Command):
    """Remove Firewall from Instance"""

    def get_parser(self, prog_name):
        parser = super(RemoveFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--firewall',
            required=True,
            metavar='<firewall>',
            help='Firewall name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/security-groups/%s' % (parsed_args.instance,
                                                    parsed_args.firewall)
        self.app.session.delete(uri)


class ListInstanceSnapshot(Lister):
    """List Instance Snapshots"""
    schema = schemas.SnapshotList(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s/snapshots' % parsed_args.instance
        data = self.app.session.get(uri)
        return data


class InstanceConsoleLog(Command):
    """Show instance console log."""

    def get_parser(self, prog_name):
        parser = super(InstanceConsoleLog, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        parser.add_argument(
            '--lines',
            help='Number of instance console log lines',
            required=False
        )
        parser.add_argument(
            '--full',
            help='Full of instance console log lines',
            default=None,
            action='store_true'
        )
        return parser

    def _check_arg_validity(self, parsed_args):
        rules = [
            (
                all((parsed_args.full, parsed_args.lines)),
                "--lines and --full must not be used together",
            )
        ]
        errors = []
        for is_invalid, err_msg in rules:
            if is_invalid:
                errors.append(dict(msg=err_msg))
        if errors:
            raise CLIError(errors)

    def take_action(self, parsed_args):
        default_lines = 100
        self._check_arg_validity(parsed_args)
        uri = '/instances/%s/logs' % parsed_args.instance

        query_params = {}
        if parsed_args.full:
            query_params['lines'] = None
        elif parsed_args.lines:
            query_params['lines'] = parsed_args.lines
        else:
            query_params['lines'] = default_lines

        data = self.app.session.get(uri, params=query_params)
        self.app.console.out(data)