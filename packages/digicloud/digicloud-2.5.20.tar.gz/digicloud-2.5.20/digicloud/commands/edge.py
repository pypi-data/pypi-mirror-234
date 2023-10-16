"""
    DigiCloud Edge SND and CDN services.
"""
import json
import os

from marshmallow.exceptions import ValidationError
from rich.prompt import Confirm, Prompt

from .base import Lister, ShowOne, Command
from ..error_handlers import CLIError
from .. import schemas
from ..utils import is_tty, t_or_f_or_n, tabulate as util_tabulate
from tabulate import tabulate


class ListDomain(Lister):
    """List edge domains"""
    schema = schemas.EdgeDomainList(many=True)

    def get_data(self, parsed_args):
        domains = self.app.session.get('/edge/domains')
        return domains


class CreateDomain(ShowOne):
    """Create Domain"""
    schema = schemas.EdgeDomainDetails()
    package_schema = schemas.EdgeDomainPackageDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Domain name',
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.name,
            'package_id': self._get_package(),
        }
        domain = self.app.session.post('/edge/domains', payload)

        if domain['is_subdomain']:
            self.app.console.print(
                "[bold yellow]{}[/bold yellow]"
                "In order to define a sub-domain in DIGICLOUD, "
                "you need to verify your ownership on Root Domain. "
                "Please add a TXT record on your root Domain DNS Setting".format(
                    "Create a TXT Record like the following: "
                    "\n\t [bold blue]_digicdn_check.{}[/bold blue] = "
                    "[bold blue]{}[/bold blue] \n".format(
                        str(parsed_args.name).split(".")[0], domain["ns_verification"]
                    )
                )
            )
        else:
            result = self.app.session.get(
                '/edge/domains/{}/ns-records'.format(domain["id"])
            )
            self.app.console.print(
                "[bold yellow]{}[/bold yellow]".format(
                    "Make sure to set DigiCloud NS records: "
                    "\n\t [bold blue]{}[/bold blue]".format(
                        "\n\t ".join(result["digicloud_ns_records"])
                    )
                )
            )
        return domain

    def _get_package(self):
        result = util_tabulate(
            self.package_schema.dump(
                self.app.session.get(
                    '/edge/packages'
                ),
                many=True,
            )
        )

        self.app.console.print(
            tabulate(
                result[1],
                headers=result[0],
                tablefmt='outline',
            )
        )

        self.app.console.print(
            "[bold yellow]{}[/bold yellow]".format(
                "Please select one from above list for your domain package!"
            )
        )

        return Prompt.ask("Package id")


class GetDomainDNSSEC(ShowOne):
    """Get Domain DNSSEC"""
    schema = schemas.DomainDNSSECDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='Domain name or id',
        )
        return parser

    def get_data(self, parsed_args):
        dnssec = self.app.session.get(
            '/edge/domains/{}/dnssec'.format(parsed_args.domain)
        )
        return dnssec


class EnableDomainDNSSEC(ShowOne):
    """Enable domain dnssec."""
    schema = schemas.DomainDNSSECDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='Domain name or id',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/dnssec'.format(parsed_args.domain)
        payload = {
            "dnssec": True,
        }
        dnssec = self.app.session.patch(uri, payload)
        return dnssec


class DisableDomainDNSSEC(ShowOne):
    """Disable domain dnssec."""
    schema = schemas.DomainDNSSECDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='Domain name or id',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/dnssec'.format(parsed_args.domain)
        payload = {
            "dnssec": False,
        }
        dnssec = self.app.session.patch(uri, payload)
        return dnssec


class GetDomainNSRecordSetting(Command):
    """Get Domain/Sub Domain NS record setting"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='Domain name or id',
        )
        return parser

    def take_action(self, parsed_args):
        domain = self.app.session.get('/edge/domains/%s' % parsed_args.domain)
        if domain['is_subdomain']:
            self.app.console.print(
                "[bold yellow]{}[/bold yellow]"
                "In order to define a sub-domain in DIGICLOUD, "
                "you need to verify your ownership on Root Domain. "
                "Please add a TXT record on your root Domain DNS Setting".format(
                    "Create a TXT Record like the following: "
                    "\n\t [bold blue]_digicdn_check.{}[/bold blue] = "
                    "[bold blue]{}[/bold blue] \n".format(
                        str(domain['name']).split(".")[0], domain["ns_verification"]
                    )
                )
            )
        else:
            result = self.app.session.get(
                '/edge/domains/{}/ns-records'.format(parsed_args.domain)
            )
            self.app.console.print(
                "[bold yellow]{}[/bold yellow]".format(
                    "Please set these NS records: \n"
                    "\t [bold blue]{}[/bold blue]".format(
                        "\n\t ".join(result["digicloud_ns_records"])
                    )
                )
            )


class VerifyNSRecord(Command):
    """Verify ns record"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='Domain name or id',
        )
        return parser

    def take_action(self, parsed_args):
        result = self.app.session.get(
            '/edge/domains/{}/verify-ns-records'.format(parsed_args.domain)
        )
        if result["result"]:
            self.app.console.print(
                "[bold green]{}[/bold green]".format(
                    "DigiCloud NS records fully activated."
                )
            )
        else:
            domain = self.app.session.get('/edge/domains/%s' % parsed_args.domain)
            if domain['is_subdomain']:
                self.app.console.print(
                    "[bold red]{}[/bold red]".format(
                        "DigiCloud was not able to verify your TXT records."
                    )
                )
                self.app.console.print(
                    "[bold yellow]{}[/bold yellow]"
                    "In order to define a sub-domain in DIGICLOUD, "
                    "you need to verify your ownership on Root Domain. "
                    "Please add a TXT record on your root Domain DNS Setting".format(
                        "Create a TXT Record like the following: "
                        "\n\t [bold blue]_digicdn_check.{}[/bold blue] = "
                        "[bold blue]{}[/bold blue] \n".format(
                            str(domain['name']).split(".")[0], domain["ns_verification"]
                        )
                    )
                )
            else:
                result = self.app.session.get(
                    '/edge/domains/{}/ns-records'.format(parsed_args.domain)
                )
                self.app.console.print(
                    "[bold red]{}[/bold red]".format(
                        "DigiCloud was not able to verify your NS records."
                    )
                )
                self.app.console.print(
                    "[bold yellow]{}[/bold yellow]".format(
                        "Make sure to set DigiCloud NS records: \n\t [bold blue]{}[/bold blue]".format(
                            "\n\t ".join(result["digicloud_ns_records"])
                        )
                    )
                )


