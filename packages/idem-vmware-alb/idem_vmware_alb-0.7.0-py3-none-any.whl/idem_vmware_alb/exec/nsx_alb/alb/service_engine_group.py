"""Exec module for managing Alb Service Engine Groups. """
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
            Alb.service_engine_group unique ID.

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
                - path: nsx_alb.alb.service_engine_group.get
                - kwargs:
                  resource_id: value
                  x_avi_version: value
                  uuid: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.service_engine_group.get resource_id=value, x_avi_version=value, uuid=value
    """

    result = dict(comment=[], ret=None, result=True)

    get = await hub.tool.nsx_alb.session.request(
        ctx,
        method="get",
        path="/serviceenginegroup/{uuid}?include_name".format(**{"uuid": resource_id})
        if resource_id
        else "/serviceenginegroup?include_name",
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
            "accelerated_networking": "accelerated_networking",
            "active_standby": "active_standby",
            "aggressive_failure_detection": "aggressive_failure_detection",
            "algo": "algo",
            "allow_burst": "allow_burst",
            "app_cache_percent": "app_cache_percent",
            "app_cache_threshold": "app_cache_threshold",
            "app_learning_memory_percent": "app_learning_memory_percent",
            "archive_shm_limit": "archive_shm_limit",
            "async_ssl": "async_ssl",
            "async_ssl_threads": "async_ssl_threads",
            "auto_rebalance": "auto_rebalance",
            "auto_rebalance_capacity_per_se": "auto_rebalance_capacity_per_se",
            "auto_rebalance_criteria": "auto_rebalance_criteria",
            "auto_rebalance_interval": "auto_rebalance_interval",
            "auto_redistribute_active_standby_load": "auto_redistribute_active_standby_load",
            "availability_zone_refs": "availability_zone_refs",
            "baremetal_dispatcher_handles_flows": "baremetal_dispatcher_handles_flows",
            "bgp_peer_monitor_failover_enabled": "bgp_peer_monitor_failover_enabled",
            "bgp_state_update_interval": "bgp_state_update_interval",
            "buffer_se": "buffer_se",
            "cloud_ref": "cloud_ref",
            "compress_ip_rules_for_each_ns_subnet": "compress_ip_rules_for_each_ns_subnet",
            "config_debugs_on_all_cores": "config_debugs_on_all_cores",
            "configpb_attributes": "configpb_attributes",
            "connection_memory_percentage": "connection_memory_percentage",
            "core_shm_app_cache": "core_shm_app_cache",
            "core_shm_app_learning": "core_shm_app_learning",
            "cpu_reserve": "cpu_reserve",
            "cpu_socket_affinity": "cpu_socket_affinity",
            "custom_securitygroups_data": "custom_securitygroups_data",
            "custom_securitygroups_mgmt": "custom_securitygroups_mgmt",
            "custom_tag": "custom_tag",
            "data_network_id": "data_network_id",
            "datascript_timeout": "datascript_timeout",
            "deactivate_ipv6_discovery": "deactivate_ipv6_discovery",
            "deactivate_kni_filtering_at_dispatcher": "deactivate_kni_filtering_at_dispatcher",
            "dedicated_dispatcher_core": "dedicated_dispatcher_core",
            "description": "description",
            "disable_avi_securitygroups": "disable_avi_securitygroups",
            "disable_csum_offloads": "disable_csum_offloads",
            "disable_flow_probes": "disable_flow_probes",
            "disable_gro": "disable_gro",
            "disable_se_memory_check": "disable_se_memory_check",
            "disable_tso": "disable_tso",
            "disk_per_se": "disk_per_se",
            "distribute_load_active_standby": "distribute_load_active_standby",
            "distribute_queues": "distribute_queues",
            "distribute_vnics": "distribute_vnics",
            "downstream_send_timeout": "downstream_send_timeout",
            "dp_aggressive_deq_interval_msec": "dp_aggressive_deq_interval_msec",
            "dp_aggressive_enq_interval_msec": "dp_aggressive_enq_interval_msec",
            "dp_aggressive_hb_frequency": "dp_aggressive_hb_frequency",
            "dp_aggressive_hb_timeout_count": "dp_aggressive_hb_timeout_count",
            "dp_deq_interval_msec": "dp_deq_interval_msec",
            "dp_enq_interval_msec": "dp_enq_interval_msec",
            "dp_hb_frequency": "dp_hb_frequency",
            "dp_hb_timeout_count": "dp_hb_timeout_count",
            "dpdk_gro_timeout_interval": "dpdk_gro_timeout_interval",
            "enable_gratarp_permanent": "enable_gratarp_permanent",
            "enable_hsm_log": "enable_hsm_log",
            "enable_hsm_priming": "enable_hsm_priming",
            "enable_multi_lb": "enable_multi_lb",
            "enable_pcap_tx_ring": "enable_pcap_tx_ring",
            "ephemeral_portrange_end": "ephemeral_portrange_end",
            "ephemeral_portrange_start": "ephemeral_portrange_start",
            "extra_config_multiplier": "extra_config_multiplier",
            "extra_shared_config_memory": "extra_shared_config_memory",
            "flow_table_new_syn_max_entries": "flow_table_new_syn_max_entries",
            "free_list_size": "free_list_size",
            "gcp_config": "gcp_config",
            "gratarp_permanent_periodicity": "gratarp_permanent_periodicity",
            "grpc_channel_connect_timeout": "grpc_channel_connect_timeout",
            "ha_mode": "ha_mode",
            "handle_per_pkt_attack": "handle_per_pkt_attack",
            "hardwaresecuritymodulegroup_ref": "hardwaresecuritymodulegroup_ref",
            "heap_minimum_config_memory": "heap_minimum_config_memory",
            "hm_on_standby": "hm_on_standby",
            "host_attribute_key": "host_attribute_key",
            "host_attribute_value": "host_attribute_value",
            "host_gateway_monitor": "host_gateway_monitor",
            "http_rum_console_log": "http_rum_console_log",
            "http_rum_min_content_length": "http_rum_min_content_length",
            "hybrid_rss_mode": "hybrid_rss_mode",
            "hypervisor": "hypervisor",
            "ignore_docker_mac_change": "ignore_docker_mac_change",
            "ignore_rtt_threshold": "ignore_rtt_threshold",
            "ingress_access_data": "ingress_access_data",
            "ingress_access_mgmt": "ingress_access_mgmt",
            "instance_flavor": "instance_flavor",
            "instance_flavor_info": "instance_flavor_info",
            "iptables": "iptables",
            "kni_allowed_server_ports": "kni_allowed_server_ports",
            "l7_conns_per_core": "l7_conns_per_core",
            "l7_resvd_listen_conns_per_core": "l7_resvd_listen_conns_per_core",
            "labels": "labels",
            "lbaction_num_requests_to_dispatch": "lbaction_num_requests_to_dispatch",
            "lbaction_rq_per_request_max_retries": "lbaction_rq_per_request_max_retries",
            "least_load_core_selection": "least_load_core_selection",
            "license_tier": "license_tier",
            "license_type": "license_type",
            "log_agent_compress_logs": "log_agent_compress_logs",
            "log_agent_debug_enabled": "log_agent_debug_enabled",
            "log_agent_file_sz_appl": "log_agent_file_sz_appl",
            "log_agent_file_sz_conn": "log_agent_file_sz_conn",
            "log_agent_file_sz_debug": "log_agent_file_sz_debug",
            "log_agent_file_sz_event": "log_agent_file_sz_event",
            "log_agent_log_storage_min_sz": "log_agent_log_storage_min_sz",
            "log_agent_max_concurrent_rsync": "log_agent_max_concurrent_rsync",
            "log_agent_max_storage_excess_percent": "log_agent_max_storage_excess_percent",
            "log_agent_max_storage_ignore_percent": "log_agent_max_storage_ignore_percent",
            "log_agent_min_storage_per_vs": "log_agent_min_storage_per_vs",
            "log_agent_sleep_interval": "log_agent_sleep_interval",
            "log_agent_trace_enabled": "log_agent_trace_enabled",
            "log_agent_unknown_vs_timer": "log_agent_unknown_vs_timer",
            "log_disksz": "log_disksz",
            "log_malloc_failure": "log_malloc_failure",
            "log_message_max_file_list_size": "log_message_max_file_list_size",
            "markers": "markers",
            "max_concurrent_external_hm": "max_concurrent_external_hm",
            "max_cpu_usage": "max_cpu_usage",
            "max_memory_per_mempool": "max_memory_per_mempool",
            "max_num_se_dps": "max_num_se_dps",
            "max_public_ips_per_lb": "max_public_ips_per_lb",
            "max_queues_per_vnic": "max_queues_per_vnic",
            "max_rules_per_lb": "max_rules_per_lb",
            "max_scaleout_per_vs": "max_scaleout_per_vs",
            "max_se": "max_se",
            "max_skb_frags": "max_skb_frags",
            "max_vs_per_se": "max_vs_per_se",
            "mem_reserve": "mem_reserve",
            "memory_for_config_update": "memory_for_config_update",
            "memory_per_se": "memory_per_se",
            "mgmt_network_ref": "mgmt_network_ref",
            "mgmt_subnet": "mgmt_subnet",
            "min_cpu_usage": "min_cpu_usage",
            "min_scaleout_per_vs": "min_scaleout_per_vs",
            "min_se": "min_se",
            "minimum_connection_memory": "minimum_connection_memory",
            "n_log_streaming_threads": "n_log_streaming_threads",
            "name": "name",
            "netlink_poller_threads": "netlink_poller_threads",
            "netlink_sock_buf_size": "netlink_sock_buf_size",
            "ngx_free_connection_stack": "ngx_free_connection_stack",
            "non_significant_log_throttle": "non_significant_log_throttle",
            "ns_helper_deq_interval_msec": "ns_helper_deq_interval_msec",
            "ntp_sync_fail_event": "ntp_sync_fail_event",
            "ntp_sync_status_interval": "ntp_sync_status_interval",
            "num_dispatcher_cores": "num_dispatcher_cores",
            "num_dispatcher_queues": "num_dispatcher_queues",
            "num_flow_cores_sum_changes_to_ignore": "num_flow_cores_sum_changes_to_ignore",
            "objsync_config": "objsync_config",
            "objsync_port": "objsync_port",
            "openstack_availability_zones": "openstack_availability_zones",
            "openstack_mgmt_network_name": "openstack_mgmt_network_name",
            "openstack_mgmt_network_uuid": "openstack_mgmt_network_uuid",
            "os_reserved_memory": "os_reserved_memory",
            "pcap_tx_mode": "pcap_tx_mode",
            "pcap_tx_ring_rd_balancing_factor": "pcap_tx_ring_rd_balancing_factor",
            "per_app": "per_app",
            "per_vs_admission_control": "per_vs_admission_control",
            "placement_mode": "placement_mode",
            "realtime_se_metrics": "realtime_se_metrics",
            "reboot_on_panic": "reboot_on_panic",
            "replay_vrf_routes_interval": "replay_vrf_routes_interval",
            "resync_time_interval": "resync_time_interval",
            "sdb_flush_interval": "sdb_flush_interval",
            "sdb_pipeline_size": "sdb_pipeline_size",
            "sdb_scan_count": "sdb_scan_count",
            "se_bandwidth_type": "se_bandwidth_type",
            "se_delayed_flow_delete": "se_delayed_flow_delete",
            "se_deprovision_delay": "se_deprovision_delay",
            "se_dos_profile": "se_dos_profile",
            "se_dp_hm_drops": "se_dp_hm_drops",
            "se_dp_if_state_poll_interval": "se_dp_if_state_poll_interval",
            "se_dp_isolation": "se_dp_isolation",
            "se_dp_isolation_num_non_dp_cpus": "se_dp_isolation_num_non_dp_cpus",
            "se_dp_log_nf_enqueue_percent": "se_dp_log_nf_enqueue_percent",
            "se_dp_log_udf_enqueue_percent": "se_dp_log_udf_enqueue_percent",
            "se_dp_max_hb_version": "se_dp_max_hb_version",
            "se_dp_vnic_queue_stall_event_sleep": "se_dp_vnic_queue_stall_event_sleep",
            "se_dp_vnic_queue_stall_threshold": "se_dp_vnic_queue_stall_threshold",
            "se_dp_vnic_queue_stall_timeout": "se_dp_vnic_queue_stall_timeout",
            "se_dp_vnic_restart_on_queue_stall_count": "se_dp_vnic_restart_on_queue_stall_count",
            "se_dp_vnic_stall_se_restart_window": "se_dp_vnic_stall_se_restart_window",
            "se_dpdk_pmd": "se_dpdk_pmd",
            "se_dump_core_on_assert": "se_dump_core_on_assert",
            "se_emulated_cores": "se_emulated_cores",
            "se_flow_probe_retries": "se_flow_probe_retries",
            "se_flow_probe_retry_timer": "se_flow_probe_retry_timer",
            "se_group_analytics_policy": "se_group_analytics_policy",
            "se_hyperthreaded_mode": "se_hyperthreaded_mode",
            "se_ip_encap_ipc": "se_ip_encap_ipc",
            "se_kni_burst_factor": "se_kni_burst_factor",
            "se_l3_encap_ipc": "se_l3_encap_ipc",
            "se_log_buffer_app_blocking_dequeue": "se_log_buffer_app_blocking_dequeue",
            "se_log_buffer_conn_blocking_dequeue": "se_log_buffer_conn_blocking_dequeue",
            "se_log_buffer_events_blocking_dequeue": "se_log_buffer_events_blocking_dequeue",
            "se_lro": "se_lro",
            "se_mp_ring_retry_count": "se_mp_ring_retry_count",
            "se_mtu": "se_mtu",
            "se_name_prefix": "se_name_prefix",
            "se_packet_buffer_max": "se_packet_buffer_max",
            "se_pcap_lookahead": "se_pcap_lookahead",
            "se_pcap_pkt_count": "se_pcap_pkt_count",
            "se_pcap_pkt_sz": "se_pcap_pkt_sz",
            "se_pcap_qdisc_bypass": "se_pcap_qdisc_bypass",
            "se_pcap_reinit_frequency": "se_pcap_reinit_frequency",
            "se_pcap_reinit_threshold": "se_pcap_reinit_threshold",
            "se_probe_port": "se_probe_port",
            "se_rl_prop": "se_rl_prop",
            "se_rum_sampling_nav_interval": "se_rum_sampling_nav_interval",
            "se_rum_sampling_nav_percent": "se_rum_sampling_nav_percent",
            "se_rum_sampling_res_interval": "se_rum_sampling_res_interval",
            "se_rum_sampling_res_percent": "se_rum_sampling_res_percent",
            "se_sb_dedicated_core": "se_sb_dedicated_core",
            "se_sb_threads": "se_sb_threads",
            "se_thread_multiplier": "se_thread_multiplier",
            "se_time_tracker_props": "se_time_tracker_props",
            "se_tracert_port_range": "se_tracert_port_range",
            "se_tunnel_mode": "se_tunnel_mode",
            "se_tunnel_udp_port": "se_tunnel_udp_port",
            "se_tx_batch_size": "se_tx_batch_size",
            "se_txq_threshold": "se_txq_threshold",
            "se_udp_encap_ipc": "se_udp_encap_ipc",
            "se_use_dpdk": "se_use_dpdk",
            "se_vnic_tx_sw_queue_flush_frequency": "se_vnic_tx_sw_queue_flush_frequency",
            "se_vnic_tx_sw_queue_size": "se_vnic_tx_sw_queue_size",
            "se_vs_hb_max_pkts_in_batch": "se_vs_hb_max_pkts_in_batch",
            "se_vs_hb_max_vs_in_pkt": "se_vs_hb_max_vs_in_pkt",
            "self_se_election": "self_se_election",
            "send_se_ready_timeout": "send_se_ready_timeout",
            "service_ip6_subnets": "service_ip6_subnets",
            "service_ip_subnets": "service_ip_subnets",
            "shm_minimum_config_memory": "shm_minimum_config_memory",
            "significant_log_throttle": "significant_log_throttle",
            "ssl_preprocess_sni_hostname": "ssl_preprocess_sni_hostname",
            "ssl_sess_cache_per_vs": "ssl_sess_cache_per_vs",
            "tenant_ref": "tenant_ref",
            "transient_shared_memory_max": "transient_shared_memory_max",
            "udf_log_throttle": "udf_log_throttle",
            "upstream_connect_timeout": "upstream_connect_timeout",
            "upstream_connpool_enable": "upstream_connpool_enable",
            "upstream_read_timeout": "upstream_read_timeout",
            "upstream_send_timeout": "upstream_send_timeout",
            "use_dp_util_for_scaleout": "use_dp_util_for_scaleout",
            "use_hyperthreaded_cores": "use_hyperthreaded_cores",
            "use_legacy_netlink": "use_legacy_netlink",
            "use_objsync": "use_objsync",
            "use_standard_alb": "use_standard_alb",
            "user_agent_cache_config": "user_agent_cache_config",
            "user_defined_metric_age": "user_defined_metric_age",
            "vcenter_clusters": "vcenter_clusters",
            "vcenter_datastore_mode": "vcenter_datastore_mode",
            "vcenter_datastores": "vcenter_datastores",
            "vcenter_datastores_include": "vcenter_datastores_include",
            "vcenter_folder": "vcenter_folder",
            "vcenter_hosts": "vcenter_hosts",
            "vcenter_parking_vnic_pg": "vcenter_parking_vnic_pg",
            "vcenters": "vcenters",
            "vcpus_per_se": "vcpus_per_se",
            "vip_asg": "vip_asg",
            "vnic_dhcp_ip_check_interval": "vnic_dhcp_ip_check_interval",
            "vnic_dhcp_ip_max_retries": "vnic_dhcp_ip_max_retries",
            "vnic_ip_delete_interval": "vnic_ip_delete_interval",
            "vnic_probe_interval": "vnic_probe_interval",
            "vnic_rpc_retry_interval": "vnic_rpc_retry_interval",
            "vnicdb_cmd_history_size": "vnicdb_cmd_history_size",
            "vs_host_redundancy": "vs_host_redundancy",
            "vs_scalein_timeout": "vs_scalein_timeout",
            "vs_scalein_timeout_for_upgrade": "vs_scalein_timeout_for_upgrade",
            "vs_scaleout_timeout": "vs_scaleout_timeout",
            "vs_se_scaleout_additional_wait_time": "vs_se_scaleout_additional_wait_time",
            "vs_se_scaleout_ready_timeout": "vs_se_scaleout_ready_timeout",
            "vs_switchover_timeout": "vs_switchover_timeout",
            "vss_placement": "vss_placement",
            "vss_placement_enabled": "vss_placement_enabled",
            "waf_mempool": "waf_mempool",
            "waf_mempool_size": "waf_mempool_size",
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
                - path: nsx_alb.alb.service_engine_group.list
                - kwargs:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.service_engine_group.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe nsx_alb.alb.service_engine_group

    """

    result = dict(comment=[], ret=[], result=True)

    list = await hub.tool.nsx_alb.session.request(
        ctx,
        method="get",
        path="/serviceenginegroup",
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
    accelerated_networking: bool = None,
    active_standby: bool = None,
    aggressive_failure_detection: bool = None,
    algo: str = None,
    allow_burst: bool = None,
    app_cache_percent: int = None,
    app_cache_threshold: int = None,
    app_learning_memory_percent: int = None,
    archive_shm_limit: int = None,
    async_ssl: bool = None,
    async_ssl_threads: int = None,
    auto_rebalance: bool = None,
    auto_rebalance_capacity_per_se: List[int] = None,
    auto_rebalance_criteria: List[str] = None,
    auto_rebalance_interval: int = None,
    auto_redistribute_active_standby_load: bool = None,
    availability_zone_refs: List[str] = None,
    baremetal_dispatcher_handles_flows: bool = None,
    bgp_peer_monitor_failover_enabled: bool = None,
    bgp_state_update_interval: int = None,
    buffer_se: int = None,
    cloud_ref: str = None,
    compress_ip_rules_for_each_ns_subnet: bool = None,
    config_debugs_on_all_cores: bool = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    connection_memory_percentage: int = None,
    core_shm_app_cache: bool = None,
    core_shm_app_learning: bool = None,
    cpu_reserve: bool = None,
    cpu_socket_affinity: bool = None,
    custom_securitygroups_data: List[str] = None,
    custom_securitygroups_mgmt: List[str] = None,
    custom_tag: List[
        make_dataclass(
            "custom_tag", [("tag_key", str), ("tag_val", str, field(default=None))]
        )
    ] = None,
    data_network_id: str = None,
    datascript_timeout: int = None,
    deactivate_ipv6_discovery: bool = None,
    deactivate_kni_filtering_at_dispatcher: bool = None,
    dedicated_dispatcher_core: bool = None,
    description: str = None,
    disable_avi_securitygroups: bool = None,
    disable_csum_offloads: bool = None,
    disable_flow_probes: bool = None,
    disable_gro: bool = None,
    disable_se_memory_check: bool = None,
    disable_tso: bool = None,
    disk_per_se: int = None,
    distribute_load_active_standby: bool = None,
    distribute_queues: bool = None,
    distribute_vnics: bool = None,
    downstream_send_timeout: int = None,
    dp_aggressive_deq_interval_msec: int = None,
    dp_aggressive_enq_interval_msec: int = None,
    dp_aggressive_hb_frequency: int = None,
    dp_aggressive_hb_timeout_count: int = None,
    dp_deq_interval_msec: int = None,
    dp_enq_interval_msec: int = None,
    dp_hb_frequency: int = None,
    dp_hb_timeout_count: int = None,
    dpdk_gro_timeout_interval: int = None,
    enable_gratarp_permanent: bool = None,
    enable_hsm_log: bool = None,
    enable_hsm_priming: bool = None,
    enable_multi_lb: bool = None,
    enable_pcap_tx_ring: bool = None,
    ephemeral_portrange_end: int = None,
    ephemeral_portrange_start: int = None,
    extra_config_multiplier: float = None,
    extra_shared_config_memory: int = None,
    flow_table_new_syn_max_entries: int = None,
    free_list_size: int = None,
    gcp_config: make_dataclass(
        "gcp_config",
        [
            ("backend_data_vpc_network_name", str, field(default=None)),
            ("backend_data_vpc_project_id", str, field(default=None)),
            ("backend_data_vpc_subnet_name", str, field(default=None)),
        ],
    ) = None,
    gratarp_permanent_periodicity: int = None,
    grpc_channel_connect_timeout: int = None,
    ha_mode: str = None,
    handle_per_pkt_attack: bool = None,
    hardwaresecuritymodulegroup_ref: str = None,
    heap_minimum_config_memory: int = None,
    hm_on_standby: bool = None,
    host_attribute_key: str = None,
    host_attribute_value: str = None,
    host_gateway_monitor: bool = None,
    http_rum_console_log: bool = None,
    http_rum_min_content_length: int = None,
    hybrid_rss_mode: bool = None,
    hypervisor: str = None,
    ignore_docker_mac_change: bool = None,
    ignore_rtt_threshold: int = None,
    ingress_access_data: str = None,
    ingress_access_mgmt: str = None,
    instance_flavor: str = None,
    instance_flavor_info: make_dataclass(
        "instance_flavor_info",
        [
            ("id", str),
            ("name", str),
            ("cost", str, field(default=None)),
            ("disk_gb", int, field(default=None)),
            ("enhanced_nw", bool, field(default=None)),
            ("is_recommended", bool, field(default=None)),
            ("max_ip6s_per_nic", int, field(default=None)),
            ("max_ips_per_nic", int, field(default=None)),
            ("max_nics", int, field(default=None)),
            (
                "meta",
                List[make_dataclass("meta", [("key", str), ("value", str)])],
                field(default=None),
            ),
            ("public", bool, field(default=None)),
            ("ram_mb", int, field(default=None)),
            ("vcpus", int, field(default=None)),
        ],
    ) = None,
    iptables: List[
        make_dataclass(
            "iptables",
            [
                ("chain", str),
                ("table", str),
                (
                    "rules",
                    List[
                        make_dataclass(
                            "rules",
                            [
                                ("action", str),
                                (
                                    "dnat_ip",
                                    make_dataclass(
                                        "dnat_ip", [("addr", str), ("type", str)]
                                    ),
                                    field(default=None),
                                ),
                                (
                                    "dst_ip",
                                    make_dataclass(
                                        "dst_ip",
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
                                    "dst_port",
                                    make_dataclass(
                                        "dst_port", [("end", int), ("start", int)]
                                    ),
                                    field(default=None),
                                ),
                                ("input_interface", str, field(default=None)),
                                ("output_interface", str, field(default=None)),
                                ("proto", str, field(default=None)),
                                (
                                    "src_ip",
                                    make_dataclass(
                                        "src_ip",
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
                                    "src_port",
                                    make_dataclass(
                                        "src_port", [("end", int), ("start", int)]
                                    ),
                                    field(default=None),
                                ),
                                ("tag", str, field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
            ],
        )
    ] = None,
    kni_allowed_server_ports: List[
        make_dataclass(
            "kni_allowed_server_ports",
            [
                ("protocol", str),
                ("range", make_dataclass("range", [("end", int), ("start", int)])),
            ],
        )
    ] = None,
    l7_conns_per_core: int = None,
    l7_resvd_listen_conns_per_core: int = None,
    labels: List[
        make_dataclass("labels", [("key", str), ("value", str, field(default=None))])
    ] = None,
    lbaction_num_requests_to_dispatch: int = None,
    lbaction_rq_per_request_max_retries: int = None,
    least_load_core_selection: bool = None,
    license_tier: str = None,
    license_type: str = None,
    log_agent_compress_logs: bool = None,
    log_agent_debug_enabled: bool = None,
    log_agent_file_sz_appl: int = None,
    log_agent_file_sz_conn: int = None,
    log_agent_file_sz_debug: int = None,
    log_agent_file_sz_event: int = None,
    log_agent_log_storage_min_sz: int = None,
    log_agent_max_concurrent_rsync: int = None,
    log_agent_max_storage_excess_percent: int = None,
    log_agent_max_storage_ignore_percent: float = None,
    log_agent_min_storage_per_vs: int = None,
    log_agent_sleep_interval: int = None,
    log_agent_trace_enabled: bool = None,
    log_agent_unknown_vs_timer: int = None,
    log_disksz: int = None,
    log_malloc_failure: bool = None,
    log_message_max_file_list_size: int = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    max_concurrent_external_hm: int = None,
    max_cpu_usage: int = None,
    max_memory_per_mempool: int = None,
    max_num_se_dps: int = None,
    max_public_ips_per_lb: int = None,
    max_queues_per_vnic: int = None,
    max_rules_per_lb: int = None,
    max_scaleout_per_vs: int = None,
    max_se: int = None,
    max_skb_frags: int = None,
    max_vs_per_se: int = None,
    mem_reserve: bool = None,
    memory_for_config_update: int = None,
    memory_per_se: int = None,
    mgmt_network_ref: str = None,
    mgmt_subnet: make_dataclass(
        "mgmt_subnet",
        [
            ("ip_addr", make_dataclass("ip_addr", [("addr", str), ("type", str)])),
            ("mask", int),
        ],
    ) = None,
    min_cpu_usage: int = None,
    min_scaleout_per_vs: int = None,
    min_se: int = None,
    minimum_connection_memory: int = None,
    n_log_streaming_threads: int = None,
    netlink_poller_threads: int = None,
    netlink_sock_buf_size: int = None,
    ngx_free_connection_stack: bool = None,
    non_significant_log_throttle: int = None,
    ns_helper_deq_interval_msec: int = None,
    ntp_sync_fail_event: bool = None,
    ntp_sync_status_interval: int = None,
    num_dispatcher_cores: int = None,
    num_dispatcher_queues: int = None,
    num_flow_cores_sum_changes_to_ignore: int = None,
    objsync_config: make_dataclass(
        "objsync_config",
        [
            ("objsync_cpu_limit", int, field(default=None)),
            ("objsync_hub_elect_interval", int, field(default=None)),
            ("objsync_reconcile_interval", int, field(default=None)),
        ],
    ) = None,
    objsync_port: int = None,
    openstack_availability_zones: List[str] = None,
    openstack_mgmt_network_name: str = None,
    openstack_mgmt_network_uuid: str = None,
    os_reserved_memory: int = None,
    pcap_tx_mode: str = None,
    pcap_tx_ring_rd_balancing_factor: int = None,
    per_app: bool = None,
    per_vs_admission_control: bool = None,
    placement_mode: str = None,
    realtime_se_metrics: make_dataclass(
        "realtime_se_metrics",
        [("enabled", bool), ("duration", int, field(default=None))],
    ) = None,
    reboot_on_panic: bool = None,
    replay_vrf_routes_interval: int = None,
    resync_time_interval: int = None,
    sdb_flush_interval: int = None,
    sdb_pipeline_size: int = None,
    sdb_scan_count: int = None,
    se_bandwidth_type: str = None,
    se_delayed_flow_delete: bool = None,
    se_deprovision_delay: int = None,
    se_dos_profile: make_dataclass(
        "se_dos_profile",
        [
            ("thresh_period", int),
            (
                "thresh_info",
                List[
                    make_dataclass(
                        "thresh_info",
                        [("attack", str), ("max_value", int), ("min_value", int)],
                    )
                ],
                field(default=None),
            ),
        ],
    ) = None,
    se_dp_hm_drops: int = None,
    se_dp_if_state_poll_interval: int = None,
    se_dp_isolation: bool = None,
    se_dp_isolation_num_non_dp_cpus: int = None,
    se_dp_log_nf_enqueue_percent: int = None,
    se_dp_log_udf_enqueue_percent: int = None,
    se_dp_max_hb_version: int = None,
    se_dp_vnic_queue_stall_event_sleep: int = None,
    se_dp_vnic_queue_stall_threshold: int = None,
    se_dp_vnic_queue_stall_timeout: int = None,
    se_dp_vnic_restart_on_queue_stall_count: int = None,
    se_dp_vnic_stall_se_restart_window: int = None,
    se_dpdk_pmd: int = None,
    se_dump_core_on_assert: bool = None,
    se_emulated_cores: int = None,
    se_flow_probe_retries: int = None,
    se_flow_probe_retry_timer: int = None,
    se_group_analytics_policy: make_dataclass(
        "se_group_analytics_policy",
        [
            (
                "metrics_event_thresholds",
                List[
                    make_dataclass(
                        "metrics_event_thresholds",
                        [
                            ("metrics_event_threshold_type", str),
                            ("reset_threshold", float, field(default=None)),
                            ("watermark_thresholds", List[int], field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            )
        ],
    ) = None,
    se_hyperthreaded_mode: str = None,
    se_ip_encap_ipc: int = None,
    se_kni_burst_factor: int = None,
    se_l3_encap_ipc: int = None,
    se_log_buffer_app_blocking_dequeue: bool = None,
    se_log_buffer_conn_blocking_dequeue: bool = None,
    se_log_buffer_events_blocking_dequeue: bool = None,
    se_lro: bool = None,
    se_mp_ring_retry_count: int = None,
    se_mtu: int = None,
    se_name_prefix: str = None,
    se_packet_buffer_max: int = None,
    se_pcap_lookahead: bool = None,
    se_pcap_pkt_count: int = None,
    se_pcap_pkt_sz: int = None,
    se_pcap_qdisc_bypass: bool = None,
    se_pcap_reinit_frequency: int = None,
    se_pcap_reinit_threshold: int = None,
    se_probe_port: int = None,
    se_rl_prop: make_dataclass(
        "se_rl_prop",
        [
            ("msf_num_stages", int, field(default=None)),
            ("msf_stage_size", int, field(default=None)),
        ],
    ) = None,
    se_rum_sampling_nav_interval: int = None,
    se_rum_sampling_nav_percent: int = None,
    se_rum_sampling_res_interval: int = None,
    se_rum_sampling_res_percent: int = None,
    se_sb_dedicated_core: bool = None,
    se_sb_threads: int = None,
    se_thread_multiplier: int = None,
    se_time_tracker_props: make_dataclass(
        "se_time_tracker_props",
        [
            ("egress_audit_mode", str, field(default=None)),
            ("egress_threshold", int, field(default=None)),
            ("event_gen_window", int, field(default=None)),
            ("ingress_audit_mode", str, field(default=None)),
            ("ingress_threshold", int, field(default=None)),
        ],
    ) = None,
    se_tracert_port_range: make_dataclass(
        "se_tracert_port_range", [("end", int), ("start", int)]
    ) = None,
    se_tunnel_mode: int = None,
    se_tunnel_udp_port: int = None,
    se_tx_batch_size: int = None,
    se_txq_threshold: int = None,
    se_udp_encap_ipc: int = None,
    se_use_dpdk: int = None,
    se_vnic_tx_sw_queue_flush_frequency: int = None,
    se_vnic_tx_sw_queue_size: int = None,
    se_vs_hb_max_pkts_in_batch: int = None,
    se_vs_hb_max_vs_in_pkt: int = None,
    self_se_election: bool = None,
    send_se_ready_timeout: int = None,
    service_ip6_subnets: List[
        make_dataclass(
            "service_ip6_subnets",
            [
                ("ip_addr", make_dataclass("ip_addr", [("addr", str), ("type", str)])),
                ("mask", int),
            ],
        )
    ] = None,
    service_ip_subnets: List[
        make_dataclass(
            "service_ip_subnets",
            [
                ("ip_addr", make_dataclass("ip_addr", [("addr", str), ("type", str)])),
                ("mask", int),
            ],
        )
    ] = None,
    shm_minimum_config_memory: int = None,
    significant_log_throttle: int = None,
    ssl_preprocess_sni_hostname: bool = None,
    ssl_sess_cache_per_vs: int = None,
    tenant_ref: str = None,
    transient_shared_memory_max: int = None,
    udf_log_throttle: int = None,
    upstream_connect_timeout: int = None,
    upstream_connpool_enable: bool = None,
    upstream_read_timeout: int = None,
    upstream_send_timeout: int = None,
    use_dp_util_for_scaleout: bool = None,
    use_hyperthreaded_cores: bool = None,
    use_legacy_netlink: bool = None,
    use_objsync: bool = None,
    use_standard_alb: bool = None,
    user_agent_cache_config: make_dataclass(
        "user_agent_cache_config",
        [
            ("batch_size", int, field(default=None)),
            ("controller_cache_size", int, field(default=None)),
            ("max_age", int, field(default=None)),
            ("max_last_hit_time", int, field(default=None)),
            ("max_upstream_queries", int, field(default=None)),
            ("max_wait_time", int, field(default=None)),
            ("num_entries_upstream_update", int, field(default=None)),
            ("percent_reserved_for_bad_bots", int, field(default=None)),
            ("percent_reserved_for_browsers", int, field(default=None)),
            ("percent_reserved_for_good_bots", int, field(default=None)),
            ("percent_reserved_for_outstanding", int, field(default=None)),
            ("se_cache_size", int, field(default=None)),
            ("upstream_update_interval", int, field(default=None)),
        ],
    ) = None,
    user_defined_metric_age: int = None,
    vcenter_clusters: make_dataclass(
        "vcenter_clusters",
        [
            ("cluster_refs", List[str], field(default=None)),
            ("include", bool, field(default=None)),
        ],
    ) = None,
    vcenter_datastore_mode: str = None,
    vcenter_datastores: List[
        make_dataclass(
            "vcenter_datastores",
            [
                ("datastore_name", str, field(default=None)),
                ("managed_object_id", str, field(default=None)),
            ],
        )
    ] = None,
    vcenter_datastores_include: bool = None,
    vcenter_folder: str = None,
    vcenter_hosts: make_dataclass(
        "vcenter_hosts",
        [
            ("host_refs", List[str], field(default=None)),
            ("include", bool, field(default=None)),
        ],
    ) = None,
    vcenter_parking_vnic_pg: str = None,
    vcenters: List[
        make_dataclass(
            "vcenters",
            [
                ("vcenter_ref", str),
                (
                    "clusters",
                    List[
                        make_dataclass(
                            "clusters",
                            [
                                ("cluster_id", str, field(default=None)),
                                ("override_vsphere_ha", bool, field(default=None)),
                                ("vmg_name", str, field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                (
                    "nsxt_clusters",
                    make_dataclass(
                        "nsxt_clusters",
                        [
                            ("cluster_ids", List[str], field(default=None)),
                            ("include", bool, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "nsxt_datastores",
                    make_dataclass(
                        "nsxt_datastores",
                        [
                            ("ds_ids", List[str], field(default=None)),
                            ("include", bool, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "nsxt_hosts",
                    make_dataclass(
                        "nsxt_hosts",
                        [
                            ("host_ids", List[str], field(default=None)),
                            ("include", bool, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                ("vcenter_folder", str, field(default=None)),
            ],
        )
    ] = None,
    vcpus_per_se: int = None,
    vip_asg: make_dataclass(
        "vip_asg",
        [
            (
                "configuration",
                make_dataclass(
                    "configuration",
                    [
                        (
                            "zones",
                            List[
                                make_dataclass(
                                    "zones",
                                    [
                                        ("availability_zone", str, field(default=None)),
                                        ("fip_capable", bool, field(default=None)),
                                        ("subnet_uuid", str, field(default=None)),
                                    ],
                                )
                            ],
                            field(default=None),
                        )
                    ],
                ),
                field(default=None),
            ),
            (
                "policy",
                make_dataclass(
                    "policy",
                    [
                        ("dns_cooldown", int, field(default=None)),
                        ("max_size", int, field(default=None)),
                        ("min_size", int, field(default=None)),
                        ("suspend", bool, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    vnic_dhcp_ip_check_interval: int = None,
    vnic_dhcp_ip_max_retries: int = None,
    vnic_ip_delete_interval: int = None,
    vnic_probe_interval: int = None,
    vnic_rpc_retry_interval: int = None,
    vnicdb_cmd_history_size: int = None,
    vs_host_redundancy: bool = None,
    vs_scalein_timeout: int = None,
    vs_scalein_timeout_for_upgrade: int = None,
    vs_scaleout_timeout: int = None,
    vs_se_scaleout_additional_wait_time: int = None,
    vs_se_scaleout_ready_timeout: int = None,
    vs_switchover_timeout: int = None,
    vss_placement: make_dataclass(
        "vss_placement",
        [
            ("core_nonaffinity", int, field(default=None)),
            ("num_subcores", int, field(default=None)),
        ],
    ) = None,
    vss_placement_enabled: bool = None,
    waf_mempool: bool = None,
    waf_mempool_size: int = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:

        resource_id(str, Optional):
            Alb.service_engine_group unique ID. Defaults to None.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

        accelerated_networking(bool, Optional):
            Enable accelerated networking option for Azure SE. Accelerated networking enables single root I/O virtualization (SR-IOV) to a SE VM. This improves networking performance. Field introduced in 17.2.14,18.1.5,18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        active_standby(bool, Optional):
            Service Engines in active/standby mode for HA failover. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        aggressive_failure_detection(bool, Optional):
            Enable aggressive failover configuration for ha. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        algo(str, Optional):
            In compact placement, Virtual Services are placed on existing SEs until max_vs_per_se limit is reached. Enum options - PLACEMENT_ALGO_PACKED, PLACEMENT_ALGO_DISTRIBUTED. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        allow_burst(bool, Optional):
            Allow SEs to be created using burst license. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        app_cache_percent(int, Optional):
            A percent value of total SE memory reserved for applicationcaching. This is an SE bootup property and requires SE restart.Requires SE Reboot. Allowed values are 0 - 100. Special values are 0- disable. Field introduced in 18.2.3. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Special default for Essentials edition is 0, Basic edition is 0, Enterprise is 10. Defaults to None.

        app_cache_threshold(int, Optional):
            The max memory that can be allocated for the app cache. This value will act as an upper bound on the cache size specified in app_cache_percent. Special values are 0- disable. Field introduced in 20.1.1. Unit is GB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        app_learning_memory_percent(int, Optional):
            A percent value of total SE memory reserved for Application learning. This is an SE bootup property and requires SE restart. Allowed values are 0 - 10. Field introduced in 18.2.3. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        archive_shm_limit(int, Optional):
            Amount of SE memory in GB until which shared memory is collected in core archive. Field introduced in 17.1.3. Unit is GB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        async_ssl(bool, Optional):
            SSL handshakes will be handled by dedicated SSL Threads.Requires SE Reboot. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        async_ssl_threads(int, Optional):
            Number of Async SSL threads per se_dp.Requires SE Reboot. Allowed values are 1-16. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        auto_rebalance(bool, Optional):
            If set, Virtual Services will be automatically migrated when load on an SE is less than minimum or more than maximum thresholds. Only Alerts are generated when the auto_rebalance is not set. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        auto_rebalance_capacity_per_se(List[int], Optional):
            Capacities of SE for auto rebalance for each criteria. Field introduced in 17.2.4. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        auto_rebalance_criteria(List[str], Optional):
            Set of criteria for SE Auto Rebalance. Enum options - SE_AUTO_REBALANCE_CPU, SE_AUTO_REBALANCE_PPS, SE_AUTO_REBALANCE_MBPS, SE_AUTO_REBALANCE_OPEN_CONNS, SE_AUTO_REBALANCE_CPS. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        auto_rebalance_interval(int, Optional):
            Frequency of rebalance, if 'Auto rebalance' is enabled. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        auto_redistribute_active_standby_load(bool, Optional):
            Redistribution of virtual services from the takeover SE to the replacement SE can cause momentary traffic loss. If the auto-redistribute load option is left in its default off state, any desired rebalancing requires calls to REST API. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        availability_zone_refs(List[str], Optional):
            Availability zones for Virtual Service High Availability. It is a reference to an object of type AvailabilityZone. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        baremetal_dispatcher_handles_flows(bool, Optional):
            Control if dispatcher core also handles TCP flows in baremetal SE. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        bgp_peer_monitor_failover_enabled(bool, Optional):
            Enable BGP peer monitoring based failover. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        bgp_state_update_interval(int, Optional):
            BGP peer state update interval. Allowed values are 5-100. Field introduced in 17.2.14,18.1.5,18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        buffer_se(int, Optional):
            Excess Service Engine capacity provisioned for HA failover. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        cloud_ref(str, Optional):
             It is a reference to an object of type Cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        compress_ip_rules_for_each_ns_subnet(bool, Optional):
            Compress IP rules into a single subnet based IP rule for each north-south IPAM subnet configured in PCAP mode in OpenShift/Kubernetes node. Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        config_debugs_on_all_cores(bool, Optional):
            Enable config debugs on all cores of SE. Field introduced in 17.2.13,18.1.5,18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        connection_memory_percentage(int, Optional):
            Percentage of memory for connection state. This will come at the expense of memory used for HTTP in-memory cache. Allowed values are 10-90. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        core_shm_app_cache(bool, Optional):
            Include shared memory for app cache in core file.Requires SE Reboot. Field introduced in 18.2.8, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        core_shm_app_learning(bool, Optional):
            Include shared memory for app learning in core file.Requires SE Reboot. Field introduced in 18.2.8, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        cpu_reserve(bool, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        cpu_socket_affinity(bool, Optional):
            Allocate all the CPU cores for the Service Engine Virtual Machines  on the same CPU socket. Applicable only for vCenter Cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        custom_securitygroups_data(List[str], Optional):
            Custom Security Groups to be associated with data vNics for SE instances in OpenStack and AWS Clouds. Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        custom_securitygroups_mgmt(List[str], Optional):
            Custom Security Groups to be associated with management vNic for SE instances in OpenStack and AWS Clouds. Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        custom_tag(List[dict[str, Any]], Optional):
            Custom tag will be used to create the tags for SE instance in AWS. Note this is not the same as the prefix for SE name. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * tag_key (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * tag_val (str, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        data_network_id(str, Optional):
            Subnet used to spin up the data nic for Service Engines, used only for Azure cloud. Overrides the cloud level setting for Service Engine subnet. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        datascript_timeout(int, Optional):
            Number of instructions before datascript times out. Allowed values are 0-100000000. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        deactivate_ipv6_discovery(bool, Optional):
            If activated, IPv6 address and route discovery are deactivated.Requires SE reboot. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        deactivate_kni_filtering_at_dispatcher(bool, Optional):
            Deactivate filtering of packets to KNI interface. To be used under surveillance of Avi Support. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dedicated_dispatcher_core(bool, Optional):
            Dedicate the core that handles packet receive/transmit from the network to just the dispatching function. Don't use it for TCP/IP and SSL functions. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        description(str, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disable_avi_securitygroups(bool, Optional):
            By default, Avi creates and manages security groups along with custom sg provided by user. Set this to True to disallow Avi to create and manage new security groups. Avi will only make use of custom security groups provided by user. This option is supported for AWS and OpenStack cloud types. Field introduced in 17.2.13,18.1.4,18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disable_csum_offloads(bool, Optional):
            Stop using TCP/UDP and IP checksum offload features of NICs. Field introduced in 17.1.14, 17.2.5, 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disable_flow_probes(bool, Optional):
            Disable Flow Probes for Scaled out VS'es. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        disable_gro(bool, Optional):
            Disable Generic Receive Offload (GRO) in DPDK poll-mode driver packet receive path.  GRO is on by default on NICs that do not support LRO (Large Receive Offload) or do not gain performance boost from LRO. Field introduced in 17.2.5, 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disable_se_memory_check(bool, Optional):
            If set, disable the config memory check done in service engine. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disable_tso(bool, Optional):
            Disable TCP Segmentation Offload (TSO) in DPDK poll-mode driver packet transmit path. TSO is on by default on NICs that support it. Field introduced in 17.2.5, 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disk_per_se(int, Optional):
            Amount of disk space for each of the Service Engine virtual machines. Unit is GB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        distribute_load_active_standby(bool, Optional):
            Use both the active and standby Service Engines for Virtual Service placement in the legacy active standby HA mode. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        distribute_queues(bool, Optional):
            Distributes queue ownership among cores so multiple cores handle dispatcher duties. Requires SE Reboot. Deprecated from 18.2.8, instead use max_queues_per_vnic. Field introduced in 17.2.8. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        distribute_vnics(bool, Optional):
            Distributes vnic ownership among cores so multiple cores handle dispatcher duties.Requires SE Reboot. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        downstream_send_timeout(int, Optional):
            Timeout for downstream to become writable. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_aggressive_deq_interval_msec(int, Optional):
            Dequeue interval for receive queue from se_dp in aggressive mode. Allowed values are 1-1000. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_aggressive_enq_interval_msec(int, Optional):
            Enqueue interval for request queue to se_dp in aggressive mode. Allowed values are 1-1000. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_aggressive_hb_frequency(int, Optional):
            Frequency of SE - SE HB messages when aggressive failure mode detection is enabled. Field introduced in 20.1.3. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_aggressive_hb_timeout_count(int, Optional):
            Consecutive HB failures after which failure is reported to controller,when aggressive failure mode detection is enabled. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_deq_interval_msec(int, Optional):
            Dequeue interval for receive queue from se_dp. Allowed values are 1-1000. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_enq_interval_msec(int, Optional):
            Enqueue interval for request queue to se_dp. Allowed values are 1-1000. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_hb_frequency(int, Optional):
            Frequency of SE - SE HB messages when aggressive failure mode detection is not enabled. Field introduced in 20.1.3. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_hb_timeout_count(int, Optional):
            Consecutive HB failures after which failure is reported to controller, when aggressive failure mode detection is not enabled. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dpdk_gro_timeout_interval(int, Optional):
            The timeout for GRO coalescing interval. 0 indicates non-timer based GRO. Allowed values are 0-900. Field introduced in 22.1.1. Unit is MICROSECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        enable_gratarp_permanent(bool, Optional):
            Enable GratArp for VIP_IP. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        enable_hsm_log(bool, Optional):
            Enable HSM luna engine logs. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        enable_hsm_priming(bool, Optional):
            (This is a beta feature). Enable HSM key priming. If enabled, key handles on the hsm will be synced to SE before processing client connections. Field introduced in 17.2.7, 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        enable_multi_lb(bool, Optional):
            Applicable only for Azure cloud with Basic SKU LB. If set, additional Azure LBs will be automatically created if resources in existing LB are exhausted. Field introduced in 17.2.10, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        enable_pcap_tx_ring(bool, Optional):
            Enable TX ring support in pcap mode of operation. TSO feature is not supported with TX Ring enabled. Deprecated from 18.2.8, instead use pcap_tx_mode. Requires SE Reboot. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ephemeral_portrange_end(int, Optional):
            End local ephemeral port number for outbound connections. Field introduced in 17.2.13, 18.1.5, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ephemeral_portrange_start(int, Optional):
            Start local ephemeral port number for outbound connections. Field introduced in 17.2.13, 18.1.5, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        extra_config_multiplier(float, Optional):
            Multiplier for extra config to support large VS/Pool config. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        extra_shared_config_memory(int, Optional):
            Extra config memory to support large Geo DB configuration. Field introduced in 17.1.1. Unit is MB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        flow_table_new_syn_max_entries(int, Optional):
            Maximum number of flow table entries that have not completed TCP three-way handshake yet. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        free_list_size(int, Optional):
            Number of entries in the free list. Field introduced in 17.2.10, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        gcp_config(dict[str, Any], Optional):
            gcp_config. Defaults to None.

            * backend_data_vpc_network_name (str, Optional):
                Service Engine Backend Data Network Name, used only for GCP cloud.Overrides the cloud level setting for Backend Data Network in GCP Two Arm Mode. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * backend_data_vpc_project_id (str, Optional):
                Project ID of the Service Engine Backend Data Network. By default, Service Engine Project ID will be used. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * backend_data_vpc_subnet_name (str, Optional):
                Service Engine Backend Data Subnet Name, used only for GCP cloud.Overrides the cloud level setting for Backend Data Subnet in GCP Two Arm Mode. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        gratarp_permanent_periodicity(int, Optional):
            GratArp periodicity for VIP-IP. Allowed values are 5-30. Field introduced in 18.2.3. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        grpc_channel_connect_timeout(int, Optional):
            Timeout in seconds that SE waits for a grpc channel to connect to server, before it retries. Allowed values are 5-45. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ha_mode(str, Optional):
            High Availability mode for all the Virtual Services using this Service Engine group. Enum options - HA_MODE_SHARED_PAIR, HA_MODE_SHARED, HA_MODE_LEGACY_ACTIVE_STANDBY. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- HA_MODE_LEGACY_ACTIVE_STANDBY), Basic edition(Allowed values- HA_MODE_LEGACY_ACTIVE_STANDBY), Enterprise with Cloud Services edition. Special default for Essentials edition is HA_MODE_LEGACY_ACTIVE_STANDBY, Basic edition is HA_MODE_LEGACY_ACTIVE_STANDBY, Enterprise is HA_MODE_SHARED. Defaults to None.

        handle_per_pkt_attack(bool, Optional):
            Configuration to handle per packet attack handling.For example, DNS Reflection Attack is a type of attack where a response packet is sent to the DNS VS.This configuration tells if such packets should be dropped without further processing. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        hardwaresecuritymodulegroup_ref(str, Optional):
             It is a reference to an object of type HardwareSecurityModuleGroup. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        heap_minimum_config_memory(int, Optional):
            Minimum required heap memory to apply any configuration. Allowed values are 0-100. Field introduced in 18.1.2. Unit is MB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        hm_on_standby(bool, Optional):
            Enable active health monitoring from the standby SE for all placed virtual services. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Special default for Essentials edition is false, Basic edition is false, Enterprise is True. Defaults to None.

        host_attribute_key(str, Optional):
            Key of a (Key, Value) pair identifying a label for a set of Nodes usually in Container Clouds. Needs to be specified together with host_attribute_value. SEs can be configured differently including HA modes across different SE Groups. May also be used for isolation between different classes of VirtualServices. VirtualServices' SE Group may be specified via annotations/labels. A OpenShift/Kubernetes namespace maybe annotated with a matching SE Group label as openshift.io/node-selector  apptype=prod. When multiple SE Groups are used in a Cloud with host attributes specified,just a single SE Group can exist as a match-all SE Group without a host_attribute_key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        host_attribute_value(str, Optional):
            Value of a (Key, Value) pair identifying a label for a set of Nodes usually in Container Clouds. Needs to be specified together with host_attribute_key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        host_gateway_monitor(bool, Optional):
            Enable the host gateway monitor when service engine is deployed as docker container. Disabled by default. Field introduced in 17.2.4. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        http_rum_console_log(bool, Optional):
            Enable Javascript console logs on the client browser when collecting client insights. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        http_rum_min_content_length(int, Optional):
            Minimum response size content length to sample for client insights. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 64), Basic edition(Allowed values- 64), Enterprise with Cloud Services edition. Defaults to None.

        hybrid_rss_mode(bool, Optional):
            Toggles SE hybrid only mode of operation in DPDK mode with RSS configured;where-in each SE datapath instance operates as an independent standalonehybrid instance performing both dispatcher and proxy function. Requires reboot. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        hypervisor(str, Optional):
            Override default hypervisor. Enum options - DEFAULT, VMWARE_ESX, KVM, VMWARE_VSAN, XEN. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ignore_docker_mac_change(bool, Optional):
            Ignore docker mac change. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ignore_rtt_threshold(int, Optional):
            Ignore RTT samples if it is above threshold. Field introduced in 17.1.6,17.2.2. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ingress_access_data(str, Optional):
            Program SE security group ingress rules to allow VIP data access from remote CIDR type. Enum options - SG_INGRESS_ACCESS_NONE, SG_INGRESS_ACCESS_ALL, SG_INGRESS_ACCESS_VPC. Field introduced in 17.1.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ingress_access_mgmt(str, Optional):
            Program SE security group ingress rules to allow SSH/ICMP management access from remote CIDR type. Enum options - SG_INGRESS_ACCESS_NONE, SG_INGRESS_ACCESS_ALL, SG_INGRESS_ACCESS_VPC. Field introduced in 17.1.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        instance_flavor(str, Optional):
            Instance/Flavor name for SE instance. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        instance_flavor_info(dict[str, Any], Optional):
            instance_flavor_info. Defaults to None.

            * cost (str, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disk_gb (int, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enhanced_nw (bool, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * id (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * is_recommended (bool, Optional):
                If a vm flavor is recommended for requested se_usage_type.Set to True if the chosen VM flavor is recommended for requested se_usage_type.Else set to False. Field introduced in 18.1.4, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_ip6s_per_nic (int, Optional):
                Maximum number of IPv6 addresses that can be configured per NIC. Field introduced in 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_ips_per_nic (int, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_nics (int, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * meta (List[dict[str, Any]], Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * key (str):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * value (str):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * name (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * public (bool, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ram_mb (int, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vcpus (int, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        iptables(List[dict[str, Any]], Optional):
            Iptable Rules. Maximum of 128 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * chain (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * rules (List[dict[str, Any]], Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * action (str):
                     Enum options - ACCEPT, DROP, REJECT, DNAT, MASQUERADE. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * dnat_ip (dict[str, Any], Optional):
                    dnat_ip

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * dst_ip (dict[str, Any], Optional):
                    dst_ip

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * dst_port (dict[str, Any], Optional):
                    dst_port

                    * end (int):
                        TCP/UDP port range end (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * start (int):
                        TCP/UDP port range start (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * input_interface (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * output_interface (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * proto (str, Optional):
                     Enum options - PROTO_TCP, PROTO_UDP, PROTO_ICMP, PROTO_ALL. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * src_ip (dict[str, Any], Optional):
                    src_ip

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * src_port (dict[str, Any], Optional):
                    src_port

                    * end (int):
                        TCP/UDP port range end (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * start (int):
                        TCP/UDP port range start (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * tag (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * table (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        kni_allowed_server_ports(List[dict[str, Any]], Optional):
            Port ranges for any servers running in inband LinuxServer clouds. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * protocol (str):
                Protocol associated with port range. Enum options - KNI_PROTO_TCP, KNI_PROTO_UDP. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * range (dict[str, Any]):
                range

                * end (int):
                    TCP/UDP port range end (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * start (int):
                    TCP/UDP port range start (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        l7_conns_per_core(int, Optional):
            Number of L7 connections that can be cached per core. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        l7_resvd_listen_conns_per_core(int, Optional):
            Number of reserved L7 listener connections per core. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        labels(List[dict[str, Any]], Optional):
            Labels associated with this SE group. Field introduced in 20.1.1. Maximum of 1 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * value (str, Optional):
                Value. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        lbaction_num_requests_to_dispatch(int, Optional):
            Number of requests to dispatch from the request. queue at a regular interval. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        lbaction_rq_per_request_max_retries(int, Optional):
            Maximum retries per request in the request queue. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        least_load_core_selection(bool, Optional):
            Select core with least load for new flow. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        license_tier(str, Optional):
            Specifies the license tier which would be used. This field by default inherits the value from cloud. Enum options - ENTERPRISE_16, ENTERPRISE, ENTERPRISE_18, BASIC, ESSENTIALS, ENTERPRISE_WITH_CLOUD_SERVICES. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        license_type(str, Optional):
            If no license type is specified then default license enforcement for the cloud type is chosen. Enum options - LIC_BACKEND_SERVERS, LIC_SOCKETS, LIC_CORES, LIC_HOSTS, LIC_SE_BANDWIDTH, LIC_METERED_SE_BANDWIDTH. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_compress_logs(bool, Optional):
            Flag to indicate if log files are compressed upon full on the Service Engine. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_debug_enabled(bool, Optional):
            Enable debug logs by default on Service Engine. This includes all other debugging logs. Debug logs can also be explcitly enabled from the CLI shell. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_file_sz_appl(int, Optional):
            Maximum application log file size before rollover. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_file_sz_conn(int, Optional):
            Maximum connection log file size before rollover. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_file_sz_debug(int, Optional):
            Maximum debug log file size before rollover. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_file_sz_event(int, Optional):
            Maximum event log file size before rollover. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_log_storage_min_sz(int, Optional):
            Minimum storage allocated for logs irrespective of memory and cores. Field introduced in 21.1.1. Unit is MB. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_max_concurrent_rsync(int, Optional):
            Maximum concurrent rsync requests initiated from log-agent to the Controller. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_max_storage_excess_percent(int, Optional):
            Excess percentage threshold of disk size to trigger cleanup of logs on the Service Engine. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_max_storage_ignore_percent(float, Optional):
            Maximum storage on the disk not allocated for logs on the Service Engine. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_min_storage_per_vs(int, Optional):
            Minimum storage allocated to any given VirtualService on the Service Engine. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_sleep_interval(int, Optional):
            Internal timer to stall log-agent and prevent it from hogging CPU cycles on the Service Engine. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_trace_enabled(bool, Optional):
            Enable trace logs by default on Service Engine. Configuration operations are logged along with other important logs by Service Engine. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_unknown_vs_timer(int, Optional):
            Timeout to purge unknown Virtual Service logs from the Service Engine. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_disksz(int, Optional):
            Maximum disk capacity (in MB) to be allocated to an SE. This is exclusively used for debug and log data. Unit is MB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        log_malloc_failure(bool, Optional):
            SE will log memory allocation related failure to the se_trace file, wherever available. Field introduced in 20.1.2. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- true), Basic edition(Allowed values- true), Enterprise with Cloud Services edition. Defaults to None.

        log_message_max_file_list_size(int, Optional):
            Maximum number of file names in a log message. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.7. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        max_concurrent_external_hm(int, Optional):
            Maximum number of external health monitors that can run concurrently in a service engine. This helps control the CPU and memory use by external health monitors. Special values are 0- Value will be internally calculated based on cpu and memory. Field introduced in 18.2.7. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_cpu_usage(int, Optional):
            When CPU usage on an SE exceeds this threshold, Virtual Services hosted on this SE may be rebalanced to other SEs to reduce load. A new SE may be created as part of this process. Allowed values are 40-90. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_memory_per_mempool(int, Optional):
            Max bytes that can be allocated in a single mempool. Field introduced in 18.1.5. Unit is MB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_num_se_dps(int, Optional):
            Configures the maximum number of se_dp processes that handles traffic. If not configured, defaults to the number of CPUs on the SE. If decreased, it will only take effect after SE reboot. Allowed values are 1-128. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Defaults to None.

        max_public_ips_per_lb(int, Optional):
            Applicable to Azure platform only. Maximum number of public IPs per Azure LB. . Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_queues_per_vnic(int, Optional):
            Maximum number of queues per vnic Setting to '0' utilises all queues that are distributed across dispatcher cores. Allowed values are 0,1,2,4,8,16. Field introduced in 18.2.7, 20.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 1), Basic edition(Allowed values- 1), Enterprise with Cloud Services edition. Defaults to None.

        max_rules_per_lb(int, Optional):
            Applicable to Azure platform only. Maximum number of rules per Azure LB. . Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_scaleout_per_vs(int, Optional):
            Maximum number of active Service Engines for the Virtual Service. Allowed values are 1-64. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_se(int, Optional):
            Maximum number of Services Engines in this group. Allowed values are 0-1000. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_skb_frags(int, Optional):
            Maximum of number of 4 KB pages allocated to the Linux kernel GRO subsystem for packet coalescing. This parameter is limited to supported kernels only. Requires SE Reboot. Allowed values are 1-17. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        max_vs_per_se(int, Optional):
            Maximum number of Virtual Services that can be placed on a single Service Engine. Allowed values are 1-1000. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        mem_reserve(bool, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        memory_for_config_update(int, Optional):
            Indicates the percent of memory reserved for config updates. Allowed values are 0-100. Field introduced in 18.1.2. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        memory_per_se(int, Optional):
            Amount of memory for each of the Service Engine virtual machines. Changes to this setting do not affect existing SEs. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        mgmt_network_ref(str, Optional):
            Management network to use for Avi Service Engines. It is a reference to an object of type Network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        mgmt_subnet(dict[str, Any], Optional):
            mgmt_subnet. Defaults to None.

            * ip_addr (dict[str, Any]):
                ip_addr

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mask (int):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        min_cpu_usage(int, Optional):
            When CPU usage on an SE falls below the minimum threshold, Virtual Services hosted on the SE may be consolidated onto other underutilized SEs. After consolidation, unused Service Engines may then be eligible for deletion. . Allowed values are 20-60. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        min_scaleout_per_vs(int, Optional):
            Minimum number of active Service Engines for the Virtual Service. Allowed values are 1-64. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        min_se(int, Optional):
            Minimum number of Services Engines in this group (relevant for SE AutoRebalance only). Allowed values are 0-1000. Field introduced in 17.2.13,18.1.3,18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        minimum_connection_memory(int, Optional):
            Indicates the percent of memory reserved for connections. Allowed values are 0-100. Field introduced in 18.1.2. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        n_log_streaming_threads(int, Optional):
            Number of threads to use for log streaming. Allowed values are 1-100. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        netlink_poller_threads(int, Optional):
            Number of threads to poll for netlink messages excluding the thread for default namespace. Requires SE Reboot. Allowed values are 1-32. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        netlink_sock_buf_size(int, Optional):
            Socket buffer size for the netlink sockets. Requires SE Reboot. Allowed values are 1-128. Field introduced in 21.1.1. Unit is MEGA_BYTES. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ngx_free_connection_stack(bool, Optional):
            Free the connection stack. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        non_significant_log_throttle(int, Optional):
            This setting limits the number of non-significant logs generated per second per core on this SE. Default is 100 logs per second. Set it to zero (0) to deactivate throttling. Field introduced in 17.1.3. Unit is PER_SECOND. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ns_helper_deq_interval_msec(int, Optional):
            Dequeue interval for receive queue from NS HELPER. Allowed values are 1-1000. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ntp_sync_fail_event(bool, Optional):
            Toggle SE NTP synchronization failure events generation. Disabled by default. Field introduced in 22.1.2. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ntp_sync_status_interval(int, Optional):
            Configures the interval at which SE synchronization status with NTP server(s) is verified. A value of zero disables SE NTP synchronization status validation. Allowed values are 120-900. Special values are 0- disable. Field introduced in 22.1.2. Unit is SEC. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        num_dispatcher_cores(int, Optional):
            Number of dispatcher cores (0,1,2,4,8 or 16). If set to 0, then number of dispatcher cores is deduced automatically.Requires SE Reboot. Allowed values are 0,1,2,4,8,16. Field introduced in 17.2.12, 18.1.3, 18.2.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Defaults to None.

        num_dispatcher_queues(int, Optional):
            Number of queues to each dispatcher. Allowed values are 1-2. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        num_flow_cores_sum_changes_to_ignore(int, Optional):
            Number of changes in num flow cores sum to ignore. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        objsync_config(dict[str, Any], Optional):
            objsync_config. Defaults to None.

            * objsync_cpu_limit (int, Optional):
                SE CPU limit for InterSE Object Distribution. Allowed values are 15-80. Field introduced in 20.1.3. Unit is PERCENT. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * objsync_hub_elect_interval (int, Optional):
                Hub election interval for InterSE Object Distribution. Allowed values are 30-300. Field introduced in 20.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * objsync_reconcile_interval (int, Optional):
                Reconcile interval for InterSE Object Distribution. Allowed values are 1-120. Field introduced in 20.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        objsync_port(int, Optional):
            TCP port on SE management interface for InterSE Object Distribution. Supported only for externally managed security groups. Not supported on full access deployments. Requires SE reboot. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        openstack_availability_zones(List[str], Optional):
             Field introduced in 17.1.1. Maximum of 5 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        openstack_mgmt_network_name(str, Optional):
            Avi Management network name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        openstack_mgmt_network_uuid(str, Optional):
            Management network UUID. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        os_reserved_memory(int, Optional):
            Amount of extra memory to be reserved for use by the Operating System on a Service Engine. Unit is MB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        pcap_tx_mode(str, Optional):
            Determines the PCAP transmit mode of operation. Requires SE Reboot. Enum options - PCAP_TX_AUTO, PCAP_TX_SOCKET, PCAP_TX_RING. Field introduced in 18.2.8, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        pcap_tx_ring_rd_balancing_factor(int, Optional):
            In PCAP mode, reserve a configured portion of TX ring resources for itself and the remaining portion for the RX ring to achieve better balance in terms of queue depth. Requires SE Reboot. Allowed values are 10-100. Field introduced in 20.1.3. Unit is PERCENT. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        per_app(bool, Optional):
            Per-app SE mode is designed for deploying dedicated load balancers per app (VS). In this mode, each SE is limited to a max of 2 VSs. vCPUs in per-app SEs count towards licensing usage at 25% rate. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        per_vs_admission_control(bool, Optional):
            Enable/Disable per VS level admission control.Enabling this feature will cause the connection and packet throttling on a particular VS that has high packet buffer consumption. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        placement_mode(str, Optional):
            If placement mode is 'Auto', Virtual Services are automatically placed on Service Engines. Enum options - PLACEMENT_MODE_AUTO. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        realtime_se_metrics(dict[str, Any], Optional):
            realtime_se_metrics. Defaults to None.

            * duration (int, Optional):
                Real time metrics collection duration in minutes. 0 for infinite. Special values are 0 - infinite. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enabled (bool):
                Enables real time metrics collection.  When deactivated, 6 hour view is the most granular the system will track. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        reboot_on_panic(bool, Optional):
            Reboot the VM or host on kernel panic. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        replay_vrf_routes_interval(int, Optional):
            Routes in VRF are replayed at the specified interval. This should be increased if there are large number of routes. Allowed values are 0-3000. Field introduced in 22.1.3. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        resync_time_interval(int, Optional):
            Time interval to re-sync SE's time with wall clock time. Allowed values are 8-600000. Field introduced in 20.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        sdb_flush_interval(int, Optional):
            SDB pipeline flush interval. Allowed values are 1-10000. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        sdb_pipeline_size(int, Optional):
            SDB pipeline size. Allowed values are 1-10000. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        sdb_scan_count(int, Optional):
            SDB scan count. Allowed values are 1-1000. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_bandwidth_type(str, Optional):
            Select the SE bandwidth for the bandwidth license. Enum options - SE_BANDWIDTH_UNLIMITED, SE_BANDWIDTH_25M, SE_BANDWIDTH_200M, SE_BANDWIDTH_1000M, SE_BANDWIDTH_10000M. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- SE_BANDWIDTH_UNLIMITED), Basic edition(Allowed values- SE_BANDWIDTH_UNLIMITED), Enterprise with Cloud Services edition. Defaults to None.

        se_delayed_flow_delete(bool, Optional):
            Delay the cleanup of flowtable entry. To be used under surveillance of Avi Support. Field introduced in 20.1.2. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- true), Basic edition(Allowed values- true), Enterprise with Cloud Services edition. Defaults to None.

        se_deprovision_delay(int, Optional):
            Duration to preserve unused Service Engine virtual machines before deleting them. If traffic to a Virtual Service were to spike up abruptly, this SE would still be available to be utilized again rather than creating a new SE. If this value is set to 0, Controller will never delete any SEs and administrator has to manually cleanup unused SEs. Allowed values are 0-525600. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dos_profile(dict[str, Any], Optional):
            se_dos_profile. Defaults to None.

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

        se_dp_hm_drops(int, Optional):
            Internal only. Used to simulate SE - SE HB failure. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_if_state_poll_interval(int, Optional):
            Number of jiffies between polling interface state. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_isolation(bool, Optional):
            Toggle support to run SE datapath instances in isolation on exclusive CPUs. This improves latency and performance. However, this could reduce the total number of se_dp instances created on that SE instance. Supported for >= 8 CPUs. Requires SE reboot. Field introduced in 20.1.4. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_isolation_num_non_dp_cpus(int, Optional):
            Number of CPUs for non se-dp tasks in SE datapath isolation mode. Translates Total cpus minus 'num_non_dp_cpus' for datapath use. It is recommended to reserve an even number of CPUs for hyper-threaded processors. Requires SE reboot. Allowed values are 1-8. Special values are 0- auto. Field introduced in 20.1.4. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_log_nf_enqueue_percent(int, Optional):
            Internal buffer full indicator on the Service Engine beyond which the unfiltered logs are abandoned. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_log_udf_enqueue_percent(int, Optional):
            Internal buffer full indicator on the Service Engine beyond which the user filtered logs are abandoned. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_max_hb_version(int, Optional):
            The highest supported SE-SE Heartbeat protocol version. This version is reported by Secondary SE to Primary SE in Heartbeat response messages. Allowed values are 1-3. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_vnic_queue_stall_event_sleep(int, Optional):
            Time (in seconds) service engine waits for after generating a Vnic transmit queue stall event before resetting theNIC. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_vnic_queue_stall_threshold(int, Optional):
            Number of consecutive transmit failures to look for before generating a Vnic transmit queue stall event. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_vnic_queue_stall_timeout(int, Optional):
            Time (in milliseconds) to wait for network/NIC recovery on detecting a transmit queue stall after which service engine resets the NIC. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_vnic_restart_on_queue_stall_count(int, Optional):
            Number of consecutive transmit queue stall events in se_dp_vnic_stall_se_restart_window to look for before restarting SE. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_vnic_stall_se_restart_window(int, Optional):
            Window of time (in seconds) during which se_dp_vnic_restart_on_queue_stall_count number of consecutive stalls results in a SE restart. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dpdk_pmd(int, Optional):
            Determines if DPDK pool mode driver should be used or not   0  Automatically determine based on hypervisor/NIC type 1  Unconditionally use DPDK poll mode driver 2  Don't use DPDK poll mode driver.Requires SE Reboot. Allowed values are 0-2. Field introduced in 18.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dump_core_on_assert(bool, Optional):
            Enable core dump on assert. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_emulated_cores(int, Optional):
            Use this to emulate more/less cpus than is actually available. One datapath process is started for each core. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Defaults to None.

        se_flow_probe_retries(int, Optional):
            Flow probe retry count if no replies are received.Requires SE Reboot. Allowed values are 0-5. Field introduced in 18.1.4, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_flow_probe_retry_timer(int, Optional):
            Timeout in milliseconds for flow probe retries.Requires SE Reboot. Allowed values are 20-50. Field introduced in 18.2.5. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_group_analytics_policy(dict[str, Any], Optional):
            se_group_analytics_policy. Defaults to None.

            * metrics_event_thresholds (List[dict[str, Any]], Optional):
                Thresholds for various events generated by metrics system. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * metrics_event_threshold_type (str):
                    Type of the metrics event threshold. This value will decide which metric rule (or rules) use configured thresholds. Enum options - THRESHOLD_TYPE_STATIC, SE_CPU_THRESHOLD, SE_MEM_THRESHOLD, SE_DISK_THRESHOLD, CONTROLLER_CPU_THRESHOLD, CONTROLLER_MEM_THRESHOLD, CONTROLLER_DISK_THRESHOLD. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * reset_threshold (float, Optional):
                    This value is used to reset the event state machine. Allowed values are 0-100. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * watermark_thresholds (List[int], Optional):
                    Threshold value for which event in raised. There can be multiple thresholds defined.Health score degrades when the the target is higher than this threshold. Allowed values are 0-100. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        se_hyperthreaded_mode(str, Optional):
            Controls the distribution of SE data path processes on CPUs which support hyper-threading. Requires hyper-threading to be enabled at host level. Requires SE Reboot. For more details please refer to SE placement KB. Enum options - SE_CPU_HT_AUTO, SE_CPU_HT_SPARSE_DISPATCHER_PRIORITY, SE_CPU_HT_SPARSE_PROXY_PRIORITY, SE_CPU_HT_PACKED_CORES. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_ip_encap_ipc(int, Optional):
            Determines if SE-SE IPC messages are encapsulated in an IP header       0        Automatically determine based on hypervisor type    1        Use IP encap unconditionally    ~[0,1]   Don't use IP encapRequires SE Reboot. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_kni_burst_factor(int, Optional):
            This knob controls the resource availability and burst size used between SE datapath and KNI. This helps in minimising packet drops when there is higher KNI traffic (non-VIP traffic from and to Linux). The factor takes the following values      0-default.     1-doubles the burst size and KNI resources.     2-quadruples the burst size and KNI resources. Allowed values are 0-2. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_l3_encap_ipc(int, Optional):
            Determines if SE-SE IPC messages use SE interface IP instead of VIP        0        Automatically determine based on hypervisor type    1        Use SE interface IP unconditionally    ~[0,1]   Don't use SE interface IPRequires SE Reboot. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_log_buffer_app_blocking_dequeue(bool, Optional):
            Internal flag that blocks dataplane until all application logs are flushed to log-agent process. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_log_buffer_conn_blocking_dequeue(bool, Optional):
            Internal flag that blocks dataplane until all connection logs are flushed to log-agent process. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_log_buffer_events_blocking_dequeue(bool, Optional):
            Internal flag that blocks dataplane until all outstanding events are flushed to log-agent process. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_lro(bool, Optional):
            Enable or disable Large Receive Optimization for vnics.Supported on VMXnet3.Requires SE Reboot. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_mp_ring_retry_count(int, Optional):
            The retry count for the multi-producer enqueue before yielding the CPU. To be used under surveillance of Avi Support. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 500), Basic edition(Allowed values- 500), Enterprise with Cloud Services edition. Defaults to None.

        se_mtu(int, Optional):
            MTU for the VNICs of SEs in the SE group. Allowed values are 512-9000. Field introduced in 18.2.8, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_name_prefix(str, Optional):
            Prefix to use for virtual machine name of Service Engines. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_packet_buffer_max(int, Optional):
            Internal use only. Used to artificially reduce the available number of packet buffers. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_pcap_lookahead(bool, Optional):
            Enables lookahead mode of packet receive in PCAP mode. Introduced to overcome an issue with hv_netvsc driver. Lookahead mode attempts to ensure that application and kernel's view of the receive rings are consistent. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_pcap_pkt_count(int, Optional):
            Max number of packets the pcap interface can hold and if the value is 0 the optimum value will be chosen. The optimum value will be chosen based on SE-memory, Cloud Type and Number of Interfaces.Requires SE Reboot. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_pcap_pkt_sz(int, Optional):
            Max size of each packet in the pcap interface. Requires SE Reboot. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_pcap_qdisc_bypass(bool, Optional):
            Bypass the kernel's traffic control layer, to deliver packets directly to the driver. Enabling this feature results in egress packets not being captured in host tcpdump. Note   brief packet reordering or loss may occur upon toggle. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_pcap_reinit_frequency(int, Optional):
            Frequency in seconds at which periodically a PCAP reinit check is triggered. May be used in conjunction with the configuration pcap_reinit_threshold. (Valid range   15 mins - 12 hours, 0 - disables). Allowed values are 900-43200. Special values are 0- disable. Field introduced in 17.2.13, 18.1.3, 18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_pcap_reinit_threshold(int, Optional):
            Threshold for input packet receive errors in PCAP mode exceeding which a PCAP reinit is triggered. If not set, an unconditional reinit is performed. This value is checked every pcap_reinit_frequency interval. Field introduced in 17.2.13, 18.1.3, 18.2.1. Unit is METRIC_COUNT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_probe_port(int, Optional):
            TCP port on SE where echo service will be run. Field introduced in 17.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_rl_prop(dict[str, Any], Optional):
            se_rl_prop. Defaults to None.

            * msf_num_stages (int, Optional):
                Number of stages in msf rate limiter. Allowed values are 1-2. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * msf_stage_size (int, Optional):
                Each stage size in msf rate limiter. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        se_rum_sampling_nav_interval(int, Optional):
            Minimum time to wait on server between taking sampleswhen sampling the navigation timing data from the end user client. Field introduced in 18.2.6. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_rum_sampling_nav_percent(int, Optional):
            Percentage of navigation timing data from the end user client, used for sampling to get client insights. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_rum_sampling_res_interval(int, Optional):
            Minimum time to wait on server between taking sampleswhen sampling the resource timing data from the end user client. Field introduced in 18.2.6. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_rum_sampling_res_percent(int, Optional):
            Percentage of resource timing data from the end user client used for sampling to get client insight. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_sb_dedicated_core(bool, Optional):
            Sideband traffic will be handled by a dedicated core.Requires SE Reboot. Field introduced in 16.5.2, 17.1.9, 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_sb_threads(int, Optional):
            Number of Sideband threads per SE.Requires SE Reboot. Allowed values are 1-128. Field introduced in 16.5.2, 17.1.9, 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_thread_multiplier(int, Optional):
            Multiplier for SE threads based on vCPU. Allowed values are 1-10. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 1), Basic edition(Allowed values- 1), Enterprise with Cloud Services edition. Defaults to None.

        se_time_tracker_props(dict[str, Any], Optional):
            se_time_tracker_props. Defaults to None.

            * egress_audit_mode (str, Optional):
                Audit queueing latency from proxy to dispatcher. Enum options - SE_TT_AUDIT_OFF, SE_TT_AUDIT_ON, SE_TT_AUDIT_ON_WITH_EVENT. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * egress_threshold (int, Optional):
                Maximum egress latency threshold between dispatcher and proxy. Field introduced in 22.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * event_gen_window (int, Optional):
                Window for cumulative event generation. Field introduced in 22.1.1. Unit is SECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ingress_audit_mode (str, Optional):
                Audit queueing latency from dispatcher to proxy. Enum options - SE_TT_AUDIT_OFF, SE_TT_AUDIT_ON, SE_TT_AUDIT_ON_WITH_EVENT. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ingress_threshold (int, Optional):
                Maximum ingress latency threshold between dispatcher and proxy. Field introduced in 22.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        se_tracert_port_range(dict[str, Any], Optional):
            se_tracert_port_range. Defaults to None.

            * end (int):
                TCP/UDP port range end (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * start (int):
                TCP/UDP port range start (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        se_tunnel_mode(int, Optional):
            Determines if Direct Secondary Return (DSR) from secondary SE is active or not  0  Automatically determine based on hypervisor type. 1  Enable tunnel mode - DSR is unconditionally disabled. 2  Disable tunnel mode - DSR is unconditionally enabled. Tunnel mode can be enabled or disabled at run-time. Allowed values are 0-2. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Defaults to None.

        se_tunnel_udp_port(int, Optional):
            UDP Port for tunneled packets from secondary to primary SE in Docker bridge mode.Requires SE Reboot. Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_tx_batch_size(int, Optional):
            Number of packets to batch for transmit to the nic. Requires SE Reboot. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_txq_threshold(int, Optional):
            Once the TX queue of the dispatcher reaches this threshold, hardware queues are not polled for further packets. To be used under surveillance of Avi Support. Allowed values are 512-32768. Field introduced in 20.1.2. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 2048), Basic edition(Allowed values- 2048), Enterprise with Cloud Services edition. Defaults to None.

        se_udp_encap_ipc(int, Optional):
            Determines if SE-SE IPC messages are encapsulated in a UDP header  0  Automatically determine based on hypervisor type. 1  Use UDP encap unconditionally.Requires SE Reboot. Allowed values are 0-1. Field introduced in 17.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_use_dpdk(int, Optional):
            Determines if DPDK library should be used or not   0  Automatically determine based on hypervisor type 1  Use DPDK if PCAP is not enabled 2  Don't use DPDK. Allowed values are 0-2. Field introduced in 18.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_vnic_tx_sw_queue_flush_frequency(int, Optional):
            Configure the frequency in milliseconds of software transmit spillover queue flush when enabled. This is necessary to flush any packets in the spillover queue in the absence of a packet transmit in the normal course of operation. Allowed values are 50-500. Special values are 0- disable. Field introduced in 20.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_vnic_tx_sw_queue_size(int, Optional):
            Configure the size of software transmit spillover queue when enabled. Requires SE Reboot. Allowed values are 128-2048. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_vs_hb_max_pkts_in_batch(int, Optional):
            Maximum number of aggregated vs heartbeat packets to send in a batch. Allowed values are 1-256. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_vs_hb_max_vs_in_pkt(int, Optional):
            Maximum number of virtualservices for which heartbeat messages are aggregated in one packet. Allowed values are 1-1024. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        self_se_election(bool, Optional):
            Enable SEs to elect a primary amongst themselves in the absence of a connectivity to controller. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        send_se_ready_timeout(int, Optional):
            Timeout for sending SE_READY without NS HELPER registration completion. Allowed values are 10-600. Field introduced in 21.1.1. Unit is SECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        service_ip6_subnets(List[dict[str, Any]], Optional):
            IPv6 Subnets assigned to the SE group. Required for VS group placement. Field introduced in 18.1.1. Maximum of 128 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * ip_addr (dict[str, Any]):
                ip_addr

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mask (int):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        service_ip_subnets(List[dict[str, Any]], Optional):
            Subnets assigned to the SE group. Required for VS group placement. Field introduced in 17.1.1. Maximum of 128 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * ip_addr (dict[str, Any]):
                ip_addr

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mask (int):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        shm_minimum_config_memory(int, Optional):
            Minimum required shared memory to apply any configuration. Allowed values are 0-100. Field introduced in 18.1.2. Unit is MB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        significant_log_throttle(int, Optional):
            This setting limits the number of significant logs generated per second per core on this SE. Default is 100 logs per second. Set it to zero (0) to deactivate throttling. Field introduced in 17.1.3. Unit is PER_SECOND. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ssl_preprocess_sni_hostname(bool, Optional):
            (Beta) Preprocess SSL Client Hello for SNI hostname extension.If set to True, this will apply SNI child's SSL protocol(s), if they are different from SNI Parent's allowed SSL protocol(s). Field introduced in 17.2.12, 18.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ssl_sess_cache_per_vs(int, Optional):
            Number of SSL sessions that can be cached per VS. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        transient_shared_memory_max(int, Optional):
            The threshold for the transient shared config memory in the SE. Allowed values are 0-100. Field introduced in 20.1.1. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        udf_log_throttle(int, Optional):
            This setting limits the number of UDF logs generated per second per core on this SE. UDF logs are generated due to the configured client log filters or the rules with logging enabled. Default is 100 logs per second. Set it to zero (0) to deactivate throttling. Field introduced in 17.1.3. Unit is PER_SECOND. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        upstream_connect_timeout(int, Optional):
            Timeout for backend connection. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        upstream_connpool_enable(bool, Optional):
            Enable upstream connection pool,. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        upstream_read_timeout(int, Optional):
            Timeout for data to be received from backend. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        upstream_send_timeout(int, Optional):
            Timeout for upstream to become writable. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 3600000), Basic edition(Allowed values- 3600000), Enterprise with Cloud Services edition. Defaults to None.

        use_dp_util_for_scaleout(bool, Optional):
            If enabled, the datapath CPU utilization is consulted by the auto scale-out logic. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        use_hyperthreaded_cores(bool, Optional):
            Enables the use of hyper-threaded cores on SE. Requires SE Reboot. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        use_legacy_netlink(bool, Optional):
            Enable legacy model of netlink notifications. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        use_objsync(bool, Optional):
            Enable InterSE Objsyc distribution framework. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        use_standard_alb(bool, Optional):
            Use Standard SKU Azure Load Balancer. By default cloud level flag is set. If not set, it inherits/uses the use_standard_alb flag from the cloud. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        user_agent_cache_config(dict[str, Any], Optional):
            user_agent_cache_config. Defaults to None.

            * batch_size (int, Optional):
                How many unknown User-Agents to batch up before querying Controller - unless max_wait_time is reached first. Allowed values are 1-500. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * controller_cache_size (int, Optional):
                The number of User-Agent entries to cache on the Controller. Allowed values are 500-10000000. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * max_age (int, Optional):
                Time interval in seconds after which an existing entry is refreshed from upstream if it has been accessed during max_last_hit_time. Allowed values are 60-604800. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * max_last_hit_time (int, Optional):
                Time interval in seconds backwards from now during which an existing entry must have been hit for refresh from upstream. Entries that have last been accessed further in the past than max_last_hit time are not included in upstream refresh requests even if they are older than 'max_age'. Allowed values are 60-604800. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * max_upstream_queries (int, Optional):
                How often at most to query controller for a given User-Agent. Allowed values are 2-100. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * max_wait_time (int, Optional):
                The time interval in seconds after which to make a request to the Controller, even if the 'batch_size' hasn't been reached yet. Allowed values are 20-100000. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * num_entries_upstream_update (int, Optional):
                How many BotUACacheResult elements to include in an upstream update message. Allowed values are 1-10000. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * percent_reserved_for_bad_bots (int, Optional):
                How much space to reserve in percent for known bad bots. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * percent_reserved_for_browsers (int, Optional):
                How much space to reserve in percent for browsers. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * percent_reserved_for_good_bots (int, Optional):
                How much space to reserve in percent for known good bots. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * percent_reserved_for_outstanding (int, Optional):
                How much space to reserve in percent for outstanding upstream requests. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * se_cache_size (int, Optional):
                The number of User-Agent entries to cache on each Service Engine. Allowed values are 500-10000000. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * upstream_update_interval (int, Optional):
                How often in seconds to send updates about User-Agent cache entries to the next upstream cache. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        user_defined_metric_age(int, Optional):
            Defines in seconds how long before an unused user-defined-metric is garbage collected. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vcenter_clusters(dict[str, Any], Optional):
            vcenter_clusters. Defaults to None.

            * cluster_refs (List[str], Optional):
                 It is a reference to an object of type VIMgrClusterRuntime. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * include (bool, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vcenter_datastore_mode(str, Optional):
             Enum options - VCENTER_DATASTORE_ANY, VCENTER_DATASTORE_LOCAL, VCENTER_DATASTORE_SHARED. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vcenter_datastores(List[dict[str, Any]], Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * datastore_name (str, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * managed_object_id (str, Optional):
                Will be used by default, if not set fallback to datastore_name. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        vcenter_datastores_include(bool, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vcenter_folder(str, Optional):
            Folder to place all the Service Engine virtual machines in vCenter. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vcenter_hosts(dict[str, Any], Optional):
            vcenter_hosts. Defaults to None.

            * host_refs (List[str], Optional):
                 It is a reference to an object of type VIMgrHostRuntime. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * include (bool, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vcenter_parking_vnic_pg(str, Optional):
            Parking port group to be used by 9 vnics at the time of SE creation. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vcenters(List[dict[str, Any]], Optional):
            VCenter information for scoping at Host/Cluster level. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * clusters (List[dict[str, Any]], Optional):
                Cluster vSphere HA configuration. Field introduced in 20.1.7, 21.1.3. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * cluster_id (str, Optional):
                    Transport node cluster. Avi derives vSphere HA property from vCenter cluster.If vSphere HA enabled on vCenter cluster, vSphere will handle HA of ServiceEngine VMs in case of underlying ESX failure.Ex MOB  domain-c23. Field introduced in 20.1.7, 21.1.3. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * override_vsphere_ha (bool, Optional):
                    If this flag set to True, Avi handles ServiceEngine failure irrespective of vSphere HA enabled on vCenter cluster or not. Field introduced in 20.1.7, 21.1.3. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * vmg_name (str, Optional):
                    Cluster VM Group name.VM Group name is unique inside cluster. Field introduced in 20.1.7, 21.1.3. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

            * nsxt_clusters (dict[str, Any], Optional):
                nsxt_clusters

                * cluster_ids (List[str], Optional):
                    List of transport node clusters. Field introduced in 20.1.6. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * include (bool, Optional):
                    Include or Exclude. Field introduced in 20.1.6. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

            * nsxt_datastores (dict[str, Any], Optional):
                nsxt_datastores

                * ds_ids (List[str], Optional):
                    List of shared datastores. Field introduced in 20.1.2. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * include (bool, Optional):
                    Include or Exclude. Field introduced in 20.1.2. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

            * nsxt_hosts (dict[str, Any], Optional):
                nsxt_hosts

                * host_ids (List[str], Optional):
                    List of transport nodes. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * include (bool, Optional):
                    Include or Exclude. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vcenter_folder (str, Optional):
                Folder to place all the Service Engine virtual machines in vCenter. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vcenter_ref (str):
                VCenter server configuration. It is a reference to an object of type VCenterServer. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vcpus_per_se(int, Optional):
            Number of vcpus for each of the Service Engine virtual machines. Changes to this setting do not affect existing SEs. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vip_asg(dict[str, Any], Optional):
            vip_asg. Defaults to None.

            * configuration (dict[str, Any], Optional):
                configuration

                * zones (List[dict[str, Any]], Optional):
                    This is the list of AZ+Subnet in which Vips will be spawned. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * availability_zone (str, Optional):
                        Availability zone associated with the subnet. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                    * fip_capable (bool, Optional):
                        Determines if the subnet is capable of hosting publicly accessible IP. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                    * subnet_uuid (str, Optional):
                        UUID of the subnet for new IP address allocation. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * policy (dict[str, Any], Optional):
                policy

                * dns_cooldown (int, Optional):
                    The amount of time, in seconds, when a Vip is withdrawn before a scaling activity starts. Field introduced in 17.2.12, 18.1.2. Unit is SECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_size (int, Optional):
                    The maximum size of the group. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * min_size (int, Optional):
                    The minimum size of the group. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * suspend (bool, Optional):
                    When set, scaling is suspended. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vnic_dhcp_ip_check_interval(int, Optional):
            DHCP ip check interval. Allowed values are 1-1000. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vnic_dhcp_ip_max_retries(int, Optional):
            DHCP ip max retries. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vnic_ip_delete_interval(int, Optional):
            wait interval before deleting IP. . Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vnic_probe_interval(int, Optional):
            Probe vnic interval. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vnic_rpc_retry_interval(int, Optional):
            Time interval for retrying the failed VNIC RPC requests. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vnicdb_cmd_history_size(int, Optional):
            Size of vnicdb command history. Allowed values are 0-65535. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vs_host_redundancy(bool, Optional):
            Ensure primary and secondary Service Engines are deployed on different physical hosts. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- true), Basic edition(Allowed values- true), Enterprise with Cloud Services edition. Special default for Essentials edition is true, Basic edition is true, Enterprise is True. Defaults to None.

        vs_scalein_timeout(int, Optional):
            Time to wait for the scaled in SE to drain existing flows before marking the scalein done. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vs_scalein_timeout_for_upgrade(int, Optional):
            During SE upgrade, Time to wait for the scaled-in SE to drain existing flows before marking the scalein done. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vs_scaleout_timeout(int, Optional):
            Time to wait for the scaled out SE to become ready before marking the scaleout done. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vs_se_scaleout_additional_wait_time(int, Optional):
            Wait time for sending scaleout ready notification after Virtual Service is marked UP. In certain deployments, there may be an additional delay to accept traffic. For example, for BGP, some time is needed for route advertisement. Allowed values are 0-300. Field introduced in 18.1.5,18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vs_se_scaleout_ready_timeout(int, Optional):
            Timeout in seconds for Service Engine to sendScaleout Ready notification of a Virtual Service. Allowed values are 0-90. Field introduced in 18.1.5,18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vs_switchover_timeout(int, Optional):
            During SE upgrade in a legacy active/standby segroup, Time to wait for the new primary SE to accept flows before marking the switchover done. Field introduced in 17.2.13,18.1.4,18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vss_placement(dict[str, Any], Optional):
            vss_placement. Defaults to None.

            * core_nonaffinity (int, Optional):
                Degree of core non-affinity for VS placement. Allowed values are 1-256. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * num_subcores (int, Optional):
                Number of sub-cores that comprise a CPU core. Allowed values are 1-128. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vss_placement_enabled(bool, Optional):
            If set, Virtual Services will be placed on only a subset of the cores of an SE. Field introduced in 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        waf_mempool(bool, Optional):
            Enable memory pool for WAF.Requires SE Reboot. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        waf_mempool_size(int, Optional):
            Memory pool size used for WAF.Requires SE Reboot. Field introduced in 17.2.3. Unit is KB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              nsx_alb.alb.service_engine_group.present:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.service_engine_group.create
    """

    result = dict(comment=[], ret=[], result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "accelerated_networking": "accelerated_networking",
        "active_standby": "active_standby",
        "aggressive_failure_detection": "aggressive_failure_detection",
        "algo": "algo",
        "allow_burst": "allow_burst",
        "app_cache_percent": "app_cache_percent",
        "app_cache_threshold": "app_cache_threshold",
        "app_learning_memory_percent": "app_learning_memory_percent",
        "archive_shm_limit": "archive_shm_limit",
        "async_ssl": "async_ssl",
        "async_ssl_threads": "async_ssl_threads",
        "auto_rebalance": "auto_rebalance",
        "auto_rebalance_capacity_per_se": "auto_rebalance_capacity_per_se",
        "auto_rebalance_criteria": "auto_rebalance_criteria",
        "auto_rebalance_interval": "auto_rebalance_interval",
        "auto_redistribute_active_standby_load": "auto_redistribute_active_standby_load",
        "availability_zone_refs": "availability_zone_refs",
        "baremetal_dispatcher_handles_flows": "baremetal_dispatcher_handles_flows",
        "bgp_peer_monitor_failover_enabled": "bgp_peer_monitor_failover_enabled",
        "bgp_state_update_interval": "bgp_state_update_interval",
        "buffer_se": "buffer_se",
        "cloud_ref": "cloud_ref",
        "compress_ip_rules_for_each_ns_subnet": "compress_ip_rules_for_each_ns_subnet",
        "config_debugs_on_all_cores": "config_debugs_on_all_cores",
        "configpb_attributes": "configpb_attributes",
        "connection_memory_percentage": "connection_memory_percentage",
        "core_shm_app_cache": "core_shm_app_cache",
        "core_shm_app_learning": "core_shm_app_learning",
        "cpu_reserve": "cpu_reserve",
        "cpu_socket_affinity": "cpu_socket_affinity",
        "custom_securitygroups_data": "custom_securitygroups_data",
        "custom_securitygroups_mgmt": "custom_securitygroups_mgmt",
        "custom_tag": "custom_tag",
        "data_network_id": "data_network_id",
        "datascript_timeout": "datascript_timeout",
        "deactivate_ipv6_discovery": "deactivate_ipv6_discovery",
        "deactivate_kni_filtering_at_dispatcher": "deactivate_kni_filtering_at_dispatcher",
        "dedicated_dispatcher_core": "dedicated_dispatcher_core",
        "description": "description",
        "disable_avi_securitygroups": "disable_avi_securitygroups",
        "disable_csum_offloads": "disable_csum_offloads",
        "disable_flow_probes": "disable_flow_probes",
        "disable_gro": "disable_gro",
        "disable_se_memory_check": "disable_se_memory_check",
        "disable_tso": "disable_tso",
        "disk_per_se": "disk_per_se",
        "distribute_load_active_standby": "distribute_load_active_standby",
        "distribute_queues": "distribute_queues",
        "distribute_vnics": "distribute_vnics",
        "downstream_send_timeout": "downstream_send_timeout",
        "dp_aggressive_deq_interval_msec": "dp_aggressive_deq_interval_msec",
        "dp_aggressive_enq_interval_msec": "dp_aggressive_enq_interval_msec",
        "dp_aggressive_hb_frequency": "dp_aggressive_hb_frequency",
        "dp_aggressive_hb_timeout_count": "dp_aggressive_hb_timeout_count",
        "dp_deq_interval_msec": "dp_deq_interval_msec",
        "dp_enq_interval_msec": "dp_enq_interval_msec",
        "dp_hb_frequency": "dp_hb_frequency",
        "dp_hb_timeout_count": "dp_hb_timeout_count",
        "dpdk_gro_timeout_interval": "dpdk_gro_timeout_interval",
        "enable_gratarp_permanent": "enable_gratarp_permanent",
        "enable_hsm_log": "enable_hsm_log",
        "enable_hsm_priming": "enable_hsm_priming",
        "enable_multi_lb": "enable_multi_lb",
        "enable_pcap_tx_ring": "enable_pcap_tx_ring",
        "ephemeral_portrange_end": "ephemeral_portrange_end",
        "ephemeral_portrange_start": "ephemeral_portrange_start",
        "extra_config_multiplier": "extra_config_multiplier",
        "extra_shared_config_memory": "extra_shared_config_memory",
        "flow_table_new_syn_max_entries": "flow_table_new_syn_max_entries",
        "free_list_size": "free_list_size",
        "gcp_config": "gcp_config",
        "gratarp_permanent_periodicity": "gratarp_permanent_periodicity",
        "grpc_channel_connect_timeout": "grpc_channel_connect_timeout",
        "ha_mode": "ha_mode",
        "handle_per_pkt_attack": "handle_per_pkt_attack",
        "hardwaresecuritymodulegroup_ref": "hardwaresecuritymodulegroup_ref",
        "heap_minimum_config_memory": "heap_minimum_config_memory",
        "hm_on_standby": "hm_on_standby",
        "host_attribute_key": "host_attribute_key",
        "host_attribute_value": "host_attribute_value",
        "host_gateway_monitor": "host_gateway_monitor",
        "http_rum_console_log": "http_rum_console_log",
        "http_rum_min_content_length": "http_rum_min_content_length",
        "hybrid_rss_mode": "hybrid_rss_mode",
        "hypervisor": "hypervisor",
        "ignore_docker_mac_change": "ignore_docker_mac_change",
        "ignore_rtt_threshold": "ignore_rtt_threshold",
        "ingress_access_data": "ingress_access_data",
        "ingress_access_mgmt": "ingress_access_mgmt",
        "instance_flavor": "instance_flavor",
        "instance_flavor_info": "instance_flavor_info",
        "iptables": "iptables",
        "kni_allowed_server_ports": "kni_allowed_server_ports",
        "l7_conns_per_core": "l7_conns_per_core",
        "l7_resvd_listen_conns_per_core": "l7_resvd_listen_conns_per_core",
        "labels": "labels",
        "lbaction_num_requests_to_dispatch": "lbaction_num_requests_to_dispatch",
        "lbaction_rq_per_request_max_retries": "lbaction_rq_per_request_max_retries",
        "least_load_core_selection": "least_load_core_selection",
        "license_tier": "license_tier",
        "license_type": "license_type",
        "log_agent_compress_logs": "log_agent_compress_logs",
        "log_agent_debug_enabled": "log_agent_debug_enabled",
        "log_agent_file_sz_appl": "log_agent_file_sz_appl",
        "log_agent_file_sz_conn": "log_agent_file_sz_conn",
        "log_agent_file_sz_debug": "log_agent_file_sz_debug",
        "log_agent_file_sz_event": "log_agent_file_sz_event",
        "log_agent_log_storage_min_sz": "log_agent_log_storage_min_sz",
        "log_agent_max_concurrent_rsync": "log_agent_max_concurrent_rsync",
        "log_agent_max_storage_excess_percent": "log_agent_max_storage_excess_percent",
        "log_agent_max_storage_ignore_percent": "log_agent_max_storage_ignore_percent",
        "log_agent_min_storage_per_vs": "log_agent_min_storage_per_vs",
        "log_agent_sleep_interval": "log_agent_sleep_interval",
        "log_agent_trace_enabled": "log_agent_trace_enabled",
        "log_agent_unknown_vs_timer": "log_agent_unknown_vs_timer",
        "log_disksz": "log_disksz",
        "log_malloc_failure": "log_malloc_failure",
        "log_message_max_file_list_size": "log_message_max_file_list_size",
        "markers": "markers",
        "max_concurrent_external_hm": "max_concurrent_external_hm",
        "max_cpu_usage": "max_cpu_usage",
        "max_memory_per_mempool": "max_memory_per_mempool",
        "max_num_se_dps": "max_num_se_dps",
        "max_public_ips_per_lb": "max_public_ips_per_lb",
        "max_queues_per_vnic": "max_queues_per_vnic",
        "max_rules_per_lb": "max_rules_per_lb",
        "max_scaleout_per_vs": "max_scaleout_per_vs",
        "max_se": "max_se",
        "max_skb_frags": "max_skb_frags",
        "max_vs_per_se": "max_vs_per_se",
        "mem_reserve": "mem_reserve",
        "memory_for_config_update": "memory_for_config_update",
        "memory_per_se": "memory_per_se",
        "mgmt_network_ref": "mgmt_network_ref",
        "mgmt_subnet": "mgmt_subnet",
        "min_cpu_usage": "min_cpu_usage",
        "min_scaleout_per_vs": "min_scaleout_per_vs",
        "min_se": "min_se",
        "minimum_connection_memory": "minimum_connection_memory",
        "n_log_streaming_threads": "n_log_streaming_threads",
        "name": "name",
        "netlink_poller_threads": "netlink_poller_threads",
        "netlink_sock_buf_size": "netlink_sock_buf_size",
        "ngx_free_connection_stack": "ngx_free_connection_stack",
        "non_significant_log_throttle": "non_significant_log_throttle",
        "ns_helper_deq_interval_msec": "ns_helper_deq_interval_msec",
        "ntp_sync_fail_event": "ntp_sync_fail_event",
        "ntp_sync_status_interval": "ntp_sync_status_interval",
        "num_dispatcher_cores": "num_dispatcher_cores",
        "num_dispatcher_queues": "num_dispatcher_queues",
        "num_flow_cores_sum_changes_to_ignore": "num_flow_cores_sum_changes_to_ignore",
        "objsync_config": "objsync_config",
        "objsync_port": "objsync_port",
        "openstack_availability_zones": "openstack_availability_zones",
        "openstack_mgmt_network_name": "openstack_mgmt_network_name",
        "openstack_mgmt_network_uuid": "openstack_mgmt_network_uuid",
        "os_reserved_memory": "os_reserved_memory",
        "pcap_tx_mode": "pcap_tx_mode",
        "pcap_tx_ring_rd_balancing_factor": "pcap_tx_ring_rd_balancing_factor",
        "per_app": "per_app",
        "per_vs_admission_control": "per_vs_admission_control",
        "placement_mode": "placement_mode",
        "realtime_se_metrics": "realtime_se_metrics",
        "reboot_on_panic": "reboot_on_panic",
        "replay_vrf_routes_interval": "replay_vrf_routes_interval",
        "resync_time_interval": "resync_time_interval",
        "sdb_flush_interval": "sdb_flush_interval",
        "sdb_pipeline_size": "sdb_pipeline_size",
        "sdb_scan_count": "sdb_scan_count",
        "se_bandwidth_type": "se_bandwidth_type",
        "se_delayed_flow_delete": "se_delayed_flow_delete",
        "se_deprovision_delay": "se_deprovision_delay",
        "se_dos_profile": "se_dos_profile",
        "se_dp_hm_drops": "se_dp_hm_drops",
        "se_dp_if_state_poll_interval": "se_dp_if_state_poll_interval",
        "se_dp_isolation": "se_dp_isolation",
        "se_dp_isolation_num_non_dp_cpus": "se_dp_isolation_num_non_dp_cpus",
        "se_dp_log_nf_enqueue_percent": "se_dp_log_nf_enqueue_percent",
        "se_dp_log_udf_enqueue_percent": "se_dp_log_udf_enqueue_percent",
        "se_dp_max_hb_version": "se_dp_max_hb_version",
        "se_dp_vnic_queue_stall_event_sleep": "se_dp_vnic_queue_stall_event_sleep",
        "se_dp_vnic_queue_stall_threshold": "se_dp_vnic_queue_stall_threshold",
        "se_dp_vnic_queue_stall_timeout": "se_dp_vnic_queue_stall_timeout",
        "se_dp_vnic_restart_on_queue_stall_count": "se_dp_vnic_restart_on_queue_stall_count",
        "se_dp_vnic_stall_se_restart_window": "se_dp_vnic_stall_se_restart_window",
        "se_dpdk_pmd": "se_dpdk_pmd",
        "se_dump_core_on_assert": "se_dump_core_on_assert",
        "se_emulated_cores": "se_emulated_cores",
        "se_flow_probe_retries": "se_flow_probe_retries",
        "se_flow_probe_retry_timer": "se_flow_probe_retry_timer",
        "se_group_analytics_policy": "se_group_analytics_policy",
        "se_hyperthreaded_mode": "se_hyperthreaded_mode",
        "se_ip_encap_ipc": "se_ip_encap_ipc",
        "se_kni_burst_factor": "se_kni_burst_factor",
        "se_l3_encap_ipc": "se_l3_encap_ipc",
        "se_log_buffer_app_blocking_dequeue": "se_log_buffer_app_blocking_dequeue",
        "se_log_buffer_conn_blocking_dequeue": "se_log_buffer_conn_blocking_dequeue",
        "se_log_buffer_events_blocking_dequeue": "se_log_buffer_events_blocking_dequeue",
        "se_lro": "se_lro",
        "se_mp_ring_retry_count": "se_mp_ring_retry_count",
        "se_mtu": "se_mtu",
        "se_name_prefix": "se_name_prefix",
        "se_packet_buffer_max": "se_packet_buffer_max",
        "se_pcap_lookahead": "se_pcap_lookahead",
        "se_pcap_pkt_count": "se_pcap_pkt_count",
        "se_pcap_pkt_sz": "se_pcap_pkt_sz",
        "se_pcap_qdisc_bypass": "se_pcap_qdisc_bypass",
        "se_pcap_reinit_frequency": "se_pcap_reinit_frequency",
        "se_pcap_reinit_threshold": "se_pcap_reinit_threshold",
        "se_probe_port": "se_probe_port",
        "se_rl_prop": "se_rl_prop",
        "se_rum_sampling_nav_interval": "se_rum_sampling_nav_interval",
        "se_rum_sampling_nav_percent": "se_rum_sampling_nav_percent",
        "se_rum_sampling_res_interval": "se_rum_sampling_res_interval",
        "se_rum_sampling_res_percent": "se_rum_sampling_res_percent",
        "se_sb_dedicated_core": "se_sb_dedicated_core",
        "se_sb_threads": "se_sb_threads",
        "se_thread_multiplier": "se_thread_multiplier",
        "se_time_tracker_props": "se_time_tracker_props",
        "se_tracert_port_range": "se_tracert_port_range",
        "se_tunnel_mode": "se_tunnel_mode",
        "se_tunnel_udp_port": "se_tunnel_udp_port",
        "se_tx_batch_size": "se_tx_batch_size",
        "se_txq_threshold": "se_txq_threshold",
        "se_udp_encap_ipc": "se_udp_encap_ipc",
        "se_use_dpdk": "se_use_dpdk",
        "se_vnic_tx_sw_queue_flush_frequency": "se_vnic_tx_sw_queue_flush_frequency",
        "se_vnic_tx_sw_queue_size": "se_vnic_tx_sw_queue_size",
        "se_vs_hb_max_pkts_in_batch": "se_vs_hb_max_pkts_in_batch",
        "se_vs_hb_max_vs_in_pkt": "se_vs_hb_max_vs_in_pkt",
        "self_se_election": "self_se_election",
        "send_se_ready_timeout": "send_se_ready_timeout",
        "service_ip6_subnets": "service_ip6_subnets",
        "service_ip_subnets": "service_ip_subnets",
        "shm_minimum_config_memory": "shm_minimum_config_memory",
        "significant_log_throttle": "significant_log_throttle",
        "ssl_preprocess_sni_hostname": "ssl_preprocess_sni_hostname",
        "ssl_sess_cache_per_vs": "ssl_sess_cache_per_vs",
        "tenant_ref": "tenant_ref",
        "transient_shared_memory_max": "transient_shared_memory_max",
        "udf_log_throttle": "udf_log_throttle",
        "upstream_connect_timeout": "upstream_connect_timeout",
        "upstream_connpool_enable": "upstream_connpool_enable",
        "upstream_read_timeout": "upstream_read_timeout",
        "upstream_send_timeout": "upstream_send_timeout",
        "use_dp_util_for_scaleout": "use_dp_util_for_scaleout",
        "use_hyperthreaded_cores": "use_hyperthreaded_cores",
        "use_legacy_netlink": "use_legacy_netlink",
        "use_objsync": "use_objsync",
        "use_standard_alb": "use_standard_alb",
        "user_agent_cache_config": "user_agent_cache_config",
        "user_defined_metric_age": "user_defined_metric_age",
        "vcenter_clusters": "vcenter_clusters",
        "vcenter_datastore_mode": "vcenter_datastore_mode",
        "vcenter_datastores": "vcenter_datastores",
        "vcenter_datastores_include": "vcenter_datastores_include",
        "vcenter_folder": "vcenter_folder",
        "vcenter_hosts": "vcenter_hosts",
        "vcenter_parking_vnic_pg": "vcenter_parking_vnic_pg",
        "vcenters": "vcenters",
        "vcpus_per_se": "vcpus_per_se",
        "vip_asg": "vip_asg",
        "vnic_dhcp_ip_check_interval": "vnic_dhcp_ip_check_interval",
        "vnic_dhcp_ip_max_retries": "vnic_dhcp_ip_max_retries",
        "vnic_ip_delete_interval": "vnic_ip_delete_interval",
        "vnic_probe_interval": "vnic_probe_interval",
        "vnic_rpc_retry_interval": "vnic_rpc_retry_interval",
        "vnicdb_cmd_history_size": "vnicdb_cmd_history_size",
        "vs_host_redundancy": "vs_host_redundancy",
        "vs_scalein_timeout": "vs_scalein_timeout",
        "vs_scalein_timeout_for_upgrade": "vs_scalein_timeout_for_upgrade",
        "vs_scaleout_timeout": "vs_scaleout_timeout",
        "vs_se_scaleout_additional_wait_time": "vs_se_scaleout_additional_wait_time",
        "vs_se_scaleout_ready_timeout": "vs_se_scaleout_ready_timeout",
        "vs_switchover_timeout": "vs_switchover_timeout",
        "vss_placement": "vss_placement",
        "vss_placement_enabled": "vss_placement_enabled",
        "waf_mempool": "waf_mempool",
        "waf_mempool_size": "waf_mempool_size",
    }

    payload = {}
    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = value

    create = await hub.tool.nsx_alb.session.request(
        ctx,
        method="post",
        path="/serviceenginegroup",
        query_params={},
        data=payload,
    )

    if not create["result"]:
        result["comment"].append(create["comment"])
        result["result"] = False
        return result

    result["comment"].append(
        f"Created nsx_alb.alb.service_engine_group '{name}'",
    )

    result["ret"] = create["ret"]

    result["ret"]["resource_id"] = create["ret"]["uuid"]
    return result


async def update(
    hub,
    ctx,
    resource_id: str,
    name: str = None,
    accelerated_networking: bool = None,
    active_standby: bool = None,
    aggressive_failure_detection: bool = None,
    algo: str = None,
    allow_burst: bool = None,
    app_cache_percent: int = None,
    app_cache_threshold: int = None,
    app_learning_memory_percent: int = None,
    archive_shm_limit: int = None,
    async_ssl: bool = None,
    async_ssl_threads: int = None,
    auto_rebalance: bool = None,
    auto_rebalance_capacity_per_se: List[int] = None,
    auto_rebalance_criteria: List[str] = None,
    auto_rebalance_interval: int = None,
    auto_redistribute_active_standby_load: bool = None,
    availability_zone_refs: List[str] = None,
    baremetal_dispatcher_handles_flows: bool = None,
    bgp_peer_monitor_failover_enabled: bool = None,
    bgp_state_update_interval: int = None,
    buffer_se: int = None,
    cloud_ref: str = None,
    compress_ip_rules_for_each_ns_subnet: bool = None,
    config_debugs_on_all_cores: bool = None,
    configpb_attributes: make_dataclass(
        "configpb_attributes", [("version", int, field(default=None))]
    ) = None,
    connection_memory_percentage: int = None,
    core_shm_app_cache: bool = None,
    core_shm_app_learning: bool = None,
    cpu_reserve: bool = None,
    cpu_socket_affinity: bool = None,
    custom_securitygroups_data: List[str] = None,
    custom_securitygroups_mgmt: List[str] = None,
    custom_tag: List[
        make_dataclass(
            "custom_tag", [("tag_key", str), ("tag_val", str, field(default=None))]
        )
    ] = None,
    data_network_id: str = None,
    datascript_timeout: int = None,
    deactivate_ipv6_discovery: bool = None,
    deactivate_kni_filtering_at_dispatcher: bool = None,
    dedicated_dispatcher_core: bool = None,
    description: str = None,
    disable_avi_securitygroups: bool = None,
    disable_csum_offloads: bool = None,
    disable_flow_probes: bool = None,
    disable_gro: bool = None,
    disable_se_memory_check: bool = None,
    disable_tso: bool = None,
    disk_per_se: int = None,
    distribute_load_active_standby: bool = None,
    distribute_queues: bool = None,
    distribute_vnics: bool = None,
    downstream_send_timeout: int = None,
    dp_aggressive_deq_interval_msec: int = None,
    dp_aggressive_enq_interval_msec: int = None,
    dp_aggressive_hb_frequency: int = None,
    dp_aggressive_hb_timeout_count: int = None,
    dp_deq_interval_msec: int = None,
    dp_enq_interval_msec: int = None,
    dp_hb_frequency: int = None,
    dp_hb_timeout_count: int = None,
    dpdk_gro_timeout_interval: int = None,
    enable_gratarp_permanent: bool = None,
    enable_hsm_log: bool = None,
    enable_hsm_priming: bool = None,
    enable_multi_lb: bool = None,
    enable_pcap_tx_ring: bool = None,
    ephemeral_portrange_end: int = None,
    ephemeral_portrange_start: int = None,
    extra_config_multiplier: float = None,
    extra_shared_config_memory: int = None,
    flow_table_new_syn_max_entries: int = None,
    free_list_size: int = None,
    gcp_config: make_dataclass(
        "gcp_config",
        [
            ("backend_data_vpc_network_name", str, field(default=None)),
            ("backend_data_vpc_project_id", str, field(default=None)),
            ("backend_data_vpc_subnet_name", str, field(default=None)),
        ],
    ) = None,
    gratarp_permanent_periodicity: int = None,
    grpc_channel_connect_timeout: int = None,
    ha_mode: str = None,
    handle_per_pkt_attack: bool = None,
    hardwaresecuritymodulegroup_ref: str = None,
    heap_minimum_config_memory: int = None,
    hm_on_standby: bool = None,
    host_attribute_key: str = None,
    host_attribute_value: str = None,
    host_gateway_monitor: bool = None,
    http_rum_console_log: bool = None,
    http_rum_min_content_length: int = None,
    hybrid_rss_mode: bool = None,
    hypervisor: str = None,
    ignore_docker_mac_change: bool = None,
    ignore_rtt_threshold: int = None,
    ingress_access_data: str = None,
    ingress_access_mgmt: str = None,
    instance_flavor: str = None,
    instance_flavor_info: make_dataclass(
        "instance_flavor_info",
        [
            ("id", str),
            ("name", str),
            ("cost", str, field(default=None)),
            ("disk_gb", int, field(default=None)),
            ("enhanced_nw", bool, field(default=None)),
            ("is_recommended", bool, field(default=None)),
            ("max_ip6s_per_nic", int, field(default=None)),
            ("max_ips_per_nic", int, field(default=None)),
            ("max_nics", int, field(default=None)),
            (
                "meta",
                List[make_dataclass("meta", [("key", str), ("value", str)])],
                field(default=None),
            ),
            ("public", bool, field(default=None)),
            ("ram_mb", int, field(default=None)),
            ("vcpus", int, field(default=None)),
        ],
    ) = None,
    iptables: List[
        make_dataclass(
            "iptables",
            [
                ("chain", str),
                ("table", str),
                (
                    "rules",
                    List[
                        make_dataclass(
                            "rules",
                            [
                                ("action", str),
                                (
                                    "dnat_ip",
                                    make_dataclass(
                                        "dnat_ip", [("addr", str), ("type", str)]
                                    ),
                                    field(default=None),
                                ),
                                (
                                    "dst_ip",
                                    make_dataclass(
                                        "dst_ip",
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
                                    "dst_port",
                                    make_dataclass(
                                        "dst_port", [("end", int), ("start", int)]
                                    ),
                                    field(default=None),
                                ),
                                ("input_interface", str, field(default=None)),
                                ("output_interface", str, field(default=None)),
                                ("proto", str, field(default=None)),
                                (
                                    "src_ip",
                                    make_dataclass(
                                        "src_ip",
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
                                    "src_port",
                                    make_dataclass(
                                        "src_port", [("end", int), ("start", int)]
                                    ),
                                    field(default=None),
                                ),
                                ("tag", str, field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
            ],
        )
    ] = None,
    kni_allowed_server_ports: List[
        make_dataclass(
            "kni_allowed_server_ports",
            [
                ("protocol", str),
                ("range", make_dataclass("range", [("end", int), ("start", int)])),
            ],
        )
    ] = None,
    l7_conns_per_core: int = None,
    l7_resvd_listen_conns_per_core: int = None,
    labels: List[
        make_dataclass("labels", [("key", str), ("value", str, field(default=None))])
    ] = None,
    lbaction_num_requests_to_dispatch: int = None,
    lbaction_rq_per_request_max_retries: int = None,
    least_load_core_selection: bool = None,
    license_tier: str = None,
    license_type: str = None,
    log_agent_compress_logs: bool = None,
    log_agent_debug_enabled: bool = None,
    log_agent_file_sz_appl: int = None,
    log_agent_file_sz_conn: int = None,
    log_agent_file_sz_debug: int = None,
    log_agent_file_sz_event: int = None,
    log_agent_log_storage_min_sz: int = None,
    log_agent_max_concurrent_rsync: int = None,
    log_agent_max_storage_excess_percent: int = None,
    log_agent_max_storage_ignore_percent: float = None,
    log_agent_min_storage_per_vs: int = None,
    log_agent_sleep_interval: int = None,
    log_agent_trace_enabled: bool = None,
    log_agent_unknown_vs_timer: int = None,
    log_disksz: int = None,
    log_malloc_failure: bool = None,
    log_message_max_file_list_size: int = None,
    markers: List[
        make_dataclass(
            "markers", [("key", str), ("values", List[str], field(default=None))]
        )
    ] = None,
    max_concurrent_external_hm: int = None,
    max_cpu_usage: int = None,
    max_memory_per_mempool: int = None,
    max_num_se_dps: int = None,
    max_public_ips_per_lb: int = None,
    max_queues_per_vnic: int = None,
    max_rules_per_lb: int = None,
    max_scaleout_per_vs: int = None,
    max_se: int = None,
    max_skb_frags: int = None,
    max_vs_per_se: int = None,
    mem_reserve: bool = None,
    memory_for_config_update: int = None,
    memory_per_se: int = None,
    mgmt_network_ref: str = None,
    mgmt_subnet: make_dataclass(
        "mgmt_subnet",
        [
            ("ip_addr", make_dataclass("ip_addr", [("addr", str), ("type", str)])),
            ("mask", int),
        ],
    ) = None,
    min_cpu_usage: int = None,
    min_scaleout_per_vs: int = None,
    min_se: int = None,
    minimum_connection_memory: int = None,
    n_log_streaming_threads: int = None,
    netlink_poller_threads: int = None,
    netlink_sock_buf_size: int = None,
    ngx_free_connection_stack: bool = None,
    non_significant_log_throttle: int = None,
    ns_helper_deq_interval_msec: int = None,
    ntp_sync_fail_event: bool = None,
    ntp_sync_status_interval: int = None,
    num_dispatcher_cores: int = None,
    num_dispatcher_queues: int = None,
    num_flow_cores_sum_changes_to_ignore: int = None,
    objsync_config: make_dataclass(
        "objsync_config",
        [
            ("objsync_cpu_limit", int, field(default=None)),
            ("objsync_hub_elect_interval", int, field(default=None)),
            ("objsync_reconcile_interval", int, field(default=None)),
        ],
    ) = None,
    objsync_port: int = None,
    openstack_availability_zones: List[str] = None,
    openstack_mgmt_network_name: str = None,
    openstack_mgmt_network_uuid: str = None,
    os_reserved_memory: int = None,
    pcap_tx_mode: str = None,
    pcap_tx_ring_rd_balancing_factor: int = None,
    per_app: bool = None,
    per_vs_admission_control: bool = None,
    placement_mode: str = None,
    realtime_se_metrics: make_dataclass(
        "realtime_se_metrics",
        [("enabled", bool), ("duration", int, field(default=None))],
    ) = None,
    reboot_on_panic: bool = None,
    replay_vrf_routes_interval: int = None,
    resync_time_interval: int = None,
    sdb_flush_interval: int = None,
    sdb_pipeline_size: int = None,
    sdb_scan_count: int = None,
    se_bandwidth_type: str = None,
    se_delayed_flow_delete: bool = None,
    se_deprovision_delay: int = None,
    se_dos_profile: make_dataclass(
        "se_dos_profile",
        [
            ("thresh_period", int),
            (
                "thresh_info",
                List[
                    make_dataclass(
                        "thresh_info",
                        [("attack", str), ("max_value", int), ("min_value", int)],
                    )
                ],
                field(default=None),
            ),
        ],
    ) = None,
    se_dp_hm_drops: int = None,
    se_dp_if_state_poll_interval: int = None,
    se_dp_isolation: bool = None,
    se_dp_isolation_num_non_dp_cpus: int = None,
    se_dp_log_nf_enqueue_percent: int = None,
    se_dp_log_udf_enqueue_percent: int = None,
    se_dp_max_hb_version: int = None,
    se_dp_vnic_queue_stall_event_sleep: int = None,
    se_dp_vnic_queue_stall_threshold: int = None,
    se_dp_vnic_queue_stall_timeout: int = None,
    se_dp_vnic_restart_on_queue_stall_count: int = None,
    se_dp_vnic_stall_se_restart_window: int = None,
    se_dpdk_pmd: int = None,
    se_dump_core_on_assert: bool = None,
    se_emulated_cores: int = None,
    se_flow_probe_retries: int = None,
    se_flow_probe_retry_timer: int = None,
    se_group_analytics_policy: make_dataclass(
        "se_group_analytics_policy",
        [
            (
                "metrics_event_thresholds",
                List[
                    make_dataclass(
                        "metrics_event_thresholds",
                        [
                            ("metrics_event_threshold_type", str),
                            ("reset_threshold", float, field(default=None)),
                            ("watermark_thresholds", List[int], field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            )
        ],
    ) = None,
    se_hyperthreaded_mode: str = None,
    se_ip_encap_ipc: int = None,
    se_kni_burst_factor: int = None,
    se_l3_encap_ipc: int = None,
    se_log_buffer_app_blocking_dequeue: bool = None,
    se_log_buffer_conn_blocking_dequeue: bool = None,
    se_log_buffer_events_blocking_dequeue: bool = None,
    se_lro: bool = None,
    se_mp_ring_retry_count: int = None,
    se_mtu: int = None,
    se_name_prefix: str = None,
    se_packet_buffer_max: int = None,
    se_pcap_lookahead: bool = None,
    se_pcap_pkt_count: int = None,
    se_pcap_pkt_sz: int = None,
    se_pcap_qdisc_bypass: bool = None,
    se_pcap_reinit_frequency: int = None,
    se_pcap_reinit_threshold: int = None,
    se_probe_port: int = None,
    se_rl_prop: make_dataclass(
        "se_rl_prop",
        [
            ("msf_num_stages", int, field(default=None)),
            ("msf_stage_size", int, field(default=None)),
        ],
    ) = None,
    se_rum_sampling_nav_interval: int = None,
    se_rum_sampling_nav_percent: int = None,
    se_rum_sampling_res_interval: int = None,
    se_rum_sampling_res_percent: int = None,
    se_sb_dedicated_core: bool = None,
    se_sb_threads: int = None,
    se_thread_multiplier: int = None,
    se_time_tracker_props: make_dataclass(
        "se_time_tracker_props",
        [
            ("egress_audit_mode", str, field(default=None)),
            ("egress_threshold", int, field(default=None)),
            ("event_gen_window", int, field(default=None)),
            ("ingress_audit_mode", str, field(default=None)),
            ("ingress_threshold", int, field(default=None)),
        ],
    ) = None,
    se_tracert_port_range: make_dataclass(
        "se_tracert_port_range", [("end", int), ("start", int)]
    ) = None,
    se_tunnel_mode: int = None,
    se_tunnel_udp_port: int = None,
    se_tx_batch_size: int = None,
    se_txq_threshold: int = None,
    se_udp_encap_ipc: int = None,
    se_use_dpdk: int = None,
    se_vnic_tx_sw_queue_flush_frequency: int = None,
    se_vnic_tx_sw_queue_size: int = None,
    se_vs_hb_max_pkts_in_batch: int = None,
    se_vs_hb_max_vs_in_pkt: int = None,
    self_se_election: bool = None,
    send_se_ready_timeout: int = None,
    service_ip6_subnets: List[
        make_dataclass(
            "service_ip6_subnets",
            [
                ("ip_addr", make_dataclass("ip_addr", [("addr", str), ("type", str)])),
                ("mask", int),
            ],
        )
    ] = None,
    service_ip_subnets: List[
        make_dataclass(
            "service_ip_subnets",
            [
                ("ip_addr", make_dataclass("ip_addr", [("addr", str), ("type", str)])),
                ("mask", int),
            ],
        )
    ] = None,
    shm_minimum_config_memory: int = None,
    significant_log_throttle: int = None,
    ssl_preprocess_sni_hostname: bool = None,
    ssl_sess_cache_per_vs: int = None,
    tenant_ref: str = None,
    transient_shared_memory_max: int = None,
    udf_log_throttle: int = None,
    upstream_connect_timeout: int = None,
    upstream_connpool_enable: bool = None,
    upstream_read_timeout: int = None,
    upstream_send_timeout: int = None,
    use_dp_util_for_scaleout: bool = None,
    use_hyperthreaded_cores: bool = None,
    use_legacy_netlink: bool = None,
    use_objsync: bool = None,
    use_standard_alb: bool = None,
    user_agent_cache_config: make_dataclass(
        "user_agent_cache_config",
        [
            ("batch_size", int, field(default=None)),
            ("controller_cache_size", int, field(default=None)),
            ("max_age", int, field(default=None)),
            ("max_last_hit_time", int, field(default=None)),
            ("max_upstream_queries", int, field(default=None)),
            ("max_wait_time", int, field(default=None)),
            ("num_entries_upstream_update", int, field(default=None)),
            ("percent_reserved_for_bad_bots", int, field(default=None)),
            ("percent_reserved_for_browsers", int, field(default=None)),
            ("percent_reserved_for_good_bots", int, field(default=None)),
            ("percent_reserved_for_outstanding", int, field(default=None)),
            ("se_cache_size", int, field(default=None)),
            ("upstream_update_interval", int, field(default=None)),
        ],
    ) = None,
    user_defined_metric_age: int = None,
    vcenter_clusters: make_dataclass(
        "vcenter_clusters",
        [
            ("cluster_refs", List[str], field(default=None)),
            ("include", bool, field(default=None)),
        ],
    ) = None,
    vcenter_datastore_mode: str = None,
    vcenter_datastores: List[
        make_dataclass(
            "vcenter_datastores",
            [
                ("datastore_name", str, field(default=None)),
                ("managed_object_id", str, field(default=None)),
            ],
        )
    ] = None,
    vcenter_datastores_include: bool = None,
    vcenter_folder: str = None,
    vcenter_hosts: make_dataclass(
        "vcenter_hosts",
        [
            ("host_refs", List[str], field(default=None)),
            ("include", bool, field(default=None)),
        ],
    ) = None,
    vcenter_parking_vnic_pg: str = None,
    vcenters: List[
        make_dataclass(
            "vcenters",
            [
                ("vcenter_ref", str),
                (
                    "clusters",
                    List[
                        make_dataclass(
                            "clusters",
                            [
                                ("cluster_id", str, field(default=None)),
                                ("override_vsphere_ha", bool, field(default=None)),
                                ("vmg_name", str, field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                (
                    "nsxt_clusters",
                    make_dataclass(
                        "nsxt_clusters",
                        [
                            ("cluster_ids", List[str], field(default=None)),
                            ("include", bool, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "nsxt_datastores",
                    make_dataclass(
                        "nsxt_datastores",
                        [
                            ("ds_ids", List[str], field(default=None)),
                            ("include", bool, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "nsxt_hosts",
                    make_dataclass(
                        "nsxt_hosts",
                        [
                            ("host_ids", List[str], field(default=None)),
                            ("include", bool, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                ("vcenter_folder", str, field(default=None)),
            ],
        )
    ] = None,
    vcpus_per_se: int = None,
    vip_asg: make_dataclass(
        "vip_asg",
        [
            (
                "configuration",
                make_dataclass(
                    "configuration",
                    [
                        (
                            "zones",
                            List[
                                make_dataclass(
                                    "zones",
                                    [
                                        ("availability_zone", str, field(default=None)),
                                        ("fip_capable", bool, field(default=None)),
                                        ("subnet_uuid", str, field(default=None)),
                                    ],
                                )
                            ],
                            field(default=None),
                        )
                    ],
                ),
                field(default=None),
            ),
            (
                "policy",
                make_dataclass(
                    "policy",
                    [
                        ("dns_cooldown", int, field(default=None)),
                        ("max_size", int, field(default=None)),
                        ("min_size", int, field(default=None)),
                        ("suspend", bool, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    vnic_dhcp_ip_check_interval: int = None,
    vnic_dhcp_ip_max_retries: int = None,
    vnic_ip_delete_interval: int = None,
    vnic_probe_interval: int = None,
    vnic_rpc_retry_interval: int = None,
    vnicdb_cmd_history_size: int = None,
    vs_host_redundancy: bool = None,
    vs_scalein_timeout: int = None,
    vs_scalein_timeout_for_upgrade: int = None,
    vs_scaleout_timeout: int = None,
    vs_se_scaleout_additional_wait_time: int = None,
    vs_se_scaleout_ready_timeout: int = None,
    vs_switchover_timeout: int = None,
    vss_placement: make_dataclass(
        "vss_placement",
        [
            ("core_nonaffinity", int, field(default=None)),
            ("num_subcores", int, field(default=None)),
        ],
    ) = None,
    vss_placement_enabled: bool = None,
    waf_mempool: bool = None,
    waf_mempool_size: int = None,
) -> Dict[str, Any]:
    """
    None
        None

    Args:
        resource_id(str):
            Alb.service_engine_group unique ID.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

        accelerated_networking(bool, Optional):
            Enable accelerated networking option for Azure SE. Accelerated networking enables single root I/O virtualization (SR-IOV) to a SE VM. This improves networking performance. Field introduced in 17.2.14,18.1.5,18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        active_standby(bool, Optional):
            Service Engines in active/standby mode for HA failover. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        aggressive_failure_detection(bool, Optional):
            Enable aggressive failover configuration for ha. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        algo(str, Optional):
            In compact placement, Virtual Services are placed on existing SEs until max_vs_per_se limit is reached. Enum options - PLACEMENT_ALGO_PACKED, PLACEMENT_ALGO_DISTRIBUTED. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        allow_burst(bool, Optional):
            Allow SEs to be created using burst license. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        app_cache_percent(int, Optional):
            A percent value of total SE memory reserved for applicationcaching. This is an SE bootup property and requires SE restart.Requires SE Reboot. Allowed values are 0 - 100. Special values are 0- disable. Field introduced in 18.2.3. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Special default for Essentials edition is 0, Basic edition is 0, Enterprise is 10. Defaults to None.

        app_cache_threshold(int, Optional):
            The max memory that can be allocated for the app cache. This value will act as an upper bound on the cache size specified in app_cache_percent. Special values are 0- disable. Field introduced in 20.1.1. Unit is GB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        app_learning_memory_percent(int, Optional):
            A percent value of total SE memory reserved for Application learning. This is an SE bootup property and requires SE restart. Allowed values are 0 - 10. Field introduced in 18.2.3. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        archive_shm_limit(int, Optional):
            Amount of SE memory in GB until which shared memory is collected in core archive. Field introduced in 17.1.3. Unit is GB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        async_ssl(bool, Optional):
            SSL handshakes will be handled by dedicated SSL Threads.Requires SE Reboot. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        async_ssl_threads(int, Optional):
            Number of Async SSL threads per se_dp.Requires SE Reboot. Allowed values are 1-16. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        auto_rebalance(bool, Optional):
            If set, Virtual Services will be automatically migrated when load on an SE is less than minimum or more than maximum thresholds. Only Alerts are generated when the auto_rebalance is not set. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        auto_rebalance_capacity_per_se(List[int], Optional):
            Capacities of SE for auto rebalance for each criteria. Field introduced in 17.2.4. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        auto_rebalance_criteria(List[str], Optional):
            Set of criteria for SE Auto Rebalance. Enum options - SE_AUTO_REBALANCE_CPU, SE_AUTO_REBALANCE_PPS, SE_AUTO_REBALANCE_MBPS, SE_AUTO_REBALANCE_OPEN_CONNS, SE_AUTO_REBALANCE_CPS. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        auto_rebalance_interval(int, Optional):
            Frequency of rebalance, if 'Auto rebalance' is enabled. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        auto_redistribute_active_standby_load(bool, Optional):
            Redistribution of virtual services from the takeover SE to the replacement SE can cause momentary traffic loss. If the auto-redistribute load option is left in its default off state, any desired rebalancing requires calls to REST API. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        availability_zone_refs(List[str], Optional):
            Availability zones for Virtual Service High Availability. It is a reference to an object of type AvailabilityZone. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        baremetal_dispatcher_handles_flows(bool, Optional):
            Control if dispatcher core also handles TCP flows in baremetal SE. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        bgp_peer_monitor_failover_enabled(bool, Optional):
            Enable BGP peer monitoring based failover. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        bgp_state_update_interval(int, Optional):
            BGP peer state update interval. Allowed values are 5-100. Field introduced in 17.2.14,18.1.5,18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        buffer_se(int, Optional):
            Excess Service Engine capacity provisioned for HA failover. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        cloud_ref(str, Optional):
             It is a reference to an object of type Cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        compress_ip_rules_for_each_ns_subnet(bool, Optional):
            Compress IP rules into a single subnet based IP rule for each north-south IPAM subnet configured in PCAP mode in OpenShift/Kubernetes node. Field introduced in 18.2.9, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        config_debugs_on_all_cores(bool, Optional):
            Enable config debugs on all cores of SE. Field introduced in 17.2.13,18.1.5,18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        configpb_attributes(dict[str, Any], Optional):
            configpb_attributes. Defaults to None.

            * version (int, Optional):
                Protobuf version number. Gets incremented if there is se Diff of federated diff in config pbs.This field will be a monotonically increasing number indicating the number of Config Update operations. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

        connection_memory_percentage(int, Optional):
            Percentage of memory for connection state. This will come at the expense of memory used for HTTP in-memory cache. Allowed values are 10-90. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        core_shm_app_cache(bool, Optional):
            Include shared memory for app cache in core file.Requires SE Reboot. Field introduced in 18.2.8, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        core_shm_app_learning(bool, Optional):
            Include shared memory for app learning in core file.Requires SE Reboot. Field introduced in 18.2.8, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        cpu_reserve(bool, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        cpu_socket_affinity(bool, Optional):
            Allocate all the CPU cores for the Service Engine Virtual Machines  on the same CPU socket. Applicable only for vCenter Cloud. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        custom_securitygroups_data(List[str], Optional):
            Custom Security Groups to be associated with data vNics for SE instances in OpenStack and AWS Clouds. Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        custom_securitygroups_mgmt(List[str], Optional):
            Custom Security Groups to be associated with management vNic for SE instances in OpenStack and AWS Clouds. Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        custom_tag(List[dict[str, Any]], Optional):
            Custom tag will be used to create the tags for SE instance in AWS. Note this is not the same as the prefix for SE name. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * tag_key (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * tag_val (str, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        data_network_id(str, Optional):
            Subnet used to spin up the data nic for Service Engines, used only for Azure cloud. Overrides the cloud level setting for Service Engine subnet. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        datascript_timeout(int, Optional):
            Number of instructions before datascript times out. Allowed values are 0-100000000. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        deactivate_ipv6_discovery(bool, Optional):
            If activated, IPv6 address and route discovery are deactivated.Requires SE reboot. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        deactivate_kni_filtering_at_dispatcher(bool, Optional):
            Deactivate filtering of packets to KNI interface. To be used under surveillance of Avi Support. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dedicated_dispatcher_core(bool, Optional):
            Dedicate the core that handles packet receive/transmit from the network to just the dispatching function. Don't use it for TCP/IP and SSL functions. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        description(str, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disable_avi_securitygroups(bool, Optional):
            By default, Avi creates and manages security groups along with custom sg provided by user. Set this to True to disallow Avi to create and manage new security groups. Avi will only make use of custom security groups provided by user. This option is supported for AWS and OpenStack cloud types. Field introduced in 17.2.13,18.1.4,18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disable_csum_offloads(bool, Optional):
            Stop using TCP/UDP and IP checksum offload features of NICs. Field introduced in 17.1.14, 17.2.5, 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disable_flow_probes(bool, Optional):
            Disable Flow Probes for Scaled out VS'es. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        disable_gro(bool, Optional):
            Disable Generic Receive Offload (GRO) in DPDK poll-mode driver packet receive path.  GRO is on by default on NICs that do not support LRO (Large Receive Offload) or do not gain performance boost from LRO. Field introduced in 17.2.5, 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disable_se_memory_check(bool, Optional):
            If set, disable the config memory check done in service engine. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disable_tso(bool, Optional):
            Disable TCP Segmentation Offload (TSO) in DPDK poll-mode driver packet transmit path. TSO is on by default on NICs that support it. Field introduced in 17.2.5, 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        disk_per_se(int, Optional):
            Amount of disk space for each of the Service Engine virtual machines. Unit is GB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        distribute_load_active_standby(bool, Optional):
            Use both the active and standby Service Engines for Virtual Service placement in the legacy active standby HA mode. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        distribute_queues(bool, Optional):
            Distributes queue ownership among cores so multiple cores handle dispatcher duties. Requires SE Reboot. Deprecated from 18.2.8, instead use max_queues_per_vnic. Field introduced in 17.2.8. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        distribute_vnics(bool, Optional):
            Distributes vnic ownership among cores so multiple cores handle dispatcher duties.Requires SE Reboot. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        downstream_send_timeout(int, Optional):
            Timeout for downstream to become writable. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_aggressive_deq_interval_msec(int, Optional):
            Dequeue interval for receive queue from se_dp in aggressive mode. Allowed values are 1-1000. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_aggressive_enq_interval_msec(int, Optional):
            Enqueue interval for request queue to se_dp in aggressive mode. Allowed values are 1-1000. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_aggressive_hb_frequency(int, Optional):
            Frequency of SE - SE HB messages when aggressive failure mode detection is enabled. Field introduced in 20.1.3. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_aggressive_hb_timeout_count(int, Optional):
            Consecutive HB failures after which failure is reported to controller,when aggressive failure mode detection is enabled. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_deq_interval_msec(int, Optional):
            Dequeue interval for receive queue from se_dp. Allowed values are 1-1000. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_enq_interval_msec(int, Optional):
            Enqueue interval for request queue to se_dp. Allowed values are 1-1000. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_hb_frequency(int, Optional):
            Frequency of SE - SE HB messages when aggressive failure mode detection is not enabled. Field introduced in 20.1.3. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dp_hb_timeout_count(int, Optional):
            Consecutive HB failures after which failure is reported to controller, when aggressive failure mode detection is not enabled. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        dpdk_gro_timeout_interval(int, Optional):
            The timeout for GRO coalescing interval. 0 indicates non-timer based GRO. Allowed values are 0-900. Field introduced in 22.1.1. Unit is MICROSECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        enable_gratarp_permanent(bool, Optional):
            Enable GratArp for VIP_IP. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        enable_hsm_log(bool, Optional):
            Enable HSM luna engine logs. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        enable_hsm_priming(bool, Optional):
            (This is a beta feature). Enable HSM key priming. If enabled, key handles on the hsm will be synced to SE before processing client connections. Field introduced in 17.2.7, 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        enable_multi_lb(bool, Optional):
            Applicable only for Azure cloud with Basic SKU LB. If set, additional Azure LBs will be automatically created if resources in existing LB are exhausted. Field introduced in 17.2.10, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        enable_pcap_tx_ring(bool, Optional):
            Enable TX ring support in pcap mode of operation. TSO feature is not supported with TX Ring enabled. Deprecated from 18.2.8, instead use pcap_tx_mode. Requires SE Reboot. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ephemeral_portrange_end(int, Optional):
            End local ephemeral port number for outbound connections. Field introduced in 17.2.13, 18.1.5, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ephemeral_portrange_start(int, Optional):
            Start local ephemeral port number for outbound connections. Field introduced in 17.2.13, 18.1.5, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        extra_config_multiplier(float, Optional):
            Multiplier for extra config to support large VS/Pool config. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        extra_shared_config_memory(int, Optional):
            Extra config memory to support large Geo DB configuration. Field introduced in 17.1.1. Unit is MB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        flow_table_new_syn_max_entries(int, Optional):
            Maximum number of flow table entries that have not completed TCP three-way handshake yet. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        free_list_size(int, Optional):
            Number of entries in the free list. Field introduced in 17.2.10, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        gcp_config(dict[str, Any], Optional):
            gcp_config. Defaults to None.

            * backend_data_vpc_network_name (str, Optional):
                Service Engine Backend Data Network Name, used only for GCP cloud.Overrides the cloud level setting for Backend Data Network in GCP Two Arm Mode. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * backend_data_vpc_project_id (str, Optional):
                Project ID of the Service Engine Backend Data Network. By default, Service Engine Project ID will be used. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * backend_data_vpc_subnet_name (str, Optional):
                Service Engine Backend Data Subnet Name, used only for GCP cloud.Overrides the cloud level setting for Backend Data Subnet in GCP Two Arm Mode. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        gratarp_permanent_periodicity(int, Optional):
            GratArp periodicity for VIP-IP. Allowed values are 5-30. Field introduced in 18.2.3. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        grpc_channel_connect_timeout(int, Optional):
            Timeout in seconds that SE waits for a grpc channel to connect to server, before it retries. Allowed values are 5-45. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ha_mode(str, Optional):
            High Availability mode for all the Virtual Services using this Service Engine group. Enum options - HA_MODE_SHARED_PAIR, HA_MODE_SHARED, HA_MODE_LEGACY_ACTIVE_STANDBY. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- HA_MODE_LEGACY_ACTIVE_STANDBY), Basic edition(Allowed values- HA_MODE_LEGACY_ACTIVE_STANDBY), Enterprise with Cloud Services edition. Special default for Essentials edition is HA_MODE_LEGACY_ACTIVE_STANDBY, Basic edition is HA_MODE_LEGACY_ACTIVE_STANDBY, Enterprise is HA_MODE_SHARED. Defaults to None.

        handle_per_pkt_attack(bool, Optional):
            Configuration to handle per packet attack handling.For example, DNS Reflection Attack is a type of attack where a response packet is sent to the DNS VS.This configuration tells if such packets should be dropped without further processing. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        hardwaresecuritymodulegroup_ref(str, Optional):
             It is a reference to an object of type HardwareSecurityModuleGroup. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        heap_minimum_config_memory(int, Optional):
            Minimum required heap memory to apply any configuration. Allowed values are 0-100. Field introduced in 18.1.2. Unit is MB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        hm_on_standby(bool, Optional):
            Enable active health monitoring from the standby SE for all placed virtual services. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Special default for Essentials edition is false, Basic edition is false, Enterprise is True. Defaults to None.

        host_attribute_key(str, Optional):
            Key of a (Key, Value) pair identifying a label for a set of Nodes usually in Container Clouds. Needs to be specified together with host_attribute_value. SEs can be configured differently including HA modes across different SE Groups. May also be used for isolation between different classes of VirtualServices. VirtualServices' SE Group may be specified via annotations/labels. A OpenShift/Kubernetes namespace maybe annotated with a matching SE Group label as openshift.io/node-selector  apptype=prod. When multiple SE Groups are used in a Cloud with host attributes specified,just a single SE Group can exist as a match-all SE Group without a host_attribute_key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        host_attribute_value(str, Optional):
            Value of a (Key, Value) pair identifying a label for a set of Nodes usually in Container Clouds. Needs to be specified together with host_attribute_key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        host_gateway_monitor(bool, Optional):
            Enable the host gateway monitor when service engine is deployed as docker container. Disabled by default. Field introduced in 17.2.4. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        http_rum_console_log(bool, Optional):
            Enable Javascript console logs on the client browser when collecting client insights. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        http_rum_min_content_length(int, Optional):
            Minimum response size content length to sample for client insights. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 64), Basic edition(Allowed values- 64), Enterprise with Cloud Services edition. Defaults to None.

        hybrid_rss_mode(bool, Optional):
            Toggles SE hybrid only mode of operation in DPDK mode with RSS configured;where-in each SE datapath instance operates as an independent standalonehybrid instance performing both dispatcher and proxy function. Requires reboot. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        hypervisor(str, Optional):
            Override default hypervisor. Enum options - DEFAULT, VMWARE_ESX, KVM, VMWARE_VSAN, XEN. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ignore_docker_mac_change(bool, Optional):
            Ignore docker mac change. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ignore_rtt_threshold(int, Optional):
            Ignore RTT samples if it is above threshold. Field introduced in 17.1.6,17.2.2. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ingress_access_data(str, Optional):
            Program SE security group ingress rules to allow VIP data access from remote CIDR type. Enum options - SG_INGRESS_ACCESS_NONE, SG_INGRESS_ACCESS_ALL, SG_INGRESS_ACCESS_VPC. Field introduced in 17.1.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ingress_access_mgmt(str, Optional):
            Program SE security group ingress rules to allow SSH/ICMP management access from remote CIDR type. Enum options - SG_INGRESS_ACCESS_NONE, SG_INGRESS_ACCESS_ALL, SG_INGRESS_ACCESS_VPC. Field introduced in 17.1.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        instance_flavor(str, Optional):
            Instance/Flavor name for SE instance. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        instance_flavor_info(dict[str, Any], Optional):
            instance_flavor_info. Defaults to None.

            * cost (str, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * disk_gb (int, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enhanced_nw (bool, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * id (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * is_recommended (bool, Optional):
                If a vm flavor is recommended for requested se_usage_type.Set to True if the chosen VM flavor is recommended for requested se_usage_type.Else set to False. Field introduced in 18.1.4, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_ip6s_per_nic (int, Optional):
                Maximum number of IPv6 addresses that can be configured per NIC. Field introduced in 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_ips_per_nic (int, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * max_nics (int, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * meta (List[dict[str, Any]], Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * key (str):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * value (str):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * name (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * public (bool, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * ram_mb (int, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vcpus (int, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        iptables(List[dict[str, Any]], Optional):
            Iptable Rules. Maximum of 128 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * chain (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * rules (List[dict[str, Any]], Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * action (str):
                     Enum options - ACCEPT, DROP, REJECT, DNAT, MASQUERADE. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * dnat_ip (dict[str, Any], Optional):
                    dnat_ip

                    * addr (str):
                        IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * type (str):
                         Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * dst_ip (dict[str, Any], Optional):
                    dst_ip

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * dst_port (dict[str, Any], Optional):
                    dst_port

                    * end (int):
                        TCP/UDP port range end (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * start (int):
                        TCP/UDP port range start (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * input_interface (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * output_interface (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * proto (str, Optional):
                     Enum options - PROTO_TCP, PROTO_UDP, PROTO_ICMP, PROTO_ALL. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * src_ip (dict[str, Any], Optional):
                    src_ip

                    * ip_addr (dict[str, Any]):
                        ip_addr

                        * addr (str):
                            IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                        * type (str):
                             Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * mask (int):
                         Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * src_port (dict[str, Any], Optional):
                    src_port

                    * end (int):
                        TCP/UDP port range end (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * start (int):
                        TCP/UDP port range start (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * tag (str, Optional):
                     Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * table (str):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        kni_allowed_server_ports(List[dict[str, Any]], Optional):
            Port ranges for any servers running in inband LinuxServer clouds. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * protocol (str):
                Protocol associated with port range. Enum options - KNI_PROTO_TCP, KNI_PROTO_UDP. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * range (dict[str, Any]):
                range

                * end (int):
                    TCP/UDP port range end (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * start (int):
                    TCP/UDP port range start (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        l7_conns_per_core(int, Optional):
            Number of L7 connections that can be cached per core. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        l7_resvd_listen_conns_per_core(int, Optional):
            Number of reserved L7 listener connections per core. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        labels(List[dict[str, Any]], Optional):
            Labels associated with this SE group. Field introduced in 20.1.1. Maximum of 1 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * value (str, Optional):
                Value. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        lbaction_num_requests_to_dispatch(int, Optional):
            Number of requests to dispatch from the request. queue at a regular interval. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        lbaction_rq_per_request_max_retries(int, Optional):
            Maximum retries per request in the request queue. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        least_load_core_selection(bool, Optional):
            Select core with least load for new flow. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        license_tier(str, Optional):
            Specifies the license tier which would be used. This field by default inherits the value from cloud. Enum options - ENTERPRISE_16, ENTERPRISE, ENTERPRISE_18, BASIC, ESSENTIALS, ENTERPRISE_WITH_CLOUD_SERVICES. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        license_type(str, Optional):
            If no license type is specified then default license enforcement for the cloud type is chosen. Enum options - LIC_BACKEND_SERVERS, LIC_SOCKETS, LIC_CORES, LIC_HOSTS, LIC_SE_BANDWIDTH, LIC_METERED_SE_BANDWIDTH. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_compress_logs(bool, Optional):
            Flag to indicate if log files are compressed upon full on the Service Engine. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_debug_enabled(bool, Optional):
            Enable debug logs by default on Service Engine. This includes all other debugging logs. Debug logs can also be explcitly enabled from the CLI shell. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_file_sz_appl(int, Optional):
            Maximum application log file size before rollover. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_file_sz_conn(int, Optional):
            Maximum connection log file size before rollover. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_file_sz_debug(int, Optional):
            Maximum debug log file size before rollover. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_file_sz_event(int, Optional):
            Maximum event log file size before rollover. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_log_storage_min_sz(int, Optional):
            Minimum storage allocated for logs irrespective of memory and cores. Field introduced in 21.1.1. Unit is MB. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_max_concurrent_rsync(int, Optional):
            Maximum concurrent rsync requests initiated from log-agent to the Controller. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_max_storage_excess_percent(int, Optional):
            Excess percentage threshold of disk size to trigger cleanup of logs on the Service Engine. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_max_storage_ignore_percent(float, Optional):
            Maximum storage on the disk not allocated for logs on the Service Engine. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_min_storage_per_vs(int, Optional):
            Minimum storage allocated to any given VirtualService on the Service Engine. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_sleep_interval(int, Optional):
            Internal timer to stall log-agent and prevent it from hogging CPU cycles on the Service Engine. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_trace_enabled(bool, Optional):
            Enable trace logs by default on Service Engine. Configuration operations are logged along with other important logs by Service Engine. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_agent_unknown_vs_timer(int, Optional):
            Timeout to purge unknown Virtual Service logs from the Service Engine. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        log_disksz(int, Optional):
            Maximum disk capacity (in MB) to be allocated to an SE. This is exclusively used for debug and log data. Unit is MB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        log_malloc_failure(bool, Optional):
            SE will log memory allocation related failure to the se_trace file, wherever available. Field introduced in 20.1.2. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- true), Basic edition(Allowed values- true), Enterprise with Cloud Services edition. Defaults to None.

        log_message_max_file_list_size(int, Optional):
            Maximum number of file names in a log message. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        markers(List[dict[str, Any]], Optional):
            List of labels to be used for granular RBAC. Field introduced in 20.1.7. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

            * key (str):
                Key for filter match. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * values (List[str], Optional):
                Values for filter match. Multiple values will be evaluated as OR. Example  key = value1 OR key = value2. Behavior for match is key = * if this field is empty. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        max_concurrent_external_hm(int, Optional):
            Maximum number of external health monitors that can run concurrently in a service engine. This helps control the CPU and memory use by external health monitors. Special values are 0- Value will be internally calculated based on cpu and memory. Field introduced in 18.2.7. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_cpu_usage(int, Optional):
            When CPU usage on an SE exceeds this threshold, Virtual Services hosted on this SE may be rebalanced to other SEs to reduce load. A new SE may be created as part of this process. Allowed values are 40-90. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_memory_per_mempool(int, Optional):
            Max bytes that can be allocated in a single mempool. Field introduced in 18.1.5. Unit is MB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_num_se_dps(int, Optional):
            Configures the maximum number of se_dp processes that handles traffic. If not configured, defaults to the number of CPUs on the SE. If decreased, it will only take effect after SE reboot. Allowed values are 1-128. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Defaults to None.

        max_public_ips_per_lb(int, Optional):
            Applicable to Azure platform only. Maximum number of public IPs per Azure LB. . Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_queues_per_vnic(int, Optional):
            Maximum number of queues per vnic Setting to '0' utilises all queues that are distributed across dispatcher cores. Allowed values are 0,1,2,4,8,16. Field introduced in 18.2.7, 20.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 1), Basic edition(Allowed values- 1), Enterprise with Cloud Services edition. Defaults to None.

        max_rules_per_lb(int, Optional):
            Applicable to Azure platform only. Maximum number of rules per Azure LB. . Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_scaleout_per_vs(int, Optional):
            Maximum number of active Service Engines for the Virtual Service. Allowed values are 1-64. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_se(int, Optional):
            Maximum number of Services Engines in this group. Allowed values are 0-1000. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        max_skb_frags(int, Optional):
            Maximum of number of 4 KB pages allocated to the Linux kernel GRO subsystem for packet coalescing. This parameter is limited to supported kernels only. Requires SE Reboot. Allowed values are 1-17. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        max_vs_per_se(int, Optional):
            Maximum number of Virtual Services that can be placed on a single Service Engine. Allowed values are 1-1000. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        mem_reserve(bool, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        memory_for_config_update(int, Optional):
            Indicates the percent of memory reserved for config updates. Allowed values are 0-100. Field introduced in 18.1.2. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        memory_per_se(int, Optional):
            Amount of memory for each of the Service Engine virtual machines. Changes to this setting do not affect existing SEs. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        mgmt_network_ref(str, Optional):
            Management network to use for Avi Service Engines. It is a reference to an object of type Network. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        mgmt_subnet(dict[str, Any], Optional):
            mgmt_subnet. Defaults to None.

            * ip_addr (dict[str, Any]):
                ip_addr

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mask (int):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        min_cpu_usage(int, Optional):
            When CPU usage on an SE falls below the minimum threshold, Virtual Services hosted on the SE may be consolidated onto other underutilized SEs. After consolidation, unused Service Engines may then be eligible for deletion. . Allowed values are 20-60. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        min_scaleout_per_vs(int, Optional):
            Minimum number of active Service Engines for the Virtual Service. Allowed values are 1-64. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        min_se(int, Optional):
            Minimum number of Services Engines in this group (relevant for SE AutoRebalance only). Allowed values are 0-1000. Field introduced in 17.2.13,18.1.3,18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        minimum_connection_memory(int, Optional):
            Indicates the percent of memory reserved for connections. Allowed values are 0-100. Field introduced in 18.1.2. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        n_log_streaming_threads(int, Optional):
            Number of threads to use for log streaming. Allowed values are 1-100. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        netlink_poller_threads(int, Optional):
            Number of threads to poll for netlink messages excluding the thread for default namespace. Requires SE Reboot. Allowed values are 1-32. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        netlink_sock_buf_size(int, Optional):
            Socket buffer size for the netlink sockets. Requires SE Reboot. Allowed values are 1-128. Field introduced in 21.1.1. Unit is MEGA_BYTES. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ngx_free_connection_stack(bool, Optional):
            Free the connection stack. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        non_significant_log_throttle(int, Optional):
            This setting limits the number of non-significant logs generated per second per core on this SE. Default is 100 logs per second. Set it to zero (0) to deactivate throttling. Field introduced in 17.1.3. Unit is PER_SECOND. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ns_helper_deq_interval_msec(int, Optional):
            Dequeue interval for receive queue from NS HELPER. Allowed values are 1-1000. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ntp_sync_fail_event(bool, Optional):
            Toggle SE NTP synchronization failure events generation. Disabled by default. Field introduced in 22.1.2. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        ntp_sync_status_interval(int, Optional):
            Configures the interval at which SE synchronization status with NTP server(s) is verified. A value of zero disables SE NTP synchronization status validation. Allowed values are 120-900. Special values are 0- disable. Field introduced in 22.1.2. Unit is SEC. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        num_dispatcher_cores(int, Optional):
            Number of dispatcher cores (0,1,2,4,8 or 16). If set to 0, then number of dispatcher cores is deduced automatically.Requires SE Reboot. Allowed values are 0,1,2,4,8,16. Field introduced in 17.2.12, 18.1.3, 18.2.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Defaults to None.

        num_dispatcher_queues(int, Optional):
            Number of queues to each dispatcher. Allowed values are 1-2. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        num_flow_cores_sum_changes_to_ignore(int, Optional):
            Number of changes in num flow cores sum to ignore. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        objsync_config(dict[str, Any], Optional):
            objsync_config. Defaults to None.

            * objsync_cpu_limit (int, Optional):
                SE CPU limit for InterSE Object Distribution. Allowed values are 15-80. Field introduced in 20.1.3. Unit is PERCENT. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * objsync_hub_elect_interval (int, Optional):
                Hub election interval for InterSE Object Distribution. Allowed values are 30-300. Field introduced in 20.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * objsync_reconcile_interval (int, Optional):
                Reconcile interval for InterSE Object Distribution. Allowed values are 1-120. Field introduced in 20.1.3. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        objsync_port(int, Optional):
            TCP port on SE management interface for InterSE Object Distribution. Supported only for externally managed security groups. Not supported on full access deployments. Requires SE reboot. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        openstack_availability_zones(List[str], Optional):
             Field introduced in 17.1.1. Maximum of 5 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        openstack_mgmt_network_name(str, Optional):
            Avi Management network name. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        openstack_mgmt_network_uuid(str, Optional):
            Management network UUID. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        os_reserved_memory(int, Optional):
            Amount of extra memory to be reserved for use by the Operating System on a Service Engine. Unit is MB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        pcap_tx_mode(str, Optional):
            Determines the PCAP transmit mode of operation. Requires SE Reboot. Enum options - PCAP_TX_AUTO, PCAP_TX_SOCKET, PCAP_TX_RING. Field introduced in 18.2.8, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        pcap_tx_ring_rd_balancing_factor(int, Optional):
            In PCAP mode, reserve a configured portion of TX ring resources for itself and the remaining portion for the RX ring to achieve better balance in terms of queue depth. Requires SE Reboot. Allowed values are 10-100. Field introduced in 20.1.3. Unit is PERCENT. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        per_app(bool, Optional):
            Per-app SE mode is designed for deploying dedicated load balancers per app (VS). In this mode, each SE is limited to a max of 2 VSs. vCPUs in per-app SEs count towards licensing usage at 25% rate. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        per_vs_admission_control(bool, Optional):
            Enable/Disable per VS level admission control.Enabling this feature will cause the connection and packet throttling on a particular VS that has high packet buffer consumption. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        placement_mode(str, Optional):
            If placement mode is 'Auto', Virtual Services are automatically placed on Service Engines. Enum options - PLACEMENT_MODE_AUTO. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        realtime_se_metrics(dict[str, Any], Optional):
            realtime_se_metrics. Defaults to None.

            * duration (int, Optional):
                Real time metrics collection duration in minutes. 0 for infinite. Special values are 0 - infinite. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * enabled (bool):
                Enables real time metrics collection.  When deactivated, 6 hour view is the most granular the system will track. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        reboot_on_panic(bool, Optional):
            Reboot the VM or host on kernel panic. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        replay_vrf_routes_interval(int, Optional):
            Routes in VRF are replayed at the specified interval. This should be increased if there are large number of routes. Allowed values are 0-3000. Field introduced in 22.1.3. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        resync_time_interval(int, Optional):
            Time interval to re-sync SE's time with wall clock time. Allowed values are 8-600000. Field introduced in 20.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        sdb_flush_interval(int, Optional):
            SDB pipeline flush interval. Allowed values are 1-10000. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        sdb_pipeline_size(int, Optional):
            SDB pipeline size. Allowed values are 1-10000. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        sdb_scan_count(int, Optional):
            SDB scan count. Allowed values are 1-1000. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_bandwidth_type(str, Optional):
            Select the SE bandwidth for the bandwidth license. Enum options - SE_BANDWIDTH_UNLIMITED, SE_BANDWIDTH_25M, SE_BANDWIDTH_200M, SE_BANDWIDTH_1000M, SE_BANDWIDTH_10000M. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- SE_BANDWIDTH_UNLIMITED), Basic edition(Allowed values- SE_BANDWIDTH_UNLIMITED), Enterprise with Cloud Services edition. Defaults to None.

        se_delayed_flow_delete(bool, Optional):
            Delay the cleanup of flowtable entry. To be used under surveillance of Avi Support. Field introduced in 20.1.2. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- true), Basic edition(Allowed values- true), Enterprise with Cloud Services edition. Defaults to None.

        se_deprovision_delay(int, Optional):
            Duration to preserve unused Service Engine virtual machines before deleting them. If traffic to a Virtual Service were to spike up abruptly, this SE would still be available to be utilized again rather than creating a new SE. If this value is set to 0, Controller will never delete any SEs and administrator has to manually cleanup unused SEs. Allowed values are 0-525600. Unit is MIN. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dos_profile(dict[str, Any], Optional):
            se_dos_profile. Defaults to None.

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

        se_dp_hm_drops(int, Optional):
            Internal only. Used to simulate SE - SE HB failure. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_if_state_poll_interval(int, Optional):
            Number of jiffies between polling interface state. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_isolation(bool, Optional):
            Toggle support to run SE datapath instances in isolation on exclusive CPUs. This improves latency and performance. However, this could reduce the total number of se_dp instances created on that SE instance. Supported for >= 8 CPUs. Requires SE reboot. Field introduced in 20.1.4. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_isolation_num_non_dp_cpus(int, Optional):
            Number of CPUs for non se-dp tasks in SE datapath isolation mode. Translates Total cpus minus 'num_non_dp_cpus' for datapath use. It is recommended to reserve an even number of CPUs for hyper-threaded processors. Requires SE reboot. Allowed values are 1-8. Special values are 0- auto. Field introduced in 20.1.4. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_log_nf_enqueue_percent(int, Optional):
            Internal buffer full indicator on the Service Engine beyond which the unfiltered logs are abandoned. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_log_udf_enqueue_percent(int, Optional):
            Internal buffer full indicator on the Service Engine beyond which the user filtered logs are abandoned. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_max_hb_version(int, Optional):
            The highest supported SE-SE Heartbeat protocol version. This version is reported by Secondary SE to Primary SE in Heartbeat response messages. Allowed values are 1-3. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_vnic_queue_stall_event_sleep(int, Optional):
            Time (in seconds) service engine waits for after generating a Vnic transmit queue stall event before resetting theNIC. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_vnic_queue_stall_threshold(int, Optional):
            Number of consecutive transmit failures to look for before generating a Vnic transmit queue stall event. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_vnic_queue_stall_timeout(int, Optional):
            Time (in milliseconds) to wait for network/NIC recovery on detecting a transmit queue stall after which service engine resets the NIC. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_vnic_restart_on_queue_stall_count(int, Optional):
            Number of consecutive transmit queue stall events in se_dp_vnic_stall_se_restart_window to look for before restarting SE. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dp_vnic_stall_se_restart_window(int, Optional):
            Window of time (in seconds) during which se_dp_vnic_restart_on_queue_stall_count number of consecutive stalls results in a SE restart. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dpdk_pmd(int, Optional):
            Determines if DPDK pool mode driver should be used or not   0  Automatically determine based on hypervisor/NIC type 1  Unconditionally use DPDK poll mode driver 2  Don't use DPDK poll mode driver.Requires SE Reboot. Allowed values are 0-2. Field introduced in 18.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_dump_core_on_assert(bool, Optional):
            Enable core dump on assert. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_emulated_cores(int, Optional):
            Use this to emulate more/less cpus than is actually available. One datapath process is started for each core. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Defaults to None.

        se_flow_probe_retries(int, Optional):
            Flow probe retry count if no replies are received.Requires SE Reboot. Allowed values are 0-5. Field introduced in 18.1.4, 18.2.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_flow_probe_retry_timer(int, Optional):
            Timeout in milliseconds for flow probe retries.Requires SE Reboot. Allowed values are 20-50. Field introduced in 18.2.5. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_group_analytics_policy(dict[str, Any], Optional):
            se_group_analytics_policy. Defaults to None.

            * metrics_event_thresholds (List[dict[str, Any]], Optional):
                Thresholds for various events generated by metrics system. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * metrics_event_threshold_type (str):
                    Type of the metrics event threshold. This value will decide which metric rule (or rules) use configured thresholds. Enum options - THRESHOLD_TYPE_STATIC, SE_CPU_THRESHOLD, SE_MEM_THRESHOLD, SE_DISK_THRESHOLD, CONTROLLER_CPU_THRESHOLD, CONTROLLER_MEM_THRESHOLD, CONTROLLER_DISK_THRESHOLD. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * reset_threshold (float, Optional):
                    This value is used to reset the event state machine. Allowed values are 0-100. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

                * watermark_thresholds (List[int], Optional):
                    Threshold value for which event in raised. There can be multiple thresholds defined.Health score degrades when the the target is higher than this threshold. Allowed values are 0-100. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        se_hyperthreaded_mode(str, Optional):
            Controls the distribution of SE data path processes on CPUs which support hyper-threading. Requires hyper-threading to be enabled at host level. Requires SE Reboot. For more details please refer to SE placement KB. Enum options - SE_CPU_HT_AUTO, SE_CPU_HT_SPARSE_DISPATCHER_PRIORITY, SE_CPU_HT_SPARSE_PROXY_PRIORITY, SE_CPU_HT_PACKED_CORES. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_ip_encap_ipc(int, Optional):
            Determines if SE-SE IPC messages are encapsulated in an IP header       0        Automatically determine based on hypervisor type    1        Use IP encap unconditionally    ~[0,1]   Don't use IP encapRequires SE Reboot. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_kni_burst_factor(int, Optional):
            This knob controls the resource availability and burst size used between SE datapath and KNI. This helps in minimising packet drops when there is higher KNI traffic (non-VIP traffic from and to Linux). The factor takes the following values      0-default.     1-doubles the burst size and KNI resources.     2-quadruples the burst size and KNI resources. Allowed values are 0-2. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_l3_encap_ipc(int, Optional):
            Determines if SE-SE IPC messages use SE interface IP instead of VIP        0        Automatically determine based on hypervisor type    1        Use SE interface IP unconditionally    ~[0,1]   Don't use SE interface IPRequires SE Reboot. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_log_buffer_app_blocking_dequeue(bool, Optional):
            Internal flag that blocks dataplane until all application logs are flushed to log-agent process. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_log_buffer_conn_blocking_dequeue(bool, Optional):
            Internal flag that blocks dataplane until all connection logs are flushed to log-agent process. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_log_buffer_events_blocking_dequeue(bool, Optional):
            Internal flag that blocks dataplane until all outstanding events are flushed to log-agent process. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_lro(bool, Optional):
            Enable or disable Large Receive Optimization for vnics.Supported on VMXnet3.Requires SE Reboot. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_mp_ring_retry_count(int, Optional):
            The retry count for the multi-producer enqueue before yielding the CPU. To be used under surveillance of Avi Support. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 500), Basic edition(Allowed values- 500), Enterprise with Cloud Services edition. Defaults to None.

        se_mtu(int, Optional):
            MTU for the VNICs of SEs in the SE group. Allowed values are 512-9000. Field introduced in 18.2.8, 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_name_prefix(str, Optional):
            Prefix to use for virtual machine name of Service Engines. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_packet_buffer_max(int, Optional):
            Internal use only. Used to artificially reduce the available number of packet buffers. Field introduced in 21.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        se_pcap_lookahead(bool, Optional):
            Enables lookahead mode of packet receive in PCAP mode. Introduced to overcome an issue with hv_netvsc driver. Lookahead mode attempts to ensure that application and kernel's view of the receive rings are consistent. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_pcap_pkt_count(int, Optional):
            Max number of packets the pcap interface can hold and if the value is 0 the optimum value will be chosen. The optimum value will be chosen based on SE-memory, Cloud Type and Number of Interfaces.Requires SE Reboot. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_pcap_pkt_sz(int, Optional):
            Max size of each packet in the pcap interface. Requires SE Reboot. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_pcap_qdisc_bypass(bool, Optional):
            Bypass the kernel's traffic control layer, to deliver packets directly to the driver. Enabling this feature results in egress packets not being captured in host tcpdump. Note   brief packet reordering or loss may occur upon toggle. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_pcap_reinit_frequency(int, Optional):
            Frequency in seconds at which periodically a PCAP reinit check is triggered. May be used in conjunction with the configuration pcap_reinit_threshold. (Valid range   15 mins - 12 hours, 0 - disables). Allowed values are 900-43200. Special values are 0- disable. Field introduced in 17.2.13, 18.1.3, 18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_pcap_reinit_threshold(int, Optional):
            Threshold for input packet receive errors in PCAP mode exceeding which a PCAP reinit is triggered. If not set, an unconditional reinit is performed. This value is checked every pcap_reinit_frequency interval. Field introduced in 17.2.13, 18.1.3, 18.2.1. Unit is METRIC_COUNT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_probe_port(int, Optional):
            TCP port on SE where echo service will be run. Field introduced in 17.2.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_rl_prop(dict[str, Any], Optional):
            se_rl_prop. Defaults to None.

            * msf_num_stages (int, Optional):
                Number of stages in msf rate limiter. Allowed values are 1-2. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * msf_stage_size (int, Optional):
                Each stage size in msf rate limiter. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        se_rum_sampling_nav_interval(int, Optional):
            Minimum time to wait on server between taking sampleswhen sampling the navigation timing data from the end user client. Field introduced in 18.2.6. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_rum_sampling_nav_percent(int, Optional):
            Percentage of navigation timing data from the end user client, used for sampling to get client insights. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_rum_sampling_res_interval(int, Optional):
            Minimum time to wait on server between taking sampleswhen sampling the resource timing data from the end user client. Field introduced in 18.2.6. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_rum_sampling_res_percent(int, Optional):
            Percentage of resource timing data from the end user client used for sampling to get client insight. Field introduced in 18.2.6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_sb_dedicated_core(bool, Optional):
            Sideband traffic will be handled by a dedicated core.Requires SE Reboot. Field introduced in 16.5.2, 17.1.9, 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_sb_threads(int, Optional):
            Number of Sideband threads per SE.Requires SE Reboot. Allowed values are 1-128. Field introduced in 16.5.2, 17.1.9, 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_thread_multiplier(int, Optional):
            Multiplier for SE threads based on vCPU. Allowed values are 1-10. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 1), Basic edition(Allowed values- 1), Enterprise with Cloud Services edition. Defaults to None.

        se_time_tracker_props(dict[str, Any], Optional):
            se_time_tracker_props. Defaults to None.

            * egress_audit_mode (str, Optional):
                Audit queueing latency from proxy to dispatcher. Enum options - SE_TT_AUDIT_OFF, SE_TT_AUDIT_ON, SE_TT_AUDIT_ON_WITH_EVENT. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * egress_threshold (int, Optional):
                Maximum egress latency threshold between dispatcher and proxy. Field introduced in 22.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * event_gen_window (int, Optional):
                Window for cumulative event generation. Field introduced in 22.1.1. Unit is SECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ingress_audit_mode (str, Optional):
                Audit queueing latency from dispatcher to proxy. Enum options - SE_TT_AUDIT_OFF, SE_TT_AUDIT_ON, SE_TT_AUDIT_ON_WITH_EVENT. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * ingress_threshold (int, Optional):
                Maximum ingress latency threshold between dispatcher and proxy. Field introduced in 22.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        se_tracert_port_range(dict[str, Any], Optional):
            se_tracert_port_range. Defaults to None.

            * end (int):
                TCP/UDP port range end (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * start (int):
                TCP/UDP port range start (inclusive). Allowed values are 1-65535. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        se_tunnel_mode(int, Optional):
            Determines if Direct Secondary Return (DSR) from secondary SE is active or not  0  Automatically determine based on hypervisor type. 1  Enable tunnel mode - DSR is unconditionally disabled. 2  Disable tunnel mode - DSR is unconditionally enabled. Tunnel mode can be enabled or disabled at run-time. Allowed values are 0-2. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 0), Basic edition(Allowed values- 0), Enterprise with Cloud Services edition. Defaults to None.

        se_tunnel_udp_port(int, Optional):
            UDP Port for tunneled packets from secondary to primary SE in Docker bridge mode.Requires SE Reboot. Field introduced in 17.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_tx_batch_size(int, Optional):
            Number of packets to batch for transmit to the nic. Requires SE Reboot. Field introduced in 18.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_txq_threshold(int, Optional):
            Once the TX queue of the dispatcher reaches this threshold, hardware queues are not polled for further packets. To be used under surveillance of Avi Support. Allowed values are 512-32768. Field introduced in 20.1.2. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 2048), Basic edition(Allowed values- 2048), Enterprise with Cloud Services edition. Defaults to None.

        se_udp_encap_ipc(int, Optional):
            Determines if SE-SE IPC messages are encapsulated in a UDP header  0  Automatically determine based on hypervisor type. 1  Use UDP encap unconditionally.Requires SE Reboot. Allowed values are 0-1. Field introduced in 17.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_use_dpdk(int, Optional):
            Determines if DPDK library should be used or not   0  Automatically determine based on hypervisor type 1  Use DPDK if PCAP is not enabled 2  Don't use DPDK. Allowed values are 0-2. Field introduced in 18.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_vnic_tx_sw_queue_flush_frequency(int, Optional):
            Configure the frequency in milliseconds of software transmit spillover queue flush when enabled. This is necessary to flush any packets in the spillover queue in the absence of a packet transmit in the normal course of operation. Allowed values are 50-500. Special values are 0- disable. Field introduced in 20.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_vnic_tx_sw_queue_size(int, Optional):
            Configure the size of software transmit spillover queue when enabled. Requires SE Reboot. Allowed values are 128-2048. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_vs_hb_max_pkts_in_batch(int, Optional):
            Maximum number of aggregated vs heartbeat packets to send in a batch. Allowed values are 1-256. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        se_vs_hb_max_vs_in_pkt(int, Optional):
            Maximum number of virtualservices for which heartbeat messages are aggregated in one packet. Allowed values are 1-1024. Field introduced in 17.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        self_se_election(bool, Optional):
            Enable SEs to elect a primary amongst themselves in the absence of a connectivity to controller. Field introduced in 18.1.2. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- false), Basic edition(Allowed values- false), Enterprise with Cloud Services edition. Defaults to None.

        send_se_ready_timeout(int, Optional):
            Timeout for sending SE_READY without NS HELPER registration completion. Allowed values are 10-600. Field introduced in 21.1.1. Unit is SECONDS. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        service_ip6_subnets(List[dict[str, Any]], Optional):
            IPv6 Subnets assigned to the SE group. Required for VS group placement. Field introduced in 18.1.1. Maximum of 128 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * ip_addr (dict[str, Any]):
                ip_addr

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mask (int):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        service_ip_subnets(List[dict[str, Any]], Optional):
            Subnets assigned to the SE group. Required for VS group placement. Field introduced in 17.1.1. Maximum of 128 items allowed. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * ip_addr (dict[str, Any]):
                ip_addr

                * addr (str):
                    IP address. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * type (str):
                     Enum options - V4, DNS, V6. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * mask (int):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        shm_minimum_config_memory(int, Optional):
            Minimum required shared memory to apply any configuration. Allowed values are 0-100. Field introduced in 18.1.2. Unit is MB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        significant_log_throttle(int, Optional):
            This setting limits the number of significant logs generated per second per core on this SE. Default is 100 logs per second. Set it to zero (0) to deactivate throttling. Field introduced in 17.1.3. Unit is PER_SECOND. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ssl_preprocess_sni_hostname(bool, Optional):
            (Beta) Preprocess SSL Client Hello for SNI hostname extension.If set to True, this will apply SNI child's SSL protocol(s), if they are different from SNI Parent's allowed SSL protocol(s). Field introduced in 17.2.12, 18.1.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        ssl_sess_cache_per_vs(int, Optional):
            Number of SSL sessions that can be cached per VS. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        tenant_ref(str, Optional):
             It is a reference to an object of type Tenant. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        transient_shared_memory_max(int, Optional):
            The threshold for the transient shared config memory in the SE. Allowed values are 0-100. Field introduced in 20.1.1. Unit is PERCENT. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        udf_log_throttle(int, Optional):
            This setting limits the number of UDF logs generated per second per core on this SE. UDF logs are generated due to the configured client log filters or the rules with logging enabled. Default is 100 logs per second. Set it to zero (0) to deactivate throttling. Field introduced in 17.1.3. Unit is PER_SECOND. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        upstream_connect_timeout(int, Optional):
            Timeout for backend connection. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        upstream_connpool_enable(bool, Optional):
            Enable upstream connection pool,. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        upstream_read_timeout(int, Optional):
            Timeout for data to be received from backend. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        upstream_send_timeout(int, Optional):
            Timeout for upstream to become writable. Field introduced in 21.1.1. Unit is MILLISECONDS. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- 3600000), Basic edition(Allowed values- 3600000), Enterprise with Cloud Services edition. Defaults to None.

        use_dp_util_for_scaleout(bool, Optional):
            If enabled, the datapath CPU utilization is consulted by the auto scale-out logic. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        use_hyperthreaded_cores(bool, Optional):
            Enables the use of hyper-threaded cores on SE. Requires SE Reboot. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        use_legacy_netlink(bool, Optional):
            Enable legacy model of netlink notifications. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        use_objsync(bool, Optional):
            Enable InterSE Objsyc distribution framework. Field introduced in 20.1.3. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        use_standard_alb(bool, Optional):
            Use Standard SKU Azure Load Balancer. By default cloud level flag is set. If not set, it inherits/uses the use_standard_alb flag from the cloud. Field introduced in 18.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        user_agent_cache_config(dict[str, Any], Optional):
            user_agent_cache_config. Defaults to None.

            * batch_size (int, Optional):
                How many unknown User-Agents to batch up before querying Controller - unless max_wait_time is reached first. Allowed values are 1-500. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * controller_cache_size (int, Optional):
                The number of User-Agent entries to cache on the Controller. Allowed values are 500-10000000. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * max_age (int, Optional):
                Time interval in seconds after which an existing entry is refreshed from upstream if it has been accessed during max_last_hit_time. Allowed values are 60-604800. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * max_last_hit_time (int, Optional):
                Time interval in seconds backwards from now during which an existing entry must have been hit for refresh from upstream. Entries that have last been accessed further in the past than max_last_hit time are not included in upstream refresh requests even if they are older than 'max_age'. Allowed values are 60-604800. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * max_upstream_queries (int, Optional):
                How often at most to query controller for a given User-Agent. Allowed values are 2-100. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * max_wait_time (int, Optional):
                The time interval in seconds after which to make a request to the Controller, even if the 'batch_size' hasn't been reached yet. Allowed values are 20-100000. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * num_entries_upstream_update (int, Optional):
                How many BotUACacheResult elements to include in an upstream update message. Allowed values are 1-10000. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * percent_reserved_for_bad_bots (int, Optional):
                How much space to reserve in percent for known bad bots. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * percent_reserved_for_browsers (int, Optional):
                How much space to reserve in percent for browsers. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * percent_reserved_for_good_bots (int, Optional):
                How much space to reserve in percent for known good bots. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * percent_reserved_for_outstanding (int, Optional):
                How much space to reserve in percent for outstanding upstream requests. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * se_cache_size (int, Optional):
                The number of User-Agent entries to cache on each Service Engine. Allowed values are 500-10000000. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

            * upstream_update_interval (int, Optional):
                How often in seconds to send updates about User-Agent cache entries to the next upstream cache. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        user_defined_metric_age(int, Optional):
            Defines in seconds how long before an unused user-defined-metric is garbage collected. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vcenter_clusters(dict[str, Any], Optional):
            vcenter_clusters. Defaults to None.

            * cluster_refs (List[str], Optional):
                 It is a reference to an object of type VIMgrClusterRuntime. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * include (bool, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vcenter_datastore_mode(str, Optional):
             Enum options - VCENTER_DATASTORE_ANY, VCENTER_DATASTORE_LOCAL, VCENTER_DATASTORE_SHARED. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vcenter_datastores(List[dict[str, Any]], Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * datastore_name (str, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * managed_object_id (str, Optional):
                Will be used by default, if not set fallback to datastore_name. Field introduced in 22.1.3. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition.

        vcenter_datastores_include(bool, Optional):
             Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vcenter_folder(str, Optional):
            Folder to place all the Service Engine virtual machines in vCenter. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vcenter_hosts(dict[str, Any], Optional):
            vcenter_hosts. Defaults to None.

            * host_refs (List[str], Optional):
                 It is a reference to an object of type VIMgrHostRuntime. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * include (bool, Optional):
                 Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vcenter_parking_vnic_pg(str, Optional):
            Parking port group to be used by 9 vnics at the time of SE creation. Field introduced in 22.1.1. Allowed in Enterprise edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vcenters(List[dict[str, Any]], Optional):
            VCenter information for scoping at Host/Cluster level. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

            * clusters (List[dict[str, Any]], Optional):
                Cluster vSphere HA configuration. Field introduced in 20.1.7, 21.1.3. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * cluster_id (str, Optional):
                    Transport node cluster. Avi derives vSphere HA property from vCenter cluster.If vSphere HA enabled on vCenter cluster, vSphere will handle HA of ServiceEngine VMs in case of underlying ESX failure.Ex MOB  domain-c23. Field introduced in 20.1.7, 21.1.3. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * override_vsphere_ha (bool, Optional):
                    If this flag set to True, Avi handles ServiceEngine failure irrespective of vSphere HA enabled on vCenter cluster or not. Field introduced in 20.1.7, 21.1.3. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * vmg_name (str, Optional):
                    Cluster VM Group name.VM Group name is unique inside cluster. Field introduced in 20.1.7, 21.1.3. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

            * nsxt_clusters (dict[str, Any], Optional):
                nsxt_clusters

                * cluster_ids (List[str], Optional):
                    List of transport node clusters. Field introduced in 20.1.6. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * include (bool, Optional):
                    Include or Exclude. Field introduced in 20.1.6. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

            * nsxt_datastores (dict[str, Any], Optional):
                nsxt_datastores

                * ds_ids (List[str], Optional):
                    List of shared datastores. Field introduced in 20.1.2. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                * include (bool, Optional):
                    Include or Exclude. Field introduced in 20.1.2. Allowed in Enterprise edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

            * nsxt_hosts (dict[str, Any], Optional):
                nsxt_hosts

                * host_ids (List[str], Optional):
                    List of transport nodes. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * include (bool, Optional):
                    Include or Exclude. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vcenter_folder (str, Optional):
                Folder to place all the Service Engine virtual machines in vCenter. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * vcenter_ref (str):
                VCenter server configuration. It is a reference to an object of type VCenterServer. Field introduced in 20.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vcpus_per_se(int, Optional):
            Number of vcpus for each of the Service Engine virtual machines. Changes to this setting do not affect existing SEs. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vip_asg(dict[str, Any], Optional):
            vip_asg. Defaults to None.

            * configuration (dict[str, Any], Optional):
                configuration

                * zones (List[dict[str, Any]], Optional):
                    This is the list of AZ+Subnet in which Vips will be spawned. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                    * availability_zone (str, Optional):
                        Availability zone associated with the subnet. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                    * fip_capable (bool, Optional):
                        Determines if the subnet is capable of hosting publicly accessible IP. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition.

                    * subnet_uuid (str, Optional):
                        UUID of the subnet for new IP address allocation. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * policy (dict[str, Any], Optional):
                policy

                * dns_cooldown (int, Optional):
                    The amount of time, in seconds, when a Vip is withdrawn before a scaling activity starts. Field introduced in 17.2.12, 18.1.2. Unit is SECONDS. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * max_size (int, Optional):
                    The maximum size of the group. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * min_size (int, Optional):
                    The minimum size of the group. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

                * suspend (bool, Optional):
                    When set, scaling is suspended. Field introduced in 17.2.12, 18.1.2. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vnic_dhcp_ip_check_interval(int, Optional):
            DHCP ip check interval. Allowed values are 1-1000. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vnic_dhcp_ip_max_retries(int, Optional):
            DHCP ip max retries. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vnic_ip_delete_interval(int, Optional):
            wait interval before deleting IP. . Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vnic_probe_interval(int, Optional):
            Probe vnic interval. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vnic_rpc_retry_interval(int, Optional):
            Time interval for retrying the failed VNIC RPC requests. Field introduced in 21.1.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vnicdb_cmd_history_size(int, Optional):
            Size of vnicdb command history. Allowed values are 0-65535. Field introduced in 21.1.1. Allowed in Enterprise edition with any value, Essentials edition with any value, Basic edition with any value, Enterprise with Cloud Services edition. Defaults to None.

        vs_host_redundancy(bool, Optional):
            Ensure primary and secondary Service Engines are deployed on different physical hosts. Allowed in Enterprise edition with any value, Essentials edition(Allowed values- true), Basic edition(Allowed values- true), Enterprise with Cloud Services edition. Special default for Essentials edition is true, Basic edition is true, Enterprise is True. Defaults to None.

        vs_scalein_timeout(int, Optional):
            Time to wait for the scaled in SE to drain existing flows before marking the scalein done. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vs_scalein_timeout_for_upgrade(int, Optional):
            During SE upgrade, Time to wait for the scaled-in SE to drain existing flows before marking the scalein done. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vs_scaleout_timeout(int, Optional):
            Time to wait for the scaled out SE to become ready before marking the scaleout done. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vs_se_scaleout_additional_wait_time(int, Optional):
            Wait time for sending scaleout ready notification after Virtual Service is marked UP. In certain deployments, there may be an additional delay to accept traffic. For example, for BGP, some time is needed for route advertisement. Allowed values are 0-300. Field introduced in 18.1.5,18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vs_se_scaleout_ready_timeout(int, Optional):
            Timeout in seconds for Service Engine to sendScaleout Ready notification of a Virtual Service. Allowed values are 0-90. Field introduced in 18.1.5,18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vs_switchover_timeout(int, Optional):
            During SE upgrade in a legacy active/standby segroup, Time to wait for the new primary SE to accept flows before marking the switchover done. Field introduced in 17.2.13,18.1.4,18.2.1. Unit is SEC. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        vss_placement(dict[str, Any], Optional):
            vss_placement. Defaults to None.

            * core_nonaffinity (int, Optional):
                Degree of core non-affinity for VS placement. Allowed values are 1-256. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

            * num_subcores (int, Optional):
                Number of sub-cores that comprise a CPU core. Allowed values are 1-128. Field introduced in 17.2.5. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition.

        vss_placement_enabled(bool, Optional):
            If set, Virtual Services will be placed on only a subset of the cores of an SE. Field introduced in 18.1.1. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        waf_mempool(bool, Optional):
            Enable memory pool for WAF.Requires SE Reboot. Field introduced in 17.2.3. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

        waf_mempool_size(int, Optional):
            Memory pool size used for WAF.Requires SE Reboot. Field introduced in 17.2.3. Unit is KB. Allowed in Enterprise edition with any value, Essentials, Basic, Enterprise with Cloud Services edition. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              nsx_alb.alb.service_engine_group.present:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.service_engine_group.update resource_id=value
    """

    result = dict(comment=[], ret=[], result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "accelerated_networking": "accelerated_networking",
        "active_standby": "active_standby",
        "aggressive_failure_detection": "aggressive_failure_detection",
        "algo": "algo",
        "allow_burst": "allow_burst",
        "app_cache_percent": "app_cache_percent",
        "app_cache_threshold": "app_cache_threshold",
        "app_learning_memory_percent": "app_learning_memory_percent",
        "archive_shm_limit": "archive_shm_limit",
        "async_ssl": "async_ssl",
        "async_ssl_threads": "async_ssl_threads",
        "auto_rebalance": "auto_rebalance",
        "auto_rebalance_capacity_per_se": "auto_rebalance_capacity_per_se",
        "auto_rebalance_criteria": "auto_rebalance_criteria",
        "auto_rebalance_interval": "auto_rebalance_interval",
        "auto_redistribute_active_standby_load": "auto_redistribute_active_standby_load",
        "availability_zone_refs": "availability_zone_refs",
        "baremetal_dispatcher_handles_flows": "baremetal_dispatcher_handles_flows",
        "bgp_peer_monitor_failover_enabled": "bgp_peer_monitor_failover_enabled",
        "bgp_state_update_interval": "bgp_state_update_interval",
        "buffer_se": "buffer_se",
        "cloud_ref": "cloud_ref",
        "compress_ip_rules_for_each_ns_subnet": "compress_ip_rules_for_each_ns_subnet",
        "config_debugs_on_all_cores": "config_debugs_on_all_cores",
        "configpb_attributes": "configpb_attributes",
        "connection_memory_percentage": "connection_memory_percentage",
        "core_shm_app_cache": "core_shm_app_cache",
        "core_shm_app_learning": "core_shm_app_learning",
        "cpu_reserve": "cpu_reserve",
        "cpu_socket_affinity": "cpu_socket_affinity",
        "custom_securitygroups_data": "custom_securitygroups_data",
        "custom_securitygroups_mgmt": "custom_securitygroups_mgmt",
        "custom_tag": "custom_tag",
        "data_network_id": "data_network_id",
        "datascript_timeout": "datascript_timeout",
        "deactivate_ipv6_discovery": "deactivate_ipv6_discovery",
        "deactivate_kni_filtering_at_dispatcher": "deactivate_kni_filtering_at_dispatcher",
        "dedicated_dispatcher_core": "dedicated_dispatcher_core",
        "description": "description",
        "disable_avi_securitygroups": "disable_avi_securitygroups",
        "disable_csum_offloads": "disable_csum_offloads",
        "disable_flow_probes": "disable_flow_probes",
        "disable_gro": "disable_gro",
        "disable_se_memory_check": "disable_se_memory_check",
        "disable_tso": "disable_tso",
        "disk_per_se": "disk_per_se",
        "distribute_load_active_standby": "distribute_load_active_standby",
        "distribute_queues": "distribute_queues",
        "distribute_vnics": "distribute_vnics",
        "downstream_send_timeout": "downstream_send_timeout",
        "dp_aggressive_deq_interval_msec": "dp_aggressive_deq_interval_msec",
        "dp_aggressive_enq_interval_msec": "dp_aggressive_enq_interval_msec",
        "dp_aggressive_hb_frequency": "dp_aggressive_hb_frequency",
        "dp_aggressive_hb_timeout_count": "dp_aggressive_hb_timeout_count",
        "dp_deq_interval_msec": "dp_deq_interval_msec",
        "dp_enq_interval_msec": "dp_enq_interval_msec",
        "dp_hb_frequency": "dp_hb_frequency",
        "dp_hb_timeout_count": "dp_hb_timeout_count",
        "dpdk_gro_timeout_interval": "dpdk_gro_timeout_interval",
        "enable_gratarp_permanent": "enable_gratarp_permanent",
        "enable_hsm_log": "enable_hsm_log",
        "enable_hsm_priming": "enable_hsm_priming",
        "enable_multi_lb": "enable_multi_lb",
        "enable_pcap_tx_ring": "enable_pcap_tx_ring",
        "ephemeral_portrange_end": "ephemeral_portrange_end",
        "ephemeral_portrange_start": "ephemeral_portrange_start",
        "extra_config_multiplier": "extra_config_multiplier",
        "extra_shared_config_memory": "extra_shared_config_memory",
        "flow_table_new_syn_max_entries": "flow_table_new_syn_max_entries",
        "free_list_size": "free_list_size",
        "gcp_config": "gcp_config",
        "gratarp_permanent_periodicity": "gratarp_permanent_periodicity",
        "grpc_channel_connect_timeout": "grpc_channel_connect_timeout",
        "ha_mode": "ha_mode",
        "handle_per_pkt_attack": "handle_per_pkt_attack",
        "hardwaresecuritymodulegroup_ref": "hardwaresecuritymodulegroup_ref",
        "heap_minimum_config_memory": "heap_minimum_config_memory",
        "hm_on_standby": "hm_on_standby",
        "host_attribute_key": "host_attribute_key",
        "host_attribute_value": "host_attribute_value",
        "host_gateway_monitor": "host_gateway_monitor",
        "http_rum_console_log": "http_rum_console_log",
        "http_rum_min_content_length": "http_rum_min_content_length",
        "hybrid_rss_mode": "hybrid_rss_mode",
        "hypervisor": "hypervisor",
        "ignore_docker_mac_change": "ignore_docker_mac_change",
        "ignore_rtt_threshold": "ignore_rtt_threshold",
        "ingress_access_data": "ingress_access_data",
        "ingress_access_mgmt": "ingress_access_mgmt",
        "instance_flavor": "instance_flavor",
        "instance_flavor_info": "instance_flavor_info",
        "iptables": "iptables",
        "kni_allowed_server_ports": "kni_allowed_server_ports",
        "l7_conns_per_core": "l7_conns_per_core",
        "l7_resvd_listen_conns_per_core": "l7_resvd_listen_conns_per_core",
        "labels": "labels",
        "lbaction_num_requests_to_dispatch": "lbaction_num_requests_to_dispatch",
        "lbaction_rq_per_request_max_retries": "lbaction_rq_per_request_max_retries",
        "least_load_core_selection": "least_load_core_selection",
        "license_tier": "license_tier",
        "license_type": "license_type",
        "log_agent_compress_logs": "log_agent_compress_logs",
        "log_agent_debug_enabled": "log_agent_debug_enabled",
        "log_agent_file_sz_appl": "log_agent_file_sz_appl",
        "log_agent_file_sz_conn": "log_agent_file_sz_conn",
        "log_agent_file_sz_debug": "log_agent_file_sz_debug",
        "log_agent_file_sz_event": "log_agent_file_sz_event",
        "log_agent_log_storage_min_sz": "log_agent_log_storage_min_sz",
        "log_agent_max_concurrent_rsync": "log_agent_max_concurrent_rsync",
        "log_agent_max_storage_excess_percent": "log_agent_max_storage_excess_percent",
        "log_agent_max_storage_ignore_percent": "log_agent_max_storage_ignore_percent",
        "log_agent_min_storage_per_vs": "log_agent_min_storage_per_vs",
        "log_agent_sleep_interval": "log_agent_sleep_interval",
        "log_agent_trace_enabled": "log_agent_trace_enabled",
        "log_agent_unknown_vs_timer": "log_agent_unknown_vs_timer",
        "log_disksz": "log_disksz",
        "log_malloc_failure": "log_malloc_failure",
        "log_message_max_file_list_size": "log_message_max_file_list_size",
        "markers": "markers",
        "max_concurrent_external_hm": "max_concurrent_external_hm",
        "max_cpu_usage": "max_cpu_usage",
        "max_memory_per_mempool": "max_memory_per_mempool",
        "max_num_se_dps": "max_num_se_dps",
        "max_public_ips_per_lb": "max_public_ips_per_lb",
        "max_queues_per_vnic": "max_queues_per_vnic",
        "max_rules_per_lb": "max_rules_per_lb",
        "max_scaleout_per_vs": "max_scaleout_per_vs",
        "max_se": "max_se",
        "max_skb_frags": "max_skb_frags",
        "max_vs_per_se": "max_vs_per_se",
        "mem_reserve": "mem_reserve",
        "memory_for_config_update": "memory_for_config_update",
        "memory_per_se": "memory_per_se",
        "mgmt_network_ref": "mgmt_network_ref",
        "mgmt_subnet": "mgmt_subnet",
        "min_cpu_usage": "min_cpu_usage",
        "min_scaleout_per_vs": "min_scaleout_per_vs",
        "min_se": "min_se",
        "minimum_connection_memory": "minimum_connection_memory",
        "n_log_streaming_threads": "n_log_streaming_threads",
        "name": "name",
        "netlink_poller_threads": "netlink_poller_threads",
        "netlink_sock_buf_size": "netlink_sock_buf_size",
        "ngx_free_connection_stack": "ngx_free_connection_stack",
        "non_significant_log_throttle": "non_significant_log_throttle",
        "ns_helper_deq_interval_msec": "ns_helper_deq_interval_msec",
        "ntp_sync_fail_event": "ntp_sync_fail_event",
        "ntp_sync_status_interval": "ntp_sync_status_interval",
        "num_dispatcher_cores": "num_dispatcher_cores",
        "num_dispatcher_queues": "num_dispatcher_queues",
        "num_flow_cores_sum_changes_to_ignore": "num_flow_cores_sum_changes_to_ignore",
        "objsync_config": "objsync_config",
        "objsync_port": "objsync_port",
        "openstack_availability_zones": "openstack_availability_zones",
        "openstack_mgmt_network_name": "openstack_mgmt_network_name",
        "openstack_mgmt_network_uuid": "openstack_mgmt_network_uuid",
        "os_reserved_memory": "os_reserved_memory",
        "pcap_tx_mode": "pcap_tx_mode",
        "pcap_tx_ring_rd_balancing_factor": "pcap_tx_ring_rd_balancing_factor",
        "per_app": "per_app",
        "per_vs_admission_control": "per_vs_admission_control",
        "placement_mode": "placement_mode",
        "realtime_se_metrics": "realtime_se_metrics",
        "reboot_on_panic": "reboot_on_panic",
        "replay_vrf_routes_interval": "replay_vrf_routes_interval",
        "resync_time_interval": "resync_time_interval",
        "sdb_flush_interval": "sdb_flush_interval",
        "sdb_pipeline_size": "sdb_pipeline_size",
        "sdb_scan_count": "sdb_scan_count",
        "se_bandwidth_type": "se_bandwidth_type",
        "se_delayed_flow_delete": "se_delayed_flow_delete",
        "se_deprovision_delay": "se_deprovision_delay",
        "se_dos_profile": "se_dos_profile",
        "se_dp_hm_drops": "se_dp_hm_drops",
        "se_dp_if_state_poll_interval": "se_dp_if_state_poll_interval",
        "se_dp_isolation": "se_dp_isolation",
        "se_dp_isolation_num_non_dp_cpus": "se_dp_isolation_num_non_dp_cpus",
        "se_dp_log_nf_enqueue_percent": "se_dp_log_nf_enqueue_percent",
        "se_dp_log_udf_enqueue_percent": "se_dp_log_udf_enqueue_percent",
        "se_dp_max_hb_version": "se_dp_max_hb_version",
        "se_dp_vnic_queue_stall_event_sleep": "se_dp_vnic_queue_stall_event_sleep",
        "se_dp_vnic_queue_stall_threshold": "se_dp_vnic_queue_stall_threshold",
        "se_dp_vnic_queue_stall_timeout": "se_dp_vnic_queue_stall_timeout",
        "se_dp_vnic_restart_on_queue_stall_count": "se_dp_vnic_restart_on_queue_stall_count",
        "se_dp_vnic_stall_se_restart_window": "se_dp_vnic_stall_se_restart_window",
        "se_dpdk_pmd": "se_dpdk_pmd",
        "se_dump_core_on_assert": "se_dump_core_on_assert",
        "se_emulated_cores": "se_emulated_cores",
        "se_flow_probe_retries": "se_flow_probe_retries",
        "se_flow_probe_retry_timer": "se_flow_probe_retry_timer",
        "se_group_analytics_policy": "se_group_analytics_policy",
        "se_hyperthreaded_mode": "se_hyperthreaded_mode",
        "se_ip_encap_ipc": "se_ip_encap_ipc",
        "se_kni_burst_factor": "se_kni_burst_factor",
        "se_l3_encap_ipc": "se_l3_encap_ipc",
        "se_log_buffer_app_blocking_dequeue": "se_log_buffer_app_blocking_dequeue",
        "se_log_buffer_conn_blocking_dequeue": "se_log_buffer_conn_blocking_dequeue",
        "se_log_buffer_events_blocking_dequeue": "se_log_buffer_events_blocking_dequeue",
        "se_lro": "se_lro",
        "se_mp_ring_retry_count": "se_mp_ring_retry_count",
        "se_mtu": "se_mtu",
        "se_name_prefix": "se_name_prefix",
        "se_packet_buffer_max": "se_packet_buffer_max",
        "se_pcap_lookahead": "se_pcap_lookahead",
        "se_pcap_pkt_count": "se_pcap_pkt_count",
        "se_pcap_pkt_sz": "se_pcap_pkt_sz",
        "se_pcap_qdisc_bypass": "se_pcap_qdisc_bypass",
        "se_pcap_reinit_frequency": "se_pcap_reinit_frequency",
        "se_pcap_reinit_threshold": "se_pcap_reinit_threshold",
        "se_probe_port": "se_probe_port",
        "se_rl_prop": "se_rl_prop",
        "se_rum_sampling_nav_interval": "se_rum_sampling_nav_interval",
        "se_rum_sampling_nav_percent": "se_rum_sampling_nav_percent",
        "se_rum_sampling_res_interval": "se_rum_sampling_res_interval",
        "se_rum_sampling_res_percent": "se_rum_sampling_res_percent",
        "se_sb_dedicated_core": "se_sb_dedicated_core",
        "se_sb_threads": "se_sb_threads",
        "se_thread_multiplier": "se_thread_multiplier",
        "se_time_tracker_props": "se_time_tracker_props",
        "se_tracert_port_range": "se_tracert_port_range",
        "se_tunnel_mode": "se_tunnel_mode",
        "se_tunnel_udp_port": "se_tunnel_udp_port",
        "se_tx_batch_size": "se_tx_batch_size",
        "se_txq_threshold": "se_txq_threshold",
        "se_udp_encap_ipc": "se_udp_encap_ipc",
        "se_use_dpdk": "se_use_dpdk",
        "se_vnic_tx_sw_queue_flush_frequency": "se_vnic_tx_sw_queue_flush_frequency",
        "se_vnic_tx_sw_queue_size": "se_vnic_tx_sw_queue_size",
        "se_vs_hb_max_pkts_in_batch": "se_vs_hb_max_pkts_in_batch",
        "se_vs_hb_max_vs_in_pkt": "se_vs_hb_max_vs_in_pkt",
        "self_se_election": "self_se_election",
        "send_se_ready_timeout": "send_se_ready_timeout",
        "service_ip6_subnets": "service_ip6_subnets",
        "service_ip_subnets": "service_ip_subnets",
        "shm_minimum_config_memory": "shm_minimum_config_memory",
        "significant_log_throttle": "significant_log_throttle",
        "ssl_preprocess_sni_hostname": "ssl_preprocess_sni_hostname",
        "ssl_sess_cache_per_vs": "ssl_sess_cache_per_vs",
        "tenant_ref": "tenant_ref",
        "transient_shared_memory_max": "transient_shared_memory_max",
        "udf_log_throttle": "udf_log_throttle",
        "upstream_connect_timeout": "upstream_connect_timeout",
        "upstream_connpool_enable": "upstream_connpool_enable",
        "upstream_read_timeout": "upstream_read_timeout",
        "upstream_send_timeout": "upstream_send_timeout",
        "use_dp_util_for_scaleout": "use_dp_util_for_scaleout",
        "use_hyperthreaded_cores": "use_hyperthreaded_cores",
        "use_legacy_netlink": "use_legacy_netlink",
        "use_objsync": "use_objsync",
        "use_standard_alb": "use_standard_alb",
        "user_agent_cache_config": "user_agent_cache_config",
        "user_defined_metric_age": "user_defined_metric_age",
        "vcenter_clusters": "vcenter_clusters",
        "vcenter_datastore_mode": "vcenter_datastore_mode",
        "vcenter_datastores": "vcenter_datastores",
        "vcenter_datastores_include": "vcenter_datastores_include",
        "vcenter_folder": "vcenter_folder",
        "vcenter_hosts": "vcenter_hosts",
        "vcenter_parking_vnic_pg": "vcenter_parking_vnic_pg",
        "vcenters": "vcenters",
        "vcpus_per_se": "vcpus_per_se",
        "vip_asg": "vip_asg",
        "vnic_dhcp_ip_check_interval": "vnic_dhcp_ip_check_interval",
        "vnic_dhcp_ip_max_retries": "vnic_dhcp_ip_max_retries",
        "vnic_ip_delete_interval": "vnic_ip_delete_interval",
        "vnic_probe_interval": "vnic_probe_interval",
        "vnic_rpc_retry_interval": "vnic_rpc_retry_interval",
        "vnicdb_cmd_history_size": "vnicdb_cmd_history_size",
        "vs_host_redundancy": "vs_host_redundancy",
        "vs_scalein_timeout": "vs_scalein_timeout",
        "vs_scalein_timeout_for_upgrade": "vs_scalein_timeout_for_upgrade",
        "vs_scaleout_timeout": "vs_scaleout_timeout",
        "vs_se_scaleout_additional_wait_time": "vs_se_scaleout_additional_wait_time",
        "vs_se_scaleout_ready_timeout": "vs_se_scaleout_ready_timeout",
        "vs_switchover_timeout": "vs_switchover_timeout",
        "vss_placement": "vss_placement",
        "vss_placement_enabled": "vss_placement_enabled",
        "waf_mempool": "waf_mempool",
        "waf_mempool_size": "waf_mempool_size",
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
            path="/serviceenginegroup/{uuid}".format(**{"uuid": resource_id}),
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
            f"Updated nsx_alb.alb.service_engine_group '{name}'",
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
            Alb.service_engine_group unique ID.

        name(str, Optional):
            Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              nsx_alb.alb.service_engine_group.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec nsx_alb.alb.service_engine_group.delete resource_id=value
    """

    result = dict(comment=[], ret=[], result=True)

    before = await hub.exec.nsx_alb.alb.service_engine_group.get(
        ctx,
        name=name,
        resource_id=resource_id,
    )
    if before["ret"]:
        tenant_name = before["ret"]["tenant_ref"].split("#")[-1]
    delete = await hub.tool.nsx_alb.session.request(
        ctx,
        method="delete",
        path="/serviceenginegroup/{uuid}".format(**{"uuid": resource_id}),
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
