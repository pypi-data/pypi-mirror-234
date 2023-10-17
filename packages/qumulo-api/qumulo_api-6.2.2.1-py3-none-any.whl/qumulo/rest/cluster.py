# Copyright (c) 2012 Qumulo, Inc.
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


from dataclasses import dataclass
from typing import Any, Dict, Mapping, NamedTuple, Optional, Sequence, Union

import qumulo.lib.request as request

from qumulo.lib.auth import Credentials
from qumulo.lib.request import Connection, RestResponse


class StripeConfig(NamedTuple):
    blocks_per_stripe: int
    data_blocks_per_stripe: int


@request.request
def list_nodes(conninfo: Connection, _credentials: Optional[Credentials]) -> RestResponse:
    method = 'GET'
    uri = '/v1/cluster/nodes/'

    return conninfo.send_request(method, uri)


@request.request
def list_node(conninfo: Connection, _credentials: Optional[Credentials], node: int) -> RestResponse:
    method = 'GET'
    uri = f'/v1/cluster/nodes/{node}'

    return conninfo.send_request(method, uri)


@request.request
def get_cluster_conf(conninfo: Connection, _credentials: Optional[Credentials]) -> RestResponse:
    method = 'GET'
    uri = '/v1/cluster/settings'

    return conninfo.send_request(method, uri)


@request.request
def put_cluster_conf(
    conninfo: Connection, _credentials: Optional[Credentials], cluster_name: str
) -> RestResponse:
    method = 'PUT'
    uri = '/v1/cluster/settings'

    config = {'cluster_name': str(cluster_name)}

    return conninfo.send_request(method, uri, body=config)


@request.request
def set_ssl_certificate(
    conninfo: Connection, _credentials: Optional[Credentials], certificate: str, private_key: str
) -> RestResponse:
    method = 'PUT'
    uri = '/v2/cluster/settings/ssl/certificate'

    config = {'certificate': str(certificate), 'private_key': str(private_key)}

    return conninfo.send_request(method, uri, body=config)


@request.request
def set_ssl_ca_certificate(
    conninfo: Connection, _credentials: Optional[Credentials], ca_cert: str
) -> RestResponse:
    method = 'PUT'
    uri = '/v2/cluster/settings/ssl/ca-certificate'
    body = {'ca_certificate': str(ca_cert)}
    return conninfo.send_request(method, uri, body=body)


@request.request
def get_ssl_ca_certificate(
    conninfo: Connection, _credentials: Optional[Credentials]
) -> RestResponse:
    method = 'GET'
    uri = '/v2/cluster/settings/ssl/ca-certificate'

    return conninfo.send_request(method, uri)


@request.request
def delete_ssl_ca_certificate(
    conninfo: Connection, _credentials: Optional[Credentials]
) -> RestResponse:
    method = 'DELETE'
    uri = '/v2/cluster/settings/ssl/ca-certificate'

    return conninfo.send_request(method, uri)


@request.request
def get_cluster_slots_status(
    conninfo: Connection, _credentials: Optional[Credentials]
) -> RestResponse:
    method = 'GET'
    uri = '/v1/cluster/slots/'

    return conninfo.send_request(method, uri)


@request.request
def get_cluster_slot_status(
    conninfo: Connection, _credentials: Optional[Credentials], slot: str
) -> RestResponse:
    method = 'GET'
    uri = f'/v1/cluster/slots/{slot}'

    return conninfo.send_request(method, uri)


@request.request
def set_cluster_slot_config(
    conninfo: Connection, _credentials: Optional[Credentials], slot: str, pattern: str
) -> RestResponse:
    method = 'PATCH'
    uri = f'/v1/cluster/slots/{slot}'

    body = {'led_pattern': pattern}

    return conninfo.send_request(method, uri, body=body)


@request.request
def get_restriper_status_deprecated(
    conninfo: Connection, _credentials: Optional[Credentials]
) -> RestResponse:
    """
    This REST endpoint is deprecated in 5.3.4, but Python binding is retained until the next
    quarterly upgrade for systest use.
    """
    method = 'GET'
    uri = '/v1/cluster/restriper/status'

    return conninfo.send_request(method, uri)


@request.request
def get_restriper_status(conninfo: Connection, _credentials: Optional[Credentials]) -> RestResponse:
    method = 'GET'
    uri = '/v1/cluster/protection/restriper/status'

    return conninfo.send_request(method, uri)