class DeleteDomain(Command):
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='Domain name or id',
        )

        parser.add_argument(
            '--yes-i-really-mean-it',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )
        return parser

    def take_action(self, parsed_args):
        domain = self.app.session.get('/edge/domains/%s' % parsed_args.domain)
        if not self.delete_domain_2_step(domain):
            return
        if not self.confirm_domain_deletion(parsed_args, domain):
            return
        self.app.session.delete('/edge/domains/%s' % parsed_args.domain)

    def confirm_domain_deletion(self, parsed_args, domain):
        if parsed_args.yes_i_really_mean_it:
            return True
        if is_tty():
            user_response = Confirm.ask(
                "You're about to delete domain named [red bold]{}[/red bold]. "
                "Are you sure?".format(
                    domain['name']
                ), default=False
            )
            if user_response:
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write(
                "Unable to perform 'domain delete' operation in non-interactive mode,"
                " without '--yes-i-really-mean-it' switch\n")
            return False

    def delete_domain_2_step(self, domain):
        if is_tty():
            domain_name = Prompt.ask(
                "[red bold]Attention:[/red bold] "
                "You're about to delete domain named [red bold]{}[/red bold]. "
                "Are you sure? Please write the domain name".format(
                    domain['name'],
                )
            )
            if domain_name == domain["name"]:
                return True
            self.app.stdout.write("Wrong domain name!\n")
            return False
        else:
            return True


class ShowDomain(ShowOne):
    schema = schemas.EdgeDomainDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='Domain name or id',
        )
        return parser

    def get_data(self, parsed_args):
        domain = self.app.session.get('/edge/domains/%s' % parsed_args.domain)
        return domain


def get_record_schema(data):
    schema_map = {
        "A": schemas.ARecordDetailsSchema(),
        "TXT": schemas.TXTRecordDetailsSchema(),
        "CNAME": schemas.CNAMERecordDetailsSchema(),
        "MX": schemas.MXRecordDetailsSchema(),
        "SRV": schemas.SRVRecordDetailsSchema(),
    }
    return schema_map.get(data["type"], None)


class ListRecord(Lister):
    """List edge records"""
    schema = schemas.RecordListSchema(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        domains = self.app.session.get('/edge/domains/{}/records'.format(parsed_args.domain))
        return domains


class ShowRecord(ShowOne):
    """Show domain details."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'record',
            metavar='<record>',
            help='edge record ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/records/{}'.format(parsed_args.domain, parsed_args.record)
        record = self.app.session.get(uri)
        self.schema = get_record_schema(record)
        return record


class DeleteRecord(Command):
    """Delete record."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'record',
            metavar='<record>',
            help='edge record ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/edge/domains/{}/records/{}'.format(parsed_args.domain, parsed_args.record)
        self.app.session.delete(uri)


class UpdateRecord(ShowOne):
    """Update record."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'record',
            metavar='<record>',
            help='edge record ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='Record name.',
            required=False,
        )
        parser.add_argument(
            '--ttl',
            metavar='<ttl>',
            help='Time to live.',
            choices=("2m", "10m", "30m", "1h", "3h", "10h",),
            required=False,
        )
        parser.add_argument(
            '--note',
            metavar='<note>',
            help='Note',
            required=False,
        )
        parser.add_argument(
            '--ip-address',
            metavar='<ip-address>',
            help='IP Address.',
            required=False,
        )

        parser.add_argument(
            '--content',
            metavar='<content>',
            help='Content.',
            required=False,
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Port.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            help='Weight.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--proto',
            metavar='<proto>',
            help='Proto.',
            required=False,
            choices=("_tcp", "_udp", "_tls"),
        )
        parser.add_argument(
            '--service',
            metavar='<service>',
            help='Service.',
            required=False,
        )
        parser.add_argument(
            '--target',
            metavar='<target>',
            help='Target.',
            required=False,
        )
        parser.add_argument(
            '--mail-server',
            metavar='<mail_server>',
            help='Mail server.',
            required=False,
        )
        parser.add_argument(
            '--priority',
            metavar='<priority>',
            help='Priority.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--proxy',
            metavar='<proxy>',
            help='proxy.',
            required=False,
            type=t_or_f_or_n,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/records/{}'.format(parsed_args.domain, parsed_args.record)
        payload = {
            key: value for key, value in vars(parsed_args).items()
            if value is not None and key in schemas.RecordListSchema.available_keys
        }
        record = self.app.session.patch(uri, payload)
        self.schema = get_record_schema(record)
        return record


class CreateRecord(ShowOne):
    """Create Record"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='Record name.',
            required=True,
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help='Record type.',
            choices=("A", "TXT", "CNAME", "MX", "SRV",),
            required=True,
            type=str.upper,
        )
        parser.add_argument(
            '--ttl',
            metavar='<ttl>',
            help='Time to live.',
            choices=("2m", "10m", "30m", "1h", "3h", "10h",),
            required=True,
        )
        parser.add_argument(
            '--note',
            metavar='<note>',
            help='Note',
            required=False,
        )
        parser.add_argument(
            '--ip-address',
            metavar='<ip-address>',
            help='IP Address.',
            required=False,
        )

        parser.add_argument(
            '--content',
            metavar='<content>',
            help='Content.',
            required=False,
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Port.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            help='Weight.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--proto',
            metavar='<proto>',
            help='Proto.',
            required=False,
            choices=("_tcp", "_udp", "_tls"),
        )
        parser.add_argument(
            '--service',
            metavar='<service>',
            help='Service.',
            required=False,
        )
        parser.add_argument(
            '--target',
            metavar='<target>',
            help='Target.',
            required=False,
        )
        parser.add_argument(
            '--mail-server',
            metavar='<mail_server>',
            help='Mail server.',
            required=False,
        )
        parser.add_argument(
            '--priority',
            metavar='<priority>',
            help='Priority.',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--proxy',
            metavar='<proxy>',
            help='proxy.',
            required=False,
            type=t_or_f_or_n,
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            key: value for key, value in vars(parsed_args).items()
            if value is not None and key in schemas.RecordListSchema.available_keys
        }
        try:
            payload = self._get_record_type_schema(payload["type"])().load(payload)
        except ValidationError as e:
            raise CLIError(self._handle_validation_error(payload["type"], e))
        record = self.app.session.post('/edge/domains/{}/records'.format(parsed_args.domain), payload)
        self.schema = get_record_schema(record)
        return record

    @staticmethod
    def _handle_validation_error(record_type: str, e: ValidationError):
        errors = []
        for key, value in e.messages.items():
            error = "".join(value)
            if error == "Unknown field.":
                msg = "can not use --{} with {} record type.".format(key, record_type)
            elif error == "Missing data for required field.":
                msg = "--{} is required by {} record type.".format(
                    key.replace("_", "-"),
                    record_type
                )
            else:
                raise NotImplementedError
            errors.append(dict(
                msg=msg
            ))
        return errors

    @staticmethod
    def _get_record_type_schema(record_type: str):
        record_schema_map = {
            "A": schemas.ARecordDetailsSchema,
            "TXT": schemas.TXTRecordDetailsSchema,
            "MX": schemas.MXRecordDetailsSchema,
            "CNAME": schemas.CNAMERecordDetailsSchema,
            "SRV": schemas.SRVRecordDetailsSchema,
        }
        return record_schema_map[record_type]


