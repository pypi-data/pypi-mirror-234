from .base import Lister, ShowOne
from .. import schemas
from ..error_handlers import CLIError


class QuotaRequestList(Lister):
    """List your namespace quota"""
    schema = schemas.QuotaRequest(many=True)

    def get_data(self, parsed_args):
        return self.app.session.get('/quota-requests')[:15]


class RequestMoreQuota(ShowOne):
    """Submit a request for more quota"""
    schema = schemas.QuotaRequest()

    def get_parser(self, prog_name):
        parser = super(RequestMoreQuota, self).get_parser(prog_name)
        parser.add_argument(
            '--quota-id',
            required=True,
            metavar='<quota_id>',
            help='Quota ID for the request',
        )

        parser.add_argument(
            '--value',
            required=True,
            metavar='<value>',
            help='Your desire value'
        )
        parser.add_argument(
            '--rule-index',
            required=False,
            type=int,
            metavar='<rule_index>',
            help='Your desire rule id'
        )

        return parser

    def get_data(self, parsed_args):
        resolution = self._check_rule_resolution(parsed_args.quota_id, parsed_args.rule_index)
        return self.app.session.post(
            '/quota-requests',
            {
                'quota_id': parsed_args.quota_id,
                'required_quota': parsed_args.value,
                'note': "Requested by CLI",
                'resolution': resolution,
            })

    def _check_rule_resolution(self, quota_id, rule_id):
        keys_map = {
            'edge.namespace.domain.record.count': 'domain_id',
        }
        uri = '/quotas/{}'.format(self.app.config['CURRENT']['Namespace ID'])
        quota_list = self.app.session.get(uri)
        related_quotas = [quota for quota in quota_list if quota['id'] == quota_id]
        related_quotas_len = len(related_quotas)
        if related_quotas_len == 1:
            return related_quotas[0]['resolution']
        elif related_quotas_len == 0:
            raise CLIError([
                dict(
                    msg="The quota id {} does not exist".format(quota_id)
                )
            ]
            )

        else:
            rule_key = keys_map.get(quota_id, None)
            if rule_key is None:
                raise CLIError([
                    dict(
                        msg="The quota id {} does not support multi rule".format(quota_id)
                    )
                ]
                )
            related_quotas.sort(key=lambda x: x['resolution'][rule_key])
            if rule_id and rule_id <= related_quotas_len:
                return related_quotas[rule_id-1]['resolution']
            else:
                errors = [
                    dict(
                        msg="Rule index {}: {}".format(index, rule['description'])
                    ) for index, rule in enumerate(related_quotas, 1)
                ]
                errors[-1]["hint"] = "You should choose one of the rules index provided above"
                raise CLIError(errors)

