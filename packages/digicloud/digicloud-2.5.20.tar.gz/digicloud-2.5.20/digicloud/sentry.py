import os

from sentry_sdk import init, set_tag


def strip_sensitive_data(event, hint):
    if 'password' in str(event).lower():
        # skip event containing sensitive information
        return None
    if 'log_record' in hint:
        # Skip the logs
        return None
    return event


def initialize_sentry(app_version, server_name, **tags):
    init(
        os.getenv(
            'SENTRY_URL',
            'https://19915a046a814dfc9940040b4f8f83b3@yggdntry.digicloud.ir//2'
        ),
        traces_sample_rate=1.0,
        before_send=strip_sensitive_data,
        release=app_version,
        server_name=server_name,
        shutdown_timeout=1
    )
    for key, value in tags.items():
        set_tag(key, value)
