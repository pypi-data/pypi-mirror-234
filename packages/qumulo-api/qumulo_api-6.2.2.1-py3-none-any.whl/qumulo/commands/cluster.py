# Copyright (c) 2013 Qumulo, Inc.
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


import argparse
import time

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

import qumulo.lib.opts
import qumulo.lib.util
import qumulo.rest.cluster as cluster
import qumulo.rest.node_state as node_state
import qumulo.rest.unconfigured_node_operations as unconfigured_node_operations

from qumulo.lib.auth import Credentials
from qumulo.lib.opts import str_decode
from qumulo.lib.request import Connection, RequestError, RestResponse
from qumulo.lib.util import are_you_sure
from qumulo.rest.cluster import get_node_replacement_plan, ModifyDryRunResponse, StripeConfig
from qumulo.rest_client import RestClient


class PasswordMismatchError(ValueError):
    pass


def get_admin_password(args: argparse.Namespace) -> str:
    """
    Get the effective admin_password to use for cluster creation

    If @a args.admin_password is None then we will prompt the user for a
    password and confirmation for the admin account (note that the entries
    will be hidden text)

    @param args.admin_password This is the passed in password from the CLI

    @return Effective admin_password to be used for cluster creation
    """
    password = args.admin_password

    if not password:
        password = qumulo.lib.opts.read_password(prompt='Enter password for Admin: ')
        confirm_password = qumulo.lib.opts.read_password(prompt='Confirm password for Admin: ')
        if password != confirm_password:
            raise PasswordMismatchError('The passwords do not match.')
        print('\n', end=' ')

    return password


def get_node_uuids_and_ips(
    args: argparse.Namespace, conninfo: Connection, credentials: Optional[Credentials]
) -> Tuple[List[str], List[str]]:
    """
    Get the actual set of node_uuids and node_ips to send to the rest call

    If the passed in args indicate that nodes should be auto-selected via the
    @a args.all_unconfigured then we perform an unconfigured nodes lookup
    and return all found nodes in the set of node_uuids.

    @param args.all_unconfigured Flag indicating whether or not we should
        utilize auto-node discovery
    @param args.node_uuids Set of manually specified node_uuids to use
    @param args.node_ips Set of manually specified node_ips to use
    @param conninfo Connection to use for the list_unconfigured_nodes rest call
    @param credentials These are the credentials to use for rest requests

    @return Returns tuple (node_uuids, node_ips) where these are the effective
        node_uuids and node_ips to use for the cluster_create rest call
    """
    node_uuids = []
    node_ips = []

    if args.all_unconfigured:
        res = unconfigured_node_operations.list_unconfigured_nodes(conninfo, credentials)

        nodes = res.data['nodes']
        node_uuids = [n['uuid'] for n in nodes]

        print(unconfigured_node_operations.fmt_unconfigured_nodes(res))
        if not qumulo.lib.opts.ask(
            'cluster create', f'\nUse above {len(nodes)} nodes to create cluster?'
        ):
            raise ValueError('No nodes selected')

    else:
        # For backward compatibility, we support multiple instances of
        # --node-uuids to append but we also would like to allow multiple
        # node uuids give to each instance.  Flatten resulting list of
        # lists.
        node_uuids = [x for sublist in args.node_uuids for x in sublist]
        node_ips = [x for sublist in args.node_ips for x in sublist]

    return node_uuids, node_ips


class ListNodesCommand(qumulo.lib.opts.Subcommand):
    NAME = 'nodes_list'
    SYNOPSIS = 'List nodes'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--node', help='Node ID')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if args.node is not None:
            print(cluster.list_node(rest_client.conninfo, rest_client.credentials, args.node))
        else:
            print(cluster.list_nodes(rest_client.conninfo, rest_client.credentials))


class GetClusterConfCommand(qumulo.lib.opts.Subcommand):
    NAME = 'cluster_conf'
    SYNOPSIS = 'Get the cluster config'

    @staticmethod
    def main(rest_client: RestClient, _args: argparse.Namespace) -> None:
        print(cluster.get_cluster_conf(rest_client.conninfo, rest_client.credentials))


class SetClusterConfCommand(qumulo.lib.opts.Subcommand):
    NAME = 'set_cluster_conf'
    SYNOPSIS = 'Set the cluster config'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--cluster-name', help='Cluster Name', required=True)

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        print(
            cluster.put_cluster_conf(
                rest_client.conninfo, rest_client.credentials, args.cluster_name
            )
        )


class SetSSLCertificateCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ssl_modify_certificate'
    SYNOPSIS = 'Set the SSL certificate chain and private key for the web UI and REST servers'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '-c',
            '--certificate',
            type=str_decode,
            required=True,
            help=(
                'SSL certificate chain in PEM format. Must contain '
                'entire certificate chain up to the root CA'
            ),
        )
        parser.add_argument(
            '-k',
            '--private-key',
            type=str_decode,
            required=True,
            help='RSA private key file in PEM format',
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        cert, key = None, None

        with open(args.certificate) as cert_f, open(args.private_key) as key_f:
            cert, key = cert_f.read(), key_f.read()

        print(cluster.set_ssl_certificate(rest_client.conninfo, rest_client.credentials, cert, key))


class SetSSLCACertificateCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ssl_modify_ca_certificate'
    SYNOPSIS = (
        'Set SSL CA certificate. This certificate is used to '
        'authenticate connections to external LDAP servers.'
    )

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '-c',
            '--certificate',
            type=str_decode,
            required=True,
            help='SSL CA certificate file in PEM format',
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        with open(args.certificate) as f:
            cert = f.read()
        print(cluster.set_ssl_ca_certificate(rest_client.conninfo, rest_client.credentials, cert))


class GetSSLCACertificateCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ssl_get_ca_certificate'
    SYNOPSIS = (
        'Get SSL CA certificate. This certificate is used to '
        'authenticate connections to external LDAP servers.'
    )

    @staticmethod
    def main(rest_client: RestClient, _args: argparse.Namespace) -> None:
        print(cluster.get_ssl_ca_certificate(rest_client.conninfo, rest_client.credentials))


class DeleteSSLCACertificateCommand(qumulo.lib.opts.Subcommand):
    NAME = 'ssl_delete_ca_certificate'
    SYNOPSIS = (
        'Delete SSL CA certificate. This certificate is used to '
        'authenticate connections to external LDAP servers.'
    )

    @staticmethod
    def main(rest_client: RestClient, _args: argparse.Namespace) -> None:
        cluster.delete_ssl_ca_certificate(rest_client.conninfo, rest_client.credentials)


class GetClusterSlotStatusCommand(qumulo.lib.opts.Subcommand):
    NAME = 'cluster_slots'
    SYNOPSIS = 'Get the cluster disk slots status'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--slot', help='Slot ID')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        if args.slot is not None:
            print(
                cluster.get_cluster_slot_status(
                    rest_client.conninfo, rest_client.credentials, args.slot
                )
            )
        else:
            print(cluster.get_cluster_slots_status(rest_client.conninfo, rest_client.credentials))


class SetClusterSlotConfigCommand(qumulo.lib.opts.Subcommand):
    NAME = 'cluster_slot_set_config'
    SYNOPSIS = (
        'Set the attributes for the given cluster slot. Currently only led_pattern may be set.'
    )

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--slot', required=True, help='Slot ID')
        led_group = parser.add_mutually_exclusive_group()
        led_group.add_argument(
            '--locate',
            help="Turn on the slot's locate LED.",
            dest='locate',
            action='store_const',
            const='LED_PATTERN_LOCATE',
        )
        led_group.add_argument(
            '--no-locate',
            help="Turn off the slot's locate LED.",
            dest='locate',
            action='store_const',
            const='LED_PATTERN_NORMAL',
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        print(
            cluster.set_cluster_slot_config(
                rest_client.conninfo, rest_client.credentials, args.slot, args.locate
            )
        )


class GetRestriperStatusCommand(qumulo.lib.opts.Subcommand):
    NAME = 'restriper_status'
    SYNOPSIS = 'Get restriper status'

    @staticmethod
    def main(rest_client: RestClient, _args: argparse.Namespace) -> None:
        print(cluster.get_restriper_status(rest_client.conninfo, rest_client.credentials))


class GetProtectionStatusCommand(qumulo.lib.opts.Subcommand):
    NAME = 'protection_status_get'
    SYNOPSIS = 'Get cluster protection status'

    @staticmethod
    def main(rest_client: RestClient, _args: argparse.Namespace) -> None:
        print(cluster.get_protection_status(rest_client.conninfo, rest_client.credentials))


class SetNodeUidLight(qumulo.lib.opts.Subcommand):
    NAME = 'set_node_identify_light'
    SYNOPSIS = 'Turn node identification light on or off'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--node', help='Node ID', required=True)
        parser.add_argument('light_state', choices=['on', 'off'], help='Should light be visible')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        light_visible = args.light_state == 'on'
        print(
            cluster.set_node_identify_light(
                rest_client.conninfo, rest_client.credentials, args.node, light_visible
            )
        )


class GetNodeChassisStatus(qumulo.lib.opts.Subcommand):
    NAME = 'node_chassis_status_get'
    SYNOPSIS = 'Get the status of node chassis'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--node', help='Node ID')

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        print(
            cluster.get_node_chassis_status(
                rest_client.conninfo, rest_client.credentials, args.node
            )
        )


def wait_for_first_quorum_following_cluster_create(
    conninfo: Connection, credentials: Optional[Credentials]
) -> None:
    """
    It's generally a good idea to wait for the first full quorum before doing anything with the
    cluster. If you don't, you may get disconnects and errors as the API switches from unconfigured
    to configured mode. You can also cause problems if you do things like `create && reboot` without
    waiting. This may cause filesystem creation to fail because the admin credentials were lost
    before ever being persisted to disk.

    Note that this method waits for a full quorum (not a degraded quorum) because the initial quorum
    for the cluster requires all nodes be present for filesystem creation, and it won't proceed
    until this is the case.
    """
    print('Cluster create command issued, waiting for initial quorum to form...')

    while True:
        try:
            state = node_state.get_node_state(conninfo, credentials).lookup('state')
            print(f'Initiator node quorum state: {state}')
            if state == 'ACTIVE':
                break
        except Exception as e:
            print(f'Transient error waiting for quorum: {e}')
        time.sleep(1)

    print('Success!')


class CreateCluster(qumulo.lib.opts.Subcommand):
    NAME = 'cluster_create'
    SYNOPSIS = 'Creates a Qumulo Cluster'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--cluster-name', '-n', help='Cluster Name', required=True)
        parser.add_argument('--admin-password', '-p', help='Administrator Password')
        parser.add_argument(
            '--blocks-per-stripe', help='Erasure coding stripe width', required=False, type=int
        )
        parser.add_argument(
            '--max-drive-failures',
            help='Maximum allowable drive failures',
            required=False,
            type=int,
        )
        parser.add_argument(
            '--max-node-failures', help='Maximum allowable node failures', required=False, type=int
        )
        parser.add_argument(
            '--accept-eula', help='Accept the EULA', dest='accept_eula', action='store_true'
        )
        parser.add_argument(
            '--reject-eula', help='Reject the EULA', dest='accept_eula', action='store_false'
        )
        parser.add_argument(
            '--host-instance-id',
            help='EC2 Instance ID of node receiving this request. AWS only.',
            default='',
        )

        node_group = parser.add_mutually_exclusive_group(required=True)
        node_group.add_argument(
            '--node-uuids', '-U', help='Cluster node UUIDs', action='append', default=[], nargs='+'
        )
        node_group.add_argument(
            '--node-ips',
            '-I',
            help='Cluster node IPv4 addresses',
            action='append',
            default=[],
            nargs='+',
        )
        node_group.add_argument(
            '--all-unconfigured',
            '-A',
            help='Use all discoverable unconfigured nodes to make cluster',
            action='store_true',
            default=False,
        )

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        admin_password = get_admin_password(args)
        node_uuids, node_ips = get_node_uuids_and_ips(
            args, rest_client.conninfo, rest_client.credentials
        )

        cluster.create_cluster(
            rest_client.conninfo,
            rest_client.credentials,
            cluster_name=args.cluster_name,
            admin_password=admin_password,
            host_instance_id=args.host_instance_id,
            node_uuids=node_uuids,
            node_ips=node_ips,
            blocks_per_stripe=args.blocks_per_stripe,
            max_drive_failures=args.max_drive_failures,
            max_node_failures=args.max_node_failures,
            eula_accepted=args.accept_eula,
        )

        wait_for_first_quorum_following_cluster_create(
            rest_client.conninfo, rest_client.credentials
        )


def _humanize_bytes(byte_size: int) -> Tuple[str, str]:
    base = 1000
    units = ['B', 'K', 'M', 'G', 'T', 'P']
    for i, unit in enumerate(units):
        val = round(byte_size / base ** i)
        if val < base:
            return str(val), unit
    return str(byte_size), 'B'


def humanize_decimal(byte_size: int) -> Tuple[str, str]:
    """
    Format number of bytes to a tuple of integer value and decimal unit (B, KB,
    MB, GB, TB, or PB) as strings.
    """
    val, unit = _humanize_bytes(byte_size)
    if unit != 'B':
        unit += 'B'
    return val, unit


def add_nodes_group(
    parser: argparse.ArgumentParser, required: bool
) -> argparse._MutuallyExclusiveGroup:
    result = parser.add_mutually_exclusive_group(required=required)
    result.add_argument(
        '--node-uuids',
        help=(
            'The UUIDs of the unconfigured nodes to add to the cluster. The system adds nodes to '
            'the cluster in the same order that you list them after this flag.'
        ),
        nargs='+',
        default=[],
    )
    result.add_argument(
        '--node-ips',
        help=(
            'The IP addresses of the unconfigured nodes to add to the cluster. The system adds '
            'nodes to the cluster in the same order that you list them after this flag.'
        ),
        nargs='+',
        default=[],
    )
    result.add_argument(
        '--all-unconfigured',
        '-A',
        help=(
            'Add all network-connected, unconfigured nodes to the cluster. This flag does not '
            'allow specifying the order of the nodes and does not apply to cloud clusters.'
        ),
        action='store_true',
    )
    return result


def set_up_node_add_parser(parser: argparse.ArgumentParser) -> None:
    add_nodes_group(parser, required=True)
    parser.add_argument(
        '--target-stripe-config',
        action='store',
        type=int,
        nargs=2,
        metavar=('BLOCKS_PER_STRIPE', 'DATA_BLOCKS_PER_STRIPE'),
        help='The stripe configuration to use',
    )
    parser.add_argument(
        '--target-max-node-failures',
        action='store',
        type=int,
        help=(
            'The minimum node fault tolerance level for the resulting cluster configuration. Note:'
            ' In certain cases, a lower node fault tolerance level can result in higher usable'
            ' capacity'
        ),
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help=(
            'Validate the node-add operation and calculate the resulting usable cluster capacity.'
            ' When you use this flag, Qumulo Core does not add nodes or begin to change data'
            ' protection configuration'
        ),
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Begin the node-add operation without asking for confirmation.',
    )


class NodeAdderOps:
    def print(self, output: str) -> None:
        raise NotImplementedError()

    def are_you_sure(self, question: str) -> bool:
        raise NotImplementedError()

    def modify_nodes(
        self,
        node_uuids: Optional[Sequence[str]],
        node_ips: Optional[Sequence[str]],
        target_max_node_failures: Optional[int],
        target_stripe_config: Optional[StripeConfig],
        nodes_to_replace: Optional[Sequence[int]],
    ) -> str:
        raise NotImplementedError()

    def modify_nodes_dry_run(
        self,
        node_uuids: Optional[Sequence[str]],
        node_ips: Optional[Sequence[str]],
        target_max_node_failures: Optional[int],
        target_stripe_config: Optional[StripeConfig],
        nodes_to_replace: Optional[Sequence[int]],
    ) -> ModifyDryRunResponse:
        raise NotImplementedError()

    def list_unconfigured_nodes(self) -> RestResponse:
        raise NotImplementedError()

    def get_target_stripe_config_from_node_replacement_plan(self) -> Optional[StripeConfig]:
        raise NotImplementedError()

    def get_nodes_to_be_replaced_from_node_replacement_plan(self) -> List[int]:
        raise NotImplementedError()


class NodeAdderAdapter(NodeAdderOps):
    def __init__(self, rest_client: RestClient):
        self.rest_client = rest_client

    def print(self, output: str) -> None:
        print(output)

    def are_you_sure(self, question: str) -> bool:
        print(question)
        return are_you_sure()

    def modify_nodes(
        self,
        node_uuids: Optional[Sequence[str]],
        node_ips: Optional[Sequence[str]],
        target_max_node_failures: Optional[int],
        target_stripe_config: Optional[StripeConfig],
        nodes_to_replace: Optional[Sequence[int]],
    ) -> str:
        return str(
            qumulo.rest.cluster.modify_nodes(
                self.rest_client.conninfo,
                self.rest_client.credentials,
                node_uuids=node_uuids,
                node_ips=node_ips,
                target_max_node_failures=target_max_node_failures,
                target_stripe_config=target_stripe_config,
                nodes_to_replace=nodes_to_replace,
            )
        )

    def modify_nodes_dry_run(
        self,
        node_uuids: Optional[Sequence[str]],
        node_ips: Optional[Sequence[str]],
        target_max_node_failures: Optional[int],
        target_stripe_config: Optional[StripeConfig],
        nodes_to_replace: Optional[Sequence[int]],
    ) -> ModifyDryRunResponse:
        response = qumulo.rest.cluster.modify_nodes_dry_run(
            self.rest_client.conninfo,
            self.rest_client.credentials,
            node_uuids=node_uuids,
            node_ips=node_ips,
            target_max_node_failures=target_max_node_failures,
            target_stripe_config=target_stripe_config,
            nodes_to_replace=nodes_to_replace,
        )
        return ModifyDryRunResponse.from_dict(response.data)

    def list_unconfigured_nodes(self) -> RestResponse:
        return unconfigured_node_operations.list_unconfigured_nodes(
            self.rest_client.conninfo, self.rest_client.credentials
        )

    def get_target_stripe_config_from_node_replacement_plan(self) -> Optional[StripeConfig]:
        plan = get_node_replacement_plan(self.rest_client.conninfo, self.rest_client.credentials)
        target_stripe_config = plan.data['target_stripe_config']
        if target_stripe_config is None:
            return None
        return StripeConfig(**target_stripe_config)

    def get_nodes_to_be_replaced_from_node_replacement_plan(self) -> List[int]:
        plan = get_node_replacement_plan(self.rest_client.conninfo, self.rest_client.credentials)
        return plan.data['nodes_to_be_replaced']


def render_node_fault_tolerance_level(node_fault_tolerance_level: int) -> str:
    if node_fault_tolerance_level == 1:
        return '1 node'
    else:
        return f'{node_fault_tolerance_level} nodes'


CapacityAndNodeFaultTolerance = Tuple[int, int]


@dataclass
class CapacityProjections:
    current: CapacityAndNodeFaultTolerance
    selected: CapacityAndNodeFaultTolerance
    alternative: Optional[CapacityAndNodeFaultTolerance] = None


class NoPlannedReconfigError(Exception):
    pass


class NoNodeReplacementPlanError(Exception):
    pass


class NodeAdder:
    """
    Responsible for handling the v2 node-add CLI (corresponding to the /v2/cluster/nodes API).

    Extracted from the Subcommand to facilitate unit-testing.
    """

    def __init__(self, ops: NodeAdderOps):
        self.ops = ops

    def print_dry_run_info(self, dry_run_info: CapacityAndNodeFaultTolerance) -> None:
        (capacity, node_fault_tolerance) = dry_run_info
        (value, unit) = humanize_decimal(capacity)
        # This case is obviously not important for real clusters, but it makes the unit tests a
        # little nicer
        if unit == 'B':
            self.ops.print(f'    Usable capacity: {capacity} bytes')
        else:
            self.ops.print(f'    Usable capacity: {value} {unit} ({capacity} bytes)')
        self.ops.print(
            '    Node fault tolerance level: '
            + render_node_fault_tolerance_level(node_fault_tolerance)
        )

    def get_capacity_projections(
        self,
        target_stripe_config: Optional[StripeConfig],
        target_max_node_failures: Optional[int],
        node_uuids: Optional[Sequence[str]] = None,
        node_ips: Optional[Sequence[str]] = None,
        nodes_to_replace: Optional[Sequence[int]] = None,
    ) -> CapacityProjections:
        def dry_run_for_nft(node_fault_tolerance: Optional[int]) -> ModifyDryRunResponse:
            return self.ops.modify_nodes_dry_run(
                node_uuids=node_uuids,
                node_ips=node_ips,
                target_max_node_failures=node_fault_tolerance,
                target_stripe_config=target_stripe_config,
                nodes_to_replace=nodes_to_replace,
            )

        # We'll just let the API decide what to do by default if target_max_node_failures is
        # omitted.
        selected_nft_projection = dry_run_for_nft(target_max_node_failures)

        result = CapacityProjections(
            current=(
                selected_nft_projection.current_capacity,
                selected_nft_projection.current_max_node_failures,
            ),
            selected=(
                selected_nft_projection.projected_capacity,
                selected_nft_projection.projected_max_node_failures,
            ),
        )

        try:
            alternative_nft_projection = dry_run_for_nft(
                selected_nft_projection.projected_max_node_failures + 1
            )
            result.alternative = (
                alternative_nft_projection.projected_capacity,
                alternative_nft_projection.projected_max_node_failures,
            )
        # It's fine if it's impossible to increase node fault tolerance further.
        except RequestError:
            pass

        return result

    def print_capacity_projections(
        self, projections: CapacityProjections, batch: bool, operation_name: str
    ) -> None:
        self.ops.print('Current cluster:')
        self.print_dry_run_info(projections.current)

        self.ops.print(f'With the selected {operation_name}:')
        self.print_dry_run_info(projections.selected)

        alternative = projections.alternative
        if not batch and alternative is not None:
            self.ops.print('')
            self.ops.print(
                f'Note that there is an alternative {operation_name} that would provide higher node'
                ' fault tolerance at the expense of usable capacity.'
            )
            self.ops.print(f'With the alternative {operation_name}:')
            self.print_dry_run_info(alternative)

            self.ops.print(
                f'To perform the alternative {operation_name}, re-run this command with '
                f'`--target-max-node-failures {alternative[1]}`.'
            )

    def print_nodes_from_plan(self, nodes_to_replace: List[int]) -> None:
        # We'll fill ranges with a list of closed intervals of nodes to replace. For example,
        # given nodes 1, 2, and 5, we'll end up with ranges of [(1, 2), (5, 5)]. We'll use this to
        # render the node IDs in a readable format even if you're e.g. replacing a 50-node cluster
        # all at once.
        ranges: List[Tuple[int, int]] = []
        # Caller should have checked for an empty list.
        start_of_range = nodes_to_replace[0]
        end_of_range = nodes_to_replace[0]
        for node in nodes_to_replace[1:]:
            if node == end_of_range + 1:
                end_of_range = node
            else:
                ranges.append((start_of_range, end_of_range))
                start_of_range = node
                end_of_range = node
        ranges.append((start_of_range, end_of_range))

        rendered_ranges = ', '.join(
            str(start) if start == end else f'{start}-{end}' for (start, end) in ranges
        )

        self.ops.print(f'Replacing node IDs {rendered_ranges}')
        self.ops.print('')

    def run(
        self,
        target_stripe_config: Optional[StripeConfig] = None,
        do_planned_transcode: bool = False,
        target_max_node_failures: Optional[int] = None,
        node_uuids: Optional[Sequence[str]] = None,
        node_ips: Optional[Sequence[str]] = None,
        all_unconfigured: bool = False,
        nodes_to_replace: Optional[Sequence[int]] = None,
        replace_all: bool = False,
        dry_run: bool = False,
        batch: bool = False,
    ) -> None:
        interactive = not (dry_run or batch)

        operation_name = 'node-add operation'
        if nodes_to_replace:
            assert not replace_all
            operation_name = 'node replacement step'
        if replace_all:
            operation_name = 'node replacement step'
            nodes_to_replace = self.ops.get_nodes_to_be_replaced_from_node_replacement_plan()
            if nodes_to_replace == []:
                raise NoNodeReplacementPlanError(
                    '--replace-all specified but no node replacement plan found.'
                )
            self.print_nodes_from_plan(nodes_to_replace)

        if target_stripe_config is not None:
            assert not do_planned_transcode
            operation_name += ' and data protection reconfiguration'
        if do_planned_transcode:
            operation_name += ' and data protection reconfiguration'
            target_stripe_config = self.ops.get_target_stripe_config_from_node_replacement_plan()
            if target_stripe_config is None:
                raise NoPlannedReconfigError(
                    'No data protection reconfiguration is present in the node replacement plan.'
                )

        if all_unconfigured:
            unconfigured = self.ops.list_unconfigured_nodes()
            nodes = unconfigured.data['nodes']
            node_uuids = [n['uuid'] for n in nodes]
            self.ops.print('Found unconfigured nodes to add:')
            table = unconfigured_node_operations.fmt_unconfigured_nodes(unconfigured)
            self.ops.print(table)
            self.ops.print('')

        projections = self.get_capacity_projections(
            target_stripe_config, target_max_node_failures, node_uuids, node_ips, nodes_to_replace
        )
        self.print_capacity_projections(projections, batch, operation_name)

        if not dry_run:
            if node_uuids is not None and len(node_uuids) > 1 and target_stripe_config is not None:
                self.ops.print('')
                self.ops.print(
                    'Important: Usable capacity does not increase until the data protection '
                    'reconfiguration is complete. If you need additional capacity immediately, '
                    'consider adding some of the nodes without data protection reconfiguration. '
                    'You can reconfigure data protection at a later time.'
                )

            self.ops.print('')
            if interactive:
                self.ops.print(
                    "Important: it isn't possible to reverse this operation. Before continuing, "
                    'check that the above information is correct, and that the nodes are ordered '
                    "correctly. It isn't possible to reorder nodes after you add them to the "
                    'cluster.'
                )
                if not self.ops.are_you_sure(f'Continue with selected {operation_name}?'):
                    return

            self.ops.print(f'Initiating {operation_name}...')
            self.ops.print(
                self.ops.modify_nodes(
                    node_uuids=node_uuids,
                    node_ips=node_ips,
                    target_max_node_failures=target_max_node_failures,
                    target_stripe_config=target_stripe_config,
                    nodes_to_replace=nodes_to_replace,
                )
            )
            self.ops.print('Visit the above URI for progress information.')


class AddNodesCommand(qumulo.lib.opts.Subcommand):
    NAME = 'add_nodes'
    SYNOPSIS = 'Add unconfigured nodes to a Qumulo cluster'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        set_up_node_add_parser(parser)

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        adapter = NodeAdderAdapter(rest_client)
        node_adder = NodeAdder(adapter)
        target_stripe_config = None
        if args.target_stripe_config is not None:
            target_blocks_per_stripe, target_data_blocks_per_stripe = args.target_stripe_config
            target_stripe_config = StripeConfig(
                target_blocks_per_stripe, target_data_blocks_per_stripe
            )
        node_adder.run(
            node_uuids=args.node_uuids,
            node_ips=args.node_ips,
            all_unconfigured=args.all_unconfigured,
            target_stripe_config=target_stripe_config,
            target_max_node_failures=args.target_max_node_failures,
            dry_run=args.dry_run,
            batch=args.batch,
        )


def set_up_register_plan_parser(register_plan_parser: argparse.ArgumentParser) -> None:
    replace_group = register_plan_parser.add_mutually_exclusive_group(required=True)
    replace_group.add_argument(
        '--nodes-to-be-replaced',
        '-n',
        metavar='NODE_ID',
        nargs='+',
        default=[],
        help='The configured nodes to replace',
    )
    replace_group.add_argument(
        '--replace-all',
        '-A',
        action='store_true',
        help='Replace all of the configured nodes in the cluster.',
    )

    register_plan_parser.add_argument(
        '--target-stripe-config',
        action='store',
        type=int,
        nargs=2,
        metavar=('BLOCKS_PER_STRIPE', 'DATA_BLOCKS_PER_STRIPE'),
        help='The final stripe configuration to use',
    )


def set_up_add_nodes_and_replace_parser(step_parser: argparse.ArgumentParser) -> None:
    add_nodes_group(step_parser, required=False)

    nodes_being_replaced_group = step_parser.add_mutually_exclusive_group(required=True)
    nodes_being_replaced_group.add_argument(
        '--nodes-being-replaced',
        '-n',
        metavar='NODE_ID',
        nargs='+',
        default=[],
        help=(
            'The configured nodes to replace. Note: These nodes must be a subset of the node'
            ' replacement plan.'
        ),
    )
    nodes_being_replaced_group.add_argument(
        '--replace-all',
        '-R',
        action='store_true',
        help='Replace all nodes in the node replacement plan.',
    )
    step_parser.add_argument(
        '--reconfigure-data-protection',
        action='store_true',
        help=(
            'Reconfigure data protection to use the stripe configuration from the node '
            'replacement plan.'
        ),
    )
    step_parser.add_argument(
        '--target-max-node-failures',
        action='store',
        type=int,
        help=(
            'The minimum node fault tolerance level for the resulting cluster configuration. '
            'Note: In certain cases, a lower node fault tolerance level can result in higher '
            'usable capacity.'
        ),
    )
    step_parser.add_argument(
        '--dry-run',
        action='store_true',
        help=(
            'Validate the node replacement step and calculate the resulting usable cluster'
            ' capacity. When you use this flag, Qumulo Core does not add or replace nodes or'
            ' begin to change data protection configuration'
        ),
    )
    step_parser.add_argument(
        '--batch',
        action='store_true',
        help='Begin the node replacement step without asking for confirmation.',
    )


class ReplaceNodesCommand(qumulo.lib.opts.Subcommand):
    NAME = 'replace_nodes'
    SYNOPSIS = 'Replace configured nodes by adding nodes to a Qumulo cluster.'

    @staticmethod
    def options(parser: argparse.ArgumentParser) -> None:
        subparsers = parser.add_subparsers(title='subcommands', dest='command', required=True)

        register_plan_parser = subparsers.add_parser(
            'register_plan', help='Configure and store a node replacement plan.'
        )
        register_plan_parser.set_defaults(run=ReplaceNodesCommand.register_plan)
        set_up_register_plan_parser(register_plan_parser)

        step_parser = subparsers.add_parser(
            'add_nodes_and_replace',
            help=(
                'Add unconfigured nodes to the cluster and replace the existing, configured nodes.'
            ),
        )
        step_parser.set_defaults(run=ReplaceNodesCommand.add_nodes_and_replace)
        set_up_add_nodes_and_replace_parser(step_parser)

        get_plan_parser = subparsers.add_parser(
            'get_plan', help='Show the details of the current node replacement plan.'
        )
        get_plan_parser.set_defaults(run=ReplaceNodesCommand.get_plan)

        cancel_parser = subparsers.add_parser(
            'cancel_plan', help='Cancel the current node replacement plan.'
        )
        cancel_parser.set_defaults(run=ReplaceNodesCommand.cancel_plan)
        cancel_parser.add_argument(
            '--batch', action='store_true', help='Do not prompt for user confirmation.'
        )

    @staticmethod
    def register_plan(rest_client: RestClient, args: argparse.Namespace) -> None:
        nodes_to_be_replaced = args.nodes_to_be_replaced
        if args.replace_all:
            nodes_list = qumulo.rest.cluster.list_nodes(
                rest_client.conninfo, rest_client.credentials
            )
            nodes_to_be_replaced = [n['id'] for n in nodes_list.data]

        stripe_config = None
        if args.target_stripe_config is not None:
            stripe_config = StripeConfig(
                blocks_per_stripe=args.target_stripe_config[0],
                data_blocks_per_stripe=args.target_stripe_config[1],
            )

        res = qumulo.rest.cluster.register_node_replacement_plan(
            rest_client.conninfo,
            rest_client.credentials,
            nodes_to_be_replaced=nodes_to_be_replaced,
            target_stripe_config=stripe_config,
        )
        if str(res) == 'null':
            print('Node replacement plan registered.')
        else:
            print(res)

    @staticmethod
    def add_nodes_and_replace(rest_client: RestClient, args: argparse.Namespace) -> None:
        adapter = NodeAdderAdapter(rest_client)
        node_adder = NodeAdder(adapter)
        node_adder.run(
            do_planned_transcode=args.reconfigure_data_protection,
            target_max_node_failures=args.target_max_node_failures,
            node_uuids=args.node_uuids,
            node_ips=args.node_ips,
            all_unconfigured=args.all_unconfigured,
            dry_run=args.dry_run,
            batch=args.batch,
            nodes_to_replace=args.nodes_being_replaced,
            replace_all=args.replace_all,
        )

    @staticmethod
    def get_plan(rest_client: RestClient, _args: argparse.Namespace) -> None:
        plan = qumulo.rest.cluster.get_node_replacement_plan(
            rest_client.conninfo, rest_client.credentials
        )

        # As requested by CS, omit target_stripe_config rather than print 'null'. Nulls in the CLI
        # often concern/confuse some customers.
        # Keep in mind that qq_internal replace_nodes_internal version does always include this
        # field.
        if plan.data['target_stripe_config'] is None:
            del plan.data['target_stripe_config']

        print(plan)

    @staticmethod
    def cancel_plan(rest_client: RestClient, args: argparse.Namespace) -> None:
        interactive = not args.batch

        print(
            'WARNING: Canceling a node replacement plan after a step has already been executed'
            ' might make it impossible to re-register and complete the plan.'
        )
        if interactive:
            print('Do you confirm that you want to cancel the node replacement?')
            if not are_you_sure():
                return

        res = qumulo.rest.cluster.register_node_replacement_plan(
            rest_client.conninfo, rest_client.credentials, nodes_to_be_replaced=[]
        )
        if str(res) == 'null':
            print('Node replacement plan canceled.')
        else:
            print(res)

    @staticmethod
    def main(rest_client: RestClient, args: argparse.Namespace) -> None:
        args.run(rest_client, args)
