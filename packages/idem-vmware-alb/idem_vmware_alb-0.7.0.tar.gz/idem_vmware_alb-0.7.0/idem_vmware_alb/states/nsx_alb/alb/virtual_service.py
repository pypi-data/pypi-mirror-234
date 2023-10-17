"""States module for managing Alb Virtual Services. """
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
    resource_id: str = None,
    active_standby_se_tag: str = None,
    advertise_down_vs: bool = None,
    allow_invalid_client_cert: bool = None,
    analytics_policy: make_dataclass(
        "analytics_policy",
        [
            ("all_headers", bool, field(default=None)),
            ("client_insights", str, field(default=None)),
            (
                "client_insights_sampling",
                make_dataclass(
                    "client_insights_sampling",
                    [
                        (
                            "client_ip",
                            make_dataclass(
                                "client_ip",
                                [
                                    ("match_criteria", str),
                                    (
                                        "addrs",
                                        List[
                                            make_dataclass(
                                                "addrs", [("addr", str), ("type", str)]
                                            )
                                        ],
                                        field(default=None),
                                    ),
                                    ("group_refs", List[str], field(default=None)),
                                    (
                                        "prefixes",
                                        List[
                                            make_dataclass(
                                                "prefixes",
                                                [
                                                    (
                                                        "ip_addr",
                                                        make_dataclass(
                                                            "ip_addr",
                                                            [
                                                                ("addr", str),
                                                                ("type", str),
                                                            ],
                                                        ),
                                                    ),
                                                    ("mask", int),
                                                ],
                                            )
                                        ],
                                        field(default=None),
                                    ),
                                    (
                                        "ranges",
                                        List[
                                            make_dataclass(
                                                "ranges",
                                                [
                                                    (
                                                        "begin",
                                                        make_dataclass(
                                                            "begin",
                                                            [
                                                                ("addr", str),
                                                                ("type", str),
                                                            ],
                                                        ),
                                                    ),
                                                    (
                                                        "end",
                                                        make_dataclass(
                                                            "end",
                                                            [
                                                                ("addr", str),
                                                                ("type", str),
                                                            ],
                                                        ),
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
                        (
                            "sample_uris",
                            make_dataclass(
                                "sample_uris",
                                [
                                    ("match_criteria", str),
                                    ("match_str", List[str], field(default=None)),
                                    (
                                        "string_group_refs",
                                        List[str],
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "skip_uris",
                            make_dataclass(
                                "skip_uris",
                                [
                                    ("match_criteria", str),
                                    ("match_str", List[str], field(default=None)),
                                    (
                                        "string_group_refs",
                                        List[str],
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
            (
                "client_log_filters",
                List[
                    make_dataclass(
                        "client_log_filters",
                        [
                            ("enabled", bool),
                            ("index", int),
                            ("name", str),
                            ("all_headers", bool, field(default=None)),
                            (
                                "client_ip",
                                make_dataclass(
                                    "client_ip",
                                    [
                                        ("match_criteria", str),
                                        (
                                            "addrs",
                                            List[
                                                make_dataclass(
                                                    "addrs",
                                                    [("addr", str), ("type", str)],
                                                )
                                            ],
                                            field(default=None),
                                        ),
                                        ("group_refs", List[str], field(default=None)),
                                        (
                                            "prefixes",
                                            List[
                                                make_dataclass(
                                                    "prefixes",
                                                    [
                                                        (
                                                            "ip_addr",
                                                            make_dataclass(
                                                                "ip_addr",
                                                                [
                                                                    ("addr", str),
                                                                    ("type", str),
                                                                ],
                                                            ),
                                                        ),
                                                        ("mask", int),
                                                    ],
                                                )
                                            ],
                                            field(default=None),
                                        ),
                                        (
                                            "ranges",
                                            List[
                                                make_dataclass(
                                                    "ranges",
                                                    [
                                                        (
                                                            "begin",
                                                            make_dataclass(
                                                                "begin",
                                                                [
                                                                    ("addr", str),
                                                                    ("type", str),
                                                                ],
                                                            ),
                                                        ),
                                                        (
                                                            "end",
                                                            make_dataclass(
                                                                "end",
                                                                [
                                                                    ("addr", str),
                                                                    ("type", str),
                                                                ],
                                                            ),
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
                            ("duration", int, field(default=None)),
                            (
                                "uri",
                                make_dataclass(
                                    "uri",
                                    [
                                        ("match_criteria", str),
                                        ("match_str", List[str], field(default=None)),
                                        (
                                            "string_group_refs",
                                            List[str],
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                        ],
                    )
                ],
                field(default=None),
            ),
            (
                "full_client_logs",
                make_dataclass(
                    "full_client_logs",
                    [
                        ("enabled", bool),
                        ("duration", int, field(default=None)),
                        ("throttle", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "learning_log_policy",
                make_dataclass(
                    "learning_log_policy",
                    [
                        ("enabled", bool, field(default=None)),
                        ("host", str, field(default=None)),
                        ("port", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "metrics_realtime_update",
                make_dataclass(
                    "metrics_realtime_update",
                    [("enabled", bool), ("duration", int, field(default=None))],
                ),
                field(default=None),
            ),
            ("significant_log_throttle", int, field(default=None)),
            ("udf_log_throttle", int, field(default=None)),
        ],
    ) = None,
    analytics_profile_ref: str = None,
    application_profile_ref: str = None,
    azure_availability_set: str = None,
    bgp_peer_labels: List[str] = None,
    bot_policy_ref: str = None,
    bulk_sync_kvcache: bool = None,
    close_client_conn_on_config_update: bool = None,
    cloud_config_cksum: str = None,
    cloud_ref: str = None,
    cloud_type: str = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    connections_rate_limit: make_dataclass(
        "connections_rate_limit",
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
    content_rewrite: make_dataclass(
        "content_rewrite",
        [
            ("rewritable_content_ref", str, field(default=None)),
            (
                "rsp_rewrite_rules",
                List[
                    make_dataclass(
                        "rsp_rewrite_rules",
                        [
                            ("enable", bool, field(default=None)),
                            ("index", int, field(default=None)),
                            ("name", str, field(default=None)),
                            (
                                "pairs",
                                List[
                                    make_dataclass(
                                        "pairs",
                                        [
                                            (
                                                "search_string",
                                                make_dataclass(
                                                    "search_string",
                                                    [
                                                        ("val", str),
                                                        (
                                                            "type",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                            ),
                                            (
                                                "replacement_string",
                                                make_dataclass(
                                                    "replacement_string",
                                                    [
                                                        (
                                                            "type",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "val",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
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
        ],
    ) = None,
    created_by: str = None,
    delay_fairness: bool = None,
    description: str = None,
    dns_info: List[
        make_dataclass(
            "dns_info",
            [
                ("algorithm", str, field(default=None)),
                (
                    "cname",
                    make_dataclass("cname", [("cname", str)]),
                    field(default=None),
                ),
                ("fqdn", str, field(default=None)),
                ("metadata", str, field(default=None)),
                ("num_records_in_response", int, field(default=None)),
                ("ttl", int, field(default=None)),
                ("type", str, field(default=None)),
            ],
        )
    ] = None,
    dns_policies: List[
        make_dataclass("dns_policies", [("dns_policy_ref", str), ("index", int)])
    ] = None,
    east_west_placement: bool = None,
    enable_autogw: bool = None,
    enable_rhi: bool = None,
    enable_rhi_snat: bool = None,
    enabled: bool = None,
    error_page_profile_ref: str = None,
    flow_dist: str = None,
    flow_label_type: str = None,
    fqdn: str = None,
    host_name_xlate: str = None,
    http_policies: List[
        make_dataclass("http_policies", [("http_policy_set_ref", str), ("index", int)])
    ] = None,
    icap_request_profile_refs: List[str] = None,
    ign_pool_net_reach: bool = None,
    jwt_config: make_dataclass(
        "jwt_config",
        [
            ("audience", str),
            ("jwt_location", str),
            ("jwt_name", str, field(default=None)),
        ],
    ) = None,
    l4_policies: List[
        make_dataclass("l4_policies", [("index", int), ("l4_policy_set_ref", str)])
    ] = None,
    ldap_vs_config: make_dataclass(
        "ldap_vs_config",
        [
            ("realm", str, field(default=None)),
            ("se_auth_ldap_bind_timeout", int, field(default=None)),
            ("se_auth_ldap_cache_size", int, field(default=None)),
            ("se_auth_ldap_connect_timeout", int, field(default=None)),
            ("se_auth_ldap_conns_per_server", int, field(default=None)),
            ("se_auth_ldap_reconnect_timeout", int, field(default=None)),
            ("se_auth_ldap_request_timeout", int, field(default=None)),
            ("se_auth_ldap_servers_failover_only", bool, field(default=None)),
        ],
    ) = None,
    limit_doser: bool = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    max_cps_per_client: int = None,
    microservice_ref: str = None,
    min_pools_up: int = None,
    network_profile_ref: str = None,
    network_security_policy_ref: str = None,
    nsx_securitygroup: List[str] = None,
    oauth_vs_config: make_dataclass(
        "oauth_vs_config",
        [
            ("cookie_name", str, field(default=None)),
            ("cookie_timeout", int, field(default=None)),
            (
                "key",
                List[
                    make_dataclass(
                        "key",
                        [
                            ("aes_key", str, field(default=None)),
                            ("hmac_key", str, field(default=None)),
                            ("name", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("logout_uri", str, field(default=None)),
            (
                "oauth_settings",
                List[
                    make_dataclass(
                        "oauth_settings",
                        [
                            ("auth_profile_ref", str),
                            (
                                "app_settings",
                                make_dataclass(
                                    "app_settings",
                                    [
                                        ("client_id", str),
                                        ("client_secret", str),
                                        (
                                            "oidc_config",
                                            make_dataclass(
                                                "oidc_config",
                                                [
                                                    (
                                                        "oidc_enable",
                                                        bool,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "profile",
                                                        bool,
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "userinfo",
                                                        bool,
                                                        field(default=None),
                                                    ),
                                                ],
                                            ),
                                            field(default=None),
                                        ),
                                        ("scopes", List[str], field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "resource_server",
                                make_dataclass(
                                    "resource_server",
                                    [
                                        ("access_type", str),
                                        (
                                            "introspection_data_timeout",
                                            int,
                                            field(default=None),
                                        ),
                                        (
                                            "jwt_params",
                                            make_dataclass(
                                                "jwt_params", [("audience", str)]
                                            ),
                                            field(default=None),
                                        ),
                                        (
                                            "opaque_token_params",
                                            make_dataclass(
                                                "opaque_token_params",
                                                [
                                                    ("server_id", str),
                                                    ("server_secret", str),
                                                ],
                                            ),
                                            field(default=None),
                                        ),
                                    ],
                                ),
                                field(default=None),
                            ),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("post_logout_redirect_uri", str, field(default=None)),
            ("redirect_uri", str, field(default=None)),
        ],
    ) = None,
    performance_limits: make_dataclass(
        "performance_limits",
        [
            ("max_concurrent_connections", int, field(default=None)),
            ("max_throughput", int, field(default=None)),
        ],
    ) = None,
    pool_group_ref: str = None,
    pool_ref: str = None,
    remove_listening_port_on_vs_down: bool = None,
    requests_rate_limit: make_dataclass(
        "requests_rate_limit",
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
    saml_sp_config: make_dataclass(
        "saml_sp_config",
        [
            ("authn_req_acs_type", str),
            ("entity_id", str),
            ("single_signon_url", str),
            ("acs_index", int, field(default=None)),
            ("cookie_name", str, field(default=None)),
            ("cookie_timeout", int, field(default=None)),
            (
                "key",
                List[
                    make_dataclass(
                        "key",
                        [
                            ("aes_key", str, field(default=None)),
                            ("hmac_key", str, field(default=None)),
                            ("name", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("signing_ssl_key_and_certificate_ref", str, field(default=None)),
            ("sp_metadata", str, field(default=None)),
            ("use_idp_session_timeout", bool, field(default=None)),
        ],
    ) = None,
    scaleout_ecmp: bool = None,
    se_group_ref: str = None,
    security_policy_ref: str = None,
    server_network_profile_ref: str = None,
    service_metadata: str = None,
    service_pool_select: List[
        make_dataclass(
            "service_pool_select",
            [
                ("service_port", int),
                ("service_pool_group_ref", str, field(default=None)),
                ("service_pool_ref", str, field(default=None)),
                ("service_port_range_end", int, field(default=None)),
                ("service_protocol", str, field(default=None)),
            ],
        )
    ] = None,
    services: List[
        make_dataclass(
            "services",
            [
                ("port", int),
                ("enable_http2", bool, field(default=None)),
                ("enable_ssl", bool, field(default=None)),
                ("horizon_internal_ports", bool, field(default=None)),
                ("is_active_ftp_data_port", bool, field(default=None)),
                ("override_application_profile_ref", str, field(default=None)),
                ("override_network_profile_ref", str, field(default=None)),
                ("port_range_end", int, field(default=None)),
            ],
        )
    ] = None,
    sideband_profile: make_dataclass(
        "sideband_profile",
        [
            (
                "ip",
                List[make_dataclass("ip", [("addr", str), ("type", str)])],
                field(default=None),
            ),
            ("sideband_max_request_body_size", int, field(default=None)),
        ],
    ) = None,
    snat_ip: List[make_dataclass("snat_ip", [("addr", str), ("type", str)])] = None,
    sp_pool_refs: List[str] = None,
    ssl_key_and_certificate_refs: List[str] = None,
    ssl_profile_ref: str = None,
    ssl_profile_selectors: List[
        make_dataclass(
            "ssl_profile_selectors",
            [
                (
                    "client_ip_list",
                    make_dataclass(
                        "client_ip_list",
                        [
                            ("match_criteria", str),
                            (
                                "addrs",
                                List[
                                    make_dataclass(
                                        "addrs", [("addr", str), ("type", str)]
                                    )
                                ],
                                field(default=None),
                            ),
                            ("group_refs", List[str], field(default=None)),
                            (
                                "prefixes",
                                List[
                                    make_dataclass(
                                        "prefixes",
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
                                "ranges",
                                List[
                                    make_dataclass(
                                        "ranges",
                                        [
                                            (
                                                "begin",
                                                make_dataclass(
                                                    "begin",
                                                    [("addr", str), ("type", str)],
                                                ),
                                            ),
                                            (
                                                "end",
                                                make_dataclass(
                                                    "end",
                                                    [("addr", str), ("type", str)],
                                                ),
                                            ),
                                        ],
                                    )
                                ],
                                field(default=None),
                            ),
                        ],
                    ),
                ),
                ("ssl_profile_ref", str),
            ],
        )
    ] = None,
    ssl_sess_cache_avg_size: int = None,
    sso_policy_ref: str = None,
    static_dns_records: List[
        make_dataclass(
            "static_dns_records",
            [
                ("type", str),
                ("algorithm", str, field(default=None)),
                (
                    "cname",
                    make_dataclass("cname", [("cname", str)]),
                    field(default=None),
                ),
                ("delegated", bool, field(default=None)),
                ("description", str, field(default=None)),
                ("fqdn", List[str], field(default=None)),
                (
                    "ip6_address",
                    List[
                        make_dataclass(
                            "ip6_address",
                            [
                                (
                                    "ip6_address",
                                    make_dataclass(
                                        "ip6_address", [("addr", str), ("type", str)]
                                    ),
                                )
                            ],
                        )
                    ],
                    field(default=None),
                ),
                (
                    "ip_address",
                    List[
                        make_dataclass(
                            "ip_address",
                            [
                                (
                                    "ip_address",
                                    make_dataclass(
                                        "ip_address", [("addr", str), ("type", str)]
                                    ),
                                )
                            ],
                        )
                    ],
                    field(default=None),
                ),
                ("metadata", str, field(default=None)),
                (
                    "mx_records",
                    List[
                        make_dataclass("mx_records", [("host", str), ("priority", int)])
                    ],
                    field(default=None),
                ),
                (
                    "ns",
                    List[
                        make_dataclass(
                            "ns",
                            [
                                ("nsname", str),
                                (
                                    "ip6_address",
                                    make_dataclass(
                                        "ip6_address", [("addr", str), ("type", str)]
                                    ),
                                    field(default=None),
                                ),
                                (
                                    "ip_address",
                                    make_dataclass(
                                        "ip_address", [("addr", str), ("type", str)]
                                    ),
                                    field(default=None),
                                ),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                ("num_records_in_response", int, field(default=None)),
                (
                    "service_locator",
                    List[
                        make_dataclass(
                            "service_locator",
                            [
                                ("port", int),
                                ("priority", int, field(default=None)),
                                ("target", str, field(default=None)),
                                ("weight", int, field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                ("ttl", int, field(default=None)),
                (
                    "txt_records",
                    List[make_dataclass("txt_records", [("text_str", str)])],
                    field(default=None),
                ),
                ("wildcard_match", bool, field(default=None)),
            ],
        )
    ] = None,
    tenant_ref: str = None,
    test_se_datastore_level_1_ref: str = None,
    topology_policies: List[
        make_dataclass("topology_policies", [("dns_policy_ref", str), ("index", int)])
    ] = None,
    traffic_clone_profile_ref: str = None,
    traffic_enabled: bool = None,
    type: str = None,
    use_bridge_ip_as_vip: bool = None,
    use_vip_as_snat: bool = None,
    vh_domain_name: List[str] = None,
    vh_matches: List[
        make_dataclass(
            "vh_matches",
            [
                ("host", str),
                (
                    "path",
                    List[
                        make_dataclass(
                            "path",
                            [
                                ("match_criteria", str),
                                ("match_case", str, field(default=None)),
                                ("match_decoded_string", bool, field(default=None)),
                                ("match_str", List[str], field(default=None)),
                                ("string_group_refs", List[str], field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                (
                    "rules",
                    List[
                        make_dataclass(
                            "rules",
                            [
                                (
                                    "matches",
                                    make_dataclass(
                                        "matches",
                                        [
                                            (
                                                "bot_detection_result",
                                                make_dataclass(
                                                    "bot_detection_result",
                                                    [
                                                        ("match_operation", str),
                                                        (
                                                            "classifications",
                                                            List[
                                                                make_dataclass(
                                                                    "classifications",
                                                                    [
                                                                        ("type", str),
                                                                        (
                                                                            "user_defined_type",
                                                                            str,
                                                                            field(
                                                                                default=None
                                                                            ),
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
                                            (
                                                "client_ip",
                                                make_dataclass(
                                                    "client_ip",
                                                    [
                                                        ("match_criteria", str),
                                                        (
                                                            "addrs",
                                                            List[
                                                                make_dataclass(
                                                                    "addrs",
                                                                    [
                                                                        ("addr", str),
                                                                        ("type", str),
                                                                    ],
                                                                )
                                                            ],
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "group_refs",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "prefixes",
                                                            List[
                                                                make_dataclass(
                                                                    "prefixes",
                                                                    [
                                                                        (
                                                                            "ip_addr",
                                                                            make_dataclass(
                                                                                "ip_addr",
                                                                                [
                                                                                    (
                                                                                        "addr",
                                                                                        str,
                                                                                    ),
                                                                                    (
                                                                                        "type",
                                                                                        str,
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ),
                                                                        ("mask", int),
                                                                    ],
                                                                )
                                                            ],
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "ranges",
                                                            List[
                                                                make_dataclass(
                                                                    "ranges",
                                                                    [
                                                                        (
                                                                            "begin",
                                                                            make_dataclass(
                                                                                "begin",
                                                                                [
                                                                                    (
                                                                                        "addr",
                                                                                        str,
                                                                                    ),
                                                                                    (
                                                                                        "type",
                                                                                        str,
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "end",
                                                                            make_dataclass(
                                                                                "end",
                                                                                [
                                                                                    (
                                                                                        "addr",
                                                                                        str,
                                                                                    ),
                                                                                    (
                                                                                        "type",
                                                                                        str,
                                                                                    ),
                                                                                ],
                                                                            ),
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
                                            (
                                                "cookie",
                                                make_dataclass(
                                                    "cookie",
                                                    [
                                                        ("match_criteria", str),
                                                        ("name", str),
                                                        (
                                                            "match_case",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "value",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                            (
                                                "geo_matches",
                                                List[
                                                    make_dataclass(
                                                        "geo_matches",
                                                        [
                                                            ("attribute", str),
                                                            ("match_operation", str),
                                                            ("values", List[str]),
                                                        ],
                                                    )
                                                ],
                                                field(default=None),
                                            ),
                                            (
                                                "hdrs",
                                                List[
                                                    make_dataclass(
                                                        "hdrs",
                                                        [
                                                            ("hdr", str),
                                                            ("match_criteria", str),
                                                            (
                                                                "match_case",
                                                                str,
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "value",
                                                                List[str],
                                                                field(default=None),
                                                            ),
                                                        ],
                                                    )
                                                ],
                                                field(default=None),
                                            ),
                                            (
                                                "host_hdr",
                                                make_dataclass(
                                                    "host_hdr",
                                                    [
                                                        ("match_criteria", str),
                                                        (
                                                            "match_case",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "value",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                            (
                                                "ip_reputation_type",
                                                make_dataclass(
                                                    "ip_reputation_type",
                                                    [
                                                        ("match_operation", str),
                                                        (
                                                            "reputation_types",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                            (
                                                "method",
                                                make_dataclass(
                                                    "method",
                                                    [
                                                        ("match_criteria", str),
                                                        (
                                                            "methods",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                            (
                                                "path",
                                                make_dataclass(
                                                    "path",
                                                    [
                                                        ("match_criteria", str),
                                                        (
                                                            "match_case",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "match_decoded_string",
                                                            bool,
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "match_str",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "string_group_refs",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                            (
                                                "protocol",
                                                make_dataclass(
                                                    "protocol",
                                                    [
                                                        ("match_criteria", str),
                                                        ("protocols", str),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                            (
                                                "query",
                                                make_dataclass(
                                                    "query",
                                                    [
                                                        ("match_criteria", str),
                                                        (
                                                            "match_case",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "match_decoded_string",
                                                            bool,
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "match_str",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "string_group_refs",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                            (
                                                "source_ip",
                                                make_dataclass(
                                                    "source_ip",
                                                    [
                                                        ("match_criteria", str),
                                                        (
                                                            "addrs",
                                                            List[
                                                                make_dataclass(
                                                                    "addrs",
                                                                    [
                                                                        ("addr", str),
                                                                        ("type", str),
                                                                    ],
                                                                )
                                                            ],
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "group_refs",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "prefixes",
                                                            List[
                                                                make_dataclass(
                                                                    "prefixes",
                                                                    [
                                                                        (
                                                                            "ip_addr",
                                                                            make_dataclass(
                                                                                "ip_addr",
                                                                                [
                                                                                    (
                                                                                        "addr",
                                                                                        str,
                                                                                    ),
                                                                                    (
                                                                                        "type",
                                                                                        str,
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ),
                                                                        ("mask", int),
                                                                    ],
                                                                )
                                                            ],
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "ranges",
                                                            List[
                                                                make_dataclass(
                                                                    "ranges",
                                                                    [
                                                                        (
                                                                            "begin",
                                                                            make_dataclass(
                                                                                "begin",
                                                                                [
                                                                                    (
                                                                                        "addr",
                                                                                        str,
                                                                                    ),
                                                                                    (
                                                                                        "type",
                                                                                        str,
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ),
                                                                        (
                                                                            "end",
                                                                            make_dataclass(
                                                                                "end",
                                                                                [
                                                                                    (
                                                                                        "addr",
                                                                                        str,
                                                                                    ),
                                                                                    (
                                                                                        "type",
                                                                                        str,
                                                                                    ),
                                                                                ],
                                                                            ),
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
                                            (
                                                "tls_fingerprint_match",
                                                make_dataclass(
                                                    "tls_fingerprint_match",
                                                    [
                                                        ("match_operation", str),
                                                        (
                                                            "fingerprints",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "string_group_refs",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                            (
                                                "version",
                                                make_dataclass(
                                                    "version",
                                                    [
                                                        ("match_criteria", str),
                                                        (
                                                            "versions",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                            (
                                                "vs_port",
                                                make_dataclass(
                                                    "vs_port",
                                                    [
                                                        ("match_criteria", str),
                                                        (
                                                            "ports",
                                                            List[int],
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                        ],
                                    ),
                                ),
                                ("name", str),
                            ],
                        )
                    ],
                    field(default=None),
                ),
            ],
        )
    ] = None,
    vh_parent_vs_ref: str = None,
    vh_type: str = None,
    vip: List[
        make_dataclass(
            "vip",
            [
                ("vip_id", str),
                ("auto_allocate_floating_ip", bool, field(default=None)),
                ("auto_allocate_ip", bool, field(default=None)),
                ("auto_allocate_ip_type", str, field(default=None)),
                ("availability_zone", str, field(default=None)),
                ("avi_allocated_fip", bool, field(default=None)),
                ("avi_allocated_vip", bool, field(default=None)),
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
                (
                    "floating_ip",
                    make_dataclass("floating_ip", [("addr", str), ("type", str)]),
                    field(default=None),
                ),
                (
                    "floating_ip6",
                    make_dataclass("floating_ip6", [("addr", str), ("type", str)]),
                    field(default=None),
                ),
                ("floating_subnet6_uuid", str, field(default=None)),
                ("floating_subnet_uuid", str, field(default=None)),
                (
                    "ip6_address",
                    make_dataclass("ip6_address", [("addr", str), ("type", str)]),
                    field(default=None),
                ),
                (
                    "ip_address",
                    make_dataclass("ip_address", [("addr", str), ("type", str)]),
                    field(default=None),
                ),
                (
                    "ipam_network_subnet",
                    make_dataclass(
                        "ipam_network_subnet",
                        [
                            ("network_ref", str, field(default=None)),
                            (
                                "subnet",
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
                                ),
                                field(default=None),
                            ),
                            (
                                "subnet6",
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
                                ),
                                field(default=None),
                            ),
                            ("subnet6_uuid", str, field(default=None)),
                            ("subnet_uuid", str, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                ("network_ref", str, field(default=None)),
                (
                    "placement_networks",
                    List[
                        make_dataclass(
                            "placement_networks",
                            [
                                ("network_ref", str, field(default=None)),
                                (
                                    "subnet",
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
                                    ),
                                    field(default=None),
                                ),
                                (
                                    "subnet6",
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
                                    ),
                                    field(default=None),
                                ),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                ("port_uuid", str, field(default=None)),
                ("prefix_length", int, field(default=None)),
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
                    field(default=None),
                ),
                (
                    "subnet6",
                    make_dataclass(
                        "subnet6",
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
                    field(default=None),
                ),
                ("subnet6_uuid", str, field(default=None)),
                ("subnet_uuid", str, field(default=None)),
            ],
        )
    ] = None,
    vrf_context_ref: str = None,
    vs_datascripts: List[
        make_dataclass(
            "vs_datascripts", [("index", int), ("vs_datascript_set_ref", str)]
        )
    ] = None,
    vsvip_cloud_config_cksum: str = None,
    vsvip_ref: str = None,
    waf_policy_ref: str = None,
    weight: int = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:
        name(str):
            Idem name of the resource.

        resource_id(str, Optional):
            Alb.virtual_service unique ID. Defaults to None.

        active_standby_se_tag(str, Optional):
            This configuration only applies if the VirtualService is in Legacy Active Standby HA mode and Load Distribution among Active Standby is enabled. This field is used to tag the VirtualService so that VirtualServices with the same tag will share the same Active ServiceEngine. VirtualServices with different tags will have different Active ServiceEngines. If one of the ServiceEngine's in the ServiceEngineGroup fails, all VirtualServices will end up using the same Active ServiceEngine. Redistribution of the VirtualServices can be either manual or automated when the failed ServiceEngine recovers. Redistribution is based on the auto redistribute property of the ServiceEngineGroup. Enum options - ACTIVE_STANDBY_SE_1, ACTIVE_STANDBY_SE_2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        advertise_down_vs(bool, Optional):
            Keep advertising Virtual Service via BGP even if it is marked down by health monitor. This setting takes effect for future Virtual Service flaps. To advertise current VSes that are down, please disable and re-enable the Virtual Service. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        allow_invalid_client_cert(bool, Optional):
            Process request even if invalid client certificate is presented. Datascript APIs need to be used for processing of such requests. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        analytics_policy(dict[str, Any], Optional):
            analytics_policy. Defaults to None.

            * all_headers (bool, Optional):
                Log all headers. Field introduced in 18.1.4, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * client_insights (str, Optional):
                Gain insights from sampled client to server HTTP requests and responses. Enum options - NO_INSIGHTS, PASSIVE, ACTIVE. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * client_insights_sampling (dict[str, Any], Optional):
                client_insights_sampling

                * client_ip (dict[str, Any], Optional):
                    client_ip

                    * addrs (List[dict[str, Any]], Optional):
                        IP address(es). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * group_refs (List[str], Optional):
                        UUID of IP address group(s). It is a reference to an object of type IpAddrGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * match_criteria (str):
                        Criterion to use for IP address matching the HTTP request. Enum options - IS_IN, IS_NOT_IN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * prefixes (List[dict[str, Any]], Optional):
                        IP address prefix(es). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * ip_addr (dict[str, Any]):
                            ip_addr

                            * addr (str):
                                IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                 Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * mask (int):
                             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * ranges (List[dict[str, Any]], Optional):
                        IP address range(s). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * begin (dict[str, Any]):
                            begin

                            * addr (str):
                                IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                 Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * end (dict[str, Any]):
                            end

                            * addr (str):
                                IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                 Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * sample_uris (dict[str, Any], Optional):
                    sample_uris

                    * match_criteria (str):
                        Criterion to use for string matching the HTTP request. Enum options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- BEGINS_WITH,DOES_NOT_BEGIN_WITH,CONTAINS,DOES_NOT_CONTAIN,ENDS_WITH,DOES_NOT_END_WITH,EQUALS,DOES_NOT_EQUAL), Basic edition(Allowed values- BEGINS_WITH,DOES_NOT_BEGIN_WITH,CONTAINS,DOES_NOT_CONTAIN,ENDS_WITH,DOES_NOT_END_WITH,EQUALS,DOES_NOT_EQUAL), Enterprise with Cloud Services edition.

                    * match_str (List[str], Optional):
                        String value(s). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * string_group_refs (List[str], Optional):
                        UUID of the string group(s). It is a reference to an object of type StringGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * skip_uris (dict[str, Any], Optional):
                    skip_uris

                    * match_criteria (str):
                        Criterion to use for string matching the HTTP request. Enum options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- BEGINS_WITH,DOES_NOT_BEGIN_WITH,CONTAINS,DOES_NOT_CONTAIN,ENDS_WITH,DOES_NOT_END_WITH,EQUALS,DOES_NOT_EQUAL), Basic edition(Allowed values- BEGINS_WITH,DOES_NOT_BEGIN_WITH,CONTAINS,DOES_NOT_CONTAIN,ENDS_WITH,DOES_NOT_END_WITH,EQUALS,DOES_NOT_EQUAL), Enterprise with Cloud Services edition.

                    * match_str (List[str], Optional):
                        String value(s). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * string_group_refs (List[str], Optional):
                        UUID of the string group(s). It is a reference to an object of type StringGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * client_log_filters (List[dict[str, Any]], Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * all_headers (bool, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * client_ip (dict[str, Any], Optional):
                    client_ip

                    * addrs (List[dict[str, Any]], Optional):
                        IP address(es). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * group_refs (List[str], Optional):
                        UUID of IP address group(s). It is a reference to an object of type IpAddrGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * match_criteria (str):
                        Criterion to use for IP address matching the HTTP request. Enum options - IS_IN, IS_NOT_IN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * prefixes (List[dict[str, Any]], Optional):
                        IP address prefix(es). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * ip_addr (dict[str, Any]):
                            ip_addr

                            * addr (str):
                                IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                 Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * mask (int):
                             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * ranges (List[dict[str, Any]], Optional):
                        IP address range(s). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * begin (dict[str, Any]):
                            begin

                            * addr (str):
                                IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                 Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * end (dict[str, Any]):
                            end

                            * addr (str):
                                IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                 Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * duration (int, Optional):
                     Special values are 0 - infinite. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * enabled (bool):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * index (int):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * uri (dict[str, Any], Optional):
                    uri

                    * match_criteria (str):
                        Criterion to use for string matching the HTTP request. Enum options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- BEGINS_WITH,DOES_NOT_BEGIN_WITH,CONTAINS,DOES_NOT_CONTAIN,ENDS_WITH,DOES_NOT_END_WITH,EQUALS,DOES_NOT_EQUAL), Basic edition(Allowed values- BEGINS_WITH,DOES_NOT_BEGIN_WITH,CONTAINS,DOES_NOT_CONTAIN,ENDS_WITH,DOES_NOT_END_WITH,EQUALS,DOES_NOT_EQUAL), Enterprise with Cloud Services edition.

                    * match_str (List[str], Optional):
                        String value(s). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * string_group_refs (List[str], Optional):
                        UUID of the string group(s). It is a reference to an object of type StringGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * full_client_logs (dict[str, Any], Optional):
                full_client_logs

                * duration (int, Optional):
                    How long should the system capture all logs, measured in minutes. Set to 0 for infinite. Special values are 0 - infinite. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * enabled (bool):
                    Capture all client logs including connections and requests.  When deactivated, only errors will be logged. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Special default for Essentials edition is false, Basic edition is false, Enterprise is False.

                * throttle (int, Optional):
                    This setting limits the number of non-significant logs generated per second for this VS on each SE. Default is 10 logs per second. Set it to zero (0) to deactivate throttling. Field introduced in 17.1.3. Unit is PER_SECOND. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * learning_log_policy (dict[str, Any], Optional):
                learning_log_policy

                * enabled (bool, Optional):
                    Determine whether app learning logging is enabled. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * host (str, Optional):
                    Host name where learning logs will be sent to. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * port (int, Optional):
                    Port number for the service listening for learning logs. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * metrics_realtime_update (dict[str, Any], Optional):
                metrics_realtime_update

                * duration (int, Optional):
                    Real time metrics collection duration in minutes. 0 for infinite. Special values are 0 - infinite. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * enabled (bool):
                    Enables real time metrics collection.  When deactivated, 6 hour view is the most granular the system will track. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * significant_log_throttle (int, Optional):
                This setting limits the number of significant logs generated per second for this VS on each SE. Default is 10 logs per second. Set it to zero (0) to deactivate throttling. Field introduced in 17.1.3. Unit is PER_SECOND. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * udf_log_throttle (int, Optional):
                This setting limits the total number of UDF logs generated per second for this VS on each SE. UDF logs are generated due to the configured client log filters or the rules with logging enabled. Default is 10 logs per second. Set it to zero (0) to deactivate throttling. Field introduced in 17.1.3. Unit is PER_SECOND. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        analytics_profile_ref(str, Optional):
            Specifies settings related to analytics. It is a reference to an object of type AnalyticsProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        application_profile_ref(str, Optional):
            Enable application layer specific features for the Virtual Service. It is a reference to an object of type ApplicationProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Special default for Essentials edition is System-L4-Application. Defaults to None.

        azure_availability_set(str, Optional):
            (internal-use)Applicable for Azure only. Azure Availability set to which this VS is associated. Internally set by the cloud connector. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        bgp_peer_labels(List[str], Optional):
            Select BGP peers, using peer label, for VsVip advertisement. Field introduced in 20.1.5. Maximum of 128 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        bot_policy_ref(str, Optional):
            Bot detection policy for the Virtual Service. It is a reference to an object of type BotDetectionPolicy. Field introduced in 21.1.1. Defaults to None.

        bulk_sync_kvcache(bool, Optional):
            (This is a beta feature). Sync Key-Value cache to the new SEs when VS is scaled out. For ex  SSL sessions are stored using VS's Key-Value cache. When the VS is scaled out, the SSL session information is synced to the new SE, allowing existing SSL sessions to be reused on the new SE. . Field introduced in 17.2.7, 18.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        close_client_conn_on_config_update(bool, Optional):
            close client connection on vs config update. Field introduced in 17.2.4. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        cloud_config_cksum(str, Optional):
            Checksum of cloud configuration for VS. Internally set by cloud connector. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        cloud_ref(str, Optional):
             It is a reference to an object of type Cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        cloud_type(str, Optional):
             Enum options - CLOUD_NONE, CLOUD_VCENTER, CLOUD_OPENSTACK, CLOUD_AWS, CLOUD_VCA, CLOUD_APIC, CLOUD_MESOS, CLOUD_LINUXSERVER, CLOUD_DOCKER_UCP, CLOUD_RANCHER, CLOUD_OSHIFT_K8S, CLOUD_AZURE, CLOUD_GCP, CLOUD_NSXT. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- CLOUD_NONE,CLOUD_VCENTER), Basic edition(Allowed values- CLOUD_NONE,CLOUD_NSXT), Enterprise with Cloud Services edition. Defaults to None.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        connections_rate_limit(dict[str, Any], Optional):
            connections_rate_limit. Defaults to None.

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

        content_rewrite(dict[str, Any], Optional):
            content_rewrite. Defaults to None.

            * rewritable_content_ref (str, Optional):
                Rewrite only content types listed in this string group. Content types not present in this list are not rewritten. It is a reference to an object of type StringGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * rsp_rewrite_rules (List[dict[str, Any]], Optional):
                Content Rewrite rules to be enabled on theresponse body. Field introduced in 21.1.3. Maximum of 1 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * enable (bool, Optional):
                    Enable rewrite rule on response body. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * index (int, Optional):
                    Index of the response rewrite rule. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * name (str, Optional):
                    Name of the response rewrite rule. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * pairs (List[dict[str, Any]], Optional):
                    List of search-and-replace string pairs for the response body. For eg. Strings 'foo' and 'bar', where all searches of 'foo' in the response body will be replaced with 'bar'. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * replacement_string (dict[str, Any], Optional):
                        replacement_string

                        * type (str, Optional):
                            Type of replacement string - can be a variable exposed from datascript, value of an HTTP variable, a custom user-input literal string, or a string with all three combined. Enum options - DATASCRIPT_VAR, AVI_VAR, LITERAL_STRING, COMBINATION_STRING. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * val (str, Optional):
                            Value of the replacement string - name of variable exposed from datascript, name of the HTTP header, a custom user-input literal string, or a string with all three combined. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * search_string (dict[str, Any]):
                        search_string

                        * type (str, Optional):
                            Type of search string - can be a variable exposed from datascript, value of an HTTP variable, a custom user-input literal string, or a regular expression. Enum options - SEARCH_DATASCRIPT_VAR, SEARCH_AVI_VAR, SEARCH_LITERAL_STRING, SEARCH_REGEX. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                        * val (str):
                            Value of search string - can be a variable exposed from datascript, value of an HTTP variable, a custom user-input literal string, or a regular expression. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        created_by(str, Optional):
            Creator name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        delay_fairness(bool, Optional):
            Select the algorithm for QoS fairness.  This determines how multiple Virtual Services sharing the same Service Engines will prioritize traffic over a congested network. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        description(str, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        dns_info(List[dict[str, Any]], Optional):
            Service discovery specific data including fully qualified domain name, type and Time-To-Live of the DNS record. Note that only one of fqdn and dns_info setting is allowed. Maximum of 1000 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * algorithm (str, Optional):
                Specifies the algorithm to pick the IP address(es) to be returned, when multiple entries are configured. This does not apply if num_records_in_response is 0. Default is consistent hash. Enum options - DNS_RECORD_RESPONSE_ROUND_ROBIN, DNS_RECORD_RESPONSE_CONSISTENT_HASH. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * cname (dict[str, Any], Optional):
                cname

                * cname (str):
                    Canonical name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * fqdn (str, Optional):
                Fully qualified domain name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * metadata (str, Optional):
                Any metadata associated with this record. Field introduced in 17.2.2. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

            * num_records_in_response (int, Optional):
                Specifies the number of records returned for this FQDN. Enter 0 to return all records. Default is 0. Allowed values are 0-20. Special values are 0- Return all records. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ttl (int, Optional):
                Time to live for fqdn record. Default value is chosen from DNS profile for this cloud if no value provided. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * type (str, Optional):
                DNS record type. Enum options - DNS_RECORD_OTHER, DNS_RECORD_A, DNS_RECORD_NS, DNS_RECORD_CNAME, DNS_RECORD_SOA, DNS_RECORD_PTR, DNS_RECORD_HINFO, DNS_RECORD_MX, DNS_RECORD_TXT, DNS_RECORD_RP, DNS_RECORD_DNSKEY, DNS_RECORD_AAAA, DNS_RECORD_SRV, DNS_RECORD_OPT, DNS_RECORD_RRSIG, DNS_RECORD_AXFR, DNS_RECORD_ANY. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        dns_policies(List[dict[str, Any]], Optional):
            DNS Policies applied on the dns traffic of the Virtual Service. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * dns_policy_ref (str):
                UUID of the dns policy. It is a reference to an object of type DnsPolicy. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * index (int):
                Index of the dns policy. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        east_west_placement(bool, Optional):
            Force placement on all SE's in service group (Mesos mode only). Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        enable_autogw(bool, Optional):
            Response traffic to clients will be sent back to the source MAC address of the connection, rather than statically sent to a default gateway. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Special default for Essentials edition is false, Basic edition is false, Enterprise is True. Defaults to None.

        enable_rhi(bool, Optional):
            Enable Route Health Injection using the BGP Config in the vrf context. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        enable_rhi_snat(bool, Optional):
            Enable Route Health Injection for Source NAT'ted floating IP Address using the BGP Config in the vrf context. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        enabled(bool, Optional):
            Enable or disable the Virtual Service. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        error_page_profile_ref(str, Optional):
            Error Page Profile to be used for this virtualservice.This profile is used to send the custom error page to the client generated by the proxy. It is a reference to an object of type ErrorPageProfile. Field introduced in 17.2.4. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        flow_dist(str, Optional):
            Criteria for flow distribution among SEs. Enum options - LOAD_AWARE, CONSISTENT_HASH_SOURCE_IP_ADDRESS, CONSISTENT_HASH_SOURCE_IP_ADDRESS_AND_PORT. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- LOAD_AWARE), Basic edition(Allowed values- LOAD_AWARE), Enterprise with Cloud Services edition. Defaults to None.

        flow_label_type(str, Optional):
            Criteria for flow labelling. Enum options - NO_LABEL, APPLICATION_LABEL, SERVICE_LABEL. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        fqdn(str, Optional):
            DNS resolvable, fully qualified domain name of the virtualservice. Only one of 'fqdn' and 'dns_info' configuration is allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        host_name_xlate(str, Optional):
            Translate the host name sent to the servers to this value.  Translate the host name sent from servers back to the value used by the client. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        http_policies(List[dict[str, Any]], Optional):
            HTTP Policies applied on the data traffic of the Virtual Service. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * http_policy_set_ref (str):
                UUID of the virtual service HTTP policy collection. It is a reference to an object of type HTTPPolicySet. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * index (int):
                Index of the virtual service HTTP policy collection. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        icap_request_profile_refs(List[str], Optional):
            The config settings for the ICAP server when checking the HTTP request. It is a reference to an object of type IcapProfile. Field introduced in 20.1.1. Maximum of 1 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ign_pool_net_reach(bool, Optional):
            Ignore Pool servers network reachability constraints for Virtual Service placement. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        jwt_config(dict[str, Any], Optional):
            jwt_config. Defaults to None.

            * audience (str):
                Uniquely identifies a resource server. This is used to validate against the aud claim. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * jwt_location (str):
                Defines where to look for JWT in the request. Enum options - JWT_LOCATION_AUTHORIZATION_HEADER, JWT_LOCATION_QUERY_PARAM. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * jwt_name (str, Optional):
                Name by which the JWT can be identified if the token is sent as a query param in the request url. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        l4_policies(List[dict[str, Any]], Optional):
            L4 Policies applied to the data traffic of the Virtual Service. Field introduced in 17.2.7. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * index (int):
                Index of the virtual service L4 policy set. Field introduced in 17.2.7. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * l4_policy_set_ref (str):
                ID of the virtual service L4 policy set. It is a reference to an object of type L4PolicySet. Field introduced in 17.2.7. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        ldap_vs_config(dict[str, Any], Optional):
            ldap_vs_config. Defaults to None.

            * realm (str, Optional):
                Basic authentication realm to present to a user along with the prompt for credentials. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * se_auth_ldap_bind_timeout (int, Optional):
                Default bind timeout enforced on connections to LDAP server. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * se_auth_ldap_cache_size (int, Optional):
                Size of LDAP auth credentials cache used on the dataplane. Field introduced in 21.1.1. Unit is BYTES. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * se_auth_ldap_connect_timeout (int, Optional):
                Default connection timeout enforced on connections to LDAP server. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * se_auth_ldap_conns_per_server (int, Optional):
                Number of concurrent connections to LDAP server by a single basic auth LDAP process. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * se_auth_ldap_reconnect_timeout (int, Optional):
                Default reconnect timeout enforced on connections to LDAP server. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * se_auth_ldap_request_timeout (int, Optional):
                Default login or group search request timeout enforced on connections to LDAP server. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * se_auth_ldap_servers_failover_only (bool, Optional):
                If enabled, connections are always made to the first available LDAP server in the list and will failover to subsequent servers. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        limit_doser(bool, Optional):
            Limit potential DoS attackers who exceed max_cps_per_client significantly to a fraction of max_cps_per_client for a while. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        max_cps_per_client(int, Optional):
            Maximum connections per second per client IP. Allowed values are 10-1000. Special values are 0- unlimited. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        microservice_ref(str, Optional):
            Microservice representing the virtual service. It is a reference to an object of type MicroService. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        min_pools_up(int, Optional):
            Minimum number of UP pools to mark VS up. Field introduced in 18.2.1, 17.2.12. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        network_profile_ref(str, Optional):
            Determines network settings such as protocol, TCP or UDP, and related options for the protocol. It is a reference to an object of type NetworkProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Special default for Essentials edition is System-TCP-Fast-Path. Defaults to None.

        network_security_policy_ref(str, Optional):
            Network security policies for the Virtual Service. It is a reference to an object of type NetworkSecurityPolicy. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        nsx_securitygroup(List[str], Optional):
            A list of NSX Groups representing the Clients which can access the Virtual IP of the Virtual Service. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        oauth_vs_config(dict[str, Any], Optional):
            oauth_vs_config. Defaults to None.

            * cookie_name (str, Optional):
                HTTP cookie name for authorized session. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * cookie_timeout (int, Optional):
                HTTP cookie timeout for authorized session. Allowed values are 1-1440. Field introduced in 21.1.3. Unit is MIN. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * key (List[dict[str, Any]], Optional):
                Key to generate the cookie. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * aes_key (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * hmac_key (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str, Optional):
                    name to use for cookie encryption. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * logout_uri (str, Optional):
                URI which triggers OAuth logout. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * oauth_settings (List[dict[str, Any]], Optional):
                Application and IDP settings for OAuth/OIDC. Field introduced in 21.1.3. Maximum of 1 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * app_settings (dict[str, Any], Optional):
                    app_settings

                    * client_id (str):
                        Application specific identifier. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * client_secret (str):
                        Application specific identifier secret. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * oidc_config (dict[str, Any], Optional):
                        oidc_config

                        * oidc_enable (bool, Optional):
                            Adds openid as one of the scopes enabling OpenID Connect flow. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                        * profile (bool, Optional):
                            Fetch profile information by enabling profile scope. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                        * userinfo (bool, Optional):
                            Fetch profile information from Userinfo Endpoint. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * scopes (List[str], Optional):
                        Scope specified to give limited access to the app. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * auth_profile_ref (str):
                    Auth Profile to use for validating users. It is a reference to an object of type AuthProfile. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * resource_server (dict[str, Any], Optional):
                    resource_server

                    * access_type (str):
                        Access token type. Enum options - ACCESS_TOKEN_TYPE_JWT, ACCESS_TOKEN_TYPE_OPAQUE. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * introspection_data_timeout (int, Optional):
                        Lifetime of the cached introspection data. Allowed values are 0-1440. Special values are 0- No caching of introspection data. Field introduced in 22.1.3. Unit is MIN. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * jwt_params (dict[str, Any], Optional):
                        jwt_params

                        * audience (str):
                            Audience parameter used for validation using JWT token. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * opaque_token_params (dict[str, Any], Optional):
                        opaque_token_params

                        * server_id (str):
                            Resource server specific identifier used to validate against introspection endpoint when access token is opaque. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                        * server_secret (str):
                            Resource server specific password/secret. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * post_logout_redirect_uri (str, Optional):
                URI to which IDP will redirect to after the logout. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * redirect_uri (str, Optional):
                Redirect URI specified in the request to Authorization Server. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        performance_limits(dict[str, Any], Optional):
            performance_limits. Defaults to None.

            * max_concurrent_connections (int, Optional):
                The maximum number of concurrent client conections allowed to the Virtual Service. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_throughput (int, Optional):
                The maximum throughput per second for all clients allowed through the client side of the Virtual Service per SE. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        pool_group_ref(str, Optional):
            The pool group is an object that contains pools. It is a reference to an object of type PoolGroup. Allowed in Enterprise edition with any value, Basic, Enterprise with Cloud Services edition. Defaults to None.

        pool_ref(str, Optional):
            The pool is an object that contains destination servers and related attributes such as load-balancing and persistence. It is a reference to an object of type Pool. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        remove_listening_port_on_vs_down(bool, Optional):
            Remove listening port if VirtualService is down. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        requests_rate_limit(dict[str, Any], Optional):
            requests_rate_limit. Defaults to None.

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

        saml_sp_config(dict[str, Any], Optional):
            saml_sp_config. Defaults to None.

            * acs_index (int, Optional):
                Index to be used in the AssertionConsumerServiceIndex attribute of the Authentication request, if the authn_req_acs_type is set to Use AssertionConsumerServiceIndex. Allowed values are 0-64. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * authn_req_acs_type (str):
                Option to set the ACS attributes in the AuthnRequest . Enum options - SAML_AUTHN_REQ_ACS_TYPE_URL, SAML_AUTHN_REQ_ACS_TYPE_INDEX, SAML_AUTHN_REQ_ACS_TYPE_NONE. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * cookie_name (str, Optional):
                HTTP cookie name for authenticated session. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * cookie_timeout (int, Optional):
                Cookie timeout in minutes. Allowed values are 1-1440. Field introduced in 18.2.3. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * entity_id (str):
                Globally unique SAML entityID for this node. The SAML application entity ID on the IDP should match this. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * key (List[dict[str, Any]], Optional):
                Key to generate the cookie. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * aes_key (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * hmac_key (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str, Optional):
                    name to use for cookie encryption. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * signing_ssl_key_and_certificate_ref (str, Optional):
                SP will use this SSL certificate to sign requests going to the IdP and decrypt the assertions coming from IdP. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * single_signon_url (str):
                SAML Single Signon endpoint to receive the Authentication response. This also specifies the destination endpoint to be configured for this application on the IDP. If the authn_req_acs_type is set to 'Use AssertionConsumerServiceURL', this endpoint will be sent in the AssertionConsumerServiceURL attribute of the Authentication request. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * sp_metadata (str, Optional):
                SAML SP metadata for this application. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

            * use_idp_session_timeout (bool, Optional):
                By enabling this field IdP can control how long the SP session can exist through the SessionNotOnOrAfter field in the AuthNStatement of SAML Response. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        scaleout_ecmp(bool, Optional):
            Disable re-distribution of flows across service engines for a virtual service. Enable if the network itself performs flow hashing with ECMP in environments such as GCP. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_group_ref(str, Optional):
            The Service Engine Group to use for this Virtual Service. Moving to a new SE Group is disruptive to existing connections for this VS. It is a reference to an object of type ServiceEngineGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        security_policy_ref(str, Optional):
            Security policy applied on the traffic of the Virtual Service. This policy is used to perform security actions such as Distributed Denial of Service (DDoS) attack mitigation, etc. It is a reference to an object of type SecurityPolicy. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        server_network_profile_ref(str, Optional):
            Determines the network settings profile for the server side of TCP proxied connections.  Leave blank to use the same settings as the client to VS side of the connection. It is a reference to an object of type NetworkProfile. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        service_metadata(str, Optional):
            Metadata pertaining to the Service provided by this virtual service. In Openshift/Kubernetes environments, egress pod info is stored. Any user input to this field will be overwritten by Avi Vantage. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        service_pool_select(List[dict[str, Any]], Optional):
            Select pool based on destination port. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * service_pool_group_ref (str, Optional):
                 It is a reference to an object of type PoolGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * service_pool_ref (str, Optional):
                 It is a reference to an object of type Pool. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * service_port (int):
                Pool based destination port. Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * service_port_range_end (int, Optional):
                The end of the Service port number range. Allowed values are 1-65535. Special values are 0- single port. Field introduced in 17.2.4. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * service_protocol (str, Optional):
                Destination protocol to match for the pool selection. If not specified, it will match any protocol. Enum options - PROTOCOL_TYPE_TCP_PROXY, PROTOCOL_TYPE_TCP_FAST_PATH, PROTOCOL_TYPE_UDP_FAST_PATH, PROTOCOL_TYPE_UDP_PROXY, PROTOCOL_TYPE_SCTP_PROXY, PROTOCOL_TYPE_SCTP_FAST_PATH. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        services(List[dict[str, Any]], Optional):
            List of Services defined for this Virtual Service. Maximum of 2048 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * enable_http2 (bool, Optional):
                Enable HTTP2 on this port. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * enable_ssl (bool, Optional):
                Enable SSL termination and offload for traffic from clients. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * horizon_internal_ports (bool, Optional):
                Used for Horizon deployment. If set used for L7 redirect. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * is_active_ftp_data_port (bool, Optional):
                Source port used by VS for active FTP data connections. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * override_application_profile_ref (str, Optional):
                Enable application layer specific features for the this specific service. It is a reference to an object of type ApplicationProfile. Field introduced in 17.2.4. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * override_network_profile_ref (str, Optional):
                Override the network profile for this specific service port. It is a reference to an object of type NetworkProfile. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * port (int):
                The Virtual Service's port number. Allowed values are 0-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * port_range_end (int, Optional):
                The end of the Virtual Service's port number range. Allowed values are 1-65535. Special values are 0- single port. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        sideband_profile(dict[str, Any], Optional):
            sideband_profile. Defaults to None.

            * ip (List[dict[str, Any]], Optional):
                IP Address of the sideband server. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * sideband_max_request_body_size (int, Optional):
                Maximum size of the request body that will be sent on the sideband. Allowed values are 0-16384. Unit is BYTES. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        snat_ip(List[dict[str, Any]], Optional):
            NAT'ted floating source IP Address(es) for upstream connection to servers. Maximum of 32 items allowed. Allowed in Enterprise edition with any value, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * addr (str):
                IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * type (str):
                 Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        sp_pool_refs(List[str], Optional):
            GSLB pools used to manage site-persistence functionality. Each site-persistence pool contains the virtualservices in all the other sites, that is auto-generated by the GSLB manager. This is a read-only field for the user. It is a reference to an object of type Pool. Field introduced in 17.2.2. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ssl_key_and_certificate_refs(List[str], Optional):
            Select or create one or two certificates, EC and/or RSA, that will be presented to SSL/TLS terminated connections. It is a reference to an object of type SSLKeyAndCertificate. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ssl_profile_ref(str, Optional):
            Determines the set of SSL versions and ciphers to accept for SSL/TLS terminated connections. It is a reference to an object of type SSLProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ssl_profile_selectors(List[dict[str, Any]], Optional):
            Select SSL Profile based on client IP address match. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * client_ip_list (dict[str, Any]):
                client_ip_list

                * addrs (List[dict[str, Any]], Optional):
                    IP address(es). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * group_refs (List[str], Optional):
                    UUID of IP address group(s). It is a reference to an object of type IpAddrGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * match_criteria (str):
                    Criterion to use for IP address matching the HTTP request. Enum options - IS_IN, IS_NOT_IN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * prefixes (List[dict[str, Any]], Optional):
                    IP address prefix(es). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ranges (List[dict[str, Any]], Optional):
                    IP address range(s). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * begin (dict[str, Any]):
                        begin

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * end (dict[str, Any]):
                        end

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ssl_profile_ref (str):
                SSL profile for the client IP addresses listed. It is a reference to an object of type SSLProfile. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        ssl_sess_cache_avg_size(int, Optional):
            Expected number of SSL session cache entries (may be exceeded). Allowed values are 1024-16383. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        sso_policy_ref(str, Optional):
            The SSO Policy attached to the virtualservice. It is a reference to an object of type SSOPolicy. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        static_dns_records(List[dict[str, Any]], Optional):
            List of static DNS records applied to this Virtual Service. These are static entries and no health monitoring is performed against the IP addresses. Maximum of 1000 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * algorithm (str, Optional):
                Specifies the algorithm to pick the IP address(es) to be returned, when multiple entries are configured. This does not apply if num_records_in_response is 0. Default is round-robin. Enum options - DNS_RECORD_RESPONSE_ROUND_ROBIN, DNS_RECORD_RESPONSE_CONSISTENT_HASH. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * cname (dict[str, Any], Optional):
                cname

                * cname (str):
                    Canonical name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * delegated (bool, Optional):
                Configured FQDNs are delegated domains (i.e. they represent a zone cut). Field introduced in 17.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * description (str, Optional):
                Details of DNS record. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * fqdn (List[str], Optional):
                Fully Qualified Domain Name. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ip6_address (List[dict[str, Any]], Optional):
                IPv6 address in AAAA record. Field introduced in 18.1.1. Maximum of 4 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ip6_address (dict[str, Any]):
                    ip6_address

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ip_address (List[dict[str, Any]], Optional):
                IP address in A record. Maximum of 4 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ip_address (dict[str, Any]):
                    ip_address

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * metadata (str, Optional):
                Internal metadata for the DNS record. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mx_records (List[dict[str, Any]], Optional):
                MX record. Field introduced in 18.2.9, 20.1.1. Maximum of 4 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * host (str):
                    Fully qualified domain name of a mailserver . The host name maps directly to one or more address records in the DNS table, and must not point to any CNAME records (RFC 2181). Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * priority (int):
                    The priority field identifies which mail server should be preferred. Allowed values are 0-65535. Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ns (List[dict[str, Any]], Optional):
                Name Server information in NS record. Field introduced in 17.1.1. Maximum of 13 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ip6_address (dict[str, Any], Optional):
                    ip6_address

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ip_address (dict[str, Any], Optional):
                    ip_address

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * nsname (str):
                    Name Server name. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * num_records_in_response (int, Optional):
                Specifies the number of records returned by the DNS service. Enter 0 to return all records. Default is 0. Allowed values are 0-20. Special values are 0- Return all records. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * service_locator (List[dict[str, Any]], Optional):
                Service locator info in SRV record. Maximum of 4 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * port (int):
                    Service port. Allowed values are 0-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * priority (int, Optional):
                    Priority of the target hosting the service, low value implies higher priority for this service record. Allowed values are 0-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * target (str, Optional):
                    Canonical hostname, of the machine hosting the service, with no trailing period. 'default.host' is valid but not 'default.host.'. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * weight (int, Optional):
                    Relative weight for service records with same priority, high value implies higher preference for this service record. Allowed values are 0-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ttl (int, Optional):
                Time To Live for this DNS record. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * txt_records (List[dict[str, Any]], Optional):
                Text record. Field introduced in 18.2.9, 20.1.1. Maximum of 4 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * text_str (str):
                    Text data associated with the FQDN. Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * type (str):
                DNS record type. Enum options - DNS_RECORD_OTHER, DNS_RECORD_A, DNS_RECORD_NS, DNS_RECORD_CNAME, DNS_RECORD_SOA, DNS_RECORD_PTR, DNS_RECORD_HINFO, DNS_RECORD_MX, DNS_RECORD_TXT, DNS_RECORD_RP, DNS_RECORD_DNSKEY, DNS_RECORD_AAAA, DNS_RECORD_SRV, DNS_RECORD_OPT, DNS_RECORD_RRSIG, DNS_RECORD_AXFR, DNS_RECORD_ANY. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * wildcard_match (bool, Optional):
                Enable wild-card match of fqdn  if an exact match is not found in the DNS table, the longest match is chosen by wild-carding the fqdn in the DNS request. Default is false. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        test_se_datastore_level_1_ref(str, Optional):
            Used for testing SE Datastore Upgrade 2.0 functionality. It is a reference to an object of type TestSeDatastoreLevel1. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        topology_policies(List[dict[str, Any]], Optional):
            Topology Policies applied on the dns traffic of the Virtual Service based onGSLB Topology algorithm. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * dns_policy_ref (str):
                UUID of the dns policy. It is a reference to an object of type DnsPolicy. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * index (int):
                Index of the dns policy. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        traffic_clone_profile_ref(str, Optional):
            Server network or list of servers for cloning traffic. It is a reference to an object of type TrafficCloneProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        traffic_enabled(bool, Optional):
            Knob to enable the Virtual Service traffic on its assigned service engines. This setting is effective only when the enabled flag is set to True. Field introduced in 17.2.8. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        type(str, Optional):
            Specify if this is a normal Virtual Service, or if it is the parent or child of an SNI-enabled virtual hosted Virtual Service. Enum options - VS_TYPE_NORMAL, VS_TYPE_VH_PARENT, VS_TYPE_VH_CHILD. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- VS_TYPE_NORMAL), Basic edition(Allowed values- VS_TYPE_NORMAL,VS_TYPE_VH_PARENT), Enterprise with Cloud Services edition. Defaults to None.

        use_bridge_ip_as_vip(bool, Optional):
            Use Bridge IP as VIP on each Host in Mesos deployments. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        use_vip_as_snat(bool, Optional):
            Use the Virtual IP as the SNAT IP for health monitoring and sending traffic to the backend servers instead of the Service Engine interface IP. The caveat of enabling this option is that the VirtualService cannot be configued in an Active-Active HA mode. DNS based Multi VIP solution has to be used for HA & Non-disruptive Upgrade purposes. Field introduced in 17.1.9,17.2.3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic, Enterprise with Cloud Services edition. Defaults to None.

        vh_domain_name(List[str], Optional):
            The exact name requested from the client's SNI-enabled TLS hello domain name field. If this is a match, the parent VS will forward the connection to this child VS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vh_matches(List[dict[str, Any]], Optional):
            Match criteria to select this child VS. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * host (str):
                Host/domain name match configuration. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * path (List[dict[str, Any]], Optional):
                Resource/uri path match configuration. Must be configured along with Host match criteria. Field deprecated in 22.1.3. Field introduced in 20.1.3. Minimum of 1 items required. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * match_case (str, Optional):
                    Case sensitivity to use for the matching. Enum options - SENSITIVE, INSENSITIVE. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * match_criteria (str):
                    Criterion to use for matching the path in the HTTP request URI. Enum options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- BEGINS_WITH,DOES_NOT_BEGIN_WITH,CONTAINS,DOES_NOT_CONTAIN,ENDS_WITH,DOES_NOT_END_WITH,EQUALS,DOES_NOT_EQUAL), Basic edition(Allowed values- BEGINS_WITH,DOES_NOT_BEGIN_WITH,CONTAINS,DOES_NOT_CONTAIN,ENDS_WITH,DOES_NOT_END_WITH,EQUALS,DOES_NOT_EQUAL), Enterprise with Cloud Services edition.

                * match_decoded_string (bool, Optional):
                    Match against the decoded URI path. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * match_str (List[str], Optional):
                    String values. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * string_group_refs (List[str], Optional):
                    UUID of the string group(s). It is a reference to an object of type StringGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * rules (List[dict[str, Any]], Optional):
                Add rules for selecting the virtual service. At least one rule must be configured. Field introduced in 22.1.3. Minimum of 1 items required. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * matches (dict[str, Any]):
                    matches

                    * bot_detection_result (dict[str, Any], Optional):
                        bot_detection_result

                        * classifications (List[dict[str, Any]], Optional):
                            Bot classification types. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                            * type (str):
                                One of the system-defined Bot classification types. Enum options - HUMAN, GOOD_BOT, BAD_BOT, DANGEROUS_BOT, USER_DEFINED_BOT, UNKNOWN_CLIENT. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                            * user_defined_type (str, Optional):
                                If 'type' has BotClassificationTypes value 'USER_DEFINED', this is the user-defined value. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                        * match_operation (str):
                            Match criteria. Enum options - IS_IN, IS_NOT_IN. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * client_ip (dict[str, Any], Optional):
                        client_ip

                        * addrs (List[dict[str, Any]], Optional):
                            IP address(es). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * addr (str):
                                IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                 Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * group_refs (List[str], Optional):
                            UUID of IP address group(s). It is a reference to an object of type IpAddrGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * match_criteria (str):
                            Criterion to use for IP address matching the HTTP request. Enum options - IS_IN, IS_NOT_IN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * prefixes (List[dict[str, Any]], Optional):
                            IP address prefix(es). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * ip_addr (dict[str, Any]):
                                ip_addr

                                * addr (str):
                                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                                * type (str):
                                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * mask (int):
                                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * ranges (List[dict[str, Any]], Optional):
                            IP address range(s). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * begin (dict[str, Any]):
                                begin

                                * addr (str):
                                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                                * type (str):
                                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * end (dict[str, Any]):
                                end

                                * addr (str):
                                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                                * type (str):
                                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * cookie (dict[str, Any], Optional):
                        cookie

                        * match_case (str, Optional):
                            Case sensitivity to use for the match. Enum options - SENSITIVE, INSENSITIVE. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * match_criteria (str):
                            Criterion to use for matching the cookie in the HTTP request. Enum options - HDR_EXISTS, HDR_DOES_NOT_EXIST, HDR_BEGINS_WITH, HDR_DOES_NOT_BEGIN_WITH, HDR_CONTAINS, HDR_DOES_NOT_CONTAIN, HDR_ENDS_WITH, HDR_DOES_NOT_END_WITH, HDR_EQUALS, HDR_DOES_NOT_EQUAL. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * name (str):
                            Name of the cookie. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * value (str, Optional):
                            String value in the cookie. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * geo_matches (List[dict[str, Any]], Optional):
                        Configure the geo information. Field introduced in 21.1.1. Maximum of 1 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                        * attribute (str):
                            The Geo data type to match on. Enum options - ATTRIBUTE_IP_PREFIX, ATTRIBUTE_COUNTRY_CODE, ATTRIBUTE_COUNTRY_NAME, ATTRIBUTE_CONTINENT_CODE, ATTRIBUTE_CONTINENT_NAME, ATTRIBUTE_REGION_NAME, ATTRIBUTE_CITY_NAME, ATTRIBUTE_ISP_NAME, ATTRIBUTE_ORGANIZATION_NAME, ATTRIBUTE_AS_NUMBER, ATTRIBUTE_AS_NAME, ATTRIBUTE_LONGITUDE, ATTRIBUTE_LATITUDE, ATTRIBUTE_CUSTOM_1, ATTRIBUTE_CUSTOM_2, ATTRIBUTE_CUSTOM_3, ATTRIBUTE_CUSTOM_4, ATTRIBUTE_CUSTOM_5, ATTRIBUTE_CUSTOM_6, ATTRIBUTE_CUSTOM_7, ATTRIBUTE_CUSTOM_8, ATTRIBUTE_CUSTOM_9, ATTRIBUTE_USER_DEFINED_MAPPING. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                        * match_operation (str):
                            Match criteria. Enum options - IS_IN, IS_NOT_IN. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                        * values (List[str]):
                            The values to match. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * hdrs (List[dict[str, Any]], Optional):
                        Configure HTTP header(s). All configured headers must match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * hdr (str):
                            Name of the HTTP header whose value is to be matched. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * match_case (str, Optional):
                            Case sensitivity to use for the match. Enum options - SENSITIVE, INSENSITIVE. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * match_criteria (str):
                            Criterion to use for matching headers in the HTTP request. Enum options - HDR_EXISTS, HDR_DOES_NOT_EXIST, HDR_BEGINS_WITH, HDR_DOES_NOT_BEGIN_WITH, HDR_CONTAINS, HDR_DOES_NOT_CONTAIN, HDR_ENDS_WITH, HDR_DOES_NOT_END_WITH, HDR_EQUALS, HDR_DOES_NOT_EQUAL. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * value (List[str], Optional):
                            String values to match in the HTTP header. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * host_hdr (dict[str, Any], Optional):
                        host_hdr

                        * match_case (str, Optional):
                            Case sensitivity to use for the match. Enum options - SENSITIVE, INSENSITIVE. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * match_criteria (str):
                            Criterion to use for the host header value match. Enum options - HDR_EXISTS, HDR_DOES_NOT_EXIST, HDR_BEGINS_WITH, HDR_DOES_NOT_BEGIN_WITH, HDR_CONTAINS, HDR_DOES_NOT_CONTAIN, HDR_ENDS_WITH, HDR_DOES_NOT_END_WITH, HDR_EQUALS, HDR_DOES_NOT_EQUAL. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * value (List[str], Optional):
                            String value(s) in the host header. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * ip_reputation_type (dict[str, Any], Optional):
                        ip_reputation_type

                        * match_operation (str):
                            Match criteria. Enum options - IS_IN, IS_NOT_IN. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * reputation_types (List[str], Optional):
                            IP reputation type. Enum options - IP_REPUTATION_TYPE_SPAM_SOURCE, IP_REPUTATION_TYPE_WINDOWS_EXPLOITS, IP_REPUTATION_TYPE_WEB_ATTACKS, IP_REPUTATION_TYPE_BOTNETS, IP_REPUTATION_TYPE_SCANNERS, IP_REPUTATION_TYPE_DOS, IP_REPUTATION_TYPE_REPUTATION, IP_REPUTATION_TYPE_PHISHING, IP_REPUTATION_TYPE_PROXY, IP_REPUTATION_TYPE_NETWORK, IP_REPUTATION_TYPE_CLOUD, IP_REPUTATION_TYPE_MOBILE_THREATS, IP_REPUTATION_TYPE_TOR, IP_REPUTATION_TYPE_ALL. Field introduced in 20.1.1. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * method (dict[str, Any], Optional):
                        method

                        * match_criteria (str):
                            Criterion to use for HTTP method matching the method in the HTTP request. Enum options - IS_IN, IS_NOT_IN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * methods (List[str], Optional):
                            Configure HTTP method(s). Enum options - HTTP_METHOD_GET, HTTP_METHOD_HEAD, HTTP_METHOD_PUT, HTTP_METHOD_DELETE, HTTP_METHOD_POST, HTTP_METHOD_OPTIONS, HTTP_METHOD_TRACE, HTTP_METHOD_CONNECT, HTTP_METHOD_PATCH, HTTP_METHOD_PROPFIND, HTTP_METHOD_PROPPATCH, HTTP_METHOD_MKCOL, HTTP_METHOD_COPY, HTTP_METHOD_MOVE, HTTP_METHOD_LOCK, HTTP_METHOD_UNLOCK. Minimum of 1 items required. Maximum of 16 items allowed. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- HTTP_METHOD_GET,HTTP_METHOD_PUT,HTTP_METHOD_POST,HTTP_METHOD_HEAD,HTTP_METHOD_OPTIONS), Basic edition(Allowed values- HTTP_METHOD_GET,HTTP_METHOD_PUT,HTTP_METHOD_POST,HTTP_METHOD_HEAD,HTTP_METHOD_OPTIONS), Enterprise with Cloud Services edition.

                    * path (dict[str, Any], Optional):
                        path

                        * match_case (str, Optional):
                            Case sensitivity to use for the matching. Enum options - SENSITIVE, INSENSITIVE. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * match_criteria (str):
                            Criterion to use for matching the path in the HTTP request URI. Enum options - BEGINS_WITH, DOES_NOT_BEGIN_WITH, CONTAINS, DOES_NOT_CONTAIN, ENDS_WITH, DOES_NOT_END_WITH, EQUALS, DOES_NOT_EQUAL, REGEX_MATCH, REGEX_DOES_NOT_MATCH. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- BEGINS_WITH,DOES_NOT_BEGIN_WITH,CONTAINS,DOES_NOT_CONTAIN,ENDS_WITH,DOES_NOT_END_WITH,EQUALS,DOES_NOT_EQUAL), Basic edition(Allowed values- BEGINS_WITH,DOES_NOT_BEGIN_WITH,CONTAINS,DOES_NOT_CONTAIN,ENDS_WITH,DOES_NOT_END_WITH,EQUALS,DOES_NOT_EQUAL), Enterprise with Cloud Services edition.

                        * match_decoded_string (bool, Optional):
                            Match against the decoded URI path. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                        * match_str (List[str], Optional):
                            String values. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * string_group_refs (List[str], Optional):
                            UUID of the string group(s). It is a reference to an object of type StringGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * protocol (dict[str, Any], Optional):
                        protocol

                        * match_criteria (str):
                            Criterion to use for protocol matching the HTTP request. Enum options - IS_IN, IS_NOT_IN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * protocols (str):
                            HTTP or HTTPS protocol. Enum options - HTTP, HTTPS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * query (dict[str, Any], Optional):
                        query

                        * match_case (str, Optional):
                            Case sensitivity to use for the match. Enum options - SENSITIVE, INSENSITIVE. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * match_criteria (str):
                            Criterion to use for matching the query in HTTP request URI. Enum options - QUERY_MATCH_CONTAINS, QUERY_MATCH_DOES_NOT_CONTAIN, QUERY_MATCH_EXISTS, QUERY_MATCH_DOES_NOT_EXIST, QUERY_MATCH_BEGINS_WITH, QUERY_MATCH_DOES_NOT_BEGIN_WITH, QUERY_MATCH_ENDS_WITH, QUERY_MATCH_DOES_NOT_END_WITH, QUERY_MATCH_EQUALS, QUERY_MATCH_DOES_NOT_EQUAL, QUERY_MATCH_REGEX_MATCH, QUERY_MATCH_REGEX_DOES_NOT_MATCH. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * match_decoded_string (bool, Optional):
                            Match against the decoded URI query. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                        * match_str (List[str], Optional):
                            String value(s). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * string_group_refs (List[str], Optional):
                            UUID of the string group(s). It is a reference to an object of type StringGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * source_ip (dict[str, Any], Optional):
                        source_ip

                        * addrs (List[dict[str, Any]], Optional):
                            IP address(es). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * addr (str):
                                IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                 Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * group_refs (List[str], Optional):
                            UUID of IP address group(s). It is a reference to an object of type IpAddrGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * match_criteria (str):
                            Criterion to use for IP address matching the HTTP request. Enum options - IS_IN, IS_NOT_IN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * prefixes (List[dict[str, Any]], Optional):
                            IP address prefix(es). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * ip_addr (dict[str, Any]):
                                ip_addr

                                * addr (str):
                                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                                * type (str):
                                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * mask (int):
                                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * ranges (List[dict[str, Any]], Optional):
                            IP address range(s). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * begin (dict[str, Any]):
                                begin

                                * addr (str):
                                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                                * type (str):
                                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * end (dict[str, Any]):
                                end

                                * addr (str):
                                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                                * type (str):
                                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * tls_fingerprint_match (dict[str, Any], Optional):
                        tls_fingerprint_match

                        * fingerprints (List[str], Optional):
                            The list of fingerprints. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                        * match_operation (str):
                            Match criteria. Enum options - IS_IN, IS_NOT_IN. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                        * string_group_refs (List[str], Optional):
                            UUIDs of the string groups. It is a reference to an object of type StringGroup. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * version (dict[str, Any], Optional):
                        version

                        * match_criteria (str):
                            Criterion to use for HTTP version matching the version used in the HTTP request. Enum options - IS_IN, IS_NOT_IN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * versions (List[str], Optional):
                            HTTP protocol version. Enum options - ZERO_NINE, ONE_ZERO, ONE_ONE, TWO_ZERO. Minimum of 1 items required. Maximum of 8 items allowed. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- ONE_ZERO,ONE_ONE), Basic edition(Allowed values- ONE_ZERO,ONE_ONE), Enterprise with Cloud Services edition.

                    * vs_port (dict[str, Any], Optional):
                        vs_port

                        * match_criteria (str):
                            Criterion to use for port matching the HTTP request. Enum options - IS_IN, IS_NOT_IN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * ports (List[int], Optional):
                            Listening TCP port(s). Allowed values are 1-65535. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str):
                    Name for the match rule. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        vh_parent_vs_ref(str, Optional):
            Specifies the Virtual Service acting as Virtual Hosting (SNI) parent. It is a reference to an object of type VirtualService. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vh_type(str, Optional):
            Specify if the Virtual Hosting VS is of type SNI or Enhanced. Enum options - VS_TYPE_VH_SNI, VS_TYPE_VH_ENHANCED. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Basic edition(Allowed values- VS_TYPE_VH_SNI,VS_TYPE_VH_ENHANCED), Enterprise with Cloud Services edition. Defaults to None.

        vip(List[dict[str, Any]], Optional):
            List of Virtual Service IPs. While creating a 'Shared VS',please use vsvip_ref to point to the shared entities. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * auto_allocate_floating_ip (bool, Optional):
                Auto-allocate floating/elastic IP from the Cloud infrastructure. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * auto_allocate_ip (bool, Optional):
                Auto-allocate VIP from the provided subnet. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * auto_allocate_ip_type (str, Optional):
                Specifies whether to auto-allocate only a V4 address, only a V6 address, or one of each type. Enum options - V4_ONLY, V6_ONLY, V4_V6. Field introduced in 18.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- V4_ONLY), Basic edition(Allowed values- V4_ONLY), Enterprise with Cloud Services edition.

            * availability_zone (str, Optional):
                Availability-zone to place the Virtual Service. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * avi_allocated_fip (bool, Optional):
                (internal-use) FIP allocated by Avi in the Cloud infrastructure. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * avi_allocated_vip (bool, Optional):
                (internal-use) VIP allocated by Avi in the Cloud infrastructure. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * discovered_networks (List[dict[str, Any]], Optional):
                Discovered networks providing reachability for client facing Vip IP. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

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
                Enable or disable the Vip. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * floating_ip (dict[str, Any], Optional):
                floating_ip

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * floating_ip6 (dict[str, Any], Optional):
                floating_ip6

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * floating_subnet6_uuid (str, Optional):
                If auto_allocate_floating_ip is True and more than one floating-ip subnets exist, then the subnet for the floating IPv6 address allocation. Field introduced in 18.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * floating_subnet_uuid (str, Optional):
                If auto_allocate_floating_ip is True and more than one floating-ip subnets exist, then the subnet for the floating IP address allocation. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ip6_address (dict[str, Any], Optional):
                ip6_address

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ip_address (dict[str, Any], Optional):
                ip_address

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ipam_network_subnet (dict[str, Any], Optional):
                ipam_network_subnet

                * network_ref (str, Optional):
                    Network for VirtualService IP allocation with Vantage as the IPAM provider. Network should be created before this is configured. It is a reference to an object of type Network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * subnet (dict[str, Any], Optional):
                    subnet

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * subnet6 (dict[str, Any], Optional):
                    subnet6

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * subnet6_uuid (str, Optional):
                    Subnet UUID or Name or Prefix for VirtualService IPv6 allocation with AWS or OpenStack as the IPAM provider. Only one of subnet or subnet_uuid configuration is allowed. Field introduced in 18.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * subnet_uuid (str, Optional):
                    Subnet UUID or Name or Prefix for VirtualService IP allocation with AWS or OpenStack as the IPAM provider. Only one of subnet or subnet_uuid configuration is allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * network_ref (str, Optional):
                Manually override the network on which the Vip is placed. It is a reference to an object of type Network. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * placement_networks (List[dict[str, Any]], Optional):
                Placement networks/subnets to use for vip placement. Field introduced in 18.2.5. Maximum of 10 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * network_ref (str, Optional):
                    Network to use for vip placement. It is a reference to an object of type Network. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * subnet (dict[str, Any], Optional):
                    subnet

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * subnet6 (dict[str, Any], Optional):
                    subnet6

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * port_uuid (str, Optional):
                (internal-use) Network port assigned to the Vip IP address. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * prefix_length (int, Optional):
                Mask applied for the Vip, non-default mask supported only for wildcard Vip. Allowed values are 0-32. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 32), Basic edition(Allowed values- 32), Enterprise with Cloud Services edition.

            * subnet (dict[str, Any], Optional):
                subnet

                * ip_addr (dict[str, Any]):
                    ip_addr

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mask (int):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * subnet6 (dict[str, Any], Optional):
                subnet6

                * ip_addr (dict[str, Any]):
                    ip_addr

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mask (int):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * subnet6_uuid (str, Optional):
                If auto_allocate_ip is True, then the subnet for the Vip IPv6 address allocation. This field is applicable only if the VirtualService belongs to an Openstack or AWS cloud, in which case it is mandatory, if auto_allocate is selected. Field introduced in 18.1.1. Allowed in Enterprise edition with any value, Basic, Enterprise with Cloud Services edition.

            * subnet_uuid (str, Optional):
                If auto_allocate_ip is True, then the subnet for the Vip IP address allocation. This field is applicable only if the VirtualService belongs to an Openstack or AWS cloud, in which case it is mandatory, if auto_allocate is selected. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vip_id (str):
                Unique ID associated with the vip. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vrf_context_ref(str, Optional):
            Virtual Routing Context that the Virtual Service is bound to. This is used to provide the isolation of the set of networks the application is attached to. It is a reference to an object of type VrfContext. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vs_datascripts(List[dict[str, Any]], Optional):
            Datascripts applied on the data traffic of the Virtual Service. Allowed in Enterprise edition with any value, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * index (int):
                Index of the virtual service datascript collection. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vs_datascript_set_ref (str):
                UUID of the virtual service datascript collection. It is a reference to an object of type VSDataScriptSet. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vsvip_cloud_config_cksum(str, Optional):
            Checksum of cloud configuration for VsVip. Internally set by cloud connector. Field introduced in 17.2.9, 18.1.2. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vsvip_ref(str, Optional):
            Mostly used during the creation of Shared VS, this field refers to entities that can be shared across Virtual Services. It is a reference to an object of type VsVip. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        waf_policy_ref(str, Optional):
            WAF policy for the Virtual Service. It is a reference to an object of type WafPolicy. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        weight(int, Optional):
            The Quality of Service weight to assign to traffic transmitted from this Virtual Service.  A higher weight will prioritize traffic versus other Virtual Services sharing the same Service Engines. Allowed values are 1-128. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 1), Basic edition(Allowed values- 1), Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


          idem_test_nsx_alb.alb.virtual_service_is_present:
              nsx_alb.nsx_alb.alb.virtual_service.present:
              - active_standby_se_tag: string
              - advertise_down_vs: bool
              - allow_invalid_client_cert: bool
              - analytics_policy:
                  all_headers: bool
                  client_insights: string
                  client_insights_sampling:
                    client_ip:
                      addrs:
                      - addr: string
                        type_: string
                      group_refs:
                      - value
                      match_criteria: string
                      prefixes:
                      - ip_addr:
                          addr: string
                          type_: string
                        mask: int
                      ranges:
                      - begin:
                          addr: string
                          type_: string
                        end:
                          addr: string
                          type_: string
                    sample_uris:
                      match_criteria: string
                      match_str:
                      - value
                      string_group_refs:
                      - value
                    skip_uris:
                      match_criteria: string
                      match_str:
                      - value
                      string_group_refs:
                      - value
                  client_log_filters:
                  - all_headers: bool
                    client_ip:
                      addrs:
                      - addr: string
                        type_: string
                      group_refs:
                      - value
                      match_criteria: string
                      prefixes:
                      - ip_addr:
                          addr: string
                          type_: string
                        mask: int
                      ranges:
                      - begin:
                          addr: string
                          type_: string
                        end:
                          addr: string
                          type_: string
                    duration: int
                    enabled: bool
                    index: int
                    name: string
                    uri:
                      match_criteria: string
                      match_str:
                      - value
                      string_group_refs:
                      - value
                  full_client_logs:
                    duration: int
                    enabled: bool
                    throttle: int
                  learning_log_policy:
                    enabled: bool
                    host: string
                    port: int
                  metrics_realtime_update:
                    duration: int
                    enabled: bool
                  significant_log_throttle: int
                  udf_log_throttle: int
              - analytics_profile_ref: string
              - application_profile_ref: string
              - azure_availability_set: string
              - bgp_peer_labels:
                - value
              - bot_policy_ref: string
              - bulk_sync_kvcache: bool
              - close_client_conn_on_config_update: bool
              - cloud_config_cksum: string
              - cloud_ref: string
              - cloud_type: string
              - configpb_attributes:
                  version: int
              - connections_rate_limit:
                  action:
                    file:
                      content_type: string
                      file_content: string
                      file_length: int
                    redirect:
                      add_string: string
                      host:
                        tokens:
                        - end_index: int
                          start_index: int
                          str_value: string
                          type_: string
                        type_: string
                      keep_query: bool
                      path:
                        tokens:
                        - end_index: int
                          start_index: int
                          str_value: string
                          type_: string
                        type_: string
                      port: int
                      protocol: string
                      status_code: string
                    status_code: string
                    type_: string
                  explicit_tracking: bool
                  fine_grain: bool
                  http_cookie: string
                  http_header: string
                  rate_limiter:
                    burst_sz: int
                    count: int
                    name: string
                    period: int
              - content_rewrite:
                  rewritable_content_ref: string
                  rsp_rewrite_rules:
                  - enable: bool
                    index: int
                    name: string
                    pairs:
                    - replacement_string:
                        type_: string
                        val: string
                      search_string:
                        type_: string
                        val: string
              - created_by: string
              - delay_fairness: bool
              - description: string
              - dns_info:
                - algorithm: string
                  cname:
                    cname: string
                  fqdn: string
                  metadata: string
                  num_records_in_response: int
                  ttl: int
                  type_: string
              - dns_policies:
                - dns_policy_ref: string
                  index: int
              - east_west_placement: bool
              - enable_autogw: bool
              - enable_rhi: bool
              - enable_rhi_snat: bool
              - enabled: bool
              - error_page_profile_ref: string
              - flow_dist: string
              - flow_label_type: string
              - fqdn: string
              - host_name_xlate: string
              - http_policies:
                - http_policy_set_ref: string
                  index: int
              - icap_request_profile_refs:
                - value
              - ign_pool_net_reach: bool
              - jwt_config:
                  audience: string
                  jwt_location: string
                  jwt_name: string
              - l4_policies:
                - index: int
                  l4_policy_set_ref: string
              - ldap_vs_config:
                  realm: string
                  se_auth_ldap_bind_timeout: int
                  se_auth_ldap_cache_size: int
                  se_auth_ldap_connect_timeout: int
                  se_auth_ldap_conns_per_server: int
                  se_auth_ldap_reconnect_timeout: int
                  se_auth_ldap_request_timeout: int
                  se_auth_ldap_servers_failover_only: bool
              - limit_doser: bool
              - markers:
                - key: string
                  values:
                  - value
              - max_cps_per_client: int
              - microservice_ref: string
              - min_pools_up: int
              - network_profile_ref: string
              - network_security_policy_ref: string
              - nsx_securitygroup:
                - value
              - oauth_vs_config:
                  cookie_name: string
                  cookie_timeout: int
                  key:
                  - aes_key: string
                    hmac_key: string
                    name: string
                  logout_uri: string
                  oauth_settings:
                  - app_settings:
                      client_id: string
                      client_secret: string
                      oidc_config:
                        oidc_enable: bool
                        profile: bool
                        userinfo: bool
                      scopes:
                      - value
                    auth_profile_ref: string
                    resource_server:
                      access_type: string
                      introspection_data_timeout: int
                      jwt_params:
                        audience: string
                      opaque_token_params:
                        server_id: string
                        server_secret: string
                  post_logout_redirect_uri: string
                  redirect_uri: string
              - performance_limits:
                  max_concurrent_connections: int
                  max_throughput: int
              - pool_group_ref: string
              - pool_ref: string
              - remove_listening_port_on_vs_down: bool
              - requests_rate_limit:
                  action:
                    file:
                      content_type: string
                      file_content: string
                      file_length: int
                    redirect:
                      add_string: string
                      host:
                        tokens:
                        - end_index: int
                          start_index: int
                          str_value: string
                          type_: string
                        type_: string
                      keep_query: bool
                      path:
                        tokens:
                        - end_index: int
                          start_index: int
                          str_value: string
                          type_: string
                        type_: string
                      port: int
                      protocol: string
                      status_code: string
                    status_code: string
                    type_: string
                  explicit_tracking: bool
                  fine_grain: bool
                  http_cookie: string
                  http_header: string
                  rate_limiter:
                    burst_sz: int
                    count: int
                    name: string
                    period: int
              - saml_sp_config:
                  acs_index: int
                  authn_req_acs_type: string
                  cookie_name: string
                  cookie_timeout: int
                  entity_id: string
                  key:
                  - aes_key: string
                    hmac_key: string
                    name: string
                  signing_ssl_key_and_certificate_ref: string
                  single_signon_url: string
                  sp_metadata: string
                  use_idp_session_timeout: bool
              - scaleout_ecmp: bool
              - se_group_ref: string
              - security_policy_ref: string
              - server_network_profile_ref: string
              - service_metadata: string
              - service_pool_select:
                - service_pool_group_ref: string
                  service_pool_ref: string
                  service_port: int
                  service_port_range_end: int
                  service_protocol: string
              - services:
                - enable_http2: bool
                  enable_ssl: bool
                  horizon_internal_ports: bool
                  is_active_ftp_data_port: bool
                  override_application_profile_ref: string
                  override_network_profile_ref: string
                  port: int
                  port_range_end: int
              - sideband_profile:
                  ip:
                  - addr: string
                    type_: string
                  sideband_max_request_body_size: int
              - snat_ip:
                - addr: string
                  type_: string
              - sp_pool_refs:
                - value
              - ssl_key_and_certificate_refs:
                - value
              - ssl_profile_ref: string
              - ssl_profile_selectors:
                - client_ip_list:
                    addrs:
                    - addr: string
                      type_: string
                    group_refs:
                    - value
                    match_criteria: string
                    prefixes:
                    - ip_addr:
                        addr: string
                        type_: string
                      mask: int
                    ranges:
                    - begin:
                        addr: string
                        type_: string
                      end:
                        addr: string
                        type_: string
                  ssl_profile_ref: string
              - ssl_sess_cache_avg_size: int
              - sso_policy_ref: string
              - static_dns_records:
                - algorithm: string
                  cname:
                    cname: string
                  delegated: bool
                  description: string
                  fqdn:
                  - value
                  ip6_address:
                  - ip6_address:
                      addr: string
                      type_: string
                  ip_address:
                  - ip_address:
                      addr: string
                      type_: string
                  metadata: string
                  mx_records:
                  - host: string
                    priority: int
                  ns:
                  - ip6_address:
                      addr: string
                      type_: string
                    ip_address:
                      addr: string
                      type_: string
                    nsname: string
                  num_records_in_response: int
                  service_locator:
                  - port: int
                    priority: int
                    target: string
                    weight: int
                  ttl: int
                  txt_records:
                  - text_str: string
                  type_: string
                  wildcard_match: bool
              - tenant_ref: string
              - test_se_datastore_level_1_ref: string
              - topology_policies:
                - dns_policy_ref: string
                  index: int
              - traffic_clone_profile_ref: string
              - traffic_enabled: bool
              - type: string
              - use_bridge_ip_as_vip: bool
              - use_vip_as_snat: bool
              - vh_domain_name:
                - value
              - vh_matches:
                - host: string
                  path:
                  - match_case: string
                    match_criteria: string
                    match_decoded_string: bool
                    match_str:
                    - value
                    string_group_refs:
                    - value
                  rules:
                  - matches:
                      bot_detection_result:
                        classifications:
                        - type_: string
                          user_defined_type: string
                        match_operation: string
                      client_ip:
                        addrs:
                        - addr: string
                          type_: string
                        group_refs:
                        - value
                        match_criteria: string
                        prefixes:
                        - ip_addr:
                            addr: string
                            type_: string
                          mask: int
                        ranges:
                        - begin:
                            addr: string
                            type_: string
                          end:
                            addr: string
                            type_: string
                      cookie:
                        match_case: string
                        match_criteria: string
                        name: string
                        value: string
                      geo_matches:
                      - attribute: string
                        match_operation: string
                        values:
                        - value
                      hdrs:
                      - hdr: string
                        match_case: string
                        match_criteria: string
                        value:
                        - value
                      host_hdr:
                        match_case: string
                        match_criteria: string
                        value:
                        - value
                      ip_reputation_type:
                        match_operation: string
                        reputation_types:
                        - value
                      method:
                        match_criteria: string
                        methods:
                        - value
                      path:
                        match_case: string
                        match_criteria: string
                        match_decoded_string: bool
                        match_str:
                        - value
                        string_group_refs:
                        - value
                      protocol:
                        match_criteria: string
                        protocols: string
                      query:
                        match_case: string
                        match_criteria: string
                        match_decoded_string: bool
                        match_str:
                        - value
                        string_group_refs:
                        - value
                      source_ip:
                        addrs:
                        - addr: string
                          type_: string
                        group_refs:
                        - value
                        match_criteria: string
                        prefixes:
                        - ip_addr:
                            addr: string
                            type_: string
                          mask: int
                        ranges:
                        - begin:
                            addr: string
                            type_: string
                          end:
                            addr: string
                            type_: string
                      tls_fingerprint_match:
                        fingerprints:
                        - value
                        match_operation: string
                        string_group_refs:
                        - value
                      version:
                        match_criteria: string
                        versions:
                        - value
                      vs_port:
                        match_criteria: string
                        ports: List[int]
                    name: string
              - vh_parent_vs_ref: string
              - vh_type: string
              - vip:
                - auto_allocate_floating_ip: bool
                  auto_allocate_ip: bool
                  auto_allocate_ip_type: string
                  availability_zone: string
                  avi_allocated_fip: bool
                  avi_allocated_vip: bool
                  discovered_networks:
                  - network_ref: string
                    subnet:
                    - ip_addr:
                        addr: string
                        type_: string
                      mask: int
                    subnet6:
                    - ip_addr:
                        addr: string
                        type_: string
                      mask: int
                  enabled: bool
                  floating_ip:
                    addr: string
                    type_: string
                  floating_ip6:
                    addr: string
                    type_: string
                  floating_subnet6_uuid: string
                  floating_subnet_uuid: string
                  ip6_address:
                    addr: string
                    type_: string
                  ip_address:
                    addr: string
                    type_: string
                  ipam_network_subnet:
                    network_ref: string
                    subnet:
                      ip_addr:
                        addr: string
                        type_: string
                      mask: int
                    subnet6:
                      ip_addr:
                        addr: string
                        type_: string
                      mask: int
                    subnet6_uuid: string
                    subnet_uuid: string
                  network_ref: string
                  placement_networks:
                  - network_ref: string
                    subnet:
                      ip_addr:
                        addr: string
                        type_: string
                      mask: int
                    subnet6:
                      ip_addr:
                        addr: string
                        type_: string
                      mask: int
                  port_uuid: string
                  prefix_length: int
                  subnet:
                    ip_addr:
                      addr: string
                      type_: string
                    mask: int
                  subnet6:
                    ip_addr:
                      addr: string
                      type_: string
                    mask: int
                  subnet6_uuid: string
                  subnet_uuid: string
                  vip_id: string
              - vrf_context_ref: string
              - vs_datascripts:
                - index: int
                  vs_datascript_set_ref: string
              - vsvip_cloud_config_cksum: string
              - vsvip_ref: string
              - waf_policy_ref: string
              - weight: int


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
        before = await hub.exec.nsx_alb.alb.virtual_service.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )

        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = before.ret

        result["comment"].append(f"'nsx_alb.alb.virtual_service:{name}' already exists")

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

        before = await hub.exec.nsx_alb.alb.virtual_service.get(
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
                    before = await hub.exec.nsx_alb.alb.virtual_service.get(
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
                    f"Would update nsx_alb.alb.virtual_service '{name}'",
                )
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.nsx_alb.alb.virtual_service.update(
                    ctx,
                    name=name,
                    resource_id=resource_id,
                    **{
                        "active_standby_se_tag": active_standby_se_tag,
                        "advertise_down_vs": advertise_down_vs,
                        "allow_invalid_client_cert": allow_invalid_client_cert,
                        "analytics_policy": analytics_policy,
                        "analytics_profile_ref": analytics_profile_ref,
                        "application_profile_ref": application_profile_ref,
                        "azure_availability_set": azure_availability_set,
                        "bgp_peer_labels": bgp_peer_labels,
                        "bot_policy_ref": bot_policy_ref,
                        "bulk_sync_kvcache": bulk_sync_kvcache,
                        "close_client_conn_on_config_update": close_client_conn_on_config_update,
                        "cloud_config_cksum": cloud_config_cksum,
                        "cloud_ref": cloud_ref,
                        "cloud_type": cloud_type,
                        "configpb_attributes": configpb_attributes,
                        "connections_rate_limit": connections_rate_limit,
                        "content_rewrite": content_rewrite,
                        "created_by": created_by,
                        "delay_fairness": delay_fairness,
                        "description": description,
                        "dns_info": dns_info,
                        "dns_policies": dns_policies,
                        "east_west_placement": east_west_placement,
                        "enable_autogw": enable_autogw,
                        "enable_rhi": enable_rhi,
                        "enable_rhi_snat": enable_rhi_snat,
                        "enabled": enabled,
                        "error_page_profile_ref": error_page_profile_ref,
                        "flow_dist": flow_dist,
                        "flow_label_type": flow_label_type,
                        "fqdn": fqdn,
                        "host_name_xlate": host_name_xlate,
                        "http_policies": http_policies,
                        "icap_request_profile_refs": icap_request_profile_refs,
                        "ign_pool_net_reach": ign_pool_net_reach,
                        "jwt_config": jwt_config,
                        "l4_policies": l4_policies,
                        "ldap_vs_config": ldap_vs_config,
                        "limit_doser": limit_doser,
                        "markers": markers,
                        "max_cps_per_client": max_cps_per_client,
                        "microservice_ref": microservice_ref,
                        "min_pools_up": min_pools_up,
                        "network_profile_ref": network_profile_ref,
                        "network_security_policy_ref": network_security_policy_ref,
                        "nsx_securitygroup": nsx_securitygroup,
                        "oauth_vs_config": oauth_vs_config,
                        "performance_limits": performance_limits,
                        "pool_group_ref": pool_group_ref,
                        "pool_ref": pool_ref,
                        "remove_listening_port_on_vs_down": remove_listening_port_on_vs_down,
                        "requests_rate_limit": requests_rate_limit,
                        "saml_sp_config": saml_sp_config,
                        "scaleout_ecmp": scaleout_ecmp,
                        "se_group_ref": se_group_ref,
                        "security_policy_ref": security_policy_ref,
                        "server_network_profile_ref": server_network_profile_ref,
                        "service_metadata": service_metadata,
                        "service_pool_select": service_pool_select,
                        "services": services,
                        "sideband_profile": sideband_profile,
                        "snat_ip": snat_ip,
                        "sp_pool_refs": sp_pool_refs,
                        "ssl_key_and_certificate_refs": ssl_key_and_certificate_refs,
                        "ssl_profile_ref": ssl_profile_ref,
                        "ssl_profile_selectors": ssl_profile_selectors,
                        "ssl_sess_cache_avg_size": ssl_sess_cache_avg_size,
                        "sso_policy_ref": sso_policy_ref,
                        "static_dns_records": static_dns_records,
                        "tenant_ref": tenant_ref,
                        "test_se_datastore_level_1_ref": test_se_datastore_level_1_ref,
                        "topology_policies": topology_policies,
                        "traffic_clone_profile_ref": traffic_clone_profile_ref,
                        "traffic_enabled": traffic_enabled,
                        "type": type,
                        "use_bridge_ip_as_vip": use_bridge_ip_as_vip,
                        "use_vip_as_snat": use_vip_as_snat,
                        "vh_domain_name": vh_domain_name,
                        "vh_matches": vh_matches,
                        "vh_parent_vs_ref": vh_parent_vs_ref,
                        "vh_type": vh_type,
                        "vip": vip,
                        "vrf_context_ref": vrf_context_ref,
                        "vs_datascripts": vs_datascripts,
                        "vsvip_cloud_config_cksum": vsvip_cloud_config_cksum,
                        "vsvip_ref": vsvip_ref,
                        "waf_policy_ref": waf_policy_ref,
                        "weight": weight,
                    },
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"].append(
                        f"Updated 'nsx_alb.alb.virtual_service:{name}'"
                    )
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.test:
            result["new_state"] = hub.tool.nsx_alb.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"] = (f"Would create nsx_alb.alb.virtual_service {name}",)
            return result
        else:
            create_ret = await hub.exec.nsx_alb.alb.virtual_service.create(
                ctx,
                name=name,
                **{
                    "resource_id": resource_id,
                    "active_standby_se_tag": active_standby_se_tag,
                    "advertise_down_vs": advertise_down_vs,
                    "allow_invalid_client_cert": allow_invalid_client_cert,
                    "analytics_policy": analytics_policy,
                    "analytics_profile_ref": analytics_profile_ref,
                    "application_profile_ref": application_profile_ref,
                    "azure_availability_set": azure_availability_set,
                    "bgp_peer_labels": bgp_peer_labels,
                    "bot_policy_ref": bot_policy_ref,
                    "bulk_sync_kvcache": bulk_sync_kvcache,
                    "close_client_conn_on_config_update": close_client_conn_on_config_update,
                    "cloud_config_cksum": cloud_config_cksum,
                    "cloud_ref": cloud_ref,
                    "cloud_type": cloud_type,
                    "configpb_attributes": configpb_attributes,
                    "connections_rate_limit": connections_rate_limit,
                    "content_rewrite": content_rewrite,
                    "created_by": created_by,
                    "delay_fairness": delay_fairness,
                    "description": description,
                    "dns_info": dns_info,
                    "dns_policies": dns_policies,
                    "east_west_placement": east_west_placement,
                    "enable_autogw": enable_autogw,
                    "enable_rhi": enable_rhi,
                    "enable_rhi_snat": enable_rhi_snat,
                    "enabled": enabled,
                    "error_page_profile_ref": error_page_profile_ref,
                    "flow_dist": flow_dist,
                    "flow_label_type": flow_label_type,
                    "fqdn": fqdn,
                    "host_name_xlate": host_name_xlate,
                    "http_policies": http_policies,
                    "icap_request_profile_refs": icap_request_profile_refs,
                    "ign_pool_net_reach": ign_pool_net_reach,
                    "jwt_config": jwt_config,
                    "l4_policies": l4_policies,
                    "ldap_vs_config": ldap_vs_config,
                    "limit_doser": limit_doser,
                    "markers": markers,
                    "max_cps_per_client": max_cps_per_client,
                    "microservice_ref": microservice_ref,
                    "min_pools_up": min_pools_up,
                    "network_profile_ref": network_profile_ref,
                    "network_security_policy_ref": network_security_policy_ref,
                    "nsx_securitygroup": nsx_securitygroup,
                    "oauth_vs_config": oauth_vs_config,
                    "performance_limits": performance_limits,
                    "pool_group_ref": pool_group_ref,
                    "pool_ref": pool_ref,
                    "remove_listening_port_on_vs_down": remove_listening_port_on_vs_down,
                    "requests_rate_limit": requests_rate_limit,
                    "saml_sp_config": saml_sp_config,
                    "scaleout_ecmp": scaleout_ecmp,
                    "se_group_ref": se_group_ref,
                    "security_policy_ref": security_policy_ref,
                    "server_network_profile_ref": server_network_profile_ref,
                    "service_metadata": service_metadata,
                    "service_pool_select": service_pool_select,
                    "services": services,
                    "sideband_profile": sideband_profile,
                    "snat_ip": snat_ip,
                    "sp_pool_refs": sp_pool_refs,
                    "ssl_key_and_certificate_refs": ssl_key_and_certificate_refs,
                    "ssl_profile_ref": ssl_profile_ref,
                    "ssl_profile_selectors": ssl_profile_selectors,
                    "ssl_sess_cache_avg_size": ssl_sess_cache_avg_size,
                    "sso_policy_ref": sso_policy_ref,
                    "static_dns_records": static_dns_records,
                    "tenant_ref": tenant_ref,
                    "test_se_datastore_level_1_ref": test_se_datastore_level_1_ref,
                    "topology_policies": topology_policies,
                    "traffic_clone_profile_ref": traffic_clone_profile_ref,
                    "traffic_enabled": traffic_enabled,
                    "type": type,
                    "use_bridge_ip_as_vip": use_bridge_ip_as_vip,
                    "use_vip_as_snat": use_vip_as_snat,
                    "vh_domain_name": vh_domain_name,
                    "vh_matches": vh_matches,
                    "vh_parent_vs_ref": vh_parent_vs_ref,
                    "vh_type": vh_type,
                    "vip": vip,
                    "vrf_context_ref": vrf_context_ref,
                    "vs_datascripts": vs_datascripts,
                    "vsvip_cloud_config_cksum": vsvip_cloud_config_cksum,
                    "vsvip_ref": vsvip_ref,
                    "waf_policy_ref": waf_policy_ref,
                    "weight": weight,
                },
            )
            result["result"] = create_ret["result"]

            if result["result"]:
                result["comment"].append(
                    f"Created 'nsx_alb.alb.virtual_service:{name}'"
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

    after = await hub.exec.nsx_alb.alb.virtual_service.get(
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
            Alb.virtual_service unique ID. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


            idem_test_nsx_alb.alb.virtual_service_is_absent:
              nsx_alb.nsx_alb.alb.virtual_service.absent:


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        result["comment"].append(f"'nsx_alb.alb.virtual_service:{name}' already absent")
        return result

    before = await hub.exec.nsx_alb.alb.virtual_service.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    if before["ret"]:
        if ctx.test:
            result["comment"] = f"Would delete nsx_alb.alb.virtual_service:{name}"
            return result

        delete_ret = await hub.exec.nsx_alb.alb.virtual_service.delete(
            ctx,
            name=name,
            resource_id=resource_id,
        )
        result["result"] = delete_ret["result"]

        if result["result"]:
            result["comment"].append(f"Deleted 'nsx_alb.alb.virtual_service:{name}'")
        else:
            # If there is any failure in delete, it should reconcile.
            # The type of data is less important here to use default reconciliation
            # If there are no changes for 3 runs with rerun_data, then it will come out of execution
            result["rerun_data"] = resource_id
            result["comment"].append(delete_ret["result"])
    else:
        result["comment"].append(f"'nsx_alb.alb.virtual_service:{name}' already absent")
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

            $ idem describe nsx_alb.alb.virtual_service
    """

    result = {}

    ret = await hub.exec.nsx_alb.alb.virtual_service.list(ctx)

    if not ret or not ret["result"]:
        hub.log.debug(
            f"Could not describe nsx_alb.alb.virtual_service {ret['comment']}"
        )
        return result

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "nsx_alb.alb.virtual_service.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