class ListUpstream(Lister):
    """List edge upstreams"""
    schema = schemas.UpstreamDetails(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        upstreams = self.app.session.get('/edge/domains/{}/upstreams'.format(parsed_args.domain))
        return upstreams


class ShowUpstream(ShowOne):
    """Show upstream details."""
    schema = schemas.UpstreamDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/upstreams/{}'.format(parsed_args.domain, parsed_args.upstream)
        upstream = self.app.session.get(uri)
        return upstream


class DeleteUpstream(Command):
    """Delete upstream."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/edge/domains/{}/upstreams/{}'.format(parsed_args.domain, parsed_args.upstream)
        self.app.session.delete(uri)


class UpdateUpstream(ShowOne):
    """Update upstream."""
    schema = schemas.UpstreamDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='upstream name.',
        )
        parser.add_argument(
            '--lb-method',
            metavar='<lb-method>',
            help='Load balancing method.',
            choices=("consistent_ip_hash", "round_robin",),
            type=str.lower,
        )
        parser.add_argument(
            '--keep-alive',
            metavar='<keep-alive>',
            help='keep alive time.',
        )
        parser.add_argument(
            '--ssl-policy',
            metavar='<ssl-policy>',
            help='SSL policy.',
            choices=("http", "https",),
            type=str.lower,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/upstreams/{}'.format(parsed_args.domain, parsed_args.upstream)
        payload = {}
        if parsed_args.name:
            payload["name"] = parsed_args.name
        if parsed_args.lb_method:
            payload["lb_method"] = parsed_args.lb_method
        if parsed_args.keep_alive:
            payload["keep_alive"] = parsed_args.keep_alive
        if parsed_args.ssl_policy:
            payload["ssl_policy"] = parsed_args.ssl_policy
        upstream = self.app.session.patch(uri, payload)
        return upstream


class CreateUpstream(ShowOne):
    """Create upstream"""
    schema = schemas.UpstreamDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='upstream name.',
            required=True,
        )
        parser.add_argument(
            '--lb-method',
            metavar='<lb-method>',
            help='Load balancing method.',
            choices=("consistent_ip_hash", "round_robin",),
            required=True,
            type=str.lower,
        )
        parser.add_argument(
            '--keep-alive',
            metavar='<keep-alive>',
            help='keep alive time.',
            required=True,
        )
        parser.add_argument(
            '--ssl-policy',
            metavar='<ssl-policy>',
            help='SSL policy.',
            choices=("http", "https",),
            required=True,
            type=str.lower,
        )
        return parser

    def get_data(self, parsed_args):
        url = '/edge/domains/{}/upstreams'.format(parsed_args.domain)
        payload = {
            "name": parsed_args.name,
            "lb_method": parsed_args.lb_method,
            "keep_alive": parsed_args.keep_alive,
            "ssl_policy": parsed_args.ssl_policy,
        }
        upstream = self.app.session.post(url, payload)
        return upstream


class ListUpstreamServer(Lister):
    """List edge upstream servers"""
    schema = schemas.UpstreamServerDetails(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
            required=True,
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        servers = self.app.session.get(
            '/edge/domains/{}/upstreams/{}/servers'.format(
                parsed_args.domain,
                parsed_args.upstream,
            ))
        return servers


class ShowUpstreamServer(ShowOne):
    """Show upstream server details."""
    schema = schemas.UpstreamServerDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'server',
            metavar='<server>',
            help='edge upstream server ID',
        )
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
            required=True,
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/upstreams/{}/servers/{}'.format(
            parsed_args.domain, parsed_args.upstream, parsed_args.server
        )
        server = self.app.session.get(uri)
        return server


class DeleteUpstreamServer(Command):
    """Delete upstream server."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'server',
            metavar='<server>',
            help='edge upstream server ID',
        )
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
            required=True,
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/edge/domains/{}/upstreams/{}/servers/{}'.format(
            parsed_args.domain, parsed_args.upstream, parsed_args.server
        )
        self.app.session.delete(uri)


