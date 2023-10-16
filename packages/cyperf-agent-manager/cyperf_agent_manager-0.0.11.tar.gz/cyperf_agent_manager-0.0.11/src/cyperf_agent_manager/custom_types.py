import click
from typing import Any, List, Tuple
from click_params import DOMAIN, IP_ADDRESS

class NetworkAddress(click.ParamType):
    name = 'NETWORK ADDRESS'

    def convert(self, value, param, ctx):
        try:
            return f'{DOMAIN.convert (value, param, ctx)}'
        except click.exceptions.BadParameter as e:
            pass

        try:
            return f'{IP_ADDRESS.convert (value, param, ctx)}'
        except click.exceptions.BadParameter as e:
            self.fail(f'{value} is neither a valid IP address nor a valid domain name', param, ctx)

    def __repr__(self):
        return 'Network Address'

NETADDR = NetworkAddress()

class NetworkAddressList(click.ParamType):
    name = 'NETWORK ADDRESS LIST'

    def __init__(self):
        self.error_msg = 'These items are not %s value: {errors}' % NETADDR.name

    def _strip_separator(self, value: str) -> str:
        return value.strip(',;: ')

    def _convert_expression_to_list(self, value: str) -> Tuple[List[str], Any]:
        errors = []
        converted_addrs = []
        for ip1 in value.split():
            for ip2 in ip1.split(','):
                for ip3 in ip2.split(';'):
                    for ip4 in ip3.split(':'):
                        if not ip4:
                            continue
                        try:
                            converted_addrs.append (NETADDR.convert(ip4, None, None))
                        except click.BadParameter:
                            errors.append(ip4)

        return errors, converted_addrs

    def convert(self, value, param, ctx):
        if isinstance(value, list):
            return value

        if value == '':
            return []

        value = self._strip_separator(value)
        errors, converted_list = self._convert_expression_to_list(value)
        if errors:
            self.fail(self.error_msg.format(errors=errors), param, ctx)

        return converted_list

    def __repr__(self):
        return 'Network Address List'

NETADDRLIST = NetworkAddressList()

class OptionalPassword(click.Option):
    override_flag = 'override_password'

    def __init__(self, *args, **kwargs):
        kwargs['prompt'] = kwargs.get('prompt', True)
        super(OptionalPassword, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if OptionalPassword.override_flag not in opts or opts[OptionalPassword.override_flag] == False:
            self.prompt = None

        return super(OptionalPassword, self).handle_parse_result(ctx, opts, args)
