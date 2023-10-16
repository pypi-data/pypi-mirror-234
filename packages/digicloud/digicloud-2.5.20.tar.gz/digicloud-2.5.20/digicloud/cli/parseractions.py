import argparse

"""
Copied from osc-lib. If we need more tools from this library, we should install it.
"""


class MultiKeyValueAction(argparse.Action):
    """A custom action to parse arguments as key1=value1,key2=value2 pairs

    Ensure that ``dest`` is a list. The list will finally contain multiple
    dicts, with key=value pairs in them.

    NOTE: The arguments string should be a comma separated key-value pairs.
    And comma(',') and equal('=') may not be used in the key or value.
    """

    def __init__(self, option_strings, dest, nargs=None,
                 required_keys=None, optional_keys=None, **kwargs):
        """Initialize the action object, and parse customized options

        Required keys and optional keys can be specified when initializing
        the action to enable the key validation. If none of them specified,
        the key validation will be skipped.

        :param required_keys: a list of required keys
        :param optional_keys: a list of optional keys
        """
        if nargs:
            msg = "Parameter 'nargs' is not allowed, but got %s"
            raise ValueError(msg % nargs)

        super(MultiKeyValueAction, self).__init__(option_strings,
                                                  dest, **kwargs)

        # required_keys: A list of keys that is required. None by default.
        if required_keys and not isinstance(required_keys, list):
            msg = "'required_keys' must be a list"
            raise TypeError(msg)
        self.required_keys = set(required_keys or [])

        # optional_keys: A list of keys that is optional. None by default.
        if optional_keys and not isinstance(optional_keys, list):
            msg = "'optional_keys' must be a list"
            raise TypeError(msg)
        self.optional_keys = set(optional_keys or [])

    def __call__(self, parser, namespace, values, metavar=None):
        # Make sure we have an empty list rather than None
        if getattr(namespace, self.dest, None) is None:
            setattr(namespace, self.dest, [])

        params = {}
        for kv in values.split(','):
            # Add value if an assignment else raise ArgumentTypeError
            if '=' in kv:
                kv_list = kv.split('=', 1)
                # NOTE(qtang): Prevent null key setting in property
                if '' == kv_list[0]:
                    msg = "Each property key must be specified: %s"
                    raise argparse.ArgumentTypeError(msg % str(kv))
                else:
                    params.update([kv_list])
            else:
                msg = "Expected comma separated 'key=value' pairs, but got: %s"
                raise argparse.ArgumentTypeError(msg % str(kv))

        # Check key validation
        valid_keys = self.required_keys | self.optional_keys
        if valid_keys:
            invalid_keys = [k for k in params if k not in valid_keys]
            if invalid_keys:
                msg = "Invalid keys %(invalid_keys)s specified.\n " \
                      "Valid keys are: %(valid_keys)s"

                raise argparse.ArgumentTypeError(msg % {
                    'invalid_keys': ', '.join(invalid_keys),
                    'valid_keys': ', '.join(valid_keys),
                })

        if self.required_keys:
            missing_keys = [k for k in self.required_keys if k not in params]
            if missing_keys:
                msg = "Missing required keys %(missing_keys)s.\n" \
                      "Required keys are: %(required_keys)s"

                raise argparse.ArgumentTypeError(msg % {
                    'missing_keys': ', '.join(missing_keys),
                    'required_keys': ', '.join(self.required_keys),
                })

        # Update the dest dict
        getattr(namespace, self.dest, []).append(params)