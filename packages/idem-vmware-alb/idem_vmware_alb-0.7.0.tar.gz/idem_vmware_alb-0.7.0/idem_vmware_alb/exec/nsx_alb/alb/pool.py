"""Exec module for managing Alb Pools. """
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
            Alb.pool unique ID.

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
                - path: nsx_alb.alb.pool.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.pool.get resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)

    get = await hub.tool.nsx_alb.session.request(
        ctx,
        method="get",
        path="/pool/{uuid}?include_name".format(**{"uuid": resource_id})
        if resource_id
        else "/pool?include_name",
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
            get["ret"]["resource_id"] = get["ret"]["results"][0]["uuid"]
            result["ret"] = get["ret"]
    else:
        get["ret"]["resource_id"] = resource_id
        result["ret"] = get["ret"]

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
                - path: nsx_alb.alb.pool.list
                - kwargs:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.pool.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe nsx_alb.alb.pool

    """

    result = dict(comment=[], ret=[], result=True)

    list = await hub.tool.nsx_alb.session.request(
        ctx,
        method="get",
        path="/pool",
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
    resource_id: str = None,
    name: str = None,
    analytics_policy: make_dataclass(
        "analytics_policy", [("enable_realtime_metrics", bool, field(default=None))]
    ) = None,
    analytics_profile_ref: str = None,
    append_port: str = None,
    application_persistence_profile_ref: str = None,
    autoscale_launch_config_ref: str = None,
    autoscale_networks: List[str] = None,
    autoscale_policy_ref: str = None,
    capacity_estimation: bool = None,
    capacity_estimation_ttfb_thresh: int = None,
    cloud_config_cksum: str = None,
    cloud_ref: str = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    conn_pool_properties: make_dataclass(
        "conn_pool_properties",
        [
            ("upstream_connpool_conn_idle_tmo", int, field(default=None)),
            ("upstream_connpool_conn_life_tmo", int, field(default=None)),
            ("upstream_connpool_conn_max_reuse", int, field(default=None)),
            ("upstream_connpool_server_max_cache", int, field(default=None)),
        ],
    ) = None,
    connection_ramp_duration: int = None,
    created_by: str = None,
    default_server_port: int = None,
    delete_server_on_dns_refresh: bool = None,
    description: str = None,
    domain_name: List[str] = None,
    east_west: bool = None,
    enable_http2: bool = None,
    enabled: bool = None,
    external_autoscale_groups: List[str] = None,
    fail_action: make_dataclass(
        "fail_action",
        [
            ("type", str),
            (
                "local_rsp",
                make_dataclass(
                    "local_rsp",
                    [
                        (
                            "file",
                            make_dataclass(
                                "file",
                                [
                                    ("content_type", str),
                                    ("file_content", str),
                                    ("file_length", int, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("status_code", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "redirect",
                make_dataclass(
                    "redirect",
                    [
                        ("host", str),
                        ("path", str, field(default=None)),
                        ("protocol", str, field(default=None)),
                        ("query", str, field(default=None)),
                        ("status_code", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    fewest_tasks_feedback_delay: int = None,
    graceful_disable_timeout: int = None,
    gslb_sp_enabled: bool = None,
    health_monitor_refs: List[str] = None,
    horizon_profile: make_dataclass(
        "horizon_profile",
        [
            ("blast_port", int, field(default=None)),
            ("pcoip_port", int, field(default=None)),
        ],
    ) = None,
    host_check_enabled: bool = None,
    http2_properties: make_dataclass(
        "http2_properties",
        [
            ("max_http2_control_frames_per_connection", int, field(default=None)),
            ("max_http2_header_field_size", int, field(default=None)),
        ],
    ) = None,
    ignore_server_port: bool = None,
    inline_health_monitor: bool = None,
    ipaddrgroup_ref: str = None,
    lb_algo_rr_per_se: bool = None,
    lb_algorithm: str = None,
    lb_algorithm_consistent_hash_hdr: str = None,
    lb_algorithm_core_nonaffinity: int = None,
    lb_algorithm_hash: str = None,
    lookup_server_by_name: bool = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    max_concurrent_connections_per_server: int = None,
    max_conn_rate_per_server: make_dataclass(
        "max_conn_rate_per_server",
        [
            (
                "action",
                make_dataclass(
                    "action",
                    [
                        (
                            "file",
                            make_dataclass(
                                "file",
                                [
                                    ("content_type", str),
                                    ("file_content", str),
                                    ("file_length", int, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "redirect",
                            make_dataclass(
                                "redirect",
                                [
                                    ("protocol", str),
                                    ("add_string", str, field(default=None)),
                                    (
                                        "host",
                                        make_dataclass(
                                            "host",
                                            [
                                                ("type", str),
                                                (
                                                    "tokens",
                                                    List[
                                                        make_dataclass(
                                                            "tokens",
                                                            [
                                                                ("type", str),
                                                                (
                                                                    "end_index",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "start_index",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "str_value",
                                                                    str,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        )
                                                    ],
                                                    field(default=None),
                                                ),
                                            ],
                                        ),
                                        field(default=None),
                                    ),
                                    ("keep_query", bool, field(default=None)),
                                    (
                                        "path",
                                        make_dataclass(
                                            "path",
                                            [
                                                ("type", str),
                                                (
                                                    "tokens",
                                                    List[
                                                        make_dataclass(
                                                            "tokens",
                                                            [
                                                                ("type", str),
                                                                (
                                                                    "end_index",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "start_index",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "str_value",
                                                                    str,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        )
                                                    ],
                                                    field(default=None),
                                                ),
                                            ],
                                        ),
                                        field(default=None),
                                    ),
                                    ("port", int, field(default=None)),
                                    ("status_code", str, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("status_code", str, field(default=None)),
                        ("type", str, field(default=None)),
                    ],
                ),
            ),
            ("explicit_tracking", bool, field(default=None)),
            ("fine_grain", bool, field(default=None)),
            ("http_cookie", str, field(default=None)),
            ("http_header", str, field(default=None)),
            (
                "rate_limiter",
                make_dataclass(
                    "rate_limiter",
                    [
                        ("count", int),
                        ("period", int),
                        ("burst_sz", int, field(default=None)),
                        ("name", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    min_health_monitors_up: int = None,
    min_servers_up: int = None,
    networks: List[
        make_dataclass(
            "networks",
            [("network_ref", str), ("server_filter", str, field(default=None))],
        )
    ] = None,
    nsx_securitygroup: List[str] = None,
    pki_profile_ref: str = None,
    placement_networks: List[
        make_dataclass(
            "placement_networks",
            [
                ("network_ref", str),
                (
                    "subnet",
                    make_dataclass(
                        "subnet",
                        [
                            (
                                "ip_addr",
                                make_dataclass(
                                    "ip_addr", [("addr", str), ("type", str)]
                                ),
                            ),
                            ("mask", int),
                        ],
                    ),
                ),
            ],
        )
    ] = None,
    pool_type: str = None,
    request_queue_depth: int = None,
    request_queue_enabled: bool = None,
    resolve_pool_by_dns: bool = None,
    rewrite_host_header_to_server_name: bool = None,
    rewrite_host_header_to_sni: bool = None,
    routing_pool: bool = None,
    server_disable_type: str = None,
    server_name: str = None,
    server_reselect: make_dataclass(
        "server_reselect",
        [
            ("enabled", bool),
            ("num_retries", int, field(default=None)),
            ("retry_nonidempotent", bool, field(default=None)),
            ("retry_timeout", int, field(default=None)),
            (
                "svr_resp_code",
                make_dataclass(
                    "svr_resp_code",
                    [
                        ("codes", List[int], field(default=None)),
                        (
                            "ranges",
                            List[
                                make_dataclass("ranges", [("begin", int), ("end", int)])
                            ],
                            field(default=None),
                        ),
                        ("resp_code_block", List[str], field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    server_timeout: int = None,
    servers: List[
        make_dataclass(
            "servers",
            [
                ("ip", make_dataclass("ip", [("addr", str), ("type", str)])),
                ("autoscaling_group_name", str, field(default=None)),
                ("availability_zone", str, field(default=None)),
                ("description", str, field(default=None)),
                (
                    "discovered_networks",
                    List[
                        make_dataclass(
                            "discovered_networks",
                            [
                                ("network_ref", str),
                                (
                                    "subnet",
                                    List[
                                        make_dataclass(
                                            "subnet",
                                            [
                                                (
                                                    "ip_addr",
                                                    make_dataclass(
                                                        "ip_addr",
                                                        [("addr", str), ("type", str)],
                                                    ),
                                                ),
                                                ("mask", int),
                                            ],
                                        )
                                    ],
                                    field(default=None),
                                ),
                                (
                                    "subnet6",
                                    List[
                                        make_dataclass(
                                            "subnet6",
                                            [
                                                (
                                                    "ip_addr",
                                                    make_dataclass(
                                                        "ip_addr",
                                                        [("addr", str), ("type", str)],
                                                    ),
                                                ),
                                                ("mask", int),
                                            ],
                                        )
                                    ],
                                    field(default=None),
                                ),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                ("enabled", bool, field(default=None)),
                ("external_orchestration_id", str, field(default=None)),
                ("external_uuid", str, field(default=None)),
                ("hostname", str, field(default=None)),
                (
                    "location",
                    make_dataclass(
                        "location",
                        [
                            ("latitude", float, field(default=None)),
                            ("longitude", float, field(default=None)),
                            ("name", str, field(default=None)),
                            ("tag", str, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                ("mac_address", str, field(default=None)),
                ("nw_ref", str, field(default=None)),
                ("port", int, field(default=None)),
                ("preference_order", int, field(default=None)),
                ("prst_hdr_val", str, field(default=None)),
                ("ratio", int, field(default=None)),
                ("resolve_server_by_dns", bool, field(default=None)),
                ("rewrite_host_header", bool, field(default=None)),
                ("server_node", str, field(default=None)),
                ("static", bool, field(default=None)),
                ("verify_network", bool, field(default=None)),
                ("vm_ref", str, field(default=None)),
            ],
        )
    ] = None,
    service_metadata: str = None,
    sni_enabled: bool = None,
    sp_gs_info: make_dataclass(
        "sp_gs_info",
        [
            ("fqdns", List[str], field(default=None)),
            ("gs_ref", str, field(default=None)),
        ],
    ) = None,
    ssl_key_and_certificate_ref: str = None,
    ssl_profile_ref: str = None,
    tenant_ref: str = None,
    tier1_lr: str = None,
    use_service_port: bool = None,
    use_service_ssl_mode: bool = None,
    vrf_ref: str = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:

        resource_id(str, Optional):
            Alb.pool unique ID. Defaults to None.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

        analytics_policy(dict[str, Any], Optional):
            analytics_policy. Defaults to None.

            * enable_realtime_metrics (bool, Optional):
                Enable real time metrics for server and pool metrics eg. l4_server.xxx, l7_server.xxx. Field introduced in 18.1.5, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        analytics_profile_ref(str, Optional):
            Specifies settings related to analytics. It is a reference to an object of type AnalyticsProfile. Field introduced in 18.1.4,18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        append_port(str, Optional):
            Allows the option to append port to hostname in the host header while sending a request to the server. By default, port is appended for non-default ports. This setting will apply for Pool's 'Rewrite Host Header to Server Name', 'Rewrite Host Header to SNI' features and Server's 'Rewrite Host Header' settings as well as HTTP healthmonitors attached to pools. Enum options - NON_DEFAULT_80_443, NEVER, ALWAYS. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- NEVER), Basic edition(Allowed values- NEVER), Enterprise with Cloud Services edition. Special default for Essentials edition is NEVER, Basic edition is NEVER, Enterprise is NON_DEFAULT_80_443. Defaults to None.

        application_persistence_profile_ref(str, Optional):
            Persistence will ensure the same user sticks to the same server for a desired duration of time. It is a reference to an object of type ApplicationPersistenceProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        autoscale_launch_config_ref(str, Optional):
            If configured then Avi will trigger orchestration of pool server creation and deletion. It is a reference to an object of type AutoScaleLaunchConfig. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        autoscale_networks(List[str], Optional):
            Network Ids for the launch configuration. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        autoscale_policy_ref(str, Optional):
            Reference to Server Autoscale Policy. It is a reference to an object of type ServerAutoScalePolicy. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        capacity_estimation(bool, Optional):
            Inline estimation of capacity of servers. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        capacity_estimation_ttfb_thresh(int, Optional):
            The maximum time-to-first-byte of a server. Allowed values are 1-5000. Special values are 0 - Automatic. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Defaults to None.

        cloud_config_cksum(str, Optional):
            Checksum of cloud configuration for Pool. Internally set by cloud connector. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        cloud_ref(str, Optional):
             It is a reference to an object of type Cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        conn_pool_properties(dict[str, Any], Optional):
            conn_pool_properties. Defaults to None.

            * upstream_connpool_conn_idle_tmo (int, Optional):
                Connection idle timeout. Allowed values are 0-86400000. Special values are 0- Infinite idle time.. Field introduced in 18.2.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 60000), Basic edition(Allowed values- 60000), Enterprise with Cloud Services edition.

            * upstream_connpool_conn_life_tmo (int, Optional):
                Connection life timeout. Allowed values are 0-86400000. Special values are 0- Infinite life time.. Field introduced in 18.2.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 600000), Basic edition(Allowed values- 600000), Enterprise with Cloud Services edition.

            * upstream_connpool_conn_max_reuse (int, Optional):
                Maximum number of times a connection can be reused. Special values are 0- unlimited. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition.

            * upstream_connpool_server_max_cache (int, Optional):
                Maximum number of connections a server can cache. Special values are 0- unlimited. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        connection_ramp_duration(int, Optional):
            Duration for which new connections will be gradually ramped up to a server recently brought online.  Useful for LB algorithms that are least connection based. Allowed values are 1-300. Special values are 0 - Immediate. Unit is MIN. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Special default for Essentials edition is 0, Basic edition is 0, Enterprise is 10. Defaults to None.

        created_by(str, Optional):
            Creator name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        default_server_port(int, Optional):
            Traffic sent to servers will use this destination server port unless overridden by the server's specific port attribute. The SSL checkbox enables Avi to server encryption. Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        delete_server_on_dns_refresh(bool, Optional):
            Indicates whether existing IPs are disabled(false) or deleted(true) on dns hostname refreshDetail -- On a dns refresh, some IPs set on pool may no longer be returned by the resolver. These IPs are deleted from the pool when this knob is set to true. They are disabled, if the knob is set to false. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- true), Basic edition(Allowed values- true), Enterprise with Cloud Services edition. Defaults to None.

        description(str, Optional):
            A description of the pool. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        domain_name(List[str], Optional):
            Comma separated list of domain names which will be used to verify the common names or subject alternative names presented by server certificates. It is performed only when common name check host_check_enabled is enabled. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        east_west(bool, Optional):
            Inherited config from VirtualService. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        enable_http2(bool, Optional):
            Enable HTTP/2 for traffic from VirtualService to all backend servers in this pool. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        enabled(bool, Optional):
            Enable or disable the pool.  Disabling will terminate all open connections and pause health monitors. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        external_autoscale_groups(List[str], Optional):
            Names of external auto-scale groups for pool servers. Currently available only for AWS and Azure. Field introduced in 17.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        fail_action(dict[str, Any], Optional):
            fail_action. Defaults to None.

            * local_rsp (dict[str, Any], Optional):
                local_rsp

                * file (dict[str, Any], Optional):
                    file

                    * content_type (str):
                        Mime-type of the content in the file. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * file_content (str):
                        File content to used in the local HTTP response body. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * file_length (int, Optional):
                        File content length. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * status_code (str, Optional):
                     Enum options - FAIL_HTTP_STATUS_CODE_200, FAIL_HTTP_STATUS_CODE_503. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * redirect (dict[str, Any], Optional):
                redirect

                * host (str):
                    The host to which the redirect request is sent. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * path (str, Optional):
                    Path configuration for the redirect request. If not set the path from the original request's URI is preserved in the redirect on pool failure. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * protocol (str, Optional):
                     Enum options - HTTP, HTTPS. Allowed in Enterprise edition with any value, Basic edition(Allowed values- HTTP), Essentials, Enterprise with Cloud Services edition. Special default for Basic edition is HTTP, Enterprise is HTTPS.

                * query (str, Optional):
                    Query configuration for the redirect request URI. If not set, the query from the original request's URI is preserved in the redirect on pool failure. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * status_code (str, Optional):
                     Enum options - HTTP_REDIRECT_STATUS_CODE_301, HTTP_REDIRECT_STATUS_CODE_302, HTTP_REDIRECT_STATUS_CODE_307. Allowed in Enterprise edition with any value, Basic edition(Allowed values- HTTP_REDIRECT_STATUS_CODE_302), Essentials, Enterprise with Cloud Services edition.

            * type (str):
                Enables a response to client when pool experiences a failure. By default TCP connection is closed. Enum options - FAIL_ACTION_HTTP_REDIRECT, FAIL_ACTION_HTTP_LOCAL_RSP, FAIL_ACTION_CLOSE_CONN, FAIL_ACTION_BACKUP_POOL. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- FAIL_ACTION_CLOSE_CONN), Basic edition(Allowed values- FAIL_ACTION_CLOSE_CONN,FAIL_ACTION_HTTP_REDIRECT), Enterprise with Cloud Services edition.

        fewest_tasks_feedback_delay(int, Optional):
            Periodicity of feedback for fewest tasks server selection algorithm. Allowed values are 1-300. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        graceful_disable_timeout(int, Optional):
            Used to gracefully disable a server. Virtual service waits for the specified time before terminating the existing connections  to the servers that are disabled. Allowed values are 1-7200. Special values are 0 - Immediate, -1 - Infinite. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        gslb_sp_enabled(bool, Optional):
            Indicates if the pool is a site-persistence pool. . Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        health_monitor_refs(List[str], Optional):
            Verify server health by applying one or more health monitors.  Active monitors generate synthetic traffic from each Service Engine and mark a server up or down based on the response. The Passive monitor listens only to client to server communication. It raises or lowers the ratio of traffic destined to a server based on successful responses. It is a reference to an object of type HealthMonitor. Maximum of 50 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        horizon_profile(dict[str, Any], Optional):
            horizon_profile. Defaults to None.

            * blast_port (int, Optional):
                Horizon blast port of the UAG server. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * pcoip_port (int, Optional):
                Horizon pcoip port of the UAG server. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        host_check_enabled(bool, Optional):
            Enable common name check for server certificate. If enabled and no explicit domain name is specified, Avi will use the incoming host header to do the match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        http2_properties(dict[str, Any], Optional):
            http2_properties. Defaults to None.

            * max_http2_control_frames_per_connection (int, Optional):
                The max number of control frames that server can send over an HTTP/2 connection. '0' means unlimited. Allowed values are 0-10000. Special values are 0- Unlimited control frames on a server side HTTP/2 connection. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * max_http2_header_field_size (int, Optional):
                The maximum size in bytes of the compressed request header field. The limit applies equally to both name and value. Allowed values are 1-8192. Field introduced in 21.1.1. Unit is BYTES. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        ignore_server_port(bool, Optional):
            Ignore the server port in building the load balancing state.Applicable only for consistent hash load balancing algorithm or Disable Port translation (use_service_port) use cases. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        inline_health_monitor(bool, Optional):
            The Passive monitor will monitor client to server connections and requests and adjust traffic load to servers based on successful responses.  This may alter the expected behavior of the LB method, such as Round Robin. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ipaddrgroup_ref(str, Optional):
            Use list of servers from Ip Address Group. It is a reference to an object of type IpAddrGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        lb_algo_rr_per_se(bool, Optional):
            Do Round Robin load load balancing at SE level instead of the default per core load balancing. Field introduced in 21.1.5, 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        lb_algorithm(str, Optional):
            The load balancing algorithm will pick a server within the pool's list of available servers. Values LB_ALGORITHM_NEAREST_SERVER and LB_ALGORITHM_TOPOLOGY are only allowed for GSLB pool. Enum options - LB_ALGORITHM_LEAST_CONNECTIONS, LB_ALGORITHM_ROUND_ROBIN, LB_ALGORITHM_FASTEST_RESPONSE, LB_ALGORITHM_CONSISTENT_HASH, LB_ALGORITHM_LEAST_LOAD, LB_ALGORITHM_FEWEST_SERVERS, LB_ALGORITHM_RANDOM, LB_ALGORITHM_FEWEST_TASKS, LB_ALGORITHM_NEAREST_SERVER, LB_ALGORITHM_CORE_AFFINITY, LB_ALGORITHM_TOPOLOGY. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- LB_ALGORITHM_LEAST_CONNECTIONS,LB_ALGORITHM_ROUND_ROBIN,LB_ALGORITHM_CONSISTENT_HASH), Basic edition(Allowed values- LB_ALGORITHM_LEAST_CONNECTIONS,LB_ALGORITHM_ROUND_ROBIN,LB_ALGORITHM_CONSISTENT_HASH), Enterprise with Cloud Services edition. Defaults to None.

        lb_algorithm_consistent_hash_hdr(str, Optional):
            HTTP header name to be used for the hash key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        lb_algorithm_core_nonaffinity(int, Optional):
            Degree of non-affinity for core affinity based server selection. Allowed values are 1-65535. Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 2), Basic edition(Allowed values- 2), Enterprise with Cloud Services edition. Defaults to None.

        lb_algorithm_hash(str, Optional):
            Criteria used as a key for determining the hash between the client and  server. Enum options - LB_ALGORITHM_CONSISTENT_HASH_SOURCE_IP_ADDRESS, LB_ALGORITHM_CONSISTENT_HASH_SOURCE_IP_ADDRESS_AND_PORT, LB_ALGORITHM_CONSISTENT_HASH_URI, LB_ALGORITHM_CONSISTENT_HASH_CUSTOM_HEADER, LB_ALGORITHM_CONSISTENT_HASH_CUSTOM_STRING, LB_ALGORITHM_CONSISTENT_HASH_CALLID. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- LB_ALGORITHM_CONSISTENT_HASH_SOURCE_IP_ADDRESS), Basic edition(Allowed values- LB_ALGORITHM_CONSISTENT_HASH_SOURCE_IP_ADDRESS), Enterprise with Cloud Services edition. Defaults to None.

        lookup_server_by_name(bool, Optional):
            Allow server lookup by name. Field introduced in 17.1.11,17.2.4. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        max_concurrent_connections_per_server(int, Optional):
            The maximum number of concurrent connections allowed to each server within the pool. NOTE  applied value will be no less than the number of service engines that the pool is placed on. If set to 0, no limit is applied. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_conn_rate_per_server(dict[str, Any], Optional):
            max_conn_rate_per_server. Defaults to None.

            * action (dict[str, Any]):
                action

                * file (dict[str, Any], Optional):
                    file

                    * content_type (str):
                        Mime-type of the content in the file. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * file_content (str):
                        File content to used in the local HTTP response body. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * file_length (int, Optional):
                        File content length. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * redirect (dict[str, Any], Optional):
                    redirect

                    * add_string (str, Optional):
                        Add a query string to the redirect URI. If keep_query is set, concatenates the add_string to the query of the incoming request. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * host (dict[str, Any], Optional):
                        host

                        * tokens (List[dict[str, Any]], Optional):
                            Token config either for the URI components or a constant string. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * end_index (int, Optional):
                                Index of the ending token in the incoming URI. Allowed values are 0-65534. Special values are 65535 - end of string. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * start_index (int, Optional):
                                Index of the starting token in the incoming URI. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * str_value (str, Optional):
                                Constant string to use as a token. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                Token type for constructing the URI. Enum options - URI_TOKEN_TYPE_HOST, URI_TOKEN_TYPE_PATH, URI_TOKEN_TYPE_STRING, URI_TOKEN_TYPE_STRING_GROUP, URI_TOKEN_TYPE_REGEX, URI_TOKEN_TYPE_REGEX_QUERY. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                            URI param type. Enum options - URI_PARAM_TYPE_TOKENIZED. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * keep_query (bool, Optional):
                        Keep or drop the query of the incoming request URI in the redirected URI. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * path (dict[str, Any], Optional):
                        path

                        * tokens (List[dict[str, Any]], Optional):
                            Token config either for the URI components or a constant string. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * end_index (int, Optional):
                                Index of the ending token in the incoming URI. Allowed values are 0-65534. Special values are 65535 - end of string. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * start_index (int, Optional):
                                Index of the starting token in the incoming URI. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * str_value (str, Optional):
                                Constant string to use as a token. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                Token type for constructing the URI. Enum options - URI_TOKEN_TYPE_HOST, URI_TOKEN_TYPE_PATH, URI_TOKEN_TYPE_STRING, URI_TOKEN_TYPE_STRING_GROUP, URI_TOKEN_TYPE_REGEX, URI_TOKEN_TYPE_REGEX_QUERY. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                            URI param type. Enum options - URI_PARAM_TYPE_TOKENIZED. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * port (int, Optional):
                        Port to which redirect the request. Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * protocol (str):
                        Protocol type. Enum options - HTTP, HTTPS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * status_code (str, Optional):
                        HTTP redirect status code. Enum options - HTTP_REDIRECT_STATUS_CODE_301, HTTP_REDIRECT_STATUS_CODE_302, HTTP_REDIRECT_STATUS_CODE_307. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * status_code (str, Optional):
                    HTTP status code for Local Response rate limit action. Enum options - HTTP_LOCAL_RESPONSE_STATUS_CODE_200, HTTP_LOCAL_RESPONSE_STATUS_CODE_204, HTTP_LOCAL_RESPONSE_STATUS_CODE_403, HTTP_LOCAL_RESPONSE_STATUS_CODE_404, HTTP_LOCAL_RESPONSE_STATUS_CODE_429, HTTP_LOCAL_RESPONSE_STATUS_CODE_501. Allowed in Enterprise edition with any value, Basic edition(Allowed values- HTTP_LOCAL_RESPONSE_STATUS_CODE_429), Essentials, Enterprise with Cloud Services edition.

                * type (str, Optional):
                    Type of action to be enforced upon hitting the rate limit. Enum options - RL_ACTION_NONE, RL_ACTION_DROP_CONN, RL_ACTION_RESET_CONN, RL_ACTION_CLOSE_CONN, RL_ACTION_LOCAL_RSP, RL_ACTION_REDIRECT. Allowed in Enterprise edition with any value, Basic edition(Allowed values- RL_ACTION_NONE,RL_ACTION_DROP_CONN), Essentials, Enterprise with Cloud Services edition.

            * explicit_tracking (bool, Optional):
                Explicitly tracks an attacker across rate periods. Allowed in Enterprise edition with any value, Basic edition(Allowed values- false), Essentials, Enterprise with Cloud Services edition.

            * fine_grain (bool, Optional):
                Enable fine granularity. Allowed in Enterprise edition with any value, Basic edition(Allowed values- false), Essentials, Enterprise with Cloud Services edition.

            * http_cookie (str, Optional):
                HTTP cookie name. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Enterprise with Cloud Services edition.

            * http_header (str, Optional):
                HTTP header name. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Enterprise with Cloud Services edition.

            * rate_limiter (dict[str, Any], Optional):
                rate_limiter

                * burst_sz (int, Optional):
                    Maximum number of connections, requests or packets to be let through instantaneously.  If this is less than count, it will have no effect. Allowed values are 0-1000000000. Field introduced in 18.2.9. Allowed in Enterprise edition with any value, Basic edition(Allowed values- 0), Essentials, Enterprise with Cloud Services edition.

                * count (int):
                    Maximum number of connections, requests or packets permitted each period. Allowed values are 1-1000000000. Field introduced in 18.2.9. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str, Optional):
                    Identifier for Rate Limit. Constructed according to context. Field introduced in 18.2.9. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * period (int):
                    Time value in seconds to enforce rate count. Allowed values are 1-1000000000. Field introduced in 18.2.9. Unit is SEC. Allowed in Enterprise edition with any value, Basic edition(Allowed values- 1), Essentials, Enterprise with Cloud Services edition.

        min_health_monitors_up(int, Optional):
            Minimum number of health monitors in UP state to mark server UP. Field introduced in 18.2.1, 17.2.12. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        min_servers_up(int, Optional):
            Minimum number of servers in UP state for marking the pool UP. Field introduced in 18.2.1, 17.2.12. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        networks(List[dict[str, Any]], Optional):
            (internal-use) Networks designated as containing servers for this pool.  The servers may be further narrowed down by a filter. This field is used internally by Avi, not editable by the user. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * network_ref (str):
                 It is a reference to an object of type VIMgrNWRuntime. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * server_filter (str, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        nsx_securitygroup(List[str], Optional):
            A list of NSX Groups where the Servers for the Pool are created . Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        pki_profile_ref(str, Optional):
            Avi will validate the SSL certificate present by a server against the selected PKI Profile. It is a reference to an object of type PKIProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        placement_networks(List[dict[str, Any]], Optional):
            Manually select the networks and subnets used to provide reachability to the pool's servers.  Specify the Subnet using the following syntax  10-1-1-0/24. Use static routes in VRF configuration when pool servers are not directly connected but routable from the service engine. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * network_ref (str):
                 It is a reference to an object of type Network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * subnet (dict[str, Any]):
                subnet

                * ip_addr (dict[str, Any]):
                    ip_addr

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mask (int):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        pool_type(str, Optional):
            Type or Purpose, the Pool is to be used for. Enum options - POOL_TYPE_GENERIC_APP, POOL_TYPE_OAUTH. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        request_queue_depth(int, Optional):
            Minimum number of requests to be queued when pool is full. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 128), Basic edition(Allowed values- 128), Enterprise with Cloud Services edition. Defaults to None.

        request_queue_enabled(bool, Optional):
            Enable request queue when pool is full. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        resolve_pool_by_dns(bool, Optional):
            This field is used as a flag to create a job for JobManager. Field introduced in 18.2.10,20.1.2. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        rewrite_host_header_to_server_name(bool, Optional):
            Rewrite incoming Host Header to server name of the server to which the request is proxied.  Enabling this feature rewrites Host Header for requests to all servers in the pool. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        rewrite_host_header_to_sni(bool, Optional):
            If SNI server name is specified, rewrite incoming host header to the SNI server name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        routing_pool(bool, Optional):
            Enable to do routing when this pool is selected to send traffic. No servers present in routing pool. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        server_disable_type(str, Optional):
            Server graceful disable timeout behaviour. Enum options - DISALLOW_NEW_CONNECTION, ALLOW_NEW_CONNECTION_IF_PERSISTENCE_PRESENT. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        server_name(str, Optional):
            Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections if SNI is enabled. If no value is specified, Avi will use the incoming host header instead. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        server_reselect(dict[str, Any], Optional):
            server_reselect. Defaults to None.

            * enabled (bool):
                Enable HTTP request reselect when server responds with specific response codes. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * num_retries (int, Optional):
                Number of times to retry an HTTP request when server responds with configured status codes. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * retry_nonidempotent (bool, Optional):
                Allow retry of non-idempotent HTTP requests. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * retry_timeout (int, Optional):
                Timeout per retry attempt, for a given request. Value of 0 indicates default timeout. Allowed values are 0-3600000. Field introduced in 18.1.5,18.2.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * svr_resp_code (dict[str, Any], Optional):
                svr_resp_code

                * codes (List[int], Optional):
                    HTTP response code to be matched. Allowed values are 400-599. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ranges (List[dict[str, Any]], Optional):
                    HTTP response code ranges to match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * begin (int):
                        Starting HTTP response status code. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * end (int):
                        Ending HTTP response status code. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * resp_code_block (List[str], Optional):
                    Block of HTTP response codes to match for server reselect. Enum options - HTTP_RSP_4XX, HTTP_RSP_5XX. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        server_timeout(int, Optional):
            Server timeout value specifies the time within which a server connection needs to be established and a request-response exchange completes between AVI and the server. Value of 0 results in using default timeout of 60 minutes. Allowed values are 0-21600000. Field introduced in 18.1.5,18.2.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        servers(List[dict[str, Any]], Optional):
            The pool directs load balanced traffic to this list of destination servers. The servers can be configured by IP address, name, network or via IP Address Group. Maximum of 5000 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * autoscaling_group_name (str, Optional):
                Name of autoscaling group this server belongs to. Field introduced in 17.1.2. Allowed in Enterprise edition with any value, Basic, Enterprise with Cloud Services edition.

            * availability_zone (str, Optional):
                Availability-zone of the server VM. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * description (str, Optional):
                A description of the Server. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * discovered_networks (List[dict[str, Any]], Optional):
                (internal-use) Discovered networks providing reachability for server IP. This field is used internally by Avi, not editable by the user. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * network_ref (str):
                    Discovered network for this IP. It is a reference to an object of type Network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * subnet (List[dict[str, Any]], Optional):
                    Discovered subnet for this IP. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * subnet6 (List[dict[str, Any]], Optional):
                    Discovered IPv6 subnet for this IP. Field introduced in 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enabled (bool, Optional):
                Enable, Disable or Graceful Disable determine if new or existing connections to the server are allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * external_orchestration_id (str, Optional):
                UID of server in external orchestration systems. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * external_uuid (str, Optional):
                UUID identifying VM in OpenStack and other external compute. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * hostname (str, Optional):
                DNS resolvable name of the server.  May be used in place of the IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ip (dict[str, Any]):
                ip

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * location (dict[str, Any], Optional):
                location

                * latitude (float, Optional):
                    Latitude of the location. This is represented as degrees.minutes. The range is from -90.0 (south) to +90.0 (north). Allowed values are -90.0-+90.0. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * longitude (float, Optional):
                    Longitude of the location. This is represented as degrees.minutes. The range is from -180.0 (west) to +180.0 (east). Allowed values are -180.0-+180.0. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str, Optional):
                    Location name in the format Country/State/City. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * tag (str, Optional):
                    Location tag string - example  USEast. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mac_address (str, Optional):
                MAC address of server. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * nw_ref (str, Optional):
                (internal-use) This field is used internally by Avi, not editable by the user. It is a reference to an object of type VIMgrNWRuntime. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * port (int, Optional):
                Optionally specify the servers port number.  This will override the pool's default server port attribute. Allowed values are 1-65535. Special values are 0- use backend port in pool. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * preference_order (int, Optional):
                Preference order of this member in the group. The DNS Service chooses the member with the lowest preference that is operationally up. Allowed values are 1-128. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

            * prst_hdr_val (str, Optional):
                Header value for custom header persistence. . Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ratio (int, Optional):
                Ratio of selecting eligible servers in the pool. Allowed values are 1-20. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * resolve_server_by_dns (bool, Optional):
                Auto resolve server's IP using DNS name. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * rewrite_host_header (bool, Optional):
                Rewrite incoming Host Header to server name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * server_node (str, Optional):
                Hostname of the node where the server VM or container resides. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * static (bool, Optional):
                If statically learned. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * verify_network (bool, Optional):
                Verify server belongs to a discovered network or reachable via a discovered network. Verify reachable network isn't the OpenStack management network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vm_ref (str, Optional):
                (internal-use) This field is used internally by Avi, not editable by the user. It is a reference to an object of type VIMgrVMRuntime. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        service_metadata(str, Optional):
            Metadata pertaining to the service provided by this Pool. In Openshift/Kubernetes environments, app metadata info is stored. Any user input to this field will be overwritten by Avi Vantage. Field introduced in 17.2.14,18.1.5,18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        sni_enabled(bool, Optional):
            Enable TLS SNI for server connections. If disabled, Avi will not send the SNI extension as part of the handshake. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        sp_gs_info(dict[str, Any], Optional):
            sp_gs_info. Defaults to None.

            * fqdns (List[str], Optional):
                FQDNs associated with the GSLB service. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * gs_ref (str, Optional):
                GSLB service uuid associated with the site persistence pool. It is a reference to an object of type GslbService. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        ssl_key_and_certificate_ref(str, Optional):
            Service Engines will present a client SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ssl_profile_ref(str, Optional):
            When enabled, Avi re-encrypts traffic to the backend servers. The specific SSL profile defines which ciphers and SSL versions will be supported. It is a reference to an object of type SSLProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        tier1_lr(str, Optional):
            This tier1_lr field should be set same as VirtualService associated for NSX-T. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        use_service_port(bool, Optional):
            Do not translate the client's destination port when sending the connection to the server. Monitor port needs to be specified for health monitors. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic, Enterprise with Cloud Services edition. Defaults to None.

        use_service_ssl_mode(bool, Optional):
            This applies only when use_service_port is set to true. If enabled, SSL mode of the connection to the server is decided by the SSL mode on the Virtualservice service port, on which the request was received. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vrf_ref(str, Optional):
            Virtual Routing Context that the pool is bound to. This is used to provide the isolation of the set of networks the pool is attached to. The pool inherits the Virtual Routing Context of the Virtual Service, and this field is used only internally, and is set by pb-transform. It is a reference to an object of type VrfContext. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              nsx_alb.alb.pool.present:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.pool.create
    """

    result = dict(comment=[], ret=[], result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "analytics_policy": "analytics_policy",
        "analytics_profile_ref": "analytics_profile_ref",
        "append_port": "append_port",
        "application_persistence_profile_ref": "application_persistence_profile_ref",
        "autoscale_launch_config_ref": "autoscale_launch_config_ref",
        "autoscale_networks": "autoscale_networks",
        "autoscale_policy_ref": "autoscale_policy_ref",
        "capacity_estimation": "capacity_estimation",
        "capacity_estimation_ttfb_thresh": "capacity_estimation_ttfb_thresh",
        "cloud_config_cksum": "cloud_config_cksum",
        "cloud_ref": "cloud_ref",
        "configpb_attributes": "configpb_attributes",
        "conn_pool_properties": "conn_pool_properties",
        "connection_ramp_duration": "connection_ramp_duration",
        "created_by": "created_by",
        "default_server_port": "default_server_port",
        "delete_server_on_dns_refresh": "delete_server_on_dns_refresh",
        "description": "description",
        "domain_name": "domain_name",
        "east_west": "east_west",
        "enable_http2": "enable_http2",
        "enabled": "enabled",
        "external_autoscale_groups": "external_autoscale_groups",
        "fail_action": "fail_action",
        "fewest_tasks_feedback_delay": "fewest_tasks_feedback_delay",
        "graceful_disable_timeout": "graceful_disable_timeout",
        "gslb_sp_enabled": "gslb_sp_enabled",
        "health_monitor_refs": "health_monitor_refs",
        "horizon_profile": "horizon_profile",
        "host_check_enabled": "host_check_enabled",
        "http2_properties": "http2_properties",
        "ignore_server_port": "ignore_server_port",
        "inline_health_monitor": "inline_health_monitor",
        "ipaddrgroup_ref": "ipaddrgroup_ref",
        "lb_algo_rr_per_se": "lb_algo_rr_per_se",
        "lb_algorithm": "lb_algorithm",
        "lb_algorithm_consistent_hash_hdr": "lb_algorithm_consistent_hash_hdr",
        "lb_algorithm_core_nonaffinity": "lb_algorithm_core_nonaffinity",
        "lb_algorithm_hash": "lb_algorithm_hash",
        "lookup_server_by_name": "lookup_server_by_name",
        "markers": "markers",
        "max_concurrent_connections_per_server": "max_concurrent_connections_per_server",
        "max_conn_rate_per_server": "max_conn_rate_per_server",
        "min_health_monitors_up": "min_health_monitors_up",
        "min_servers_up": "min_servers_up",
        "name": "name",
        "networks": "networks",
        "nsx_securitygroup": "nsx_securitygroup",
        "pki_profile_ref": "pki_profile_ref",
        "placement_networks": "placement_networks",
        "pool_type": "pool_type",
        "request_queue_depth": "request_queue_depth",
        "request_queue_enabled": "request_queue_enabled",
        "resolve_pool_by_dns": "resolve_pool_by_dns",
        "rewrite_host_header_to_server_name": "rewrite_host_header_to_server_name",
        "rewrite_host_header_to_sni": "rewrite_host_header_to_sni",
        "routing_pool": "routing_pool",
        "server_disable_type": "server_disable_type",
        "server_name": "server_name",
        "server_reselect": "server_reselect",
        "server_timeout": "server_timeout",
        "servers": "servers",
        "service_metadata": "service_metadata",
        "sni_enabled": "sni_enabled",
        "sp_gs_info": "sp_gs_info",
        "ssl_key_and_certificate_ref": "ssl_key_and_certificate_ref",
        "ssl_profile_ref": "ssl_profile_ref",
        "tenant_ref": "tenant_ref",
        "tier1_lr": "tier1_lr",
        "use_service_port": "use_service_port",
        "use_service_ssl_mode": "use_service_ssl_mode",
        "vrf_ref": "vrf_ref",
    }

    payload = {}
    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = value

    create = await hub.tool.nsx_alb.session.request(
        ctx,
        method="post",
        path="/pool",
        query_params={},
        data=payload,
    )

    if not create["result"]:
        result["comment"].append(create["comment"])
        result["result"] = False
        return result

    result["comment"].append(
        f"Created nsx_alb.alb.pool '{name}'",
    )

    result["ret"] = create["ret"]

    result["ret"]["resource_id"] = create["ret"]["uuid"]
    return result


async def update(
    hub,
    ctx,
    resource_id: str,
    name: str = None,
    analytics_policy: make_dataclass(
        "analytics_policy", [("enable_realtime_metrics", bool, field(default=None))]
    ) = None,
    analytics_profile_ref: str = None,
    append_port: str = None,
    application_persistence_profile_ref: str = None,
    autoscale_launch_config_ref: str = None,
    autoscale_networks: List[str] = None,
    autoscale_policy_ref: str = None,
    capacity_estimation: bool = None,
    capacity_estimation_ttfb_thresh: int = None,
    cloud_config_cksum: str = None,
    cloud_ref: str = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    conn_pool_properties: make_dataclass(
        "conn_pool_properties",
        [
            ("upstream_connpool_conn_idle_tmo", int, field(default=None)),
            ("upstream_connpool_conn_life_tmo", int, field(default=None)),
            ("upstream_connpool_conn_max_reuse", int, field(default=None)),
            ("upstream_connpool_server_max_cache", int, field(default=None)),
        ],
    ) = None,
    connection_ramp_duration: int = None,
    created_by: str = None,
    default_server_port: int = None,
    delete_server_on_dns_refresh: bool = None,
    description: str = None,
    domain_name: List[str] = None,
    east_west: bool = None,
    enable_http2: bool = None,
    enabled: bool = None,
    external_autoscale_groups: List[str] = None,
    fail_action: make_dataclass(
        "fail_action",
        [
            ("type", str),
            (
                "local_rsp",
                make_dataclass(
                    "local_rsp",
                    [
                        (
                            "file",
                            make_dataclass(
                                "file",
                                [
                                    ("content_type", str),
                                    ("file_content", str),
                                    ("file_length", int, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("status_code", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "redirect",
                make_dataclass(
                    "redirect",
                    [
                        ("host", str),
                        ("path", str, field(default=None)),
                        ("protocol", str, field(default=None)),
                        ("query", str, field(default=None)),
                        ("status_code", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    fewest_tasks_feedback_delay: int = None,
    graceful_disable_timeout: int = None,
    gslb_sp_enabled: bool = None,
    health_monitor_refs: List[str] = None,
    horizon_profile: make_dataclass(
        "horizon_profile",
        [
            ("blast_port", int, field(default=None)),
            ("pcoip_port", int, field(default=None)),
        ],
    ) = None,
    host_check_enabled: bool = None,
    http2_properties: make_dataclass(
        "http2_properties",
        [
            ("max_http2_control_frames_per_connection", int, field(default=None)),
            ("max_http2_header_field_size", int, field(default=None)),
        ],
    ) = None,
    ignore_server_port: bool = None,
    inline_health_monitor: bool = None,
    ipaddrgroup_ref: str = None,
    lb_algo_rr_per_se: bool = None,
    lb_algorithm: str = None,
    lb_algorithm_consistent_hash_hdr: str = None,
    lb_algorithm_core_nonaffinity: int = None,
    lb_algorithm_hash: str = None,
    lookup_server_by_name: bool = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    max_concurrent_connections_per_server: int = None,
    max_conn_rate_per_server: make_dataclass(
        "max_conn_rate_per_server",
        [
            (
                "action",
                make_dataclass(
                    "action",
                    [
                        (
                            "file",
                            make_dataclass(
                                "file",
                                [
                                    ("content_type", str),
                                    ("file_content", str),
                                    ("file_length", int, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "redirect",
                            make_dataclass(
                                "redirect",
                                [
                                    ("protocol", str),
                                    ("add_string", str, field(default=None)),
                                    (
                                        "host",
                                        make_dataclass(
                                            "host",
                                            [
                                                ("type", str),
                                                (
                                                    "tokens",
                                                    List[
                                                        make_dataclass(
                                                            "tokens",
                                                            [
                                                                ("type", str),
                                                                (
                                                                    "end_index",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "start_index",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "str_value",
                                                                    str,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        )
                                                    ],
                                                    field(default=None),
                                                ),
                                            ],
                                        ),
                                        field(default=None),
                                    ),
                                    ("keep_query", bool, field(default=None)),
                                    (
                                        "path",
                                        make_dataclass(
                                            "path",
                                            [
                                                ("type", str),
                                                (
                                                    "tokens",
                                                    List[
                                                        make_dataclass(
                                                            "tokens",
                                                            [
                                                                ("type", str),
                                                                (
                                                                    "end_index",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "start_index",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "str_value",
                                                                    str,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        )
                                                    ],
                                                    field(default=None),
                                                ),
                                            ],
                                        ),
                                        field(default=None),
                                    ),
                                    ("port", int, field(default=None)),
                                    ("status_code", str, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("status_code", str, field(default=None)),
                        ("type", str, field(default=None)),
                    ],
                ),
            ),
            ("explicit_tracking", bool, field(default=None)),
            ("fine_grain", bool, field(default=None)),
            ("http_cookie", str, field(default=None)),
            ("http_header", str, field(default=None)),
            (
                "rate_limiter",
                make_dataclass(
                    "rate_limiter",
                    [
                        ("count", int),
                        ("period", int),
                        ("burst_sz", int, field(default=None)),
                        ("name", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    min_health_monitors_up: int = None,
    min_servers_up: int = None,
    networks: List[
        make_dataclass(
            "networks",
            [("network_ref", str), ("server_filter", str, field(default=None))],
        )
    ] = None,
    nsx_securitygroup: List[str] = None,
    pki_profile_ref: str = None,
    placement_networks: List[
        make_dataclass(
            "placement_networks",
            [
                ("network_ref", str),
                (
                    "subnet",
                    make_dataclass(
                        "subnet",
                        [
                            (
                                "ip_addr",
                                make_dataclass(
                                    "ip_addr", [("addr", str), ("type", str)]
                                ),
                            ),
                            ("mask", int),
                        ],
                    ),
                ),
            ],
        )
    ] = None,
    pool_type: str = None,
    request_queue_depth: int = None,
    request_queue_enabled: bool = None,
    resolve_pool_by_dns: bool = None,
    rewrite_host_header_to_server_name: bool = None,
    rewrite_host_header_to_sni: bool = None,
    routing_pool: bool = None,
    server_disable_type: str = None,
    server_name: str = None,
    server_reselect: make_dataclass(
        "server_reselect",
        [
            ("enabled", bool),
            ("num_retries", int, field(default=None)),
            ("retry_nonidempotent", bool, field(default=None)),
            ("retry_timeout", int, field(default=None)),
            (
                "svr_resp_code",
                make_dataclass(
                    "svr_resp_code",
                    [
                        ("codes", List[int], field(default=None)),
                        (
                            "ranges",
                            List[
                                make_dataclass("ranges", [("begin", int), ("end", int)])
                            ],
                            field(default=None),
                        ),
                        ("resp_code_block", List[str], field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    server_timeout: int = None,
    servers: List[
        make_dataclass(
            "servers",
            [
                ("ip", make_dataclass("ip", [("addr", str), ("type", str)])),
                ("autoscaling_group_name", str, field(default=None)),
                ("availability_zone", str, field(default=None)),
                ("description", str, field(default=None)),
                (
                    "discovered_networks",
                    List[
                        make_dataclass(
                            "discovered_networks",
                            [
                                ("network_ref", str),
                                (
                                    "subnet",
                                    List[
                                        make_dataclass(
                                            "subnet",
                                            [
                                                (
                                                    "ip_addr",
                                                    make_dataclass(
                                                        "ip_addr",
                                                        [("addr", str), ("type", str)],
                                                    ),
                                                ),
                                                ("mask", int),
                                            ],
                                        )
                                    ],
                                    field(default=None),
                                ),
                                (
                                    "subnet6",
                                    List[
                                        make_dataclass(
                                            "subnet6",
                                            [
                                                (
                                                    "ip_addr",
                                                    make_dataclass(
                                                        "ip_addr",
                                                        [("addr", str), ("type", str)],
                                                    ),
                                                ),
                                                ("mask", int),
                                            ],
                                        )
                                    ],
                                    field(default=None),
                                ),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                ("enabled", bool, field(default=None)),
                ("external_orchestration_id", str, field(default=None)),
                ("external_uuid", str, field(default=None)),
                ("hostname", str, field(default=None)),
                (
                    "location",
                    make_dataclass(
                        "location",
                        [
                            ("latitude", float, field(default=None)),
                            ("longitude", float, field(default=None)),
                            ("name", str, field(default=None)),
                            ("tag", str, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                ("mac_address", str, field(default=None)),
                ("nw_ref", str, field(default=None)),
                ("port", int, field(default=None)),
                ("preference_order", int, field(default=None)),
                ("prst_hdr_val", str, field(default=None)),
                ("ratio", int, field(default=None)),
                ("resolve_server_by_dns", bool, field(default=None)),
                ("rewrite_host_header", bool, field(default=None)),
                ("server_node", str, field(default=None)),
                ("static", bool, field(default=None)),
                ("verify_network", bool, field(default=None)),
                ("vm_ref", str, field(default=None)),
            ],
        )
    ] = None,
    service_metadata: str = None,
    sni_enabled: bool = None,
    sp_gs_info: make_dataclass(
        "sp_gs_info",
        [
            ("fqdns", List[str], field(default=None)),
            ("gs_ref", str, field(default=None)),
        ],
    ) = None,
    ssl_key_and_certificate_ref: str = None,
    ssl_profile_ref: str = None,
    tenant_ref: str = None,
    tier1_lr: str = None,
    use_service_port: bool = None,
    use_service_ssl_mode: bool = None,
    vrf_ref: str = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:
        resource_id(str):
            Alb.pool unique ID.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

        analytics_policy(dict[str, Any], Optional):
            analytics_policy. Defaults to None.

            * enable_realtime_metrics (bool, Optional):
                Enable real time metrics for server and pool metrics eg. l4_server.xxx, l7_server.xxx. Field introduced in 18.1.5, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        analytics_profile_ref(str, Optional):
            Specifies settings related to analytics. It is a reference to an object of type AnalyticsProfile. Field introduced in 18.1.4,18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        append_port(str, Optional):
            Allows the option to append port to hostname in the host header while sending a request to the server. By default, port is appended for non-default ports. This setting will apply for Pool's 'Rewrite Host Header to Server Name', 'Rewrite Host Header to SNI' features and Server's 'Rewrite Host Header' settings as well as HTTP healthmonitors attached to pools. Enum options - NON_DEFAULT_80_443, NEVER, ALWAYS. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- NEVER), Basic edition(Allowed values- NEVER), Enterprise with Cloud Services edition. Special default for Essentials edition is NEVER, Basic edition is NEVER, Enterprise is NON_DEFAULT_80_443. Defaults to None.

        application_persistence_profile_ref(str, Optional):
            Persistence will ensure the same user sticks to the same server for a desired duration of time. It is a reference to an object of type ApplicationPersistenceProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        autoscale_launch_config_ref(str, Optional):
            If configured then Avi will trigger orchestration of pool server creation and deletion. It is a reference to an object of type AutoScaleLaunchConfig. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        autoscale_networks(List[str], Optional):
            Network Ids for the launch configuration. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        autoscale_policy_ref(str, Optional):
            Reference to Server Autoscale Policy. It is a reference to an object of type ServerAutoScalePolicy. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        capacity_estimation(bool, Optional):
            Inline estimation of capacity of servers. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        capacity_estimation_ttfb_thresh(int, Optional):
            The maximum time-to-first-byte of a server. Allowed values are 1-5000. Special values are 0 - Automatic. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Defaults to None.

        cloud_config_cksum(str, Optional):
            Checksum of cloud configuration for Pool. Internally set by cloud connector. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        cloud_ref(str, Optional):
             It is a reference to an object of type Cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        conn_pool_properties(dict[str, Any], Optional):
            conn_pool_properties. Defaults to None.

            * upstream_connpool_conn_idle_tmo (int, Optional):
                Connection idle timeout. Allowed values are 0-86400000. Special values are 0- Infinite idle time.. Field introduced in 18.2.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 60000), Basic edition(Allowed values- 60000), Enterprise with Cloud Services edition.

            * upstream_connpool_conn_life_tmo (int, Optional):
                Connection life timeout. Allowed values are 0-86400000. Special values are 0- Infinite life time.. Field introduced in 18.2.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 600000), Basic edition(Allowed values- 600000), Enterprise with Cloud Services edition.

            * upstream_connpool_conn_max_reuse (int, Optional):
                Maximum number of times a connection can be reused. Special values are 0- unlimited. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition.

            * upstream_connpool_server_max_cache (int, Optional):
                Maximum number of connections a server can cache. Special values are 0- unlimited. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        connection_ramp_duration(int, Optional):
            Duration for which new connections will be gradually ramped up to a server recently brought online.  Useful for LB algorithms that are least connection based. Allowed values are 1-300. Special values are 0 - Immediate. Unit is MIN. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Special default for Essentials edition is 0, Basic edition is 0, Enterprise is 10. Defaults to None.

        created_by(str, Optional):
            Creator name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        default_server_port(int, Optional):
            Traffic sent to servers will use this destination server port unless overridden by the server's specific port attribute. The SSL checkbox enables Avi to server encryption. Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        delete_server_on_dns_refresh(bool, Optional):
            Indicates whether existing IPs are disabled(false) or deleted(true) on dns hostname refreshDetail -- On a dns refresh, some IPs set on pool may no longer be returned by the resolver. These IPs are deleted from the pool when this knob is set to true. They are disabled, if the knob is set to false. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- true), Basic edition(Allowed values- true), Enterprise with Cloud Services edition. Defaults to None.

        description(str, Optional):
            A description of the pool. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        domain_name(List[str], Optional):
            Comma separated list of domain names which will be used to verify the common names or subject alternative names presented by server certificates. It is performed only when common name check host_check_enabled is enabled. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        east_west(bool, Optional):
            Inherited config from VirtualService. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        enable_http2(bool, Optional):
            Enable HTTP/2 for traffic from VirtualService to all backend servers in this pool. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        enabled(bool, Optional):
            Enable or disable the pool.  Disabling will terminate all open connections and pause health monitors. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        external_autoscale_groups(List[str], Optional):
            Names of external auto-scale groups for pool servers. Currently available only for AWS and Azure. Field introduced in 17.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        fail_action(dict[str, Any], Optional):
            fail_action. Defaults to None.

            * local_rsp (dict[str, Any], Optional):
                local_rsp

                * file (dict[str, Any], Optional):
                    file

                    * content_type (str):
                        Mime-type of the content in the file. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * file_content (str):
                        File content to used in the local HTTP response body. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * file_length (int, Optional):
                        File content length. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * status_code (str, Optional):
                     Enum options - FAIL_HTTP_STATUS_CODE_200, FAIL_HTTP_STATUS_CODE_503. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * redirect (dict[str, Any], Optional):
                redirect

                * host (str):
                    The host to which the redirect request is sent. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * path (str, Optional):
                    Path configuration for the redirect request. If not set the path from the original request's URI is preserved in the redirect on pool failure. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * protocol (str, Optional):
                     Enum options - HTTP, HTTPS. Allowed in Enterprise edition with any value, Basic edition(Allowed values- HTTP), Essentials, Enterprise with Cloud Services edition. Special default for Basic edition is HTTP, Enterprise is HTTPS.

                * query (str, Optional):
                    Query configuration for the redirect request URI. If not set, the query from the original request's URI is preserved in the redirect on pool failure. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * status_code (str, Optional):
                     Enum options - HTTP_REDIRECT_STATUS_CODE_301, HTTP_REDIRECT_STATUS_CODE_302, HTTP_REDIRECT_STATUS_CODE_307. Allowed in Enterprise edition with any value, Basic edition(Allowed values- HTTP_REDIRECT_STATUS_CODE_302), Essentials, Enterprise with Cloud Services edition.

            * type (str):
                Enables a response to client when pool experiences a failure. By default TCP connection is closed. Enum options - FAIL_ACTION_HTTP_REDIRECT, FAIL_ACTION_HTTP_LOCAL_RSP, FAIL_ACTION_CLOSE_CONN, FAIL_ACTION_BACKUP_POOL. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- FAIL_ACTION_CLOSE_CONN), Basic edition(Allowed values- FAIL_ACTION_CLOSE_CONN,FAIL_ACTION_HTTP_REDIRECT), Enterprise with Cloud Services edition.

        fewest_tasks_feedback_delay(int, Optional):
            Periodicity of feedback for fewest tasks server selection algorithm. Allowed values are 1-300. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        graceful_disable_timeout(int, Optional):
            Used to gracefully disable a server. Virtual service waits for the specified time before terminating the existing connections  to the servers that are disabled. Allowed values are 1-7200. Special values are 0 - Immediate, -1 - Infinite. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        gslb_sp_enabled(bool, Optional):
            Indicates if the pool is a site-persistence pool. . Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        health_monitor_refs(List[str], Optional):
            Verify server health by applying one or more health monitors.  Active monitors generate synthetic traffic from each Service Engine and mark a server up or down based on the response. The Passive monitor listens only to client to server communication. It raises or lowers the ratio of traffic destined to a server based on successful responses. It is a reference to an object of type HealthMonitor. Maximum of 50 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        horizon_profile(dict[str, Any], Optional):
            horizon_profile. Defaults to None.

            * blast_port (int, Optional):
                Horizon blast port of the UAG server. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * pcoip_port (int, Optional):
                Horizon pcoip port of the UAG server. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        host_check_enabled(bool, Optional):
            Enable common name check for server certificate. If enabled and no explicit domain name is specified, Avi will use the incoming host header to do the match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        http2_properties(dict[str, Any], Optional):
            http2_properties. Defaults to None.

            * max_http2_control_frames_per_connection (int, Optional):
                The max number of control frames that server can send over an HTTP/2 connection. '0' means unlimited. Allowed values are 0-10000. Special values are 0- Unlimited control frames on a server side HTTP/2 connection. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * max_http2_header_field_size (int, Optional):
                The maximum size in bytes of the compressed request header field. The limit applies equally to both name and value. Allowed values are 1-8192. Field introduced in 21.1.1. Unit is BYTES. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        ignore_server_port(bool, Optional):
            Ignore the server port in building the load balancing state.Applicable only for consistent hash load balancing algorithm or Disable Port translation (use_service_port) use cases. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        inline_health_monitor(bool, Optional):
            The Passive monitor will monitor client to server connections and requests and adjust traffic load to servers based on successful responses.  This may alter the expected behavior of the LB method, such as Round Robin. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ipaddrgroup_ref(str, Optional):
            Use list of servers from Ip Address Group. It is a reference to an object of type IpAddrGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        lb_algo_rr_per_se(bool, Optional):
            Do Round Robin load load balancing at SE level instead of the default per core load balancing. Field introduced in 21.1.5, 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        lb_algorithm(str, Optional):
            The load balancing algorithm will pick a server within the pool's list of available servers. Values LB_ALGORITHM_NEAREST_SERVER and LB_ALGORITHM_TOPOLOGY are only allowed for GSLB pool. Enum options - LB_ALGORITHM_LEAST_CONNECTIONS, LB_ALGORITHM_ROUND_ROBIN, LB_ALGORITHM_FASTEST_RESPONSE, LB_ALGORITHM_CONSISTENT_HASH, LB_ALGORITHM_LEAST_LOAD, LB_ALGORITHM_FEWEST_SERVERS, LB_ALGORITHM_RANDOM, LB_ALGORITHM_FEWEST_TASKS, LB_ALGORITHM_NEAREST_SERVER, LB_ALGORITHM_CORE_AFFINITY, LB_ALGORITHM_TOPOLOGY. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- LB_ALGORITHM_LEAST_CONNECTIONS,LB_ALGORITHM_ROUND_ROBIN,LB_ALGORITHM_CONSISTENT_HASH), Basic edition(Allowed values- LB_ALGORITHM_LEAST_CONNECTIONS,LB_ALGORITHM_ROUND_ROBIN,LB_ALGORITHM_CONSISTENT_HASH), Enterprise with Cloud Services edition. Defaults to None.

        lb_algorithm_consistent_hash_hdr(str, Optional):
            HTTP header name to be used for the hash key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        lb_algorithm_core_nonaffinity(int, Optional):
            Degree of non-affinity for core affinity based server selection. Allowed values are 1-65535. Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 2), Basic edition(Allowed values- 2), Enterprise with Cloud Services edition. Defaults to None.

        lb_algorithm_hash(str, Optional):
            Criteria used as a key for determining the hash between the client and  server. Enum options - LB_ALGORITHM_CONSISTENT_HASH_SOURCE_IP_ADDRESS, LB_ALGORITHM_CONSISTENT_HASH_SOURCE_IP_ADDRESS_AND_PORT, LB_ALGORITHM_CONSISTENT_HASH_URI, LB_ALGORITHM_CONSISTENT_HASH_CUSTOM_HEADER, LB_ALGORITHM_CONSISTENT_HASH_CUSTOM_STRING, LB_ALGORITHM_CONSISTENT_HASH_CALLID. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- LB_ALGORITHM_CONSISTENT_HASH_SOURCE_IP_ADDRESS), Basic edition(Allowed values- LB_ALGORITHM_CONSISTENT_HASH_SOURCE_IP_ADDRESS), Enterprise with Cloud Services edition. Defaults to None.

        lookup_server_by_name(bool, Optional):
            Allow server lookup by name. Field introduced in 17.1.11,17.2.4. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        max_concurrent_connections_per_server(int, Optional):
            The maximum number of concurrent connections allowed to each server within the pool. NOTE  applied value will be no less than the number of service engines that the pool is placed on. If set to 0, no limit is applied. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_conn_rate_per_server(dict[str, Any], Optional):
            max_conn_rate_per_server. Defaults to None.

            * action (dict[str, Any]):
                action

                * file (dict[str, Any], Optional):
                    file

                    * content_type (str):
                        Mime-type of the content in the file. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * file_content (str):
                        File content to used in the local HTTP response body. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * file_length (int, Optional):
                        File content length. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * redirect (dict[str, Any], Optional):
                    redirect

                    * add_string (str, Optional):
                        Add a query string to the redirect URI. If keep_query is set, concatenates the add_string to the query of the incoming request. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * host (dict[str, Any], Optional):
                        host

                        * tokens (List[dict[str, Any]], Optional):
                            Token config either for the URI components or a constant string. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * end_index (int, Optional):
                                Index of the ending token in the incoming URI. Allowed values are 0-65534. Special values are 65535 - end of string. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * start_index (int, Optional):
                                Index of the starting token in the incoming URI. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * str_value (str, Optional):
                                Constant string to use as a token. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                Token type for constructing the URI. Enum options - URI_TOKEN_TYPE_HOST, URI_TOKEN_TYPE_PATH, URI_TOKEN_TYPE_STRING, URI_TOKEN_TYPE_STRING_GROUP, URI_TOKEN_TYPE_REGEX, URI_TOKEN_TYPE_REGEX_QUERY. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                            URI param type. Enum options - URI_PARAM_TYPE_TOKENIZED. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * keep_query (bool, Optional):
                        Keep or drop the query of the incoming request URI in the redirected URI. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * path (dict[str, Any], Optional):
                        path

                        * tokens (List[dict[str, Any]], Optional):
                            Token config either for the URI components or a constant string. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * end_index (int, Optional):
                                Index of the ending token in the incoming URI. Allowed values are 0-65534. Special values are 65535 - end of string. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * start_index (int, Optional):
                                Index of the starting token in the incoming URI. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * str_value (str, Optional):
                                Constant string to use as a token. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                Token type for constructing the URI. Enum options - URI_TOKEN_TYPE_HOST, URI_TOKEN_TYPE_PATH, URI_TOKEN_TYPE_STRING, URI_TOKEN_TYPE_STRING_GROUP, URI_TOKEN_TYPE_REGEX, URI_TOKEN_TYPE_REGEX_QUERY. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                            URI param type. Enum options - URI_PARAM_TYPE_TOKENIZED. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * port (int, Optional):
                        Port to which redirect the request. Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * protocol (str):
                        Protocol type. Enum options - HTTP, HTTPS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * status_code (str, Optional):
                        HTTP redirect status code. Enum options - HTTP_REDIRECT_STATUS_CODE_301, HTTP_REDIRECT_STATUS_CODE_302, HTTP_REDIRECT_STATUS_CODE_307. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * status_code (str, Optional):
                    HTTP status code for Local Response rate limit action. Enum options - HTTP_LOCAL_RESPONSE_STATUS_CODE_200, HTTP_LOCAL_RESPONSE_STATUS_CODE_204, HTTP_LOCAL_RESPONSE_STATUS_CODE_403, HTTP_LOCAL_RESPONSE_STATUS_CODE_404, HTTP_LOCAL_RESPONSE_STATUS_CODE_429, HTTP_LOCAL_RESPONSE_STATUS_CODE_501. Allowed in Enterprise edition with any value, Basic edition(Allowed values- HTTP_LOCAL_RESPONSE_STATUS_CODE_429), Essentials, Enterprise with Cloud Services edition.

                * type (str, Optional):
                    Type of action to be enforced upon hitting the rate limit. Enum options - RL_ACTION_NONE, RL_ACTION_DROP_CONN, RL_ACTION_RESET_CONN, RL_ACTION_CLOSE_CONN, RL_ACTION_LOCAL_RSP, RL_ACTION_REDIRECT. Allowed in Enterprise edition with any value, Basic edition(Allowed values- RL_ACTION_NONE,RL_ACTION_DROP_CONN), Essentials, Enterprise with Cloud Services edition.

            * explicit_tracking (bool, Optional):
                Explicitly tracks an attacker across rate periods. Allowed in Enterprise edition with any value, Basic edition(Allowed values- false), Essentials, Enterprise with Cloud Services edition.

            * fine_grain (bool, Optional):
                Enable fine granularity. Allowed in Enterprise edition with any value, Basic edition(Allowed values- false), Essentials, Enterprise with Cloud Services edition.

            * http_cookie (str, Optional):
                HTTP cookie name. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Enterprise with Cloud Services edition.

            * http_header (str, Optional):
                HTTP header name. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Enterprise with Cloud Services edition.

            * rate_limiter (dict[str, Any], Optional):
                rate_limiter

                * burst_sz (int, Optional):
                    Maximum number of connections, requests or packets to be let through instantaneously.  If this is less than count, it will have no effect. Allowed values are 0-1000000000. Field introduced in 18.2.9. Allowed in Enterprise edition with any value, Basic edition(Allowed values- 0), Essentials, Enterprise with Cloud Services edition.

                * count (int):
                    Maximum number of connections, requests or packets permitted each period. Allowed values are 1-1000000000. Field introduced in 18.2.9. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str, Optional):
                    Identifier for Rate Limit. Constructed according to context. Field introduced in 18.2.9. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * period (int):
                    Time value in seconds to enforce rate count. Allowed values are 1-1000000000. Field introduced in 18.2.9. Unit is SEC. Allowed in Enterprise edition with any value, Basic edition(Allowed values- 1), Essentials, Enterprise with Cloud Services edition.

        min_health_monitors_up(int, Optional):
            Minimum number of health monitors in UP state to mark server UP. Field introduced in 18.2.1, 17.2.12. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        min_servers_up(int, Optional):
            Minimum number of servers in UP state for marking the pool UP. Field introduced in 18.2.1, 17.2.12. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        networks(List[dict[str, Any]], Optional):
            (internal-use) Networks designated as containing servers for this pool.  The servers may be further narrowed down by a filter. This field is used internally by Avi, not editable by the user. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * network_ref (str):
                 It is a reference to an object of type VIMgrNWRuntime. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * server_filter (str, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        nsx_securitygroup(List[str], Optional):
            A list of NSX Groups where the Servers for the Pool are created . Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        pki_profile_ref(str, Optional):
            Avi will validate the SSL certificate present by a server against the selected PKI Profile. It is a reference to an object of type PKIProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        placement_networks(List[dict[str, Any]], Optional):
            Manually select the networks and subnets used to provide reachability to the pool's servers.  Specify the Subnet using the following syntax  10-1-1-0/24. Use static routes in VRF configuration when pool servers are not directly connected but routable from the service engine. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * network_ref (str):
                 It is a reference to an object of type Network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * subnet (dict[str, Any]):
                subnet

                * ip_addr (dict[str, Any]):
                    ip_addr

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mask (int):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        pool_type(str, Optional):
            Type or Purpose, the Pool is to be used for. Enum options - POOL_TYPE_GENERIC_APP, POOL_TYPE_OAUTH. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        request_queue_depth(int, Optional):
            Minimum number of requests to be queued when pool is full. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 128), Basic edition(Allowed values- 128), Enterprise with Cloud Services edition. Defaults to None.

        request_queue_enabled(bool, Optional):
            Enable request queue when pool is full. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        resolve_pool_by_dns(bool, Optional):
            This field is used as a flag to create a job for JobManager. Field introduced in 18.2.10,20.1.2. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        rewrite_host_header_to_server_name(bool, Optional):
            Rewrite incoming Host Header to server name of the server to which the request is proxied.  Enabling this feature rewrites Host Header for requests to all servers in the pool. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        rewrite_host_header_to_sni(bool, Optional):
            If SNI server name is specified, rewrite incoming host header to the SNI server name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        routing_pool(bool, Optional):
            Enable to do routing when this pool is selected to send traffic. No servers present in routing pool. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        server_disable_type(str, Optional):
            Server graceful disable timeout behaviour. Enum options - DISALLOW_NEW_CONNECTION, ALLOW_NEW_CONNECTION_IF_PERSISTENCE_PRESENT. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        server_name(str, Optional):
            Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections if SNI is enabled. If no value is specified, Avi will use the incoming host header instead. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        server_reselect(dict[str, Any], Optional):
            server_reselect. Defaults to None.

            * enabled (bool):
                Enable HTTP request reselect when server responds with specific response codes. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * num_retries (int, Optional):
                Number of times to retry an HTTP request when server responds with configured status codes. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * retry_nonidempotent (bool, Optional):
                Allow retry of non-idempotent HTTP requests. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * retry_timeout (int, Optional):
                Timeout per retry attempt, for a given request. Value of 0 indicates default timeout. Allowed values are 0-3600000. Field introduced in 18.1.5,18.2.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * svr_resp_code (dict[str, Any], Optional):
                svr_resp_code

                * codes (List[int], Optional):
                    HTTP response code to be matched. Allowed values are 400-599. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ranges (List[dict[str, Any]], Optional):
                    HTTP response code ranges to match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * begin (int):
                        Starting HTTP response status code. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * end (int):
                        Ending HTTP response status code. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * resp_code_block (List[str], Optional):
                    Block of HTTP response codes to match for server reselect. Enum options - HTTP_RSP_4XX, HTTP_RSP_5XX. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        server_timeout(int, Optional):
            Server timeout value specifies the time within which a server connection needs to be established and a request-response exchange completes between AVI and the server. Value of 0 results in using default timeout of 60 minutes. Allowed values are 0-21600000. Field introduced in 18.1.5,18.2.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        servers(List[dict[str, Any]], Optional):
            The pool directs load balanced traffic to this list of destination servers. The servers can be configured by IP address, name, network or via IP Address Group. Maximum of 5000 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * autoscaling_group_name (str, Optional):
                Name of autoscaling group this server belongs to. Field introduced in 17.1.2. Allowed in Enterprise edition with any value, Basic, Enterprise with Cloud Services edition.

            * availability_zone (str, Optional):
                Availability-zone of the server VM. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * description (str, Optional):
                A description of the Server. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * discovered_networks (List[dict[str, Any]], Optional):
                (internal-use) Discovered networks providing reachability for server IP. This field is used internally by Avi, not editable by the user. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * network_ref (str):
                    Discovered network for this IP. It is a reference to an object of type Network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * subnet (List[dict[str, Any]], Optional):
                    Discovered subnet for this IP. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * subnet6 (List[dict[str, Any]], Optional):
                    Discovered IPv6 subnet for this IP. Field introduced in 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enabled (bool, Optional):
                Enable, Disable or Graceful Disable determine if new or existing connections to the server are allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * external_orchestration_id (str, Optional):
                UID of server in external orchestration systems. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * external_uuid (str, Optional):
                UUID identifying VM in OpenStack and other external compute. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * hostname (str, Optional):
                DNS resolvable name of the server.  May be used in place of the IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ip (dict[str, Any]):
                ip

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * location (dict[str, Any], Optional):
                location

                * latitude (float, Optional):
                    Latitude of the location. This is represented as degrees.minutes. The range is from -90.0 (south) to +90.0 (north). Allowed values are -90.0-+90.0. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * longitude (float, Optional):
                    Longitude of the location. This is represented as degrees.minutes. The range is from -180.0 (west) to +180.0 (east). Allowed values are -180.0-+180.0. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str, Optional):
                    Location name in the format Country/State/City. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * tag (str, Optional):
                    Location tag string - example  USEast. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mac_address (str, Optional):
                MAC address of server. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * nw_ref (str, Optional):
                (internal-use) This field is used internally by Avi, not editable by the user. It is a reference to an object of type VIMgrNWRuntime. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * port (int, Optional):
                Optionally specify the servers port number.  This will override the pool's default server port attribute. Allowed values are 1-65535. Special values are 0- use backend port in pool. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * preference_order (int, Optional):
                Preference order of this member in the group. The DNS Service chooses the member with the lowest preference that is operationally up. Allowed values are 1-128. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

            * prst_hdr_val (str, Optional):
                Header value for custom header persistence. . Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ratio (int, Optional):
                Ratio of selecting eligible servers in the pool. Allowed values are 1-20. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * resolve_server_by_dns (bool, Optional):
                Auto resolve server's IP using DNS name. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * rewrite_host_header (bool, Optional):
                Rewrite incoming Host Header to server name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * server_node (str, Optional):
                Hostname of the node where the server VM or container resides. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * static (bool, Optional):
                If statically learned. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * verify_network (bool, Optional):
                Verify server belongs to a discovered network or reachable via a discovered network. Verify reachable network isn't the OpenStack management network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vm_ref (str, Optional):
                (internal-use) This field is used internally by Avi, not editable by the user. It is a reference to an object of type VIMgrVMRuntime. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        service_metadata(str, Optional):
            Metadata pertaining to the service provided by this Pool. In Openshift/Kubernetes environments, app metadata info is stored. Any user input to this field will be overwritten by Avi Vantage. Field introduced in 17.2.14,18.1.5,18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        sni_enabled(bool, Optional):
            Enable TLS SNI for server connections. If disabled, Avi will not send the SNI extension as part of the handshake. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        sp_gs_info(dict[str, Any], Optional):
            sp_gs_info. Defaults to None.

            * fqdns (List[str], Optional):
                FQDNs associated with the GSLB service. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * gs_ref (str, Optional):
                GSLB service uuid associated with the site persistence pool. It is a reference to an object of type GslbService. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        ssl_key_and_certificate_ref(str, Optional):
            Service Engines will present a client SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ssl_profile_ref(str, Optional):
            When enabled, Avi re-encrypts traffic to the backend servers. The specific SSL profile defines which ciphers and SSL versions will be supported. It is a reference to an object of type SSLProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        tier1_lr(str, Optional):
            This tier1_lr field should be set same as VirtualService associated for NSX-T. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        use_service_port(bool, Optional):
            Do not translate the client's destination port when sending the connection to the server. Monitor port needs to be specified for health monitors. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic, Enterprise with Cloud Services edition. Defaults to None.

        use_service_ssl_mode(bool, Optional):
            This applies only when use_service_port is set to true. If enabled, SSL mode of the connection to the server is decided by the SSL mode on the Virtualservice service port, on which the request was received. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vrf_ref(str, Optional):
            Virtual Routing Context that the pool is bound to. This is used to provide the isolation of the set of networks the pool is attached to. The pool inherits the Virtual Routing Context of the Virtual Service, and this field is used only internally, and is set by pb-transform. It is a reference to an object of type VrfContext. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              nsx_alb.alb.pool.present:
                - resource_id: value
                - x_avi_version: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.pool.update resource_id=value, x_avi_version=value
    """

    result = dict(comment=[], ret=[], result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "analytics_policy": "analytics_policy",
        "analytics_profile_ref": "analytics_profile_ref",
        "append_port": "append_port",
        "application_persistence_profile_ref": "application_persistence_profile_ref",
        "autoscale_launch_config_ref": "autoscale_launch_config_ref",
        "autoscale_networks": "autoscale_networks",
        "autoscale_policy_ref": "autoscale_policy_ref",
        "capacity_estimation": "capacity_estimation",
        "capacity_estimation_ttfb_thresh": "capacity_estimation_ttfb_thresh",
        "cloud_config_cksum": "cloud_config_cksum",
        "cloud_ref": "cloud_ref",
        "configpb_attributes": "configpb_attributes",
        "conn_pool_properties": "conn_pool_properties",
        "connection_ramp_duration": "connection_ramp_duration",
        "created_by": "created_by",
        "default_server_port": "default_server_port",
        "delete_server_on_dns_refresh": "delete_server_on_dns_refresh",
        "description": "description",
        "domain_name": "domain_name",
        "east_west": "east_west",
        "enable_http2": "enable_http2",
        "enabled": "enabled",
        "external_autoscale_groups": "external_autoscale_groups",
        "fail_action": "fail_action",
        "fewest_tasks_feedback_delay": "fewest_tasks_feedback_delay",
        "graceful_disable_timeout": "graceful_disable_timeout",
        "gslb_sp_enabled": "gslb_sp_enabled",
        "health_monitor_refs": "health_monitor_refs",
        "horizon_profile": "horizon_profile",
        "host_check_enabled": "host_check_enabled",
        "http2_properties": "http2_properties",
        "ignore_server_port": "ignore_server_port",
        "inline_health_monitor": "inline_health_monitor",
        "ipaddrgroup_ref": "ipaddrgroup_ref",
        "lb_algo_rr_per_se": "lb_algo_rr_per_se",
        "lb_algorithm": "lb_algorithm",
        "lb_algorithm_consistent_hash_hdr": "lb_algorithm_consistent_hash_hdr",
        "lb_algorithm_core_nonaffinity": "lb_algorithm_core_nonaffinity",
        "lb_algorithm_hash": "lb_algorithm_hash",
        "lookup_server_by_name": "lookup_server_by_name",
        "markers": "markers",
        "max_concurrent_connections_per_server": "max_concurrent_connections_per_server",
        "max_conn_rate_per_server": "max_conn_rate_per_server",
        "min_health_monitors_up": "min_health_monitors_up",
        "min_servers_up": "min_servers_up",
        "name": "name",
        "networks": "networks",
        "nsx_securitygroup": "nsx_securitygroup",
        "pki_profile_ref": "pki_profile_ref",
        "placement_networks": "placement_networks",
        "pool_type": "pool_type",
        "request_queue_depth": "request_queue_depth",
        "request_queue_enabled": "request_queue_enabled",
        "resolve_pool_by_dns": "resolve_pool_by_dns",
        "rewrite_host_header_to_server_name": "rewrite_host_header_to_server_name",
        "rewrite_host_header_to_sni": "rewrite_host_header_to_sni",
        "routing_pool": "routing_pool",
        "server_disable_type": "server_disable_type",
        "server_name": "server_name",
        "server_reselect": "server_reselect",
        "server_timeout": "server_timeout",
        "servers": "servers",
        "service_metadata": "service_metadata",
        "sni_enabled": "sni_enabled",
        "sp_gs_info": "sp_gs_info",
        "ssl_key_and_certificate_ref": "ssl_key_and_certificate_ref",
        "ssl_profile_ref": "ssl_profile_ref",
        "tenant_ref": "tenant_ref",
        "tier1_lr": "tier1_lr",
        "use_service_port": "use_service_port",
        "use_service_ssl_mode": "use_service_ssl_mode",
        "vrf_ref": "vrf_ref",
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
            path="/pool/{uuid}".format(**{"uuid": resource_id}),
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
            f"Updated nsx_alb.alb.pool '{name}'",
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
            Alb.pool unique ID.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              nsx_alb.alb.pool.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.pool.delete resource_id=value
    """

    result = dict(comment=[], ret=[], result=True)

    before = await hub.exec.nsx_alb.alb.pool.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )
    if before["ret"]:
        tenant_name = before["ret"]["tenant_ref"].split("#")[-1]
    delete = await hub.tool.nsx_alb.session.request(
        ctx,
        method="delete",
        path="/pool/{uuid}".format(**{"uuid": resource_id}),
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
