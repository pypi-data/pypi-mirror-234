"""
    DigiCloud InstanceTypes Service.
"""
from digicloud import schemas
from .base import Lister, ShowOne


class ListInstanceType(Lister):
    """List instance-types."""
    schema = schemas.InstanceType(many=True)

    def get_parser(self, prog_name):
        parser = super(ListInstanceType, self).get_parser(prog_name)
        parser.add_argument(
            '--family',
            metavar='<family>',
            help='Filter by family',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/instance-types'
        if parsed_args.family:
            uri = '/instance-types?family=%s' % parsed_args.family
        data = self._sort_instance_types(self.app.session.get(uri))
        return data

    def _sort_instance_types(self, instance_types):
        return sorted(
            instance_types,
            key=lambda item: (
                # Sorting keys
                item.get('family'),
                item.get('vcpus'),
                item.get('ram'),
            ),
            reverse=True
        )


class ShowInstanceType(ShowOne):
    """Show instance-type details."""
    schema = schemas.InstanceType()

    def get_parser(self, prog_name):
        parser = super(ShowInstanceType, self).get_parser(prog_name)
        parser.add_argument(
            'instance_type',
            metavar='<instance type>',
            help='InstanceType name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = f'/instance-types/{parsed_args.instance_type}'
        data = self.app.session.get(uri)
        return data
