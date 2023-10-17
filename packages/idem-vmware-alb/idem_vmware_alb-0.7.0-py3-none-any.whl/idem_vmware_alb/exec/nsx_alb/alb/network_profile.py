"""Exec module for managing Alb Network Profiles. """
from collections import OrderedDict
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["soft_fail"]

__func_alias__ = {"list_": "list"}


async def get(
    hub, ctx, resource_id: str = None, name: str = None, tenant_ref: str = None
) -> Dict[str, Any]:
    """
    None
        None

    Args:
        resource_id(str):
            Alb.network_profile unique ID.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

        tenant_ref(str, Optional):
            Avi Tenant Header. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: nsx_alb.alb.network_profile.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.network_profile.get resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)

    get = await hub.tool.nsx_alb.session.request(
        ctx,
        method="get",
        path="/networkprofile/{uuid}?include_name".format(**{"uuid": resource_id})
        if resource_id
        else "/networkprofile?include_name",
        query_params={"name": name},
        data={},
        headers={"X-Avi-Tenant": tenant_ref} if tenant_ref else {"X-Avi-Tenant": "*"},
    )

    if not get["result"]:
        # Send empty result for not found
        if get["status"] == 404:
            result["comment"].append(f"Get '{name}' result is empty")
            result["result"] = False
            return result

        result["comment"].append(get["comment"])
        result["result"] = False
        return result

    # Case: Empty results
    if not get["ret"]:
        result["comment"].append(f"Get '{name}' result is empty")
        return result

    if "results" in get["ret"].keys():
        if get["ret"]["count"] != 0:
            # Convert raw response into present format
            raw_resource = get["ret"]["results"][0]
            resource_id = get["ret"]["results"][0]["uuid"]
        else:
            return result
    else:
        # Convert raw response into present format
        raw_resource = get["ret"]

    resource_in_present_format = {"name": name, "resource_id": resource_id}
    resource_parameters = OrderedDict(
        {
            "configpb_attributes": "configpb_attributes",
            "connection_mirror": "connection_mirror",
            "description": "description",
            "markers": "markers",
            "name": "name",
            "profile": "profile",
            "tenant_ref": "tenant_ref",
        }
    )

    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_in_present_format[parameter_present] = raw_resource.get(
                parameter_raw
            )

    result["ret"] = resource_in_present_format

    return result


async def list_(hub, ctx) -> Dict[str, Any]:
    """
    None
        None

    Args:

        name(str, Optional):
            Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: nsx_alb.alb.network_profile.list
                - kwargs:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.network_profile.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe nsx_alb.alb.network_profile

    """

    result = dict(comment=[], ret=[], result=True)

    list = await hub.tool.nsx_alb.session.request(
        ctx,
        method="get",
        path="/networkprofile",
        query_params={},
        data={},
        headers={"X-Avi-Tenant": "*"},
    )

    if not list["result"]:
        result["comment"].append(list["comment"])
        result["result"] = False
        return result

    for resource in list["ret"]["results"]:
        # TODO Handle pagination if required
        resource["resource_id"] = resource.get("uuid")
        result["ret"].append(resource)

    return result


async def create(
    hub,
    ctx,
    profile: make_dataclass(
        "profile",
        [
            ("type", str),
            (
                "sctp_fast_path_profile",
                make_dataclass(
                    "sctp_fast_path_profile",
                    [
                        ("enable_init_chunk_protection", bool, field(default=None)),
                        ("idle_timeout", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "sctp_proxy_profile",
                make_dataclass(
                    "sctp_proxy_profile",
                    [
                        ("cookie_expiration_timeout", int, field(default=None)),
                        ("heartbeat_interval", int, field(default=None)),
                        ("idle_timeout", int, field(default=None)),
                        ("max_retransmissions_association", int, field(default=None)),
                        ("max_retransmissions_init_chunks", int, field(default=None)),
                        ("number_of_streams", int, field(default=None)),
                        ("receive_window", int, field(default=None)),
                        ("reset_timeout", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "tcp_fast_path_profile",
                make_dataclass(
                    "tcp_fast_path_profile",
                    [
                        (
                            "dsr_profile",
                            make_dataclass(
                                "dsr_profile",
                                [("dsr_encap_type", str), ("dsr_type", str)],
                            ),
                            field(default=None),
                        ),
                        ("enable_syn_protection", bool, field(default=None)),
                        ("session_idle_timeout", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "tcp_proxy_profile",
                make_dataclass(
                    "tcp_proxy_profile",
                    [
                        ("aggressive_congestion_avoidance", bool, field(default=None)),
                        ("auto_window_growth", bool, field(default=None)),
                        ("automatic", bool, field(default=None)),
                        ("cc_algo", str, field(default=None)),
                        (
                            "congestion_recovery_scaling_factor",
                            int,
                            field(default=None),
                        ),
                        ("idle_connection_timeout", int, field(default=None)),
                        ("idle_connection_type", str, field(default=None)),
                        ("ignore_time_wait", bool, field(default=None)),
                        ("ip_dscp", int, field(default=None)),
                        ("keepalive_in_halfclose_state", bool, field(default=None)),
                        ("max_retransmissions", int, field(default=None)),
                        ("max_segment_size", int, field(default=None)),
                        ("max_syn_retransmissions", int, field(default=None)),
                        ("min_rexmt_timeout", int, field(default=None)),
                        ("nagles_algorithm", bool, field(default=None)),
                        ("reassembly_queue_size", int, field(default=None)),
                        ("receive_window", int, field(default=None)),
                        ("reorder_threshold", int, field(default=None)),
                        ("slow_start_scaling_factor", int, field(default=None)),
                        ("time_wait_delay", int, field(default=None)),
                        ("use_interface_mtu", bool, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "udp_fast_path_profile",
                make_dataclass(
                    "udp_fast_path_profile",
                    [
                        (
                            "dsr_profile",
                            make_dataclass(
                                "dsr_profile",
                                [("dsr_encap_type", str), ("dsr_type", str)],
                            ),
                            field(default=None),
                        ),
                        ("per_pkt_loadbalance", bool, field(default=None)),
                        ("session_idle_timeout", int, field(default=None)),
                        ("snat", bool, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "udp_proxy_profile",
                make_dataclass(
                    "udp_proxy_profile",
                    [("session_idle_timeout", int, field(default=None))],
                ),
                field(default=None),
            ),
        ],
    ),
    resource_id: str = None,
    name: str = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    connection_mirror: bool = None,
    description: str = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    tenant_ref: str = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:

        profile(dict[str, Any]):
            profile.

            * sctp_fast_path_profile (dict[str, Any], Optional):
                sctp_fast_path_profile

                * enable_init_chunk_protection (bool, Optional):
                    When enabled, Avi will complete the 4-way handshake with the client before forwarding any packets to the server.  This will protect the server from INIT chunks flood and half open connections. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * idle_timeout (int, Optional):
                    SCTP autoclose timeout. 0 means autoclose deactivated. Allowed values are 0-247483647. Field introduced in 22.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * sctp_proxy_profile (dict[str, Any], Optional):
                sctp_proxy_profile

                * cookie_expiration_timeout (int, Optional):
                    SCTP cookie expiration timeout. Allowed values are 60-3600. Field introduced in 22.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * heartbeat_interval (int, Optional):
                    SCTP heartbeat interval. Allowed values are 30-247483647. Field introduced in 22.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * idle_timeout (int, Optional):
                    SCTP autoclose timeout. 0 means autoclose deactivated. Allowed values are 0-247483647. Field introduced in 22.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * max_retransmissions_association (int, Optional):
                    SCTP maximum retransmissions for association. Allowed values are 1-247483647. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * max_retransmissions_init_chunks (int, Optional):
                    SCTP maximum retransmissions for INIT chunks. Allowed values are 1-247483647. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * number_of_streams (int, Optional):
                    Number of incoming SCTP Streams. Allowed values are 1-65535. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * receive_window (int, Optional):
                    SCTP send and receive buffer size. Allowed values are 2-65536. Field introduced in 22.1.3. Unit is KB. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * reset_timeout (int, Optional):
                    SCTP reset timeout. 0 means 5 times RTO max. Allowed values are 0-247483647. Field introduced in 22.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * tcp_fast_path_profile (dict[str, Any], Optional):
                tcp_fast_path_profile

                * dsr_profile (dict[str, Any], Optional):
                    dsr_profile

                    * dsr_encap_type (str):
                        Encapsulation type to use when DSR is L3. Enum options - ENCAP_IPINIP, ENCAP_GRE. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * dsr_type (str):
                        DSR type L2/L3. Enum options - DSR_TYPE_L2, DSR_TYPE_L3. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * enable_syn_protection (bool, Optional):
                    When enabled, Avi will complete the 3-way handshake with the client before forwarding any packets to the server.  This will protect the server from SYN flood and half open SYN connections. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

                * session_idle_timeout (int, Optional):
                    The amount of time (in sec) for which a connection needs to be idle before it is eligible to be deleted. Allowed values are 5-14400. Special values are 0 - infinite. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * tcp_proxy_profile (dict[str, Any], Optional):
                tcp_proxy_profile

                * aggressive_congestion_avoidance (bool, Optional):
                    Controls the our congestion window to send, normally it's 1 mss, If this option is turned on, we use 10 msses. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * auto_window_growth (bool, Optional):
                    Controls whether the windows are static or supports autogrowth. Maximum that it can grow to is limited to 4MB. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * automatic (bool, Optional):
                    Dynamically pick the relevant parameters for connections. Allowed in Enterprise edition with any value, Basic edition(Allowed values- true), Essentials, Enterprise with Cloud Services edition.

                * cc_algo (str, Optional):
                    Controls the congestion control algorithm we use. Enum options - CC_ALGO_NEW_RENO, CC_ALGO_CUBIC, CC_ALGO_HTCP. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * congestion_recovery_scaling_factor (int, Optional):
                    Congestion window scaling factor after recovery. Allowed values are 0-8. Field introduced in 17.2.12, 18.1.3, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * idle_connection_timeout (int, Optional):
                    The duration for keepalive probes or session idle timeout. Max value is 14400 seconds, min is 5.  Set to 0 to allow infinite idle time. Allowed values are 5-14400. Special values are 0 - infinite. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * idle_connection_type (str, Optional):
                    Controls the behavior of idle connections. Enum options - KEEP_ALIVE, CLOSE_IDLE. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ignore_time_wait (bool, Optional):
                    A new SYN is accepted from the same 4-tuple even if there is already a connection in TIME_WAIT state.  This is equivalent of setting Time Wait Delay to 0. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ip_dscp (int, Optional):
                    Controls the value of the Differentiated Services Code Point field inserted in the IP header.  This has two options   Set to a specific value, or Pass Through, which uses the incoming DSCP value. Allowed values are 0-63. Special values are MAX - Passthrough. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * keepalive_in_halfclose_state (bool, Optional):
                    Controls whether to keep the connection alive with keepalive messages in the TCP half close state. The interval for sending keepalive messages is 30s. If a timeout is already configured in the network profile, this will not override it. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_retransmissions (int, Optional):
                    The number of attempts at retransmit before closing the connection. Allowed values are 3-8. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_segment_size (int, Optional):
                    Maximum TCP segment size. Allowed values are 512-9000. Special values are 0 - Use Interface MTU. Unit is BYTES. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_syn_retransmissions (int, Optional):
                    The maximum number of attempts at retransmitting a SYN packet before giving up. Allowed values are 3-8. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * min_rexmt_timeout (int, Optional):
                    The minimum wait time (in millisec) to retransmit packet. Allowed values are 50-5000. Field introduced in 17.2.8. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * nagles_algorithm (bool, Optional):
                    Consolidates small data packets to send clients fewer but larger packets.  Adversely affects real time protocols such as telnet or SSH. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * reassembly_queue_size (int, Optional):
                    Maximum number of TCP segments that can be queued for reassembly. Configuring this to 0 disables the feature and provides unlimited queuing. Field introduced in 17.2.13, 18.1.4, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * receive_window (int, Optional):
                    Size of the receive window. Allowed values are 2-65536. Unit is KB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * reorder_threshold (int, Optional):
                    Controls the number of duplicate acks required to trigger retransmission. Setting a higher value reduces retransmission caused by packet reordering. A larger value is recommended in public cloud environments where packet reordering is quite common. The default value is 8 in public cloud platforms (AWS, Azure, GCP), and 3 in other environments. Allowed values are 1-100. Field introduced in 17.2.7. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * slow_start_scaling_factor (int, Optional):
                    Congestion window scaling factor during slow start. Allowed values are 0-8. Field introduced in 17.2.12, 18.1.3, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * time_wait_delay (int, Optional):
                    The time (in millisec) to wait before closing a connection in the TIME_WAIT state. Allowed values are 500-2000. Special values are 0 - immediate. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * use_interface_mtu (bool, Optional):
                    Use the interface MTU to calculate the TCP max segment size. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * type (str):
                Configure one of either proxy or fast path profiles. Enum options - PROTOCOL_TYPE_TCP_PROXY, PROTOCOL_TYPE_TCP_FAST_PATH, PROTOCOL_TYPE_UDP_FAST_PATH, PROTOCOL_TYPE_UDP_PROXY, PROTOCOL_TYPE_SCTP_PROXY, PROTOCOL_TYPE_SCTP_FAST_PATH. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- PROTOCOL_TYPE_TCP_FAST_PATH,PROTOCOL_TYPE_UDP_FAST_PATH), Basic edition(Allowed values- PROTOCOL_TYPE_TCP_PROXY,PROTOCOL_TYPE_TCP_FAST_PATH,PROTOCOL_TYPE_UDP_FAST_PATH), Enterprise with Cloud Services edition.

            * udp_fast_path_profile (dict[str, Any], Optional):
                udp_fast_path_profile

                * dsr_profile (dict[str, Any], Optional):
                    dsr_profile

                    * dsr_encap_type (str):
                        Encapsulation type to use when DSR is L3. Enum options - ENCAP_IPINIP, ENCAP_GRE. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * dsr_type (str):
                        DSR type L2/L3. Enum options - DSR_TYPE_L2, DSR_TYPE_L3. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * per_pkt_loadbalance (bool, Optional):
                    When enabled, every UDP packet is considered a new transaction and may be load balanced to a different server.  When disabled, packets from the same client source IP and port are sent to the same server. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

                * session_idle_timeout (int, Optional):
                    The amount of time (in sec) for which a flow needs to be idle before it is deleted. Allowed values are 2-3600. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * snat (bool, Optional):
                    When disabled, Source NAT will not be performed for all client UDP packets. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * udp_proxy_profile (dict[str, Any], Optional):
                udp_proxy_profile

                * session_idle_timeout (int, Optional):
                    The amount of time (in sec) for which a flow needs to be idle before it is deleted. Allowed values are 2-3600. Field introduced in 17.2.8, 18.1.3, 18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        resource_id(str, Optional):
            Alb.network_profile unique ID. Defaults to None.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        connection_mirror(bool, Optional):
            When enabled, Avi mirrors all TCP fastpath connections to standby. Applicable only in Legacy HA Mode. Field introduced in 18.1.3,18.2.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic, Enterprise with Cloud Services edition. Defaults to None.

        description(str, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              nsx_alb.alb.network_profile.present:
                - profile: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.network_profile.create profile=value
    """

    result = dict(comment=[], ret=[], result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "configpb_attributes": "configpb_attributes",
        "connection_mirror": "connection_mirror",
        "description": "description",
        "markers": "markers",
        "name": "name",
        "profile": "profile",
        "tenant_ref": "tenant_ref",
    }

    payload = {}
    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = value

    create = await hub.tool.nsx_alb.session.request(
        ctx,
        method="post",
        path="/networkprofile",
        query_params={},
        data=payload,
    )

    if not create["result"]:
        result["comment"].append(create["comment"])
        result["result"] = False
        return result

    result["comment"].append(
        f"Created nsx_alb.alb.network_profile '{name}'",
    )

    result["ret"] = create["ret"]

    result["ret"]["resource_id"] = create["ret"]["uuid"]
    return result


