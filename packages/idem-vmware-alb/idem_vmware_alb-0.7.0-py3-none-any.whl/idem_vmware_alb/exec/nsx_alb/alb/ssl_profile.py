"""Exec module for managing Alb Ssl Profiles. """
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
            Alb.ssl_profile unique ID.

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
                - path: nsx_alb.alb.ssl_profile.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.ssl_profile.get resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)

    get = await hub.tool.nsx_alb.session.request(
        ctx,
        method="get",
        path="/sslprofile/{uuid}?include_name".format(**{"uuid": resource_id})
        if resource_id
        else "/sslprofile?include_name",
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
            "accepted_ciphers": "accepted_ciphers",
            "accepted_versions": "accepted_versions",
            "cipher_enums": "cipher_enums",
            "ciphersuites": "ciphersuites",
            "configpb_attributes": "configpb_attributes",
            "description": "description",
            "dhparam": "dhparam",
            "ec_named_curve": "ec_named_curve",
            "enable_early_data": "enable_early_data",
            "enable_ssl_session_reuse": "enable_ssl_session_reuse",
            "is_federated": "is_federated",
            "markers": "markers",
            "name": "name",
            "prefer_client_cipher_ordering": "prefer_client_cipher_ordering",
            "send_close_notify": "send_close_notify",
            "signature_algorithm": "signature_algorithm",
            "ssl_rating": "ssl_rating",
            "ssl_session_timeout": "ssl_session_timeout",
            "tags": "tags",
            "tenant_ref": "tenant_ref",
            "type": "type",
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
                - path: nsx_alb.alb.ssl_profile.list
                - kwargs:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.ssl_profile.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe nsx_alb.alb.ssl_profile

    """

    result = dict(comment=[], ret=[], result=True)

    list = await hub.tool.nsx_alb.session.request(
        ctx,
        method="get",
        path="/sslprofile",
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
    accepted_ciphers: str = None,
    accepted_versions: List[
        make_dataclass("accepted_versions", [("type", str)])
    ] = None,
    cipher_enums: List[str] = None,
    ciphersuites: str = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    description: str = None,
    dhparam: str = None,
    ec_named_curve: str = None,
    enable_early_data: bool = None,
    enable_ssl_session_reuse: bool = None,
    is_federated: bool = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    prefer_client_cipher_ordering: bool = None,
    send_close_notify: bool = None,
    signature_algorithm: str = None,
    ssl_rating: make_dataclass(
        "ssl_rating",
        [
            ("compatibility_rating", str, field(default=None)),
            ("performance_rating", str, field(default=None)),
            ("security_score", str, field(default=None)),
        ],
    ) = None,
    ssl_session_timeout: int = None,
    tags: List[
        make_dataclass("tags", [("value", str), ("type", str, field(default=None))])
    ] = None,
    tenant_ref: str = None,
    type: str = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:

        resource_id(str, Optional):
            Alb.ssl_profile unique ID. Defaults to None.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

        accepted_ciphers(str, Optional):
            Ciphers suites represented as defined by https //www.openssl.org/docs/man1.1.1/man1/ciphers.html. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        accepted_versions(List[dict[str, Any]], Optional):
            Set of versions accepted by the server. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * type (str):
                 Enum options - SSL_VERSION_SSLV3, SSL_VERSION_TLS1, SSL_VERSION_TLS1_1, SSL_VERSION_TLS1_2, SSL_VERSION_TLS1_3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- SSL_VERSION_SSLV3,SSL_VERSION_TLS1,SSL_VERSION_TLS1_1,SSL_VERSION_TLS1_2), Basic edition(Allowed values- SSL_VERSION_SSLV3,SSL_VERSION_TLS1,SSL_VERSION_TLS1_1,SSL_VERSION_TLS1_2), Enterprise with Cloud Services edition.

        cipher_enums(List[str], Optional):
             Enum options - TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384, TLS_RSA_WITH_AES_128_GCM_SHA256, TLS_RSA_WITH_AES_256_GCM_SHA384, TLS_RSA_WITH_AES_128_CBC_SHA256, TLS_RSA_WITH_AES_256_CBC_SHA256, TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA, TLS_RSA_WITH_AES_128_CBC_SHA, TLS_RSA_WITH_AES_256_CBC_SHA, TLS_RSA_WITH_3DES_EDE_CBC_SHA, TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256, TLS_AES_128_GCM_SHA256. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_CBC_SHA256,TLS_RSA_WITH_AES_256_CBC_SHA256,TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_3DES_EDE_CBC_SHA), Basic edition(Allowed values- TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_CBC_SHA256,TLS_RSA_WITH_AES_256_CBC_SHA256,TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_3DES_EDE_CBC_SHA), Enterprise with Cloud Services edition. Defaults to None.

        ciphersuites(str, Optional):
            TLS 1.3 Ciphers suites represented as defined by U(https //www.openssl.org/docs/man1.1.1/man1/ciphers.html). Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Special default for Essentials edition is TLS_AES_256_GCM_SHA384-TLS_AES_128_GCM_SHA256, Basic edition is TLS_AES_256_GCM_SHA384-TLS_AES_128_GCM_SHA256, Enterprise is TLS_AES_256_GCM_SHA384-TLS_CHACHA20_POLY1305_SHA256-TLS_AES_128_GCM_SHA256. Defaults to None.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        description(str, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        dhparam(str, Optional):
            DH Parameters used in SSL. At this time, it is not configurable and is set to 2048 bits. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ec_named_curve(str, Optional):
            Elliptic Curve Cryptography NamedCurves (TLS Supported Groups)represented as defined by RFC 8422-Section 5.1.1 andhttps //www.openssl.org/docs/man1.1.0/man3/SSL_CTX_set1_curves.html. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        enable_early_data(bool, Optional):
            Enable early data processing for TLS1.3 connections. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        enable_ssl_session_reuse(bool, Optional):
            Enable SSL session re-use. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        is_federated(bool, Optional):
            It Specifies whether the object has to be replicated to the GSLB followers. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        prefer_client_cipher_ordering(bool, Optional):
            Prefer the SSL cipher ordering presented by the client during the SSL handshake over the one specified in the SSL Profile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        send_close_notify(bool, Optional):
            Send 'close notify' alert message for a clean shutdown of the SSL connection. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        signature_algorithm(str, Optional):
            Signature Algorithms represented as defined by RFC5246-Section 7.4.1.4.1 andhttps //www.openssl.org/docs/man1.1.0/man3/SSL_CTX_set1_client_sigalgs_list.html. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ssl_rating(dict[str, Any], Optional):
            ssl_rating. Defaults to None.

            * compatibility_rating (str, Optional):
                 Enum options - SSL_SCORE_NOT_SECURE, SSL_SCORE_VERY_BAD, SSL_SCORE_BAD, SSL_SCORE_AVERAGE, SSL_SCORE_GOOD, SSL_SCORE_EXCELLENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * performance_rating (str, Optional):
                 Enum options - SSL_SCORE_NOT_SECURE, SSL_SCORE_VERY_BAD, SSL_SCORE_BAD, SSL_SCORE_AVERAGE, SSL_SCORE_GOOD, SSL_SCORE_EXCELLENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * security_score (str, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        ssl_session_timeout(int, Optional):
            The amount of time in seconds before an SSL session expires. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        tags(List[dict[str, Any]], Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * type (str, Optional):
                 Enum options - AVI_DEFINED, USER_DEFINED, VCENTER_DEFINED. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * value (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        type(str, Optional):
            SSL Profile Type. Enum options - SSL_PROFILE_TYPE_APPLICATION, SSL_PROFILE_TYPE_SYSTEM. Field introduced in 17.2.8. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              nsx_alb.alb.ssl_profile.present:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.ssl_profile.create
    """

    result = dict(comment=[], ret=[], result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "accepted_ciphers": "accepted_ciphers",
        "accepted_versions": "accepted_versions",
        "cipher_enums": "cipher_enums",
        "ciphersuites": "ciphersuites",
        "configpb_attributes": "configpb_attributes",
        "description": "description",
        "dhparam": "dhparam",
        "ec_named_curve": "ec_named_curve",
        "enable_early_data": "enable_early_data",
        "enable_ssl_session_reuse": "enable_ssl_session_reuse",
        "is_federated": "is_federated",
        "markers": "markers",
        "name": "name",
        "prefer_client_cipher_ordering": "prefer_client_cipher_ordering",
        "send_close_notify": "send_close_notify",
        "signature_algorithm": "signature_algorithm",
        "ssl_rating": "ssl_rating",
        "ssl_session_timeout": "ssl_session_timeout",
        "tags": "tags",
        "tenant_ref": "tenant_ref",
        "type": "type",
    }

    payload = {}
    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = value

    create = await hub.tool.nsx_alb.session.request(
        ctx,
        method="post",
        path="/sslprofile",
        query_params={},
        data=payload,
    )

    if not create["result"]:
        result["comment"].append(create["comment"])
        result["result"] = False
        return result

    result["comment"].append(
        f"Created nsx_alb.alb.ssl_profile '{name}'",
    )

    result["ret"] = create["ret"]

    result["ret"]["resource_id"] = create["ret"]["uuid"]
    return result


async def update(
    hub,
    ctx,
    resource_id: str,
    name: str = None,
    accepted_ciphers: str = None,
    accepted_versions: List[
        make_dataclass("accepted_versions", [("type", str)])
    ] = None,
    cipher_enums: List[str] = None,
    ciphersuites: str = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    description: str = None,
    dhparam: str = None,
    ec_named_curve: str = None,
    enable_early_data: bool = None,
    enable_ssl_session_reuse: bool = None,
    is_federated: bool = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    prefer_client_cipher_ordering: bool = None,
    send_close_notify: bool = None,
    signature_algorithm: str = None,
    ssl_rating: make_dataclass(
        "ssl_rating",
        [
            ("compatibility_rating", str, field(default=None)),
            ("performance_rating", str, field(default=None)),
            ("security_score", str, field(default=None)),
        ],
    ) = None,
    ssl_session_timeout: int = None,
    tags: List[
        make_dataclass("tags", [("value", str), ("type", str, field(default=None))])
    ] = None,
    tenant_ref: str = None,
    type: str = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:
        resource_id(str):
            Alb.ssl_profile unique ID.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

        accepted_ciphers(str, Optional):
            Ciphers suites represented as defined by https //www.openssl.org/docs/man1.1.1/man1/ciphers.html. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        accepted_versions(List[dict[str, Any]], Optional):
            Set of versions accepted by the server. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * type (str):
                 Enum options - SSL_VERSION_SSLV3, SSL_VERSION_TLS1, SSL_VERSION_TLS1_1, SSL_VERSION_TLS1_2, SSL_VERSION_TLS1_3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- SSL_VERSION_SSLV3,SSL_VERSION_TLS1,SSL_VERSION_TLS1_1,SSL_VERSION_TLS1_2), Basic edition(Allowed values- SSL_VERSION_SSLV3,SSL_VERSION_TLS1,SSL_VERSION_TLS1_1,SSL_VERSION_TLS1_2), Enterprise with Cloud Services edition.

        cipher_enums(List[str], Optional):
             Enum options - TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384, TLS_RSA_WITH_AES_128_GCM_SHA256, TLS_RSA_WITH_AES_256_GCM_SHA384, TLS_RSA_WITH_AES_128_CBC_SHA256, TLS_RSA_WITH_AES_256_CBC_SHA256, TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA, TLS_RSA_WITH_AES_128_CBC_SHA, TLS_RSA_WITH_AES_256_CBC_SHA, TLS_RSA_WITH_3DES_EDE_CBC_SHA, TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256, TLS_AES_128_GCM_SHA256. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_CBC_SHA256,TLS_RSA_WITH_AES_256_CBC_SHA256,TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_3DES_EDE_CBC_SHA), Basic edition(Allowed values- TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_CBC_SHA256,TLS_RSA_WITH_AES_256_CBC_SHA256,TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_3DES_EDE_CBC_SHA), Enterprise with Cloud Services edition. Defaults to None.

        ciphersuites(str, Optional):
            TLS 1.3 Ciphers suites represented as defined by U(https //www.openssl.org/docs/man1.1.1/man1/ciphers.html). Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Special default for Essentials edition is TLS_AES_256_GCM_SHA384-TLS_AES_128_GCM_SHA256, Basic edition is TLS_AES_256_GCM_SHA384-TLS_AES_128_GCM_SHA256, Enterprise is TLS_AES_256_GCM_SHA384-TLS_CHACHA20_POLY1305_SHA256-TLS_AES_128_GCM_SHA256. Defaults to None.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        description(str, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        dhparam(str, Optional):
            DH Parameters used in SSL. At this time, it is not configurable and is set to 2048 bits. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ec_named_curve(str, Optional):
            Elliptic Curve Cryptography NamedCurves (TLS Supported Groups)represented as defined by RFC 8422-Section 5.1.1 andhttps //www.openssl.org/docs/man1.1.0/man3/SSL_CTX_set1_curves.html. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        enable_early_data(bool, Optional):
            Enable early data processing for TLS1.3 connections. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        enable_ssl_session_reuse(bool, Optional):
            Enable SSL session re-use. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        is_federated(bool, Optional):
            It Specifies whether the object has to be replicated to the GSLB followers. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        prefer_client_cipher_ordering(bool, Optional):
            Prefer the SSL cipher ordering presented by the client during the SSL handshake over the one specified in the SSL Profile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        send_close_notify(bool, Optional):
            Send 'close notify' alert message for a clean shutdown of the SSL connection. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        signature_algorithm(str, Optional):
            Signature Algorithms represented as defined by RFC5246-Section 7.4.1.4.1 andhttps //www.openssl.org/docs/man1.1.0/man3/SSL_CTX_set1_client_sigalgs_list.html. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ssl_rating(dict[str, Any], Optional):
            ssl_rating. Defaults to None.

            * compatibility_rating (str, Optional):
                 Enum options - SSL_SCORE_NOT_SECURE, SSL_SCORE_VERY_BAD, SSL_SCORE_BAD, SSL_SCORE_AVERAGE, SSL_SCORE_GOOD, SSL_SCORE_EXCELLENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * performance_rating (str, Optional):
                 Enum options - SSL_SCORE_NOT_SECURE, SSL_SCORE_VERY_BAD, SSL_SCORE_BAD, SSL_SCORE_AVERAGE, SSL_SCORE_GOOD, SSL_SCORE_EXCELLENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * security_score (str, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        ssl_session_timeout(int, Optional):
            The amount of time in seconds before an SSL session expires. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        tags(List[dict[str, Any]], Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * type (str, Optional):
                 Enum options - AVI_DEFINED, USER_DEFINED, VCENTER_DEFINED. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * value (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        type(str, Optional):
            SSL Profile Type. Enum options - SSL_PROFILE_TYPE_APPLICATION, SSL_PROFILE_TYPE_SYSTEM. Field introduced in 17.2.8. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              nsx_alb.alb.ssl_profile.present:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.ssl_profile.update resource_id=value
    """

    result = dict(comment=[], ret=[], result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "accepted_ciphers": "accepted_ciphers",
        "accepted_versions": "accepted_versions",
        "cipher_enums": "cipher_enums",
        "ciphersuites": "ciphersuites",
        "configpb_attributes": "configpb_attributes",
        "description": "description",
        "dhparam": "dhparam",
        "ec_named_curve": "ec_named_curve",
        "enable_early_data": "enable_early_data",
        "enable_ssl_session_reuse": "enable_ssl_session_reuse",
        "is_federated": "is_federated",
        "markers": "markers",
        "name": "name",
        "prefer_client_cipher_ordering": "prefer_client_cipher_ordering",
        "send_close_notify": "send_close_notify",
        "signature_algorithm": "signature_algorithm",
        "ssl_rating": "ssl_rating",
        "ssl_session_timeout": "ssl_session_timeout",
        "tags": "tags",
        "tenant_ref": "tenant_ref",
        "type": "type",
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
            path="/sslprofile/{uuid}".format(**{"uuid": resource_id}),
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
            f"Updated nsx_alb.alb.ssl_profile '{name}'",
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
            Alb.ssl_profile unique ID.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              nsx_alb.alb.ssl_profile.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.ssl_profile.delete resource_id=value
    """

    result = dict(comment=[], ret=[], result=True)

    before = await hub.exec.nsx_alb.alb.ssl_profile.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )
    if before["ret"]:
        tenant_name = before["ret"]["tenant_ref"].split("#")[-1]
    delete = await hub.tool.nsx_alb.session.request(
        ctx,
        method="delete",
        path="/sslprofile/{uuid}".format(**{"uuid": resource_id}),
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
