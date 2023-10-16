from datetime import datetime

import tzlocal
import pytz
from marshmallow import Schema, fields, INCLUDE, post_dump

from digicloud import formatter


class APIDatetime(fields.Str):
    default_input_format = None  # Default format is  ISO_8601
    default_tz = pytz.UTC  # API uses UTC
    default_output_format = "%Y/%m/%d %H:%M"

    def _serialize(self, value, attr, obj, **kwargs):
        try:
            input_tz_datetime = self._parse_datetime_str(value)
            output_tz_datetime = self._get_user_tz_datetime(input_tz_datetime)
            return output_tz_datetime.strftime(self.default_output_format)
        except Exception:

            return "N/A"

    def _get_user_tz_datetime(self, dt_value):
        if self.metadata.get("as_timezone"):
            tz = pytz.timezone(self.metadata.get("as_timezone"))
        else:
            tz = tzlocal.get_localzone()
        return dt_value.astimezone(tz)

    def _parse_datetime_str(self, datetime_str):
        fmt = self.metadata.get("datetime_format", self.default_input_format)
        if fmt is None:
            naive_dt = datetime.fromisoformat(datetime_str)
        else:
            naive_dt = datetime.strptime(datetime_str, fmt)
        return naive_dt.replace(tzinfo=self.default_tz)  # API is always UTC