async def update(
    hub,
    ctx,
    resource_id: str,
    profile: make_dataclass(
        "profile",
        [
            ("type", str),
            (
                "sctp_fast_path_profile",
                make_dataclass(
                    "sctp_fast_path_profile",
                    [
                        ("enable_init_chunk_protection", bool, field(default=None)),
                        ("idle_timeout", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "sctp_proxy_profile",
                make_dataclass(
                    "sctp_proxy_profile",
                    [
                        ("cookie_expiration_timeout", int, field(default=None)),
                        ("heartbeat_interval", int, field(default=None)),
                        ("idle_timeout", int, field(default=None)),
                        ("max_retransmissions_association", int, field(default=None)),
                        ("max_retransmissions_init_chunks", int, field(default=None)),
                        ("number_of_streams", int, field(default=None)),
                        ("receive_window", int, field(default=None)),
                        ("reset_timeout", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "tcp_fast_path_profile",
                make_dataclass(
                    "tcp_fast_path_profile",
                    [
                        (
                            "dsr_profile",
                            make_dataclass(
                                "dsr_profile",
                                [("dsr_encap_type", str), ("dsr_type", str)],
                            ),
                            field(default=None),
                        ),
                        ("enable_syn_protection", bool, field(default=None)),
                        ("session_idle_timeout", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "tcp_proxy_profile",
                make_dataclass(
                    "tcp_proxy_profile",
                    [
                        ("aggressive_congestion_avoidance", bool, field(default=None)),
                        ("auto_window_growth", bool, field(default=None)),
                        ("automatic", bool, field(default=None)),
                        ("cc_algo", str, field(default=None)),
                        (
                            "congestion_recovery_scaling_factor",
                            int,
                            field(default=None),
                        ),
                        ("idle_connection_timeout", int, field(default=None)),
                        ("idle_connection_type", str, field(default=None)),
                        ("ignore_time_wait", bool, field(default=None)),
                        ("ip_dscp", int, field(default=None)),
                        ("keepalive_in_halfclose_state", bool, field(default=None)),
                        ("max_retransmissions", int, field(default=None)),
                        ("max_segment_size", int, field(default=None)),
                        ("max_syn_retransmissions", int, field(default=None)),
                        ("min_rexmt_timeout", int, field(default=None)),
                        ("nagles_algorithm", bool, field(default=None)),
                        ("reassembly_queue_size", int, field(default=None)),
                        ("receive_window", int, field(default=None)),
                        ("reorder_threshold", int, field(default=None)),
                        ("slow_start_scaling_factor", int, field(default=None)),
                        ("time_wait_delay", int, field(default=None)),
                        ("use_interface_mtu", bool, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "udp_fast_path_profile",
                make_dataclass(
                    "udp_fast_path_profile",
                    [
                        (
                            "dsr_profile",
                            make_dataclass(
                                "dsr_profile",
                                [("dsr_encap_type", str), ("dsr_type", str)],
                            ),
                            field(default=None),
                        ),
                        ("per_pkt_loadbalance", bool, field(default=None)),
                        ("session_idle_timeout", int, field(default=None)),
                        ("snat", bool, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "udp_proxy_profile",
                make_dataclass(
                    "udp_proxy_profile",
                    [("session_idle_timeout", int, field(default=None))],
                ),
                field(default=None),
            ),
        ],
    ),
    name: str = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    connection_mirror: bool = None,
    description: str = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    tenant_ref: str = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:
        resource_id(str):
            Alb.network_profile unique ID.

        profile(dict[str, Any]):
            profile.

            * sctp_fast_path_profile (dict[str, Any], Optional):
                sctp_fast_path_profile

                * enable_init_chunk_protection (bool, Optional):
                    When enabled, Avi will complete the 4-way handshake with the client before forwarding any packets to the server.  This will protect the server from INIT chunks flood and half open connections. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * idle_timeout (int, Optional):
                    SCTP autoclose timeout. 0 means autoclose deactivated. Allowed values are 0-247483647. Field introduced in 22.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * sctp_proxy_profile (dict[str, Any], Optional):
                sctp_proxy_profile

                * cookie_expiration_timeout (int, Optional):
                    SCTP cookie expiration timeout. Allowed values are 60-3600. Field introduced in 22.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * heartbeat_interval (int, Optional):
                    SCTP heartbeat interval. Allowed values are 30-247483647. Field introduced in 22.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * idle_timeout (int, Optional):
                    SCTP autoclose timeout. 0 means autoclose deactivated. Allowed values are 0-247483647. Field introduced in 22.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * max_retransmissions_association (int, Optional):
                    SCTP maximum retransmissions for association. Allowed values are 1-247483647. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * max_retransmissions_init_chunks (int, Optional):
                    SCTP maximum retransmissions for INIT chunks. Allowed values are 1-247483647. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * number_of_streams (int, Optional):
                    Number of incoming SCTP Streams. Allowed values are 1-65535. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * receive_window (int, Optional):
                    SCTP send and receive buffer size. Allowed values are 2-65536. Field introduced in 22.1.3. Unit is KB. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * reset_timeout (int, Optional):
                    SCTP reset timeout. 0 means 5 times RTO max. Allowed values are 0-247483647. Field introduced in 22.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * tcp_fast_path_profile (dict[str, Any], Optional):
                tcp_fast_path_profile

                * dsr_profile (dict[str, Any], Optional):
                    dsr_profile

                    * dsr_encap_type (str):
                        Encapsulation type to use when DSR is L3. Enum options - ENCAP_IPINIP, ENCAP_GRE. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * dsr_type (str):
                        DSR type L2/L3. Enum options - DSR_TYPE_L2, DSR_TYPE_L3. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * enable_syn_protection (bool, Optional):
                    When enabled, Avi will complete the 3-way handshake with the client before forwarding any packets to the server.  This will protect the server from SYN flood and half open SYN connections. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

                * session_idle_timeout (int, Optional):
                    The amount of time (in sec) for which a connection needs to be idle before it is eligible to be deleted. Allowed values are 5-14400. Special values are 0 - infinite. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * tcp_proxy_profile (dict[str, Any], Optional):
                tcp_proxy_profile

                * aggressive_congestion_avoidance (bool, Optional):
                    Controls the our congestion window to send, normally it's 1 mss, If this option is turned on, we use 10 msses. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * auto_window_growth (bool, Optional):
                    Controls whether the windows are static or supports autogrowth. Maximum that it can grow to is limited to 4MB. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * automatic (bool, Optional):
                    Dynamically pick the relevant parameters for connections. Allowed in Enterprise edition with any value, Basic edition(Allowed values- true), Essentials, Enterprise with Cloud Services edition.

                * cc_algo (str, Optional):
                    Controls the congestion control algorithm we use. Enum options - CC_ALGO_NEW_RENO, CC_ALGO_CUBIC, CC_ALGO_HTCP. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * congestion_recovery_scaling_factor (int, Optional):
                    Congestion window scaling factor after recovery. Allowed values are 0-8. Field introduced in 17.2.12, 18.1.3, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * idle_connection_timeout (int, Optional):
                    The duration for keepalive probes or session idle timeout. Max value is 14400 seconds, min is 5.  Set to 0 to allow infinite idle time. Allowed values are 5-14400. Special values are 0 - infinite. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * idle_connection_type (str, Optional):
                    Controls the behavior of idle connections. Enum options - KEEP_ALIVE, CLOSE_IDLE. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ignore_time_wait (bool, Optional):
                    A new SYN is accepted from the same 4-tuple even if there is already a connection in TIME_WAIT state.  This is equivalent of setting Time Wait Delay to 0. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ip_dscp (int, Optional):
                    Controls the value of the Differentiated Services Code Point field inserted in the IP header.  This has two options   Set to a specific value, or Pass Through, which uses the incoming DSCP value. Allowed values are 0-63. Special values are MAX - Passthrough. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * keepalive_in_halfclose_state (bool, Optional):
                    Controls whether to keep the connection alive with keepalive messages in the TCP half close state. The interval for sending keepalive messages is 30s. If a timeout is already configured in the network profile, this will not override it. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_retransmissions (int, Optional):
                    The number of attempts at retransmit before closing the connection. Allowed values are 3-8. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_segment_size (int, Optional):
                    Maximum TCP segment size. Allowed values are 512-9000. Special values are 0 - Use Interface MTU. Unit is BYTES. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_syn_retransmissions (int, Optional):
                    The maximum number of attempts at retransmitting a SYN packet before giving up. Allowed values are 3-8. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * min_rexmt_timeout (int, Optional):
                    The minimum wait time (in millisec) to retransmit packet. Allowed values are 50-5000. Field introduced in 17.2.8. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * nagles_algorithm (bool, Optional):
                    Consolidates small data packets to send clients fewer but larger packets.  Adversely affects real time protocols such as telnet or SSH. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * reassembly_queue_size (int, Optional):
                    Maximum number of TCP segments that can be queued for reassembly. Configuring this to 0 disables the feature and provides unlimited queuing. Field introduced in 17.2.13, 18.1.4, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * receive_window (int, Optional):
                    Size of the receive window. Allowed values are 2-65536. Unit is KB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * reorder_threshold (int, Optional):
                    Controls the number of duplicate acks required to trigger retransmission. Setting a higher value reduces retransmission caused by packet reordering. A larger value is recommended in public cloud environments where packet reordering is quite common. The default value is 8 in public cloud platforms (AWS, Azure, GCP), and 3 in other environments. Allowed values are 1-100. Field introduced in 17.2.7. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * slow_start_scaling_factor (int, Optional):
                    Congestion window scaling factor during slow start. Allowed values are 0-8. Field introduced in 17.2.12, 18.1.3, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * time_wait_delay (int, Optional):
                    The time (in millisec) to wait before closing a connection in the TIME_WAIT state. Allowed values are 500-2000. Special values are 0 - immediate. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * use_interface_mtu (bool, Optional):
                    Use the interface MTU to calculate the TCP max segment size. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * type (str):
                Configure one of either proxy or fast path profiles. Enum options - PROTOCOL_TYPE_TCP_PROXY, PROTOCOL_TYPE_TCP_FAST_PATH, PROTOCOL_TYPE_UDP_FAST_PATH, PROTOCOL_TYPE_UDP_PROXY, PROTOCOL_TYPE_SCTP_PROXY, PROTOCOL_TYPE_SCTP_FAST_PATH. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- PROTOCOL_TYPE_TCP_FAST_PATH,PROTOCOL_TYPE_UDP_FAST_PATH), Basic edition(Allowed values- PROTOCOL_TYPE_TCP_PROXY,PROTOCOL_TYPE_TCP_FAST_PATH,PROTOCOL_TYPE_UDP_FAST_PATH), Enterprise with Cloud Services edition.

            * udp_fast_path_profile (dict[str, Any], Optional):
                udp_fast_path_profile

                * dsr_profile (dict[str, Any], Optional):
                    dsr_profile

                    * dsr_encap_type (str):
                        Encapsulation type to use when DSR is L3. Enum options - ENCAP_IPINIP, ENCAP_GRE. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * dsr_type (str):
                        DSR type L2/L3. Enum options - DSR_TYPE_L2, DSR_TYPE_L3. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * per_pkt_loadbalance (bool, Optional):
                    When enabled, every UDP packet is considered a new transaction and may be load balanced to a different server.  When disabled, packets from the same client source IP and port are sent to the same server. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

                * session_idle_timeout (int, Optional):
                    The amount of time (in sec) for which a flow needs to be idle before it is deleted. Allowed values are 2-3600. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * snat (bool, Optional):
                    When disabled, Source NAT will not be performed for all client UDP packets. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * udp_proxy_profile (dict[str, Any], Optional):
                udp_proxy_profile

                * session_idle_timeout (int, Optional):
                    The amount of time (in sec) for which a flow needs to be idle before it is deleted. Allowed values are 2-3600. Field introduced in 17.2.8, 18.1.3, 18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        connection_mirror(bool, Optional):
            When enabled, Avi mirrors all TCP fastpath connections to standby. Applicable only in Legacy HA Mode. Field introduced in 18.1.3,18.2.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic, Enterprise with Cloud Services edition. Defaults to None.

        description(str, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.


    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              nsx_alb.alb.network_profile.present:
                - resource_id: value
                - profile: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.network_profile.update resource_id=value, profile=value
    """

    result = dict(comment=[], ret=[], result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "configpb_attributes": "configpb_attributes",
        "connection_mirror": "connection_mirror",
        "description": "description",
        "markers": "markers",
        "name": "name",
        "profile": "profile",
        "tenant_ref": "tenant_ref",
    }

    payload = {}
    for key, value in desired_state.items():
        if (
            key in resource_to_raw_input_mapping.keys()
            and value is not None
            and key != "_last_modified"
        ):
            payload[resource_to_raw_input_mapping[key]] = value

    if payload:
        update = await hub.tool.nsx_alb.session.request(
            ctx,
            method="put",
            path="/networkprofile/{uuid}".format(**{"uuid": resource_id}),
            query_params={},
            data=payload,
        )

        if not update["result"]:
            result["comment"].append(update["comment"])
            result["result"] = False
            return result

        result["ret"] = update["ret"]
        result["resource_id"] = update["ret"]["uuid"]
        result["comment"].append(
            f"Updated nsx_alb.alb.network_profile '{name}'",
        )

    return result


async def delete(
    hub,
    ctx,
    resource_id: str,
    name: str = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:
        resource_id(str):
            Alb.network_profile unique ID.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              nsx_alb.alb.network_profile.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.network_profile.delete resource_id=value
    """

    result = dict(comment=[], ret=[], result=True)

    before = await hub.exec.nsx_alb.alb.network_profile.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )
    if before["ret"]:
        tenant_name = before["ret"]["tenant_ref"].split("#")[-1]
    delete = await hub.tool.nsx_alb.session.request(
        ctx,
        method="delete",
        path="/networkprofile/{uuid}".format(**{"uuid": resource_id}),
        query_params={},
        data={},
        headers={"X-Avi-Tenant": tenant_name},
    )

    if not delete["result"]:
        result["comment"].append(delete["comment"])
        result["result"] = False
        return result

    result["comment"].append(f"Deleted '{name}'")
    return result