class UpdateUpstreamServer(ShowOne):
    """Update upstream server."""
    schema = schemas.UpstreamServerDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'server',
            metavar='<server>',
            help='edge upstream server ID',
        )
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
            required=True,
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        parser.add_argument(
            '--ip-domain',
            metavar='<ip-domain>',
            help='Server ip domain.',
            required=True,
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Server port.',
            required=True,
            type=int,
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            help='server weight.',
            required=True,
            type=int,
        )
        parser.add_argument(
            '--fail-timeout',
            metavar='<fail-timeout>',
            help='Server fail timeout.',
            required=True,
            type=int,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/upstreams/{}/servers/{}'.format(
            parsed_args.domain, parsed_args.upstream, parsed_args.server
        )
        payload = {}
        if parsed_args.ip_domain:
            payload["ip_domain"] = parsed_args.ip_domain
        if parsed_args.port:
            payload["port"] = parsed_args.port
        if parsed_args.weight:
            payload["weight"] = parsed_args.weight
        if parsed_args.fail_timeout:
            payload["fail_timeout"] = parsed_args.fail_timeout
        server = self.app.session.patch(uri, payload)
        return server


class CreateUpstreamServer(ShowOne):
    """Create upstream server"""
    schema = schemas.UpstreamServerDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='edge upstream name or ID',
            required=True,
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        parser.add_argument(
            '--ip-domain',
            metavar='<ip-domain>',
            help='Server ip domain.',
            required=True,
        )
        parser.add_argument(
            '--port',
            metavar='<port>',
            help='Server port.',
            required=True,
            type=int,
        )
        parser.add_argument(
            '--weight',
            metavar='<weight>',
            help='server weight.',
            required=True,
            type=int,
        )
        parser.add_argument(
            '--fail-timeout',
            metavar='<fail-timeout>',
            help='Server fail timeout.',
            required=True,
            type=int,
        )
        return parser

    def get_data(self, parsed_args):
        url = '/edge/domains/{}/upstreams/{}/servers'.format(parsed_args.domain, parsed_args.upstream)
        payload = {
            "ip_domain": parsed_args.ip_domain,
            "port": parsed_args.port,
            "weight": parsed_args.weight,
            "fail_timeout": parsed_args.fail_timeout,
        }
        server = self.app.session.post(url, payload)
        return server


class ShowSSL(ShowOne):
    """Show ssl details."""
    schema = schemas.SSLDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='edge domain name ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/ssl'.format(parsed_args.domain)
        ssl = self.app.session.get(uri)
        return ssl


class UpdateSSL(ShowOne):
    """Update ssl."""
    schema = schemas.SSLDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='edge domain ID or name',
        )
        parser.add_argument(
            '--type',
            metavar='<type>',
            help='SSL type.',
            choices=("custom", "auto", ),
        )
        parser.add_argument(
            '--policy',
            metavar='<policy>',
            help='SSL policy.',
            choices=("normal", "strict",),
        )
        parser.add_argument(
            '--enable',
            metavar='<enable>',
            help='SSL enable.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--hsts',
            metavar='<hsts>',
            help='SSL hsts.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--https-redirect',
            metavar='<https-redirect>',
            help='SSL https redirect.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--ocsp-check',
            metavar='<ocsp-check>',
            help='SSL Ocsp',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--min-tls-versions',
            metavar='<min-tls-versions>',
            help='SSL Min TLS Versions.',
            choices=(
                'TLS_1_0',
                'TLS_1_1',
                'TLS_1_2',
                'TLS_1_3',
            ),
        )
        parser.add_argument(
            '--private-key',
            metavar='<private-key>',
            help='SSL private-key filename.',
        )
        parser.add_argument(
            '--public-key',
            metavar='<public-key>',
            help='SSL public-key filename.',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/ssl'.format(
            parsed_args.domain,
        )
        payload = {}
        if parsed_args.type:
            payload["type"] = parsed_args.type
        if parsed_args.policy:
            payload["policy"] = parsed_args.policy
        if parsed_args.enable is not None:
            payload["enable"] = parsed_args.enable
        if parsed_args.hsts is not None:
            payload["hsts"] = parsed_args.hsts
        if parsed_args.https_redirect is not None:
            payload["https_redirect"] = parsed_args.https_redirect
        if parsed_args.ocsp_check is not None:
            payload["ocsp_check"] = parsed_args.ocsp_check
        if parsed_args.min_tls_versions is not None:
            payload["min_tls_versions"] = parsed_args.min_tls_versions
        if parsed_args.public_key:
            with open(os.path.expanduser(parsed_args.public_key)) as file_:
                payload["public_key"] = file_.read()
        if parsed_args.private_key:
            with open(os.path.expanduser(parsed_args.private_key)) as file_:
                payload["private_key"] = file_.read()

        server = self.app.session.patch(uri, payload)
        return server


