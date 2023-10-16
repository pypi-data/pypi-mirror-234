"""
    DigiCloud Image Service
"""

from digicloud import schemas
from digicloud.commands.base import Lister, ShowOne


class ListImage(Lister):
    """List images"""
    schema = schemas.ImageList(many=True)

    def get_data(self, parsed_args):
        data = self.app.session.get('/images')
        return data


class ShowImage(ShowOne):
    """Show image details."""
    schema = schemas.ImageDetails()

    def get_parser(self, prog_name):
        parser = super(ShowImage, self).get_parser(prog_name)
        parser.add_argument(
            'image',
            metavar='<image>',
            help='Image name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/images/%s' % parsed_args.image
        data = self.app.session.get(uri)
        return data
