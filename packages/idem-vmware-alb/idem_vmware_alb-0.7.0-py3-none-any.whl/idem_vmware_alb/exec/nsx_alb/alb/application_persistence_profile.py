"""Exec module for managing Alb Application Persistence Profiles. """
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
            Alb.application_persistence_profile unique ID.

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
                - path: nsx_alb.alb.application_persistence_profile.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.application_persistence_profile.get resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)

    get = await hub.tool.nsx_alb.session.request(
        ctx,
        method="get",
        path="/applicationpersistenceprofile/{uuid}?include_name".format(
            **{"uuid": resource_id}
        )
        if resource_id
        else "/applicationpersistenceprofile?include_name",
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
            "app_cookie_persistence_profile": "app_cookie_persistence_profile",
            "configpb_attributes": "configpb_attributes",
            "description": "description",
            "hdr_persistence_profile": "hdr_persistence_profile",
            "http_cookie_persistence_profile": "http_cookie_persistence_profile",
            "ip_persistence_profile": "ip_persistence_profile",
            "is_federated": "is_federated",
            "markers": "markers",
            "name": "name",
            "persistence_type": "persistence_type",
            "server_hm_down_recovery": "server_hm_down_recovery",
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
                - path: nsx_alb.alb.application_persistence_profile.list
                - kwargs:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.application_persistence_profile.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe nsx_alb.alb.application_persistence_profile

    """

    result = dict(comment=[], ret=[], result=True)

    list = await hub.tool.nsx_alb.session.request(
        ctx,
        method="get",
        path="/applicationpersistenceprofile",
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
    persistence_type: str,
    resource_id: str = None,
    name: str = None,
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

        persistence_type(str):
            Method used to persist clients to the same server for a duration of time or a session. Enum options - PERSISTENCE_TYPE_CLIENT_IP_ADDRESS, PERSISTENCE_TYPE_HTTP_COOKIE, PERSISTENCE_TYPE_TLS, PERSISTENCE_TYPE_CLIENT_IPV6_ADDRESS, PERSISTENCE_TYPE_CUSTOM_HTTP_HEADER, PERSISTENCE_TYPE_APP_COOKIE, PERSISTENCE_TYPE_GSLB_SITE. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- PERSISTENCE_TYPE_CLIENT_IP_ADDRESS,PERSISTENCE_TYPE_HTTP_COOKIE), Basic edition(Allowed values- PERSISTENCE_TYPE_CLIENT_IP_ADDRESS,PERSISTENCE_TYPE_HTTP_COOKIE), Enterprise with Cloud Services edition.

        resource_id(str, Optional):
            Alb.application_persistence_profile unique ID. Defaults to None.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

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

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              nsx_alb.alb.application_persistence_profile.present:
                - persistence_type: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.application_persistence_profile.create persistence_type=value
    """

    result = dict(comment=[], ret=[], result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "app_cookie_persistence_profile": "app_cookie_persistence_profile",
        "configpb_attributes": "configpb_attributes",
        "description": "description",
        "hdr_persistence_profile": "hdr_persistence_profile",
        "http_cookie_persistence_profile": "http_cookie_persistence_profile",
        "ip_persistence_profile": "ip_persistence_profile",
        "is_federated": "is_federated",
        "markers": "markers",
        "name": "name",
        "persistence_type": "persistence_type",
        "server_hm_down_recovery": "server_hm_down_recovery",
        "tenant_ref": "tenant_ref",
    }

    payload = {}
    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = value

    create = await hub.tool.nsx_alb.session.request(
        ctx,
        method="post",
        path="/applicationpersistenceprofile",
        query_params={},
        data=payload,
    )

    if not create["result"]:
        result["comment"].append(create["comment"])
        result["result"] = False
        return result

    result["comment"].append(
        f"Created nsx_alb.alb.application_persistence_profile '{name}'",
    )

    result["ret"] = create["ret"]

    result["ret"]["resource_id"] = create["ret"]["uuid"]
    return result


async def update(
    hub,
    ctx,
    resource_id: str,
    persistence_type: str,
    name: str = None,
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
        resource_id(str):
            Alb.application_persistence_profile unique ID.

        persistence_type(str):
            Method used to persist clients to the same server for a duration of time or a session. Enum options - PERSISTENCE_TYPE_CLIENT_IP_ADDRESS, PERSISTENCE_TYPE_HTTP_COOKIE, PERSISTENCE_TYPE_TLS, PERSISTENCE_TYPE_CLIENT_IPV6_ADDRESS, PERSISTENCE_TYPE_CUSTOM_HTTP_HEADER, PERSISTENCE_TYPE_APP_COOKIE, PERSISTENCE_TYPE_GSLB_SITE. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- PERSISTENCE_TYPE_CLIENT_IP_ADDRESS,PERSISTENCE_TYPE_HTTP_COOKIE), Basic edition(Allowed values- PERSISTENCE_TYPE_CLIENT_IP_ADDRESS,PERSISTENCE_TYPE_HTTP_COOKIE), Enterprise with Cloud Services edition.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

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

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              nsx_alb.alb.application_persistence_profile.present:
                - resource_id: value
                - persistence_type: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.application_persistence_profile.update resource_id=value, persistence_type=value
    """

    result = dict(comment=[], ret=[], result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "app_cookie_persistence_profile": "app_cookie_persistence_profile",
        "configpb_attributes": "configpb_attributes",
        "description": "description",
        "hdr_persistence_profile": "hdr_persistence_profile",
        "http_cookie_persistence_profile": "http_cookie_persistence_profile",
        "ip_persistence_profile": "ip_persistence_profile",
        "is_federated": "is_federated",
        "markers": "markers",
        "name": "name",
        "persistence_type": "persistence_type",
        "server_hm_down_recovery": "server_hm_down_recovery",
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
            path="/applicationpersistenceprofile/{uuid}".format(
                **{"uuid": resource_id}
            ),
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
            f"Updated nsx_alb.alb.application_persistence_profile '{name}'",
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
            Alb.application_persistence_profile unique ID.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              nsx_alb.alb.application_persistence_profile.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.application_persistence_profile.delete resource_id=value
    """

    result = dict(comment=[], ret=[], result=True)

    before = await hub.exec.nsx_alb.alb.application_persistence_profile.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )
    if before["ret"]:
        tenant_name = before["ret"]["tenant_ref"].split("#")[-1]

    delete = await hub.tool.nsx_alb.session.request(
        ctx,
        method="delete",
        path="/applicationpersistenceprofile/{uuid}".format(**{"uuid": resource_id}),
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
