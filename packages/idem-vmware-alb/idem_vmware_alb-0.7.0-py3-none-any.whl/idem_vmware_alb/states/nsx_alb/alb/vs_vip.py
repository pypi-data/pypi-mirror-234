"""States module for managing Alb Vs Vips. """
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
    bgp_peer_labels: List[str] = None,
    cloud_ref: str = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
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
    east_west_placement: bool = None,
    ipam_selector: make_dataclass(
        "ipam_selector",
        [
            ("type", str),
            (
                "labels",
                List[
                    make_dataclass(
                        "labels", [("key", str), ("value", str, field(default=None))]
                    )
                ],
                field(default=None),
            ),
        ],
    ) = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    tenant_ref: str = None,
    tier1_lr: str = None,
    use_standard_alb: bool = None,
    vip: List[
        make_dataclass(
            "vip",
            [
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
                ("vip_id", str, field(default=None)),
            ],
        )
    ] = None,
    vrf_context_ref: str = None,
    vsvip_cloud_config_cksum: str = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:
        name(str):
            Idem name of the resource.

        resource_id(str, Optional):
            Alb.vs_vip unique ID. Defaults to None.

        bgp_peer_labels(List[str], Optional):
            Select BGP peers, using peer label, for VsVip advertisement. Field introduced in 20.1.5. Maximum of 128 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        cloud_ref(str, Optional):
             It is a reference to an object of type Cloud. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        dns_info(List[dict[str, Any]], Optional):
            Service discovery specific data including fully qualified domain name, type and Time-To-Live of the DNS record. Field introduced in 17.1.1. Maximum of 1000 items allowed. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

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

        east_west_placement(bool, Optional):
            Force placement on all Service Engines in the Service Engine Group (Container clouds only). Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        ipam_selector(dict[str, Any], Optional):
            ipam_selector. Defaults to None.

            * labels (List[dict[str, Any]], Optional):
                Labels as key value pairs to select on. Field introduced in 20.1.3. Minimum of 1 items required. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * key (str):
                    Key. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * value (str, Optional):
                    Value. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * type (str):
                Selector type. Enum options - SELECTOR_IPAM. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.5. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        tier1_lr(str, Optional):
            This sets the placement scope of virtualservice to given tier1 logical router in Nsx-t. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        use_standard_alb(bool, Optional):
            This overrides the cloud level default and needs to match the SE Group value in which it will be used if the SE Group use_standard_alb value is set. This is only used when FIP is used for VS on Azure Cloud. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vip(List[dict[str, Any]], Optional):
            List of Virtual Service IPs and other shareable entities. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

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

            * vip_id (str, Optional):
                Unique ID associated with the vip. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vrf_context_ref(str, Optional):
            Virtual Routing Context that the Virtual Service is bound to. This is used to provide the isolation of the set of networks the application is attached to. It is a reference to an object of type VrfContext. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vsvip_cloud_config_cksum(str, Optional):
            Checksum of cloud configuration for VsVip. Internally set by cloud connector. Field introduced in 17.2.9, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


          idem_test_nsx_alb.alb.vs_vip_is_present:
              nsx_alb.nsx_alb.alb.vs_vip.present:
              - bgp_peer_labels:
                - value
              - cloud_ref: string
              - configpb_attributes:
                  version: int
              - dns_info:
                - algorithm: string
                  cname:
                    cname: string
                  fqdn: string
                  metadata: string
                  num_records_in_response: int
                  ttl: int
                  type_: string
              - east_west_placement: bool
              - ipam_selector:
                  labels:
                  - key: string
                    value: string
                  type_: string
              - markers:
                - key: string
                  values:
                  - value
              - tenant_ref: string
              - tier1_lr: string
              - use_standard_alb: bool
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
              - vsvip_cloud_config_cksum: string


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    for count in range(0, len(vip)):
        if not vip[count].get("vip_id"):
            vip[count]["vip_id"] = count

    if resource_id:
        before = await hub.exec.nsx_alb.alb.vs_vip.get(
            ctx,
            name=name,
            resource_id=resource_id,
        )

        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = before.ret

        result["comment"].append(f"'nsx_alb.alb.vs_vip:{name}' already exists")

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

        before = await hub.exec.nsx_alb.alb.vs_vip.get(
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
                    before = await hub.exec.nsx_alb.alb.vs_vip.get(
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
                result["comment"] = (f"Would update nsx_alb.alb.vs_vip '{name}'",)
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.nsx_alb.alb.vs_vip.update(
                    ctx,
                    name=name,
                    resource_id=resource_id,
                    **{
                        "bgp_peer_labels": bgp_peer_labels,
                        "cloud_ref": cloud_ref,
                        "configpb_attributes": configpb_attributes,
                        "dns_info": dns_info,
                        "east_west_placement": east_west_placement,
                        "ipam_selector": ipam_selector,
                        "markers": markers,
                        "tenant_ref": tenant_ref,
                        "tier1_lr": tier1_lr,
                        "use_standard_alb": use_standard_alb,
                        "vip": vip,
                        "vrf_context_ref": vrf_context_ref,
                        "vsvip_cloud_config_cksum": vsvip_cloud_config_cksum,
                    },
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"].append(f"Updated 'nsx_alb.alb.vs_vip:{name}'")
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.test:
            result["new_state"] = hub.tool.nsx_alb.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"] = (f"Would create nsx_alb.alb.vs_vip {name}",)
            return result
        else:
            create_ret = await hub.exec.nsx_alb.alb.vs_vip.create(
                ctx,
                name=name,
                **{
                    "resource_id": resource_id,
                    "bgp_peer_labels": bgp_peer_labels,
                    "cloud_ref": cloud_ref,
                    "configpb_attributes": configpb_attributes,
                    "dns_info": dns_info,
                    "east_west_placement": east_west_placement,
                    "ipam_selector": ipam_selector,
                    "markers": markers,
                    "tenant_ref": tenant_ref,
                    "tier1_lr": tier1_lr,
                    "use_standard_alb": use_standard_alb,
                    "vip": vip,
                    "vrf_context_ref": vrf_context_ref,
                    "vsvip_cloud_config_cksum": vsvip_cloud_config_cksum,
                },
            )
            result["result"] = create_ret["result"]

            if result["result"]:
                result["comment"].append(f"Created 'nsx_alb.alb.vs_vip:{name}'")
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

    after = await hub.exec.nsx_alb.alb.vs_vip.get(
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
            Alb.vs_vip unique ID. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


            idem_test_nsx_alb.alb.vs_vip_is_absent:
              nsx_alb.nsx_alb.alb.vs_vip.absent:

    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        result["comment"].append(f"'nsx_alb.alb.vs_vip:{name}' already absent")
        return result

    before = await hub.exec.nsx_alb.alb.vs_vip.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    if before["ret"]:
        if ctx.test:
            result["comment"] = f"Would delete nsx_alb.alb.vs_vip:{name}"
            return result

        delete_ret = await hub.exec.nsx_alb.alb.vs_vip.delete(
            ctx,
            name=name,
            resource_id=resource_id,
        )
        result["result"] = delete_ret["result"]

        if result["result"]:
            result["comment"].append(f"Deleted 'nsx_alb.alb.vs_vip:{name}'")
        else:
            # If there is any failure in delete, it should reconcile.
            # The type of data is less important here to use default reconciliation
            # If there are no changes for 3 runs with rerun_data, then it will come out of execution
            result["rerun_data"] = resource_id
            result["comment"].append(delete_ret["result"])
    else:
        result["comment"].append(f"'nsx_alb.alb.vs_vip:{name}' already absent")
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

            $ idem describe nsx_alb.alb.vs_vip
    """

    result = {}

    ret = await hub.exec.nsx_alb.alb.vs_vip.list(ctx)

    if not ret or not ret["result"]:
        hub.log.debug(f"Could not describe nsx_alb.alb.vs_vip {ret['comment']}")
        return result

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "nsx_alb.alb.vs_vip.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