class NetworkList(Schema):
    name = fields.Str()
    description = fields.Str()
    subnets = fields.Function(lambda s: ", ".join([
        subnet['name'] for subnet in s.get('subnets', [])
    ]) or "N/A")
    has_gateway_interface = fields.Boolean()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class NetworkDetail(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    status = fields.Str()
    admin_state = fields.Str()
    subnets = fields.List(fields.Dict(), )
    mtu = fields.Int()
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class PublicIPList(Schema):
    name = fields.Str()
    public_ip_address = fields.Str()
    description = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class PublicIPDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    public_ip_address = fields.Str()
    status = fields.Str()
    router_id = fields.Str()
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class RouterList(Schema):
    name = fields.Str()
    description = fields.Str()
    has_gateway = fields.Str()
    gateway_address = fields.Str()
    admin_state = fields.Str()
    status = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class RouterDetails(RouterList):
    id = fields.Str()
    routes = fields.List(fields.Dict)

    class Meta:
        ordered = True


class RouterInterfaceList(Schema):
    id = fields.Str()
    network = fields.Str(attribute='network_name')
    subnet = fields.Str(attribute='subnet_name')
    ip_address = fields.Str()
    status = fields.Str()
    admin_state = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class RouterInterfaceDetails(RouterInterfaceList):
    firewalls = fields.List(fields.Str, attribute='security_groups')
    created_at = APIDatetime()

    class Meta:
        ordered = True


class FirewallRuleList(Schema):
    id = fields.Str()
    ethertype = fields.Str()
    direction = fields.Str()
    protocol = fields.Str()
    port_range_max = fields.Int()
    port_range_min = fields.Int()
    remote_ip_prefix = fields.Str()
    description = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class FirewallRuleDetails(Schema):
    id = fields.Str()
    firewall_id = fields.Str(attribute='security_group_id')
    ethertype = fields.Str()
    direction = fields.Str()
    protocol = fields.Str()
    port_range_max = fields.Int()
    port_range_min = fields.Int()
    remote_ip_prefix = fields.Str()
    description = fields.Str()
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class FirewallList(Schema):
    name = fields.Str()
    description = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class FirewallDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class ImageList(Schema):
    name = fields.Str()

    class Meta:
        ordered = True


class SSHKeyList(Schema):
    name = fields.Str()
    finger_print = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class SSHKeyDetails(SSHKeyList):
    id = fields.Str()
    updated_at = APIDatetime()
    created_at = APIDatetime()


class ImageDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    size = fields.Function(lambda v: formatter.format_size(v['size'], multiplier=1))
    default_user = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class InstanceList(Schema):
    name = fields.Str()
    description = fields.Str()
    type = fields.Str()
    addresses = fields.List(fields.Str())
    instance_type = fields.Str()
    status = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class ServerGroupDetails(Schema):
    class ServerGroupRules(Schema):
        max_server_per_host = fields.Int()

    id = fields.Str()
    name = fields.Str()
    policy = fields.Str()
    namespace_id = fields.Str()
    openstack_id = fields.Str()
    rules = fields.Nested(ServerGroupRules)
    members = fields.List(fields.Str())
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class InstanceDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    key_name = fields.Str()
    firewalls = fields.List(fields.Str(), attribute='security_groups')
    addresses = fields.List(fields.Str())
    access_ip = fields.Str()
    cores = fields.Str()
    memory = fields.Function(lambda v: formatter.format_ram(int(v['memory'])))
    root_volume_size = fields.Integer()
    root_volume_type = fields.Str()
    instance_type = fields.Str()
    status = fields.Str()
    type = fields.Str()
    os_name = fields.Str()
    os_username = fields.Str()
    server_groups = fields.List(fields.Str)
    namespace_id = fields.Str()
    description = fields.Str()
    created_by = fields.Str()
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class InstanceGroupDetails(Schema):
    name = fields.Str()
    instance_ids = fields.List(fields.Str())

    class Meta:
        ordered = True


class InstanceVolume(Schema):
    volume = fields.Str()
    instance = fields.Str()
    volume_type = fields.Str()
    device = fields.Str()
    size = fields.Function(lambda v: formatter.format_size(v['size']))

    class Meta:
        ordered = True


class InstanceInterface(Schema):
    id = fields.Str()
    net_id = fields.Str()
    mac_addr = fields.Str()
    port_state = fields.Str()
    fixed_ips = fields.List(fields.Dict())

    class Meta:
        ordered = True


class ListInstanceInterface(Schema):
    id = fields.Str()
    network_id = fields.Str()
    mac_address = fields.Str()
    port_state = fields.Str()
    public_ip = fields.Str()
    port_security_enabled = fields.Boolean()
    fixed_ips = fields.List(fields.Dict())

    class Meta:
        ordered = True


class InstanceInterfaceDetail(Schema):
    id = fields.Str()
    admin_state = fields.Str()
    mac_addr = fields.Str()
    port_security_enabled = fields.Bool()
    updated_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%SZ")
    created_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        ordered = True


class SnapshotList(Schema):
    name = fields.Str()
    description = fields.Str()
    status = fields.Str()
    updated_at = fields.Str()

    class Meta:
        ordered = True


class SnapshotDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    status = fields.Str()
    volume_ids = fields.List(fields.Str)
    created_at = fields.Str()
    updated_at = fields.Str()

    class Meta:
        ordered = True


class InstanceType(Schema):
    name = fields.Str()
    family = fields.Str()
    ram = fields.Function(lambda v: formatter.format_ram(v['ram']),
                          data_key="Memory (GB)", )
    disk = fields.Int(data_key="Disk (GB)")
    vcpus = fields.Str()

    class Meta:
        ordered = True


class RouterStaticRouteSchema(Schema):
    destination = fields.Str()
    nexthop = fields.Str()


class IPAllocationPool(Schema):
    start = fields.Str(required=True)
    end = fields.Str(required=True)


class SubnetList(Schema):
    name = fields.Str()
    description = fields.Str()
    cidr = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class SubnetDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    ip_version = fields.Str()
    network_id = fields.Str()
    gateway_ip = fields.Str()
    cidr = fields.Str()
    enable_dhcp = fields.Boolean()
    allocation_pools = fields.List(fields.Nested(IPAllocationPool))
    dns_nameservers = fields.List(fields.Str)
    host_routes = fields.List(fields.Nested(RouterStaticRouteSchema))
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class VolumeList(Schema):
    name = fields.Str()
    description = fields.Str()
    size = fields.Function(lambda v: formatter.format_size(v['size']))
    volume_type = fields.Str()
    status = fields.Str()
    attached_to = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class VolumeDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    size = fields.Function(lambda v: formatter.format_size(v['size']))
    volume_type = fields.Str()
    status = fields.Str()
    bootable = fields.Bool()
    instance = fields.Str(attribute='attachment_info.instance')
    device = fields.Str(attribute='attachment_info.device')
    attached_at = APIDatetime(
        attribute='attachment_info.attached_at',
        datetime_format="%Y-%m-%dT%H:%M:%S.%f")
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class NamespaceList(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    updated_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        ordered = True


class NamespaceDetails(NamespaceList):
    updated_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S")
    created_at = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        ordered = True


class NamespaceMemberList(Schema):
    id = fields.Str()
    email = fields.Function(lambda data: data['email'] if 'email' in data else data['invitee_email'])
    role = fields.Str(default="")
    membership = fields.Method("_determine_membership")

    def _determine_membership(self, data):
        if 'invitation_date' in data:
            invitation_date = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S").serialize('invitation_date', data)
            return f"invitation pending since {invitation_date}"
        else:
            return "member"

    class Meta:
        ordered = True


class UserInvitation(Schema):
    id = fields.Str()
    namespace = fields.Function(lambda invite: invite['namespace']['name'])
    invited_by = fields.Function(lambda invite: "{} {} ({})".format(
        invite['inviter']['first_name'],
        invite['inviter']['last_name'],
        invite['inviter']['email'],
    ))
    invitation_date = APIDatetime(datetime_format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        ordered = True


class NamespaceQuota(Schema):
    id = fields.Str()
    description = fields.Str()
    quota = fields.Int()
    used = fields.Int(allow_none=True)

    class Meta:
        ordered = True


class ErrorSchema(Schema):
    error_code = fields.Str()
    message = fields.Str()

    class Meta:
        unknown = INCLUDE


class ExternalVpnConnectionDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    auth_mode = fields.Str()
    psk = fields.Str(required=True)
    initiator = fields.Str()
    admin_state_up = fields.Bool()
    mtu = fields.Int()
    dpd = fields.Dict()
    peer_address = fields.Str()
    peer_id = fields.Str()
    ike_policy = fields.Str(required=True)
    ipsec_policy = fields.Str(required=True)
    # VPN service attrs
    router_id = fields.Function(lambda data: data["vpn_service"]["router_id"])
    # endpoint group attrs
    local_endpoint_group = fields.Function(
        lambda data: data["local_endpoint_group"]["endpoints"])
    peer_endpoint_group = fields.Function(
        lambda data: data["peer_endpoint_group"]["endpoints"])
    status = fields.Str()
    created_at = APIDatetime()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class ExternalVpnConnectionInList(Schema):
    name = fields.Str()
    description = fields.Str()
    initiator = fields.Str()
    admin_state_up = fields.Bool()
    mtu = fields.Int()
    auth_mode = fields.Str()
    peer_address = fields.Str()
    status = fields.Str()
    ipsec_policy = fields.Str()
    ike_policy = fields.Str()
    psk = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class QuotaRequest(Schema):
    quota_id = fields.Str()
    required_quota = fields.Int()
    status = fields.Str()
    updated_at = fields.Str()

    class Meta:
        ordered = True


class EdgeDomainList(Schema):
    id = fields.Str()
    name = fields.Str()
    status = fields.Str()
    record_count = fields.Integer()
    is_subdomain = fields.Boolean()
    ns_verification = fields.Str()

    class Meta:
        ordered = True


class EdgeDomainDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    is_subdomain = fields.Boolean()
    ns_verification = fields.Str()

    class Meta:
        ordered = True


class EdgeDomainPackageDetails(Schema):
    id = fields.Str()
    package_name_en = fields.Str()
    package_name_fa = fields.Str()

    class Meta:
        ordered = True


class DomainDNSSECDetails(Schema):
    dnssec = fields.Boolean()
    ds = fields.Str()

    class Meta:
        ordered = True


class RecordListSchema(Schema):
    available_keys = ("id", "name", "ttl", "note", "type", "ip_address", "proxy", "content", "port", "weight", "proto",
                      "service", "target", "priority", "mail_server",)
    id = fields.Str()
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    ttl = fields.Str(required=True)
    note = fields.Str(required=False)
    proxy = fields.Boolean(required=False)

    class Meta:
        ordered = True


class ARecordDetailsSchema(RecordListSchema):
    ip_address = fields.Str(required=True)
    proxy = fields.Boolean(required=False, missing=False)


class TXTRecordDetailsSchema(RecordListSchema):
    content = fields.Str(required=True)


class CNAMERecordDetailsSchema(RecordListSchema):
    target = fields.Str(required=True)
    proxy = fields.Boolean(required=False, missing=False)


class MXRecordDetailsSchema(RecordListSchema):
    mail_server = fields.Str(required=True)
    priority = fields.Integer(required=True)


class SRVRecordDetailsSchema(RecordListSchema):
    port = fields.Integer(required=True)
    weight = fields.Integer(required=True)
    proto = fields.Str(required=True)
    service = fields.Str(required=True)
    target = fields.Str(required=True)
    priority = fields.Integer(required=True)


class HealthCheckDetail(Schema):
    id = fields.Str()
    name = fields.Str()
    openstack_id = fields.Str()
    delay = fields.Int()
    max_retries = fields.Int()
    max_retries_down = fields.Int()
    timeout = fields.Int()
    type = fields.Str()
    operating_status = fields.Str()
    created_at = APIDatetime()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class BackendMemberDetail(Schema):
    id = fields.Str()
    ip_address = fields.Str()
    port = fields.Str()
    operating_status = fields.Str()
    created_at = APIDatetime()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class BackendDetail(Schema):
    id = fields.Str()
    algorithm = fields.Str()
    protocol = fields.Str()
    health_checks = fields.Function(lambda lb: [hc["id"] for hc in lb["health_checks"]])
    members = fields.Function(lambda lb: [member["id"] for member in lb["members"]])
    updated_at = APIDatetime()
    created_at = APIDatetime()

    class Meta:
        ordered = True


class FrontendDetail(Schema):
    id = fields.Str()
    port = fields.Str()
    protocol = fields.Str()
    timeout_client_data = fields.Int()
    timeout_tcp_inspect = fields.Int()
    timeout_member_connect = fields.Int()
    timeout_member_data = fields.Int()
    connection_limit = fields.Int()
    updated_at = APIDatetime()
    created_at = APIDatetime()
    default_backend_id = fields.Str()

    class Meta:
        ordered = True


class LoadBalancerList(Schema):
    name = fields.Str()
    description = fields.Str()
    ip_address = fields.Str()
    status = fields.Str()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class LoadBalancerDetail(Schema):
    id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    status = fields.Str()
    backends = fields.Function(lambda lb: [backend["id"] for backend in lb["backends"]])
    frontends = fields.Function(lambda lb: [frontend["id"] for frontend in lb["frontends"]])
    ip_address = fields.Str()
    created_at = APIDatetime()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class AccessKeyDetails(Schema):
    access_key = fields.Str()
    secret_key = fields.Str()
    is_active = fields.Boolean()

    class Meta:
        ordered = True


class UpstreamDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    lb_method = fields.Str()
    keep_alive = fields.Int()
    ssl_policy = fields.Str()
    servers_count = fields.Int()

    class Meta:
        ordered = True


class UpstreamServerDetails(Schema):
    id = fields.Str()
    ip_domain = fields.Str()
    port = fields.Int()
    weight = fields.Int()
    fail_timeout = fields.Int()

    class Meta:
        ordered = True


class SSLDetails(Schema):
    id = fields.Str()
    type = fields.Str()
    policy = fields.Str()
    enable = fields.Boolean()
    hsts = fields.Boolean()
    https_redirect = fields.Boolean()
    ocsp_check = fields.Boolean()
    min_tls_versions = fields.Str()
    expires_at = APIDatetime()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class LocationDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    path = fields.Str()
    path_case_sensitive = fields.Bool()
    upstream_id = fields.Str()
    origin_headers = fields.List(fields.Dict())
    response_headers = fields.List(fields.Dict())
    updated_at = APIDatetime()
    cache_enabled = fields.Bool()
    cache_ttl = fields.Str()
    cache_key = fields.Str()
    cache_cookie_name = fields.Str()
    cache_zone = fields.Str()
    secure_link_enable = fields.Bool()
    secure_link_secret = fields.Str()
    redirect_enable = fields.Bool()
    redirect_url = fields.Str()
    redirect_status_code = fields.Integer()
    rate_limit_id = fields.Str()

    @post_dump
    def convert_redirect_status_code(self, data, **kwargs):
        redirect_status_code_dict = {
            301: "permanent",
            302: "temporary",
        }
        data["redirect_status_code"] = redirect_status_code_dict[
            data["redirect_status_code"]
        ]

        if not data['redirect_enable']:
            data['redirect_status_code'] = None

        return data

    class Meta:
        ordered = True


class EdgeFirewallDetails(Schema):
    id = fields.Str()
    location_id = fields.Str()
    input = fields.Str()
    value = fields.Str()
    action = fields.Str()
    operator = fields.Str()
    priority = fields.Int()
    updated_at = APIDatetime()

    class Meta:
        ordered = True


class CacheZoneList(Schema):
    id = fields.Str()
    name = fields.Str()

    class Meta:
        ordered = True


class GeneralSettingSchema(Schema):
    id = fields.Str()
    origin_headers = fields.List(fields.Dict())
    response_headers = fields.List(fields.Dict())
    developer_mode = fields.Boolean()
    maintenance_mode = fields.Boolean()
    redirect_to_www = fields.Boolean()
    ip_geolocation = fields.Boolean()
    intercept_errors = fields.Boolean()
    max_upload_size = fields.Int()
    custom_host_header = fields.Str()
    created_at = fields.Str(dump_only=True)
    updated_at = fields.Str(dump_only=True)

    class Meta:
        ordered = True


class RateLimitDetails(Schema):
    id = fields.Str()
    name = fields.Str()
    time = fields.Str()
    requests = fields.Int()
    burst = fields.Int()
    exclusion_list = fields.List(fields.Str())
    created_at = fields.Str()
    updated_at = fields.Str()

    class Meta:
        ordered = True


def handle_nested_data_keys(data, nested_data, nested_key):
    if isinstance(nested_data, dict):
        for key, value in nested_data.items():
            data["%s_%s" % (nested_key, key)] = value
    elif isinstance(nested_data, list):
        for index, item in enumerate(nested_data):
            for key, value in item.items():
                data["%s_%s_%s" % (nested_key, index, key)] = value


class LifetimeSchema(Schema):
    units = fields.Str(required=True)
    value = fields.Int(required=True)


class IKEPolicySchema(Schema):
    name = fields.Str(required=True)
    id = fields.Str(dump_only=True)
    auth_algorithm = fields.Str(required=True)
    encryption_algorithm = fields.Str(required=True)
    pfs = fields.Str(required=True)
    lifetime = fields.Nested(LifetimeSchema)
    ike_version = fields.Str(required=True)
    updated_at = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)


class IPSecPolicySchema(Schema):
    name = fields.Str(required=True)
    id = fields.Str(dump_only=True)
    auth_algorithm = fields.Str(required=True)
    encapsulation_mode = fields.Str(required=True)
    encryption_algorithm = fields.Str(required=True)
    pfs = fields.Str(required=True)
    transform_protocol = fields.Str(required=True)
    lifetime = fields.Nested(LifetimeSchema)
    updated_at = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)


class PSKSchema(Schema):
    name = fields.Str(required=True)
    id = fields.Str(dump_only=True)
    psk = fields.Str(required=True)
    updated_at = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
