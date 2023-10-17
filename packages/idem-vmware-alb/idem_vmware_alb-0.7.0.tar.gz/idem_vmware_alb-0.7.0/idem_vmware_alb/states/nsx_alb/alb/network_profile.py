"""States module for managing Alb Network Profiles. """
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

import dict_tools.differ as differ

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
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
        name(str):
            Idem name of the resource.

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

    Example:
        .. code-block:: sls


          idem_test_nsx_alb.alb.network_profile_is_present:
              nsx_alb.nsx_alb.alb.network_profile.present:
              - configpb_attributes:
                  version: int
              - connection_mirror: bool
              - description: string
              - markers:
                - key: string
                  values:
                  - value
              - profile:
                  sctp_fast_path_profile:
                    enable_init_chunk_protection: bool
                    idle_timeout: int
                  sctp_proxy_profile:
                    cookie_expiration_timeout: int
                    heartbeat_interval: int
                    idle_timeout: int
                    max_retransmissions_association: int
                    max_retransmissions_init_chunks: int
                    number_of_streams: int
                    receive_window: int
                    reset_timeout: int
                  tcp_fast_path_profile:
                    dsr_profile:
                      dsr_encap_type: string
                      dsr_type: string
                    enable_syn_protection: bool
                    session_idle_timeout: int
                  tcp_proxy_profile:
                    aggressive_congestion_avoidance: bool
                    auto_window_growth: bool
                    automatic: bool
                    cc_algo: string
                    congestion_recovery_scaling_factor: int
                    idle_connection_timeout: int
                    idle_connection_type: string
                    ignore_time_wait: bool
                    ip_dscp: int
                    keepalive_in_halfclose_state: bool
                    max_retransmissions: int
                    max_segment_size: int
                    max_syn_retransmissions: int
                    min_rexmt_timeout: int
                    nagles_algorithm: bool
                    reassembly_queue_size: int
                    receive_window: int
                    reorder_threshold: int
                    slow_start_scaling_factor: int
                    time_wait_delay: int
                    use_interface_mtu: bool
                  type_: string
                  udp_fast_path_profile:
                    dsr_profile:
                      dsr_encap_type: string
                      dsr_type: string
                    per_pkt_loadbalance: bool
                    session_idle_timeout: int
                    snat: bool
                  udp_proxy_profile:
                    session_idle_timeout: int
              - tenant_ref: string


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    if resource_id:
        before = await hub.exec.nsx_alb.alb.network_profile.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )

        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = before.ret

        result["comment"].append(f"'nsx_alb.alb.network_profile:{name}' already exists")

    elif not hub.OPT.idem.get("get_resource_only_with_resource_id", False):
        if not tenant_ref:
            tenant_ref_acct = ctx.acct.get("tenant_ref")
            if tenant_ref_acct:
                tenant_ref = tenant_ref_acct
            else:
                tenant_ref = "admin"
        if "name" in tenant_ref:
            tenant_ref = tenant_ref.split("=")[1]
        else:
            tenant_ref = tenant_ref.split("#")[-1]

        before = await hub.exec.nsx_alb.alb.network_profile.get(
            ctx, name=name, tenant_ref=tenant_ref
        )
        if before["ret"]:
            result["old_state"] = before.ret
            resource_id = before["ret"]["resource_id"]
        else:
            resource_id = None

    if result["old_state"]:
        # If there are changes in desired state from existing state
        if desired_state:
            desired_state = await hub.tool.nsx_alb.utils.get_appended_prefix(
                ctx, data=desired_state
            )
        if desired_state:
            for k, v in desired_state.items():
                if ("_ref" in k and isinstance(v, str)) and ("name=" in v):
                    before = await hub.exec.nsx_alb.alb.network_profile.get(
                        ctx,
                        name=name,
                        resource_id=resource_id,
                    )
                    url = before["ret"].get(k).split("#")[0]
                    desired_state.update({k: url})
        changes = differ.deep_diff(before.ret if before.ret else {}, desired_state)

        if bool(changes.get("new")):
            if ctx.test:
                result[
                    "new_state"
                ] = hub.tool.nsx_alb.test_state_utils.generate_test_state(
                    enforced_state={}, desired_state=desired_state
                )
                result["comment"] = (
                    f"Would update nsx_alb.alb.network_profile '{name}'",
                )
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.nsx_alb.alb.network_profile.update(
                    ctx,
                    name=name,
                    resource_id=resource_id,
                    **{
                        "configpb_attributes": configpb_attributes,
                        "connection_mirror": connection_mirror,
                        "description": description,
                        "markers": markers,
                        "profile": profile,
                        "tenant_ref": tenant_ref,
                    },
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"].append(
                        f"Updated 'nsx_alb.alb.network_profile:{name}'"
                    )
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.test:
            result["new_state"] = hub.tool.nsx_alb.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"] = (f"Would create nsx_alb.alb.network_profile {name}",)
            return result
        else:
            create_ret = await hub.exec.nsx_alb.alb.network_profile.create(
                ctx,
                name=name,
                **{
                    "resource_id": resource_id,
                    "configpb_attributes": configpb_attributes,
                    "connection_mirror": connection_mirror,
                    "description": description,
                    "markers": markers,
                    "profile": profile,
                    "tenant_ref": tenant_ref,
                },
            )
            result["result"] = create_ret["result"]

            if result["result"]:
                result["comment"].append(
                    f"Created 'nsx_alb.alb.network_profile:{name}'"
                )
                resource_id = create_ret["ret"]["resource_id"]
                # Safeguard for any future errors so that the resource_id is saved in the ESM
                result["new_state"] = dict(name=name, resource_id=resource_id)
            else:
                result["comment"].append(create_ret["comment"])

    if not result["result"]:
        # If there is any failure in create/update, it should reconcile.
        # The type of data is less important here to use default reconciliation
        # If there are no changes for 3 runs with rerun_data, then it will come out of execution
        result["rerun_data"] = dict(name=name, resource_id=resource_id)

    after = await hub.exec.nsx_alb.alb.network_profile.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )
    result["new_state"] = after.ret
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """

    None
        None

    Args:
        name(str):
            Idem name of the resource.

        resource_id(str, Optional):
            Alb.network_profile unique ID. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


            idem_test_nsx_alb.alb.network_profile_is_absent:
              nsx_alb.nsx_alb.alb.network_profile.absent:


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        result["comment"].append(f"'nsx_alb.alb.network_profile:{name}' already absent")
        return result

    before = await hub.exec.nsx_alb.alb.network_profile.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    if before["ret"]:
        if ctx.test:
            result["comment"] = f"Would delete nsx_alb.alb.network_profile:{name}"
            return result

        delete_ret = await hub.exec.nsx_alb.alb.network_profile.delete(
            ctx,
            name=name,
            resource_id=resource_id,
        )
        result["result"] = delete_ret["result"]

        if result["result"]:
            result["comment"].append(f"Deleted 'nsx_alb.alb.network_profile:{name}'")
        else:
            # If there is any failure in delete, it should reconcile.
            # The type of data is less important here to use default reconciliation
            # If there are no changes for 3 runs with rerun_data, then it will come out of execution
            result["rerun_data"] = resource_id
            result["comment"].append(delete_ret["result"])
    else:
        result["comment"].append(f"'nsx_alb.alb.network_profile:{name}' already absent")
        return result

    result["old_state"] = before.ret
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function


    None
        None

    Args:

    Returns:
        Dict[str, Any]

    Example:

        .. code-block:: bash

            $ idem describe nsx_alb.alb.network_profile
    """

    result = {}

    ret = await hub.exec.nsx_alb.alb.network_profile.list(ctx)

    if not ret or not ret["result"]:
        hub.log.debug(
            f"Could not describe nsx_alb.alb.network_profile {ret['comment']}"
        )
        return result

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "nsx_alb.alb.network_profile.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
