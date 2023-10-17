"""Exec module for managing Alb Clouds. """
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
            Alb.cloud unique ID.

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
                - path: nsx_alb.alb.cloud.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.cloud.get resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)

    get = await hub.tool.nsx_alb.session.request(
        ctx,
        method="get",
        path="/cloud/{uuid}?include_name".format(**{"uuid": resource_id})
        if resource_id
        else "/cloud?include_name",
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
            "autoscale_polling_interval": "autoscale_polling_interval",
            "aws_configuration": "aws_configuration",
            "azure_configuration": "azure_configuration",
            "cloudstack_configuration": "cloudstack_configuration",
            "configpb_attributes": "configpb_attributes",
            "custom_tags": "custom_tags",
            "dhcp_enabled": "dhcp_enabled",
            "dns_provider_ref": "dns_provider_ref",
            "dns_resolution_on_se": "dns_resolution_on_se",
            "dns_resolvers": "dns_resolvers",
            "docker_configuration": "docker_configuration",
            "east_west_dns_provider_ref": "east_west_dns_provider_ref",
            "east_west_ipam_provider_ref": "east_west_ipam_provider_ref",
            "enable_vip_on_all_interfaces": "enable_vip_on_all_interfaces",
            "enable_vip_static_routes": "enable_vip_static_routes",
            "gcp_configuration": "gcp_configuration",
            "ip6_autocfg_enabled": "ip6_autocfg_enabled",
            "ipam_provider_ref": "ipam_provider_ref",
            "license_tier": "license_tier",
            "license_type": "license_type",
            "linuxserver_configuration": "linuxserver_configuration",
            "maintenance_mode": "maintenance_mode",
            "markers": "markers",
            "metrics_polling_interval": "metrics_polling_interval",
            "mtu": "mtu",
            "name": "name",
            "nsxt_configuration": "nsxt_configuration",
            "ntp_configuration": "ntp_configuration",
            "obj_name_prefix": "obj_name_prefix",
            "openstack_configuration": "openstack_configuration",
            "prefer_static_routes": "prefer_static_routes",
            "proxy_configuration": "proxy_configuration",
            "rancher_configuration": "rancher_configuration",
            "se_group_template_ref": "se_group_template_ref",
            "state_based_dns_registration": "state_based_dns_registration",
            "tenant_ref": "tenant_ref",
            "vca_configuration": "vca_configuration",
            "vcenter_configuration": "vcenter_configuration",
            "vmc_deployment": "vmc_deployment",
            "vtype": "vtype",
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
                - path: nsx_alb.alb.cloud.list
                - kwargs:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.cloud.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe nsx_alb.alb.cloud

    """

    result = dict(comment=[], ret=[], result=True)

    list = await hub.tool.nsx_alb.session.request(
        ctx,
        method="get",
        path="/cloud",
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
    vtype: str,
    resource_id: str = None,
    name: str = None,
    autoscale_polling_interval: int = None,
    aws_configuration: make_dataclass(
        "aws_configuration",
        [
            ("vpc_id", str),
            ("access_key_id", str, field(default=None)),
            ("asg_poll_interval", int, field(default=None)),
            (
                "ebs_encryption",
                make_dataclass(
                    "ebs_encryption",
                    [
                        ("master_key", str, field(default=None)),
                        ("mode", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("free_elasticips", bool, field(default=None)),
            ("iam_assume_role", str, field(default=None)),
            ("publish_vip_to_public_zone", bool, field(default=None)),
            ("region", str, field(default=None)),
            ("route53_integration", bool, field(default=None)),
            (
                "s3_encryption",
                make_dataclass(
                    "s3_encryption",
                    [
                        ("master_key", str, field(default=None)),
                        ("mode", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("secret_access_key", str, field(default=None)),
            (
                "sqs_encryption",
                make_dataclass(
                    "sqs_encryption",
                    [
                        ("master_key", str, field(default=None)),
                        ("mode", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("ttl", int, field(default=None)),
            ("use_iam_roles", bool, field(default=None)),
            ("use_sns_sqs", bool, field(default=None)),
            ("vpc", str, field(default=None)),
            (
                "zones",
                List[
                    make_dataclass(
                        "zones",
                        [
                            ("availability_zone", str),
                            ("mgmt_network_name", str),
                            ("mgmt_network_uuid", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
        ],
    ) = None,
    azure_configuration: make_dataclass(
        "azure_configuration",
        [
            ("availability_zones", List[str], field(default=None)),
            ("cloud_credentials_ref", str, field(default=None)),
            ("des_id", str, field(default=None)),
            ("location", str, field(default=None)),
            (
                "network_info",
                List[
                    make_dataclass(
                        "network_info",
                        [
                            ("management_network_id", str, field(default=None)),
                            ("se_network_id", str, field(default=None)),
                            ("virtual_network_id", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("resource_group", str, field(default=None)),
            ("se_storage_account", str, field(default=None)),
            ("subscription_id", str, field(default=None)),
            ("use_azure_dns", bool, field(default=None)),
            ("use_enhanced_ha", bool, field(default=None)),
            ("use_managed_disks", bool, field(default=None)),
            ("use_standard_alb", bool, field(default=None)),
        ],
    ) = None,
    cloudstack_configuration: make_dataclass(
        "cloudstack_configuration",
        [
            ("access_key_id", str),
            ("api_url", str),
            ("mgmt_network_name", str),
            ("secret_access_key", str),
            ("cntr_public_ip", str, field(default=None)),
            ("hypervisor", str, field(default=None)),
            ("mgmt_network_uuid", str, field(default=None)),
        ],
    ) = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    custom_tags: List[
        make_dataclass(
            "custom_tags", [("tag_key", str), ("tag_val", str, field(default=None))]
        )
    ] = None,
    dhcp_enabled: bool = None,
    dns_provider_ref: str = None,
    dns_resolution_on_se: bool = None,
    dns_resolvers: List[
        make_dataclass(
            "dns_resolvers",
            [
                ("resolver_name", str),
                ("fixed_ttl", int, field(default=None)),
                ("min_ttl", int, field(default=None)),
                (
                    "nameserver_ips",
                    List[
                        make_dataclass("nameserver_ips", [("addr", str), ("type", str)])
                    ],
                    field(default=None),
                ),
                ("use_mgmt", bool, field(default=None)),
            ],
        )
    ] = None,
    docker_configuration: make_dataclass(
        "docker_configuration",
        [
            ("app_sync_frequency", int, field(default=None)),
            ("ca_tls_key_and_certificate_ref", str, field(default=None)),
            ("client_tls_key_and_certificate_ref", str, field(default=None)),
            ("container_port_match_http_service", bool, field(default=None)),
            ("coredump_directory", str, field(default=None)),
            ("disable_auto_backend_service_sync", bool, field(default=None)),
            ("disable_auto_frontend_service_sync", bool, field(default=None)),
            ("disable_auto_se_creation", bool, field(default=None)),
            (
                "docker_registry_se",
                make_dataclass(
                    "docker_registry_se",
                    [
                        (
                            "oshift_registry",
                            make_dataclass(
                                "oshift_registry",
                                [
                                    ("registry_namespace", str, field(default=None)),
                                    ("registry_service", str, field(default=None)),
                                    (
                                        "registry_vip",
                                        make_dataclass(
                                            "registry_vip",
                                            [("addr", str), ("type", str)],
                                        ),
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("password", str, field(default=None)),
                        ("private", bool, field(default=None)),
                        ("registry", str, field(default=None)),
                        ("username", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "east_west_placement_subnet",
                make_dataclass(
                    "east_west_placement_subnet",
                    [
                        (
                            "ip_addr",
                            make_dataclass("ip_addr", [("addr", str), ("type", str)]),
                        ),
                        ("mask", int),
                    ],
                ),
                field(default=None),
            ),
            ("enable_event_subscription", bool, field(default=None)),
            ("feproxy_container_port_as_service", bool, field(default=None)),
            ("feproxy_vips_enable_proxy_arp", bool, field(default=None)),
            ("fleet_endpoint", str, field(default=None)),
            ("http_container_ports", List[int], field(default=None)),
            ("se_deployment_method", str, field(default=None)),
            (
                "se_exclude_attributes",
                List[
                    make_dataclass(
                        "se_exclude_attributes",
                        [("attribute", str), ("value", str, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            (
                "se_include_attributes",
                List[
                    make_dataclass(
                        "se_include_attributes",
                        [("attribute", str), ("value", str, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            ("se_spawn_rate", int, field(default=None)),
            ("se_volume", str, field(default=None)),
            ("services_accessible_all_interfaces", bool, field(default=None)),
            ("ssh_user_ref", str, field(default=None)),
            ("ucp_nodes", List[str], field(default=None)),
            ("use_container_ip_port", bool, field(default=None)),
            ("use_controller_image", bool, field(default=None)),
        ],
    ) = None,
    east_west_dns_provider_ref: str = None,
    east_west_ipam_provider_ref: str = None,
    enable_vip_on_all_interfaces: bool = None,
    enable_vip_static_routes: bool = None,
    gcp_configuration: make_dataclass(
        "gcp_configuration",
        [
            (
                "network_config",
                make_dataclass(
                    "network_config",
                    [
                        ("config", str),
                        (
                            "inband",
                            make_dataclass(
                                "inband",
                                [
                                    ("vpc_network_name", str),
                                    ("vpc_subnet_name", str),
                                    ("vpc_project_id", str, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "one_arm",
                            make_dataclass(
                                "one_arm",
                                [
                                    ("data_vpc_network_name", str),
                                    ("data_vpc_subnet_name", str),
                                    ("management_vpc_network_name", str),
                                    ("management_vpc_subnet_name", str),
                                    ("data_vpc_project_id", str, field(default=None)),
                                    (
                                        "management_vpc_project_id",
                                        str,
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "two_arm",
                            make_dataclass(
                                "two_arm",
                                [
                                    ("backend_data_vpc_network_name", str),
                                    ("backend_data_vpc_subnet_name", str),
                                    ("frontend_data_vpc_network_name", str),
                                    ("frontend_data_vpc_subnet_name", str),
                                    ("management_vpc_network_name", str),
                                    ("management_vpc_subnet_name", str),
                                    (
                                        "backend_data_vpc_project_id",
                                        str,
                                        field(default=None),
                                    ),
                                    (
                                        "frontend_data_vpc_project_id",
                                        str,
                                        field(default=None),
                                    ),
                                    (
                                        "management_vpc_project_id",
                                        str,
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
            ),
            ("region_name", str),
            ("se_project_id", str),
            (
                "vip_allocation_strategy",
                make_dataclass(
                    "vip_allocation_strategy",
                    [
                        ("mode", str),
                        (
                            "ilb",
                            make_dataclass(
                                "ilb",
                                [
                                    (
                                        "cloud_router_names",
                                        List[str],
                                        field(default=None),
                                    )
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "routes",
                            make_dataclass(
                                "routes",
                                [
                                    (
                                        "match_se_group_subnet",
                                        bool,
                                        field(default=None),
                                    ),
                                    ("route_priority", int, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
            ),
            ("zones", List[str]),
            ("cloud_credentials_ref", str, field(default=None)),
            (
                "encryption_keys",
                make_dataclass(
                    "encryption_keys",
                    [
                        ("gcs_bucket_kms_key_id", str, field(default=None)),
                        ("gcs_objects_kms_key_id", str, field(default=None)),
                        ("se_disk_kms_key_id", str, field(default=None)),
                        ("se_image_kms_key_id", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("firewall_target_tags", List[str], field(default=None)),
            ("gcp_service_account_email", str, field(default=None)),
            ("gcs_bucket_name", str, field(default=None)),
            ("gcs_project_id", str, field(default=None)),
        ],
    ) = None,
    ip6_autocfg_enabled: bool = None,
    ipam_provider_ref: str = None,
    license_tier: str = None,
    license_type: str = None,
    linuxserver_configuration: make_dataclass(
        "linuxserver_configuration",
        [
            (
                "hosts",
                List[
                    make_dataclass(
                        "hosts",
                        [
                            (
                                "host_ip",
                                make_dataclass(
                                    "host_ip", [("addr", str), ("type", str)]
                                ),
                            ),
                            (
                                "host_attr",
                                List[
                                    make_dataclass(
                                        "host_attr",
                                        [
                                            ("attr_key", str),
                                            ("attr_val", str, field(default=None)),
                                        ],
                                    )
                                ],
                                field(default=None),
                            ),
                            ("node_availability_zone", str, field(default=None)),
                            ("se_group_ref", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("se_inband_mgmt", bool, field(default=None)),
            ("se_log_disk_path", str, field(default=None)),
            ("se_log_disk_size_gb", int, field(default=None)),
            ("se_sys_disk_path", str, field(default=None)),
            ("se_sys_disk_size_gb", int, field(default=None)),
            ("ssh_user_ref", str, field(default=None)),
        ],
    ) = None,
    maintenance_mode: bool = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    metrics_polling_interval: int = None,
    mtu: int = None,
    nsxt_configuration: make_dataclass(
        "nsxt_configuration",
        [
            ("automate_dfw_rules", bool, field(default=None)),
            (
                "data_network_config",
                make_dataclass(
                    "data_network_config",
                    [
                        ("transport_zone", str),
                        ("tz_type", str),
                        (
                            "tier1_segment_config",
                            make_dataclass(
                                "tier1_segment_config",
                                [
                                    ("segment_config_mode", str),
                                    (
                                        "automatic",
                                        make_dataclass(
                                            "automatic",
                                            [
                                                (
                                                    "nsxt_segment_subnet",
                                                    make_dataclass(
                                                        "nsxt_segment_subnet",
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
                                                    ),
                                                ),
                                                (
                                                    "num_se_per_segment",
                                                    int,
                                                    field(default=None),
                                                ),
                                                (
                                                    "tier1_lr_ids",
                                                    List[str],
                                                    field(default=None),
                                                ),
                                            ],
                                        ),
                                        field(default=None),
                                    ),
                                    (
                                        "manual",
                                        make_dataclass(
                                            "manual",
                                            [
                                                (
                                                    "tier1_lrs",
                                                    List[
                                                        make_dataclass(
                                                            "tier1_lrs",
                                                            [
                                                                ("tier1_lr_id", str),
                                                                (
                                                                    "locale_service",
                                                                    str,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "segment_id",
                                                                    str,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        )
                                                    ],
                                                    field(default=None),
                                                )
                                            ],
                                        ),
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("vlan_segments", List[str], field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("domain_id", str, field(default=None)),
            ("enforcementpoint_id", str, field(default=None)),
            (
                "management_network_config",
                make_dataclass(
                    "management_network_config",
                    [
                        ("transport_zone", str),
                        ("tz_type", str),
                        (
                            "overlay_segment",
                            make_dataclass(
                                "overlay_segment",
                                [
                                    ("tier1_lr_id", str),
                                    ("locale_service", str, field(default=None)),
                                    ("segment_id", str, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("vlan_segment", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("nsxt_credentials_ref", str, field(default=None)),
            ("nsxt_url", str, field(default=None)),
            ("site_id", str, field(default=None)),
            ("vmc_mode", bool, field(default=None)),
            ("vpc_mode", bool, field(default=None)),
        ],
    ) = None,
    ntp_configuration: make_dataclass(
        "ntp_configuration",
        [
            (
                "ntp_authentication_keys",
                List[
                    make_dataclass(
                        "ntp_authentication_keys",
                        [
                            ("key", str),
                            ("key_number", int),
                            ("algorithm", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            (
                "ntp_server_list",
                List[make_dataclass("ntp_server_list", [("addr", str), ("type", str)])],
                field(default=None),
            ),
            (
                "ntp_servers",
                List[
                    make_dataclass(
                        "ntp_servers",
                        [
                            (
                                "server",
                                make_dataclass(
                                    "server", [("addr", str), ("type", str)]
                                ),
                            ),
                            ("key_number", int, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
        ],
    ) = None,
    obj_name_prefix: str = None,
    openstack_configuration: make_dataclass(
        "openstack_configuration",
        [
            ("admin_tenant", str),
            ("mgmt_network_name", str),
            ("privilege", str),
            ("username", str),
            ("admin_tenant_uuid", str, field(default=None)),
            ("allowed_address_pairs", bool, field(default=None)),
            ("anti_affinity", bool, field(default=None)),
            ("auth_url", str, field(default=None)),
            ("config_drive", bool, field(default=None)),
            ("contrail_disable_policy", bool, field(default=None)),
            ("contrail_endpoint", str, field(default=None)),
            ("contrail_plugin", bool, field(default=None)),
            (
                "custom_se_image_properties",
                List[
                    make_dataclass(
                        "custom_se_image_properties",
                        [("name", str), ("value", str, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            ("enable_os_object_caching", bool, field(default=None)),
            ("enable_tagging", bool, field(default=None)),
            ("external_networks", bool, field(default=None)),
            ("free_floatingips", bool, field(default=None)),
            ("hypervisor", str, field(default=None)),
            (
                "hypervisor_properties",
                List[
                    make_dataclass(
                        "hypervisor_properties",
                        [
                            ("hypervisor", str),
                            (
                                "image_properties",
                                List[
                                    make_dataclass(
                                        "image_properties",
                                        [
                                            ("name", str),
                                            ("value", str, field(default=None)),
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
            ("img_format", str, field(default=None)),
            ("import_keystone_tenants", bool, field(default=None)),
            ("insecure", bool, field(default=None)),
            ("keystone_host", str, field(default=None)),
            ("map_admin_to_cloudadmin", bool, field(default=None)),
            ("mgmt_network_uuid", str, field(default=None)),
            ("name_owner", bool, field(default=None)),
            ("neutron_rbac", bool, field(default=None)),
            ("password", str, field(default=None)),
            ("prov_name", List[str], field(default=None)),
            (
                "provider_vip_networks",
                List[
                    make_dataclass(
                        "provider_vip_networks",
                        [
                            ("os_network_uuid", str, field(default=None)),
                            ("os_tenant_uuids", List[str], field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("region", str, field(default=None)),
            (
                "role_mapping",
                List[
                    make_dataclass(
                        "role_mapping", [("avi_role", str), ("os_role", str)]
                    )
                ],
                field(default=None),
            ),
            ("security_groups", bool, field(default=None)),
            ("tenant_se", bool, field(default=None)),
            ("use_admin_url", bool, field(default=None)),
            ("use_internal_endpoints", bool, field(default=None)),
            ("use_keystone_auth", bool, field(default=None)),
            ("vip_port_in_admin_tenant", bool, field(default=None)),
        ],
    ) = None,
    prefer_static_routes: bool = None,
    proxy_configuration: make_dataclass(
        "proxy_configuration",
        [
            ("host", str),
            ("port", int),
            ("password", str, field(default=None)),
            ("username", str, field(default=None)),
        ],
    ) = None,
    rancher_configuration: make_dataclass(
        "rancher_configuration",
        [
            ("access_key", str, field(default=None)),
            ("app_sync_frequency", int, field(default=None)),
            ("container_port_match_http_service", bool, field(default=None)),
            ("coredump_directory", str, field(default=None)),
            ("disable_auto_backend_service_sync", bool, field(default=None)),
            ("disable_auto_frontend_service_sync", bool, field(default=None)),
            ("disable_auto_se_creation", bool, field(default=None)),
            (
                "docker_registry_se",
                make_dataclass(
                    "docker_registry_se",
                    [
                        (
                            "oshift_registry",
                            make_dataclass(
                                "oshift_registry",
                                [
                                    ("registry_namespace", str, field(default=None)),
                                    ("registry_service", str, field(default=None)),
                                    (
                                        "registry_vip",
                                        make_dataclass(
                                            "registry_vip",
                                            [("addr", str), ("type", str)],
                                        ),
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("password", str, field(default=None)),
                        ("private", bool, field(default=None)),
                        ("registry", str, field(default=None)),
                        ("username", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "east_west_placement_subnet",
                make_dataclass(
                    "east_west_placement_subnet",
                    [
                        (
                            "ip_addr",
                            make_dataclass("ip_addr", [("addr", str), ("type", str)]),
                        ),
                        ("mask", int),
                    ],
                ),
                field(default=None),
            ),
            ("enable_event_subscription", bool, field(default=None)),
            ("feproxy_container_port_as_service", bool, field(default=None)),
            ("feproxy_vips_enable_proxy_arp", bool, field(default=None)),
            ("fleet_endpoint", str, field(default=None)),
            ("http_container_ports", List[int], field(default=None)),
            (
                "nuage_controller",
                make_dataclass(
                    "nuage_controller",
                    [
                        ("nuage_organization", str, field(default=None)),
                        ("nuage_password", str, field(default=None)),
                        ("nuage_port", int, field(default=None)),
                        ("nuage_username", str, field(default=None)),
                        ("nuage_vsd_host", str, field(default=None)),
                        ("se_domain", str, field(default=None)),
                        ("se_enterprise", str, field(default=None)),
                        ("se_network", str, field(default=None)),
                        ("se_policy_group", str, field(default=None)),
                        ("se_user", str, field(default=None)),
                        ("se_zone", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("rancher_servers", List[str], field(default=None)),
            ("se_deployment_method", str, field(default=None)),
            (
                "se_exclude_attributes",
                List[
                    make_dataclass(
                        "se_exclude_attributes",
                        [("attribute", str), ("value", str, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            (
                "se_include_attributes",
                List[
                    make_dataclass(
                        "se_include_attributes",
                        [("attribute", str), ("value", str, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            ("se_spawn_rate", int, field(default=None)),
            ("se_volume", str, field(default=None)),
            ("secret_key", str, field(default=None)),
            ("services_accessible_all_interfaces", bool, field(default=None)),
            ("ssh_user_ref", str, field(default=None)),
            ("use_container_ip_port", bool, field(default=None)),
            ("use_controller_image", bool, field(default=None)),
        ],
    ) = None,
    se_group_template_ref: str = None,
    state_based_dns_registration: bool = None,
    tenant_ref: str = None,
    vca_configuration: make_dataclass(
        "vca_configuration",
        [
            ("privilege", str),
            ("vca_host", str),
            ("vca_instance", str),
            ("vca_mgmt_network", str),
            ("vca_orgnization", str),
            ("vca_password", str),
            ("vca_username", str),
            ("vca_vdc", str),
        ],
    ) = None,
    vcenter_configuration: make_dataclass(
        "vcenter_configuration",
        [
            ("privilege", str),
            (
                "content_lib",
                make_dataclass(
                    "content_lib",
                    [
                        ("id", str, field(default=None)),
                        ("name", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("datacenter", str, field(default=None)),
            ("deactivate_vm_discovery", bool, field(default=None)),
            ("is_nsx_environment", bool, field(default=None)),
            (
                "management_ip_subnet",
                make_dataclass(
                    "management_ip_subnet",
                    [
                        (
                            "ip_addr",
                            make_dataclass("ip_addr", [("addr", str), ("type", str)]),
                        ),
                        ("mask", int),
                    ],
                ),
                field(default=None),
            ),
            ("management_network", str, field(default=None)),
            ("password", str, field(default=None)),
            ("use_content_lib", bool, field(default=None)),
            ("username", str, field(default=None)),
            ("vcenter_template_se_location", str, field(default=None)),
            ("vcenter_url", str, field(default=None)),
        ],
    ) = None,
    vmc_deployment: bool = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:

        vtype(str):
            Cloud type. Enum options - CLOUD_NONE, CLOUD_VCENTER, CLOUD_OPENSTACK, CLOUD_AWS, CLOUD_VCA, CLOUD_APIC, CLOUD_MESOS, CLOUD_LINUXSERVER, CLOUD_DOCKER_UCP, CLOUD_RANCHER, CLOUD_OSHIFT_K8S, CLOUD_AZURE, CLOUD_GCP, CLOUD_NSXT. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- CLOUD_NONE,CLOUD_VCENTER), Basic edition(Allowed values- CLOUD_NONE,CLOUD_NSXT), Enterprise with Cloud Services edition.

        resource_id(str, Optional):
            Alb.cloud unique ID. Defaults to None.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

        autoscale_polling_interval(int, Optional):
            CloudConnector polling interval in seconds for external autoscale groups, minimum 60 seconds. Allowed values are 60-3600. Field introduced in 18.2.2. Unit is SECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 60), Basic edition(Allowed values- 60), Enterprise with Cloud Services edition. Defaults to None.

        aws_configuration(dict[str, Any], Optional):
            aws_configuration. Defaults to None.

            * access_key_id (str, Optional):
                AWS access key ID. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * asg_poll_interval (int, Optional):
                Time interval between periodic polling of all Auto Scaling Groups. Allowed values are 60-1800. Field introduced in 17.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ebs_encryption (dict[str, Any], Optional):
                ebs_encryption

                * master_key (str, Optional):
                    AWS KMS ARN ID of the master key for encryption. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mode (str, Optional):
                    AWS encryption mode. Enum options - AWS_ENCRYPTION_MODE_NONE, AWS_ENCRYPTION_MODE_SSE_KMS. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * free_elasticips (bool, Optional):
                Free unused elastic IP addresses. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * iam_assume_role (str, Optional):
                IAM assume role for cross-account access. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * publish_vip_to_public_zone (bool, Optional):
                If enabled and the virtual service is not floating ip capable, vip will be published to both private and public zones. Field introduced in 17.2.10. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * region (str, Optional):
                AWS region. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * route53_integration (bool, Optional):
                If enabled, create/update DNS entries in Amazon Route 53 zones. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * s3_encryption (dict[str, Any], Optional):
                s3_encryption

                * master_key (str, Optional):
                    AWS KMS ARN ID of the master key for encryption. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mode (str, Optional):
                    AWS encryption mode. Enum options - AWS_ENCRYPTION_MODE_NONE, AWS_ENCRYPTION_MODE_SSE_KMS. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * secret_access_key (str, Optional):
                AWS secret access key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * sqs_encryption (dict[str, Any], Optional):
                sqs_encryption

                * master_key (str, Optional):
                    AWS KMS ARN ID of the master key for encryption. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mode (str, Optional):
                    AWS encryption mode. Enum options - AWS_ENCRYPTION_MODE_NONE, AWS_ENCRYPTION_MODE_SSE_KMS. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ttl (int, Optional):
                Default TTL for all records. Allowed values are 1-172800. Field introduced in 17.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_iam_roles (bool, Optional):
                Use IAM roles instead of access and secret key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_sns_sqs (bool, Optional):
                Use SNS/SQS based notifications for monitoring Auto Scaling Groups. Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vpc (str, Optional):
                VPC name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vpc_id (str):
                VPC ID. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * zones (List[dict[str, Any]], Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * availability_zone (str):
                    Availability zone. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mgmt_network_name (str):
                    Name or CIDR of the network in the Availability Zone that will be used as management network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mgmt_network_uuid (str, Optional):
                    UUID of the network in the Availability Zone that will be used as management network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        azure_configuration(dict[str, Any], Optional):
            azure_configuration. Defaults to None.

            * availability_zones (List[str], Optional):
                Availability zones to be used in Azure. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * cloud_credentials_ref (str, Optional):
                Credentials to access azure cloud. It is a reference to an object of type CloudConnectorUser. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * des_id (str, Optional):
                Disks Encryption Set resource-id (des_id) to encrypt se image and managed disk using customer-managed-keys. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * location (str, Optional):
                Azure location where this cloud will be located. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * network_info (List[dict[str, Any]], Optional):
                Azure virtual network and subnet information. Field introduced in 17.2.1. Minimum of 1 items required. Maximum of 1 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * management_network_id (str, Optional):
                    Id of the Azure subnet used as management network for the Service Engines. If set, Service Engines will have a dedicated management NIC, otherwise, they operate in inband mode. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_network_id (str, Optional):
                    Id of the Azure subnet where Avi Controller will create the Service Engines. . Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * virtual_network_id (str, Optional):
                    Virtual network where Virtual IPs will belong. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * resource_group (str, Optional):
                Azure resource group dedicated for Avi Controller. Avi Controller will create all its resources in this resource group. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_storage_account (str, Optional):
                Storage Account to be used for uploading SE VHD images to Azure. Must include the resource group name. Format '<resource-group> <storage-account-name>'. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * subscription_id (str, Optional):
                Subscription Id for the Azure subscription. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_azure_dns (bool, Optional):
                Azure is the DNS provider. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_enhanced_ha (bool, Optional):
                Use Azure's enhanced HA features. This needs a public IP to be associated with the VIP. . Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_managed_disks (bool, Optional):
                Use Azure managed disks for SE storage. Field introduced in 17.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_standard_alb (bool, Optional):
                Use Standard SKU Azure Load Balancer. By default Basic SKU Load Balancer is used. Field introduced in 17.2.7. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        cloudstack_configuration(dict[str, Any], Optional):
            cloudstack_configuration. Defaults to None.

            * access_key_id (str):
                CloudStack API Key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * api_url (str):
                CloudStack API URL. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * cntr_public_ip (str, Optional):
                If controller's management IP is in a private network, a publicly accessible IP to reach the controller. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * hypervisor (str, Optional):
                Default hypervisor type. Enum options - DEFAULT, VMWARE_ESX, KVM, VMWARE_VSAN, XEN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mgmt_network_name (str):
                Avi Management network name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mgmt_network_uuid (str, Optional):
                Avi Management network name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * secret_access_key (str):
                CloudStack Secret Key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        custom_tags(List[dict[str, Any]], Optional):
            Custom tags for all Avi created resources in the cloud infrastructure. Field introduced in 17.1.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * tag_key (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * tag_val (str, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        dhcp_enabled(bool, Optional):
            Select the IP address management scheme. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        dns_provider_ref(str, Optional):
            DNS Profile for the cloud. It is a reference to an object of type IpamDnsProviderProfile. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dns_resolution_on_se(bool, Optional):
            By default, pool member FQDNs are resolved on the Controller. When this is set, pool member FQDNs are instead resolved on Service Engines in this cloud. This is useful in scenarios where pool member FQDNs can only be resolved from Service Engines and not from the Controller. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        dns_resolvers(List[dict[str, Any]], Optional):
            DNS resolver for the cloud. Field introduced in 20.1.5. Maximum of 1 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * fixed_ttl (int, Optional):
                If configured, this value used for refreshing the DNS entries.Overrides both received_ttl and min_ttl. The entries are refreshed only on fixed_ttleven when received_ttl is less than fixed_ttl. Allowed values are 5-2147483647. Field introduced in 20.1.5. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * min_ttl (int, Optional):
                If configured, the min_ttl overrides the ttl from responses when ttl < min_ttl,effectively ttl = max(recieved_ttl, min_ttl). Allowed values are 5-2147483647. Field introduced in 20.1.5. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * nameserver_ips (List[dict[str, Any]], Optional):
                Name server IPv4 addresses. Field introduced in 20.1.5. Minimum of 1 items required. Maximum of 10 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * resolver_name (str):
                Unique name for resolver config. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * use_mgmt (bool, Optional):
                If enabled, DNS resolution is performed via management network. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        docker_configuration(dict[str, Any], Optional):
            docker_configuration. Defaults to None.

            * app_sync_frequency (int, Optional):
                Sync frequency in seconds with frameworks. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ca_tls_key_and_certificate_ref (str, Optional):
                UUID of the UCP CA TLS cert and key. It is a reference to an object of type SSLKeyAndCertificate. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * client_tls_key_and_certificate_ref (str, Optional):
                UUID of the client TLS cert and key. It is a reference to an object of type SSLKeyAndCertificate. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * container_port_match_http_service (bool, Optional):
                Perform container port matching to create a HTTP Virtualservice instead of a TCP/UDP VirtualService. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * coredump_directory (str, Optional):
                Directory to mount to check for core dumps on Service Engines. This will be mapped read only to /var/crash on any new Service Engines. This is a disruptive change. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disable_auto_backend_service_sync (bool, Optional):
                Disable auto service sync for back end services. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disable_auto_frontend_service_sync (bool, Optional):
                Disable auto service sync for front end services. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disable_auto_se_creation (bool, Optional):
                Disable SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * docker_registry_se (dict[str, Any], Optional):
                docker_registry_se

                * oshift_registry (dict[str, Any], Optional):
                    oshift_registry

                    * registry_namespace (str, Optional):
                        Namespace for the ServiceEngine image to be hosted in Openshift Integrated registry. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * registry_service (str, Optional):
                        Name of the Integrated registry Service in Openshift. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * registry_vip (dict[str, Any], Optional):
                        registry_vip

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * password (str, Optional):
                    Password for docker registry. Authorized 'regular user' password if registry is Openshift integrated registry. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * private (bool, Optional):
                    Set if docker registry is private. Avi controller will not attempt to push SE image to the registry, unless se_repository_push is set. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * registry (str, Optional):
                    Avi ServiceEngine repository name. For private registry, it's registry port/repository, for public registry, it's registry/repository, for openshift registry, it's registry port/namespace/repo. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * username (str, Optional):
                    Username for docker registry. Authorized 'regular user' if registry is Openshift integrated registry. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * east_west_placement_subnet (dict[str, Any], Optional):
                east_west_placement_subnet

                * ip_addr (dict[str, Any]):
                    ip_addr

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mask (int):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enable_event_subscription (bool, Optional):
                Enable Docker event subscription. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * feproxy_container_port_as_service (bool, Optional):
                For Front End proxies, use container port as service port. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * feproxy_vips_enable_proxy_arp (bool, Optional):
                Enable proxy ARP from Host interface for Front End  proxies. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * fleet_endpoint (str, Optional):
                Optional fleet remote endpoint if fleet is used for SE deployment. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_container_ports (List[int], Optional):
                List of container ports that create a HTTP Virtualservice instead of a TCP/UDP VirtualService. Defaults to 80. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_deployment_method (str, Optional):
                Use Fleet/SSH for SE deployment. Enum options - SE_CREATE_FLEET, SE_CREATE_SSH, SE_CREATE_POD. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_exclude_attributes (List[dict[str, Any]], Optional):
                Exclude hosts with attributes for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * attribute (str):
                    Attribute to match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * value (str, Optional):
                    Attribute value. If not set, match any value. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_include_attributes (List[dict[str, Any]], Optional):
                Create SEs just on hosts with include attributes. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * attribute (str):
                    Attribute to match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * value (str, Optional):
                    Attribute value. If not set, match any value. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_spawn_rate (int, Optional):
                New SE spawn rate per minute. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_volume (str, Optional):
                Host volume to be used as a disk for Avi SE, This is a disruptive change. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * services_accessible_all_interfaces (bool, Optional):
                Make service ports accessible on all Host interfaces in addition to East-West VIP and/or bridge IP. Usually enabled AWS clusters to export East-West services on Host interface. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ssh_user_ref (str, Optional):
                Cloud connector user uuid for SSH to hosts. It is a reference to an object of type CloudConnectorUser. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ucp_nodes (List[str], Optional):
                List of Docker UCP nodes; In case of a load balanced UCP cluster, use Virtual IP of the cluster. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_container_ip_port (bool, Optional):
                Use container IP address port for pool instead of host IP address hostport. This mode is applicable if the container IP is reachable (not a private NATed IP) from other hosts in a routed environment for containers. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_controller_image (bool, Optional):
                If true, use controller generated SE docker image via fileservice, else use docker repository image as defined by docker_registry_se. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        east_west_dns_provider_ref(str, Optional):
            DNS Profile for East-West services. It is a reference to an object of type IpamDnsProviderProfile. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        east_west_ipam_provider_ref(str, Optional):
            Ipam Profile for East-West services. Warning - Please use virtual subnets in this IPAM profile that do not conflict with the underlay networks or any overlay networks in the cluster. For example in AWS and GCP, 169.254.0.0/16 is used for storing instance metadata. Hence, it should not be used in this profile. It is a reference to an object of type IpamDnsProviderProfile. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        enable_vip_on_all_interfaces(bool, Optional):
            Enable VIP on all data interfaces for the Cloud. Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        enable_vip_static_routes(bool, Optional):
            Use static routes for VIP side network resolution during VirtualService placement. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        gcp_configuration(dict[str, Any], Optional):
            gcp_configuration. Defaults to None.

            * cloud_credentials_ref (str, Optional):
                Credentials to access Google Cloud Platform APIs. It is a reference to an object of type CloudConnectorUser. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * encryption_keys (dict[str, Any], Optional):
                encryption_keys

                * gcs_bucket_kms_key_id (str, Optional):
                    CMEK Resource ID to encrypt Google Cloud Storage Bucket. This Bucket is used to upload Service Engine raw image. Field introduced in 18.2.10, 20.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * gcs_objects_kms_key_id (str, Optional):
                    CMEK Resource ID to encrypt Service Engine raw image. The raw image is a Google Cloud Storage Object. Field introduced in 18.2.10, 20.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * se_disk_kms_key_id (str, Optional):
                    CMEK Resource ID to encrypt Service Engine Disks. Field introduced in 18.2.10, 20.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * se_image_kms_key_id (str, Optional):
                    CMEK Resource ID to encrypt Service Engine GCE Image. Field introduced in 18.2.10, 20.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * firewall_target_tags (List[str], Optional):
                Firewall rule network target tags which will be applied on Service Engines to allow ingress and egress traffic for Service Engines. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * gcp_service_account_email (str, Optional):
                Email of GCP Service Account to be associated to the Service Engines. Field introduced in 20.1.7, 21.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * gcs_bucket_name (str, Optional):
                Google Cloud Storage Bucket Name where Service Engine image will be uploaded. This image will be deleted once the image is created in Google compute images. By default, a bucket will be created if this field is not specified. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * gcs_project_id (str, Optional):
                Google Cloud Storage Project ID where Service Engine image will be uploaded. This image will be deleted once the image is created in Google compute images. By default, Service Engine Project ID will be used. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * network_config (dict[str, Any]):
                network_config

                * config (str):
                    Config Mode for Google Cloud network configuration. Enum options - INBAND_MANAGEMENT, ONE_ARM_MODE, TWO_ARM_MODE. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * inband (dict[str, Any], Optional):
                    inband

                    * vpc_network_name (str):
                        Service Engine Network Name. Field introduced in 18.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * vpc_project_id (str, Optional):
                        Project ID of the Service Engine Network. By default, Service Engine Project ID will be used. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * vpc_subnet_name (str):
                        Service Engine Network Subnet Name. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * one_arm (dict[str, Any], Optional):
                    one_arm

                    * data_vpc_network_name (str):
                        Service Engine Data Network Name. Field introduced in 18.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * data_vpc_project_id (str, Optional):
                        Project ID of the Service Engine Data Network. By default, Service Engine Project ID will be used. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * data_vpc_subnet_name (str):
                        Service Engine Data Network Subnet Name. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * management_vpc_network_name (str):
                        Service Engine Management Network Name. Field introduced in 18.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * management_vpc_project_id (str, Optional):
                        Project ID of the Service Engine Management Network. By default, Service Engine Project ID will be used. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * management_vpc_subnet_name (str):
                        Service Engine Management Network Subnet Name. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * two_arm (dict[str, Any], Optional):
                    two_arm

                    * backend_data_vpc_network_name (str):
                        Service Engine Backend Data Network Name. Field introduced in 18.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * backend_data_vpc_project_id (str, Optional):
                        Project ID of the Service Engine Backend Data Network. By default, Service Engine Project ID will be used. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * backend_data_vpc_subnet_name (str):
                        Service Engine Backend Data Network Subnet Name. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * frontend_data_vpc_network_name (str):
                        Service Engine Frontend Data Network Name. Field introduced in 18.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * frontend_data_vpc_project_id (str, Optional):
                        Project ID of the Service Engine Frontend Data Network. By default, Service Engine Project ID will be used. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * frontend_data_vpc_subnet_name (str):
                        Service Engine Frontend Data Network Subnet Name. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * management_vpc_network_name (str):
                        Service Engine Management Network Name. Field introduced in 18.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * management_vpc_project_id (str, Optional):
                        Project ID of the Service Engine Management Network. By default, Service Engine Project ID will be used. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * management_vpc_subnet_name (str):
                        Service Engine Management Network Subnet Name. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * region_name (str):
                Google Cloud Platform Region Name where Service Engines will be spawned. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_project_id (str):
                Google Cloud Platform Project ID where Service Engines will be spawned. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vip_allocation_strategy (dict[str, Any]):
                vip_allocation_strategy

                * ilb (dict[str, Any], Optional):
                    ilb

                    * cloud_router_names (List[str], Optional):
                        Google Cloud Router Names to advertise BYOIP. Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mode (str):
                    VIP Allocation Mode. Enum options - ROUTES, ILB. Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * routes (dict[str, Any], Optional):
                    routes

                    * match_se_group_subnet (bool, Optional):
                        Match SE group subnets for VIP placement. Default is to not match SE group subnets. Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * route_priority (int, Optional):
                        Priority of the routes created in GCP. Field introduced in 20.1.7, 21.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * zones (List[str]):
                Google Cloud Platform Zones where Service Engines will be distributed for HA. Field introduced in 18.2.1. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        ip6_autocfg_enabled(bool, Optional):
            Enable IPv6 auto configuration. Field introduced in 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ipam_provider_ref(str, Optional):
            Ipam Profile for the cloud. It is a reference to an object of type IpamDnsProviderProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        license_tier(str, Optional):
            Specifies the default license tier which would be used by new SE Groups. This field by default inherits the value from system configuration. Enum options - ENTERPRISE_16, ENTERPRISE, ENTERPRISE_18, BASIC, ESSENTIALS, ENTERPRISE_WITH_CLOUD_SERVICES. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        license_type(str, Optional):
            If no license type is specified then default license enforcement for the cloud type is chosen. The default mappings are Container Cloud is Max Ses, OpenStack and VMware is cores and linux it is Sockets. Enum options - LIC_BACKEND_SERVERS, LIC_SOCKETS, LIC_CORES, LIC_HOSTS, LIC_SE_BANDWIDTH, LIC_METERED_SE_BANDWIDTH. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        linuxserver_configuration(dict[str, Any], Optional):
            linuxserver_configuration. Defaults to None.

            * hosts (List[dict[str, Any]], Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * host_attr (List[dict[str, Any]], Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * attr_key (str):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * attr_val (str, Optional):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * host_ip (dict[str, Any]):
                    host_ip

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * node_availability_zone (str, Optional):
                    Node's availability zone. ServiceEngines belonging to the availability zone will be rebooted during a manual DR failover. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_group_ref (str, Optional):
                    The SE Group association for the SE. If None, then 'Default-Group' SEGroup is associated with the SE. It is a reference to an object of type ServiceEngineGroup. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_inband_mgmt (bool, Optional):
                Flag to notify the SE's in this cloud have an inband management interface, this can be overridden at SE host level by setting host_attr attr_key as SE_INBAND_MGMT with value of true or false. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_log_disk_path (str, Optional):
                SE Client Logs disk path for cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_log_disk_size_gb (int, Optional):
                SE Client Log disk size for cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_sys_disk_path (str, Optional):
                SE System Logs disk path for cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_sys_disk_size_gb (int, Optional):
                SE System Logs disk size for cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ssh_user_ref (str, Optional):
                Cloud connector user uuid for SSH to hosts. It is a reference to an object of type CloudConnectorUser. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        maintenance_mode(bool, Optional):
            Cloud is in maintenance mode. Field introduced in 20.1.7,21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        metrics_polling_interval(int, Optional):
            Cloud metrics collector polling interval in seconds. Field introduced in 22.1.1. Unit is SECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        mtu(int, Optional):
            MTU setting for the cloud. Unit is BYTES. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        nsxt_configuration(dict[str, Any], Optional):
            nsxt_configuration. Defaults to None.

            * automate_dfw_rules (bool, Optional):
                Automatically create DFW rules for VirtualService in NSX-T Manager. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Basic edition(Allowed values- false), Essentials, Enterprise with Cloud Services edition.

            * data_network_config (dict[str, Any], Optional):
                data_network_config

                * tier1_segment_config (dict[str, Any], Optional):
                    tier1_segment_config

                    * automatic (dict[str, Any], Optional):
                        automatic

                        * nsxt_segment_subnet (dict[str, Any]):
                            nsxt_segment_subnet

                            * ip_addr (dict[str, Any]):
                                ip_addr

                                * addr (str):
                                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                                * type (str):
                                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * mask (int):
                                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * num_se_per_segment (int, Optional):
                            The number of SE data vNic's that can be connected to the Avi logical segment. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * tier1_lr_ids (List[str], Optional):
                            Tier1 logical router IDs. Field introduced in 20.1.1. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * manual (dict[str, Any], Optional):
                        manual

                        * tier1_lrs (List[dict[str, Any]], Optional):
                            Tier1 logical router placement information. Field introduced in 20.1.1. Minimum of 1 items required. Maximum of 256 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * locale_service (str, Optional):
                                Locale-services configuration, holds T1 edge-cluster information. When VirtualService is enabled with preserve client IP, ServiceInsertion VirtualEndpoint will be created in this locale-service. By default Avi controller picks default locale-service on T1. If more than one locale-services are present, this will be used for resolving the same. Example locale-service path - /infra/tier-1s/London_Tier1Gateway1/locale-services/London_Tier1LocalServices-1. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                            * segment_id (str, Optional):
                                Overlay segment path. Example- /infra/segments/Seg-Web-T1-01. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * tier1_lr_id (str):
                                Tier1 logical router path. Example- /infra/tier-1s/T1-01. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * segment_config_mode (str):
                        Config Mode for selecting the placement logical segments for Avi ServiceEngine data path. Enum options - TIER1_SEGMENT_MANUAL, TIER1_SEGMENT_AUTOMATIC. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Basic edition(Allowed values- TIER1_SEGMENT_MANUAL), Essentials, Enterprise with Cloud Services edition.

                * transport_zone (str):
                    Data transport zone path for Avi Service Engines. Example- /infra/sites/default/enforcement-points/default/transport-zones/xxx-xxx-xxxx. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * tz_type (str):
                    Data transport zone type overlay or vlan. Enum options - OVERLAY, VLAN. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * vlan_segments (List[str], Optional):
                    Data vlan segments path to use for Avi Service Engines. Example- /infra/segments/vlanls. This should be set only when transport zone is of type VLAN. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * domain_id (str, Optional):
                Domain where NSGroup objects belongs to. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enforcementpoint_id (str, Optional):
                Enforcement point is where the rules of a policy to apply. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * management_network_config (dict[str, Any], Optional):
                management_network_config

                * overlay_segment (dict[str, Any], Optional):
                    overlay_segment

                    * locale_service (str, Optional):
                        Locale-services configuration, holds T1 edge-cluster information. When VirtualService is enabled with preserve client IP, ServiceInsertion VirtualEndpoint will be created in this locale-service. By default Avi controller picks default locale-service on T1. If more than one locale-services are present, this will be used for resolving the same. Example locale-service path - /infra/tier-1s/London_Tier1Gateway1/locale-services/London_Tier1LocalServices-1. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * segment_id (str, Optional):
                        Overlay segment path. Example- /infra/segments/Seg-Web-T1-01. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * tier1_lr_id (str):
                        Tier1 logical router path. Example- /infra/tier-1s/T1-01. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * transport_zone (str):
                    Management transport zone path for Avi Service Engines. Example- /infra/sites/default/enforcement-points/default/transport-zones/xxx-xxx-xxxx. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * tz_type (str):
                    Management transport zone type overlay or vlan. Enum options - OVERLAY, VLAN. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * vlan_segment (str, Optional):
                    Management vlan segment path to use for Avi Service Engines. Example- /infra/segments/vlanls. This should be set only when transport zone is of type VLAN. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * nsxt_credentials_ref (str, Optional):
                Credentials to access NSX-T manager. It is a reference to an object of type CloudConnectorUser. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * nsxt_url (str, Optional):
                NSX-T manager hostname or IP address. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * site_id (str, Optional):
                Site where transport zone belongs to. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vmc_mode (bool, Optional):
                VMC mode. Field introduced in 23.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * vpc_mode (bool, Optional):
                VPC Mode. Field introduced in 23.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        ntp_configuration(dict[str, Any], Optional):
            ntp_configuration. Defaults to None.

            * ntp_authentication_keys (List[dict[str, Any]], Optional):
                NTP Authentication keys. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * algorithm (str, Optional):
                    Message Digest Algorithm used for NTP authentication. Default is NTP_AUTH_ALGORITHM_MD5. Enum options - NTP_AUTH_ALGORITHM_MD5, NTP_AUTH_ALGORITHM_SHA1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * key (str):
                    NTP Authentication key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * key_number (int):
                    Key number to be assigned to the authentication-key. Allowed values are 1-65534. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ntp_server_list (List[dict[str, Any]], Optional):
                List of NTP server hostnames or IP addresses. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ntp_servers (List[dict[str, Any]], Optional):
                List of NTP Servers. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * key_number (int, Optional):
                    Key number from the list of trusted keys used to authenticate this server. Allowed values are 1-65534. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server (dict[str, Any]):
                    server

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        obj_name_prefix(str, Optional):
            Default prefix for all automatically created objects in this cloud. This prefix can be overridden by the SE-Group template. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        openstack_configuration(dict[str, Any], Optional):
            openstack_configuration. Defaults to None.

            * admin_tenant (str):
                OpenStack admin tenant (or project) information. For Keystone v3, provide the project information in project@domain format. Domain need not be specified if the project belongs to the 'Default' domain. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * admin_tenant_uuid (str, Optional):
                admin-tenant's UUID in OpenStack. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * allowed_address_pairs (bool, Optional):
                If false, allowed-address-pairs extension will not be used. . Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * anti_affinity (bool, Optional):
                If true, an anti-affinity policy will be applied to all SEs of a SE-Group, else no such policy will be applied. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * auth_url (str, Optional):
                Auth URL for connecting to keystone. If this is specified, any value provided for keystone_host is ignored. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * config_drive (bool, Optional):
                If false, metadata service will be used instead of  config-drive functionality to retrieve SE VM metadata. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * contrail_disable_policy (bool, Optional):
                When set to True, the VIP and Data ports will be programmed to set virtual machine interface disable-policy. Please refer Contrail documentation for more on disable-policy. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * contrail_endpoint (str, Optional):
                Contrail VNC endpoint url (example http //10.10.10.100 8082). By default, 'http //' scheme and 8082 port will be used if not provided in the url. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * contrail_plugin (bool, Optional):
                Enable Contrail plugin mode. (deprecated). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * custom_se_image_properties (List[dict[str, Any]], Optional):
                Custom image properties to be set on a Service Engine image. Only hw_vif_multiqueue_enabled property is supported. Other properties will be ignored. Field introduced in 18.2.7, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str):
                    Property name. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * value (str, Optional):
                    Property value. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enable_os_object_caching (bool, Optional):
                When enabled, frequently used objects like networks, subnets, routers etc. are cached to improve performance and reduce load on OpenStack Controllers. Suitable for OpenStack environments where Neutron resources are not frequently created, updated, or deleted.The cache is refreshed when cloud GC API is issued. Field introduced in 21.1.5, 22.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * enable_tagging (bool, Optional):
                When set to True, OpenStack resources created by Avi are tagged with Avi Cloud UUID. Field introduced in 21.1.5, 22.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * external_networks (bool, Optional):
                If True, allow selection of networks marked as 'external' for management,  vip or data networks. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * free_floatingips (bool, Optional):
                Free unused floating IPs. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * hypervisor (str, Optional):
                Default hypervisor type, only KVM is supported. Enum options - DEFAULT, VMWARE_ESX, KVM, VMWARE_VSAN, XEN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * hypervisor_properties (List[dict[str, Any]], Optional):
                Custom properties per hypervisor type. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * hypervisor (str):
                    Hypervisor type. Enum options - DEFAULT, VMWARE_ESX, KVM, VMWARE_VSAN, XEN. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * image_properties (List[dict[str, Any]], Optional):
                    Custom properties to be associated with the SE image in Glance for this hypervisor type. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * name (str):
                        Property name. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * value (str, Optional):
                        Property value. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * img_format (str, Optional):
                If OS_IMG_FMT_RAW, use RAW images else use QCOW2 for KVM. Enum options - OS_IMG_FMT_AUTO, OS_IMG_FMT_QCOW2, OS_IMG_FMT_VMDK, OS_IMG_FMT_RAW, OS_IMG_FMT_FLAT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * import_keystone_tenants (bool, Optional):
                Import keystone tenants list into Avi. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * insecure (bool, Optional):
                Allow self-signed certificates when communicating with https service endpoints. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * keystone_host (str, Optional):
                Keystone's hostname or IP address. (Deprecated) Use auth_url instead. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * map_admin_to_cloudadmin (bool, Optional):
                If True, map Avi 'admin' tenant to the admin_tenant of the Cloud. Else map Avi 'admin' to OpenStack 'admin' tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mgmt_network_name (str):
                Avi Management network name or cidr. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mgmt_network_uuid (str, Optional):
                Management network UUID. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * name_owner (bool, Optional):
                If True, embed owner info in VIP port 'name', else embed owner info in 'device_id' field. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * neutron_rbac (bool, Optional):
                If True, enable neutron rbac discovery of networks shared across tenants/projects. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * password (str, Optional):
                The password Avi Vantage will use when authenticating to Keystone. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * privilege (str):
                Access privilege. Enum options - NO_ACCESS, READ_ACCESS, WRITE_ACCESS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * prov_name (List[str], Optional):
                LBaaS provider name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * provider_vip_networks (List[dict[str, Any]], Optional):
                A tenant can normally use its own networks and any networks shared with it. In addition, this setting provides extra networks that are usable by tenants. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * os_network_uuid (str, Optional):
                    Neutron network UUID. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * os_tenant_uuids (List[str], Optional):
                    UUIDs of OpenStack tenants that should be allowed to use the specified Neutron network for VIPs. Use '*' to make this network available to all tenants. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * region (str, Optional):
                Region name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * role_mapping (List[dict[str, Any]], Optional):
                Defines the mapping from OpenStack role names to avi local role names. For an OpenStack role, this mapping is consulted only if there is no local Avi role with the same name as the OpenStack role. This is an ordered list and only the first matching entry is used. You can use '*' to match all OpenStack role names. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * avi_role (str):
                    Role name in Avi. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * os_role (str):
                    Role name in OpenStack. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * security_groups (bool, Optional):
                If false, security-groups extension will not be used. . Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * tenant_se (bool, Optional):
                If true, then SEs will be created in the appropriate tenants, else SEs will be created in the admin_tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_admin_url (bool, Optional):
                If admin URLs are either inaccessible or not to be accessed from Avi Controller, then set this to False. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_internal_endpoints (bool, Optional):
                Use internalURL for OpenStack endpoints instead of the default publicURL endpoints. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_keystone_auth (bool, Optional):
                Use keystone for user authentication. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * username (str):
                The username Avi Vantage will use when authenticating to Keystone. For Keystone v3, provide the user information in user@domain format, unless that user belongs to the Default domain. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vip_port_in_admin_tenant (bool, Optional):
                When set to True, VIP ports are created in OpenStack tenant configured as admin_tenant in cloud. Otherwise, default behavior is to create VIP ports in user tenant. Field introduced in 21.1.5, 22.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        prefer_static_routes(bool, Optional):
            Prefer static routes over interface routes during VirtualService placement. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        proxy_configuration(dict[str, Any], Optional):
            proxy_configuration. Defaults to None.

            * host (str):
                Proxy hostname or IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * password (str, Optional):
                Password for proxy. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * port (int):
                Proxy port. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * username (str, Optional):
                Username for proxy. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        rancher_configuration(dict[str, Any], Optional):
            rancher_configuration. Defaults to None.

            * access_key (str, Optional):
                Access key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * app_sync_frequency (int, Optional):
                Sync frequency in seconds with frameworks. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * container_port_match_http_service (bool, Optional):
                Perform container port matching to create a HTTP Virtualservice instead of a TCP/UDP VirtualService. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * coredump_directory (str, Optional):
                Directory to mount to check for core dumps on Service Engines. This will be mapped read only to /var/crash on any new Service Engines. This is a disruptive change. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disable_auto_backend_service_sync (bool, Optional):
                Disable auto service sync for back end services. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disable_auto_frontend_service_sync (bool, Optional):
                Disable auto service sync for front end services. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disable_auto_se_creation (bool, Optional):
                Disable SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * docker_registry_se (dict[str, Any], Optional):
                docker_registry_se

                * oshift_registry (dict[str, Any], Optional):
                    oshift_registry

                    * registry_namespace (str, Optional):
                        Namespace for the ServiceEngine image to be hosted in Openshift Integrated registry. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * registry_service (str, Optional):
                        Name of the Integrated registry Service in Openshift. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * registry_vip (dict[str, Any], Optional):
                        registry_vip

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * password (str, Optional):
                    Password for docker registry. Authorized 'regular user' password if registry is Openshift integrated registry. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * private (bool, Optional):
                    Set if docker registry is private. Avi controller will not attempt to push SE image to the registry, unless se_repository_push is set. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * registry (str, Optional):
                    Avi ServiceEngine repository name. For private registry, it's registry port/repository, for public registry, it's registry/repository, for openshift registry, it's registry port/namespace/repo. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * username (str, Optional):
                    Username for docker registry. Authorized 'regular user' if registry is Openshift integrated registry. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * east_west_placement_subnet (dict[str, Any], Optional):
                east_west_placement_subnet

                * ip_addr (dict[str, Any]):
                    ip_addr

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mask (int):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enable_event_subscription (bool, Optional):
                Enable Docker event subscription. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * feproxy_container_port_as_service (bool, Optional):
                For Front End proxies, use container port as service port. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * feproxy_vips_enable_proxy_arp (bool, Optional):
                Enable proxy ARP from Host interface for Front End  proxies. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * fleet_endpoint (str, Optional):
                Optional fleet remote endpoint if fleet is used for SE deployment. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_container_ports (List[int], Optional):
                List of container ports that create a HTTP Virtualservice instead of a TCP/UDP VirtualService. Defaults to 80. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * nuage_controller (dict[str, Any], Optional):
                nuage_controller

                * nuage_organization (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * nuage_password (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * nuage_port (int, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * nuage_username (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * nuage_vsd_host (str, Optional):
                    Nuage VSD host name or IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_domain (str, Optional):
                    Domain to be used for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_enterprise (str, Optional):
                    Enterprise to be used for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_network (str, Optional):
                    Network to be used for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_policy_group (str, Optional):
                    Policy Group to be used for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_user (str, Optional):
                    User to be used for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_zone (str, Optional):
                    Zone to be used for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * rancher_servers (List[str], Optional):
                List of Rancher servers; In case of a load balanced Rancher multi cluster, use Virtual IP of the cluster. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_deployment_method (str, Optional):
                Use Fleet/SSH for SE deployment. Enum options - SE_CREATE_FLEET, SE_CREATE_SSH, SE_CREATE_POD. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_exclude_attributes (List[dict[str, Any]], Optional):
                Exclude hosts with attributes for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * attribute (str):
                    Attribute to match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * value (str, Optional):
                    Attribute value. If not set, match any value. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_include_attributes (List[dict[str, Any]], Optional):
                Create SEs just on hosts with include attributes. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * attribute (str):
                    Attribute to match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * value (str, Optional):
                    Attribute value. If not set, match any value. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_spawn_rate (int, Optional):
                New SE spawn rate per minute. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_volume (str, Optional):
                Host volume to be used as a disk for Avi SE, This is a disruptive change. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * secret_key (str, Optional):
                Secret key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * services_accessible_all_interfaces (bool, Optional):
                Make service ports accessible on all Host interfaces in addition to East-West VIP and/or bridge IP. Usually enabled AWS clusters to export East-West services on Host interface. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ssh_user_ref (str, Optional):
                Cloud connector user uuid for SSH to hosts. It is a reference to an object of type CloudConnectorUser. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_container_ip_port (bool, Optional):
                Use container IP address port for pool instead of host IP address hostport. This mode is applicable if the container IP is reachable (not a private NATed IP) from other hosts in a routed environment for containers. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_controller_image (bool, Optional):
                If true, use controller generated SE docker image via fileservice, else use docker repository image as defined by docker_registry_se. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        se_group_template_ref(str, Optional):
            The Service Engine Group to use as template. It is a reference to an object of type ServiceEngineGroup. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        state_based_dns_registration(bool, Optional):
            DNS records for VIPs are added/deleted based on the operational state of the VIPs. Field introduced in 17.1.12. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- true), Basic edition(Allowed values- true), Enterprise with Cloud Services edition. Defaults to None.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vca_configuration(dict[str, Any], Optional):
            vca_configuration. Defaults to None.

            * privilege (str):
                vCloudAir access mode. Enum options - NO_ACCESS, READ_ACCESS, WRITE_ACCESS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_host (str):
                vCloudAir host address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_instance (str):
                vCloudAir instance ID. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_mgmt_network (str):
                vCloudAir management network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_orgnization (str):
                vCloudAir orgnization ID. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_password (str):
                vCloudAir password. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_username (str):
                vCloudAir username. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_vdc (str):
                vCloudAir virtual data center name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vcenter_configuration(dict[str, Any], Optional):
            vcenter_configuration. Defaults to None.

            * content_lib (dict[str, Any], Optional):
                content_lib

                * id (str, Optional):
                    Content Library Id. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str, Optional):
                    Content Library name. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * datacenter (str, Optional):
                Datacenter for virtual infrastructure discovery. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * deactivate_vm_discovery (bool, Optional):
                If true, VM's on the vCenter will not be discovered.Set it to true if there are more than 10000 VMs in the datacenter. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * is_nsx_environment (bool, Optional):
                If true, NSX-T segment spanning multiple VDS with vCenter cloud are merged to a single network in Avi. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * management_ip_subnet (dict[str, Any], Optional):
                management_ip_subnet

                * ip_addr (dict[str, Any]):
                    ip_addr

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mask (int):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * management_network (str, Optional):
                Management network to use for Avi Service Engines. It is a reference to an object of type VIMgrNWRuntime. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * password (str, Optional):
                The password Avi Vantage will use when authenticating with vCenter. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * privilege (str):
                Set the access mode to vCenter as either Read, which allows Avi to discover networks and servers, or Write, which also allows Avi to create Service Engines and configure their network properties. Enum options - NO_ACCESS, READ_ACCESS, WRITE_ACCESS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_content_lib (bool, Optional):
                If false, Service Engine image will not be pushed to content library. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Enterprise with Cloud Services edition.

            * username (str, Optional):
                The username Avi Vantage will use when authenticating with vCenter. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vcenter_template_se_location (str, Optional):
                Avi Service Engine Template in vCenter to be used for creating Service Engines. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vcenter_url (str, Optional):
                vCenter hostname or IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vmc_deployment(bool, Optional):
            This deployment is VMware on AWS cloud. Field introduced in 20.1.5, 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              nsx_alb.alb.cloud.present:
                - x_avi_version: value
                - vtype: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.cloud.create x_avi_version=value, vtype=value
    """

    result = dict(comment=[], ret=[], result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "autoscale_polling_interval": "autoscale_polling_interval",
        "aws_configuration": "aws_configuration",
        "azure_configuration": "azure_configuration",
        "cloudstack_configuration": "cloudstack_configuration",
        "configpb_attributes": "configpb_attributes",
        "custom_tags": "custom_tags",
        "dhcp_enabled": "dhcp_enabled",
        "dns_provider_ref": "dns_provider_ref",
        "dns_resolution_on_se": "dns_resolution_on_se",
        "dns_resolvers": "dns_resolvers",
        "docker_configuration": "docker_configuration",
        "east_west_dns_provider_ref": "east_west_dns_provider_ref",
        "east_west_ipam_provider_ref": "east_west_ipam_provider_ref",
        "enable_vip_on_all_interfaces": "enable_vip_on_all_interfaces",
        "enable_vip_static_routes": "enable_vip_static_routes",
        "gcp_configuration": "gcp_configuration",
        "ip6_autocfg_enabled": "ip6_autocfg_enabled",
        "ipam_provider_ref": "ipam_provider_ref",
        "license_tier": "license_tier",
        "license_type": "license_type",
        "linuxserver_configuration": "linuxserver_configuration",
        "maintenance_mode": "maintenance_mode",
        "markers": "markers",
        "metrics_polling_interval": "metrics_polling_interval",
        "mtu": "mtu",
        "name": "name",
        "nsxt_configuration": "nsxt_configuration",
        "ntp_configuration": "ntp_configuration",
        "obj_name_prefix": "obj_name_prefix",
        "openstack_configuration": "openstack_configuration",
        "prefer_static_routes": "prefer_static_routes",
        "proxy_configuration": "proxy_configuration",
        "rancher_configuration": "rancher_configuration",
        "se_group_template_ref": "se_group_template_ref",
        "state_based_dns_registration": "state_based_dns_registration",
        "tenant_ref": "tenant_ref",
        "vca_configuration": "vca_configuration",
        "vcenter_configuration": "vcenter_configuration",
        "vmc_deployment": "vmc_deployment",
        "vtype": "vtype",
    }

    payload = {}
    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = value

    create = await hub.tool.nsx_alb.session.request(
        ctx,
        method="post",
        path="/cloud",
        query_params={},
        data=payload,
    )

    if not create["result"]:
        result["comment"].append(create["comment"])
        result["result"] = False
        return result

    result["comment"].append(
        f"Created nsx_alb.alb.cloud '{name}'",
    )

    result["ret"] = create["ret"]

    result["ret"]["resource_id"] = create["ret"]["uuid"]
    return result


async def update(
    hub,
    ctx,
    resource_id: str,
    vtype: str,
    name: str = None,
    autoscale_polling_interval: int = None,
    aws_configuration: make_dataclass(
        "aws_configuration",
        [
            ("vpc_id", str),
            ("access_key_id", str, field(default=None)),
            ("asg_poll_interval", int, field(default=None)),
            (
                "ebs_encryption",
                make_dataclass(
                    "ebs_encryption",
                    [
                        ("master_key", str, field(default=None)),
                        ("mode", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("free_elasticips", bool, field(default=None)),
            ("iam_assume_role", str, field(default=None)),
            ("publish_vip_to_public_zone", bool, field(default=None)),
            ("region", str, field(default=None)),
            ("route53_integration", bool, field(default=None)),
            (
                "s3_encryption",
                make_dataclass(
                    "s3_encryption",
                    [
                        ("master_key", str, field(default=None)),
                        ("mode", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("secret_access_key", str, field(default=None)),
            (
                "sqs_encryption",
                make_dataclass(
                    "sqs_encryption",
                    [
                        ("master_key", str, field(default=None)),
                        ("mode", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("ttl", int, field(default=None)),
            ("use_iam_roles", bool, field(default=None)),
            ("use_sns_sqs", bool, field(default=None)),
            ("vpc", str, field(default=None)),
            (
                "zones",
                List[
                    make_dataclass(
                        "zones",
                        [
                            ("availability_zone", str),
                            ("mgmt_network_name", str),
                            ("mgmt_network_uuid", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
        ],
    ) = None,
    azure_configuration: make_dataclass(
        "azure_configuration",
        [
            ("availability_zones", List[str], field(default=None)),
            ("cloud_credentials_ref", str, field(default=None)),
            ("des_id", str, field(default=None)),
            ("location", str, field(default=None)),
            (
                "network_info",
                List[
                    make_dataclass(
                        "network_info",
                        [
                            ("management_network_id", str, field(default=None)),
                            ("se_network_id", str, field(default=None)),
                            ("virtual_network_id", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("resource_group", str, field(default=None)),
            ("se_storage_account", str, field(default=None)),
            ("subscription_id", str, field(default=None)),
            ("use_azure_dns", bool, field(default=None)),
            ("use_enhanced_ha", bool, field(default=None)),
            ("use_managed_disks", bool, field(default=None)),
            ("use_standard_alb", bool, field(default=None)),
        ],
    ) = None,
    cloudstack_configuration: make_dataclass(
        "cloudstack_configuration",
        [
            ("access_key_id", str),
            ("api_url", str),
            ("mgmt_network_name", str),
            ("secret_access_key", str),
            ("cntr_public_ip", str, field(default=None)),
            ("hypervisor", str, field(default=None)),
            ("mgmt_network_uuid", str, field(default=None)),
        ],
    ) = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    custom_tags: List[
        make_dataclass(
            "custom_tags", [("tag_key", str), ("tag_val", str, field(default=None))]
        )
    ] = None,
    dhcp_enabled: bool = None,
    dns_provider_ref: str = None,
    dns_resolution_on_se: bool = None,
    dns_resolvers: List[
        make_dataclass(
            "dns_resolvers",
            [
                ("resolver_name", str),
                ("fixed_ttl", int, field(default=None)),
                ("min_ttl", int, field(default=None)),
                (
                    "nameserver_ips",
                    List[
                        make_dataclass("nameserver_ips", [("addr", str), ("type", str)])
                    ],
                    field(default=None),
                ),
                ("use_mgmt", bool, field(default=None)),
            ],
        )
    ] = None,
    docker_configuration: make_dataclass(
        "docker_configuration",
        [
            ("app_sync_frequency", int, field(default=None)),
            ("ca_tls_key_and_certificate_ref", str, field(default=None)),
            ("client_tls_key_and_certificate_ref", str, field(default=None)),
            ("container_port_match_http_service", bool, field(default=None)),
            ("coredump_directory", str, field(default=None)),
            ("disable_auto_backend_service_sync", bool, field(default=None)),
            ("disable_auto_frontend_service_sync", bool, field(default=None)),
            ("disable_auto_se_creation", bool, field(default=None)),
            (
                "docker_registry_se",
                make_dataclass(
                    "docker_registry_se",
                    [
                        (
                            "oshift_registry",
                            make_dataclass(
                                "oshift_registry",
                                [
                                    ("registry_namespace", str, field(default=None)),
                                    ("registry_service", str, field(default=None)),
                                    (
                                        "registry_vip",
                                        make_dataclass(
                                            "registry_vip",
                                            [("addr", str), ("type", str)],
                                        ),
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("password", str, field(default=None)),
                        ("private", bool, field(default=None)),
                        ("registry", str, field(default=None)),
                        ("username", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "east_west_placement_subnet",
                make_dataclass(
                    "east_west_placement_subnet",
                    [
                        (
                            "ip_addr",
                            make_dataclass("ip_addr", [("addr", str), ("type", str)]),
                        ),
                        ("mask", int),
                    ],
                ),
                field(default=None),
            ),
            ("enable_event_subscription", bool, field(default=None)),
            ("feproxy_container_port_as_service", bool, field(default=None)),
            ("feproxy_vips_enable_proxy_arp", bool, field(default=None)),
            ("fleet_endpoint", str, field(default=None)),
            ("http_container_ports", List[int], field(default=None)),
            ("se_deployment_method", str, field(default=None)),
            (
                "se_exclude_attributes",
                List[
                    make_dataclass(
                        "se_exclude_attributes",
                        [("attribute", str), ("value", str, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            (
                "se_include_attributes",
                List[
                    make_dataclass(
                        "se_include_attributes",
                        [("attribute", str), ("value", str, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            ("se_spawn_rate", int, field(default=None)),
            ("se_volume", str, field(default=None)),
            ("services_accessible_all_interfaces", bool, field(default=None)),
            ("ssh_user_ref", str, field(default=None)),
            ("ucp_nodes", List[str], field(default=None)),
            ("use_container_ip_port", bool, field(default=None)),
            ("use_controller_image", bool, field(default=None)),
        ],
    ) = None,
    east_west_dns_provider_ref: str = None,
    east_west_ipam_provider_ref: str = None,
    enable_vip_on_all_interfaces: bool = None,
    enable_vip_static_routes: bool = None,
    gcp_configuration: make_dataclass(
        "gcp_configuration",
        [
            (
                "network_config",
                make_dataclass(
                    "network_config",
                    [
                        ("config", str),
                        (
                            "inband",
                            make_dataclass(
                                "inband",
                                [
                                    ("vpc_network_name", str),
                                    ("vpc_subnet_name", str),
                                    ("vpc_project_id", str, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "one_arm",
                            make_dataclass(
                                "one_arm",
                                [
                                    ("data_vpc_network_name", str),
                                    ("data_vpc_subnet_name", str),
                                    ("management_vpc_network_name", str),
                                    ("management_vpc_subnet_name", str),
                                    ("data_vpc_project_id", str, field(default=None)),
                                    (
                                        "management_vpc_project_id",
                                        str,
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "two_arm",
                            make_dataclass(
                                "two_arm",
                                [
                                    ("backend_data_vpc_network_name", str),
                                    ("backend_data_vpc_subnet_name", str),
                                    ("frontend_data_vpc_network_name", str),
                                    ("frontend_data_vpc_subnet_name", str),
                                    ("management_vpc_network_name", str),
                                    ("management_vpc_subnet_name", str),
                                    (
                                        "backend_data_vpc_project_id",
                                        str,
                                        field(default=None),
                                    ),
                                    (
                                        "frontend_data_vpc_project_id",
                                        str,
                                        field(default=None),
                                    ),
                                    (
                                        "management_vpc_project_id",
                                        str,
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
            ),
            ("region_name", str),
            ("se_project_id", str),
            (
                "vip_allocation_strategy",
                make_dataclass(
                    "vip_allocation_strategy",
                    [
                        ("mode", str),
                        (
                            "ilb",
                            make_dataclass(
                                "ilb",
                                [
                                    (
                                        "cloud_router_names",
                                        List[str],
                                        field(default=None),
                                    )
                                ],
                            ),
                            field(default=None),
                        ),
                        (
                            "routes",
                            make_dataclass(
                                "routes",
                                [
                                    (
                                        "match_se_group_subnet",
                                        bool,
                                        field(default=None),
                                    ),
                                    ("route_priority", int, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
            ),
            ("zones", List[str]),
            ("cloud_credentials_ref", str, field(default=None)),
            (
                "encryption_keys",
                make_dataclass(
                    "encryption_keys",
                    [
                        ("gcs_bucket_kms_key_id", str, field(default=None)),
                        ("gcs_objects_kms_key_id", str, field(default=None)),
                        ("se_disk_kms_key_id", str, field(default=None)),
                        ("se_image_kms_key_id", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("firewall_target_tags", List[str], field(default=None)),
            ("gcp_service_account_email", str, field(default=None)),
            ("gcs_bucket_name", str, field(default=None)),
            ("gcs_project_id", str, field(default=None)),
        ],
    ) = None,
    ip6_autocfg_enabled: bool = None,
    ipam_provider_ref: str = None,
    license_tier: str = None,
    license_type: str = None,
    linuxserver_configuration: make_dataclass(
        "linuxserver_configuration",
        [
            (
                "hosts",
                List[
                    make_dataclass(
                        "hosts",
                        [
                            (
                                "host_ip",
                                make_dataclass(
                                    "host_ip", [("addr", str), ("type", str)]
                                ),
                            ),
                            (
                                "host_attr",
                                List[
                                    make_dataclass(
                                        "host_attr",
                                        [
                                            ("attr_key", str),
                                            ("attr_val", str, field(default=None)),
                                        ],
                                    )
                                ],
                                field(default=None),
                            ),
                            ("node_availability_zone", str, field(default=None)),
                            ("se_group_ref", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("se_inband_mgmt", bool, field(default=None)),
            ("se_log_disk_path", str, field(default=None)),
            ("se_log_disk_size_gb", int, field(default=None)),
            ("se_sys_disk_path", str, field(default=None)),
            ("se_sys_disk_size_gb", int, field(default=None)),
            ("ssh_user_ref", str, field(default=None)),
        ],
    ) = None,
    maintenance_mode: bool = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    metrics_polling_interval: int = None,
    mtu: int = None,
    nsxt_configuration: make_dataclass(
        "nsxt_configuration",
        [
            ("automate_dfw_rules", bool, field(default=None)),
            (
                "data_network_config",
                make_dataclass(
                    "data_network_config",
                    [
                        ("transport_zone", str),
                        ("tz_type", str),
                        (
                            "tier1_segment_config",
                            make_dataclass(
                                "tier1_segment_config",
                                [
                                    ("segment_config_mode", str),
                                    (
                                        "automatic",
                                        make_dataclass(
                                            "automatic",
                                            [
                                                (
                                                    "nsxt_segment_subnet",
                                                    make_dataclass(
                                                        "nsxt_segment_subnet",
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
                                                    ),
                                                ),
                                                (
                                                    "num_se_per_segment",
                                                    int,
                                                    field(default=None),
                                                ),
                                                (
                                                    "tier1_lr_ids",
                                                    List[str],
                                                    field(default=None),
                                                ),
                                            ],
                                        ),
                                        field(default=None),
                                    ),
                                    (
                                        "manual",
                                        make_dataclass(
                                            "manual",
                                            [
                                                (
                                                    "tier1_lrs",
                                                    List[
                                                        make_dataclass(
                                                            "tier1_lrs",
                                                            [
                                                                ("tier1_lr_id", str),
                                                                (
                                                                    "locale_service",
                                                                    str,
                                                                    field(default=None),
                                                                ),
                                                                (
                                                                    "segment_id",
                                                                    str,
                                                                    field(default=None),
                                                                ),
                                                            ],
                                                        )
                                                    ],
                                                    field(default=None),
                                                )
                                            ],
                                        ),
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("vlan_segments", List[str], field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("domain_id", str, field(default=None)),
            ("enforcementpoint_id", str, field(default=None)),
            (
                "management_network_config",
                make_dataclass(
                    "management_network_config",
                    [
                        ("transport_zone", str),
                        ("tz_type", str),
                        (
                            "overlay_segment",
                            make_dataclass(
                                "overlay_segment",
                                [
                                    ("tier1_lr_id", str),
                                    ("locale_service", str, field(default=None)),
                                    ("segment_id", str, field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("vlan_segment", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("nsxt_credentials_ref", str, field(default=None)),
            ("nsxt_url", str, field(default=None)),
            ("site_id", str, field(default=None)),
            ("vmc_mode", bool, field(default=None)),
            ("vpc_mode", bool, field(default=None)),
        ],
    ) = None,
    ntp_configuration: make_dataclass(
        "ntp_configuration",
        [
            (
                "ntp_authentication_keys",
                List[
                    make_dataclass(
                        "ntp_authentication_keys",
                        [
                            ("key", str),
                            ("key_number", int),
                            ("algorithm", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            (
                "ntp_server_list",
                List[make_dataclass("ntp_server_list", [("addr", str), ("type", str)])],
                field(default=None),
            ),
            (
                "ntp_servers",
                List[
                    make_dataclass(
                        "ntp_servers",
                        [
                            (
                                "server",
                                make_dataclass(
                                    "server", [("addr", str), ("type", str)]
                                ),
                            ),
                            ("key_number", int, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
        ],
    ) = None,
    obj_name_prefix: str = None,
    openstack_configuration: make_dataclass(
        "openstack_configuration",
        [
            ("admin_tenant", str),
            ("mgmt_network_name", str),
            ("privilege", str),
            ("username", str),
            ("admin_tenant_uuid", str, field(default=None)),
            ("allowed_address_pairs", bool, field(default=None)),
            ("anti_affinity", bool, field(default=None)),
            ("auth_url", str, field(default=None)),
            ("config_drive", bool, field(default=None)),
            ("contrail_disable_policy", bool, field(default=None)),
            ("contrail_endpoint", str, field(default=None)),
            ("contrail_plugin", bool, field(default=None)),
            (
                "custom_se_image_properties",
                List[
                    make_dataclass(
                        "custom_se_image_properties",
                        [("name", str), ("value", str, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            ("enable_os_object_caching", bool, field(default=None)),
            ("enable_tagging", bool, field(default=None)),
            ("external_networks", bool, field(default=None)),
            ("free_floatingips", bool, field(default=None)),
            ("hypervisor", str, field(default=None)),
            (
                "hypervisor_properties",
                List[
                    make_dataclass(
                        "hypervisor_properties",
                        [
                            ("hypervisor", str),
                            (
                                "image_properties",
                                List[
                                    make_dataclass(
                                        "image_properties",
                                        [
                                            ("name", str),
                                            ("value", str, field(default=None)),
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
            ("img_format", str, field(default=None)),
            ("import_keystone_tenants", bool, field(default=None)),
            ("insecure", bool, field(default=None)),
            ("keystone_host", str, field(default=None)),
            ("map_admin_to_cloudadmin", bool, field(default=None)),
            ("mgmt_network_uuid", str, field(default=None)),
            ("name_owner", bool, field(default=None)),
            ("neutron_rbac", bool, field(default=None)),
            ("password", str, field(default=None)),
            ("prov_name", List[str], field(default=None)),
            (
                "provider_vip_networks",
                List[
                    make_dataclass(
                        "provider_vip_networks",
                        [
                            ("os_network_uuid", str, field(default=None)),
                            ("os_tenant_uuids", List[str], field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            ("region", str, field(default=None)),
            (
                "role_mapping",
                List[
                    make_dataclass(
                        "role_mapping", [("avi_role", str), ("os_role", str)]
                    )
                ],
                field(default=None),
            ),
            ("security_groups", bool, field(default=None)),
            ("tenant_se", bool, field(default=None)),
            ("use_admin_url", bool, field(default=None)),
            ("use_internal_endpoints", bool, field(default=None)),
            ("use_keystone_auth", bool, field(default=None)),
            ("vip_port_in_admin_tenant", bool, field(default=None)),
        ],
    ) = None,
    prefer_static_routes: bool = None,
    proxy_configuration: make_dataclass(
        "proxy_configuration",
        [
            ("host", str),
            ("port", int),
            ("password", str, field(default=None)),
            ("username", str, field(default=None)),
        ],
    ) = None,
    rancher_configuration: make_dataclass(
        "rancher_configuration",
        [
            ("access_key", str, field(default=None)),
            ("app_sync_frequency", int, field(default=None)),
            ("container_port_match_http_service", bool, field(default=None)),
            ("coredump_directory", str, field(default=None)),
            ("disable_auto_backend_service_sync", bool, field(default=None)),
            ("disable_auto_frontend_service_sync", bool, field(default=None)),
            ("disable_auto_se_creation", bool, field(default=None)),
            (
                "docker_registry_se",
                make_dataclass(
                    "docker_registry_se",
                    [
                        (
                            "oshift_registry",
                            make_dataclass(
                                "oshift_registry",
                                [
                                    ("registry_namespace", str, field(default=None)),
                                    ("registry_service", str, field(default=None)),
                                    (
                                        "registry_vip",
                                        make_dataclass(
                                            "registry_vip",
                                            [("addr", str), ("type", str)],
                                        ),
                                        field(default=None),
                                    ),
                                ],
                            ),
                            field(default=None),
                        ),
                        ("password", str, field(default=None)),
                        ("private", bool, field(default=None)),
                        ("registry", str, field(default=None)),
                        ("username", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "east_west_placement_subnet",
                make_dataclass(
                    "east_west_placement_subnet",
                    [
                        (
                            "ip_addr",
                            make_dataclass("ip_addr", [("addr", str), ("type", str)]),
                        ),
                        ("mask", int),
                    ],
                ),
                field(default=None),
            ),
            ("enable_event_subscription", bool, field(default=None)),
            ("feproxy_container_port_as_service", bool, field(default=None)),
            ("feproxy_vips_enable_proxy_arp", bool, field(default=None)),
            ("fleet_endpoint", str, field(default=None)),
            ("http_container_ports", List[int], field(default=None)),
            (
                "nuage_controller",
                make_dataclass(
                    "nuage_controller",
                    [
                        ("nuage_organization", str, field(default=None)),
                        ("nuage_password", str, field(default=None)),
                        ("nuage_port", int, field(default=None)),
                        ("nuage_username", str, field(default=None)),
                        ("nuage_vsd_host", str, field(default=None)),
                        ("se_domain", str, field(default=None)),
                        ("se_enterprise", str, field(default=None)),
                        ("se_network", str, field(default=None)),
                        ("se_policy_group", str, field(default=None)),
                        ("se_user", str, field(default=None)),
                        ("se_zone", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("rancher_servers", List[str], field(default=None)),
            ("se_deployment_method", str, field(default=None)),
            (
                "se_exclude_attributes",
                List[
                    make_dataclass(
                        "se_exclude_attributes",
                        [("attribute", str), ("value", str, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            (
                "se_include_attributes",
                List[
                    make_dataclass(
                        "se_include_attributes",
                        [("attribute", str), ("value", str, field(default=None))],
                    )
                ],
                field(default=None),
            ),
            ("se_spawn_rate", int, field(default=None)),
            ("se_volume", str, field(default=None)),
            ("secret_key", str, field(default=None)),
            ("services_accessible_all_interfaces", bool, field(default=None)),
            ("ssh_user_ref", str, field(default=None)),
            ("use_container_ip_port", bool, field(default=None)),
            ("use_controller_image", bool, field(default=None)),
        ],
    ) = None,
    se_group_template_ref: str = None,
    state_based_dns_registration: bool = None,
    tenant_ref: str = None,
    vca_configuration: make_dataclass(
        "vca_configuration",
        [
            ("privilege", str),
            ("vca_host", str),
            ("vca_instance", str),
            ("vca_mgmt_network", str),
            ("vca_orgnization", str),
            ("vca_password", str),
            ("vca_username", str),
            ("vca_vdc", str),
        ],
    ) = None,
    vcenter_configuration: make_dataclass(
        "vcenter_configuration",
        [
            ("privilege", str),
            (
                "content_lib",
                make_dataclass(
                    "content_lib",
                    [
                        ("id", str, field(default=None)),
                        ("name", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("datacenter", str, field(default=None)),
            ("deactivate_vm_discovery", bool, field(default=None)),
            ("is_nsx_environment", bool, field(default=None)),
            (
                "management_ip_subnet",
                make_dataclass(
                    "management_ip_subnet",
                    [
                        (
                            "ip_addr",
                            make_dataclass("ip_addr", [("addr", str), ("type", str)]),
                        ),
                        ("mask", int),
                    ],
                ),
                field(default=None),
            ),
            ("management_network", str, field(default=None)),
            ("password", str, field(default=None)),
            ("use_content_lib", bool, field(default=None)),
            ("username", str, field(default=None)),
            ("vcenter_template_se_location", str, field(default=None)),
            ("vcenter_url", str, field(default=None)),
        ],
    ) = None,
    vmc_deployment: bool = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:
        resource_id(str):
            Alb.cloud unique ID.

        vtype(str):
            Cloud type. Enum options - CLOUD_NONE, CLOUD_VCENTER, CLOUD_OPENSTACK, CLOUD_AWS, CLOUD_VCA, CLOUD_APIC, CLOUD_MESOS, CLOUD_LINUXSERVER, CLOUD_DOCKER_UCP, CLOUD_RANCHER, CLOUD_OSHIFT_K8S, CLOUD_AZURE, CLOUD_GCP, CLOUD_NSXT. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- CLOUD_NONE,CLOUD_VCENTER), Basic edition(Allowed values- CLOUD_NONE,CLOUD_NSXT), Enterprise with Cloud Services edition.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

        autoscale_polling_interval(int, Optional):
            CloudConnector polling interval in seconds for external autoscale groups, minimum 60 seconds. Allowed values are 60-3600. Field introduced in 18.2.2. Unit is SECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 60), Basic edition(Allowed values- 60), Enterprise with Cloud Services edition. Defaults to None.

        aws_configuration(dict[str, Any], Optional):
            aws_configuration. Defaults to None.

            * access_key_id (str, Optional):
                AWS access key ID. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * asg_poll_interval (int, Optional):
                Time interval between periodic polling of all Auto Scaling Groups. Allowed values are 60-1800. Field introduced in 17.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ebs_encryption (dict[str, Any], Optional):
                ebs_encryption

                * master_key (str, Optional):
                    AWS KMS ARN ID of the master key for encryption. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mode (str, Optional):
                    AWS encryption mode. Enum options - AWS_ENCRYPTION_MODE_NONE, AWS_ENCRYPTION_MODE_SSE_KMS. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * free_elasticips (bool, Optional):
                Free unused elastic IP addresses. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * iam_assume_role (str, Optional):
                IAM assume role for cross-account access. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * publish_vip_to_public_zone (bool, Optional):
                If enabled and the virtual service is not floating ip capable, vip will be published to both private and public zones. Field introduced in 17.2.10. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * region (str, Optional):
                AWS region. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * route53_integration (bool, Optional):
                If enabled, create/update DNS entries in Amazon Route 53 zones. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * s3_encryption (dict[str, Any], Optional):
                s3_encryption

                * master_key (str, Optional):
                    AWS KMS ARN ID of the master key for encryption. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mode (str, Optional):
                    AWS encryption mode. Enum options - AWS_ENCRYPTION_MODE_NONE, AWS_ENCRYPTION_MODE_SSE_KMS. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * secret_access_key (str, Optional):
                AWS secret access key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * sqs_encryption (dict[str, Any], Optional):
                sqs_encryption

                * master_key (str, Optional):
                    AWS KMS ARN ID of the master key for encryption. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mode (str, Optional):
                    AWS encryption mode. Enum options - AWS_ENCRYPTION_MODE_NONE, AWS_ENCRYPTION_MODE_SSE_KMS. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ttl (int, Optional):
                Default TTL for all records. Allowed values are 1-172800. Field introduced in 17.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_iam_roles (bool, Optional):
                Use IAM roles instead of access and secret key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_sns_sqs (bool, Optional):
                Use SNS/SQS based notifications for monitoring Auto Scaling Groups. Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vpc (str, Optional):
                VPC name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vpc_id (str):
                VPC ID. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * zones (List[dict[str, Any]], Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * availability_zone (str):
                    Availability zone. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mgmt_network_name (str):
                    Name or CIDR of the network in the Availability Zone that will be used as management network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mgmt_network_uuid (str, Optional):
                    UUID of the network in the Availability Zone that will be used as management network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        azure_configuration(dict[str, Any], Optional):
            azure_configuration. Defaults to None.

            * availability_zones (List[str], Optional):
                Availability zones to be used in Azure. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * cloud_credentials_ref (str, Optional):
                Credentials to access azure cloud. It is a reference to an object of type CloudConnectorUser. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * des_id (str, Optional):
                Disks Encryption Set resource-id (des_id) to encrypt se image and managed disk using customer-managed-keys. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * location (str, Optional):
                Azure location where this cloud will be located. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * network_info (List[dict[str, Any]], Optional):
                Azure virtual network and subnet information. Field introduced in 17.2.1. Minimum of 1 items required. Maximum of 1 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * management_network_id (str, Optional):
                    Id of the Azure subnet used as management network for the Service Engines. If set, Service Engines will have a dedicated management NIC, otherwise, they operate in inband mode. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_network_id (str, Optional):
                    Id of the Azure subnet where Avi Controller will create the Service Engines. . Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * virtual_network_id (str, Optional):
                    Virtual network where Virtual IPs will belong. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * resource_group (str, Optional):
                Azure resource group dedicated for Avi Controller. Avi Controller will create all its resources in this resource group. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_storage_account (str, Optional):
                Storage Account to be used for uploading SE VHD images to Azure. Must include the resource group name. Format '<resource-group> <storage-account-name>'. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * subscription_id (str, Optional):
                Subscription Id for the Azure subscription. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_azure_dns (bool, Optional):
                Azure is the DNS provider. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_enhanced_ha (bool, Optional):
                Use Azure's enhanced HA features. This needs a public IP to be associated with the VIP. . Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_managed_disks (bool, Optional):
                Use Azure managed disks for SE storage. Field introduced in 17.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_standard_alb (bool, Optional):
                Use Standard SKU Azure Load Balancer. By default Basic SKU Load Balancer is used. Field introduced in 17.2.7. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        cloudstack_configuration(dict[str, Any], Optional):
            cloudstack_configuration. Defaults to None.

            * access_key_id (str):
                CloudStack API Key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * api_url (str):
                CloudStack API URL. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * cntr_public_ip (str, Optional):
                If controller's management IP is in a private network, a publicly accessible IP to reach the controller. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * hypervisor (str, Optional):
                Default hypervisor type. Enum options - DEFAULT, VMWARE_ESX, KVM, VMWARE_VSAN, XEN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mgmt_network_name (str):
                Avi Management network name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mgmt_network_uuid (str, Optional):
                Avi Management network name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * secret_access_key (str):
                CloudStack Secret Key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        custom_tags(List[dict[str, Any]], Optional):
            Custom tags for all Avi created resources in the cloud infrastructure. Field introduced in 17.1.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * tag_key (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * tag_val (str, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        dhcp_enabled(bool, Optional):
            Select the IP address management scheme. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        dns_provider_ref(str, Optional):
            DNS Profile for the cloud. It is a reference to an object of type IpamDnsProviderProfile. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dns_resolution_on_se(bool, Optional):
            By default, pool member FQDNs are resolved on the Controller. When this is set, pool member FQDNs are instead resolved on Service Engines in this cloud. This is useful in scenarios where pool member FQDNs can only be resolved from Service Engines and not from the Controller. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        dns_resolvers(List[dict[str, Any]], Optional):
            DNS resolver for the cloud. Field introduced in 20.1.5. Maximum of 1 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * fixed_ttl (int, Optional):
                If configured, this value used for refreshing the DNS entries.Overrides both received_ttl and min_ttl. The entries are refreshed only on fixed_ttleven when received_ttl is less than fixed_ttl. Allowed values are 5-2147483647. Field introduced in 20.1.5. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * min_ttl (int, Optional):
                If configured, the min_ttl overrides the ttl from responses when ttl < min_ttl,effectively ttl = max(recieved_ttl, min_ttl). Allowed values are 5-2147483647. Field introduced in 20.1.5. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * nameserver_ips (List[dict[str, Any]], Optional):
                Name server IPv4 addresses. Field introduced in 20.1.5. Minimum of 1 items required. Maximum of 10 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * resolver_name (str):
                Unique name for resolver config. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * use_mgmt (bool, Optional):
                If enabled, DNS resolution is performed via management network. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        docker_configuration(dict[str, Any], Optional):
            docker_configuration. Defaults to None.

            * app_sync_frequency (int, Optional):
                Sync frequency in seconds with frameworks. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ca_tls_key_and_certificate_ref (str, Optional):
                UUID of the UCP CA TLS cert and key. It is a reference to an object of type SSLKeyAndCertificate. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * client_tls_key_and_certificate_ref (str, Optional):
                UUID of the client TLS cert and key. It is a reference to an object of type SSLKeyAndCertificate. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * container_port_match_http_service (bool, Optional):
                Perform container port matching to create a HTTP Virtualservice instead of a TCP/UDP VirtualService. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * coredump_directory (str, Optional):
                Directory to mount to check for core dumps on Service Engines. This will be mapped read only to /var/crash on any new Service Engines. This is a disruptive change. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disable_auto_backend_service_sync (bool, Optional):
                Disable auto service sync for back end services. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disable_auto_frontend_service_sync (bool, Optional):
                Disable auto service sync for front end services. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disable_auto_se_creation (bool, Optional):
                Disable SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * docker_registry_se (dict[str, Any], Optional):
                docker_registry_se

                * oshift_registry (dict[str, Any], Optional):
                    oshift_registry

                    * registry_namespace (str, Optional):
                        Namespace for the ServiceEngine image to be hosted in Openshift Integrated registry. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * registry_service (str, Optional):
                        Name of the Integrated registry Service in Openshift. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * registry_vip (dict[str, Any], Optional):
                        registry_vip

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * password (str, Optional):
                    Password for docker registry. Authorized 'regular user' password if registry is Openshift integrated registry. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * private (bool, Optional):
                    Set if docker registry is private. Avi controller will not attempt to push SE image to the registry, unless se_repository_push is set. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * registry (str, Optional):
                    Avi ServiceEngine repository name. For private registry, it's registry port/repository, for public registry, it's registry/repository, for openshift registry, it's registry port/namespace/repo. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * username (str, Optional):
                    Username for docker registry. Authorized 'regular user' if registry is Openshift integrated registry. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * east_west_placement_subnet (dict[str, Any], Optional):
                east_west_placement_subnet

                * ip_addr (dict[str, Any]):
                    ip_addr

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mask (int):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enable_event_subscription (bool, Optional):
                Enable Docker event subscription. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * feproxy_container_port_as_service (bool, Optional):
                For Front End proxies, use container port as service port. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * feproxy_vips_enable_proxy_arp (bool, Optional):
                Enable proxy ARP from Host interface for Front End  proxies. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * fleet_endpoint (str, Optional):
                Optional fleet remote endpoint if fleet is used for SE deployment. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_container_ports (List[int], Optional):
                List of container ports that create a HTTP Virtualservice instead of a TCP/UDP VirtualService. Defaults to 80. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_deployment_method (str, Optional):
                Use Fleet/SSH for SE deployment. Enum options - SE_CREATE_FLEET, SE_CREATE_SSH, SE_CREATE_POD. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_exclude_attributes (List[dict[str, Any]], Optional):
                Exclude hosts with attributes for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * attribute (str):
                    Attribute to match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * value (str, Optional):
                    Attribute value. If not set, match any value. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_include_attributes (List[dict[str, Any]], Optional):
                Create SEs just on hosts with include attributes. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * attribute (str):
                    Attribute to match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * value (str, Optional):
                    Attribute value. If not set, match any value. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_spawn_rate (int, Optional):
                New SE spawn rate per minute. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_volume (str, Optional):
                Host volume to be used as a disk for Avi SE, This is a disruptive change. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * services_accessible_all_interfaces (bool, Optional):
                Make service ports accessible on all Host interfaces in addition to East-West VIP and/or bridge IP. Usually enabled AWS clusters to export East-West services on Host interface. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ssh_user_ref (str, Optional):
                Cloud connector user uuid for SSH to hosts. It is a reference to an object of type CloudConnectorUser. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ucp_nodes (List[str], Optional):
                List of Docker UCP nodes; In case of a load balanced UCP cluster, use Virtual IP of the cluster. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_container_ip_port (bool, Optional):
                Use container IP address port for pool instead of host IP address hostport. This mode is applicable if the container IP is reachable (not a private NATed IP) from other hosts in a routed environment for containers. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_controller_image (bool, Optional):
                If true, use controller generated SE docker image via fileservice, else use docker repository image as defined by docker_registry_se. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        east_west_dns_provider_ref(str, Optional):
            DNS Profile for East-West services. It is a reference to an object of type IpamDnsProviderProfile. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        east_west_ipam_provider_ref(str, Optional):
            Ipam Profile for East-West services. Warning - Please use virtual subnets in this IPAM profile that do not conflict with the underlay networks or any overlay networks in the cluster. For example in AWS and GCP, 169.254.0.0/16 is used for storing instance metadata. Hence, it should not be used in this profile. It is a reference to an object of type IpamDnsProviderProfile. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        enable_vip_on_all_interfaces(bool, Optional):
            Enable VIP on all data interfaces for the Cloud. Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        enable_vip_static_routes(bool, Optional):
            Use static routes for VIP side network resolution during VirtualService placement. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        gcp_configuration(dict[str, Any], Optional):
            gcp_configuration. Defaults to None.

            * cloud_credentials_ref (str, Optional):
                Credentials to access Google Cloud Platform APIs. It is a reference to an object of type CloudConnectorUser. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * encryption_keys (dict[str, Any], Optional):
                encryption_keys

                * gcs_bucket_kms_key_id (str, Optional):
                    CMEK Resource ID to encrypt Google Cloud Storage Bucket. This Bucket is used to upload Service Engine raw image. Field introduced in 18.2.10, 20.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * gcs_objects_kms_key_id (str, Optional):
                    CMEK Resource ID to encrypt Service Engine raw image. The raw image is a Google Cloud Storage Object. Field introduced in 18.2.10, 20.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * se_disk_kms_key_id (str, Optional):
                    CMEK Resource ID to encrypt Service Engine Disks. Field introduced in 18.2.10, 20.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * se_image_kms_key_id (str, Optional):
                    CMEK Resource ID to encrypt Service Engine GCE Image. Field introduced in 18.2.10, 20.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * firewall_target_tags (List[str], Optional):
                Firewall rule network target tags which will be applied on Service Engines to allow ingress and egress traffic for Service Engines. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * gcp_service_account_email (str, Optional):
                Email of GCP Service Account to be associated to the Service Engines. Field introduced in 20.1.7, 21.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * gcs_bucket_name (str, Optional):
                Google Cloud Storage Bucket Name where Service Engine image will be uploaded. This image will be deleted once the image is created in Google compute images. By default, a bucket will be created if this field is not specified. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * gcs_project_id (str, Optional):
                Google Cloud Storage Project ID where Service Engine image will be uploaded. This image will be deleted once the image is created in Google compute images. By default, Service Engine Project ID will be used. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * network_config (dict[str, Any]):
                network_config

                * config (str):
                    Config Mode for Google Cloud network configuration. Enum options - INBAND_MANAGEMENT, ONE_ARM_MODE, TWO_ARM_MODE. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * inband (dict[str, Any], Optional):
                    inband

                    * vpc_network_name (str):
                        Service Engine Network Name. Field introduced in 18.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * vpc_project_id (str, Optional):
                        Project ID of the Service Engine Network. By default, Service Engine Project ID will be used. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * vpc_subnet_name (str):
                        Service Engine Network Subnet Name. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * one_arm (dict[str, Any], Optional):
                    one_arm

                    * data_vpc_network_name (str):
                        Service Engine Data Network Name. Field introduced in 18.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * data_vpc_project_id (str, Optional):
                        Project ID of the Service Engine Data Network. By default, Service Engine Project ID will be used. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * data_vpc_subnet_name (str):
                        Service Engine Data Network Subnet Name. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * management_vpc_network_name (str):
                        Service Engine Management Network Name. Field introduced in 18.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * management_vpc_project_id (str, Optional):
                        Project ID of the Service Engine Management Network. By default, Service Engine Project ID will be used. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * management_vpc_subnet_name (str):
                        Service Engine Management Network Subnet Name. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * two_arm (dict[str, Any], Optional):
                    two_arm

                    * backend_data_vpc_network_name (str):
                        Service Engine Backend Data Network Name. Field introduced in 18.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * backend_data_vpc_project_id (str, Optional):
                        Project ID of the Service Engine Backend Data Network. By default, Service Engine Project ID will be used. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * backend_data_vpc_subnet_name (str):
                        Service Engine Backend Data Network Subnet Name. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * frontend_data_vpc_network_name (str):
                        Service Engine Frontend Data Network Name. Field introduced in 18.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * frontend_data_vpc_project_id (str, Optional):
                        Project ID of the Service Engine Frontend Data Network. By default, Service Engine Project ID will be used. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * frontend_data_vpc_subnet_name (str):
                        Service Engine Frontend Data Network Subnet Name. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * management_vpc_network_name (str):
                        Service Engine Management Network Name. Field introduced in 18.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * management_vpc_project_id (str, Optional):
                        Project ID of the Service Engine Management Network. By default, Service Engine Project ID will be used. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * management_vpc_subnet_name (str):
                        Service Engine Management Network Subnet Name. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * region_name (str):
                Google Cloud Platform Region Name where Service Engines will be spawned. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_project_id (str):
                Google Cloud Platform Project ID where Service Engines will be spawned. Field introduced in 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vip_allocation_strategy (dict[str, Any]):
                vip_allocation_strategy

                * ilb (dict[str, Any], Optional):
                    ilb

                    * cloud_router_names (List[str], Optional):
                        Google Cloud Router Names to advertise BYOIP. Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mode (str):
                    VIP Allocation Mode. Enum options - ROUTES, ILB. Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * routes (dict[str, Any], Optional):
                    routes

                    * match_se_group_subnet (bool, Optional):
                        Match SE group subnets for VIP placement. Default is to not match SE group subnets. Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * route_priority (int, Optional):
                        Priority of the routes created in GCP. Field introduced in 20.1.7, 21.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * zones (List[str]):
                Google Cloud Platform Zones where Service Engines will be distributed for HA. Field introduced in 18.2.1. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        ip6_autocfg_enabled(bool, Optional):
            Enable IPv6 auto configuration. Field introduced in 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ipam_provider_ref(str, Optional):
            Ipam Profile for the cloud. It is a reference to an object of type IpamDnsProviderProfile. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        license_tier(str, Optional):
            Specifies the default license tier which would be used by new SE Groups. This field by default inherits the value from system configuration. Enum options - ENTERPRISE_16, ENTERPRISE, ENTERPRISE_18, BASIC, ESSENTIALS, ENTERPRISE_WITH_CLOUD_SERVICES. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        license_type(str, Optional):
            If no license type is specified then default license enforcement for the cloud type is chosen. The default mappings are Container Cloud is Max Ses, OpenStack and VMware is cores and linux it is Sockets. Enum options - LIC_BACKEND_SERVERS, LIC_SOCKETS, LIC_CORES, LIC_HOSTS, LIC_SE_BANDWIDTH, LIC_METERED_SE_BANDWIDTH. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        linuxserver_configuration(dict[str, Any], Optional):
            linuxserver_configuration. Defaults to None.

            * hosts (List[dict[str, Any]], Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * host_attr (List[dict[str, Any]], Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * attr_key (str):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * attr_val (str, Optional):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * host_ip (dict[str, Any]):
                    host_ip

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * node_availability_zone (str, Optional):
                    Node's availability zone. ServiceEngines belonging to the availability zone will be rebooted during a manual DR failover. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_group_ref (str, Optional):
                    The SE Group association for the SE. If None, then 'Default-Group' SEGroup is associated with the SE. It is a reference to an object of type ServiceEngineGroup. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_inband_mgmt (bool, Optional):
                Flag to notify the SE's in this cloud have an inband management interface, this can be overridden at SE host level by setting host_attr attr_key as SE_INBAND_MGMT with value of true or false. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_log_disk_path (str, Optional):
                SE Client Logs disk path for cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_log_disk_size_gb (int, Optional):
                SE Client Log disk size for cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_sys_disk_path (str, Optional):
                SE System Logs disk path for cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_sys_disk_size_gb (int, Optional):
                SE System Logs disk size for cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ssh_user_ref (str, Optional):
                Cloud connector user uuid for SSH to hosts. It is a reference to an object of type CloudConnectorUser. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        maintenance_mode(bool, Optional):
            Cloud is in maintenance mode. Field introduced in 20.1.7,21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        metrics_polling_interval(int, Optional):
            Cloud metrics collector polling interval in seconds. Field introduced in 22.1.1. Unit is SECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        mtu(int, Optional):
            MTU setting for the cloud. Unit is BYTES. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        nsxt_configuration(dict[str, Any], Optional):
            nsxt_configuration. Defaults to None.

            * automate_dfw_rules (bool, Optional):
                Automatically create DFW rules for VirtualService in NSX-T Manager. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Basic edition(Allowed values- false), Essentials, Enterprise with Cloud Services edition.

            * data_network_config (dict[str, Any], Optional):
                data_network_config

                * tier1_segment_config (dict[str, Any], Optional):
                    tier1_segment_config

                    * automatic (dict[str, Any], Optional):
                        automatic

                        * nsxt_segment_subnet (dict[str, Any]):
                            nsxt_segment_subnet

                            * ip_addr (dict[str, Any]):
                                ip_addr

                                * addr (str):
                                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                                * type (str):
                                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * mask (int):
                                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * num_se_per_segment (int, Optional):
                            The number of SE data vNic's that can be connected to the Avi logical segment. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * tier1_lr_ids (List[str], Optional):
                            Tier1 logical router IDs. Field introduced in 20.1.1. Minimum of 1 items required. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * manual (dict[str, Any], Optional):
                        manual

                        * tier1_lrs (List[dict[str, Any]], Optional):
                            Tier1 logical router placement information. Field introduced in 20.1.1. Minimum of 1 items required. Maximum of 256 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * locale_service (str, Optional):
                                Locale-services configuration, holds T1 edge-cluster information. When VirtualService is enabled with preserve client IP, ServiceInsertion VirtualEndpoint will be created in this locale-service. By default Avi controller picks default locale-service on T1. If more than one locale-services are present, this will be used for resolving the same. Example locale-service path - /infra/tier-1s/London_Tier1Gateway1/locale-services/London_Tier1LocalServices-1. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                            * segment_id (str, Optional):
                                Overlay segment path. Example- /infra/segments/Seg-Web-T1-01. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                            * tier1_lr_id (str):
                                Tier1 logical router path. Example- /infra/tier-1s/T1-01. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * segment_config_mode (str):
                        Config Mode for selecting the placement logical segments for Avi ServiceEngine data path. Enum options - TIER1_SEGMENT_MANUAL, TIER1_SEGMENT_AUTOMATIC. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Basic edition(Allowed values- TIER1_SEGMENT_MANUAL), Essentials, Enterprise with Cloud Services edition.

                * transport_zone (str):
                    Data transport zone path for Avi Service Engines. Example- /infra/sites/default/enforcement-points/default/transport-zones/xxx-xxx-xxxx. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * tz_type (str):
                    Data transport zone type overlay or vlan. Enum options - OVERLAY, VLAN. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * vlan_segments (List[str], Optional):
                    Data vlan segments path to use for Avi Service Engines. Example- /infra/segments/vlanls. This should be set only when transport zone is of type VLAN. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * domain_id (str, Optional):
                Domain where NSGroup objects belongs to. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enforcementpoint_id (str, Optional):
                Enforcement point is where the rules of a policy to apply. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * management_network_config (dict[str, Any], Optional):
                management_network_config

                * overlay_segment (dict[str, Any], Optional):
                    overlay_segment

                    * locale_service (str, Optional):
                        Locale-services configuration, holds T1 edge-cluster information. When VirtualService is enabled with preserve client IP, ServiceInsertion VirtualEndpoint will be created in this locale-service. By default Avi controller picks default locale-service on T1. If more than one locale-services are present, this will be used for resolving the same. Example locale-service path - /infra/tier-1s/London_Tier1Gateway1/locale-services/London_Tier1LocalServices-1. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                    * segment_id (str, Optional):
                        Overlay segment path. Example- /infra/segments/Seg-Web-T1-01. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * tier1_lr_id (str):
                        Tier1 logical router path. Example- /infra/tier-1s/T1-01. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * transport_zone (str):
                    Management transport zone path for Avi Service Engines. Example- /infra/sites/default/enforcement-points/default/transport-zones/xxx-xxx-xxxx. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * tz_type (str):
                    Management transport zone type overlay or vlan. Enum options - OVERLAY, VLAN. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * vlan_segment (str, Optional):
                    Management vlan segment path to use for Avi Service Engines. Example- /infra/segments/vlanls. This should be set only when transport zone is of type VLAN. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * nsxt_credentials_ref (str, Optional):
                Credentials to access NSX-T manager. It is a reference to an object of type CloudConnectorUser. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * nsxt_url (str, Optional):
                NSX-T manager hostname or IP address. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * site_id (str, Optional):
                Site where transport zone belongs to. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vmc_mode (bool, Optional):
                VMC mode. Field introduced in 23.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * vpc_mode (bool, Optional):
                VPC Mode. Field introduced in 23.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        ntp_configuration(dict[str, Any], Optional):
            ntp_configuration. Defaults to None.

            * ntp_authentication_keys (List[dict[str, Any]], Optional):
                NTP Authentication keys. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * algorithm (str, Optional):
                    Message Digest Algorithm used for NTP authentication. Default is NTP_AUTH_ALGORITHM_MD5. Enum options - NTP_AUTH_ALGORITHM_MD5, NTP_AUTH_ALGORITHM_SHA1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * key (str):
                    NTP Authentication key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * key_number (int):
                    Key number to be assigned to the authentication-key. Allowed values are 1-65534. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ntp_server_list (List[dict[str, Any]], Optional):
                List of NTP server hostnames or IP addresses. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ntp_servers (List[dict[str, Any]], Optional):
                List of NTP Servers. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * key_number (int, Optional):
                    Key number from the list of trusted keys used to authenticate this server. Allowed values are 1-65534. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * server (dict[str, Any]):
                    server

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        obj_name_prefix(str, Optional):
            Default prefix for all automatically created objects in this cloud. This prefix can be overridden by the SE-Group template. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        openstack_configuration(dict[str, Any], Optional):
            openstack_configuration. Defaults to None.

            * admin_tenant (str):
                OpenStack admin tenant (or project) information. For Keystone v3, provide the project information in project@domain format. Domain need not be specified if the project belongs to the 'Default' domain. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * admin_tenant_uuid (str, Optional):
                admin-tenant's UUID in OpenStack. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * allowed_address_pairs (bool, Optional):
                If false, allowed-address-pairs extension will not be used. . Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * anti_affinity (bool, Optional):
                If true, an anti-affinity policy will be applied to all SEs of a SE-Group, else no such policy will be applied. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * auth_url (str, Optional):
                Auth URL for connecting to keystone. If this is specified, any value provided for keystone_host is ignored. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * config_drive (bool, Optional):
                If false, metadata service will be used instead of  config-drive functionality to retrieve SE VM metadata. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * contrail_disable_policy (bool, Optional):
                When set to True, the VIP and Data ports will be programmed to set virtual machine interface disable-policy. Please refer Contrail documentation for more on disable-policy. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * contrail_endpoint (str, Optional):
                Contrail VNC endpoint url (example http //10.10.10.100 8082). By default, 'http //' scheme and 8082 port will be used if not provided in the url. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * contrail_plugin (bool, Optional):
                Enable Contrail plugin mode. (deprecated). Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * custom_se_image_properties (List[dict[str, Any]], Optional):
                Custom image properties to be set on a Service Engine image. Only hw_vif_multiqueue_enabled property is supported. Other properties will be ignored. Field introduced in 18.2.7, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str):
                    Property name. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * value (str, Optional):
                    Property value. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enable_os_object_caching (bool, Optional):
                When enabled, frequently used objects like networks, subnets, routers etc. are cached to improve performance and reduce load on OpenStack Controllers. Suitable for OpenStack environments where Neutron resources are not frequently created, updated, or deleted.The cache is refreshed when cloud GC API is issued. Field introduced in 21.1.5, 22.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * enable_tagging (bool, Optional):
                When set to True, OpenStack resources created by Avi are tagged with Avi Cloud UUID. Field introduced in 21.1.5, 22.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * external_networks (bool, Optional):
                If True, allow selection of networks marked as 'external' for management,  vip or data networks. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * free_floatingips (bool, Optional):
                Free unused floating IPs. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * hypervisor (str, Optional):
                Default hypervisor type, only KVM is supported. Enum options - DEFAULT, VMWARE_ESX, KVM, VMWARE_VSAN, XEN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * hypervisor_properties (List[dict[str, Any]], Optional):
                Custom properties per hypervisor type. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * hypervisor (str):
                    Hypervisor type. Enum options - DEFAULT, VMWARE_ESX, KVM, VMWARE_VSAN, XEN. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * image_properties (List[dict[str, Any]], Optional):
                    Custom properties to be associated with the SE image in Glance for this hypervisor type. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * name (str):
                        Property name. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * value (str, Optional):
                        Property value. Field introduced in 17.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * img_format (str, Optional):
                If OS_IMG_FMT_RAW, use RAW images else use QCOW2 for KVM. Enum options - OS_IMG_FMT_AUTO, OS_IMG_FMT_QCOW2, OS_IMG_FMT_VMDK, OS_IMG_FMT_RAW, OS_IMG_FMT_FLAT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * import_keystone_tenants (bool, Optional):
                Import keystone tenants list into Avi. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * insecure (bool, Optional):
                Allow self-signed certificates when communicating with https service endpoints. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * keystone_host (str, Optional):
                Keystone's hostname or IP address. (Deprecated) Use auth_url instead. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * map_admin_to_cloudadmin (bool, Optional):
                If True, map Avi 'admin' tenant to the admin_tenant of the Cloud. Else map Avi 'admin' to OpenStack 'admin' tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mgmt_network_name (str):
                Avi Management network name or cidr. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mgmt_network_uuid (str, Optional):
                Management network UUID. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * name_owner (bool, Optional):
                If True, embed owner info in VIP port 'name', else embed owner info in 'device_id' field. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * neutron_rbac (bool, Optional):
                If True, enable neutron rbac discovery of networks shared across tenants/projects. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * password (str, Optional):
                The password Avi Vantage will use when authenticating to Keystone. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * privilege (str):
                Access privilege. Enum options - NO_ACCESS, READ_ACCESS, WRITE_ACCESS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * prov_name (List[str], Optional):
                LBaaS provider name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * provider_vip_networks (List[dict[str, Any]], Optional):
                A tenant can normally use its own networks and any networks shared with it. In addition, this setting provides extra networks that are usable by tenants. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * os_network_uuid (str, Optional):
                    Neutron network UUID. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * os_tenant_uuids (List[str], Optional):
                    UUIDs of OpenStack tenants that should be allowed to use the specified Neutron network for VIPs. Use '*' to make this network available to all tenants. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * region (str, Optional):
                Region name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * role_mapping (List[dict[str, Any]], Optional):
                Defines the mapping from OpenStack role names to avi local role names. For an OpenStack role, this mapping is consulted only if there is no local Avi role with the same name as the OpenStack role. This is an ordered list and only the first matching entry is used. You can use '*' to match all OpenStack role names. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * avi_role (str):
                    Role name in Avi. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * os_role (str):
                    Role name in OpenStack. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * security_groups (bool, Optional):
                If false, security-groups extension will not be used. . Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * tenant_se (bool, Optional):
                If true, then SEs will be created in the appropriate tenants, else SEs will be created in the admin_tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_admin_url (bool, Optional):
                If admin URLs are either inaccessible or not to be accessed from Avi Controller, then set this to False. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_internal_endpoints (bool, Optional):
                Use internalURL for OpenStack endpoints instead of the default publicURL endpoints. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_keystone_auth (bool, Optional):
                Use keystone for user authentication. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * username (str):
                The username Avi Vantage will use when authenticating to Keystone. For Keystone v3, provide the user information in user@domain format, unless that user belongs to the Default domain. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vip_port_in_admin_tenant (bool, Optional):
                When set to True, VIP ports are created in OpenStack tenant configured as admin_tenant in cloud. Otherwise, default behavior is to create VIP ports in user tenant. Field introduced in 21.1.5, 22.1.2. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        prefer_static_routes(bool, Optional):
            Prefer static routes over interface routes during VirtualService placement. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        proxy_configuration(dict[str, Any], Optional):
            proxy_configuration. Defaults to None.

            * host (str):
                Proxy hostname or IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * password (str, Optional):
                Password for proxy. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * port (int):
                Proxy port. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * username (str, Optional):
                Username for proxy. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        rancher_configuration(dict[str, Any], Optional):
            rancher_configuration. Defaults to None.

            * access_key (str, Optional):
                Access key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * app_sync_frequency (int, Optional):
                Sync frequency in seconds with frameworks. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * container_port_match_http_service (bool, Optional):
                Perform container port matching to create a HTTP Virtualservice instead of a TCP/UDP VirtualService. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * coredump_directory (str, Optional):
                Directory to mount to check for core dumps on Service Engines. This will be mapped read only to /var/crash on any new Service Engines. This is a disruptive change. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disable_auto_backend_service_sync (bool, Optional):
                Disable auto service sync for back end services. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disable_auto_frontend_service_sync (bool, Optional):
                Disable auto service sync for front end services. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disable_auto_se_creation (bool, Optional):
                Disable SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * docker_registry_se (dict[str, Any], Optional):
                docker_registry_se

                * oshift_registry (dict[str, Any], Optional):
                    oshift_registry

                    * registry_namespace (str, Optional):
                        Namespace for the ServiceEngine image to be hosted in Openshift Integrated registry. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * registry_service (str, Optional):
                        Name of the Integrated registry Service in Openshift. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * registry_vip (dict[str, Any], Optional):
                        registry_vip

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * password (str, Optional):
                    Password for docker registry. Authorized 'regular user' password if registry is Openshift integrated registry. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * private (bool, Optional):
                    Set if docker registry is private. Avi controller will not attempt to push SE image to the registry, unless se_repository_push is set. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * registry (str, Optional):
                    Avi ServiceEngine repository name. For private registry, it's registry port/repository, for public registry, it's registry/repository, for openshift registry, it's registry port/namespace/repo. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * username (str, Optional):
                    Username for docker registry. Authorized 'regular user' if registry is Openshift integrated registry. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * east_west_placement_subnet (dict[str, Any], Optional):
                east_west_placement_subnet

                * ip_addr (dict[str, Any]):
                    ip_addr

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mask (int):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enable_event_subscription (bool, Optional):
                Enable Docker event subscription. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * feproxy_container_port_as_service (bool, Optional):
                For Front End proxies, use container port as service port. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * feproxy_vips_enable_proxy_arp (bool, Optional):
                Enable proxy ARP from Host interface for Front End  proxies. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * fleet_endpoint (str, Optional):
                Optional fleet remote endpoint if fleet is used for SE deployment. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * http_container_ports (List[int], Optional):
                List of container ports that create a HTTP Virtualservice instead of a TCP/UDP VirtualService. Defaults to 80. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * nuage_controller (dict[str, Any], Optional):
                nuage_controller

                * nuage_organization (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * nuage_password (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * nuage_port (int, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * nuage_username (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * nuage_vsd_host (str, Optional):
                    Nuage VSD host name or IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_domain (str, Optional):
                    Domain to be used for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_enterprise (str, Optional):
                    Enterprise to be used for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_network (str, Optional):
                    Network to be used for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_policy_group (str, Optional):
                    Policy Group to be used for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_user (str, Optional):
                    User to be used for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * se_zone (str, Optional):
                    Zone to be used for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * rancher_servers (List[str], Optional):
                List of Rancher servers; In case of a load balanced Rancher multi cluster, use Virtual IP of the cluster. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_deployment_method (str, Optional):
                Use Fleet/SSH for SE deployment. Enum options - SE_CREATE_FLEET, SE_CREATE_SSH, SE_CREATE_POD. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_exclude_attributes (List[dict[str, Any]], Optional):
                Exclude hosts with attributes for SE creation. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * attribute (str):
                    Attribute to match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * value (str, Optional):
                    Attribute value. If not set, match any value. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_include_attributes (List[dict[str, Any]], Optional):
                Create SEs just on hosts with include attributes. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * attribute (str):
                    Attribute to match. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * value (str, Optional):
                    Attribute value. If not set, match any value. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_spawn_rate (int, Optional):
                New SE spawn rate per minute. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * se_volume (str, Optional):
                Host volume to be used as a disk for Avi SE, This is a disruptive change. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * secret_key (str, Optional):
                Secret key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * services_accessible_all_interfaces (bool, Optional):
                Make service ports accessible on all Host interfaces in addition to East-West VIP and/or bridge IP. Usually enabled AWS clusters to export East-West services on Host interface. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ssh_user_ref (str, Optional):
                Cloud connector user uuid for SSH to hosts. It is a reference to an object of type CloudConnectorUser. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_container_ip_port (bool, Optional):
                Use container IP address port for pool instead of host IP address hostport. This mode is applicable if the container IP is reachable (not a private NATed IP) from other hosts in a routed environment for containers. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_controller_image (bool, Optional):
                If true, use controller generated SE docker image via fileservice, else use docker repository image as defined by docker_registry_se. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        se_group_template_ref(str, Optional):
            The Service Engine Group to use as template. It is a reference to an object of type ServiceEngineGroup. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        state_based_dns_registration(bool, Optional):
            DNS records for VIPs are added/deleted based on the operational state of the VIPs. Field introduced in 17.1.12. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- true), Basic edition(Allowed values- true), Enterprise with Cloud Services edition. Defaults to None.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vca_configuration(dict[str, Any], Optional):
            vca_configuration. Defaults to None.

            * privilege (str):
                vCloudAir access mode. Enum options - NO_ACCESS, READ_ACCESS, WRITE_ACCESS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_host (str):
                vCloudAir host address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_instance (str):
                vCloudAir instance ID. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_mgmt_network (str):
                vCloudAir management network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_orgnization (str):
                vCloudAir orgnization ID. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_password (str):
                vCloudAir password. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_username (str):
                vCloudAir username. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vca_vdc (str):
                vCloudAir virtual data center name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vcenter_configuration(dict[str, Any], Optional):
            vcenter_configuration. Defaults to None.

            * content_lib (dict[str, Any], Optional):
                content_lib

                * id (str, Optional):
                    Content Library Id. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * name (str, Optional):
                    Content Library name. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * datacenter (str, Optional):
                Datacenter for virtual infrastructure discovery. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * deactivate_vm_discovery (bool, Optional):
                If true, VM's on the vCenter will not be discovered.Set it to true if there are more than 10000 VMs in the datacenter. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * is_nsx_environment (bool, Optional):
                If true, NSX-T segment spanning multiple VDS with vCenter cloud are merged to a single network in Avi. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * management_ip_subnet (dict[str, Any], Optional):
                management_ip_subnet

                * ip_addr (dict[str, Any]):
                    ip_addr

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * mask (int):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * management_network (str, Optional):
                Management network to use for Avi Service Engines. It is a reference to an object of type VIMgrNWRuntime. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * password (str, Optional):
                The password Avi Vantage will use when authenticating with vCenter. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * privilege (str):
                Set the access mode to vCenter as either Read, which allows Avi to discover networks and servers, or Write, which also allows Avi to create Service Engines and configure their network properties. Enum options - NO_ACCESS, READ_ACCESS, WRITE_ACCESS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * use_content_lib (bool, Optional):
                If false, Service Engine image will not be pushed to content library. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Enterprise with Cloud Services edition.

            * username (str, Optional):
                The username Avi Vantage will use when authenticating with vCenter. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vcenter_template_se_location (str, Optional):
                Avi Service Engine Template in vCenter to be used for creating Service Engines. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vcenter_url (str, Optional):
                vCenter hostname or IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vmc_deployment(bool, Optional):
            This deployment is VMware on AWS cloud. Field introduced in 20.1.5, 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              nsx_alb.alb.cloud.present:
                - resource_id: value
                - vtype: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.cloud.update resource_id=value, vtype=value
    """

    result = dict(comment=[], ret=[], result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "autoscale_polling_interval": "autoscale_polling_interval",
        "aws_configuration": "aws_configuration",
        "azure_configuration": "azure_configuration",
        "cloudstack_configuration": "cloudstack_configuration",
        "configpb_attributes": "configpb_attributes",
        "custom_tags": "custom_tags",
        "dhcp_enabled": "dhcp_enabled",
        "dns_provider_ref": "dns_provider_ref",
        "dns_resolution_on_se": "dns_resolution_on_se",
        "dns_resolvers": "dns_resolvers",
        "docker_configuration": "docker_configuration",
        "east_west_dns_provider_ref": "east_west_dns_provider_ref",
        "east_west_ipam_provider_ref": "east_west_ipam_provider_ref",
        "enable_vip_on_all_interfaces": "enable_vip_on_all_interfaces",
        "enable_vip_static_routes": "enable_vip_static_routes",
        "gcp_configuration": "gcp_configuration",
        "ip6_autocfg_enabled": "ip6_autocfg_enabled",
        "ipam_provider_ref": "ipam_provider_ref",
        "license_tier": "license_tier",
        "license_type": "license_type",
        "linuxserver_configuration": "linuxserver_configuration",
        "maintenance_mode": "maintenance_mode",
        "markers": "markers",
        "metrics_polling_interval": "metrics_polling_interval",
        "mtu": "mtu",
        "name": "name",
        "nsxt_configuration": "nsxt_configuration",
        "ntp_configuration": "ntp_configuration",
        "obj_name_prefix": "obj_name_prefix",
        "openstack_configuration": "openstack_configuration",
        "prefer_static_routes": "prefer_static_routes",
        "proxy_configuration": "proxy_configuration",
        "rancher_configuration": "rancher_configuration",
        "se_group_template_ref": "se_group_template_ref",
        "state_based_dns_registration": "state_based_dns_registration",
        "tenant_ref": "tenant_ref",
        "vca_configuration": "vca_configuration",
        "vcenter_configuration": "vcenter_configuration",
        "vmc_deployment": "vmc_deployment",
        "vtype": "vtype",
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
            path="/cloud/{uuid}".format(**{"uuid": resource_id}),
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
            f"Updated nsx_alb.alb.cloud '{name}'",
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
            Alb.cloud unique ID.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              nsx_alb.alb.cloud.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.cloud.delete resource_id=value
    """

    result = dict(comment=[], ret=[], result=True)

    before = await hub.exec.nsx_alb.alb.cloud.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )
    if before["ret"]:
        tenant_name = before["ret"]["tenant_ref"].split("#")[-1]
    delete = await hub.tool.nsx_alb.session.request(
        ctx,
        method="delete",
        path="/cloud/{uuid}".format(**{"uuid": resource_id}),
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
