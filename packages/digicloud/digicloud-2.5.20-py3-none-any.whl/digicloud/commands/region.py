from digicloud.commands.base import Lister, ShowOne
from digicloud.error_handlers import CLIError


class ListRegions(Lister):
    """List available regions"""

    def get_data(self, parsed_args):
        return self.app.session.get('/regions')


class SelectRegion(ShowOne):
    """Select specific region to setup"""

    def get_parser(self, prog_name):
        parser = super(SelectRegion, self).get_parser(prog_name)

        parser.add_argument(
            'region_name',
            metavar='<region_name>',
            help="Region name"
        )

        return parser

    def get_data(self, parsed_args):
        regions = {region['name'] for region in self.app.session.get('/regions')}
        if parsed_args.region_name not in regions:
            raise CLIError([dict(
                msg="We have no such a region in Digicloud",
                hint='Check our current regions via '
                     '[blue bold]digicloud region list[/blue bold]'
            )])
        self.app.config['AUTH_HEADERS'].update({
            'Digicloud-Region': parsed_args.region_name,
        })
        return {'Region': parsed_args.region_name}


class CurrentRegion(ShowOne):
    """Show current selected region"""

    def get_data(self, parsed_args):
        header = self.app.config.get('AUTH_HEADERS')
        if header is not None:
            selected_region = header.get('Digicloud-Region', 'No region selected')
        else:
            selected_region = 'No region selected'

        return {'Region': selected_region}
