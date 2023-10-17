"""States module for managing Alb Application Profiles. """
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
    type: str,
    resource_id: str = None,
    app_service_type: str = None,
    cloud_config_cksum: str = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    created_by: str = None,
    description: str = None,
    dns_service_profile: make_dataclass(
        "dns_service_profile",
        [
            ("aaaa_empty_response", bool, field(default=None)),
            ("admin_email", str, field(default=None)),
            ("dns_over_tcp_enabled", bool, field(default=None)),
            (
                "dns_zones",
                List[
                    make_dataclass(
                        "dns_zones",
                        [
                            ("domain_name", str),
                            ("admin_email", str, field(default=None)),
                            ("name_server", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("domain_names", List[str], field(default=None)),
            ("ecs_stripping_enabled", bool, field(default=None)),
            ("edns", bool, field(default=None)),
            ("edns_client_subnet_prefix_len", int, field(default=None)),
            ("error_response", str, field(default=None)),
            ("name_server", str, field(default=None)),
            ("negative_caching_ttl", int, field(default=None)),
            ("num_dns_ip", int, field(default=None)),
            ("ttl", int, field(default=None)),
        ],
    ) = None,
    dos_rl_profile: make_dataclass(
        "dos_rl_profile",
        [
            (
                "dos_profile",
                make_dataclass(
                    "dos_profile",
                    [
                        ("thresh_period", int),
                        (
                            "thresh_info",
                            List[
                                make_dataclass(
                                    "thresh_info",
                                    [
                                        ("attack", str),
                                        ("max_value", int),
                                        ("min_value", int),
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
                "rl_profile",
                make_dataclass(
                    "rl_profile",
                    [
                        (
                            "client_ip_connections_rate_limit",
                            make_dataclass(
                                "client_ip_connections_rate_limit",
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
                                                            (
                                                                "file_length",
                                                                int,
                                                                field(default=None),
                                                            ),
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
                                                            (
                                                                "add_string",
                                                                str,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "keep_query",
                                                                bool,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "port",
                                                                int,
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "status_code",
                                                                str,
                                                                field(default=None),
                                                            ),
                                                        ],
                                                    ),
                                                    field(default=None),
                                                ),
                                                (
                                                    "status_code",
                                                    str,
                                                    field(default=None),
                                                ),
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
                            ),
                            field(default=None),
                        ),
                        (
                            "client_ip_failed_requests_rate_limit",
                            make_dataclass(
                                "client_ip_failed_requests_rate_limit",
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
                                                            (
                                                                "file_length",
                                                                int,
                                                                field(default=None),
                                                            ),
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
                                                            (
                                                                "add_string",
                                                                str,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "keep_query",
                                                                bool,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "port",
                                                                int,
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "status_code",
                                                                str,
                                                                field(default=None),
                                                            ),
                                                        ],
                                                    ),
                                                    field(default=None),
                                                ),
                                                (
                                                    "status_code",
                                                    str,
                                                    field(default=None),
                                                ),
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
                            ),
                            field(default=None),
                        ),
                        (
                            "client_ip_requests_rate_limit",
                            make_dataclass(
                                "client_ip_requests_rate_limit",
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
                                                            (
                                                                "file_length",
                                                                int,
                                                                field(default=None),
                                                            ),
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
                                                            (
                                                                "add_string",
                                                                str,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "keep_query",
                                                                bool,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "port",
                                                                int,
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "status_code",
                                                                str,
                                                                field(default=None),
                                                            ),
                                                        ],
                                                    ),
                                                    field(default=None),
                                                ),
                                                (
                                                    "status_code",
                                                    str,
                                                    field(default=None),
                                                ),
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
                            ),
                            field(default=None),
                        ),
                        (
                            "client_ip_scanners_requests_rate_limit",
                            make_dataclass(
                                "client_ip_scanners_requests_rate_limit",
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
                                                            (
                                                                "file_length",
                                                                int,
                                                                field(default=None),
                                                            ),
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
                                                            (
                                                                "add_string",
                                                                str,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "keep_query",
                                                                bool,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "port",
                                                                int,
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "status_code",
                                                                str,
                                                                field(default=None),
                                                            ),
                                                        ],
                                                    ),
                                                    field(default=None),
                                                ),
                                                (
                                                    "status_code",
                                                    str,
                                                    field(default=None),
                                                ),
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
                            ),
                            field(default=None),
                        ),
                        (
                            "client_ip_to_uri_failed_requests_rate_limit",
                            make_dataclass(
                                "client_ip_to_uri_failed_requests_rate_limit",
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
                                                            (
                                                                "file_length",
                                                                int,
                                                                field(default=None),
                                                            ),
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
                                                            (
                                                                "add_string",
                                                                str,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "keep_query",
                                                                bool,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "port",
                                                                int,
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "status_code",
                                                                str,
                                                                field(default=None),
                                                            ),
                                                        ],
                                                    ),
                                                    field(default=None),
                                                ),
                                                (
                                                    "status_code",
                                                    str,
                                                    field(default=None),
                                                ),
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
                            ),
                            field(default=None),
                        ),
                        (
                            "client_ip_to_uri_requests_rate_limit",
                            make_dataclass(
                                "client_ip_to_uri_requests_rate_limit",
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
                                                            (
                                                                "file_length",
                                                                int,
                                                                field(default=None),
                                                            ),
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
                                                            (
                                                                "add_string",
                                                                str,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "keep_query",
                                                                bool,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "port",
                                                                int,
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "status_code",
                                                                str,
                                                                field(default=None),
                                                            ),
                                                        ],
                                                    ),
                                                    field(default=None),
                                                ),
                                                (
                                                    "status_code",
                                                    str,
                                                    field(default=None),
                                                ),
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
                            ),
                            field(default=None),
                        ),
                        (
                            "custom_requests_rate_limit",
                            make_dataclass(
                                "custom_requests_rate_limit",
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
                                                            (
                                                                "file_length",
                                                                int,
                                                                field(default=None),
                                                            ),
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
                                                            (
                                                                "add_string",
                                                                str,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "keep_query",
                                                                bool,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "port",
                                                                int,
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "status_code",
                                                                str,
                                                                field(default=None),
                                                            ),
                                                        ],
                                                    ),
                                                    field(default=None),
                                                ),
                                                (
                                                    "status_code",
                                                    str,
                                                    field(default=None),
                                                ),
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
                            ),
                            field(default=None),
                        ),
                        (
                            "http_header_rate_limits",
                            List[
                                make_dataclass(
                                    "http_header_rate_limits",
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
                                                                (
                                                                    "file_length",
                                                                    int,
                                                                    field(default=None),
                                                                ),
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
                                                                (
                                                                    "add_string",
                                                                    str,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "host",
                                                                    make_dataclass(
                                                                        "host",
                                                                        [
                                                                            (
                                                                                "type",
                                                                                str,
                                                                            ),
                                                                            (
                                                                                "tokens",
                                                                                List[
                                                                                    make_dataclass(
                                                                                        "tokens",
                                                                                        [
                                                                                            (
                                                                                                "type",
                                                                                                str,
                                                                                            ),
                                                                                            (
                                                                                                "end_index",
                                                                                                int,
                                                                                                field(
                                                                                                    default=None
                                                                                                ),
                                                                                            ),
                                                                                            (
                                                                                                "start_index",
                                                                                                int,
                                                                                                field(
                                                                                                    default=None
                                                                                                ),
                                                                                            ),
                                                                                            (
                                                                                                "str_value",
                                                                                                str,
                                                                                                field(
                                                                                                    default=None
                                                                                                ),
                                                                                            ),
                                                                                        ],
                                                                                    )
                                                                                ],
                                                                                field(
                                                                                    default=None
                                                                                ),
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "keep_query",
                                                                    bool,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "path",
                                                                    make_dataclass(
                                                                        "path",
                                                                        [
                                                                            (
                                                                                "type",
                                                                                str,
                                                                            ),
                                                                            (
                                                                                "tokens",
                                                                                List[
                                                                                    make_dataclass(
                                                                                        "tokens",
                                                                                        [
                                                                                            (
                                                                                                "type",
                                                                                                str,
                                                                                            ),
                                                                                            (
                                                                                                "end_index",
                                                                                                int,
                                                                                                field(
                                                                                                    default=None
                                                                                                ),
                                                                                            ),
                                                                                            (
                                                                                                "start_index",
                                                                                                int,
                                                                                                field(
                                                                                                    default=None
                                                                                                ),
                                                                                            ),
                                                                                            (
                                                                                                "str_value",
                                                                                                str,
                                                                                                field(
                                                                                                    default=None
                                                                                                ),
                                                                                            ),
                                                                                        ],
                                                                                    )
                                                                                ],
                                                                                field(
                                                                                    default=None
                                                                                ),
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "port",
                                                                    int,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "status_code",
                                                                    str,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        ),
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "status_code",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                    ("type", str, field(default=None)),
                                                ],
                                            ),
                                        ),
                                        (
                                            "explicit_tracking",
                                            bool,
                                            field(default=None),
                                        ),
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
                                                    (
                                                        "burst_sz",
                                                        int,
                                                        field(default=None),
                                                    ),
                                                    ("name", str, field(default=None)),
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
                            "uri_failed_requests_rate_limit",
                            make_dataclass(
                                "uri_failed_requests_rate_limit",
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
                                                            (
                                                                "file_length",
                                                                int,
                                                                field(default=None),
                                                            ),
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
                                                            (
                                                                "add_string",
                                                                str,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "keep_query",
                                                                bool,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "port",
                                                                int,
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "status_code",
                                                                str,
                                                                field(default=None),
                                                            ),
                                                        ],
                                                    ),
                                                    field(default=None),
                                                ),
                                                (
                                                    "status_code",
                                                    str,
                                                    field(default=None),
                                                ),
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
                            ),
                            field(default=None),
                        ),
                        (
                            "uri_requests_rate_limit",
                            make_dataclass(
                                "uri_requests_rate_limit",
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
                                                            (
                                                                "file_length",
                                                                int,
                                                                field(default=None),
                                                            ),
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
                                                            (
                                                                "add_string",
                                                                str,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "keep_query",
                                                                bool,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "port",
                                                                int,
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "status_code",
                                                                str,
                                                                field(default=None),
                                                            ),
                                                        ],
                                                    ),
                                                    field(default=None),
                                                ),
                                                (
                                                    "status_code",
                                                    str,
                                                    field(default=None),
                                                ),
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
                            ),
                            field(default=None),
                        ),
                        (
                            "uri_scanners_requests_rate_limit",
                            make_dataclass(
                                "uri_scanners_requests_rate_limit",
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
                                                            (
                                                                "file_length",
                                                                int,
                                                                field(default=None),
                                                            ),
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
                                                            (
                                                                "add_string",
                                                                str,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "keep_query",
                                                                bool,
                                                                field(default=None),
                                                            ),
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
                                                                                        (
                                                                                            "type",
                                                                                            str,
                                                                                        ),
                                                                                        (
                                                                                            "end_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "start_index",
                                                                                            int,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                        (
                                                                                            "str_value",
                                                                                            str,
                                                                                            field(
                                                                                                default=None
                                                                                            ),
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ],
                                                                            field(
                                                                                default=None
                                                                            ),
                                                                        ),
                                                                    ],
                                                                ),
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "port",
                                                                int,
                                                                field(default=None),
                                                            ),
                                                            (
                                                                "status_code",
                                                                str,
                                                                field(default=None),
                                                            ),
                                                        ],
                                                    ),
                                                    field(default=None),
                                                ),
                                                (
                                                    "status_code",
                                                    str,
                                                    field(default=None),
                                                ),
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
                            ),
                            field(default=None),
                        ),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    http_profile: make_dataclass(
        "http_profile",
        [
            ("allow_dots_in_header_name", bool, field(default=None)),
            (
                "cache_config",
                make_dataclass(
                    "cache_config",
                    [
                        ("age_header", bool, field(default=None)),
                        ("aggressive", bool, field(default=None)),
                        ("date_header", bool, field(default=None)),
                        ("default_expire", int, field(default=None)),
                        ("enabled", bool, field(default=None)),
                        ("heuristic_expire", bool, field(default=None)),
                        ("ignore_request_cache_control", bool, field(default=None)),
                        ("max_cache_size", int, field(default=None)),
                        ("max_object_size", int, field(default=None)),
                        ("mime_types_block_group_refs", List[str], field(default=None)),
                        ("mime_types_block_lists", List[str], field(default=None)),
                        ("mime_types_group_refs", List[str], field(default=None)),
                        ("mime_types_list", List[str], field(default=None)),
                        ("min_object_size", int, field(default=None)),
                        ("query_cacheable", bool, field(default=None)),
                        (
                            "uri_non_cacheable",
                            make_dataclass(
                                "uri_non_cacheable",
                                [
                                    ("match_criteria", str),
                                    ("match_case", str, field(default=None)),
                                    ("match_decoded_string", bool, field(default=None)),
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
                        ("xcache_header", bool, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("client_body_timeout", int, field(default=None)),
            ("client_header_timeout", int, field(default=None)),
            ("client_max_body_size", int, field(default=None)),
            ("client_max_header_size", int, field(default=None)),
            ("client_max_request_size", int, field(default=None)),
            ("collect_client_tls_fingerprint", bool, field(default=None)),
            (
                "compression_profile",
                make_dataclass(
                    "compression_profile",
                    [
                        ("compression", bool),
                        ("remove_accept_encoding_header", bool),
                        ("type", str),
                        ("buf_num", int, field(default=None)),
                        ("buf_size", int, field(default=None)),
                        ("compressible_content_ref", str, field(default=None)),
                        (
                            "filter",
                            List[
                                make_dataclass(
                                    "filter",
                                    [
                                        ("index", int),
                                        ("level", str),
                                        ("name", str),
                                        ("devices_ref", str, field(default=None)),
                                        (
                                            "ip_addr_prefixes",
                                            List[
                                                make_dataclass(
                                                    "ip_addr_prefixes",
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
                                            "ip_addr_ranges",
                                            List[
                                                make_dataclass(
                                                    "ip_addr_ranges",
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
                                        (
                                            "ip_addrs",
                                            List[
                                                make_dataclass(
                                                    "ip_addrs",
                                                    [("addr", str), ("type", str)],
                                                )
                                            ],
                                            field(default=None),
                                        ),
                                        ("ip_addrs_ref", str, field(default=None)),
                                        ("match", str, field(default=None)),
                                        ("user_agent", List[str], field(default=None)),
                                    ],
                                )
                            ],
                            field(default=None),
                        ),
                        ("hash_size", int, field(default=None)),
                        ("level_aggressive", int, field(default=None)),
                        ("level_normal", int, field(default=None)),
                        ("max_low_rtt", int, field(default=None)),
                        ("min_high_rtt", int, field(default=None)),
                        ("min_length", int, field(default=None)),
                        ("mobile_str_ref", str, field(default=None)),
                        ("window_size", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("connection_multiplexing_enabled", bool, field(default=None)),
            ("detect_ntlm_app", bool, field(default=None)),
            ("disable_keepalive_posts_msie6", bool, field(default=None)),
            ("disable_sni_hostname_check", bool, field(default=None)),
            ("enable_chunk_merge", bool, field(default=None)),
            ("enable_fire_and_forget", bool, field(default=None)),
            ("enable_request_body_buffering", bool, field(default=None)),
            ("enable_request_body_metrics", bool, field(default=None)),
            ("fwd_close_hdr_for_bound_connections", bool, field(default=None)),
            ("hsts_enabled", bool, field(default=None)),
            ("hsts_max_age", int, field(default=None)),
            ("hsts_subdomains_enabled", bool, field(default=None)),
            (
                "http2_profile",
                make_dataclass(
                    "http2_profile",
                    [
                        ("enable_http2_server_push", bool, field(default=None)),
                        ("http2_initial_window_size", int, field(default=None)),
                        (
                            "max_http2_concurrent_pushes_per_connection",
                            int,
                            field(default=None),
                        ),
                        (
                            "max_http2_concurrent_streams_per_connection",
                            int,
                            field(default=None),
                        ),
                        (
                            "max_http2_control_frames_per_connection",
                            int,
                            field(default=None),
                        ),
                        (
                            "max_http2_empty_data_frames_per_connection",
                            int,
                            field(default=None),
                        ),
                        ("max_http2_header_field_size", int, field(default=None)),
                        (
                            "max_http2_queued_frames_to_client_per_connection",
                            int,
                            field(default=None),
                        ),
                        ("max_http2_requests_per_connection", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("http_to_https", bool, field(default=None)),
            ("http_upstream_buffer_size", int, field(default=None)),
            ("httponly_enabled", bool, field(default=None)),
            ("keepalive_header", bool, field(default=None)),
            ("keepalive_timeout", int, field(default=None)),
            ("max_bad_rps_cip", int, field(default=None)),
            ("max_bad_rps_cip_uri", int, field(default=None)),
            ("max_bad_rps_uri", int, field(default=None)),
            ("max_header_count", int, field(default=None)),
            ("max_keepalive_requests", int, field(default=None)),
            ("max_response_headers_size", int, field(default=None)),
            ("max_rps_cip", int, field(default=None)),
            ("max_rps_cip_uri", int, field(default=None)),
            ("max_rps_unknown_cip", int, field(default=None)),
            ("max_rps_unknown_uri", int, field(default=None)),
            ("max_rps_uri", int, field(default=None)),
            ("pass_through_x_accel_headers", bool, field(default=None)),
            ("pki_profile_ref", str, field(default=None)),
            ("post_accept_timeout", int, field(default=None)),
            ("reset_conn_http_on_ssl_port", bool, field(default=None)),
            ("respond_with_100_continue", bool, field(default=None)),
            ("secure_cookie_enabled", bool, field(default=None)),
            ("server_side_redirect_to_https", bool, field(default=None)),
            (
                "ssl_client_certificate_action",
                make_dataclass(
                    "ssl_client_certificate_action",
                    [
                        ("close_connection", bool, field(default=None)),
                        (
                            "headers",
                            List[
                                make_dataclass(
                                    "headers",
                                    [
                                        ("request_header", str, field(default=None)),
                                        (
                                            "request_header_value",
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
            ("ssl_client_certificate_mode", str, field(default=None)),
            (
                "true_client_ip",
                make_dataclass(
                    "true_client_ip",
                    [
                        ("direction", str, field(default=None)),
                        ("headers", List[str], field(default=None)),
                        ("index_in_header", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("use_app_keepalive_timeout", bool, field(default=None)),
            ("use_true_client_ip", bool, field(default=None)),
            ("websockets_enabled", bool, field(default=None)),
            ("x_forwarded_proto_enabled", bool, field(default=None)),
            ("xff_alternate_name", str, field(default=None)),
            ("xff_enabled", bool, field(default=None)),
            ("xff_update", str, field(default=None)),
        ],
    ) = None,
    l4_ssl_profile: make_dataclass(
        "l4_ssl_profile", [("ssl_stream_idle_timeout", int, field(default=None))]
    ) = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    preserve_client_ip: bool = None,
    preserve_client_port: bool = None,
    preserve_dest_ip_port: bool = None,
    sip_service_profile: make_dataclass(
        "sip_service_profile", [("transaction_timeout", int, field(default=None))]
    ) = None,
    tcp_app_profile: make_dataclass(
        "tcp_app_profile",
        [
            (
                "ftp_profile",
                make_dataclass(
                    "ftp_profile",
                    [
                        ("deactivate_active", bool, field(default=None)),
                        ("deactivate_passive", bool, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("pki_profile_ref", str, field(default=None)),
            ("proxy_protocol_enabled", bool, field(default=None)),
            ("proxy_protocol_version", str, field(default=None)),
            ("ssl_client_certificate_mode", str, field(default=None)),
        ],
    ) = None,
    tenant_ref: str = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:
        name(str):
            Idem name of the resource.

        type(str):
            Specifies which application layer proxy is enabled for the virtual service. Enum options - APPLICATION_PROFILE_TYPE_L4, APPLICATION_PROFILE_TYPE_HTTP, APPLICATION_PROFILE_TYPE_SYSLOG, APPLICATION_PROFILE_TYPE_DNS, APPLICATION_PROFILE_TYPE_SSL, APPLICATION_PROFILE_TYPE_SIP. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- APPLICATION_PROFILE_TYPE_L4), Basic edition(Allowed values- APPLICATION_PROFILE_TYPE_L4,APPLICATION_PROFILE_TYPE_HTTP), Enterprise with Cloud Services edition.

        resource_id(str, Optional):
            Alb.application_profile unique ID. Defaults to None.

        app_service_type(str, Optional):
            Specifies app service type for an application. Enum options - APP_SERVICE_TYPE_L7_HORIZON, APP_SERVICE_TYPE_L4_BLAST, APP_SERVICE_TYPE_L4_PCOIP, APP_SERVICE_TYPE_L4_FTP. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        cloud_config_cksum(str, Optional):
            Checksum of application profiles. Internally set by cloud connector. Field introduced in 17.2.14, 18.1.5, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        created_by(str, Optional):
            Name of the application profile creator. Field introduced in 17.2.14, 18.1.5, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        description(str, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        dns_service_profile(dict[str, Any], Optional):
            dns_service_profile. Defaults to None.

            * aaaa_empty_response (bool, Optional):
                Respond to AAAA queries with empty response when there are only IPV4 records. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * admin_email (str, Optional):
                Email address of the administrator responsible for this zone . This field is used in SOA records (rname) pertaining to all domain names specified as authoritative domain names. If not configured, the default value 'hostmaster' is used in SOA responses. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * dns_over_tcp_enabled (bool, Optional):
                Enable DNS query/response over TCP. This enables analytics for pass-through queries as well. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * dns_zones (List[dict[str, Any]], Optional):
                DNS zones hosted on this Virtual Service. Field introduced in 18.2.6. Maximum of 100 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * admin_email (str, Optional):
                    Email address of the administrator responsible for this zone. This field is used in SOA records as rname (RFC 1035). If not configured, it is inherited from the DNS service profile. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * domain_name (str):
                    Domain name authoritatively serviced by this Virtual Service. Queries for FQDNs that are sub domains of this domain and do not have any DNS record in Avi are dropped or NXDomain response sent. For domains which are present, SOA parameters are sent in answer section of response if query type is SOA. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name_server (str, Optional):
                    The primary name server for this zone. This field is used in SOA records as mname (RFC 1035). If not configured, it is inherited from the DNS service profile. If even that is not configured, the domain name is used instead. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * domain_names (List[str], Optional):
                Subdomain names serviced by this Virtual Service. These are configured as Ends-With semantics. Maximum of 100 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ecs_stripping_enabled (bool, Optional):
                Enable stripping of EDNS client subnet (ecs) option towards client if DNS service inserts ecs option in the DNS query towards upstream servers. Field introduced in 17.1.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * edns (bool, Optional):
                Enable DNS service to be aware of EDNS (Extension mechanism for DNS). EDNS extensions are parsed and shown in logs. For GSLB services, the EDNS client subnet option can be used to influence Load Balancing. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * edns_client_subnet_prefix_len (int, Optional):
                Specifies the IP address prefix length to use in the EDNS client subnet (ECS) option. When the incoming request does not have any ECS option and the prefix length is specified, an ECS option is inserted in the request passed to upstream server. If the incoming request already has an ECS option, the prefix length (and correspondingly the address) in the ECS option is updated, with the minimum of the prefix length present in the incoming and the configured prefix length, before passing the request to upstream server. Allowed values are 1-32. Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * error_response (str, Optional):
                Drop or respond to client when the DNS service encounters an error processing a client query. By default, such a request is dropped without any response, or passed through to a passthrough pool, if configured. When set to respond, an appropriate response is sent to client, e.g. NXDOMAIN response for non-existent records, empty NOERROR response for unsupported queries, etc. Enum options - DNS_ERROR_RESPONSE_ERROR, DNS_ERROR_RESPONSE_NONE. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * name_server (str, Optional):
                The <domain-name>  of the name server that was the original or primary source of data for this zone. This field is used in SOA records (mname) pertaining to all domain names specified as authoritative domain names. If not configured, domain name is used as name server in SOA response. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * negative_caching_ttl (int, Optional):
                Specifies the TTL value (in seconds) for SOA (Start of Authority) (corresponding to a authoritative domain owned by this DNS Virtual Service) record's minimum TTL served by the DNS Virtual Service. Allowed values are 0-86400. Field introduced in 17.2.4. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * num_dns_ip (int, Optional):
                Specifies the number of IP addresses returned by the DNS Service. Enter 0 to return all IP addresses. Allowed values are 1-20. Special values are 0- Return all IP addresses. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ttl (int, Optional):
                Specifies the TTL value (in seconds) for records served by DNS Service. Allowed values are 0-86400. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        dos_rl_profile(dict[str, Any], Optional):
            dos_rl_profile. Defaults to None.

            * dos_profile (dict[str, Any], Optional):
                dos_profile

                * thresh_info (List[dict[str, Any]], Optional):
                    Attack type, min and max values for DoS attack detection. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * attack (str):
                        Attack type. Enum options - LAND, SMURF, ICMP_PING_FLOOD, UNKOWN_PROTOCOL, TEARDROP, IP_FRAG_OVERRUN, IP_FRAG_TOOSMALL, IP_FRAG_FULL, IP_FRAG_INCOMPLETE, PORT_SCAN, TCP_NON_SYN_FLOOD_OLD, SYN_FLOOD, BAD_RST_FLOOD, MALFORMED_FLOOD, FAKE_SESSION, ZERO_WINDOW_STRESS, SMALL_WINDOW_STRESS, DOS_HTTP_TIMEOUT, DOS_HTTP_ERROR, DOS_HTTP_ABORT, DOS_SSL_ERROR, DOS_APP_ERROR, DOS_REQ_IP_RL_DROP, DOS_REQ_URI_RL_DROP, DOS_REQ_URI_SCAN_BAD_RL_DROP, DOS_REQ_URI_SCAN_UNKNOWN_RL_DROP, DOS_REQ_IP_URI_RL_DROP, DOS_CONN_IP_RL_DROP, DOS_SLOW_URL, TCP_NON_SYN_FLOOD, DOS_REQ_CIP_SCAN_BAD_RL_DROP, DOS_REQ_CIP_SCAN_UNKNOWN_RL_DROP, DOS_REQ_IP_RL_DROP_BAD, DOS_REQ_URI_RL_DROP_BAD, DOS_REQ_IP_URI_RL_DROP_BAD, POLICY_DROPS, DOS_CONN_RL_DROP, DOS_REQ_RL_DROP, DOS_REQ_HDR_RL_DROP, DOS_REQ_CUSTOM_RL_DROP, DNS_ATTACK_REFLECTION, DNS_ATTACK_AMPLIFICATION_EGRESS, TCP_SLOW_AND_LOW, DNS_ATTACK_NXDOMAIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * max_value (int):
                        Maximum number of packets or connections or requests in a given interval of time to be deemed as attack. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * min_value (int):
                        Minimum number of packets or connections or requests in a given interval of time to be deemed as attack. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * thresh_period (int):
                    Timer value in seconds to collect DoS attack metrics based on threshold on the Service Engine for this Virtual Service. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * rl_profile (dict[str, Any], Optional):
                rl_profile

                * client_ip_connections_rate_limit (dict[str, Any], Optional):
                    client_ip_connections_rate_limit

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

                * client_ip_failed_requests_rate_limit (dict[str, Any], Optional):
                    client_ip_failed_requests_rate_limit

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

                * client_ip_requests_rate_limit (dict[str, Any], Optional):
                    client_ip_requests_rate_limit

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

                * client_ip_scanners_requests_rate_limit (dict[str, Any], Optional):
                    client_ip_scanners_requests_rate_limit

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

                * client_ip_to_uri_failed_requests_rate_limit (dict[str, Any], Optional):
                    client_ip_to_uri_failed_requests_rate_limit

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

                * client_ip_to_uri_requests_rate_limit (dict[str, Any], Optional):
                    client_ip_to_uri_requests_rate_limit

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

                * custom_requests_rate_limit (dict[str, Any], Optional):
                    custom_requests_rate_limit

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

                * http_header_rate_limits (List[dict[str, Any]], Optional):
                    Rate Limit all HTTP requests from all client IP addresses that contain any single HTTP header value. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

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

                * uri_failed_requests_rate_limit (dict[str, Any], Optional):
                    uri_failed_requests_rate_limit

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

                * uri_requests_rate_limit (dict[str, Any], Optional):
                    uri_requests_rate_limit

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

                * uri_scanners_requests_rate_limit (dict[str, Any], Optional):
                    uri_scanners_requests_rate_limit

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

        http_profile(dict[str, Any], Optional):
            http_profile. Defaults to None.

            * allow_dots_in_header_name (bool, Optional):
                Allow use of dot (.) in HTTP header names, for instance Header.app.special  PickAppVersionX. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * cache_config (dict[str, Any], Optional):
                cache_config

                * age_header (bool, Optional):
                    Add an Age header to content served from cache, which indicates to the client the number of seconds the object has been in the cache. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * aggressive (bool, Optional):
                    Enable/disable caching objects without Cache-Control headers. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * date_header (bool, Optional):
                    If a Date header was not added by the server, add a Date header to the object served from cache.  This indicates to the client when the object was originally sent by the server to the cache. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * default_expire (int, Optional):
                    Default expiration time of cache objects received from the server without a Cache-Control expiration header.  This value may be overwritten by the Heuristic Expire setting. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * enabled (bool, Optional):
                    Enable/disable HTTP object caching.When enabling caching for the first time, SE Group app_cache_percent must be set to allocate shared memory required for caching (A service engine restart is needed after setting/resetting the SE group value). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * heuristic_expire (bool, Optional):
                    If a response object from the server does not include the Cache-Control header, but does include a Last-Modified header, the system will use this time to calculate the Cache-Control expiration.  If unable to solicit an Last-Modified header, then the system will fall back to the Cache Expire Time value. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ignore_request_cache_control (bool, Optional):
                    Ignore client's cache control headers when fetching or storing from and to the cache. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_cache_size (int, Optional):
                    Max size, in bytes, of the cache.  The default, zero, indicates auto configuration. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_object_size (int, Optional):
                    Maximum size of an object to store in the cache. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mime_types_block_group_refs (List[str], Optional):
                    Blocklist string group of non-cacheable mime types. It is a reference to an object of type StringGroup. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * mime_types_block_lists (List[str], Optional):
                    Blocklist of non-cacheable mime types. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * mime_types_group_refs (List[str], Optional):
                    Allowlist string group of cacheable mime types. If both Cacheable Mime Types string list and string group are empty, this defaults to */*. It is a reference to an object of type StringGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mime_types_list (List[str], Optional):
                    Allowlist of cacheable mime types. If both Cacheable Mime Types string list and string group are empty, this defaults to */*. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * min_object_size (int, Optional):
                    Minimum size of an object to store in the cache. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * query_cacheable (bool, Optional):
                    Allow caching of objects whose URI included a query argument.  When disabled, these objects are not cached.  When enabled, the request must match the URI query to be considered a hit. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * uri_non_cacheable (dict[str, Any], Optional):
                    uri_non_cacheable

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

                * xcache_header (bool, Optional):
                    Add an X-Cache header to content served from cache, which indicates to the client that the object was served from an intermediate cache. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * client_body_timeout (int, Optional):
                The maximum length of time allowed between consecutive read operations for a client request body. The value '0' specifies no timeout. This setting generally impacts the length of time allowed for a client to send a POST. Allowed values are 0-100000000. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 30000), Basic edition with any value, Enterprise with Cloud Services edition.

            * client_header_timeout (int, Optional):
                The maximum length of time allowed for a client to transmit an entire request header. This helps mitigate various forms of SlowLoris attacks. Allowed values are 10-100000000. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 10000), Basic edition(Allowed values- 10000), Enterprise with Cloud Services edition.

            * client_max_body_size (int, Optional):
                Maximum size for the client request body.  This limits the size of the client data that can be uploaded/posted as part of a single HTTP Request.  Default 0 => Unlimited. Unit is KB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * client_max_header_size (int, Optional):
                Maximum size in Kbytes of a single HTTP header in the client request. Allowed values are 1-64. Unit is KB. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 12), Basic, Enterprise with Cloud Services edition.

            * client_max_request_size (int, Optional):
                Maximum size in Kbytes of all the client HTTP request headers.This value can be overriden by client_max_header_size if that is larger. Allowed values are 1-256. Unit is KB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * collect_client_tls_fingerprint (bool, Optional):
                If enabled, the client's TLS fingerprint will be collected and included in the Application Log. For Virtual Services with Bot Detection enabled, TLS fingerprints are always computed if 'use_tls_fingerprint' is enabled in the Bot Detection Policy's User-Agent detection component. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * compression_profile (dict[str, Any], Optional):
                compression_profile

                * buf_num (int, Optional):
                    Number of buffers to use for compression output. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * buf_size (int, Optional):
                    Size of each buffer used for compression output, this should ideally be a multiple of pagesize. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * compressible_content_ref (str, Optional):
                    Compress only content types listed in this string group. Content types not present in this list are not compressed. It is a reference to an object of type StringGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * compression (bool):
                    Compress HTTP response content if it wasn't already compressed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * filter (List[dict[str, Any]], Optional):
                    Custom filters used when auto compression is not selected. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * devices_ref (str, Optional):
                         It is a reference to an object of type StringGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * index (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * ip_addr_prefixes (List[dict[str, Any]], Optional):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * ip_addr (dict[str, Any]):
                            ip_addr

                            * addr (str):
                                IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * type (str):
                                 Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * mask (int):
                             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * ip_addr_ranges (List[dict[str, Any]], Optional):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

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

                    * ip_addrs (List[dict[str, Any]], Optional):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * ip_addrs_ref (str, Optional):
                         It is a reference to an object of type IpAddrGroup. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * level (str):
                         Enum options - AGGRESSIVE_COMPRESSION, NORMAL_COMPRESSION, NO_COMPRESSION. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * match (str, Optional):
                        Whether to apply Filter when group criteria is matched or not. Enum options - IS_IN, IS_NOT_IN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * name (str):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * user_agent (List[str], Optional):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * hash_size (int, Optional):
                    hash size used by compression, rounded to the last power of 2. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * level_aggressive (int, Optional):
                    Level of compression to apply on content selected for aggressive compression. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * level_normal (int, Optional):
                    Level of compression to apply on content selected for normal compression. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * max_low_rtt (int, Optional):
                    If client RTT is higher than this threshold, enable normal compression on the response. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * min_high_rtt (int, Optional):
                    If client RTT is higher than this threshold, enable aggressive compression on the response.  . Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * min_length (int, Optional):
                    Minimum response content length to enable compression. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * mobile_str_ref (str, Optional):
                    Values that identify mobile browsers in order to enable aggressive compression. It is a reference to an object of type StringGroup. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * remove_accept_encoding_header (bool):
                    Offload compression from the servers to AVI. Saves compute cycles on the servers. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                    Compress content automatically or add custom filters to define compressible content and compression levels. Enum options - AUTO_COMPRESSION, CUSTOM_COMPRESSION. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * window_size (int, Optional):
                    window size used by compression, rounded to the last power of 2. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * connection_multiplexing_enabled (bool, Optional):
                Allows HTTP requests, not just TCP connections, to be load balanced across servers.  Proxied TCP connections to servers may be reused by multiple clients to improve performance. Not compatible with Preserve Client IP. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * detect_ntlm_app (bool, Optional):
                Detect NTLM apps based on the HTTP Response from the server. Once detected, connection multiplexing will be disabled for that connection. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

            * disable_keepalive_posts_msie6 (bool, Optional):
                Disable keep-alive client side connections for older browsers based off MS Internet Explorer 6.0 (MSIE6). For some applications, this might break NTLM authentication for older clients based off MSIE6. For such applications, set this option to false to allow keep-alive connections. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- true), Basic edition(Allowed values- true), Enterprise with Cloud Services edition.

            * disable_sni_hostname_check (bool, Optional):
                Disable strict check between TLS servername and HTTP Host name. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enable_chunk_merge (bool, Optional):
                Enable chunk body merge for chunked transfer encoding response. Field introduced in 18.2.7. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enable_fire_and_forget (bool, Optional):
                Enable support for fire and forget feature. If enabled, request from client is forwarded to server even if client prematurely closes the connection. Field introduced in 17.2.4. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * enable_request_body_buffering (bool, Optional):
                Enable request body buffering for POST requests. If enabled, max buffer size is set to lower of 32M or the value (non-zero) configured in client_max_body_size. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enable_request_body_metrics (bool, Optional):
                Enable HTTP request body metrics. If enabled, requests from clients are parsed and relevant statistics about them are gathered. Currently, it processes HTTP POST requests with Content-Type application/x-www-form-urlencoded or multipart/form-data, and adds the number of detected parameters to the l7_client.http_params_count. This is an experimental feature and it may have performance impact. Use it when detailed information about the number of HTTP POST parameters is needed, e.g. for WAF sizing. Field introduced in 18.1.5, 18.2.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * fwd_close_hdr_for_bound_connections (bool, Optional):
                Forward the Connection  Close header coming from backend server to the client if connection-switching is enabled, i.e. front-end and backend connections are bound together. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * hsts_enabled (bool, Optional):
                Inserts HTTP Strict-Transport-Security header in the HTTPS response.  HSTS can help mitigate man-in-the-middle attacks by telling browsers that support HSTS that they should only access this site via HTTPS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * hsts_max_age (int, Optional):
                Number of days for which the client should regard this virtual service as a known HSTS host. Allowed values are 0-10000. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 365), Basic edition(Allowed values- 365), Enterprise with Cloud Services edition.

            * hsts_subdomains_enabled (bool, Optional):
                Insert the 'includeSubdomains' directive in the HTTP Strict-Transport-Security header. Adding the includeSubdomains directive signals the User-Agent that the HSTS Policy applies to this HSTS Host as well as any subdomains of the host's domain name. Field introduced in 17.2.13, 18.1.4, 18.2.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Special default for Essentials edition is false, Basic edition is false, Enterprise is True.

            * http2_profile (dict[str, Any], Optional):
                http2_profile

                * enable_http2_server_push (bool, Optional):
                    Enables automatic conversion of preload links specified in the 'Link' response header fields into Server push requests. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * http2_initial_window_size (int, Optional):
                    The initial flow control window size in KB for HTTP/2 streams. Allowed values are 64-32768. Field introduced in 18.2.10, 20.1.1. Unit is KB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_http2_concurrent_pushes_per_connection (int, Optional):
                    Maximum number of concurrent push streams over a client side HTTP/2 connection. Allowed values are 1-256. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * max_http2_concurrent_streams_per_connection (int, Optional):
                    Maximum number of concurrent streams over a client side HTTP/2 connection. Allowed values are 1-256. Field introduced in 18.2.10, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_http2_control_frames_per_connection (int, Optional):
                    Maximum number of control frames that client can send over an HTTP/2 connection. '0' means unlimited. Allowed values are 0-10000. Special values are 0- Unlimited control frames on a client side HTTP/2 connection. Field introduced in 18.2.10, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_http2_empty_data_frames_per_connection (int, Optional):
                    Maximum number of empty data frames that client can send over an HTTP/2 connection. '0' means unlimited. Allowed values are 0-10000. Special values are 0- Unlimited empty data frames over a client side HTTP/2 connection. Field introduced in 18.2.10, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_http2_header_field_size (int, Optional):
                    Maximum size in bytes of the compressed request header field. The limit applies equally to both name and value. Allowed values are 1-8192. Field introduced in 18.2.10, 20.1.1. Unit is BYTES. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_http2_queued_frames_to_client_per_connection (int, Optional):
                    Maximum number of frames that can be queued waiting to be sent over a client side HTTP/2 connection at any given time. '0' means unlimited. Allowed values are 0-10000. Special values are 0- Unlimited frames can be queued on a client side HTTP/2 connection. Field introduced in 18.2.10, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_http2_requests_per_connection (int, Optional):
                    Maximum number of requests over a client side HTTP/2 connection. Allowed values are 0-10000. Special values are 0- Unlimited requests on a client side HTTP/2 connection. Field introduced in 18.2.10, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_to_https (bool, Optional):
                Client requests received via HTTP will be redirected to HTTPS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic, Enterprise with Cloud Services edition.

            * http_upstream_buffer_size (int, Optional):
                Size of HTTP buffer in kB. Allowed values are 1-256. Special values are 0- Auto compute the size of buffer. Field introduced in 20.1.1. Unit is KB. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition.

            * httponly_enabled (bool, Optional):
                Mark HTTP cookies as HTTPonly.  This helps mitigate cross site scripting attacks as browsers will not allow these cookies to be read by third parties, such as javascript. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * keepalive_header (bool, Optional):
                Send HTTP 'Keep-Alive' header to the client. By default, the timeout specified in the 'Keep-Alive Timeout' field will be used unless the 'Use App Keepalive Timeout' flag is set, in which case the timeout sent by the application will be honored. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * keepalive_timeout (int, Optional):
                The max idle time allowed between HTTP requests over a Keep-alive connection. Allowed values are 10-100000000. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 30000), Basic, Enterprise with Cloud Services edition.

            * max_bad_rps_cip (int, Optional):
                Maximum bad requests per second per client IP. Allowed values are 10-1000. Special values are 0- unlimited. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_bad_rps_cip_uri (int, Optional):
                Maximum bad requests per second per client IP and URI. Allowed values are 10-1000. Special values are 0- unlimited. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_bad_rps_uri (int, Optional):
                Maximum bad requests per second per URI. Allowed values are 10-1000. Special values are 0- unlimited. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_header_count (int, Optional):
                Maximum number of headers allowed in HTTP request and response. Allowed values are 0-4096. Special values are 0- unlimited headers in request and response. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Special default for Essentials edition is 0, Basic edition is 0, Enterprise is 256.

            * max_keepalive_requests (int, Optional):
                The max number of HTTP requests that can be sent over a Keep-Alive connection. '0' means unlimited. Allowed values are 0-1000000. Special values are 0- Unlimited requests on a connection. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 100), Basic edition(Allowed values- 100), Enterprise with Cloud Services edition.

            * max_response_headers_size (int, Optional):
                Maximum size in Kbytes of all the HTTP response headers. Allowed values are 1-256. Unit is KB. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 48), Basic, Enterprise with Cloud Services edition.

            * max_rps_cip (int, Optional):
                Maximum requests per second per client IP. Allowed values are 10-1000. Special values are 0- unlimited. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_rps_cip_uri (int, Optional):
                Maximum requests per second per client IP and URI. Allowed values are 10-1000. Special values are 0- unlimited. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_rps_unknown_cip (int, Optional):
                Maximum unknown client IPs per second. Allowed values are 10-1000. Special values are 0- unlimited. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_rps_unknown_uri (int, Optional):
                Maximum unknown URIs per second. Allowed values are 10-1000. Special values are 0- unlimited. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_rps_uri (int, Optional):
                Maximum requests per second per URI. Allowed values are 10-1000. Special values are 0- unlimited. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * pass_through_x_accel_headers (bool, Optional):
                Pass through X-ACCEL headers. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * pki_profile_ref (str, Optional):
                Select the PKI profile to be associated with the Virtual Service. This profile defines the Certificate Authority and Revocation List. It is a reference to an object of type PKIProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * post_accept_timeout (int, Optional):
                The max allowed length of time between a client establishing a TCP connection and Avi receives the first byte of the client's HTTP request. Allowed values are 10-100000000. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 30000), Basic edition(Allowed values- 30000), Enterprise with Cloud Services edition.

            * reset_conn_http_on_ssl_port (bool, Optional):
                If enabled, an HTTP request on an SSL port will result in connection close instead of a 400 response. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * respond_with_100_continue (bool, Optional):
                Avi will respond with 100-Continue response if Expect  100-Continue header received from client. Field introduced in 17.2.8. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * secure_cookie_enabled (bool, Optional):
                Mark server cookies with the 'Secure' attribute.  Client browsers will not send a cookie marked as secure over an unencrypted connection.  If Avi is terminating SSL from clients and passing it as HTTP to the server, the server may return cookies without the secure flag set. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * server_side_redirect_to_https (bool, Optional):
                When terminating client SSL sessions at Avi, servers may incorrectly send redirect to clients as HTTP.  This option will rewrite the server's redirect responses for this virtual service from HTTP to HTTPS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * ssl_client_certificate_action (dict[str, Any], Optional):
                ssl_client_certificate_action

                * close_connection (bool, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * headers (List[dict[str, Any]], Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * request_header (str, Optional):
                        If this header exists, reset the connection. If the ssl variable is specified, add a header with this value. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * request_header_value (str, Optional):
                        Set the request header with the value as indicated by this SSL variable. Eg. send the whole certificate in PEM format. Enum options - HTTP_POLICY_VAR_CLIENT_IP, HTTP_POLICY_VAR_VS_PORT, HTTP_POLICY_VAR_VS_IP, HTTP_POLICY_VAR_HTTP_HDR, HTTP_POLICY_VAR_SSL_CLIENT_FINGERPRINT, HTTP_POLICY_VAR_SSL_CLIENT_SERIAL, HTTP_POLICY_VAR_SSL_CLIENT_ISSUER, HTTP_POLICY_VAR_SSL_CLIENT_SUBJECT, HTTP_POLICY_VAR_SSL_CLIENT_RAW, HTTP_POLICY_VAR_SSL_PROTOCOL, HTTP_POLICY_VAR_SSL_SERVER_NAME, HTTP_POLICY_VAR_USER_NAME, HTTP_POLICY_VAR_SSL_CIPHER, HTTP_POLICY_VAR_REQUEST_ID, HTTP_POLICY_VAR_SSL_CLIENT_VERSION, HTTP_POLICY_VAR_SSL_CLIENT_SIGALG, HTTP_POLICY_VAR_SSL_CLIENT_NOTVALIDBEFORE, HTTP_POLICY_VAR_SSL_CLIENT_NOTVALIDAFTER, HTTP_POLICY_VAR_SSL_CLIENT_ESCAPED, HTTP_POLICY_VAR_SOURCE_IP. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ssl_client_certificate_mode (str, Optional):
                Specifies whether the client side verification is set to none, request or require. Enum options - SSL_CLIENT_CERTIFICATE_NONE, SSL_CLIENT_CERTIFICATE_REQUEST, SSL_CLIENT_CERTIFICATE_REQUIRE. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- SSL_CLIENT_CERTIFICATE_NONE,SSL_CLIENT_CERTIFICATE_REQUIRE), Basic edition(Allowed values- SSL_CLIENT_CERTIFICATE_NONE,SSL_CLIENT_CERTIFICATE_REQUIRE), Enterprise with Cloud Services edition.

            * true_client_ip (dict[str, Any], Optional):
                true_client_ip

                * direction (str, Optional):
                    Denotes the end from which to count the IPs in the specified header value. Enum options - LEFT, RIGHT. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * headers (List[str], Optional):
                    Headers to derive client IP from. The header value needs to be a comma-separated list of IP addresses. If none specified and use_true_client_ip is set to true, it will use X-Forwarded-For header, if present. Field introduced in 21.1.3. Maximum of 1 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * index_in_header (int, Optional):
                    Position in the configured direction, in the specified header's value, to be used to set true client IP. If the value is greater than the number of IP addresses in the header, then the last IP address in the configured direction in the header will be used. Allowed values are 1-1000. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * use_app_keepalive_timeout (bool, Optional):
                Use 'Keep-Alive' header timeout sent by application instead of sending the HTTP Keep-Alive Timeout. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * use_true_client_ip (bool, Optional):
                Detect client IP from user specified header. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * websockets_enabled (bool, Optional):
                Enable Websockets proxy for traffic from clients to the virtual service. Connections to this VS start in HTTP mode. If the client requests an Upgrade to Websockets, and the server responds back with success, then the connection is upgraded to WebSockets mode. . Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * x_forwarded_proto_enabled (bool, Optional):
                Insert an X-Forwarded-Proto header in the request sent to the server.  When the client connects via SSL, Avi terminates the SSL, and then forwards the requests to the servers via HTTP, so the servers can determine the original protocol via this header.  In this example, the value will be 'https'. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * xff_alternate_name (str, Optional):
                Provide a custom name for the X-Forwarded-For header sent to the servers. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * xff_enabled (bool, Optional):
                The client's original IP address is inserted into an HTTP request header sent to the server.  Servers may use this address for logging or other purposes, rather than Avi's source NAT address used in the Avi to server IP connection. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * xff_update (str, Optional):
                Configure how incoming X-Forwarded-For headers from the client are handled. Enum options - REPLACE_XFF_HEADERS, APPEND_TO_THE_XFF_HEADER, ADD_NEW_XFF_HEADER. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        l4_ssl_profile(dict[str, Any], Optional):
            l4_ssl_profile. Defaults to None.

            * ssl_stream_idle_timeout (int, Optional):
                L4 stream idle connection timeout in seconds. Allowed values are 60-86400. Field introduced in 22.1.2. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        preserve_client_ip(bool, Optional):
            Specifies if client IP needs to be preserved for backend connection. Not compatible with Connection Multiplexing. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        preserve_client_port(bool, Optional):
            Specifies if we need to preserve client port while preserving client IP for backend connections. Field introduced in 17.2.7. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        preserve_dest_ip_port(bool, Optional):
            Specifies if destination IP and port needs to be preserved for backend connection. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        sip_service_profile(dict[str, Any], Optional):
            sip_service_profile. Defaults to None.

            * transaction_timeout (int, Optional):
                SIP transaction timeout in seconds. Allowed values are 2-512. Field introduced in 17.2.8, 18.1.3, 18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        tcp_app_profile(dict[str, Any], Optional):
            tcp_app_profile. Defaults to None.

            * ftp_profile (dict[str, Any], Optional):
                ftp_profile

                * deactivate_active (bool, Optional):
                    Deactivate active FTP mode. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * deactivate_passive (bool, Optional):
                    Deactivate passive FTP mode. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * pki_profile_ref (str, Optional):
                Select the PKI profile to be associated with the Virtual Service. This profile defines the Certificate Authority and Revocation List. It is a reference to an object of type PKIProfile. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * proxy_protocol_enabled (bool, Optional):
                Enable/Disable the usage of proxy protocol to convey client connection information to the back-end servers.  Valid only for L4 application profiles and TCP proxy. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * proxy_protocol_version (str, Optional):
                Version of proxy protocol to be used to convey client connection information to the back-end servers. Enum options - PROXY_PROTOCOL_VERSION_1, PROXY_PROTOCOL_VERSION_2. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- PROXY_PROTOCOL_VERSION_1), Basic edition(Allowed values- PROXY_PROTOCOL_VERSION_1), Enterprise with Cloud Services edition.

            * ssl_client_certificate_mode (str, Optional):
                Specifies whether the client side verification is set to none, request or require. Enum options - SSL_CLIENT_CERTIFICATE_NONE, SSL_CLIENT_CERTIFICATE_REQUEST, SSL_CLIENT_CERTIFICATE_REQUIRE. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- SSL_CLIENT_CERTIFICATE_NONE), Basic edition(Allowed values- SSL_CLIENT_CERTIFICATE_NONE), Enterprise with Cloud Services edition.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


          idem_test_nsx_alb.alb.application_profile_is_present:
              nsx_alb.nsx_alb.alb.application_profile.present:
              - app_service_type: string
              - cloud_config_cksum: string
              - configpb_attributes:
                  version: int
              - created_by: string
              - description: string
              - dns_service_profile:
                  aaaa_empty_response: bool
                  admin_email: string
                  dns_over_tcp_enabled: bool
                  dns_zones:
                  - admin_email: string
                    domain_name: string
                    name_server: string
                  domain_names:
                  - value
                  ecs_stripping_enabled: bool
                  edns: bool
                  edns_client_subnet_prefix_len: int
                  error_response: string
                  name_server: string
                  negative_caching_ttl: int
                  num_dns_ip: int
                  ttl: int
              - dos_rl_profile:
                  dos_profile:
                    thresh_info:
                    - attack: string
                      max_value: int
                      min_value: int
                    thresh_period: int
                  rl_profile:
                    client_ip_connections_rate_limit:
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
                    client_ip_failed_requests_rate_limit:
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
                    client_ip_requests_rate_limit:
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
                    client_ip_scanners_requests_rate_limit:
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
                    client_ip_to_uri_failed_requests_rate_limit:
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
                    client_ip_to_uri_requests_rate_limit:
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
                    custom_requests_rate_limit:
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
                    http_header_rate_limits:
                    - action:
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
                    uri_failed_requests_rate_limit:
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
                    uri_requests_rate_limit:
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
                    uri_scanners_requests_rate_limit:
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
              - http_profile:
                  allow_dots_in_header_name: bool
                  cache_config:
                    age_header: bool
                    aggressive: bool
                    date_header: bool
                    default_expire: int
                    enabled: bool
                    heuristic_expire: bool
                    ignore_request_cache_control: bool
                    max_cache_size: int
                    max_object_size: int
                    mime_types_block_group_refs:
                    - value
                    mime_types_block_lists:
                    - value
                    mime_types_group_refs:
                    - value
                    mime_types_list:
                    - value
                    min_object_size: int
                    query_cacheable: bool
                    uri_non_cacheable:
                      match_case: string
                      match_criteria: string
                      match_decoded_string: bool
                      match_str:
                      - value
                      string_group_refs:
                      - value
                    xcache_header: bool
                  client_body_timeout: int
                  client_header_timeout: int
                  client_max_body_size: int
                  client_max_header_size: int
                  client_max_request_size: int
                  collect_client_tls_fingerprint: bool
                  compression_profile:
                    buf_num: int
                    buf_size: int
                    compressible_content_ref: string
                    compression: bool
                    filter_:
                    - devices_ref: string
                      index: int
                      ip_addr_prefixes:
                      - ip_addr:
                          addr: string
                          type_: string
                        mask: int
                      ip_addr_ranges:
                      - begin:
                          addr: string
                          type_: string
                        end:
                          addr: string
                          type_: string
                      ip_addrs:
                      - addr: string
                        type_: string
                      ip_addrs_ref: string
                      level: string
                      match: string
                      name: string
                      user_agent:
                      - value
                    hash_size: int
                    level_aggressive: int
                    level_normal: int
                    max_low_rtt: int
                    min_high_rtt: int
                    min_length: int
                    mobile_str_ref: string
                    remove_accept_encoding_header: bool
                    type_: string
                    window_size: int
                  connection_multiplexing_enabled: bool
                  detect_ntlm_app: bool
                  disable_keepalive_posts_msie6: bool
                  disable_sni_hostname_check: bool
                  enable_chunk_merge: bool
                  enable_fire_and_forget: bool
                  enable_request_body_buffering: bool
                  enable_request_body_metrics: bool
                  fwd_close_hdr_for_bound_connections: bool
                  hsts_enabled: bool
                  hsts_max_age: int
                  hsts_subdomains_enabled: bool
                  http2_profile:
                    enable_http2_server_push: bool
                    http2_initial_window_size: int
                    max_http2_concurrent_pushes_per_connection: int
                    max_http2_concurrent_streams_per_connection: int
                    max_http2_control_frames_per_connection: int
                    max_http2_empty_data_frames_per_connection: int
                    max_http2_header_field_size: int
                    max_http2_queued_frames_to_client_per_connection: int
                    max_http2_requests_per_connection: int
                  http_to_https: bool
                  http_upstream_buffer_size: int
                  httponly_enabled: bool
                  keepalive_header: bool
                  keepalive_timeout: int
                  max_bad_rps_cip: int
                  max_bad_rps_cip_uri: int
                  max_bad_rps_uri: int
                  max_header_count: int
                  max_keepalive_requests: int
                  max_response_headers_size: int
                  max_rps_cip: int
                  max_rps_cip_uri: int
                  max_rps_unknown_cip: int
                  max_rps_unknown_uri: int
                  max_rps_uri: int
                  pass_through_x_accel_headers: bool
                  pki_profile_ref: string
                  post_accept_timeout: int
                  reset_conn_http_on_ssl_port: bool
                  respond_with_100_continue: bool
                  secure_cookie_enabled: bool
                  server_side_redirect_to_https: bool
                  ssl_client_certificate_action:
                    close_connection: bool
                    headers:
                    - request_header: string
                      request_header_value: string
                  ssl_client_certificate_mode: string
                  true_client_ip:
                    direction: string
                    headers:
                    - value
                    index_in_header: int
                  use_app_keepalive_timeout: bool
                  use_true_client_ip: bool
                  websockets_enabled: bool
                  x_forwarded_proto_enabled: bool
                  xff_alternate_name: string
                  xff_enabled: bool
                  xff_update: string
              - l4_ssl_profile:
                  ssl_stream_idle_timeout: int
              - markers:
                - key: string
                  values:
                  - value
              - preserve_client_ip: bool
              - preserve_client_port: bool
              - preserve_dest_ip_port: bool
              - sip_service_profile:
                  transaction_timeout: int
              - tcp_app_profile:
                  ftp_profile:
                    deactivate_active: bool
                    deactivate_passive: bool
                  pki_profile_ref: string
                  proxy_protocol_enabled: bool
                  proxy_protocol_version: string
                  ssl_client_certificate_mode: string
              - tenant_ref: string
              - type: string


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
        before = await hub.exec.nsx_alb.alb.application_profile.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )

        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = before.ret

        result["comment"].append(
            f"'nsx_alb.alb.application_profile:{name}' already exists"
        )

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

        before = await hub.exec.nsx_alb.alb.application_profile.get(
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
                    before = await hub.exec.nsx_alb.alb.application_profile.get(
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
                    f"Would update nsx_alb.alb.application_profile '{name}'",
                )
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.nsx_alb.alb.application_profile.update(
                    ctx,
                    name=name,
                    resource_id=resource_id,
                    **{
                        "app_service_type": app_service_type,
                        "cloud_config_cksum": cloud_config_cksum,
                        "configpb_attributes": configpb_attributes,
                        "created_by": created_by,
                        "description": description,
                        "dns_service_profile": dns_service_profile,
                        "dos_rl_profile": dos_rl_profile,
                        "http_profile": http_profile,
                        "l4_ssl_profile": l4_ssl_profile,
                        "markers": markers,
                        "preserve_client_ip": preserve_client_ip,
                        "preserve_client_port": preserve_client_port,
                        "preserve_dest_ip_port": preserve_dest_ip_port,
                        "sip_service_profile": sip_service_profile,
                        "tcp_app_profile": tcp_app_profile,
                        "tenant_ref": tenant_ref,
                        "type": type,
                    },
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"].append(
                        f"Updated 'nsx_alb.alb.application_profile:{name}'"
                    )
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.test:
            result["new_state"] = hub.tool.nsx_alb.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"] = (
                f"Would create nsx_alb.alb.application_profile {name}",
            )
            return result
        else:
            create_ret = await hub.exec.nsx_alb.alb.application_profile.create(
                ctx,
                name=name,
                **{
                    "resource_id": resource_id,
                    "app_service_type": app_service_type,
                    "cloud_config_cksum": cloud_config_cksum,
                    "configpb_attributes": configpb_attributes,
                    "created_by": created_by,
                    "description": description,
                    "dns_service_profile": dns_service_profile,
                    "dos_rl_profile": dos_rl_profile,
                    "http_profile": http_profile,
                    "l4_ssl_profile": l4_ssl_profile,
                    "markers": markers,
                    "preserve_client_ip": preserve_client_ip,
                    "preserve_client_port": preserve_client_port,
                    "preserve_dest_ip_port": preserve_dest_ip_port,
                    "sip_service_profile": sip_service_profile,
                    "tcp_app_profile": tcp_app_profile,
                    "tenant_ref": tenant_ref,
                    "type": type,
                },
            )
            result["result"] = create_ret["result"]

            if result["result"]:
                result["comment"].append(
                    f"Created 'nsx_alb.alb.application_profile:{name}'"
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

    after = await hub.exec.nsx_alb.alb.application_profile.get(
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
            Alb.application_profile unique ID. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


            idem_test_nsx_alb.alb.application_profile_is_absent:
              nsx_alb.nsx_alb.alb.application_profile.absent:


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        result["comment"].append(
            f"'nsx_alb.alb.application_profile:{name}' already absent"
        )
        return result

    before = await hub.exec.nsx_alb.alb.application_profile.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    if before["ret"]:
        if ctx.test:
            result["comment"] = f"Would delete nsx_alb.alb.application_profile:{name}"
            return result

        delete_ret = await hub.exec.nsx_alb.alb.application_profile.delete(
            ctx,
            name=name,
            resource_id=resource_id,
        )
        result["result"] = delete_ret["result"]

        if result["result"]:
            result["comment"].append(
                f"Deleted 'nsx_alb.alb.application_profile:{name}'"
            )
        else:
            # If there is any failure in delete, it should reconcile.
            # The type of data is less important here to use default reconciliation
            # If there are no changes for 3 runs with rerun_data, then it will come out of execution
            result["rerun_data"] = resource_id
            result["comment"].append(delete_ret["result"])
    else:
        result["comment"].append(
            f"'nsx_alb.alb.application_profile:{name}' already absent"
        )
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

            $ idem describe nsx_alb.alb.application_profile
    """

    result = {}

    ret = await hub.exec.nsx_alb.alb.application_profile.list(ctx)

    if not ret or not ret["result"]:
        hub.log.debug(
            f"Could not describe nsx_alb.alb.application_profile {ret['comment']}"
        )
        return result

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "nsx_alb.alb.application_profile.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