@request.request
def get_protection_status(
    conninfo: Connection, _credentials: Optional[Credentials]
) -> RestResponse:
    method = 'GET'
    uri = '/v1/cluster/protection/status'

    return conninfo.send_request(method, uri)


@request.request
def set_node_identify_light(
    conninfo: Connection, _credentials: Optional[Credentials], node: int, light_visible: bool
) -> RestResponse:
    method = 'POST'
    uri = f'/v1/cluster/nodes/{node}/uid-light'

    body = {'light_visible': light_visible}

    return conninfo.send_request(method, uri, body=body)


@request.request
def get_node_chassis_status(
    conninfo: Connection, _credentials: Optional[Credentials], node: Optional[int] = None
) -> RestResponse:
    method = 'GET'

    if node is not None:
        uri = f'/v1/cluster/nodes/{node}/chassis'
    else:
        uri = '/v1/cluster/nodes/chassis/'

    return conninfo.send_request(method, uri)


# This should match the max_drive_failures enumeration in /v1/cluster/create
PROTECTION_LEVEL_MAP = {'RECOMMENDED': -1, 'TWO_DRIVES': 2, 'THREE_DRIVES': 3}


def sanitize_max_drive_failures(param: Optional[Union[str, int]]) -> Optional[int]:
    """
    In order to avoid revving the bindings, we need to continue to support the
    old-style drive failures params, which are strings that must be either
    RECOMMENDED, TWO_DRIVES or THREE_DRIVES.  These can easily be translated
    into an optional int, matching the v2 REST endpoint.
    """
    if param is None:
        return param
    if isinstance(param, int):
        return param

    if param not in PROTECTION_LEVEL_MAP:
        raise ValueError(f"invalid max drive failures count: '{param}'")

    value = PROTECTION_LEVEL_MAP[param]
    return value if value > 0 else None


@request.request
def create_cluster(
    conninfo: Connection,
    _credentials: Optional[Credentials],
    cluster_name: str,
    admin_password: str,
    node_uuids: Optional[Sequence[str]] = None,
    node_ips: Optional[Sequence[str]] = None,
    eula_accepted: bool = True,
    host_instance_id: Optional[str] = None,
    blocks_per_stripe: Optional[int] = None,
    max_drive_failures: Optional[Union[str, int]] = None,
    max_node_failures: Optional[int] = None,
) -> RestResponse:
    method = 'POST'
    uri = '/v2/cluster/create'

    cluster_create_request = {
        'eula_accepted': eula_accepted,
        'cluster_name': str(cluster_name),
        'node_uuids': [] if node_uuids is None else list(node_uuids),
        'node_ips': [] if node_ips is None else list(node_ips),
        'admin_password': str(admin_password),
    }

    if host_instance_id is not None:
        cluster_create_request['host_instance_id'] = host_instance_id

    if blocks_per_stripe is not None:
        cluster_create_request['blocks_per_stripe'] = blocks_per_stripe

    sanitized_max_drive_failures = sanitize_max_drive_failures(max_drive_failures)
    if sanitized_max_drive_failures is not None:
        cluster_create_request['max_drive_failures'] = sanitized_max_drive_failures

    if max_node_failures is not None:
        cluster_create_request['max_node_failures'] = max_node_failures

    return conninfo.send_request(method, uri, body=cluster_create_request)


@request.request
def add_node(
    conninfo: Connection,
    _credentials: Optional[Credentials],
    node_uuids: Optional[Sequence[str]] = None,
    node_ips: Optional[Sequence[str]] = None,
    blobs: Optional[Sequence[object]] = None,
    optimize_node_fault_tolerance_over_usable_capacity: bool = False,
) -> RestResponse:
    method = 'POST'
    uri = '/v1/cluster/nodes/'

    req = {
        'node_uuids': [] if node_uuids is None else list(node_uuids),
        'node_ips': [] if node_ips is None else list(node_ips),
        'blobs': [] if blobs is None else list(blobs),
        'optimize_node_fault_tolerance_over_usable_capacity': optimize_node_fault_tolerance_over_usable_capacity,
    }

    return conninfo.send_request(method, uri, body=req)


