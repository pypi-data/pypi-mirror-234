"""States module for managing Alb Health Monitors. """
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
    allow_duplicate_monitors: bool = None,
    authentication: make_dataclass(
        "authentication", [("password", str), ("username", str)]
    ) = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    description: str = None,
    disable_quickstart: bool = None,
    dns_monitor: make_dataclass(
        "dns_monitor",
        [
            ("query_name", str),
            ("qtype", str, field(default=None)),
            ("rcode", str, field(default=None)),
            ("record_type", str, field(default=None)),
            ("response_string", str, field(default=None)),
        ],
    ) = None,
    external_monitor: make_dataclass(
        "external_monitor",
        [
            ("command_code", str),
            ("command_parameters", str, field(default=None)),
            ("command_path", str, field(default=None)),
            ("command_variables", str, field(default=None)),
        ],
    ) = None,
    failed_checks: int = None,
    ftp_monitor: make_dataclass(
        "ftp_monitor",
        [
            ("filename", str),
            ("mode", str),
            (
                "ssl_attributes",
                make_dataclass(
                    "ssl_attributes",
                    [
                        ("ssl_profile_ref", str),
                        ("pki_profile_ref", str, field(default=None)),
                        ("server_name", str, field(default=None)),
                        ("ssl_key_and_certificate_ref", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    ftps_monitor: make_dataclass(
        "ftps_monitor",
        [
            ("filename", str),
            ("mode", str),
            (
                "ssl_attributes",
                make_dataclass(
                    "ssl_attributes",
                    [
                        ("ssl_profile_ref", str),
                        ("pki_profile_ref", str, field(default=None)),
                        ("server_name", str, field(default=None)),
                        ("ssl_key_and_certificate_ref", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    http_monitor: make_dataclass(
        "http_monitor",
        [
            ("auth_type", str, field(default=None)),
            ("exact_http_request", bool, field(default=None)),
            ("http_request", str, field(default=None)),
            ("http_request_body", str, field(default=None)),
            ("http_response", str, field(default=None)),
            ("http_response_code", List[str], field(default=None)),
            ("maintenance_code", List[int], field(default=None)),
            ("maintenance_response", str, field(default=None)),
            ("response_size", int, field(default=None)),
            (
                "ssl_attributes",
                make_dataclass(
                    "ssl_attributes",
                    [
                        ("ssl_profile_ref", str),
                        ("pki_profile_ref", str, field(default=None)),
                        ("server_name", str, field(default=None)),
                        ("ssl_key_and_certificate_ref", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    https_monitor: make_dataclass(
        "https_monitor",
        [
            ("auth_type", str, field(default=None)),
            ("exact_http_request", bool, field(default=None)),
            ("http_request", str, field(default=None)),
            ("http_request_body", str, field(default=None)),
            ("http_response", str, field(default=None)),
            ("http_response_code", List[str], field(default=None)),
            ("maintenance_code", List[int], field(default=None)),
            ("maintenance_response", str, field(default=None)),
            ("response_size", int, field(default=None)),
            (
                "ssl_attributes",
                make_dataclass(
                    "ssl_attributes",
                    [
                        ("ssl_profile_ref", str),
                        ("pki_profile_ref", str, field(default=None)),
                        ("server_name", str, field(default=None)),
                        ("ssl_key_and_certificate_ref", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    imap_monitor: make_dataclass(
        "imap_monitor",
        [
            ("folder", str, field(default=None)),
            (
                "ssl_attributes",
                make_dataclass(
                    "ssl_attributes",
                    [
                        ("ssl_profile_ref", str),
                        ("pki_profile_ref", str, field(default=None)),
                        ("server_name", str, field(default=None)),
                        ("ssl_key_and_certificate_ref", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    imaps_monitor: make_dataclass(
        "imaps_monitor",
        [
            ("folder", str, field(default=None)),
            (
                "ssl_attributes",
                make_dataclass(
                    "ssl_attributes",
                    [
                        ("ssl_profile_ref", str),
                        ("pki_profile_ref", str, field(default=None)),
                        ("server_name", str, field(default=None)),
                        ("ssl_key_and_certificate_ref", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    is_federated: bool = None,
    ldap_monitor: make_dataclass(
        "ldap_monitor",
        [
            ("base_dn", str),
            ("attributes", str, field(default=None)),
            ("filter", str, field(default=None)),
            ("scope", str, field(default=None)),
            (
                "ssl_attributes",
                make_dataclass(
                    "ssl_attributes",
                    [
                        ("ssl_profile_ref", str),
                        ("pki_profile_ref", str, field(default=None)),
                        ("server_name", str, field(default=None)),
                        ("ssl_key_and_certificate_ref", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    ldaps_monitor: make_dataclass(
        "ldaps_monitor",
        [
            ("base_dn", str),
            ("attributes", str, field(default=None)),
            ("filter", str, field(default=None)),
            ("scope", str, field(default=None)),
            (
                "ssl_attributes",
                make_dataclass(
                    "ssl_attributes",
                    [
                        ("ssl_profile_ref", str),
                        ("pki_profile_ref", str, field(default=None)),
                        ("server_name", str, field(default=None)),
                        ("ssl_key_and_certificate_ref", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    monitor_port: int = None,
    pop3_monitor: make_dataclass(
        "pop3_monitor",
        [
            (
                "ssl_attributes",
                make_dataclass(
                    "ssl_attributes",
                    [
                        ("ssl_profile_ref", str),
                        ("pki_profile_ref", str, field(default=None)),
                        ("server_name", str, field(default=None)),
                        ("ssl_key_and_certificate_ref", str, field(default=None)),
                    ],
                ),
                field(default=None),
            )
        ],
    ) = None,
    pop3s_monitor: make_dataclass(
        "pop3s_monitor",
        [
            (
                "ssl_attributes",
                make_dataclass(
                    "ssl_attributes",
                    [
                        ("ssl_profile_ref", str),
                        ("pki_profile_ref", str, field(default=None)),
                        ("server_name", str, field(default=None)),
                        ("ssl_key_and_certificate_ref", str, field(default=None)),
                    ],
                ),
                field(default=None),
            )
        ],
    ) = None,
    radius_monitor: make_dataclass(
        "radius_monitor", [("password", str), ("shared_secret", str), ("username", str)]
    ) = None,
    receive_timeout: int = None,
    sctp_monitor: make_dataclass(
        "sctp_monitor",
        [
            ("sctp_request", str, field(default=None)),
            ("sctp_response", str, field(default=None)),
        ],
    ) = None,
    send_interval: int = None,
    sip_monitor: make_dataclass(
        "sip_monitor",
        [
            ("sip_monitor_transport", str, field(default=None)),
            ("sip_request_code", str, field(default=None)),
            ("sip_response", str, field(default=None)),
        ],
    ) = None,
    smtp_monitor: make_dataclass(
        "smtp_monitor",
        [
            ("domainname", str, field(default=None)),
            ("mail_data", str, field(default=None)),
            ("recipients_ids", List[str], field(default=None)),
            ("sender_id", str, field(default=None)),
            (
                "ssl_attributes",
                make_dataclass(
                    "ssl_attributes",
                    [
                        ("ssl_profile_ref", str),
                        ("pki_profile_ref", str, field(default=None)),
                        ("server_name", str, field(default=None)),
                        ("ssl_key_and_certificate_ref", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    smtps_monitor: make_dataclass(
        "smtps_monitor",
        [
            ("domainname", str, field(default=None)),
            ("mail_data", str, field(default=None)),
            ("recipients_ids", List[str], field(default=None)),
            ("sender_id", str, field(default=None)),
            (
                "ssl_attributes",
                make_dataclass(
                    "ssl_attributes",
                    [
                        ("ssl_profile_ref", str),
                        ("pki_profile_ref", str, field(default=None)),
                        ("server_name", str, field(default=None)),
                        ("ssl_key_and_certificate_ref", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    successful_checks: int = None,
    tcp_monitor: make_dataclass(
        "tcp_monitor",
        [
            ("maintenance_response", str, field(default=None)),
            ("tcp_half_open", bool, field(default=None)),
            ("tcp_request", str, field(default=None)),
            ("tcp_response", str, field(default=None)),
        ],
    ) = None,
    tenant_ref: str = None,
    udp_monitor: make_dataclass(
        "udp_monitor",
        [
            ("maintenance_response", str, field(default=None)),
            ("udp_request", str, field(default=None)),
            ("udp_response", str, field(default=None)),
        ],
    ) = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:
        name(str):
            Idem name of the resource.

        type(str):
            Type of the health monitor. Enum options - HEALTH_MONITOR_PING, HEALTH_MONITOR_TCP, HEALTH_MONITOR_HTTP, HEALTH_MONITOR_HTTPS, HEALTH_MONITOR_EXTERNAL, HEALTH_MONITOR_UDP, HEALTH_MONITOR_DNS, HEALTH_MONITOR_GSLB, HEALTH_MONITOR_SIP, HEALTH_MONITOR_RADIUS, HEALTH_MONITOR_SMTP, HEALTH_MONITOR_SMTPS, HEALTH_MONITOR_POP3, HEALTH_MONITOR_POP3S, HEALTH_MONITOR_IMAP, HEALTH_MONITOR_IMAPS, HEALTH_MONITOR_FTP, HEALTH_MONITOR_FTPS, HEALTH_MONITOR_LDAP, HEALTH_MONITOR_LDAPS, HEALTH_MONITOR_SCTP. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- HEALTH_MONITOR_PING,HEALTH_MONITOR_TCP,HEALTH_MONITOR_UDP), Basic edition(Allowed values- HEALTH_MONITOR_PING,HEALTH_MONITOR_TCP,HEALTH_MONITOR_UDP,HEALTH_MONITOR_HTTP,HEALTH_MONITOR_HTTPS), Enterprise with Cloud Services edition.

        resource_id(str, Optional):
            Alb.health_monitor unique ID. Defaults to None.

        allow_duplicate_monitors(bool, Optional):
            By default, multiple instances of the same healthmonitor to the same server are suppressed intelligently. In rare cases, the monitor may have specific constructs that go beyond the server keys (ip, port, etc.) during which such suppression is not desired. Use this knob to allow duplicates. Field introduced in 18.2.8. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- true), Basic edition(Allowed values- true), Enterprise with Cloud Services edition. Defaults to None.

        authentication(dict[str, Any], Optional):
            authentication. Defaults to None.

            * password (str):
                Password for server authentication. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * username (str):
                Username for server authentication. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        description(str, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disable_quickstart(bool, Optional):
            During addition of a server or healthmonitors or during bootup, Avi performs sequential health checks rather than waiting for send-interval to kick in, to mark the server up as soon as possible. This knob may be used to turn this feature off. Field introduced in 18.2.7. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        dns_monitor(dict[str, Any], Optional):
            dns_monitor. Defaults to None.

            * qtype (str, Optional):
                  Query_Type  Response has atleast one answer of which      the resource record type matches the query type   Any_Type  Response should contain atleast one answer  AnyThing  An empty answer is enough. Enum options - DNS_QUERY_TYPE, DNS_ANY_TYPE, DNS_ANY_THING. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * query_name (str):
                The DNS monitor will query the DNS server for the fully qualified name in this field. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * rcode (str, Optional):
                When No Error is selected, a DNS query will be marked failed is any error code is returned by the server.  With Any selected, the monitor ignores error code in the responses. Enum options - RCODE_NO_ERROR, RCODE_ANYTHING. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * record_type (str, Optional):
                Resource record type used in the healthmonitor DNS query, only A or AAAA type supported. Enum options - DNS_RECORD_OTHER, DNS_RECORD_A, DNS_RECORD_NS, DNS_RECORD_CNAME, DNS_RECORD_SOA, DNS_RECORD_PTR, DNS_RECORD_HINFO, DNS_RECORD_MX, DNS_RECORD_TXT, DNS_RECORD_RP, DNS_RECORD_DNSKEY, DNS_RECORD_AAAA, DNS_RECORD_SRV, DNS_RECORD_OPT, DNS_RECORD_RRSIG, DNS_RECORD_AXFR, DNS_RECORD_ANY. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * response_string (str, Optional):
                The resource record of the queried DNS server's response for the Request Name must include the IP address defined in this field. . Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        external_monitor(dict[str, Any], Optional):
            external_monitor. Defaults to None.

            * command_code (str):
                Command script provided inline. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * command_parameters (str, Optional):
                Optional arguments to feed into the script. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * command_path (str, Optional):
                Path of external health monitor script. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * command_variables (str, Optional):
                Environment variables to be fed into the script. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        failed_checks(int, Optional):
            Number of continuous failed health checks before the server is marked down. Allowed values are 1-50. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ftp_monitor(dict[str, Any], Optional):
            ftp_monitor. Defaults to None.

            * filename (str):
                Filename to download with full path. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * mode (str):
                FTP data transfer process mode. Enum options - FTP_PASSIVE_MODE, FTP_PORT_MODE. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ssl_attributes (dict[str, Any], Optional):
                ssl_attributes

                * pki_profile_ref (str, Optional):
                    PKI profile used to validate the SSL certificate presented by a server. It is a reference to an object of type PKIProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server_name (str, Optional):
                    Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections indicating SNI is enabled. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_key_and_certificate_ref (str, Optional):
                    Service engines will present this SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_profile_ref (str):
                    SSL profile defines ciphers and SSL versions to be used for healthmonitor traffic to the back-end servers. It is a reference to an object of type SSLProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        ftps_monitor(dict[str, Any], Optional):
            ftps_monitor. Defaults to None.

            * filename (str):
                Filename to download with full path. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * mode (str):
                FTP data transfer process mode. Enum options - FTP_PASSIVE_MODE, FTP_PORT_MODE. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ssl_attributes (dict[str, Any], Optional):
                ssl_attributes

                * pki_profile_ref (str, Optional):
                    PKI profile used to validate the SSL certificate presented by a server. It is a reference to an object of type PKIProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server_name (str, Optional):
                    Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections indicating SNI is enabled. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_key_and_certificate_ref (str, Optional):
                    Service engines will present this SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_profile_ref (str):
                    SSL profile defines ciphers and SSL versions to be used for healthmonitor traffic to the back-end servers. It is a reference to an object of type SSLProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        http_monitor(dict[str, Any], Optional):
            http_monitor. Defaults to None.

            * auth_type (str, Optional):
                Type of the authentication method. Enum options - AUTH_BASIC, AUTH_NTLM. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * exact_http_request (bool, Optional):
                Use the exact http_request string as specified by user, without any automatic insert of headers like Host header. Field introduced in 17.1.6,17.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_request (str, Optional):
                Send an HTTP request to the server.  The default GET / HTTP/1.0 may be extended with additional headers or information.  For instance, GET /index.htm HTTP/1.1 Host  www.site.com Connection  Close. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_request_body (str, Optional):
                HTTP request body. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_response (str, Optional):
                Match for a keyword in the first 2Kb of the server header and body response. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_response_code (List[str], Optional):
                List of HTTP response codes to match as successful.  Default is 2xx. Enum options - HTTP_ANY, HTTP_1XX, HTTP_2XX, HTTP_3XX, HTTP_4XX, HTTP_5XX. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * maintenance_code (List[int], Optional):
                Match or look for this HTTP response code indicating server maintenance.  A successful match results in the server being marked down. Allowed values are 101-599. Maximum of 4 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * maintenance_response (str, Optional):
                Match or look for this keyword in the first 2KB of server header and body response indicating server maintenance.  A successful match results in the server being marked down. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * response_size (int, Optional):
                Expected http/https response page size. Allowed values are 2048-16384. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ssl_attributes (dict[str, Any], Optional):
                ssl_attributes

                * pki_profile_ref (str, Optional):
                    PKI profile used to validate the SSL certificate presented by a server. It is a reference to an object of type PKIProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server_name (str, Optional):
                    Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections indicating SNI is enabled. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_key_and_certificate_ref (str, Optional):
                    Service engines will present this SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_profile_ref (str):
                    SSL profile defines ciphers and SSL versions to be used for healthmonitor traffic to the back-end servers. It is a reference to an object of type SSLProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        https_monitor(dict[str, Any], Optional):
            https_monitor. Defaults to None.

            * auth_type (str, Optional):
                Type of the authentication method. Enum options - AUTH_BASIC, AUTH_NTLM. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * exact_http_request (bool, Optional):
                Use the exact http_request string as specified by user, without any automatic insert of headers like Host header. Field introduced in 17.1.6,17.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_request (str, Optional):
                Send an HTTP request to the server.  The default GET / HTTP/1.0 may be extended with additional headers or information.  For instance, GET /index.htm HTTP/1.1 Host  www.site.com Connection  Close. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_request_body (str, Optional):
                HTTP request body. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_response (str, Optional):
                Match for a keyword in the first 2Kb of the server header and body response. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_response_code (List[str], Optional):
                List of HTTP response codes to match as successful.  Default is 2xx. Enum options - HTTP_ANY, HTTP_1XX, HTTP_2XX, HTTP_3XX, HTTP_4XX, HTTP_5XX. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * maintenance_code (List[int], Optional):
                Match or look for this HTTP response code indicating server maintenance.  A successful match results in the server being marked down. Allowed values are 101-599. Maximum of 4 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * maintenance_response (str, Optional):
                Match or look for this keyword in the first 2KB of server header and body response indicating server maintenance.  A successful match results in the server being marked down. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * response_size (int, Optional):
                Expected http/https response page size. Allowed values are 2048-16384. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ssl_attributes (dict[str, Any], Optional):
                ssl_attributes

                * pki_profile_ref (str, Optional):
                    PKI profile used to validate the SSL certificate presented by a server. It is a reference to an object of type PKIProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server_name (str, Optional):
                    Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections indicating SNI is enabled. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_key_and_certificate_ref (str, Optional):
                    Service engines will present this SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_profile_ref (str):
                    SSL profile defines ciphers and SSL versions to be used for healthmonitor traffic to the back-end servers. It is a reference to an object of type SSLProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        imap_monitor(dict[str, Any], Optional):
            imap_monitor. Defaults to None.

            * folder (str, Optional):
                Folder to access. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ssl_attributes (dict[str, Any], Optional):
                ssl_attributes

                * pki_profile_ref (str, Optional):
                    PKI profile used to validate the SSL certificate presented by a server. It is a reference to an object of type PKIProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server_name (str, Optional):
                    Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections indicating SNI is enabled. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_key_and_certificate_ref (str, Optional):
                    Service engines will present this SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_profile_ref (str):
                    SSL profile defines ciphers and SSL versions to be used for healthmonitor traffic to the back-end servers. It is a reference to an object of type SSLProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        imaps_monitor(dict[str, Any], Optional):
            imaps_monitor. Defaults to None.

            * folder (str, Optional):
                Folder to access. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ssl_attributes (dict[str, Any], Optional):
                ssl_attributes

                * pki_profile_ref (str, Optional):
                    PKI profile used to validate the SSL certificate presented by a server. It is a reference to an object of type PKIProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server_name (str, Optional):
                    Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections indicating SNI is enabled. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_key_and_certificate_ref (str, Optional):
                    Service engines will present this SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_profile_ref (str):
                    SSL profile defines ciphers and SSL versions to be used for healthmonitor traffic to the back-end servers. It is a reference to an object of type SSLProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        is_federated(bool, Optional):
            This field describes the object's replication scope. If the field is set to false, then the object is visible within the controller-cluster and its associated service-engines.  If the field is set to true, then the object is replicated across the federation.  . Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        ldap_monitor(dict[str, Any], Optional):
            ldap_monitor. Defaults to None.

            * attributes (str, Optional):
                Attributes which will be retrieved. commas can be used to delimit more than one attributes (example- cn,address,email). Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * base_dn (str):
                DN(Distinguished Name) of a directory entry. which will be starting point of the search. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * filter (str, Optional):
                Filter to search entries in specified scope. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * scope (str, Optional):
                Search scope which can be base, one, sub. Enum options - LDAP_BASE_MODE, LDAP_ONE_MODE, LDAP_SUB_MODE. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ssl_attributes (dict[str, Any], Optional):
                ssl_attributes

                * pki_profile_ref (str, Optional):
                    PKI profile used to validate the SSL certificate presented by a server. It is a reference to an object of type PKIProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server_name (str, Optional):
                    Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections indicating SNI is enabled. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_key_and_certificate_ref (str, Optional):
                    Service engines will present this SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_profile_ref (str):
                    SSL profile defines ciphers and SSL versions to be used for healthmonitor traffic to the back-end servers. It is a reference to an object of type SSLProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        ldaps_monitor(dict[str, Any], Optional):
            ldaps_monitor. Defaults to None.

            * attributes (str, Optional):
                Attributes which will be retrieved. commas can be used to delimit more than one attributes (example- cn,address,email). Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * base_dn (str):
                DN(Distinguished Name) of a directory entry. which will be starting point of the search. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * filter (str, Optional):
                Filter to search entries in specified scope. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * scope (str, Optional):
                Search scope which can be base, one, sub. Enum options - LDAP_BASE_MODE, LDAP_ONE_MODE, LDAP_SUB_MODE. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ssl_attributes (dict[str, Any], Optional):
                ssl_attributes

                * pki_profile_ref (str, Optional):
                    PKI profile used to validate the SSL certificate presented by a server. It is a reference to an object of type PKIProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server_name (str, Optional):
                    Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections indicating SNI is enabled. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_key_and_certificate_ref (str, Optional):
                    Service engines will present this SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_profile_ref (str):
                    SSL profile defines ciphers and SSL versions to be used for healthmonitor traffic to the back-end servers. It is a reference to an object of type SSLProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        monitor_port(int, Optional):
            Use this port instead of the port defined for the server in the Pool. If the monitor succeeds to this port, the load balanced traffic will still be sent to the port of the server defined within the Pool. Allowed values are 1-65535. Special values are 0 - Use server port. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        pop3_monitor(dict[str, Any], Optional):
            pop3_monitor. Defaults to None.

            * ssl_attributes (dict[str, Any], Optional):
                ssl_attributes

                * pki_profile_ref (str, Optional):
                    PKI profile used to validate the SSL certificate presented by a server. It is a reference to an object of type PKIProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server_name (str, Optional):
                    Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections indicating SNI is enabled. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_key_and_certificate_ref (str, Optional):
                    Service engines will present this SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_profile_ref (str):
                    SSL profile defines ciphers and SSL versions to be used for healthmonitor traffic to the back-end servers. It is a reference to an object of type SSLProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        pop3s_monitor(dict[str, Any], Optional):
            pop3s_monitor. Defaults to None.

            * ssl_attributes (dict[str, Any], Optional):
                ssl_attributes

                * pki_profile_ref (str, Optional):
                    PKI profile used to validate the SSL certificate presented by a server. It is a reference to an object of type PKIProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server_name (str, Optional):
                    Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections indicating SNI is enabled. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_key_and_certificate_ref (str, Optional):
                    Service engines will present this SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_profile_ref (str):
                    SSL profile defines ciphers and SSL versions to be used for healthmonitor traffic to the back-end servers. It is a reference to an object of type SSLProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        radius_monitor(dict[str, Any], Optional):
            radius_monitor. Defaults to None.

            * password (str):
                Radius monitor will query Radius server with this password. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * shared_secret (str):
                Radius monitor will query Radius server with this shared secret. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * username (str):
                Radius monitor will query Radius server with this username. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        receive_timeout(int, Optional):
            A valid response from the server is expected within the receive timeout window.  This timeout must be less than the send interval.  If server status is regularly flapping up and down, consider increasing this value. Allowed values are 1-2400. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        sctp_monitor(dict[str, Any], Optional):
            sctp_monitor. Defaults to None.

            * sctp_request (str, Optional):
                Request data to send after completing the SCTP handshake. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * sctp_response (str, Optional):
                Match for the desired keyword in the first 2Kb of the server's SCTP response. If this field is left blank, no server response is required. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        send_interval(int, Optional):
            Frequency, in seconds, that monitors are sent to a server. Allowed values are 1-3600. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        sip_monitor(dict[str, Any], Optional):
            sip_monitor. Defaults to None.

            * sip_monitor_transport (str, Optional):
                Specify the transport protocol TCP or UDP, to be used for SIP health monitor. The default transport is UDP. Enum options - SIP_UDP_PROTO, SIP_TCP_PROTO. Field introduced in 17.2.14, 18.1.5, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * sip_request_code (str, Optional):
                Specify the SIP request to be sent to the server. By default, SIP OPTIONS request will be sent. Enum options - SIP_OPTIONS. Field introduced in 17.2.8, 18.1.3, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * sip_response (str, Optional):
                Match for a keyword in the first 2KB of the server header and body response. By default, it matches for SIP/2.0. Field introduced in 17.2.8, 18.1.3, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        smtp_monitor(dict[str, Any], Optional):
            smtp_monitor. Defaults to None.

            * domainname (str, Optional):
                Sender domain name. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * mail_data (str, Optional):
                Mail data. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * recipients_ids (List[str], Optional):
                Mail recipients. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * sender_id (str, Optional):
                Mail sender. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ssl_attributes (dict[str, Any], Optional):
                ssl_attributes

                * pki_profile_ref (str, Optional):
                    PKI profile used to validate the SSL certificate presented by a server. It is a reference to an object of type PKIProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server_name (str, Optional):
                    Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections indicating SNI is enabled. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_key_and_certificate_ref (str, Optional):
                    Service engines will present this SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_profile_ref (str):
                    SSL profile defines ciphers and SSL versions to be used for healthmonitor traffic to the back-end servers. It is a reference to an object of type SSLProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        smtps_monitor(dict[str, Any], Optional):
            smtps_monitor. Defaults to None.

            * domainname (str, Optional):
                Sender domain name. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * mail_data (str, Optional):
                Mail data. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * recipients_ids (List[str], Optional):
                Mail recipients. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * sender_id (str, Optional):
                Mail sender. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ssl_attributes (dict[str, Any], Optional):
                ssl_attributes

                * pki_profile_ref (str, Optional):
                    PKI profile used to validate the SSL certificate presented by a server. It is a reference to an object of type PKIProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server_name (str, Optional):
                    Fully qualified DNS hostname which will be used in the TLS SNI extension in server connections indicating SNI is enabled. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_key_and_certificate_ref (str, Optional):
                    Service engines will present this SSL certificate to the server. It is a reference to an object of type SSLKeyAndCertificate. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * ssl_profile_ref (str):
                    SSL profile defines ciphers and SSL versions to be used for healthmonitor traffic to the back-end servers. It is a reference to an object of type SSLProfile. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        successful_checks(int, Optional):
            Number of continuous successful health checks before server is marked up. Allowed values are 1-50. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        tcp_monitor(dict[str, Any], Optional):
            tcp_monitor. Defaults to None.

            * maintenance_response (str, Optional):
                Match or look for this keyword in the first 2KB of server's response indicating server maintenance.  A successful match results in the server being marked down. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * tcp_half_open (bool, Optional):
                Configure TCP health monitor to use half-open TCP connections to monitor the health of backend servers thereby avoiding consumption of a full fledged server side connection and the overhead and logs associated with it.  This method is light-weight as it makes use of listener in server's kernel layer to measure the health and a child socket or user thread is not created on the server side. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition.

            * tcp_request (str, Optional):
                Request data to send after completing the TCP handshake. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * tcp_response (str, Optional):
                Match for the desired keyword in the first 2Kb of the server's TCP response. If this field is left blank, no server response is required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        udp_monitor(dict[str, Any], Optional):
            udp_monitor. Defaults to None.

            * maintenance_response (str, Optional):
                Match or look for this keyword in the first 2KB of server's response indicating server maintenance.  A successful match results in the server being marked down. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * udp_request (str, Optional):
                Send UDP request. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * udp_response (str, Optional):
                Match for keyword in the UDP response. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


          idem_test_nsx_alb.alb.health_monitor_is_present:
              nsx_alb.nsx_alb.alb.health_monitor.present:
              - allow_duplicate_monitors: bool
              - authentication:
                  password: string
                  username: string
              - configpb_attributes:
                  version: int
              - description: string
              - disable_quickstart: bool
              - dns_monitor:
                  qtype: string
                  query_name: string
                  rcode: string
                  record_type: string
                  response_string: string
              - external_monitor:
                  command_code: string
                  command_parameters: string
                  command_path: string
                  command_variables: string
              - failed_checks: int
              - ftp_monitor:
                  filename: string
                  mode: string
                  ssl_attributes:
                    pki_profile_ref: string
                    server_name: string
                    ssl_key_and_certificate_ref: string
                    ssl_profile_ref: string
              - ftps_monitor:
                  filename: string
                  mode: string
                  ssl_attributes:
                    pki_profile_ref: string
                    server_name: string
                    ssl_key_and_certificate_ref: string
                    ssl_profile_ref: string
              - http_monitor:
                  auth_type: string
                  exact_http_request: bool
                  http_request: string
                  http_request_body: string
                  http_response: string
                  http_response_code:
                  - value
                  maintenance_code: List[int]
                  maintenance_response: string
                  response_size: int
                  ssl_attributes:
                    pki_profile_ref: string
                    server_name: string
                    ssl_key_and_certificate_ref: string
                    ssl_profile_ref: string
              - https_monitor:
                  auth_type: string
                  exact_http_request: bool
                  http_request: string
                  http_request_body: string
                  http_response: string
                  http_response_code:
                  - value
                  maintenance_code: List[int]
                  maintenance_response: string
                  response_size: int
                  ssl_attributes:
                    pki_profile_ref: string
                    server_name: string
                    ssl_key_and_certificate_ref: string
                    ssl_profile_ref: string
              - imap_monitor:
                  folder: string
                  ssl_attributes:
                    pki_profile_ref: string
                    server_name: string
                    ssl_key_and_certificate_ref: string
                    ssl_profile_ref: string
              - imaps_monitor:
                  folder: string
                  ssl_attributes:
                    pki_profile_ref: string
                    server_name: string
                    ssl_key_and_certificate_ref: string
                    ssl_profile_ref: string
              - is_federated: bool
              - ldap_monitor:
                  attributes: string
                  base_dn: string
                  filter_: string
                  scope: string
                  ssl_attributes:
                    pki_profile_ref: string
                    server_name: string
                    ssl_key_and_certificate_ref: string
                    ssl_profile_ref: string
              - ldaps_monitor:
                  attributes: string
                  base_dn: string
                  filter_: string
                  scope: string
                  ssl_attributes:
                    pki_profile_ref: string
                    server_name: string
                    ssl_key_and_certificate_ref: string
                    ssl_profile_ref: string
              - markers:
                - key: string
                  values:
                  - value
              - monitor_port: int
              - pop3_monitor:
                  ssl_attributes:
                    pki_profile_ref: string
                    server_name: string
                    ssl_key_and_certificate_ref: string
                    ssl_profile_ref: string
              - pop3s_monitor:
                  ssl_attributes:
                    pki_profile_ref: string
                    server_name: string
                    ssl_key_and_certificate_ref: string
                    ssl_profile_ref: string
              - radius_monitor:
                  password: string
                  shared_secret: string
                  username: string
              - receive_timeout: int
              - sctp_monitor:
                  sctp_request: string
                  sctp_response: string
              - send_interval: int
              - sip_monitor:
                  sip_monitor_transport: string
                  sip_request_code: string
                  sip_response: string
              - smtp_monitor:
                  domainname: string
                  mail_data: string
                  recipients_ids:
                  - value
                  sender_id: string
                  ssl_attributes:
                    pki_profile_ref: string
                    server_name: string
                    ssl_key_and_certificate_ref: string
                    ssl_profile_ref: string
              - smtps_monitor:
                  domainname: string
                  mail_data: string
                  recipients_ids:
                  - value
                  sender_id: string
                  ssl_attributes:
                    pki_profile_ref: string
                    server_name: string
                    ssl_key_and_certificate_ref: string
                    ssl_profile_ref: string
              - successful_checks: int
              - tcp_monitor:
                  maintenance_response: string
                  tcp_half_open: bool
                  tcp_request: string
                  tcp_response: string
              - tenant_ref: string
              - type_: string
              - udp_monitor:
                  maintenance_response: string
                  udp_request: string
                  udp_response: string


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
        before = await hub.exec.nsx_alb.alb.health_monitor.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )

        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = before.ret

        result["comment"].append(f"'nsx_alb.alb.health_monitor:{name}' already exists")

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

        before = await hub.exec.nsx_alb.alb.health_monitor.get(
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
                    before = await hub.exec.nsx_alb.alb.health_monitor.get(
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
                    f"Would update nsx_alb.alb.health_monitor '{name}'",
                )
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.nsx_alb.alb.health_monitor.update(
                    ctx,
                    name=name,
                    resource_id=resource_id,
                    **{
                        "allow_duplicate_monitors": allow_duplicate_monitors,
                        "authentication": authentication,
                        "configpb_attributes": configpb_attributes,
                        "description": description,
                        "disable_quickstart": disable_quickstart,
                        "dns_monitor": dns_monitor,
                        "external_monitor": external_monitor,
                        "failed_checks": failed_checks,
                        "ftp_monitor": ftp_monitor,
                        "ftps_monitor": ftps_monitor,
                        "http_monitor": http_monitor,
                        "https_monitor": https_monitor,
                        "imap_monitor": imap_monitor,
                        "imaps_monitor": imaps_monitor,
                        "is_federated": is_federated,
                        "ldap_monitor": ldap_monitor,
                        "ldaps_monitor": ldaps_monitor,
                        "markers": markers,
                        "monitor_port": monitor_port,
                        "pop3_monitor": pop3_monitor,
                        "pop3s_monitor": pop3s_monitor,
                        "radius_monitor": radius_monitor,
                        "receive_timeout": receive_timeout,
                        "sctp_monitor": sctp_monitor,
                        "send_interval": send_interval,
                        "sip_monitor": sip_monitor,
                        "smtp_monitor": smtp_monitor,
                        "smtps_monitor": smtps_monitor,
                        "successful_checks": successful_checks,
                        "tcp_monitor": tcp_monitor,
                        "tenant_ref": tenant_ref,
                        "type": type,
                        "udp_monitor": udp_monitor,
                    },
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"].append(
                        f"Updated 'nsx_alb.alb.health_monitor:{name}'"
                    )
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.test:
            result["new_state"] = hub.tool.nsx_alb.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"] = (f"Would create nsx_alb.alb.health_monitor {name}",)
            return result
        else:
            create_ret = await hub.exec.nsx_alb.alb.health_monitor.create(
                ctx,
                name=name,
                **{
                    "resource_id": resource_id,
                    "allow_duplicate_monitors": allow_duplicate_monitors,
                    "authentication": authentication,
                    "configpb_attributes": configpb_attributes,
                    "description": description,
                    "disable_quickstart": disable_quickstart,
                    "dns_monitor": dns_monitor,
                    "external_monitor": external_monitor,
                    "failed_checks": failed_checks,
                    "ftp_monitor": ftp_monitor,
                    "ftps_monitor": ftps_monitor,
                    "http_monitor": http_monitor,
                    "https_monitor": https_monitor,
                    "imap_monitor": imap_monitor,
                    "imaps_monitor": imaps_monitor,
                    "is_federated": is_federated,
                    "ldap_monitor": ldap_monitor,
                    "ldaps_monitor": ldaps_monitor,
                    "markers": markers,
                    "monitor_port": monitor_port,
                    "pop3_monitor": pop3_monitor,
                    "pop3s_monitor": pop3s_monitor,
                    "radius_monitor": radius_monitor,
                    "receive_timeout": receive_timeout,
                    "sctp_monitor": sctp_monitor,
                    "send_interval": send_interval,
                    "sip_monitor": sip_monitor,
                    "smtp_monitor": smtp_monitor,
                    "smtps_monitor": smtps_monitor,
                    "successful_checks": successful_checks,
                    "tcp_monitor": tcp_monitor,
                    "tenant_ref": tenant_ref,
                    "type": type,
                    "udp_monitor": udp_monitor,
                },
            )
            result["result"] = create_ret["result"]

            if result["result"]:
                result["comment"].append(f"Created 'nsx_alb.alb.health_monitor:{name}'")
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

    after = await hub.exec.nsx_alb.alb.health_monitor.get(
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
            Alb.health_monitor unique ID. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


            idem_test_nsx_alb.alb.health_monitor_is_absent:
              nsx_alb.nsx_alb.alb.health_monitor.absent:

    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        result["comment"].append(f"'nsx_alb.alb.health_monitor:{name}' already absent")
        return result

    before = await hub.exec.nsx_alb.alb.health_monitor.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    if before["ret"]:
        if ctx.test:
            result["comment"] = f"Would delete nsx_alb.alb.health_monitor:{name}"
            return result

        delete_ret = await hub.exec.nsx_alb.alb.health_monitor.delete(
            ctx,
            name=name,
            resource_id=resource_id,
        )
        result["result"] = delete_ret["result"]

        if result["result"]:
            result["comment"].append(f"Deleted 'nsx_alb.alb.health_monitor:{name}'")
        else:
            # If there is any failure in delete, it should reconcile.
            # The type of data is less important here to use default reconciliation
            # If there are no changes for 3 runs with rerun_data, then it will come out of execution
            result["rerun_data"] = resource_id
            result["comment"].append(delete_ret["result"])
    else:
        result["comment"].append(f"'nsx_alb.alb.health_monitor:{name}' already absent")
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

            $ idem describe nsx_alb.alb.health_monitor
    """

    result = {}

    ret = await hub.exec.nsx_alb.alb.health_monitor.list(ctx)

    if not ret or not ret["result"]:
        hub.log.debug(f"Could not describe nsx_alb.alb.health_monitor {ret['comment']}")
        return result

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "nsx_alb.alb.health_monitor.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