class ListLocation(Lister):
    """List edge locations"""
    schema = schemas.LocationDetails(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        locations = self.app.session.get('/edge/domains/{}/locations'.format(parsed_args.domain))
        return locations


class ShowLocation(ShowOne):
    """Show location details."""
    schema = schemas.LocationDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'location',
            metavar='<location>',
            help='edge location name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/locations/{}'.format(parsed_args.domain, parsed_args.location)
        location = self.app.session.get(uri)
        return location


class DeleteLocation(Command):
    """Delete location."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'location',
            metavar='<location>',
            help='edge location name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/edge/domains/{}/locations/{}'.format(parsed_args.domain, parsed_args.location)
        self.app.session.delete(uri)


class UpdateLocation(ShowOne):
    """Update location."""
    schema = schemas.LocationDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'location',
            metavar='<location>',
            help='edge location name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='upstream name.',
        )
        parser.add_argument(
            '--path',
            metavar='<path>',
            help='edge location path.',
        )
        parser.add_argument(
            '--path-case-sensitive',
            metavar='<path-case-sensitive>',
            help='path case sensitive enabled.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='location upstream.',
        )
        parser.add_argument(
            '--origin-headers',
            metavar='<origin-headers>',
            help='location origin headers.',
        )
        parser.add_argument(
            '--response-headers',
            metavar='<response-headers>',
            help='location response headers.',
        )
        parser.add_argument(
            '--cache-enabled',
            metavar='<cache-enabled>',
            help='location cache enabled.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--cache-ttl',
            metavar='<cache-ttl>',
            help='location cache time to live.',
            choices=("2m", "10m", "30m", "1h", "3h", "10h", "1d", "2d", "1w", "1M",),
        )
        parser.add_argument(
            '--cache-key',
            metavar='<cache-key>',
            help='location cache key.',
            choices=("u", "uq", "uqc",),
            type=str.lower,
        )
        parser.add_argument(
            '--cache-cookie-name',
            metavar='<cache-cookie-name>',
            help='location cache cookie name.',
        )
        parser.add_argument(
            '--cache-zone',
            metavar='<cache-zone>',
            help='location cache zone id.',
        )
        parser.add_argument(
            '--secure-link-enable',
            metavar='<secure-link-enable>',
            help='secure link enabled.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--secure-link-secret',
            metavar='<secure-link-secret>',
            help='secure link secret.',
        )
        parser.add_argument(
            '--redirect-enable',
            metavar='<redirect-enable>',
            help='redirect enabled.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--redirect-url',
            metavar='<redirect-url>',
            help='redirect url.',
        )
        parser.add_argument(
            '--redirect-status-code',
            metavar='<redirect-status-code>',
            help='redirect status code.',
            choices=("permanent", "temporary",),
            type=str.lower,
        )
        parser.add_argument(
            '--rate-limit',
            metavar='<rate-limit>',
            help='location rate limit id.',
        )
        return parser

    def get_data(self, parsed_args):
        redirect_status_code_dict = {
            "permanent": 301,
            "temporary": 302,
        }
        uri = '/edge/domains/{}/locations/{}'.format(parsed_args.domain, parsed_args.location)
        payload = {}

        if parsed_args.name:
            payload["name"] = parsed_args.name
        if parsed_args.path:
            payload["path"] = parsed_args.path
        if parsed_args.path_case_sensitive is not None:
            payload["path_case_sensitive"] = parsed_args.path_case_sensitive
        if parsed_args.upstream:
            payload["upstream_id"] = parsed_args.upstream
        if parsed_args.origin_headers:
            if str(parsed_args.origin_headers).lower() == "null":
                payload["origin_headers"] = []
            else:
                with open(os.path.expanduser(parsed_args.origin_headers)) as file_:
                    origin_headers_content = file_.read()
                    try:
                        payload["origin_headers"] = json.loads(origin_headers_content)
                    except json.decoder.JSONDecodeError as e:
                        raise CLIError(
                            [dict(msg="origin-headers is not a valid json")])
        if parsed_args.response_headers:
            if str(parsed_args.response_headers).lower() == "null":
                payload["response_headers"] = []
            else:
                with open(os.path.expanduser(parsed_args.response_headers)) as file_:
                    response_headers_content = file_.read()
                    try:
                        payload["response_headers"] = json.loads(response_headers_content)
                    except json.decoder.JSONDecodeError as e:
                        raise CLIError(
                            [dict(msg="response-headers is not a valid json")])
        if parsed_args.cache_enabled is not None:
            payload["cache_enabled"] = parsed_args.cache_enabled
        if parsed_args.cache_ttl:
            payload["cache_ttl"] = parsed_args.cache_ttl
        if parsed_args.cache_key:
            payload["cache_key"] = parsed_args.cache_key
        if parsed_args.cache_cookie_name:
            payload["cache_cookie_name"] = parsed_args.cache_cookie_name
        if parsed_args.cache_zone:
            payload["cache_zone"] = parsed_args.cache_zone
        if parsed_args.secure_link_enable is not None:
            payload["secure_link_enable"] = parsed_args.secure_link_enable
        if parsed_args.secure_link_secret:
            payload["secure_link_secret"] = parsed_args.secure_link_secret
        if parsed_args.redirect_enable is not None:
            payload["redirect_enable"] = parsed_args.redirect_enable
            if parsed_args.redirect_enable is True:
                if not parsed_args.redirect_url:
                    raise CLIError(
                        [dict(
                            msg="You need to specify redirect_url "
                                "when redirect_enable switch is True"
                        )]
                    )
                if not parsed_args.redirect_status_code:
                    payload["redirect_status_code"] = 302
        if parsed_args.redirect_url:
            payload["redirect_url"] = parsed_args.redirect_url
        if parsed_args.redirect_status_code:
            payload["redirect_status_code"] = redirect_status_code_dict[
                parsed_args.redirect_status_code
            ]
        if parsed_args.rate_limit:
            payload["rate_limit_id"] = parsed_args.rate_limit
        location = self.app.session.patch(uri, payload)
        return location


class CreateLocation(ShowOne):
    """Create location"""
    schema = schemas.LocationDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='upstream name.',
            required=True,
        )
        parser.add_argument(
            '--path',
            metavar='<path>',
            help='edge location path.',
            required=True,
        )
        parser.add_argument(
            '--path-case-sensitive',
            metavar='<path-case-sensitive>',
            help='path case sensitive enabled.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--upstream',
            metavar='<upstream>',
            help='location upstream id.',
            required=True,
        )
        parser.add_argument(
            '--origin-headers',
            metavar='<origin-headers>',
            help='location origin headers.',
        )
        parser.add_argument(
            '--response-headers',
            metavar='<response-headers>',
            help='location response headers.',
        )
        parser.add_argument(
            '--cache-enabled',
            metavar='<cache-enabled>',
            help='location cache enabled.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--cache-ttl',
            metavar='<cache-ttl>',
            help='location cache time to live.',
            choices=("2m", "10m", "30m", "1h", "3h", "10h", "1d", "2d", "1w", "1M",),
        )
        parser.add_argument(
            '--cache-key',
            metavar='<cache-key>',
            help='location cache key.',
            choices=("u", "uq", "uqc",),
            type=str.lower,
        )
        parser.add_argument(
            '--cache-cookie-name',
            metavar='<cache-cookie-name>',
            help='location cache cookie name.',
        )
        parser.add_argument(
            '--cache-zone',
            metavar='<cache-zone>',
            help='location cache zone id.',
        )
        parser.add_argument(
            '--secure-link-enable',
            metavar='<secure-link-enable>',
            help='secure link enabled.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--secure-link-secret',
            metavar='<secure-link-secret>',
            help='secure link secret.',
        )
        parser.add_argument(
            '--redirect-enable',
            metavar='<redirect-enable>',
            help='redirect enabled.',
            type=t_or_f_or_n,
        )
        parser.add_argument(
            '--redirect-url',
            metavar='<redirect-url>',
            help='redirect url.',
        )
        parser.add_argument(
            '--redirect-status-code',
            metavar='<redirect-status-code>',
            help='redirect status code.',
            choices=("permanent", "temporary",),
            type=str.lower,
        )
        parser.add_argument(
            '--rate-limit',
            metavar='<rate-limit>',
            help='location rate limit id.',
        )
        return parser

    def get_data(self, parsed_args):
        redirect_status_code_dict = {
            "permanent": 301,
            "temporary": 302,
        }
        url = '/edge/domains/{}/locations'.format(parsed_args.domain)
        payload = {
            "name": parsed_args.name,
            "path": parsed_args.path,
            "upstream_id": parsed_args.upstream,
            "redirect_enable": False,
            "redirect_status_code": 302,
        }
        if parsed_args.path_case_sensitive is not None:
            payload["path_case_sensitive"] = parsed_args.path_case_sensitive
        if parsed_args.origin_headers:
            with open(os.path.expanduser(parsed_args.origin_headers)) as file_:
                origin_headers_content = file_.read()
                try:
                    payload["origin_headers"] = json.loads(origin_headers_content)
                except json.decoder.JSONDecodeError as e:
                    raise CLIError(
                        [dict(msg="origin-headers is not a valid json")])
        if parsed_args.response_headers:
            with open(os.path.expanduser(parsed_args.response_headers)) as file_:
                response_headers_content = file_.read()
                try:
                    payload["response_headers"] = json.loads(response_headers_content)
                except json.decoder.JSONDecodeError as e:
                    raise CLIError(
                        [dict(msg="response-headers is not a valid json")])
        if parsed_args.cache_enabled is not None:
            payload["cache_enabled"] = parsed_args.cache_enabled
        if parsed_args.cache_ttl:
            payload["cache_ttl"] = parsed_args.cache_ttl
        if parsed_args.cache_key:
            payload["cache_key"] = parsed_args.cache_key
        if parsed_args.cache_cookie_name:
            payload["cache_cookie_name"] = parsed_args.cache_cookie_name
        if parsed_args.cache_zone:
            payload["cache_zone"] = parsed_args.cache_zone
        if parsed_args.secure_link_enable is not None:
            payload["secure_link_enable"] = parsed_args.secure_link_enable
        if parsed_args.secure_link_secret:
            payload["secure_link_secret"] = parsed_args.secure_link_secret
        if parsed_args.redirect_enable is not None:
            payload["redirect_enable"] = parsed_args.redirect_enable
            if parsed_args.redirect_enable is True:
                if parsed_args.redirect_url:
                    payload["redirect_url"] = parsed_args.redirect_url
                else:
                    raise CLIError(
                        [dict(
                            msg="You need to specify redirect_url "
                                "when redirect_enable switch is True"
                        )]
                    )
            if parsed_args.redirect_status_code:
                payload["redirect_status_code"] = redirect_status_code_dict[
                    parsed_args.redirect_status_code
                ]
        if parsed_args.rate_limit:
            payload["rate_limit_id"] = parsed_args.rate_limit
        location = self.app.session.post(url, payload)
        return location


class ListFirewall(Lister):
    """List edge firewalls"""
    schema = schemas.EdgeFirewallDetails(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        firewalls = self.app.session.get('/edge/domains/{}/firewalls'.format(parsed_args.domain))
        return firewalls


class ShowFirewall(ShowOne):
    """Show firewall details."""
    schema = schemas.EdgeFirewallDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'firewall',
            metavar='<firewall>',
            help='edge firewall ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/firewalls/{}'.format(parsed_args.domain, parsed_args.firewall)
        firewall = self.app.session.get(uri)
        return firewall


class DeleteFirewall(Command):
    """Delete firewall."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'firewall',
            metavar='<firewall>',
            help='edge firewall ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/edge/domains/{}/firewalls/{}'.format(parsed_args.domain, parsed_args.firewall)
        self.app.session.delete(uri)


class UpdateFirewall(ShowOne):
    """Update firewall."""
    schema = schemas.EdgeFirewallDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'firewall',
            metavar='<firewall>',
            help='edge firewall ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--input',
            metavar='<input>',
            help='firewall rule input type.',
            choices=("ip", "asn", "country", "continent",),
            type=str.lower,
        )
        parser.add_argument(
            '--value',
            metavar='<value>',
            help='firewall rule value path.',
        )
        parser.add_argument(
            '--action',
            metavar='<action>',
            help='firewall rule action.',
            choices=("allow", "block", "javascript_challenge", "captcha_challenge",),
            type=str.lower,
        )
        parser.add_argument(
            '--operator',
            metavar='<operator>',
            help='firewall rule operator',
            choices=("eq", "neq",),
            type=str.lower,
        )
        parser.add_argument(
            '--location',
            metavar='<location>',
            help='firewall location id.',
        )
        parser.add_argument(
            '--priority',
            metavar='<priority>',
            help='firewall rule priority.',
            type=int,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/firewalls/{}'.format(parsed_args.domain, parsed_args.firewall)
        payload = {}
        if parsed_args.input:
            payload["input"] = parsed_args.input
        if parsed_args.value:
            payload["value"] = parsed_args.value
        if parsed_args.action:
            payload["action"] = parsed_args.action
        if parsed_args.operator:
            payload["operator"] = parsed_args.operator
        if parsed_args.location:
            payload["location"] = parsed_args.location
        if parsed_args.priority:
            payload["priority"] = parsed_args.priority
        location = self.app.session.patch(uri, payload)
        return location


class CreateFirewall(ShowOne):
    """Create firewall"""
    schema = schemas.EdgeFirewallDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--input',
            metavar='<input>',
            help='firewall rule input type.',
            choices=("ip", "asn", "country", "continent",),
            type=str.lower,
            required=True,
        )
        parser.add_argument(
            '--value',
            metavar='<value>',
            help='firewall rule value path.',
            required=True,
        )
        parser.add_argument(
            '--action',
            metavar='<action>',
            help='firewall rule action.',
            choices=("allow", "block", "javascript_challenge", "captcha_challenge",),
            type=str.lower,
            required=True,
        )
        parser.add_argument(
            '--operator',
            metavar='<operator>',
            help='firewall rule operator',
            choices=("eq", "neq",),
            type=str.lower,
            required=True,
        )
        parser.add_argument(
            '--location',
            metavar='<location>',
            help='firewall location id.',
            required=True,
        )
        parser.add_argument(
            '--priority',
            metavar='<priority>',
            help='firewall rule priority.',
            type=int,
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        url = '/edge/domains/{}/firewalls'.format(parsed_args.domain)
        payload = {
            "input": parsed_args.input,
            "value": parsed_args.value,
            "action": parsed_args.action,
            "operator": parsed_args.operator,
            "location_id": parsed_args.location,
            "priority": parsed_args.priority,
        }
        location = self.app.session.post(url, payload)
        return location


class ListCacheZone(Lister):
    """List edge cache zones"""
    schema = schemas.CacheZoneList(many=True)

    def get_data(self, parsed_args):
        domains = self.app.session.get('/edge/cache-zones')
        return domains


class ShowGeneralSetting(ShowOne):
    """Show general setting details."""
    schema = schemas.GeneralSettingSchema()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='edge domain name ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/general-setting'.format(parsed_args.domain)
        general_setting = self.app.session.get(uri)
        return general_setting


class UpdateGeneralSetting(ShowOne):
    """Update general setting."""
    schema = schemas.GeneralSettingSchema()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='edge domain ID or name',
        )
        parser.add_argument(
            '--developer-mode',
            metavar='<developer-mode>',
            help='General setting developer mode.',
            type=t_or_f_or_n,
            required=False,
        )
        parser.add_argument(
            '--maintenance-mode',
            metavar='<maintenance-mode>',
            help='General setting maintenance mode.',
            type=t_or_f_or_n,
            required=False,
        )
        parser.add_argument(
            '--redirect-to-www',
            metavar='<redirect-to-www>',
            help='General setting redirect to www.',
            type=t_or_f_or_n,
            required=False,
        )
        parser.add_argument(
            '--ip-geolocation',
            metavar='<ip-geolocation>',
            help='General setting ip geo location.',
            type=t_or_f_or_n,
            required=False,
        )
        parser.add_argument(
            '--intercept-errors',
            metavar='<intercept_errors>',
            help='General setting intercepts errors.',
            type=t_or_f_or_n,
            required=False,
        )
        parser.add_argument(
            '--max-upload-size',
            metavar='<max-upload-size>',
            help='General setting max upload size.',
            type=int,
            required=False,
        )
        parser.add_argument(
            '--custom-host-header',
            metavar='<custom-host-header>',
            help='General setting custom host header.',
            type=str,
            required=False,
        )
        parser.add_argument(
            '--origin-headers',
            metavar='<origin-headers>',
            help='location origin headers.',
            required=False,
        )
        parser.add_argument(
            '--response-headers',
            metavar='<response-headers>',
            help='location response headers.',
            required=False,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/general-setting'.format(
            parsed_args.domain,
        )
        payload = {}
        if parsed_args.developer_mode is not None:
            payload["developer_mode"] = parsed_args.developer_mode
        if parsed_args.maintenance_mode is not None:
            payload["maintenance_mode"] = parsed_args.maintenance_mode
        if parsed_args.redirect_to_www is not None:
            payload["redirect_to_www"] = parsed_args.redirect_to_www
        if parsed_args.ip_geolocation is not None:
            payload["ip_geolocation"] = parsed_args.ip_geolocation
        if parsed_args.intercept_errors is not None:
            payload["intercept_errors"] = parsed_args.intercept_errors
        if parsed_args.max_upload_size is not None:
            payload["max_upload_size"] = parsed_args.max_upload_size
        if parsed_args.custom_host_header:
            payload["custom_host_header"] = parsed_args.custom_host_header
        if parsed_args.origin_headers:
            with open(os.path.expanduser(parsed_args.origin_headers)) as file_:
                origin_headers_content = file_.read()
                try:
                    payload["origin_headers"] = json.loads(origin_headers_content)
                except json.decoder.JSONDecodeError as e:
                    raise CLIError(
                        [dict(msg="origin-headers is not a valid json")])
        if parsed_args.response_headers:
            with open(os.path.expanduser(parsed_args.response_headers)) as file_:
                response_headers_content = file_.read()
                try:
                    payload["response_headers"] = json.loads(response_headers_content)
                except json.decoder.JSONDecodeError as e:
                    raise CLIError(
                        [dict(msg="response-headers is not a valid json")])
        server = self.app.session.patch(uri, payload)
        return server