@request.request
def calculate_node_add_capacity(
    conninfo: Connection,
    _credentials: Optional[Credentials],
    node_uuids: Optional[Sequence[str]] = None,
    node_ips: Optional[Sequence[str]] = None,
) -> RestResponse:
    method = 'POST'
    uri = '/v1/cluster/calculate-node-add-capacity'

    req = {
        'node_uuids': [] if node_uuids is None else list(node_uuids),
        'node_ips': [] if node_ips is None else list(node_ips),
    }

    return conninfo.send_request(method, uri, body=req)


@request.request
def modify_nodes(
    conninfo: Connection,
    _credentials: Optional[Credentials],
    node_uuids: Optional[Sequence[str]] = None,
    node_ips: Optional[Sequence[str]] = None,
    nodes_to_replace: Optional[Sequence[int]] = None,
    blobs: Optional[Sequence[object]] = None,
    target_max_node_failures: Optional[int] = None,
    target_stripe_config: Optional[StripeConfig] = None,
) -> RestResponse:
    method = 'POST'
    uri = '/v2/cluster/nodes/'

    req = {
        'node_uuids': [] if node_uuids is None else list(node_uuids),
        'node_ips': [] if node_ips is None else list(node_ips),
        'nodes_to_replace': [] if nodes_to_replace is None else list(nodes_to_replace),
        'blobs': [] if blobs is None else list(blobs),
    }

    if target_max_node_failures:
        req['target_max_node_failures'] = target_max_node_failures

    if target_stripe_config:
        req['target_stripe_config'] = {
            'blocks_per_stripe': target_stripe_config.blocks_per_stripe,
            'data_blocks_per_stripe': target_stripe_config.data_blocks_per_stripe,
        }

    return conninfo.send_request(method, uri, body=req)


@dataclass
class ModifyDryRunResponse:
    current_capacity: int
    current_max_node_failures: int
    projected_capacity: int
    projected_max_node_failures: int

    @staticmethod
    def from_dict(data: Mapping[str, Any]) -> 'ModifyDryRunResponse':
        return ModifyDryRunResponse(
            current_capacity=int(data['current_capacity']),
            current_max_node_failures=int(data['current_max_node_failures']),
            projected_capacity=int(data['projected_capacity']),
            projected_max_node_failures=int(data['projected_max_node_failures']),
        )


@request.request
def modify_nodes_dry_run(
    conninfo: Connection,
    _credentials: Optional[Credentials],
    node_uuids: Optional[Sequence[str]] = None,
    node_ips: Optional[Sequence[str]] = None,
    nodes_to_replace: Optional[Sequence[int]] = None,
    blobs: Optional[Sequence[object]] = None,
    target_max_node_failures: Optional[int] = None,
    target_stripe_config: Optional[StripeConfig] = None,
) -> RestResponse:
    method = 'POST'
    uri = '/v2/cluster/nodes/dry-run'

    req = {
        'node_uuids': [] if node_uuids is None else list(node_uuids),
        'node_ips': [] if node_ips is None else list(node_ips),
        'nodes_to_replace': [] if nodes_to_replace is None else list(nodes_to_replace),
        'blobs': [] if blobs is None else list(blobs),
    }

    if target_max_node_failures:
        req['target_max_node_failures'] = target_max_node_failures

    if target_stripe_config:
        req['target_stripe_config'] = {
            'blocks_per_stripe': target_stripe_config.blocks_per_stripe,
            'data_blocks_per_stripe': target_stripe_config.data_blocks_per_stripe,
        }

    return conninfo.send_request(method, uri, body=req)


@request.request
def register_node_replacement_plan(
    conninfo: Connection,
    _credentials: Optional[Credentials],
    nodes_to_be_replaced: Sequence[int],
    target_stripe_config: Optional[StripeConfig] = None,
) -> RestResponse:
    method = 'POST'
    uri = '/v1/cluster/node-replacement-plan/'

    req: Dict[str, Any] = {'nodes_to_be_replaced': nodes_to_be_replaced}
    if target_stripe_config:
        req['target_stripe_config'] = {
            'blocks_per_stripe': target_stripe_config.blocks_per_stripe,
            'data_blocks_per_stripe': target_stripe_config.data_blocks_per_stripe,
        }

    return conninfo.send_request(method, uri, body=req)


@request.request
def get_node_replacement_plan(
    conninfo: Connection, _credentials: Optional[Credentials]
) -> RestResponse:
    method = 'GET'
    uri = '/v1/cluster/node-replacement-plan/'

    resp = conninfo.send_request(method, uri)
    del resp.data['target_compatibility_class']
    return resp
