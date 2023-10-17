"""States module for managing Alb Application Persistence Profiles. """
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
    persistence_type: str,
    resource_id: str = None,
    app_cookie_persistence_profile: make_dataclass(
        "app_cookie_persistence_profile",
        [
            ("prst_hdr_name", str),
            ("encryption_key", str, field(default=None)),
            ("timeout", int, field(default=None)),
        ],
    ) = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    description: str = None,
    hdr_persistence_profile: make_dataclass(
        "hdr_persistence_profile", [("prst_hdr_name", str, field(default=None))]
    ) = None,
    http_cookie_persistence_profile: make_dataclass(
        "http_cookie_persistence_profile",
        [
            ("always_send_cookie", bool, field(default=None)),
            ("cookie_name", str, field(default=None)),
            ("encryption_key", str, field(default=None)),
            ("http_only", bool, field(default=None)),
            ("is_persistent_cookie", bool, field(default=None)),
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
            ("timeout", int, field(default=None)),
        ],
    ) = None,
    ip_persistence_profile: make_dataclass(
        "ip_persistence_profile",
        [
            ("ip_mask", int, field(default=None)),
            ("ip_persistent_timeout", int, field(default=None)),
        ],
    ) = None,
    is_federated: bool = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    server_hm_down_recovery: str = None,
    tenant_ref: str = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:
        name(str):
            Idem name of the resource.

        persistence_type(str):
            Method used to persist clients to the same server for a duration of time or a session. Enum options - PERSISTENCE_TYPE_CLIENT_IP_ADDRESS, PERSISTENCE_TYPE_HTTP_COOKIE, PERSISTENCE_TYPE_TLS, PERSISTENCE_TYPE_CLIENT_IPV6_ADDRESS, PERSISTENCE_TYPE_CUSTOM_HTTP_HEADER, PERSISTENCE_TYPE_APP_COOKIE, PERSISTENCE_TYPE_GSLB_SITE. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- PERSISTENCE_TYPE_CLIENT_IP_ADDRESS,PERSISTENCE_TYPE_HTTP_COOKIE), Basic edition(Allowed values- PERSISTENCE_TYPE_CLIENT_IP_ADDRESS,PERSISTENCE_TYPE_HTTP_COOKIE), Enterprise with Cloud Services edition.

        resource_id(str, Optional):
            Alb.application_persistence_profile unique ID. Defaults to None.

        app_cookie_persistence_profile(dict[str, Any], Optional):
            app_cookie_persistence_profile. Defaults to None.

            * encryption_key (str, Optional):
                Key to use for cookie encryption. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * prst_hdr_name (str):
                Header or cookie name for application cookie persistence. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * timeout (int, Optional):
                The length of time after a client's connections have closed before expiring the client's persistence to a server. Allowed values are 1-720. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        description(str, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        hdr_persistence_profile(dict[str, Any], Optional):
            hdr_persistence_profile. Defaults to None.

            * prst_hdr_name (str, Optional):
                Header name for custom header persistence. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        http_cookie_persistence_profile(dict[str, Any], Optional):
            http_cookie_persistence_profile. Defaults to None.

            * always_send_cookie (bool, Optional):
                If no persistence cookie was received from the client, always send it. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * cookie_name (str, Optional):
                HTTP cookie name for cookie persistence. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * encryption_key (str, Optional):
                Key name to use for cookie encryption. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_only (bool, Optional):
                Sets the HttpOnly attribute in the cookie. Setting this helps to prevent the client side scripts from accessing this cookie, if supported by browser. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * is_persistent_cookie (bool, Optional):
                When True, the cookie used is a persistent cookie, i.e. the cookie shouldn't be used at the end of the timeout. By default, it is set to false, making the cookie a session cookie, which allows clients to use it even after the timeout, if the session is still open. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * key (List[dict[str, Any]], Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * aes_key (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * hmac_key (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str, Optional):
                    name to use for cookie encryption. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * timeout (int, Optional):
                The maximum lifetime of any session cookie. No value or 'zero' indicates no timeout. Allowed values are 1-14400. Special values are 0- No Timeout. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        ip_persistence_profile(dict[str, Any], Optional):
            ip_persistence_profile. Defaults to None.

            * ip_mask (int, Optional):
                Mask to be applied on client IP. This may be used to persist clients from a subnet to the same server. When set to 0, all requests are sent to the same server. Allowed values are 0-128. Field introduced in 18.2.7. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ip_persistent_timeout (int, Optional):
                The length of time after a client's connections have closed before expiring the client's persistence to a server. Allowed values are 1-720. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        is_federated(bool, Optional):
            This field describes the object's replication scope. If the field is set to false, then the object is visible within the controller-cluster and its associated service-engines.  If the field is set to true, then the object is replicated across the federation.  . Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        server_hm_down_recovery(str, Optional):
            Specifies behavior when a persistent server has been marked down by a health monitor. Enum options - HM_DOWN_PICK_NEW_SERVER, HM_DOWN_ABORT_CONNECTION, HM_DOWN_CONTINUE_PERSISTENT_SERVER. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- HM_DOWN_PICK_NEW_SERVER), Basic edition(Allowed values- HM_DOWN_PICK_NEW_SERVER), Enterprise with Cloud Services edition. Defaults to None.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


          idem_test_nsx_alb.alb.application_persistence_profile_is_present:
              nsx_alb.nsx_alb.alb.application_persistence_profile.present:
              - app_cookie_persistence_profile:
                  encryption_key: string
                  prst_hdr_name: string
                  timeout: int
              - configpb_attributes:
                  version: int
              - description: string
              - hdr_persistence_profile:
                  prst_hdr_name: string
              - http_cookie_persistence_profile:
                  always_send_cookie: bool
                  cookie_name: string
                  encryption_key: string
                  http_only: bool
                  is_persistent_cookie: bool
                  key:
                  - aes_key: string
                    hmac_key: string
                    name: string
                  timeout: int
              - ip_persistence_profile:
                  ip_mask: int
                  ip_persistent_timeout: int
              - is_federated: bool
              - markers:
                - key: string
                  values:
                  - value
              - persistence_type: string
              - server_hm_down_recovery: string
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
        before = await hub.exec.nsx_alb.alb.application_persistence_profile.get(
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
            f"'nsx_alb.alb.application_persistence_profile:{name}' already exists"
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

        before = await hub.exec.nsx_alb.alb.application_persistence_profile.get(
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
                    before = (
                        await hub.exec.nsx_alb.alb.application_persistence_profile.get(
                            ctx,
                            name=name,
                            resource_id=resource_id,
                        )
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
                    f"Would update nsx_alb.alb.application_persistence_profile '{name}'",
                )
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.nsx_alb.alb.application_persistence_profile.update(
                    ctx,
                    name=name,
                    resource_id=resource_id,
                    **{
                        "app_cookie_persistence_profile": app_cookie_persistence_profile,
                        "configpb_attributes": configpb_attributes,
                        "description": description,
                        "hdr_persistence_profile": hdr_persistence_profile,
                        "http_cookie_persistence_profile": http_cookie_persistence_profile,
                        "ip_persistence_profile": ip_persistence_profile,
                        "is_federated": is_federated,
                        "markers": markers,
                        "persistence_type": persistence_type,
                        "server_hm_down_recovery": server_hm_down_recovery,
                        "tenant_ref": tenant_ref,
                    },
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"].append(
                        f"Updated 'nsx_alb.alb.application_persistence_profile:{name}'"
                    )
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.test:
            result["new_state"] = hub.tool.nsx_alb.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"] = (
                f"Would create nsx_alb.alb.application_persistence_profile {name}",
            )
            return result
        else:
            create_ret = await hub.exec.nsx_alb.alb.application_persistence_profile.create(
                ctx,
                name=name,
                **{
                    "resource_id": resource_id,
                    "app_cookie_persistence_profile": app_cookie_persistence_profile,
                    "configpb_attributes": configpb_attributes,
                    "description": description,
                    "hdr_persistence_profile": hdr_persistence_profile,
                    "http_cookie_persistence_profile": http_cookie_persistence_profile,
                    "ip_persistence_profile": ip_persistence_profile,
                    "is_federated": is_federated,
                    "markers": markers,
                    "persistence_type": persistence_type,
                    "server_hm_down_recovery": server_hm_down_recovery,
                    "tenant_ref": tenant_ref,
                },
            )
            result["result"] = create_ret["result"]

            if result["result"]:
                result["comment"].append(
                    f"Created 'nsx_alb.alb.application_persistence_profile:{name}'"
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

    after = await hub.exec.nsx_alb.alb.application_persistence_profile.get(
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
            Alb.application_persistence_profile unique ID. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


            idem_test_nsx_alb.alb.application_persistence_profile_is_absent:
              nsx_alb.nsx_alb.alb.application_persistence_profile.absent:


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        result["comment"].append(
            f"'nsx_alb.alb.application_persistence_profile:{name}' already absent"
        )
        return result

    before = await hub.exec.nsx_alb.alb.application_persistence_profile.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    if before["ret"]:
        if ctx.test:
            result[
                "comment"
            ] = f"Would delete nsx_alb.alb.application_persistence_profile:{name}"
            return result

        delete_ret = await hub.exec.nsx_alb.alb.application_persistence_profile.delete(
            ctx,
            name=name,
            resource_id=resource_id,
        )
        result["result"] = delete_ret["result"]

        if result["result"]:
            result["comment"].append(
                f"Deleted 'nsx_alb.alb.application_persistence_profile:{name}'"
            )
        else:
            # If there is any failure in delete, it should reconcile.
            # The type of data is less important here to use default reconciliation
            # If there are no changes for 3 runs with rerun_data, then it will come out of execution
            result["rerun_data"] = resource_id
            result["comment"].append(delete_ret["result"])
    else:
        result["comment"].append(
            f"'nsx_alb.alb.application_persistence_profile:{name}' already absent"
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

            $ idem describe nsx_alb.alb.application_persistence_profile
    """

    result = {}

    ret = await hub.exec.nsx_alb.alb.application_persistence_profile.list(ctx)

    if not ret or not ret["result"]:
        hub.log.debug(
            f"Could not describe nsx_alb.alb.application_persistence_profile {ret['comment']}"
        )
        return result

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "nsx_alb.alb.application_persistence_profile.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