class PurgeCache(Command):
    """purge cache"""
    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'domain',
            metavar='<domain>',
            help='edge domain ID or name',
        )
        parser.add_argument(
            '--url',
            metavar='<url>',
            help='url to purge cache',
            required=True,
        )
        parser.add_argument(
            '--method',
            metavar='<method>',
            help='Url method purge cache.',
            choices=("GET", "HEAD", "OPTIONAL",),
            type=str.upper,
            required=False,
        )
        parser.add_argument(
            '--cookies',
            metavar='<cookies>',
            help='purge cache url cookies path.',
            required=False,
        )

        return parser

    def take_action(self, parsed_args):
        uri = '/edge/domains/{}/purge-cache'.format(
            parsed_args.domain,
        )
        payload = {}
        if parsed_args.url:
            payload["url"] = parsed_args.url
        if parsed_args.method:
            payload["method"] = parsed_args.method
        if parsed_args.cookies:
            with open(os.path.expanduser(parsed_args.cookies)) as file_:
                cookie_content = file_.read()
                try:
                    payload["cookies"] = json.loads(cookie_content)
                except json.decoder.JSONDecodeError as e:
                    raise CLIError(
                        [dict(msg="cookies is not a valid json")])
        server = self.app.session.post(uri, payload)
        return server


