# Copyright (c) 2015 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


import json
import sys
import textwrap

from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter

import qumulo.lib.opts
import qumulo.lib.util
import qumulo.rest.dns as dns

from qumulo.lib.opts import str_decode
from qumulo.rest.dns import ApiDnsClearCache

# XXX: Please add types to the functions in this file. Static type checking in
# Python prevents bugs!
# mypy: ignore-errors
from qumulo.rest_client import RestClient


class ResolveIpAddressesCommand(qumulo.lib.opts.Subcommand):
    NAME = 'dns_resolve_ips'
    SYNOPSIS = 'Resolve IP addresses to hostnames'

    @staticmethod
    def options(parser: ArgumentParser) -> None:
        parser.add_argument('--ips', required=True, nargs='+', help='IP addresses to resolve')
        parser.add_argument(
            '--dns-config-id',
            required=False,
            type=int,
            help=(
                'The DNS config ID used to resolve. If there is only one DNS config, this value is'
                ' optional.'
            ),
        )

    @staticmethod
    def main(rest_client: RestClient, args: Namespace) -> None:
        print(
            dns.resolve_ips_to_names(
                rest_client.conninfo,
                rest_client.credentials,
                args.ips,
                dns_config_id=args.dns_config_id,
            )
        )


class ResolveHostnamesCommand(qumulo.lib.opts.Subcommand):
    NAME = 'dns_resolve_hostnames'
    SYNOPSIS = 'Resolve hostnames to IP addresses'

    @staticmethod
    def options(parser: ArgumentParser) -> None:
        parser.add_argument('--hosts', required=True, nargs='+', help='Hostnames to resolve')
        parser.add_argument(
            '--dns-config-id',
            required=False,
            type=int,
            help=(
                'The DNS config ID used to resolve. If there is only one DNS config, this value is'
                ' optional.'
            ),
        )

    @staticmethod
    def main(rest_client: RestClient, args: Namespace) -> None:
        print(
            dns.resolve_names_to_ips(
                rest_client.conninfo,
                rest_client.credentials,
                args.hosts,
                dns_config_id=args.dns_config_id,
            )
        )


class ClearDnsCacheCommand(qumulo.lib.opts.Subcommand):
    NAME = 'dns_clear_cache'
    SYNOPSIS = 'Clear the local DNS cache for a specific DNS configuration.'

    @staticmethod
    def options(parser: ArgumentParser) -> None:
        parser.add_argument(
            '--dns-config-id',
            required=True,
            type=int,
            help='ID of the dns config of which the cache entries should be cleared.',
        )

        skip_args = parser.add_mutually_exclusive_group(required=False)

        skip_args.add_argument(
            '--skip-reverse-cache',
            action='store_true',
            default=False,
            help='When this flag is set, the reverse lookup cache is not cleared.',
        )

        skip_args.add_argument(
            '--skip-forward-cache',
            action='store_true',
            default=False,
            help='When this flag is set, the forward lookup cache is not cleared.',
        )

    @staticmethod
    def main(rest_client: RestClient, args: Namespace) -> None:
        options = ApiDnsClearCache(
            dns_config_id=args.dns_config_id,
            skip_forward_cache=args.skip_forward_cache,
            skip_reverse_cache=args.skip_reverse_cache,
        )
        dns.clear_cache(rest_client.conninfo, rest_client.credentials, options)


#  _             _
# | | ___   ___ | | ___   _ _ __
# | |/ _ \ / _ \| |/ / | | | '_ \
# | | (_) | (_) |   <| |_| | |_) |
# |_|\___/ \___/|_|\_\\__,_| .__/____
#                          |_| |_____|
#                           _     _
#   _____   _____ _ __ _ __(_) __| | ___  ___
#  / _ \ \ / / _ \ '__| '__| |/ _` |/ _ \/ __|
# | (_) \ V /  __/ |  | |  | | (_| |  __/\__ \
#  \___/ \_/ \___|_|  |_|  |_|\__,_|\___||___/
#  FIGLET: lookup_overrides
#


class DNSLookupOverridesGetCommand(qumulo.lib.opts.Subcommand):
    NAME = 'dns_get_lookup_overrides'
    SYNOPSIS = 'List the configured set of DNS lookup overrides.'
    DESCRIPTION = textwrap.dedent(
        """\
        List the configured set of DNS lookup overrides.

        These rules override any lookup results from the configured DNS servers
        and serve as static mappings between IP address and hostname."""
    )

    @staticmethod
    def main(rest_client: RestClient, _args: Namespace) -> None:
        print(dns.lookup_overrides_get(rest_client.conninfo, rest_client.credentials))


class DNSLookupOverridesSetCommand(qumulo.lib.opts.Subcommand):
    NAME = 'dns_set_lookup_overrides'
    SYNOPSIS = 'Replace the configured set of DNS lookup overrides.'
    DESCRIPTION = textwrap.dedent(
        """\
        Replace the configured set of DNS lookup overrides.

        These rules override any lookup results from the configured DNS
        servers and serve as static mappings between IP address and hostname.
        The provided overrides document should have the following structure:

        {
          "lookup_overrides": [
              {"ip_address": "1.2.3.4", "aliases": ["foo.com", "www.foo.com"]},
              {"ip_address": "2.3.4.5", "aliases": ["bar.com", "www.bar.com"]}
          ]
        }

        The first hostname in the "aliases" list is what will be resolved
        when doing reverse lookups from IP address to hostname."""
    )

    @staticmethod
    def options(parser: ArgumentParser) -> None:
        parser.formatter_class = RawDescriptionHelpFormatter
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--file', help='JSON-encoded file containing overrides.', type=str_decode
        )
        group.add_argument(
            '--stdin', action='store_true', help='Read JSON-encoded overrides from stdin'
        )

    @staticmethod
    def main(rest_client: RestClient, args: Namespace) -> None:
        infile = open(args.file, 'rb') if args.file else sys.stdin
        overrides = json.load(infile)
        dns.lookup_overrides_set(rest_client.conninfo, rest_client.credentials, overrides)
