"""States module for managing Alb Ssl Profiles. """
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
        name(str):
            Idem name of the resource.

        resource_id(str, Optional):
            Alb.ssl_profile unique ID. Defaults to None.

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

    Example:
        .. code-block:: sls


          idem_test_nsx_alb.alb.ssl_profile_is_present:
              nsx_alb.nsx_alb.alb.ssl_profile.present:
              - accepted_ciphers: string
              - accepted_versions:
                - type_: string
              - cipher_enums:
                - value
              - ciphersuites: string
              - configpb_attributes:
                  version: int
              - description: string
              - dhparam: string
              - ec_named_curve: string
              - enable_early_data: bool
              - enable_ssl_session_reuse: bool
              - is_federated: bool
              - markers:
                - key: string
                  values:
                  - value
              - prefer_client_cipher_ordering: bool
              - send_close_notify: bool
              - signature_algorithm: string
              - ssl_rating:
                  compatibility_rating: string
                  performance_rating: string
                  security_score: string
              - ssl_session_timeout: int
              - tags:
                - type_: string
                  value: string
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
        before = await hub.exec.nsx_alb.alb.ssl_profile.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )

        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = before.ret

        result["comment"].append(f"'nsx_alb.alb.ssl_profile:{name}' already exists")

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

        before = await hub.exec.nsx_alb.alb.ssl_profile.get(
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
                    before = await hub.exec.nsx_alb.alb.ssl_profile.get(
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
                result["comment"] = (f"Would update nsx_alb.alb.ssl_profile '{name}'",)
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.nsx_alb.alb.ssl_profile.update(
                    ctx,
                    name=name,
                    resource_id=resource_id,
                    **{
                        "accepted_ciphers": accepted_ciphers,
                        "accepted_versions": accepted_versions,
                        "cipher_enums": cipher_enums,
                        "ciphersuites": ciphersuites,
                        "configpb_attributes": configpb_attributes,
                        "description": description,
                        "dhparam": dhparam,
                        "ec_named_curve": ec_named_curve,
                        "enable_early_data": enable_early_data,
                        "enable_ssl_session_reuse": enable_ssl_session_reuse,
                        "is_federated": is_federated,
                        "markers": markers,
                        "prefer_client_cipher_ordering": prefer_client_cipher_ordering,
                        "send_close_notify": send_close_notify,
                        "signature_algorithm": signature_algorithm,
                        "ssl_rating": ssl_rating,
                        "ssl_session_timeout": ssl_session_timeout,
                        "tags": tags,
                        "tenant_ref": tenant_ref,
                        "type": type,
                    },
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"].append(
                        f"Updated 'nsx_alb.alb.ssl_profile:{name}'"
                    )
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.test:
            result["new_state"] = hub.tool.nsx_alb.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"] = (f"Would create nsx_alb.alb.ssl_profile {name}",)
            return result
        else:
            create_ret = await hub.exec.nsx_alb.alb.ssl_profile.create(
                ctx,
                name=name,
                **{
                    "resource_id": resource_id,
                    "accepted_ciphers": accepted_ciphers,
                    "accepted_versions": accepted_versions,
                    "cipher_enums": cipher_enums,
                    "ciphersuites": ciphersuites,
                    "configpb_attributes": configpb_attributes,
                    "description": description,
                    "dhparam": dhparam,
                    "ec_named_curve": ec_named_curve,
                    "enable_early_data": enable_early_data,
                    "enable_ssl_session_reuse": enable_ssl_session_reuse,
                    "is_federated": is_federated,
                    "markers": markers,
                    "prefer_client_cipher_ordering": prefer_client_cipher_ordering,
                    "send_close_notify": send_close_notify,
                    "signature_algorithm": signature_algorithm,
                    "ssl_rating": ssl_rating,
                    "ssl_session_timeout": ssl_session_timeout,
                    "tags": tags,
                    "tenant_ref": tenant_ref,
                    "type": type,
                },
            )
            result["result"] = create_ret["result"]

            if result["result"]:
                result["comment"].append(f"Created 'nsx_alb.alb.ssl_profile:{name}'")
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

    after = await hub.exec.nsx_alb.alb.ssl_profile.get(
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
            Alb.ssl_profile unique ID. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


            idem_test_nsx_alb.alb.ssl_profile_is_absent:
              nsx_alb.nsx_alb.alb.ssl_profile.absent:

    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        result["comment"].append(f"'nsx_alb.alb.ssl_profile:{name}' already absent")
        return result

    before = await hub.exec.nsx_alb.alb.ssl_profile.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    if before["ret"]:
        if ctx.test:
            result["comment"] = f"Would delete nsx_alb.alb.ssl_profile:{name}"
            return result

        delete_ret = await hub.exec.nsx_alb.alb.ssl_profile.delete(
            ctx,
            name=name,
            resource_id=resource_id,
        )
        result["result"] = delete_ret["result"]

        if result["result"]:
            result["comment"].append(f"Deleted 'nsx_alb.alb.ssl_profile:{name}'")
        else:
            # If there is any failure in delete, it should reconcile.
            # The type of data is less important here to use default reconciliation
            # If there are no changes for 3 runs with rerun_data, then it will come out of execution
            result["rerun_data"] = resource_id
            result["comment"].append(delete_ret["result"])
    else:
        result["comment"].append(f"'nsx_alb.alb.ssl_profile:{name}' already absent")
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

            $ idem describe nsx_alb.alb.ssl_profile
    """

    result = {}

    ret = await hub.exec.nsx_alb.alb.ssl_profile.list(ctx)

    if not ret or not ret["result"]:
        hub.log.debug(f"Could not describe nsx_alb.alb.ssl_profile {ret['comment']}")
        return result

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "nsx_alb.alb.ssl_profile.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