class ListRateLimit(Lister):
    """List edge rate limits"""
    schema = schemas.RateLimitDetails(many=True)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        rate_limits = self.app.session.get('/edge/domains/{}/rate-limits'.format(parsed_args.domain))
        return rate_limits


class ShowRateLimit(ShowOne):
    """Show rate limit details."""
    schema = schemas.RateLimitDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'rate_limit',
            metavar='<rate-limit>',
            help='edge rate limit name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain ID',
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/rate-limits/{}'.format(parsed_args.domain, parsed_args.rate_limit)
        rate_limit = self.app.session.get(uri)
        return rate_limit


class DeleteRateLimit(Command):
    """Delete rate limit."""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'rate_limit',
            metavar='<rate-limit>',
            help='edge rate limit name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID',
            required=True,
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/edge/domains/{}/rate-limits/{}'.format(parsed_args.domain, parsed_args.rate_limit)
        self.app.session.delete(uri)


class UpdateRateLimit(ShowOne):
    """Update rate limit."""
    schema = schemas.RateLimitDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            'rate_limit',
            metavar='<rate-limit>',
            help='edge rate limit name or ID',
        )
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='rate limit name.',
        )
        parser.add_argument(
            '--requests',
            metavar='<requests>',
            help='edge rate limit requests.',
            type=int,
        )
        parser.add_argument(
            '--burst',
            metavar='<burst>',
            help='rate limit burst type.',
            type=int,
        )
        parser.add_argument(
            '--exclusions',
            metavar='<exclusions>',
            help='List rate limit exclusions.',
            nargs='+',
        )
        parser.add_argument(
            '--time',
            metavar='<time>',
            help='rate limit time.',
            choices=("s", "m",),
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/edge/domains/{}/rate-limits/{}'.format(parsed_args.domain, parsed_args.rate_limit)
        payload = {}
        if parsed_args.name:
            payload["name"] = parsed_args.name
        if parsed_args.requests:
            payload["requests"] = parsed_args.requests
        if parsed_args.burst:
            payload["burst"] = parsed_args.burst
        if parsed_args.time:
            payload["time"] = parsed_args.time
        if parsed_args.exclusions:
            payload["exclusion_list"] = parsed_args.exclusions
        rate_limit = self.app.session.patch(uri, payload)
        return rate_limit


class CreateRateLimit(ShowOne):
    """Create rate limit"""
    schema = schemas.RateLimitDetails()

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--domain',
            metavar='<domain>',
            help='edge domain Name or ID.',
            required=True,
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='rate limit name.',
            required=True,
        )
        parser.add_argument(
            '--requests',
            metavar='<requests>',
            help='edge rate limit requests.',
            type=int,
            required=True,
        )
        parser.add_argument(
            '--burst',
            metavar='<burst>',
            help='rate limit burst type.',
            type=int,
            required=True,
        )
        parser.add_argument(
            '--exclusions',
            metavar='<exclusions>',
            help='List rate limit exclusions.',
            nargs='+',
        )
        parser.add_argument(
            '--time',
            metavar='<time>',
            help='rate limit time.',
            choices=("s", "m",),
            required=True,
        )
        return parser

    def get_data(self, parsed_args):
        url = '/edge/domains/{}/rate-limits'.format(parsed_args.domain)
        payload = {
            "name": parsed_args.name,
            "requests": parsed_args.requests,
            "burst": parsed_args.burst,
            "time": parsed_args.time,
        }
        if parsed_args.exclusions:
            payload["exclusion_list"] = parsed_args.exclusions
        rate_limit = self.app.session.post(url, payload)
        return rate_limit
