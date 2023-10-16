'''
# `vsphere_compute_cluster`

Refer to the Terraform Registory for docs: [`vsphere_compute_cluster`](https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ComputeCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vsphere.computeCluster.ComputeCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster vsphere_compute_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        datacenter_id: builtins.str,
        name: builtins.str,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        dpm_automation_level: typing.Optional[builtins.str] = None,
        dpm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dpm_threshold: typing.Optional[jsii.Number] = None,
        drs_advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        drs_automation_level: typing.Optional[builtins.str] = None,
        drs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drs_enable_predictive_drs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drs_enable_vm_overrides: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drs_migration_threshold: typing.Optional[jsii.Number] = None,
        drs_scale_descendants_shares: typing.Optional[builtins.str] = None,
        folder: typing.Optional[builtins.str] = None,
        force_evacuate_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ha_admission_control_failover_host_system_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ha_admission_control_host_failure_tolerance: typing.Optional[jsii.Number] = None,
        ha_admission_control_performance_tolerance: typing.Optional[jsii.Number] = None,
        ha_admission_control_policy: typing.Optional[builtins.str] = None,
        ha_admission_control_resource_percentage_auto_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ha_admission_control_resource_percentage_cpu: typing.Optional[jsii.Number] = None,
        ha_admission_control_resource_percentage_memory: typing.Optional[jsii.Number] = None,
        ha_admission_control_slot_policy_explicit_cpu: typing.Optional[jsii.Number] = None,
        ha_admission_control_slot_policy_explicit_memory: typing.Optional[jsii.Number] = None,
        ha_admission_control_slot_policy_use_explicit_size: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ha_advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        ha_datastore_apd_recovery_action: typing.Optional[builtins.str] = None,
        ha_datastore_apd_response: typing.Optional[builtins.str] = None,
        ha_datastore_apd_response_delay: typing.Optional[jsii.Number] = None,
        ha_datastore_pdl_response: typing.Optional[builtins.str] = None,
        ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ha_heartbeat_datastore_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ha_heartbeat_datastore_policy: typing.Optional[builtins.str] = None,
        ha_host_isolation_response: typing.Optional[builtins.str] = None,
        ha_host_monitoring: typing.Optional[builtins.str] = None,
        ha_vm_component_protection: typing.Optional[builtins.str] = None,
        ha_vm_dependency_restart_condition: typing.Optional[builtins.str] = None,
        ha_vm_failure_interval: typing.Optional[jsii.Number] = None,
        ha_vm_maximum_failure_window: typing.Optional[jsii.Number] = None,
        ha_vm_maximum_resets: typing.Optional[jsii.Number] = None,
        ha_vm_minimum_uptime: typing.Optional[jsii.Number] = None,
        ha_vm_monitoring: typing.Optional[builtins.str] = None,
        ha_vm_restart_additional_delay: typing.Optional[jsii.Number] = None,
        ha_vm_restart_priority: typing.Optional[builtins.str] = None,
        ha_vm_restart_timeout: typing.Optional[jsii.Number] = None,
        host_cluster_exit_timeout: typing.Optional[jsii.Number] = None,
        host_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_system_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        proactive_ha_automation_level: typing.Optional[builtins.str] = None,
        proactive_ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        proactive_ha_moderate_remediation: typing.Optional[builtins.str] = None,
        proactive_ha_provider_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        proactive_ha_severe_remediation: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        vsan_compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_dedup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_disk_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeClusterVsanDiskGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vsan_dit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_dit_rekey_interval: typing.Optional[jsii.Number] = None,
        vsan_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_network_diagnostic_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_performance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_remote_datastore_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vsan_unmap_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_verbose_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster vsphere_compute_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param datacenter_id: The managed object ID of the datacenter to put the cluster in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#datacenter_id ComputeCluster#datacenter_id}
        :param name: Name for the new cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#name ComputeCluster#name}
        :param custom_attributes: A list of custom attributes to set on this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#custom_attributes ComputeCluster#custom_attributes}
        :param dpm_automation_level: The automation level for host power operations in this cluster. Can be one of manual or automated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#dpm_automation_level ComputeCluster#dpm_automation_level}
        :param dpm_enabled: Enable DPM support for DRS. This allows you to dynamically control the power of hosts depending on the needs of virtual machines in the cluster. Requires that DRS be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#dpm_enabled ComputeCluster#dpm_enabled}
        :param dpm_threshold: A value between 1 and 5 indicating the threshold of load within the cluster that influences host power operations. This affects both power on and power off operations - a lower setting will tolerate more of a surplus/deficit than a higher setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#dpm_threshold ComputeCluster#dpm_threshold}
        :param drs_advanced_options: Advanced configuration options for DRS and DPM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_advanced_options ComputeCluster#drs_advanced_options}
        :param drs_automation_level: The default automation level for all virtual machines in this cluster. Can be one of manual, partiallyAutomated, or fullyAutomated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_automation_level ComputeCluster#drs_automation_level}
        :param drs_enabled: Enable DRS for this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_enabled ComputeCluster#drs_enabled}
        :param drs_enable_predictive_drs: When true, enables DRS to use data from vRealize Operations Manager to make proactive DRS recommendations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_enable_predictive_drs ComputeCluster#drs_enable_predictive_drs}
        :param drs_enable_vm_overrides: When true, allows individual VM overrides within this cluster to be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_enable_vm_overrides ComputeCluster#drs_enable_vm_overrides}
        :param drs_migration_threshold: A value between 1 and 5 indicating the threshold of imbalance tolerated between hosts. A lower setting will tolerate more imbalance while a higher setting will tolerate less. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_migration_threshold ComputeCluster#drs_migration_threshold}
        :param drs_scale_descendants_shares: Enable scalable shares for all descendants of this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_scale_descendants_shares ComputeCluster#drs_scale_descendants_shares}
        :param folder: The name of the folder to locate the cluster in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#folder ComputeCluster#folder}
        :param force_evacuate_on_destroy: Force removal of all hosts in the cluster during destroy and make them standalone hosts. Use of this flag mainly exists for testing and is not recommended in normal use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#force_evacuate_on_destroy ComputeCluster#force_evacuate_on_destroy}
        :param ha_admission_control_failover_host_system_ids: When ha_admission_control_policy is failoverHosts, this defines the managed object IDs of hosts to use as dedicated failover hosts. These hosts are kept as available as possible - admission control will block access to the host, and DRS will ignore the host when making recommendations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_failover_host_system_ids ComputeCluster#ha_admission_control_failover_host_system_ids}
        :param ha_admission_control_host_failure_tolerance: The maximum number of failed hosts that admission control tolerates when making decisions on whether to permit virtual machine operations. The maximum is one less than the number of hosts in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_host_failure_tolerance ComputeCluster#ha_admission_control_host_failure_tolerance}
        :param ha_admission_control_performance_tolerance: The percentage of resource reduction that a cluster of VMs can tolerate in case of a failover. A value of 0 produces warnings only, whereas a value of 100 disables the setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_performance_tolerance ComputeCluster#ha_admission_control_performance_tolerance}
        :param ha_admission_control_policy: The type of admission control policy to use with vSphere HA, which controls whether or not specific VM operations are permitted in the cluster in order to protect the reliability of the cluster. Can be one of resourcePercentage, slotPolicy, failoverHosts, or disabled. Note that disabling admission control is not recommended and can lead to service issues. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_policy ComputeCluster#ha_admission_control_policy}
        :param ha_admission_control_resource_percentage_auto_compute: When ha_admission_control_policy is resourcePercentage, automatically determine available resource percentages by subtracting the average number of host resources represented by the ha_admission_control_host_failure_tolerance setting from the total amount of resources in the cluster. Disable to supply user-defined values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_resource_percentage_auto_compute ComputeCluster#ha_admission_control_resource_percentage_auto_compute}
        :param ha_admission_control_resource_percentage_cpu: When ha_admission_control_policy is resourcePercentage, this controls the user-defined percentage of CPU resources in the cluster to reserve for failover. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_resource_percentage_cpu ComputeCluster#ha_admission_control_resource_percentage_cpu}
        :param ha_admission_control_resource_percentage_memory: When ha_admission_control_policy is resourcePercentage, this controls the user-defined percentage of memory resources in the cluster to reserve for failover. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_resource_percentage_memory ComputeCluster#ha_admission_control_resource_percentage_memory}
        :param ha_admission_control_slot_policy_explicit_cpu: When ha_admission_control_policy is slotPolicy, this controls the user-defined CPU slot size, in MHz. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_slot_policy_explicit_cpu ComputeCluster#ha_admission_control_slot_policy_explicit_cpu}
        :param ha_admission_control_slot_policy_explicit_memory: When ha_admission_control_policy is slotPolicy, this controls the user-defined memory slot size, in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_slot_policy_explicit_memory ComputeCluster#ha_admission_control_slot_policy_explicit_memory}
        :param ha_admission_control_slot_policy_use_explicit_size: When ha_admission_control_policy is slotPolicy, this setting controls whether or not you wish to supply explicit values to CPU and memory slot sizes. The default is to gather a automatic average based on all powered-on virtual machines currently in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_slot_policy_use_explicit_size ComputeCluster#ha_admission_control_slot_policy_use_explicit_size}
        :param ha_advanced_options: Advanced configuration options for vSphere HA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_advanced_options ComputeCluster#ha_advanced_options}
        :param ha_datastore_apd_recovery_action: When ha_vm_component_protection is enabled, controls the action to take on virtual machines if an APD status on an affected datastore clears in the middle of an APD event. Can be one of none or reset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_datastore_apd_recovery_action ComputeCluster#ha_datastore_apd_recovery_action}
        :param ha_datastore_apd_response: When ha_vm_component_protection is enabled, controls the action to take on virtual machines when the cluster has detected loss to all paths to a relevant datastore. Can be one of disabled, warning, restartConservative, or restartAggressive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_datastore_apd_response ComputeCluster#ha_datastore_apd_response}
        :param ha_datastore_apd_response_delay: When ha_vm_component_protection is enabled, controls the delay in seconds to wait after an APD timeout event to execute the response action defined in ha_datastore_apd_response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_datastore_apd_response_delay ComputeCluster#ha_datastore_apd_response_delay}
        :param ha_datastore_pdl_response: When ha_vm_component_protection is enabled, controls the action to take on virtual machines when the cluster has detected a permanent device loss to a relevant datastore. Can be one of disabled, warning, or restartAggressive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_datastore_pdl_response ComputeCluster#ha_datastore_pdl_response}
        :param ha_enabled: Enable vSphere HA for this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_enabled ComputeCluster#ha_enabled}
        :param ha_heartbeat_datastore_ids: The list of managed object IDs for preferred datastores to use for HA heartbeating. This setting is only useful when ha_heartbeat_datastore_policy is set to either userSelectedDs or allFeasibleDsWithUserPreference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_heartbeat_datastore_ids ComputeCluster#ha_heartbeat_datastore_ids}
        :param ha_heartbeat_datastore_policy: The selection policy for HA heartbeat datastores. Can be one of allFeasibleDs, userSelectedDs, or allFeasibleDsWithUserPreference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_heartbeat_datastore_policy ComputeCluster#ha_heartbeat_datastore_policy}
        :param ha_host_isolation_response: The action to take on virtual machines when a host has detected that it has been isolated from the rest of the cluster. Can be one of none, powerOff, or shutdown. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_host_isolation_response ComputeCluster#ha_host_isolation_response}
        :param ha_host_monitoring: Global setting that controls whether vSphere HA remediates VMs on host failure. Can be one of enabled or disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_host_monitoring ComputeCluster#ha_host_monitoring}
        :param ha_vm_component_protection: Controls vSphere VM component protection for virtual machines in this cluster. This allows vSphere HA to react to failures between hosts and specific virtual machine components, such as datastores. Can be one of enabled or disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_component_protection ComputeCluster#ha_vm_component_protection}
        :param ha_vm_dependency_restart_condition: The condition used to determine whether or not VMs in a certain restart priority class are online, allowing HA to move on to restarting VMs on the next priority. Can be one of none, poweredOn, guestHbStatusGreen, or appHbStatusGreen. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_dependency_restart_condition ComputeCluster#ha_vm_dependency_restart_condition}
        :param ha_vm_failure_interval: If a heartbeat from a virtual machine is not received within this configured interval, the virtual machine is marked as failed. The value is in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_failure_interval ComputeCluster#ha_vm_failure_interval}
        :param ha_vm_maximum_failure_window: The length of the reset window in which ha_vm_maximum_resets can operate. When this window expires, no more resets are attempted regardless of the setting configured in ha_vm_maximum_resets. -1 means no window, meaning an unlimited reset time is allotted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_maximum_failure_window ComputeCluster#ha_vm_maximum_failure_window}
        :param ha_vm_maximum_resets: The maximum number of resets that HA will perform to a virtual machine when responding to a failure event. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_maximum_resets ComputeCluster#ha_vm_maximum_resets}
        :param ha_vm_minimum_uptime: The time, in seconds, that HA waits after powering on a virtual machine before monitoring for heartbeats. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_minimum_uptime ComputeCluster#ha_vm_minimum_uptime}
        :param ha_vm_monitoring: The type of virtual machine monitoring to use when HA is enabled in the cluster. Can be one of vmMonitoringDisabled, vmMonitoringOnly, or vmAndAppMonitoring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_monitoring ComputeCluster#ha_vm_monitoring}
        :param ha_vm_restart_additional_delay: Additional delay in seconds after ready condition is met. A VM is considered ready at this point. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_restart_additional_delay ComputeCluster#ha_vm_restart_additional_delay}
        :param ha_vm_restart_priority: The default restart priority for affected VMs when vSphere detects a host failure. Can be one of lowest, low, medium, high, or highest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_restart_priority ComputeCluster#ha_vm_restart_priority}
        :param ha_vm_restart_timeout: The maximum time, in seconds, that vSphere HA will wait for virtual machines in one priority to be ready before proceeding with the next priority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_restart_timeout ComputeCluster#ha_vm_restart_timeout}
        :param host_cluster_exit_timeout: The timeout for each host maintenance mode operation when removing hosts from a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#host_cluster_exit_timeout ComputeCluster#host_cluster_exit_timeout}
        :param host_managed: Must be set if cluster enrollment is managed from host resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#host_managed ComputeCluster#host_managed}
        :param host_system_ids: The managed object IDs of the hosts to put in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#host_system_ids ComputeCluster#host_system_ids}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#id ComputeCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param proactive_ha_automation_level: The DRS behavior for proactive HA recommendations. Can be one of Automated or Manual. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_automation_level ComputeCluster#proactive_ha_automation_level}
        :param proactive_ha_enabled: Enables proactive HA, allowing for vSphere to get HA data from external providers and use DRS to perform remediation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_enabled ComputeCluster#proactive_ha_enabled}
        :param proactive_ha_moderate_remediation: The configured remediation for moderately degraded hosts. Can be one of MaintenanceMode or QuarantineMode. Note that this cannot be set to MaintenanceMode when proactive_ha_severe_remediation is set to QuarantineMode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_moderate_remediation ComputeCluster#proactive_ha_moderate_remediation}
        :param proactive_ha_provider_ids: The list of IDs for health update providers configured for this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_provider_ids ComputeCluster#proactive_ha_provider_ids}
        :param proactive_ha_severe_remediation: The configured remediation for severely degraded hosts. Can be one of MaintenanceMode or QuarantineMode. Note that this cannot be set to QuarantineMode when proactive_ha_moderate_remediation is set to MaintenanceMode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_severe_remediation ComputeCluster#proactive_ha_severe_remediation}
        :param tags: A list of tag IDs to apply to this object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#tags ComputeCluster#tags}
        :param vsan_compression_enabled: Whether the vSAN compression service is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_compression_enabled ComputeCluster#vsan_compression_enabled}
        :param vsan_dedup_enabled: Whether the vSAN deduplication service is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_dedup_enabled ComputeCluster#vsan_dedup_enabled}
        :param vsan_disk_group: vsan_disk_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_disk_group ComputeCluster#vsan_disk_group}
        :param vsan_dit_encryption_enabled: Whether the vSAN data-in-transit encryption is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_dit_encryption_enabled ComputeCluster#vsan_dit_encryption_enabled}
        :param vsan_dit_rekey_interval: When vsan_dit_encryption_enabled is enabled, sets the rekey interval of data-in-transit encryption (in minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_dit_rekey_interval ComputeCluster#vsan_dit_rekey_interval}
        :param vsan_enabled: Whether the vSAN service is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_enabled ComputeCluster#vsan_enabled}
        :param vsan_network_diagnostic_mode_enabled: Whether the vSAN network diagnostic mode is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_network_diagnostic_mode_enabled ComputeCluster#vsan_network_diagnostic_mode_enabled}
        :param vsan_performance_enabled: Whether the vSAN performance service is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_performance_enabled ComputeCluster#vsan_performance_enabled}
        :param vsan_remote_datastore_ids: The managed object IDs of the vSAN datastore to be mounted on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_remote_datastore_ids ComputeCluster#vsan_remote_datastore_ids}
        :param vsan_unmap_enabled: Whether the vSAN unmap service is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_unmap_enabled ComputeCluster#vsan_unmap_enabled}
        :param vsan_verbose_mode_enabled: Whether the vSAN verbose mode is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_verbose_mode_enabled ComputeCluster#vsan_verbose_mode_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d9ec692d92b24a65224aed0e724338f0cd7313cfd48925db94cc279dff4065)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeClusterConfig(
            datacenter_id=datacenter_id,
            name=name,
            custom_attributes=custom_attributes,
            dpm_automation_level=dpm_automation_level,
            dpm_enabled=dpm_enabled,
            dpm_threshold=dpm_threshold,
            drs_advanced_options=drs_advanced_options,
            drs_automation_level=drs_automation_level,
            drs_enabled=drs_enabled,
            drs_enable_predictive_drs=drs_enable_predictive_drs,
            drs_enable_vm_overrides=drs_enable_vm_overrides,
            drs_migration_threshold=drs_migration_threshold,
            drs_scale_descendants_shares=drs_scale_descendants_shares,
            folder=folder,
            force_evacuate_on_destroy=force_evacuate_on_destroy,
            ha_admission_control_failover_host_system_ids=ha_admission_control_failover_host_system_ids,
            ha_admission_control_host_failure_tolerance=ha_admission_control_host_failure_tolerance,
            ha_admission_control_performance_tolerance=ha_admission_control_performance_tolerance,
            ha_admission_control_policy=ha_admission_control_policy,
            ha_admission_control_resource_percentage_auto_compute=ha_admission_control_resource_percentage_auto_compute,
            ha_admission_control_resource_percentage_cpu=ha_admission_control_resource_percentage_cpu,
            ha_admission_control_resource_percentage_memory=ha_admission_control_resource_percentage_memory,
            ha_admission_control_slot_policy_explicit_cpu=ha_admission_control_slot_policy_explicit_cpu,
            ha_admission_control_slot_policy_explicit_memory=ha_admission_control_slot_policy_explicit_memory,
            ha_admission_control_slot_policy_use_explicit_size=ha_admission_control_slot_policy_use_explicit_size,
            ha_advanced_options=ha_advanced_options,
            ha_datastore_apd_recovery_action=ha_datastore_apd_recovery_action,
            ha_datastore_apd_response=ha_datastore_apd_response,
            ha_datastore_apd_response_delay=ha_datastore_apd_response_delay,
            ha_datastore_pdl_response=ha_datastore_pdl_response,
            ha_enabled=ha_enabled,
            ha_heartbeat_datastore_ids=ha_heartbeat_datastore_ids,
            ha_heartbeat_datastore_policy=ha_heartbeat_datastore_policy,
            ha_host_isolation_response=ha_host_isolation_response,
            ha_host_monitoring=ha_host_monitoring,
            ha_vm_component_protection=ha_vm_component_protection,
            ha_vm_dependency_restart_condition=ha_vm_dependency_restart_condition,
            ha_vm_failure_interval=ha_vm_failure_interval,
            ha_vm_maximum_failure_window=ha_vm_maximum_failure_window,
            ha_vm_maximum_resets=ha_vm_maximum_resets,
            ha_vm_minimum_uptime=ha_vm_minimum_uptime,
            ha_vm_monitoring=ha_vm_monitoring,
            ha_vm_restart_additional_delay=ha_vm_restart_additional_delay,
            ha_vm_restart_priority=ha_vm_restart_priority,
            ha_vm_restart_timeout=ha_vm_restart_timeout,
            host_cluster_exit_timeout=host_cluster_exit_timeout,
            host_managed=host_managed,
            host_system_ids=host_system_ids,
            id=id,
            proactive_ha_automation_level=proactive_ha_automation_level,
            proactive_ha_enabled=proactive_ha_enabled,
            proactive_ha_moderate_remediation=proactive_ha_moderate_remediation,
            proactive_ha_provider_ids=proactive_ha_provider_ids,
            proactive_ha_severe_remediation=proactive_ha_severe_remediation,
            tags=tags,
            vsan_compression_enabled=vsan_compression_enabled,
            vsan_dedup_enabled=vsan_dedup_enabled,
            vsan_disk_group=vsan_disk_group,
            vsan_dit_encryption_enabled=vsan_dit_encryption_enabled,
            vsan_dit_rekey_interval=vsan_dit_rekey_interval,
            vsan_enabled=vsan_enabled,
            vsan_network_diagnostic_mode_enabled=vsan_network_diagnostic_mode_enabled,
            vsan_performance_enabled=vsan_performance_enabled,
            vsan_remote_datastore_ids=vsan_remote_datastore_ids,
            vsan_unmap_enabled=vsan_unmap_enabled,
            vsan_verbose_mode_enabled=vsan_verbose_mode_enabled,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putVsanDiskGroup")
    def put_vsan_disk_group(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeClusterVsanDiskGroup", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c476472cf56c38050ef7fc3b5230f0b5932ce7fa283d87dd7fb05a0a75d9632a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVsanDiskGroup", [value]))

    @jsii.member(jsii_name="resetCustomAttributes")
    def reset_custom_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomAttributes", []))

    @jsii.member(jsii_name="resetDpmAutomationLevel")
    def reset_dpm_automation_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDpmAutomationLevel", []))

    @jsii.member(jsii_name="resetDpmEnabled")
    def reset_dpm_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDpmEnabled", []))

    @jsii.member(jsii_name="resetDpmThreshold")
    def reset_dpm_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDpmThreshold", []))

    @jsii.member(jsii_name="resetDrsAdvancedOptions")
    def reset_drs_advanced_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrsAdvancedOptions", []))

    @jsii.member(jsii_name="resetDrsAutomationLevel")
    def reset_drs_automation_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrsAutomationLevel", []))

    @jsii.member(jsii_name="resetDrsEnabled")
    def reset_drs_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrsEnabled", []))

    @jsii.member(jsii_name="resetDrsEnablePredictiveDrs")
    def reset_drs_enable_predictive_drs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrsEnablePredictiveDrs", []))

    @jsii.member(jsii_name="resetDrsEnableVmOverrides")
    def reset_drs_enable_vm_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrsEnableVmOverrides", []))

    @jsii.member(jsii_name="resetDrsMigrationThreshold")
    def reset_drs_migration_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrsMigrationThreshold", []))

    @jsii.member(jsii_name="resetDrsScaleDescendantsShares")
    def reset_drs_scale_descendants_shares(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDrsScaleDescendantsShares", []))

    @jsii.member(jsii_name="resetFolder")
    def reset_folder(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFolder", []))

    @jsii.member(jsii_name="resetForceEvacuateOnDestroy")
    def reset_force_evacuate_on_destroy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceEvacuateOnDestroy", []))

    @jsii.member(jsii_name="resetHaAdmissionControlFailoverHostSystemIds")
    def reset_ha_admission_control_failover_host_system_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaAdmissionControlFailoverHostSystemIds", []))

    @jsii.member(jsii_name="resetHaAdmissionControlHostFailureTolerance")
    def reset_ha_admission_control_host_failure_tolerance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaAdmissionControlHostFailureTolerance", []))

    @jsii.member(jsii_name="resetHaAdmissionControlPerformanceTolerance")
    def reset_ha_admission_control_performance_tolerance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaAdmissionControlPerformanceTolerance", []))

    @jsii.member(jsii_name="resetHaAdmissionControlPolicy")
    def reset_ha_admission_control_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaAdmissionControlPolicy", []))

    @jsii.member(jsii_name="resetHaAdmissionControlResourcePercentageAutoCompute")
    def reset_ha_admission_control_resource_percentage_auto_compute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaAdmissionControlResourcePercentageAutoCompute", []))

    @jsii.member(jsii_name="resetHaAdmissionControlResourcePercentageCpu")
    def reset_ha_admission_control_resource_percentage_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaAdmissionControlResourcePercentageCpu", []))

    @jsii.member(jsii_name="resetHaAdmissionControlResourcePercentageMemory")
    def reset_ha_admission_control_resource_percentage_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaAdmissionControlResourcePercentageMemory", []))

    @jsii.member(jsii_name="resetHaAdmissionControlSlotPolicyExplicitCpu")
    def reset_ha_admission_control_slot_policy_explicit_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaAdmissionControlSlotPolicyExplicitCpu", []))

    @jsii.member(jsii_name="resetHaAdmissionControlSlotPolicyExplicitMemory")
    def reset_ha_admission_control_slot_policy_explicit_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaAdmissionControlSlotPolicyExplicitMemory", []))

    @jsii.member(jsii_name="resetHaAdmissionControlSlotPolicyUseExplicitSize")
    def reset_ha_admission_control_slot_policy_use_explicit_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaAdmissionControlSlotPolicyUseExplicitSize", []))

    @jsii.member(jsii_name="resetHaAdvancedOptions")
    def reset_ha_advanced_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaAdvancedOptions", []))

    @jsii.member(jsii_name="resetHaDatastoreApdRecoveryAction")
    def reset_ha_datastore_apd_recovery_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaDatastoreApdRecoveryAction", []))

    @jsii.member(jsii_name="resetHaDatastoreApdResponse")
    def reset_ha_datastore_apd_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaDatastoreApdResponse", []))

    @jsii.member(jsii_name="resetHaDatastoreApdResponseDelay")
    def reset_ha_datastore_apd_response_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaDatastoreApdResponseDelay", []))

    @jsii.member(jsii_name="resetHaDatastorePdlResponse")
    def reset_ha_datastore_pdl_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaDatastorePdlResponse", []))

    @jsii.member(jsii_name="resetHaEnabled")
    def reset_ha_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaEnabled", []))

    @jsii.member(jsii_name="resetHaHeartbeatDatastoreIds")
    def reset_ha_heartbeat_datastore_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaHeartbeatDatastoreIds", []))

    @jsii.member(jsii_name="resetHaHeartbeatDatastorePolicy")
    def reset_ha_heartbeat_datastore_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaHeartbeatDatastorePolicy", []))

    @jsii.member(jsii_name="resetHaHostIsolationResponse")
    def reset_ha_host_isolation_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaHostIsolationResponse", []))

    @jsii.member(jsii_name="resetHaHostMonitoring")
    def reset_ha_host_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaHostMonitoring", []))

    @jsii.member(jsii_name="resetHaVmComponentProtection")
    def reset_ha_vm_component_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaVmComponentProtection", []))

    @jsii.member(jsii_name="resetHaVmDependencyRestartCondition")
    def reset_ha_vm_dependency_restart_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaVmDependencyRestartCondition", []))

    @jsii.member(jsii_name="resetHaVmFailureInterval")
    def reset_ha_vm_failure_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaVmFailureInterval", []))

    @jsii.member(jsii_name="resetHaVmMaximumFailureWindow")
    def reset_ha_vm_maximum_failure_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaVmMaximumFailureWindow", []))

    @jsii.member(jsii_name="resetHaVmMaximumResets")
    def reset_ha_vm_maximum_resets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaVmMaximumResets", []))

    @jsii.member(jsii_name="resetHaVmMinimumUptime")
    def reset_ha_vm_minimum_uptime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaVmMinimumUptime", []))

    @jsii.member(jsii_name="resetHaVmMonitoring")
    def reset_ha_vm_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaVmMonitoring", []))

    @jsii.member(jsii_name="resetHaVmRestartAdditionalDelay")
    def reset_ha_vm_restart_additional_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaVmRestartAdditionalDelay", []))

    @jsii.member(jsii_name="resetHaVmRestartPriority")
    def reset_ha_vm_restart_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaVmRestartPriority", []))

    @jsii.member(jsii_name="resetHaVmRestartTimeout")
    def reset_ha_vm_restart_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHaVmRestartTimeout", []))

    @jsii.member(jsii_name="resetHostClusterExitTimeout")
    def reset_host_cluster_exit_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostClusterExitTimeout", []))

    @jsii.member(jsii_name="resetHostManaged")
    def reset_host_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostManaged", []))

    @jsii.member(jsii_name="resetHostSystemIds")
    def reset_host_system_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostSystemIds", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProactiveHaAutomationLevel")
    def reset_proactive_ha_automation_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProactiveHaAutomationLevel", []))

    @jsii.member(jsii_name="resetProactiveHaEnabled")
    def reset_proactive_ha_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProactiveHaEnabled", []))

    @jsii.member(jsii_name="resetProactiveHaModerateRemediation")
    def reset_proactive_ha_moderate_remediation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProactiveHaModerateRemediation", []))

    @jsii.member(jsii_name="resetProactiveHaProviderIds")
    def reset_proactive_ha_provider_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProactiveHaProviderIds", []))

    @jsii.member(jsii_name="resetProactiveHaSevereRemediation")
    def reset_proactive_ha_severe_remediation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProactiveHaSevereRemediation", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetVsanCompressionEnabled")
    def reset_vsan_compression_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsanCompressionEnabled", []))

    @jsii.member(jsii_name="resetVsanDedupEnabled")
    def reset_vsan_dedup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsanDedupEnabled", []))

    @jsii.member(jsii_name="resetVsanDiskGroup")
    def reset_vsan_disk_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsanDiskGroup", []))

    @jsii.member(jsii_name="resetVsanDitEncryptionEnabled")
    def reset_vsan_dit_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsanDitEncryptionEnabled", []))

    @jsii.member(jsii_name="resetVsanDitRekeyInterval")
    def reset_vsan_dit_rekey_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsanDitRekeyInterval", []))

    @jsii.member(jsii_name="resetVsanEnabled")
    def reset_vsan_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsanEnabled", []))

    @jsii.member(jsii_name="resetVsanNetworkDiagnosticModeEnabled")
    def reset_vsan_network_diagnostic_mode_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsanNetworkDiagnosticModeEnabled", []))

    @jsii.member(jsii_name="resetVsanPerformanceEnabled")
    def reset_vsan_performance_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsanPerformanceEnabled", []))

    @jsii.member(jsii_name="resetVsanRemoteDatastoreIds")
    def reset_vsan_remote_datastore_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsanRemoteDatastoreIds", []))

    @jsii.member(jsii_name="resetVsanUnmapEnabled")
    def reset_vsan_unmap_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsanUnmapEnabled", []))

    @jsii.member(jsii_name="resetVsanVerboseModeEnabled")
    def reset_vsan_verbose_mode_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVsanVerboseModeEnabled", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="resourcePoolId")
    def resource_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourcePoolId"))

    @builtins.property
    @jsii.member(jsii_name="vsanDiskGroup")
    def vsan_disk_group(self) -> "ComputeClusterVsanDiskGroupList":
        return typing.cast("ComputeClusterVsanDiskGroupList", jsii.get(self, "vsanDiskGroup"))

    @builtins.property
    @jsii.member(jsii_name="customAttributesInput")
    def custom_attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "customAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="datacenterIdInput")
    def datacenter_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datacenterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dpmAutomationLevelInput")
    def dpm_automation_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dpmAutomationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="dpmEnabledInput")
    def dpm_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dpmEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dpmThresholdInput")
    def dpm_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dpmThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="drsAdvancedOptionsInput")
    def drs_advanced_options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "drsAdvancedOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="drsAutomationLevelInput")
    def drs_automation_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "drsAutomationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="drsEnabledInput")
    def drs_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "drsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="drsEnablePredictiveDrsInput")
    def drs_enable_predictive_drs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "drsEnablePredictiveDrsInput"))

    @builtins.property
    @jsii.member(jsii_name="drsEnableVmOverridesInput")
    def drs_enable_vm_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "drsEnableVmOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="drsMigrationThresholdInput")
    def drs_migration_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "drsMigrationThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="drsScaleDescendantsSharesInput")
    def drs_scale_descendants_shares_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "drsScaleDescendantsSharesInput"))

    @builtins.property
    @jsii.member(jsii_name="folderInput")
    def folder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "folderInput"))

    @builtins.property
    @jsii.member(jsii_name="forceEvacuateOnDestroyInput")
    def force_evacuate_on_destroy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceEvacuateOnDestroyInput"))

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlFailoverHostSystemIdsInput")
    def ha_admission_control_failover_host_system_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "haAdmissionControlFailoverHostSystemIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlHostFailureToleranceInput")
    def ha_admission_control_host_failure_tolerance_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haAdmissionControlHostFailureToleranceInput"))

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlPerformanceToleranceInput")
    def ha_admission_control_performance_tolerance_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haAdmissionControlPerformanceToleranceInput"))

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlPolicyInput")
    def ha_admission_control_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haAdmissionControlPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlResourcePercentageAutoComputeInput")
    def ha_admission_control_resource_percentage_auto_compute_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "haAdmissionControlResourcePercentageAutoComputeInput"))

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlResourcePercentageCpuInput")
    def ha_admission_control_resource_percentage_cpu_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haAdmissionControlResourcePercentageCpuInput"))

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlResourcePercentageMemoryInput")
    def ha_admission_control_resource_percentage_memory_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haAdmissionControlResourcePercentageMemoryInput"))

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlSlotPolicyExplicitCpuInput")
    def ha_admission_control_slot_policy_explicit_cpu_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haAdmissionControlSlotPolicyExplicitCpuInput"))

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlSlotPolicyExplicitMemoryInput")
    def ha_admission_control_slot_policy_explicit_memory_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haAdmissionControlSlotPolicyExplicitMemoryInput"))

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlSlotPolicyUseExplicitSizeInput")
    def ha_admission_control_slot_policy_use_explicit_size_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "haAdmissionControlSlotPolicyUseExplicitSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="haAdvancedOptionsInput")
    def ha_advanced_options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "haAdvancedOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="haDatastoreApdRecoveryActionInput")
    def ha_datastore_apd_recovery_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haDatastoreApdRecoveryActionInput"))

    @builtins.property
    @jsii.member(jsii_name="haDatastoreApdResponseDelayInput")
    def ha_datastore_apd_response_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haDatastoreApdResponseDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="haDatastoreApdResponseInput")
    def ha_datastore_apd_response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haDatastoreApdResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="haDatastorePdlResponseInput")
    def ha_datastore_pdl_response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haDatastorePdlResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="haEnabledInput")
    def ha_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "haEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="haHeartbeatDatastoreIdsInput")
    def ha_heartbeat_datastore_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "haHeartbeatDatastoreIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="haHeartbeatDatastorePolicyInput")
    def ha_heartbeat_datastore_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haHeartbeatDatastorePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="haHostIsolationResponseInput")
    def ha_host_isolation_response_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haHostIsolationResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="haHostMonitoringInput")
    def ha_host_monitoring_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haHostMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="haVmComponentProtectionInput")
    def ha_vm_component_protection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haVmComponentProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="haVmDependencyRestartConditionInput")
    def ha_vm_dependency_restart_condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haVmDependencyRestartConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="haVmFailureIntervalInput")
    def ha_vm_failure_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haVmFailureIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="haVmMaximumFailureWindowInput")
    def ha_vm_maximum_failure_window_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haVmMaximumFailureWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="haVmMaximumResetsInput")
    def ha_vm_maximum_resets_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haVmMaximumResetsInput"))

    @builtins.property
    @jsii.member(jsii_name="haVmMinimumUptimeInput")
    def ha_vm_minimum_uptime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haVmMinimumUptimeInput"))

    @builtins.property
    @jsii.member(jsii_name="haVmMonitoringInput")
    def ha_vm_monitoring_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haVmMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="haVmRestartAdditionalDelayInput")
    def ha_vm_restart_additional_delay_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haVmRestartAdditionalDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="haVmRestartPriorityInput")
    def ha_vm_restart_priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "haVmRestartPriorityInput"))

    @builtins.property
    @jsii.member(jsii_name="haVmRestartTimeoutInput")
    def ha_vm_restart_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "haVmRestartTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="hostClusterExitTimeoutInput")
    def host_cluster_exit_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hostClusterExitTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="hostManagedInput")
    def host_managed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "hostManagedInput"))

    @builtins.property
    @jsii.member(jsii_name="hostSystemIdsInput")
    def host_system_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostSystemIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="proactiveHaAutomationLevelInput")
    def proactive_ha_automation_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proactiveHaAutomationLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="proactiveHaEnabledInput")
    def proactive_ha_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "proactiveHaEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="proactiveHaModerateRemediationInput")
    def proactive_ha_moderate_remediation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proactiveHaModerateRemediationInput"))

    @builtins.property
    @jsii.member(jsii_name="proactiveHaProviderIdsInput")
    def proactive_ha_provider_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "proactiveHaProviderIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="proactiveHaSevereRemediationInput")
    def proactive_ha_severe_remediation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proactiveHaSevereRemediationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="vsanCompressionEnabledInput")
    def vsan_compression_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vsanCompressionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="vsanDedupEnabledInput")
    def vsan_dedup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vsanDedupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="vsanDiskGroupInput")
    def vsan_disk_group_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeClusterVsanDiskGroup"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeClusterVsanDiskGroup"]]], jsii.get(self, "vsanDiskGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="vsanDitEncryptionEnabledInput")
    def vsan_dit_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vsanDitEncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="vsanDitRekeyIntervalInput")
    def vsan_dit_rekey_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vsanDitRekeyIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="vsanEnabledInput")
    def vsan_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vsanEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="vsanNetworkDiagnosticModeEnabledInput")
    def vsan_network_diagnostic_mode_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vsanNetworkDiagnosticModeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="vsanPerformanceEnabledInput")
    def vsan_performance_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vsanPerformanceEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="vsanRemoteDatastoreIdsInput")
    def vsan_remote_datastore_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vsanRemoteDatastoreIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="vsanUnmapEnabledInput")
    def vsan_unmap_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vsanUnmapEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="vsanVerboseModeEnabledInput")
    def vsan_verbose_mode_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vsanVerboseModeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="customAttributes")
    def custom_attributes(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "customAttributes"))

    @custom_attributes.setter
    def custom_attributes(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c986ac1347f1ac017672faf4123302fbbc7bce9b1164f0f14ed96458b25f43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="datacenterId")
    def datacenter_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datacenterId"))

    @datacenter_id.setter
    def datacenter_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c343c1448f143a69b31c958b864d46dfddae7974f9fffa7df6c369b35cbbe8a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datacenterId", value)

    @builtins.property
    @jsii.member(jsii_name="dpmAutomationLevel")
    def dpm_automation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dpmAutomationLevel"))

    @dpm_automation_level.setter
    def dpm_automation_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d33189b0374fbe3c2be40cec4db145710ca7ad94a7f2dc253a10657bda8bfb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dpmAutomationLevel", value)

    @builtins.property
    @jsii.member(jsii_name="dpmEnabled")
    def dpm_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dpmEnabled"))

    @dpm_enabled.setter
    def dpm_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__707352eec66304de0f2eadee9af4e003a76f57c1a5844539ecf64daf68db8487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dpmEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="dpmThreshold")
    def dpm_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dpmThreshold"))

    @dpm_threshold.setter
    def dpm_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c1e774067ea40929ffabdb358793ea7ea3e26473c32a91f227b6bfe6e12fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dpmThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="drsAdvancedOptions")
    def drs_advanced_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "drsAdvancedOptions"))

    @drs_advanced_options.setter
    def drs_advanced_options(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7187a17eb296c36237433c401fd3c8c76fb683d591e0768d8bd87b604ff60a27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drsAdvancedOptions", value)

    @builtins.property
    @jsii.member(jsii_name="drsAutomationLevel")
    def drs_automation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "drsAutomationLevel"))

    @drs_automation_level.setter
    def drs_automation_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c839fa263f8ebb3a27de8e5dcb7f1a7031e999bdd63ba0158e81f2ed4c03100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drsAutomationLevel", value)

    @builtins.property
    @jsii.member(jsii_name="drsEnabled")
    def drs_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "drsEnabled"))

    @drs_enabled.setter
    def drs_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9887b6cdef2e9ad2dd5dfef89d9dde3015a42b4612446af8d61b7af185635a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="drsEnablePredictiveDrs")
    def drs_enable_predictive_drs(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "drsEnablePredictiveDrs"))

    @drs_enable_predictive_drs.setter
    def drs_enable_predictive_drs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7b74ee1e1bd5e7f9535b23068964aa958cabdfd5e50d14f098f2f6d51110d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drsEnablePredictiveDrs", value)

    @builtins.property
    @jsii.member(jsii_name="drsEnableVmOverrides")
    def drs_enable_vm_overrides(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "drsEnableVmOverrides"))

    @drs_enable_vm_overrides.setter
    def drs_enable_vm_overrides(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff2192ea7f018c7d0ece28876fa8efcb1d8ac23c80c15fffdef28c9d197b84df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drsEnableVmOverrides", value)

    @builtins.property
    @jsii.member(jsii_name="drsMigrationThreshold")
    def drs_migration_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "drsMigrationThreshold"))

    @drs_migration_threshold.setter
    def drs_migration_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b0454732bc285dbaba92a81b31de5d49b2a9fc33fd89469d7a19d8b4ad4db9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drsMigrationThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="drsScaleDescendantsShares")
    def drs_scale_descendants_shares(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "drsScaleDescendantsShares"))

    @drs_scale_descendants_shares.setter
    def drs_scale_descendants_shares(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c26eda8cdc5f00bf916026350c44e5382ce2a2dfe0f9c15a6e16d50dccbe22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "drsScaleDescendantsShares", value)

    @builtins.property
    @jsii.member(jsii_name="folder")
    def folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folder"))

    @folder.setter
    def folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf7eb82a5a878358836d5e18a0656728c42043482bd19bbb0c8a2df859d9c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folder", value)

    @builtins.property
    @jsii.member(jsii_name="forceEvacuateOnDestroy")
    def force_evacuate_on_destroy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceEvacuateOnDestroy"))

    @force_evacuate_on_destroy.setter
    def force_evacuate_on_destroy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dae9d17db92f75826a81710df799736ab4f90e72a766b98ada366a823a534cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceEvacuateOnDestroy", value)

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlFailoverHostSystemIds")
    def ha_admission_control_failover_host_system_ids(
        self,
    ) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "haAdmissionControlFailoverHostSystemIds"))

    @ha_admission_control_failover_host_system_ids.setter
    def ha_admission_control_failover_host_system_ids(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad265b6c2347b64d68e538f074ee0361326396fad9af93c84c333a36d656fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haAdmissionControlFailoverHostSystemIds", value)

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlHostFailureTolerance")
    def ha_admission_control_host_failure_tolerance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haAdmissionControlHostFailureTolerance"))

    @ha_admission_control_host_failure_tolerance.setter
    def ha_admission_control_host_failure_tolerance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1442bc28bb0e33d2cd42b40d648d4ea33d482585b47f3bf1dd22b5412075c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haAdmissionControlHostFailureTolerance", value)

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlPerformanceTolerance")
    def ha_admission_control_performance_tolerance(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haAdmissionControlPerformanceTolerance"))

    @ha_admission_control_performance_tolerance.setter
    def ha_admission_control_performance_tolerance(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb9be7f1d7dcf6c08708b2721537dd3c621f97ed479291c080a074637b049e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haAdmissionControlPerformanceTolerance", value)

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlPolicy")
    def ha_admission_control_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haAdmissionControlPolicy"))

    @ha_admission_control_policy.setter
    def ha_admission_control_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd432a71f5e280fcf4bb2504eca535920f46365f47a9d7e737fd224aa0f3bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haAdmissionControlPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlResourcePercentageAutoCompute")
    def ha_admission_control_resource_percentage_auto_compute(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "haAdmissionControlResourcePercentageAutoCompute"))

    @ha_admission_control_resource_percentage_auto_compute.setter
    def ha_admission_control_resource_percentage_auto_compute(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ffc69951522f724a25389f97e9f5d8a838d793f3e3901d0146bfaa897814b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haAdmissionControlResourcePercentageAutoCompute", value)

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlResourcePercentageCpu")
    def ha_admission_control_resource_percentage_cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haAdmissionControlResourcePercentageCpu"))

    @ha_admission_control_resource_percentage_cpu.setter
    def ha_admission_control_resource_percentage_cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e845b1b7b14e35a31eb54099f21ae7139a0925255ca7acecb5828a9a939e0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haAdmissionControlResourcePercentageCpu", value)

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlResourcePercentageMemory")
    def ha_admission_control_resource_percentage_memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haAdmissionControlResourcePercentageMemory"))

    @ha_admission_control_resource_percentage_memory.setter
    def ha_admission_control_resource_percentage_memory(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837205521ec9eb6c2b2d34008dd5f85dcfdac37c17f1bea5768dd38872a88fcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haAdmissionControlResourcePercentageMemory", value)

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlSlotPolicyExplicitCpu")
    def ha_admission_control_slot_policy_explicit_cpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haAdmissionControlSlotPolicyExplicitCpu"))

    @ha_admission_control_slot_policy_explicit_cpu.setter
    def ha_admission_control_slot_policy_explicit_cpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73d6f69e3b0ac9e3e25e6c1cde284c79214cfa8bdb94cd141af90d454993e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haAdmissionControlSlotPolicyExplicitCpu", value)

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlSlotPolicyExplicitMemory")
    def ha_admission_control_slot_policy_explicit_memory(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haAdmissionControlSlotPolicyExplicitMemory"))

    @ha_admission_control_slot_policy_explicit_memory.setter
    def ha_admission_control_slot_policy_explicit_memory(
        self,
        value: jsii.Number,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ad6dcf8ece606f787014482ff21bdbb8a7df3c41d0f93ada2b9ad2b52022f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haAdmissionControlSlotPolicyExplicitMemory", value)

    @builtins.property
    @jsii.member(jsii_name="haAdmissionControlSlotPolicyUseExplicitSize")
    def ha_admission_control_slot_policy_use_explicit_size(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "haAdmissionControlSlotPolicyUseExplicitSize"))

    @ha_admission_control_slot_policy_use_explicit_size.setter
    def ha_admission_control_slot_policy_use_explicit_size(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224d04a8970ad94372dcc80236e730c519e1678eafa90981e12eeea8c200c4b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haAdmissionControlSlotPolicyUseExplicitSize", value)

    @builtins.property
    @jsii.member(jsii_name="haAdvancedOptions")
    def ha_advanced_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "haAdvancedOptions"))

    @ha_advanced_options.setter
    def ha_advanced_options(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce3dcc6e54f9ee00e27730c3e2bb3a12b83232fdae5fb4efe55b4ae414f7641)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haAdvancedOptions", value)

    @builtins.property
    @jsii.member(jsii_name="haDatastoreApdRecoveryAction")
    def ha_datastore_apd_recovery_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haDatastoreApdRecoveryAction"))

    @ha_datastore_apd_recovery_action.setter
    def ha_datastore_apd_recovery_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f6bec720ca52fba92522906b15e26ada26fbe9cd218a02b3bece35ee63ddfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haDatastoreApdRecoveryAction", value)

    @builtins.property
    @jsii.member(jsii_name="haDatastoreApdResponse")
    def ha_datastore_apd_response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haDatastoreApdResponse"))

    @ha_datastore_apd_response.setter
    def ha_datastore_apd_response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e83ccf5ff27f38a6147a63c5b8c851884abae02fc238d71eb5c87d23ec604e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haDatastoreApdResponse", value)

    @builtins.property
    @jsii.member(jsii_name="haDatastoreApdResponseDelay")
    def ha_datastore_apd_response_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haDatastoreApdResponseDelay"))

    @ha_datastore_apd_response_delay.setter
    def ha_datastore_apd_response_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e84ca52dd6b15213fbfbe4773663b7605f55623db4d788eb6146fc00f9e595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haDatastoreApdResponseDelay", value)

    @builtins.property
    @jsii.member(jsii_name="haDatastorePdlResponse")
    def ha_datastore_pdl_response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haDatastorePdlResponse"))

    @ha_datastore_pdl_response.setter
    def ha_datastore_pdl_response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02dba7880be945dd467836edb4f141029712d75f436f4adbdd97ae867f08aa12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haDatastorePdlResponse", value)

    @builtins.property
    @jsii.member(jsii_name="haEnabled")
    def ha_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "haEnabled"))

    @ha_enabled.setter
    def ha_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec3f28fd9011c7afbc9445c14abd9c8d55aee5a3b7ab7abd9e0b158e53e9bc9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="haHeartbeatDatastoreIds")
    def ha_heartbeat_datastore_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "haHeartbeatDatastoreIds"))

    @ha_heartbeat_datastore_ids.setter
    def ha_heartbeat_datastore_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08179ce56a36cf203292fe7280b4a23967e48f0bfa7f2c6a1062b4ea0284937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haHeartbeatDatastoreIds", value)

    @builtins.property
    @jsii.member(jsii_name="haHeartbeatDatastorePolicy")
    def ha_heartbeat_datastore_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haHeartbeatDatastorePolicy"))

    @ha_heartbeat_datastore_policy.setter
    def ha_heartbeat_datastore_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f99378c4b8de7eabbb20c1942243269c53c07081fada387a184dca0825febd01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haHeartbeatDatastorePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="haHostIsolationResponse")
    def ha_host_isolation_response(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haHostIsolationResponse"))

    @ha_host_isolation_response.setter
    def ha_host_isolation_response(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbd5b3106f8bdf4c1ac37cceeb32315af12fde1d17ff188cff9f3ffc182f2917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haHostIsolationResponse", value)

    @builtins.property
    @jsii.member(jsii_name="haHostMonitoring")
    def ha_host_monitoring(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haHostMonitoring"))

    @ha_host_monitoring.setter
    def ha_host_monitoring(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ada4ab30bc7f6b407ce7ac7ed6ee2d50720af9abfb56d3071eb80825d968159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haHostMonitoring", value)

    @builtins.property
    @jsii.member(jsii_name="haVmComponentProtection")
    def ha_vm_component_protection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haVmComponentProtection"))

    @ha_vm_component_protection.setter
    def ha_vm_component_protection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf0761e0463e08af0bab58c4213fdbe6dcb23134d714163affe04c5958b0500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haVmComponentProtection", value)

    @builtins.property
    @jsii.member(jsii_name="haVmDependencyRestartCondition")
    def ha_vm_dependency_restart_condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haVmDependencyRestartCondition"))

    @ha_vm_dependency_restart_condition.setter
    def ha_vm_dependency_restart_condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__616328225b77065904ea66e6cc68e56355968f6e120208a9b77f65f35ce4f2a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haVmDependencyRestartCondition", value)

    @builtins.property
    @jsii.member(jsii_name="haVmFailureInterval")
    def ha_vm_failure_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haVmFailureInterval"))

    @ha_vm_failure_interval.setter
    def ha_vm_failure_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c6ff7617b7a2b7afd5cb3ddaa5637b97296ee0d9644a827d855187e25cf8b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haVmFailureInterval", value)

    @builtins.property
    @jsii.member(jsii_name="haVmMaximumFailureWindow")
    def ha_vm_maximum_failure_window(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haVmMaximumFailureWindow"))

    @ha_vm_maximum_failure_window.setter
    def ha_vm_maximum_failure_window(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880cd1d984000531a36f9143c7a5935a830d7ec4182ca2b190d9cd5193ebe6ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haVmMaximumFailureWindow", value)

    @builtins.property
    @jsii.member(jsii_name="haVmMaximumResets")
    def ha_vm_maximum_resets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haVmMaximumResets"))

    @ha_vm_maximum_resets.setter
    def ha_vm_maximum_resets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3369252caca237d8aaa106287e47b52a3e802bdfe88136cccd42e11908940943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haVmMaximumResets", value)

    @builtins.property
    @jsii.member(jsii_name="haVmMinimumUptime")
    def ha_vm_minimum_uptime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haVmMinimumUptime"))

    @ha_vm_minimum_uptime.setter
    def ha_vm_minimum_uptime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a42eb2ed30e4cb4bd3665d074a3d6f5e7844bdb3fe3564e86c8e54cfe1a259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haVmMinimumUptime", value)

    @builtins.property
    @jsii.member(jsii_name="haVmMonitoring")
    def ha_vm_monitoring(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haVmMonitoring"))

    @ha_vm_monitoring.setter
    def ha_vm_monitoring(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db82a70df820c72696906e66a61fb9304b651605f7d2c48afe64386ec9ce5c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haVmMonitoring", value)

    @builtins.property
    @jsii.member(jsii_name="haVmRestartAdditionalDelay")
    def ha_vm_restart_additional_delay(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haVmRestartAdditionalDelay"))

    @ha_vm_restart_additional_delay.setter
    def ha_vm_restart_additional_delay(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c43aa4deb2fc8affe6d8f89a7894d2b51240ca859ccb1479f864a1a1fe8a93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haVmRestartAdditionalDelay", value)

    @builtins.property
    @jsii.member(jsii_name="haVmRestartPriority")
    def ha_vm_restart_priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "haVmRestartPriority"))

    @ha_vm_restart_priority.setter
    def ha_vm_restart_priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848a31618ecc15ab26a82251da2f6d3ad8eac851cb096fc491d2f1f9a5e0098f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haVmRestartPriority", value)

    @builtins.property
    @jsii.member(jsii_name="haVmRestartTimeout")
    def ha_vm_restart_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haVmRestartTimeout"))

    @ha_vm_restart_timeout.setter
    def ha_vm_restart_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a306ec95f458fe3e6f547ddf6365625d07c410a272b93fe31726baa1748d53d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "haVmRestartTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="hostClusterExitTimeout")
    def host_cluster_exit_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hostClusterExitTimeout"))

    @host_cluster_exit_timeout.setter
    def host_cluster_exit_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9da73662d1bbdd5a4ffdc9b55b716922288ed0e03955ae61fa629eac06b1cfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostClusterExitTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="hostManaged")
    def host_managed(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "hostManaged"))

    @host_managed.setter
    def host_managed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3cff929d67a6c645cfedc6e9824560ac3256ddb2cb1fa5b8c8a1094c320047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostManaged", value)

    @builtins.property
    @jsii.member(jsii_name="hostSystemIds")
    def host_system_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostSystemIds"))

    @host_system_ids.setter
    def host_system_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8750e6171d665b35361bbfc971bd57b887940bb2a0e78bf6f0ae2c41fa97c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostSystemIds", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f80285c58a96bccbb67d68fe192d828ca65a97bd328decad4863cfb6ceca2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__031c54b8f7314c12c4ae3444934e5f6bb9500bd7bb062fef339ade8fd406682d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="proactiveHaAutomationLevel")
    def proactive_ha_automation_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proactiveHaAutomationLevel"))

    @proactive_ha_automation_level.setter
    def proactive_ha_automation_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__867680882efc9a70a2a980dbd2dd65d2ac0fe1c1b2a3a723c081fe1b69486d43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proactiveHaAutomationLevel", value)

    @builtins.property
    @jsii.member(jsii_name="proactiveHaEnabled")
    def proactive_ha_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "proactiveHaEnabled"))

    @proactive_ha_enabled.setter
    def proactive_ha_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58a25b734f4d8da20846ee2d80d87acf9400fc3228458b325c1734724d4eaff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proactiveHaEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="proactiveHaModerateRemediation")
    def proactive_ha_moderate_remediation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proactiveHaModerateRemediation"))

    @proactive_ha_moderate_remediation.setter
    def proactive_ha_moderate_remediation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e7fc159385fc109ae43145d351440ea3ca5417f8c60ca61b1a1048c4f7cd6d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proactiveHaModerateRemediation", value)

    @builtins.property
    @jsii.member(jsii_name="proactiveHaProviderIds")
    def proactive_ha_provider_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "proactiveHaProviderIds"))

    @proactive_ha_provider_ids.setter
    def proactive_ha_provider_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb51707ae0e856f0874b53cc29c282cdde062aeeae3d6c19bab027020cb8ad50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proactiveHaProviderIds", value)

    @builtins.property
    @jsii.member(jsii_name="proactiveHaSevereRemediation")
    def proactive_ha_severe_remediation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proactiveHaSevereRemediation"))

    @proactive_ha_severe_remediation.setter
    def proactive_ha_severe_remediation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5feaef7eb6df7bd000f7fc5d7d913c482c73beb1783b6c1693e16cd6d30580f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proactiveHaSevereRemediation", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e71eea758dd8974e4ff9b243c975eb1971d0c3cf231a6d245cc486141cd4f5ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="vsanCompressionEnabled")
    def vsan_compression_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vsanCompressionEnabled"))

    @vsan_compression_enabled.setter
    def vsan_compression_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f64f42159cf18562bf8c143c116674beb576752c669c76f190c15ba7ab8f68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsanCompressionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="vsanDedupEnabled")
    def vsan_dedup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vsanDedupEnabled"))

    @vsan_dedup_enabled.setter
    def vsan_dedup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360a441f446fb66a4faa7d22541ac5194186cb257ca1a32f413d63c24c64a8f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsanDedupEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="vsanDitEncryptionEnabled")
    def vsan_dit_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vsanDitEncryptionEnabled"))

    @vsan_dit_encryption_enabled.setter
    def vsan_dit_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e182f82aa76ab9b046ebf2c15467f72cf9d8fcd4f282a913c5b0ba9caeb9b016)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsanDitEncryptionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="vsanDitRekeyInterval")
    def vsan_dit_rekey_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vsanDitRekeyInterval"))

    @vsan_dit_rekey_interval.setter
    def vsan_dit_rekey_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bbc412e832ad297036276355a55954e48e2f66bde71aa50b7a56ff94c167e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsanDitRekeyInterval", value)

    @builtins.property
    @jsii.member(jsii_name="vsanEnabled")
    def vsan_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vsanEnabled"))

    @vsan_enabled.setter
    def vsan_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34281f63f4288e9443883af3acb9fb2f9f912a0bf900b78416165238651ec61a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsanEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="vsanNetworkDiagnosticModeEnabled")
    def vsan_network_diagnostic_mode_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vsanNetworkDiagnosticModeEnabled"))

    @vsan_network_diagnostic_mode_enabled.setter
    def vsan_network_diagnostic_mode_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9f0cb111783efabd48c4ec43e221e79ff7bd14385df60b6b4424c6c32e6b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsanNetworkDiagnosticModeEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="vsanPerformanceEnabled")
    def vsan_performance_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vsanPerformanceEnabled"))

    @vsan_performance_enabled.setter
    def vsan_performance_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ce6cdef835ccba366174f8abd9d30580ca1411612eb24f353dedd1685572ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsanPerformanceEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="vsanRemoteDatastoreIds")
    def vsan_remote_datastore_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vsanRemoteDatastoreIds"))

    @vsan_remote_datastore_ids.setter
    def vsan_remote_datastore_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e9f8dabf13df8b03bb59960f7e22963af7011ac32099ecc67c53ad8c76411c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsanRemoteDatastoreIds", value)

    @builtins.property
    @jsii.member(jsii_name="vsanUnmapEnabled")
    def vsan_unmap_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vsanUnmapEnabled"))

    @vsan_unmap_enabled.setter
    def vsan_unmap_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de5d736336237ed230b16335abb4faa51f4c6ca2cc68e03cf2feb036dbb14ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsanUnmapEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="vsanVerboseModeEnabled")
    def vsan_verbose_mode_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vsanVerboseModeEnabled"))

    @vsan_verbose_mode_enabled.setter
    def vsan_verbose_mode_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd4e3dc12850519ce445812a521e8bca0c8c103de7ef9ef661abc5e70cbafa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vsanVerboseModeEnabled", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vsphere.computeCluster.ComputeClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "datacenter_id": "datacenterId",
        "name": "name",
        "custom_attributes": "customAttributes",
        "dpm_automation_level": "dpmAutomationLevel",
        "dpm_enabled": "dpmEnabled",
        "dpm_threshold": "dpmThreshold",
        "drs_advanced_options": "drsAdvancedOptions",
        "drs_automation_level": "drsAutomationLevel",
        "drs_enabled": "drsEnabled",
        "drs_enable_predictive_drs": "drsEnablePredictiveDrs",
        "drs_enable_vm_overrides": "drsEnableVmOverrides",
        "drs_migration_threshold": "drsMigrationThreshold",
        "drs_scale_descendants_shares": "drsScaleDescendantsShares",
        "folder": "folder",
        "force_evacuate_on_destroy": "forceEvacuateOnDestroy",
        "ha_admission_control_failover_host_system_ids": "haAdmissionControlFailoverHostSystemIds",
        "ha_admission_control_host_failure_tolerance": "haAdmissionControlHostFailureTolerance",
        "ha_admission_control_performance_tolerance": "haAdmissionControlPerformanceTolerance",
        "ha_admission_control_policy": "haAdmissionControlPolicy",
        "ha_admission_control_resource_percentage_auto_compute": "haAdmissionControlResourcePercentageAutoCompute",
        "ha_admission_control_resource_percentage_cpu": "haAdmissionControlResourcePercentageCpu",
        "ha_admission_control_resource_percentage_memory": "haAdmissionControlResourcePercentageMemory",
        "ha_admission_control_slot_policy_explicit_cpu": "haAdmissionControlSlotPolicyExplicitCpu",
        "ha_admission_control_slot_policy_explicit_memory": "haAdmissionControlSlotPolicyExplicitMemory",
        "ha_admission_control_slot_policy_use_explicit_size": "haAdmissionControlSlotPolicyUseExplicitSize",
        "ha_advanced_options": "haAdvancedOptions",
        "ha_datastore_apd_recovery_action": "haDatastoreApdRecoveryAction",
        "ha_datastore_apd_response": "haDatastoreApdResponse",
        "ha_datastore_apd_response_delay": "haDatastoreApdResponseDelay",
        "ha_datastore_pdl_response": "haDatastorePdlResponse",
        "ha_enabled": "haEnabled",
        "ha_heartbeat_datastore_ids": "haHeartbeatDatastoreIds",
        "ha_heartbeat_datastore_policy": "haHeartbeatDatastorePolicy",
        "ha_host_isolation_response": "haHostIsolationResponse",
        "ha_host_monitoring": "haHostMonitoring",
        "ha_vm_component_protection": "haVmComponentProtection",
        "ha_vm_dependency_restart_condition": "haVmDependencyRestartCondition",
        "ha_vm_failure_interval": "haVmFailureInterval",
        "ha_vm_maximum_failure_window": "haVmMaximumFailureWindow",
        "ha_vm_maximum_resets": "haVmMaximumResets",
        "ha_vm_minimum_uptime": "haVmMinimumUptime",
        "ha_vm_monitoring": "haVmMonitoring",
        "ha_vm_restart_additional_delay": "haVmRestartAdditionalDelay",
        "ha_vm_restart_priority": "haVmRestartPriority",
        "ha_vm_restart_timeout": "haVmRestartTimeout",
        "host_cluster_exit_timeout": "hostClusterExitTimeout",
        "host_managed": "hostManaged",
        "host_system_ids": "hostSystemIds",
        "id": "id",
        "proactive_ha_automation_level": "proactiveHaAutomationLevel",
        "proactive_ha_enabled": "proactiveHaEnabled",
        "proactive_ha_moderate_remediation": "proactiveHaModerateRemediation",
        "proactive_ha_provider_ids": "proactiveHaProviderIds",
        "proactive_ha_severe_remediation": "proactiveHaSevereRemediation",
        "tags": "tags",
        "vsan_compression_enabled": "vsanCompressionEnabled",
        "vsan_dedup_enabled": "vsanDedupEnabled",
        "vsan_disk_group": "vsanDiskGroup",
        "vsan_dit_encryption_enabled": "vsanDitEncryptionEnabled",
        "vsan_dit_rekey_interval": "vsanDitRekeyInterval",
        "vsan_enabled": "vsanEnabled",
        "vsan_network_diagnostic_mode_enabled": "vsanNetworkDiagnosticModeEnabled",
        "vsan_performance_enabled": "vsanPerformanceEnabled",
        "vsan_remote_datastore_ids": "vsanRemoteDatastoreIds",
        "vsan_unmap_enabled": "vsanUnmapEnabled",
        "vsan_verbose_mode_enabled": "vsanVerboseModeEnabled",
    },
)
class ComputeClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        datacenter_id: builtins.str,
        name: builtins.str,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        dpm_automation_level: typing.Optional[builtins.str] = None,
        dpm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dpm_threshold: typing.Optional[jsii.Number] = None,
        drs_advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        drs_automation_level: typing.Optional[builtins.str] = None,
        drs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drs_enable_predictive_drs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drs_enable_vm_overrides: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        drs_migration_threshold: typing.Optional[jsii.Number] = None,
        drs_scale_descendants_shares: typing.Optional[builtins.str] = None,
        folder: typing.Optional[builtins.str] = None,
        force_evacuate_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ha_admission_control_failover_host_system_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ha_admission_control_host_failure_tolerance: typing.Optional[jsii.Number] = None,
        ha_admission_control_performance_tolerance: typing.Optional[jsii.Number] = None,
        ha_admission_control_policy: typing.Optional[builtins.str] = None,
        ha_admission_control_resource_percentage_auto_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ha_admission_control_resource_percentage_cpu: typing.Optional[jsii.Number] = None,
        ha_admission_control_resource_percentage_memory: typing.Optional[jsii.Number] = None,
        ha_admission_control_slot_policy_explicit_cpu: typing.Optional[jsii.Number] = None,
        ha_admission_control_slot_policy_explicit_memory: typing.Optional[jsii.Number] = None,
        ha_admission_control_slot_policy_use_explicit_size: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ha_advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        ha_datastore_apd_recovery_action: typing.Optional[builtins.str] = None,
        ha_datastore_apd_response: typing.Optional[builtins.str] = None,
        ha_datastore_apd_response_delay: typing.Optional[jsii.Number] = None,
        ha_datastore_pdl_response: typing.Optional[builtins.str] = None,
        ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ha_heartbeat_datastore_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ha_heartbeat_datastore_policy: typing.Optional[builtins.str] = None,
        ha_host_isolation_response: typing.Optional[builtins.str] = None,
        ha_host_monitoring: typing.Optional[builtins.str] = None,
        ha_vm_component_protection: typing.Optional[builtins.str] = None,
        ha_vm_dependency_restart_condition: typing.Optional[builtins.str] = None,
        ha_vm_failure_interval: typing.Optional[jsii.Number] = None,
        ha_vm_maximum_failure_window: typing.Optional[jsii.Number] = None,
        ha_vm_maximum_resets: typing.Optional[jsii.Number] = None,
        ha_vm_minimum_uptime: typing.Optional[jsii.Number] = None,
        ha_vm_monitoring: typing.Optional[builtins.str] = None,
        ha_vm_restart_additional_delay: typing.Optional[jsii.Number] = None,
        ha_vm_restart_priority: typing.Optional[builtins.str] = None,
        ha_vm_restart_timeout: typing.Optional[jsii.Number] = None,
        host_cluster_exit_timeout: typing.Optional[jsii.Number] = None,
        host_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        host_system_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        proactive_ha_automation_level: typing.Optional[builtins.str] = None,
        proactive_ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        proactive_ha_moderate_remediation: typing.Optional[builtins.str] = None,
        proactive_ha_provider_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        proactive_ha_severe_remediation: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        vsan_compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_dedup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_disk_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeClusterVsanDiskGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vsan_dit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_dit_rekey_interval: typing.Optional[jsii.Number] = None,
        vsan_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_network_diagnostic_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_performance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_remote_datastore_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        vsan_unmap_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vsan_verbose_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param datacenter_id: The managed object ID of the datacenter to put the cluster in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#datacenter_id ComputeCluster#datacenter_id}
        :param name: Name for the new cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#name ComputeCluster#name}
        :param custom_attributes: A list of custom attributes to set on this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#custom_attributes ComputeCluster#custom_attributes}
        :param dpm_automation_level: The automation level for host power operations in this cluster. Can be one of manual or automated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#dpm_automation_level ComputeCluster#dpm_automation_level}
        :param dpm_enabled: Enable DPM support for DRS. This allows you to dynamically control the power of hosts depending on the needs of virtual machines in the cluster. Requires that DRS be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#dpm_enabled ComputeCluster#dpm_enabled}
        :param dpm_threshold: A value between 1 and 5 indicating the threshold of load within the cluster that influences host power operations. This affects both power on and power off operations - a lower setting will tolerate more of a surplus/deficit than a higher setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#dpm_threshold ComputeCluster#dpm_threshold}
        :param drs_advanced_options: Advanced configuration options for DRS and DPM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_advanced_options ComputeCluster#drs_advanced_options}
        :param drs_automation_level: The default automation level for all virtual machines in this cluster. Can be one of manual, partiallyAutomated, or fullyAutomated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_automation_level ComputeCluster#drs_automation_level}
        :param drs_enabled: Enable DRS for this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_enabled ComputeCluster#drs_enabled}
        :param drs_enable_predictive_drs: When true, enables DRS to use data from vRealize Operations Manager to make proactive DRS recommendations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_enable_predictive_drs ComputeCluster#drs_enable_predictive_drs}
        :param drs_enable_vm_overrides: When true, allows individual VM overrides within this cluster to be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_enable_vm_overrides ComputeCluster#drs_enable_vm_overrides}
        :param drs_migration_threshold: A value between 1 and 5 indicating the threshold of imbalance tolerated between hosts. A lower setting will tolerate more imbalance while a higher setting will tolerate less. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_migration_threshold ComputeCluster#drs_migration_threshold}
        :param drs_scale_descendants_shares: Enable scalable shares for all descendants of this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_scale_descendants_shares ComputeCluster#drs_scale_descendants_shares}
        :param folder: The name of the folder to locate the cluster in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#folder ComputeCluster#folder}
        :param force_evacuate_on_destroy: Force removal of all hosts in the cluster during destroy and make them standalone hosts. Use of this flag mainly exists for testing and is not recommended in normal use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#force_evacuate_on_destroy ComputeCluster#force_evacuate_on_destroy}
        :param ha_admission_control_failover_host_system_ids: When ha_admission_control_policy is failoverHosts, this defines the managed object IDs of hosts to use as dedicated failover hosts. These hosts are kept as available as possible - admission control will block access to the host, and DRS will ignore the host when making recommendations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_failover_host_system_ids ComputeCluster#ha_admission_control_failover_host_system_ids}
        :param ha_admission_control_host_failure_tolerance: The maximum number of failed hosts that admission control tolerates when making decisions on whether to permit virtual machine operations. The maximum is one less than the number of hosts in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_host_failure_tolerance ComputeCluster#ha_admission_control_host_failure_tolerance}
        :param ha_admission_control_performance_tolerance: The percentage of resource reduction that a cluster of VMs can tolerate in case of a failover. A value of 0 produces warnings only, whereas a value of 100 disables the setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_performance_tolerance ComputeCluster#ha_admission_control_performance_tolerance}
        :param ha_admission_control_policy: The type of admission control policy to use with vSphere HA, which controls whether or not specific VM operations are permitted in the cluster in order to protect the reliability of the cluster. Can be one of resourcePercentage, slotPolicy, failoverHosts, or disabled. Note that disabling admission control is not recommended and can lead to service issues. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_policy ComputeCluster#ha_admission_control_policy}
        :param ha_admission_control_resource_percentage_auto_compute: When ha_admission_control_policy is resourcePercentage, automatically determine available resource percentages by subtracting the average number of host resources represented by the ha_admission_control_host_failure_tolerance setting from the total amount of resources in the cluster. Disable to supply user-defined values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_resource_percentage_auto_compute ComputeCluster#ha_admission_control_resource_percentage_auto_compute}
        :param ha_admission_control_resource_percentage_cpu: When ha_admission_control_policy is resourcePercentage, this controls the user-defined percentage of CPU resources in the cluster to reserve for failover. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_resource_percentage_cpu ComputeCluster#ha_admission_control_resource_percentage_cpu}
        :param ha_admission_control_resource_percentage_memory: When ha_admission_control_policy is resourcePercentage, this controls the user-defined percentage of memory resources in the cluster to reserve for failover. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_resource_percentage_memory ComputeCluster#ha_admission_control_resource_percentage_memory}
        :param ha_admission_control_slot_policy_explicit_cpu: When ha_admission_control_policy is slotPolicy, this controls the user-defined CPU slot size, in MHz. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_slot_policy_explicit_cpu ComputeCluster#ha_admission_control_slot_policy_explicit_cpu}
        :param ha_admission_control_slot_policy_explicit_memory: When ha_admission_control_policy is slotPolicy, this controls the user-defined memory slot size, in MB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_slot_policy_explicit_memory ComputeCluster#ha_admission_control_slot_policy_explicit_memory}
        :param ha_admission_control_slot_policy_use_explicit_size: When ha_admission_control_policy is slotPolicy, this setting controls whether or not you wish to supply explicit values to CPU and memory slot sizes. The default is to gather a automatic average based on all powered-on virtual machines currently in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_slot_policy_use_explicit_size ComputeCluster#ha_admission_control_slot_policy_use_explicit_size}
        :param ha_advanced_options: Advanced configuration options for vSphere HA. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_advanced_options ComputeCluster#ha_advanced_options}
        :param ha_datastore_apd_recovery_action: When ha_vm_component_protection is enabled, controls the action to take on virtual machines if an APD status on an affected datastore clears in the middle of an APD event. Can be one of none or reset. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_datastore_apd_recovery_action ComputeCluster#ha_datastore_apd_recovery_action}
        :param ha_datastore_apd_response: When ha_vm_component_protection is enabled, controls the action to take on virtual machines when the cluster has detected loss to all paths to a relevant datastore. Can be one of disabled, warning, restartConservative, or restartAggressive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_datastore_apd_response ComputeCluster#ha_datastore_apd_response}
        :param ha_datastore_apd_response_delay: When ha_vm_component_protection is enabled, controls the delay in seconds to wait after an APD timeout event to execute the response action defined in ha_datastore_apd_response. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_datastore_apd_response_delay ComputeCluster#ha_datastore_apd_response_delay}
        :param ha_datastore_pdl_response: When ha_vm_component_protection is enabled, controls the action to take on virtual machines when the cluster has detected a permanent device loss to a relevant datastore. Can be one of disabled, warning, or restartAggressive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_datastore_pdl_response ComputeCluster#ha_datastore_pdl_response}
        :param ha_enabled: Enable vSphere HA for this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_enabled ComputeCluster#ha_enabled}
        :param ha_heartbeat_datastore_ids: The list of managed object IDs for preferred datastores to use for HA heartbeating. This setting is only useful when ha_heartbeat_datastore_policy is set to either userSelectedDs or allFeasibleDsWithUserPreference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_heartbeat_datastore_ids ComputeCluster#ha_heartbeat_datastore_ids}
        :param ha_heartbeat_datastore_policy: The selection policy for HA heartbeat datastores. Can be one of allFeasibleDs, userSelectedDs, or allFeasibleDsWithUserPreference. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_heartbeat_datastore_policy ComputeCluster#ha_heartbeat_datastore_policy}
        :param ha_host_isolation_response: The action to take on virtual machines when a host has detected that it has been isolated from the rest of the cluster. Can be one of none, powerOff, or shutdown. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_host_isolation_response ComputeCluster#ha_host_isolation_response}
        :param ha_host_monitoring: Global setting that controls whether vSphere HA remediates VMs on host failure. Can be one of enabled or disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_host_monitoring ComputeCluster#ha_host_monitoring}
        :param ha_vm_component_protection: Controls vSphere VM component protection for virtual machines in this cluster. This allows vSphere HA to react to failures between hosts and specific virtual machine components, such as datastores. Can be one of enabled or disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_component_protection ComputeCluster#ha_vm_component_protection}
        :param ha_vm_dependency_restart_condition: The condition used to determine whether or not VMs in a certain restart priority class are online, allowing HA to move on to restarting VMs on the next priority. Can be one of none, poweredOn, guestHbStatusGreen, or appHbStatusGreen. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_dependency_restart_condition ComputeCluster#ha_vm_dependency_restart_condition}
        :param ha_vm_failure_interval: If a heartbeat from a virtual machine is not received within this configured interval, the virtual machine is marked as failed. The value is in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_failure_interval ComputeCluster#ha_vm_failure_interval}
        :param ha_vm_maximum_failure_window: The length of the reset window in which ha_vm_maximum_resets can operate. When this window expires, no more resets are attempted regardless of the setting configured in ha_vm_maximum_resets. -1 means no window, meaning an unlimited reset time is allotted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_maximum_failure_window ComputeCluster#ha_vm_maximum_failure_window}
        :param ha_vm_maximum_resets: The maximum number of resets that HA will perform to a virtual machine when responding to a failure event. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_maximum_resets ComputeCluster#ha_vm_maximum_resets}
        :param ha_vm_minimum_uptime: The time, in seconds, that HA waits after powering on a virtual machine before monitoring for heartbeats. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_minimum_uptime ComputeCluster#ha_vm_minimum_uptime}
        :param ha_vm_monitoring: The type of virtual machine monitoring to use when HA is enabled in the cluster. Can be one of vmMonitoringDisabled, vmMonitoringOnly, or vmAndAppMonitoring. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_monitoring ComputeCluster#ha_vm_monitoring}
        :param ha_vm_restart_additional_delay: Additional delay in seconds after ready condition is met. A VM is considered ready at this point. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_restart_additional_delay ComputeCluster#ha_vm_restart_additional_delay}
        :param ha_vm_restart_priority: The default restart priority for affected VMs when vSphere detects a host failure. Can be one of lowest, low, medium, high, or highest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_restart_priority ComputeCluster#ha_vm_restart_priority}
        :param ha_vm_restart_timeout: The maximum time, in seconds, that vSphere HA will wait for virtual machines in one priority to be ready before proceeding with the next priority. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_restart_timeout ComputeCluster#ha_vm_restart_timeout}
        :param host_cluster_exit_timeout: The timeout for each host maintenance mode operation when removing hosts from a cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#host_cluster_exit_timeout ComputeCluster#host_cluster_exit_timeout}
        :param host_managed: Must be set if cluster enrollment is managed from host resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#host_managed ComputeCluster#host_managed}
        :param host_system_ids: The managed object IDs of the hosts to put in the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#host_system_ids ComputeCluster#host_system_ids}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#id ComputeCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param proactive_ha_automation_level: The DRS behavior for proactive HA recommendations. Can be one of Automated or Manual. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_automation_level ComputeCluster#proactive_ha_automation_level}
        :param proactive_ha_enabled: Enables proactive HA, allowing for vSphere to get HA data from external providers and use DRS to perform remediation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_enabled ComputeCluster#proactive_ha_enabled}
        :param proactive_ha_moderate_remediation: The configured remediation for moderately degraded hosts. Can be one of MaintenanceMode or QuarantineMode. Note that this cannot be set to MaintenanceMode when proactive_ha_severe_remediation is set to QuarantineMode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_moderate_remediation ComputeCluster#proactive_ha_moderate_remediation}
        :param proactive_ha_provider_ids: The list of IDs for health update providers configured for this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_provider_ids ComputeCluster#proactive_ha_provider_ids}
        :param proactive_ha_severe_remediation: The configured remediation for severely degraded hosts. Can be one of MaintenanceMode or QuarantineMode. Note that this cannot be set to QuarantineMode when proactive_ha_moderate_remediation is set to MaintenanceMode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_severe_remediation ComputeCluster#proactive_ha_severe_remediation}
        :param tags: A list of tag IDs to apply to this object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#tags ComputeCluster#tags}
        :param vsan_compression_enabled: Whether the vSAN compression service is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_compression_enabled ComputeCluster#vsan_compression_enabled}
        :param vsan_dedup_enabled: Whether the vSAN deduplication service is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_dedup_enabled ComputeCluster#vsan_dedup_enabled}
        :param vsan_disk_group: vsan_disk_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_disk_group ComputeCluster#vsan_disk_group}
        :param vsan_dit_encryption_enabled: Whether the vSAN data-in-transit encryption is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_dit_encryption_enabled ComputeCluster#vsan_dit_encryption_enabled}
        :param vsan_dit_rekey_interval: When vsan_dit_encryption_enabled is enabled, sets the rekey interval of data-in-transit encryption (in minutes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_dit_rekey_interval ComputeCluster#vsan_dit_rekey_interval}
        :param vsan_enabled: Whether the vSAN service is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_enabled ComputeCluster#vsan_enabled}
        :param vsan_network_diagnostic_mode_enabled: Whether the vSAN network diagnostic mode is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_network_diagnostic_mode_enabled ComputeCluster#vsan_network_diagnostic_mode_enabled}
        :param vsan_performance_enabled: Whether the vSAN performance service is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_performance_enabled ComputeCluster#vsan_performance_enabled}
        :param vsan_remote_datastore_ids: The managed object IDs of the vSAN datastore to be mounted on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_remote_datastore_ids ComputeCluster#vsan_remote_datastore_ids}
        :param vsan_unmap_enabled: Whether the vSAN unmap service is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_unmap_enabled ComputeCluster#vsan_unmap_enabled}
        :param vsan_verbose_mode_enabled: Whether the vSAN verbose mode is enabled for the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_verbose_mode_enabled ComputeCluster#vsan_verbose_mode_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__998fa1202162dcf9606c49257684397a1340e5033d8a826820908621f584b2df)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument datacenter_id", value=datacenter_id, expected_type=type_hints["datacenter_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
            check_type(argname="argument dpm_automation_level", value=dpm_automation_level, expected_type=type_hints["dpm_automation_level"])
            check_type(argname="argument dpm_enabled", value=dpm_enabled, expected_type=type_hints["dpm_enabled"])
            check_type(argname="argument dpm_threshold", value=dpm_threshold, expected_type=type_hints["dpm_threshold"])
            check_type(argname="argument drs_advanced_options", value=drs_advanced_options, expected_type=type_hints["drs_advanced_options"])
            check_type(argname="argument drs_automation_level", value=drs_automation_level, expected_type=type_hints["drs_automation_level"])
            check_type(argname="argument drs_enabled", value=drs_enabled, expected_type=type_hints["drs_enabled"])
            check_type(argname="argument drs_enable_predictive_drs", value=drs_enable_predictive_drs, expected_type=type_hints["drs_enable_predictive_drs"])
            check_type(argname="argument drs_enable_vm_overrides", value=drs_enable_vm_overrides, expected_type=type_hints["drs_enable_vm_overrides"])
            check_type(argname="argument drs_migration_threshold", value=drs_migration_threshold, expected_type=type_hints["drs_migration_threshold"])
            check_type(argname="argument drs_scale_descendants_shares", value=drs_scale_descendants_shares, expected_type=type_hints["drs_scale_descendants_shares"])
            check_type(argname="argument folder", value=folder, expected_type=type_hints["folder"])
            check_type(argname="argument force_evacuate_on_destroy", value=force_evacuate_on_destroy, expected_type=type_hints["force_evacuate_on_destroy"])
            check_type(argname="argument ha_admission_control_failover_host_system_ids", value=ha_admission_control_failover_host_system_ids, expected_type=type_hints["ha_admission_control_failover_host_system_ids"])
            check_type(argname="argument ha_admission_control_host_failure_tolerance", value=ha_admission_control_host_failure_tolerance, expected_type=type_hints["ha_admission_control_host_failure_tolerance"])
            check_type(argname="argument ha_admission_control_performance_tolerance", value=ha_admission_control_performance_tolerance, expected_type=type_hints["ha_admission_control_performance_tolerance"])
            check_type(argname="argument ha_admission_control_policy", value=ha_admission_control_policy, expected_type=type_hints["ha_admission_control_policy"])
            check_type(argname="argument ha_admission_control_resource_percentage_auto_compute", value=ha_admission_control_resource_percentage_auto_compute, expected_type=type_hints["ha_admission_control_resource_percentage_auto_compute"])
            check_type(argname="argument ha_admission_control_resource_percentage_cpu", value=ha_admission_control_resource_percentage_cpu, expected_type=type_hints["ha_admission_control_resource_percentage_cpu"])
            check_type(argname="argument ha_admission_control_resource_percentage_memory", value=ha_admission_control_resource_percentage_memory, expected_type=type_hints["ha_admission_control_resource_percentage_memory"])
            check_type(argname="argument ha_admission_control_slot_policy_explicit_cpu", value=ha_admission_control_slot_policy_explicit_cpu, expected_type=type_hints["ha_admission_control_slot_policy_explicit_cpu"])
            check_type(argname="argument ha_admission_control_slot_policy_explicit_memory", value=ha_admission_control_slot_policy_explicit_memory, expected_type=type_hints["ha_admission_control_slot_policy_explicit_memory"])
            check_type(argname="argument ha_admission_control_slot_policy_use_explicit_size", value=ha_admission_control_slot_policy_use_explicit_size, expected_type=type_hints["ha_admission_control_slot_policy_use_explicit_size"])
            check_type(argname="argument ha_advanced_options", value=ha_advanced_options, expected_type=type_hints["ha_advanced_options"])
            check_type(argname="argument ha_datastore_apd_recovery_action", value=ha_datastore_apd_recovery_action, expected_type=type_hints["ha_datastore_apd_recovery_action"])
            check_type(argname="argument ha_datastore_apd_response", value=ha_datastore_apd_response, expected_type=type_hints["ha_datastore_apd_response"])
            check_type(argname="argument ha_datastore_apd_response_delay", value=ha_datastore_apd_response_delay, expected_type=type_hints["ha_datastore_apd_response_delay"])
            check_type(argname="argument ha_datastore_pdl_response", value=ha_datastore_pdl_response, expected_type=type_hints["ha_datastore_pdl_response"])
            check_type(argname="argument ha_enabled", value=ha_enabled, expected_type=type_hints["ha_enabled"])
            check_type(argname="argument ha_heartbeat_datastore_ids", value=ha_heartbeat_datastore_ids, expected_type=type_hints["ha_heartbeat_datastore_ids"])
            check_type(argname="argument ha_heartbeat_datastore_policy", value=ha_heartbeat_datastore_policy, expected_type=type_hints["ha_heartbeat_datastore_policy"])
            check_type(argname="argument ha_host_isolation_response", value=ha_host_isolation_response, expected_type=type_hints["ha_host_isolation_response"])
            check_type(argname="argument ha_host_monitoring", value=ha_host_monitoring, expected_type=type_hints["ha_host_monitoring"])
            check_type(argname="argument ha_vm_component_protection", value=ha_vm_component_protection, expected_type=type_hints["ha_vm_component_protection"])
            check_type(argname="argument ha_vm_dependency_restart_condition", value=ha_vm_dependency_restart_condition, expected_type=type_hints["ha_vm_dependency_restart_condition"])
            check_type(argname="argument ha_vm_failure_interval", value=ha_vm_failure_interval, expected_type=type_hints["ha_vm_failure_interval"])
            check_type(argname="argument ha_vm_maximum_failure_window", value=ha_vm_maximum_failure_window, expected_type=type_hints["ha_vm_maximum_failure_window"])
            check_type(argname="argument ha_vm_maximum_resets", value=ha_vm_maximum_resets, expected_type=type_hints["ha_vm_maximum_resets"])
            check_type(argname="argument ha_vm_minimum_uptime", value=ha_vm_minimum_uptime, expected_type=type_hints["ha_vm_minimum_uptime"])
            check_type(argname="argument ha_vm_monitoring", value=ha_vm_monitoring, expected_type=type_hints["ha_vm_monitoring"])
            check_type(argname="argument ha_vm_restart_additional_delay", value=ha_vm_restart_additional_delay, expected_type=type_hints["ha_vm_restart_additional_delay"])
            check_type(argname="argument ha_vm_restart_priority", value=ha_vm_restart_priority, expected_type=type_hints["ha_vm_restart_priority"])
            check_type(argname="argument ha_vm_restart_timeout", value=ha_vm_restart_timeout, expected_type=type_hints["ha_vm_restart_timeout"])
            check_type(argname="argument host_cluster_exit_timeout", value=host_cluster_exit_timeout, expected_type=type_hints["host_cluster_exit_timeout"])
            check_type(argname="argument host_managed", value=host_managed, expected_type=type_hints["host_managed"])
            check_type(argname="argument host_system_ids", value=host_system_ids, expected_type=type_hints["host_system_ids"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument proactive_ha_automation_level", value=proactive_ha_automation_level, expected_type=type_hints["proactive_ha_automation_level"])
            check_type(argname="argument proactive_ha_enabled", value=proactive_ha_enabled, expected_type=type_hints["proactive_ha_enabled"])
            check_type(argname="argument proactive_ha_moderate_remediation", value=proactive_ha_moderate_remediation, expected_type=type_hints["proactive_ha_moderate_remediation"])
            check_type(argname="argument proactive_ha_provider_ids", value=proactive_ha_provider_ids, expected_type=type_hints["proactive_ha_provider_ids"])
            check_type(argname="argument proactive_ha_severe_remediation", value=proactive_ha_severe_remediation, expected_type=type_hints["proactive_ha_severe_remediation"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vsan_compression_enabled", value=vsan_compression_enabled, expected_type=type_hints["vsan_compression_enabled"])
            check_type(argname="argument vsan_dedup_enabled", value=vsan_dedup_enabled, expected_type=type_hints["vsan_dedup_enabled"])
            check_type(argname="argument vsan_disk_group", value=vsan_disk_group, expected_type=type_hints["vsan_disk_group"])
            check_type(argname="argument vsan_dit_encryption_enabled", value=vsan_dit_encryption_enabled, expected_type=type_hints["vsan_dit_encryption_enabled"])
            check_type(argname="argument vsan_dit_rekey_interval", value=vsan_dit_rekey_interval, expected_type=type_hints["vsan_dit_rekey_interval"])
            check_type(argname="argument vsan_enabled", value=vsan_enabled, expected_type=type_hints["vsan_enabled"])
            check_type(argname="argument vsan_network_diagnostic_mode_enabled", value=vsan_network_diagnostic_mode_enabled, expected_type=type_hints["vsan_network_diagnostic_mode_enabled"])
            check_type(argname="argument vsan_performance_enabled", value=vsan_performance_enabled, expected_type=type_hints["vsan_performance_enabled"])
            check_type(argname="argument vsan_remote_datastore_ids", value=vsan_remote_datastore_ids, expected_type=type_hints["vsan_remote_datastore_ids"])
            check_type(argname="argument vsan_unmap_enabled", value=vsan_unmap_enabled, expected_type=type_hints["vsan_unmap_enabled"])
            check_type(argname="argument vsan_verbose_mode_enabled", value=vsan_verbose_mode_enabled, expected_type=type_hints["vsan_verbose_mode_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "datacenter_id": datacenter_id,
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if dpm_automation_level is not None:
            self._values["dpm_automation_level"] = dpm_automation_level
        if dpm_enabled is not None:
            self._values["dpm_enabled"] = dpm_enabled
        if dpm_threshold is not None:
            self._values["dpm_threshold"] = dpm_threshold
        if drs_advanced_options is not None:
            self._values["drs_advanced_options"] = drs_advanced_options
        if drs_automation_level is not None:
            self._values["drs_automation_level"] = drs_automation_level
        if drs_enabled is not None:
            self._values["drs_enabled"] = drs_enabled
        if drs_enable_predictive_drs is not None:
            self._values["drs_enable_predictive_drs"] = drs_enable_predictive_drs
        if drs_enable_vm_overrides is not None:
            self._values["drs_enable_vm_overrides"] = drs_enable_vm_overrides
        if drs_migration_threshold is not None:
            self._values["drs_migration_threshold"] = drs_migration_threshold
        if drs_scale_descendants_shares is not None:
            self._values["drs_scale_descendants_shares"] = drs_scale_descendants_shares
        if folder is not None:
            self._values["folder"] = folder
        if force_evacuate_on_destroy is not None:
            self._values["force_evacuate_on_destroy"] = force_evacuate_on_destroy
        if ha_admission_control_failover_host_system_ids is not None:
            self._values["ha_admission_control_failover_host_system_ids"] = ha_admission_control_failover_host_system_ids
        if ha_admission_control_host_failure_tolerance is not None:
            self._values["ha_admission_control_host_failure_tolerance"] = ha_admission_control_host_failure_tolerance
        if ha_admission_control_performance_tolerance is not None:
            self._values["ha_admission_control_performance_tolerance"] = ha_admission_control_performance_tolerance
        if ha_admission_control_policy is not None:
            self._values["ha_admission_control_policy"] = ha_admission_control_policy
        if ha_admission_control_resource_percentage_auto_compute is not None:
            self._values["ha_admission_control_resource_percentage_auto_compute"] = ha_admission_control_resource_percentage_auto_compute
        if ha_admission_control_resource_percentage_cpu is not None:
            self._values["ha_admission_control_resource_percentage_cpu"] = ha_admission_control_resource_percentage_cpu
        if ha_admission_control_resource_percentage_memory is not None:
            self._values["ha_admission_control_resource_percentage_memory"] = ha_admission_control_resource_percentage_memory
        if ha_admission_control_slot_policy_explicit_cpu is not None:
            self._values["ha_admission_control_slot_policy_explicit_cpu"] = ha_admission_control_slot_policy_explicit_cpu
        if ha_admission_control_slot_policy_explicit_memory is not None:
            self._values["ha_admission_control_slot_policy_explicit_memory"] = ha_admission_control_slot_policy_explicit_memory
        if ha_admission_control_slot_policy_use_explicit_size is not None:
            self._values["ha_admission_control_slot_policy_use_explicit_size"] = ha_admission_control_slot_policy_use_explicit_size
        if ha_advanced_options is not None:
            self._values["ha_advanced_options"] = ha_advanced_options
        if ha_datastore_apd_recovery_action is not None:
            self._values["ha_datastore_apd_recovery_action"] = ha_datastore_apd_recovery_action
        if ha_datastore_apd_response is not None:
            self._values["ha_datastore_apd_response"] = ha_datastore_apd_response
        if ha_datastore_apd_response_delay is not None:
            self._values["ha_datastore_apd_response_delay"] = ha_datastore_apd_response_delay
        if ha_datastore_pdl_response is not None:
            self._values["ha_datastore_pdl_response"] = ha_datastore_pdl_response
        if ha_enabled is not None:
            self._values["ha_enabled"] = ha_enabled
        if ha_heartbeat_datastore_ids is not None:
            self._values["ha_heartbeat_datastore_ids"] = ha_heartbeat_datastore_ids
        if ha_heartbeat_datastore_policy is not None:
            self._values["ha_heartbeat_datastore_policy"] = ha_heartbeat_datastore_policy
        if ha_host_isolation_response is not None:
            self._values["ha_host_isolation_response"] = ha_host_isolation_response
        if ha_host_monitoring is not None:
            self._values["ha_host_monitoring"] = ha_host_monitoring
        if ha_vm_component_protection is not None:
            self._values["ha_vm_component_protection"] = ha_vm_component_protection
        if ha_vm_dependency_restart_condition is not None:
            self._values["ha_vm_dependency_restart_condition"] = ha_vm_dependency_restart_condition
        if ha_vm_failure_interval is not None:
            self._values["ha_vm_failure_interval"] = ha_vm_failure_interval
        if ha_vm_maximum_failure_window is not None:
            self._values["ha_vm_maximum_failure_window"] = ha_vm_maximum_failure_window
        if ha_vm_maximum_resets is not None:
            self._values["ha_vm_maximum_resets"] = ha_vm_maximum_resets
        if ha_vm_minimum_uptime is not None:
            self._values["ha_vm_minimum_uptime"] = ha_vm_minimum_uptime
        if ha_vm_monitoring is not None:
            self._values["ha_vm_monitoring"] = ha_vm_monitoring
        if ha_vm_restart_additional_delay is not None:
            self._values["ha_vm_restart_additional_delay"] = ha_vm_restart_additional_delay
        if ha_vm_restart_priority is not None:
            self._values["ha_vm_restart_priority"] = ha_vm_restart_priority
        if ha_vm_restart_timeout is not None:
            self._values["ha_vm_restart_timeout"] = ha_vm_restart_timeout
        if host_cluster_exit_timeout is not None:
            self._values["host_cluster_exit_timeout"] = host_cluster_exit_timeout
        if host_managed is not None:
            self._values["host_managed"] = host_managed
        if host_system_ids is not None:
            self._values["host_system_ids"] = host_system_ids
        if id is not None:
            self._values["id"] = id
        if proactive_ha_automation_level is not None:
            self._values["proactive_ha_automation_level"] = proactive_ha_automation_level
        if proactive_ha_enabled is not None:
            self._values["proactive_ha_enabled"] = proactive_ha_enabled
        if proactive_ha_moderate_remediation is not None:
            self._values["proactive_ha_moderate_remediation"] = proactive_ha_moderate_remediation
        if proactive_ha_provider_ids is not None:
            self._values["proactive_ha_provider_ids"] = proactive_ha_provider_ids
        if proactive_ha_severe_remediation is not None:
            self._values["proactive_ha_severe_remediation"] = proactive_ha_severe_remediation
        if tags is not None:
            self._values["tags"] = tags
        if vsan_compression_enabled is not None:
            self._values["vsan_compression_enabled"] = vsan_compression_enabled
        if vsan_dedup_enabled is not None:
            self._values["vsan_dedup_enabled"] = vsan_dedup_enabled
        if vsan_disk_group is not None:
            self._values["vsan_disk_group"] = vsan_disk_group
        if vsan_dit_encryption_enabled is not None:
            self._values["vsan_dit_encryption_enabled"] = vsan_dit_encryption_enabled
        if vsan_dit_rekey_interval is not None:
            self._values["vsan_dit_rekey_interval"] = vsan_dit_rekey_interval
        if vsan_enabled is not None:
            self._values["vsan_enabled"] = vsan_enabled
        if vsan_network_diagnostic_mode_enabled is not None:
            self._values["vsan_network_diagnostic_mode_enabled"] = vsan_network_diagnostic_mode_enabled
        if vsan_performance_enabled is not None:
            self._values["vsan_performance_enabled"] = vsan_performance_enabled
        if vsan_remote_datastore_ids is not None:
            self._values["vsan_remote_datastore_ids"] = vsan_remote_datastore_ids
        if vsan_unmap_enabled is not None:
            self._values["vsan_unmap_enabled"] = vsan_unmap_enabled
        if vsan_verbose_mode_enabled is not None:
            self._values["vsan_verbose_mode_enabled"] = vsan_verbose_mode_enabled

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def datacenter_id(self) -> builtins.str:
        '''The managed object ID of the datacenter to put the cluster in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#datacenter_id ComputeCluster#datacenter_id}
        '''
        result = self._values.get("datacenter_id")
        assert result is not None, "Required property 'datacenter_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name for the new cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#name ComputeCluster#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A list of custom attributes to set on this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#custom_attributes ComputeCluster#custom_attributes}
        '''
        result = self._values.get("custom_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def dpm_automation_level(self) -> typing.Optional[builtins.str]:
        '''The automation level for host power operations in this cluster. Can be one of manual or automated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#dpm_automation_level ComputeCluster#dpm_automation_level}
        '''
        result = self._values.get("dpm_automation_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dpm_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable DPM support for DRS.

        This allows you to dynamically control the power of hosts depending on the needs of virtual machines in the cluster. Requires that DRS be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#dpm_enabled ComputeCluster#dpm_enabled}
        '''
        result = self._values.get("dpm_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dpm_threshold(self) -> typing.Optional[jsii.Number]:
        '''A value between 1 and 5 indicating the threshold of load within the cluster that influences host power operations.

        This affects both power on and power off operations - a lower setting will tolerate more of a surplus/deficit than a higher setting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#dpm_threshold ComputeCluster#dpm_threshold}
        '''
        result = self._values.get("dpm_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def drs_advanced_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Advanced configuration options for DRS and DPM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_advanced_options ComputeCluster#drs_advanced_options}
        '''
        result = self._values.get("drs_advanced_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def drs_automation_level(self) -> typing.Optional[builtins.str]:
        '''The default automation level for all virtual machines in this cluster. Can be one of manual, partiallyAutomated, or fullyAutomated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_automation_level ComputeCluster#drs_automation_level}
        '''
        result = self._values.get("drs_automation_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def drs_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable DRS for this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_enabled ComputeCluster#drs_enabled}
        '''
        result = self._values.get("drs_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drs_enable_predictive_drs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, enables DRS to use data from vRealize Operations Manager to make proactive DRS recommendations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_enable_predictive_drs ComputeCluster#drs_enable_predictive_drs}
        '''
        result = self._values.get("drs_enable_predictive_drs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drs_enable_vm_overrides(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When true, allows individual VM overrides within this cluster to be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_enable_vm_overrides ComputeCluster#drs_enable_vm_overrides}
        '''
        result = self._values.get("drs_enable_vm_overrides")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def drs_migration_threshold(self) -> typing.Optional[jsii.Number]:
        '''A value between 1 and 5 indicating the threshold of imbalance tolerated between hosts.

        A lower setting will tolerate more imbalance while a higher setting will tolerate less.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_migration_threshold ComputeCluster#drs_migration_threshold}
        '''
        result = self._values.get("drs_migration_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def drs_scale_descendants_shares(self) -> typing.Optional[builtins.str]:
        '''Enable scalable shares for all descendants of this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#drs_scale_descendants_shares ComputeCluster#drs_scale_descendants_shares}
        '''
        result = self._values.get("drs_scale_descendants_shares")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def folder(self) -> typing.Optional[builtins.str]:
        '''The name of the folder to locate the cluster in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#folder ComputeCluster#folder}
        '''
        result = self._values.get("folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_evacuate_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Force removal of all hosts in the cluster during destroy and make them standalone hosts.

        Use of this flag mainly exists for testing and is not recommended in normal use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#force_evacuate_on_destroy ComputeCluster#force_evacuate_on_destroy}
        '''
        result = self._values.get("force_evacuate_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ha_admission_control_failover_host_system_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''When ha_admission_control_policy is failoverHosts, this defines the managed object IDs of hosts to use as dedicated failover hosts.

        These hosts are kept as available as possible - admission control will block access to the host, and DRS will ignore the host when making recommendations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_failover_host_system_ids ComputeCluster#ha_admission_control_failover_host_system_ids}
        '''
        result = self._values.get("ha_admission_control_failover_host_system_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ha_admission_control_host_failure_tolerance(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''The maximum number of failed hosts that admission control tolerates when making decisions on whether to permit virtual machine operations.

        The maximum is one less than the number of hosts in the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_host_failure_tolerance ComputeCluster#ha_admission_control_host_failure_tolerance}
        '''
        result = self._values.get("ha_admission_control_host_failure_tolerance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_admission_control_performance_tolerance(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''The percentage of resource reduction that a cluster of VMs can tolerate in case of a failover.

        A value of 0 produces warnings only, whereas a value of 100 disables the setting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_performance_tolerance ComputeCluster#ha_admission_control_performance_tolerance}
        '''
        result = self._values.get("ha_admission_control_performance_tolerance")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_admission_control_policy(self) -> typing.Optional[builtins.str]:
        '''The type of admission control policy to use with vSphere HA, which controls whether or not specific VM operations are permitted in the cluster in order to protect the reliability of the cluster.

        Can be one of resourcePercentage, slotPolicy, failoverHosts, or disabled. Note that disabling admission control is not recommended and can lead to service issues.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_policy ComputeCluster#ha_admission_control_policy}
        '''
        result = self._values.get("ha_admission_control_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha_admission_control_resource_percentage_auto_compute(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When ha_admission_control_policy is resourcePercentage, automatically determine available resource percentages by subtracting the average number of host resources represented by the ha_admission_control_host_failure_tolerance setting from the total amount of resources in the cluster.

        Disable to supply user-defined values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_resource_percentage_auto_compute ComputeCluster#ha_admission_control_resource_percentage_auto_compute}
        '''
        result = self._values.get("ha_admission_control_resource_percentage_auto_compute")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ha_admission_control_resource_percentage_cpu(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''When ha_admission_control_policy is resourcePercentage, this controls the user-defined percentage of CPU resources in the cluster to reserve for failover.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_resource_percentage_cpu ComputeCluster#ha_admission_control_resource_percentage_cpu}
        '''
        result = self._values.get("ha_admission_control_resource_percentage_cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_admission_control_resource_percentage_memory(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''When ha_admission_control_policy is resourcePercentage, this controls the user-defined percentage of memory resources in the cluster to reserve for failover.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_resource_percentage_memory ComputeCluster#ha_admission_control_resource_percentage_memory}
        '''
        result = self._values.get("ha_admission_control_resource_percentage_memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_admission_control_slot_policy_explicit_cpu(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''When ha_admission_control_policy is slotPolicy, this controls the user-defined CPU slot size, in MHz.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_slot_policy_explicit_cpu ComputeCluster#ha_admission_control_slot_policy_explicit_cpu}
        '''
        result = self._values.get("ha_admission_control_slot_policy_explicit_cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_admission_control_slot_policy_explicit_memory(
        self,
    ) -> typing.Optional[jsii.Number]:
        '''When ha_admission_control_policy is slotPolicy, this controls the user-defined memory slot size, in MB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_slot_policy_explicit_memory ComputeCluster#ha_admission_control_slot_policy_explicit_memory}
        '''
        result = self._values.get("ha_admission_control_slot_policy_explicit_memory")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_admission_control_slot_policy_use_explicit_size(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When ha_admission_control_policy is slotPolicy, this setting controls whether or not you wish to supply explicit values to CPU and memory slot sizes.

        The default is to gather a automatic average based on all powered-on virtual machines currently in the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_admission_control_slot_policy_use_explicit_size ComputeCluster#ha_admission_control_slot_policy_use_explicit_size}
        '''
        result = self._values.get("ha_admission_control_slot_policy_use_explicit_size")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ha_advanced_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Advanced configuration options for vSphere HA.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_advanced_options ComputeCluster#ha_advanced_options}
        '''
        result = self._values.get("ha_advanced_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def ha_datastore_apd_recovery_action(self) -> typing.Optional[builtins.str]:
        '''When ha_vm_component_protection is enabled, controls the action to take on virtual machines if an APD status on an affected datastore clears in the middle of an APD event.

        Can be one of none or reset.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_datastore_apd_recovery_action ComputeCluster#ha_datastore_apd_recovery_action}
        '''
        result = self._values.get("ha_datastore_apd_recovery_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha_datastore_apd_response(self) -> typing.Optional[builtins.str]:
        '''When ha_vm_component_protection is enabled, controls the action to take on virtual machines when the cluster has detected loss to all paths to a relevant datastore.

        Can be one of disabled, warning, restartConservative, or restartAggressive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_datastore_apd_response ComputeCluster#ha_datastore_apd_response}
        '''
        result = self._values.get("ha_datastore_apd_response")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha_datastore_apd_response_delay(self) -> typing.Optional[jsii.Number]:
        '''When ha_vm_component_protection is enabled, controls the delay in seconds to wait after an APD timeout event to execute the response action defined in ha_datastore_apd_response.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_datastore_apd_response_delay ComputeCluster#ha_datastore_apd_response_delay}
        '''
        result = self._values.get("ha_datastore_apd_response_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_datastore_pdl_response(self) -> typing.Optional[builtins.str]:
        '''When ha_vm_component_protection is enabled, controls the action to take on virtual machines when the cluster has detected a permanent device loss to a relevant datastore.

        Can be one of disabled, warning, or restartAggressive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_datastore_pdl_response ComputeCluster#ha_datastore_pdl_response}
        '''
        result = self._values.get("ha_datastore_pdl_response")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable vSphere HA for this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_enabled ComputeCluster#ha_enabled}
        '''
        result = self._values.get("ha_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ha_heartbeat_datastore_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of managed object IDs for preferred datastores to use for HA heartbeating.

        This setting is only useful when ha_heartbeat_datastore_policy is set to either userSelectedDs or allFeasibleDsWithUserPreference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_heartbeat_datastore_ids ComputeCluster#ha_heartbeat_datastore_ids}
        '''
        result = self._values.get("ha_heartbeat_datastore_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ha_heartbeat_datastore_policy(self) -> typing.Optional[builtins.str]:
        '''The selection policy for HA heartbeat datastores. Can be one of allFeasibleDs, userSelectedDs, or allFeasibleDsWithUserPreference.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_heartbeat_datastore_policy ComputeCluster#ha_heartbeat_datastore_policy}
        '''
        result = self._values.get("ha_heartbeat_datastore_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha_host_isolation_response(self) -> typing.Optional[builtins.str]:
        '''The action to take on virtual machines when a host has detected that it has been isolated from the rest of the cluster.

        Can be one of none, powerOff, or shutdown.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_host_isolation_response ComputeCluster#ha_host_isolation_response}
        '''
        result = self._values.get("ha_host_isolation_response")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha_host_monitoring(self) -> typing.Optional[builtins.str]:
        '''Global setting that controls whether vSphere HA remediates VMs on host failure. Can be one of enabled or disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_host_monitoring ComputeCluster#ha_host_monitoring}
        '''
        result = self._values.get("ha_host_monitoring")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha_vm_component_protection(self) -> typing.Optional[builtins.str]:
        '''Controls vSphere VM component protection for virtual machines in this cluster.

        This allows vSphere HA to react to failures between hosts and specific virtual machine components, such as datastores. Can be one of enabled or disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_component_protection ComputeCluster#ha_vm_component_protection}
        '''
        result = self._values.get("ha_vm_component_protection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha_vm_dependency_restart_condition(self) -> typing.Optional[builtins.str]:
        '''The condition used to determine whether or not VMs in a certain restart priority class are online, allowing HA to move on to restarting VMs on the next priority.

        Can be one of none, poweredOn, guestHbStatusGreen, or appHbStatusGreen.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_dependency_restart_condition ComputeCluster#ha_vm_dependency_restart_condition}
        '''
        result = self._values.get("ha_vm_dependency_restart_condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha_vm_failure_interval(self) -> typing.Optional[jsii.Number]:
        '''If a heartbeat from a virtual machine is not received within this configured interval, the virtual machine is marked as failed.

        The value is in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_failure_interval ComputeCluster#ha_vm_failure_interval}
        '''
        result = self._values.get("ha_vm_failure_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_vm_maximum_failure_window(self) -> typing.Optional[jsii.Number]:
        '''The length of the reset window in which ha_vm_maximum_resets can operate.

        When this window expires, no more resets are attempted regardless of the setting configured in ha_vm_maximum_resets. -1 means no window, meaning an unlimited reset time is allotted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_maximum_failure_window ComputeCluster#ha_vm_maximum_failure_window}
        '''
        result = self._values.get("ha_vm_maximum_failure_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_vm_maximum_resets(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of resets that HA will perform to a virtual machine when responding to a failure event.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_maximum_resets ComputeCluster#ha_vm_maximum_resets}
        '''
        result = self._values.get("ha_vm_maximum_resets")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_vm_minimum_uptime(self) -> typing.Optional[jsii.Number]:
        '''The time, in seconds, that HA waits after powering on a virtual machine before monitoring for heartbeats.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_minimum_uptime ComputeCluster#ha_vm_minimum_uptime}
        '''
        result = self._values.get("ha_vm_minimum_uptime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_vm_monitoring(self) -> typing.Optional[builtins.str]:
        '''The type of virtual machine monitoring to use when HA is enabled in the cluster.

        Can be one of vmMonitoringDisabled, vmMonitoringOnly, or vmAndAppMonitoring.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_monitoring ComputeCluster#ha_vm_monitoring}
        '''
        result = self._values.get("ha_vm_monitoring")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha_vm_restart_additional_delay(self) -> typing.Optional[jsii.Number]:
        '''Additional delay in seconds after ready condition is met. A VM is considered ready at this point.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_restart_additional_delay ComputeCluster#ha_vm_restart_additional_delay}
        '''
        result = self._values.get("ha_vm_restart_additional_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ha_vm_restart_priority(self) -> typing.Optional[builtins.str]:
        '''The default restart priority for affected VMs when vSphere detects a host failure.

        Can be one of lowest, low, medium, high, or highest.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_restart_priority ComputeCluster#ha_vm_restart_priority}
        '''
        result = self._values.get("ha_vm_restart_priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ha_vm_restart_timeout(self) -> typing.Optional[jsii.Number]:
        '''The maximum time, in seconds, that vSphere HA will wait for virtual machines in one priority to be ready before proceeding with the next priority.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#ha_vm_restart_timeout ComputeCluster#ha_vm_restart_timeout}
        '''
        result = self._values.get("ha_vm_restart_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def host_cluster_exit_timeout(self) -> typing.Optional[jsii.Number]:
        '''The timeout for each host maintenance mode operation when removing hosts from a cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#host_cluster_exit_timeout ComputeCluster#host_cluster_exit_timeout}
        '''
        result = self._values.get("host_cluster_exit_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def host_managed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Must be set if cluster enrollment is managed from host resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#host_managed ComputeCluster#host_managed}
        '''
        result = self._values.get("host_managed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def host_system_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The managed object IDs of the hosts to put in the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#host_system_ids ComputeCluster#host_system_ids}
        '''
        result = self._values.get("host_system_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#id ComputeCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proactive_ha_automation_level(self) -> typing.Optional[builtins.str]:
        '''The DRS behavior for proactive HA recommendations. Can be one of Automated or Manual.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_automation_level ComputeCluster#proactive_ha_automation_level}
        '''
        result = self._values.get("proactive_ha_automation_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proactive_ha_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables proactive HA, allowing for vSphere to get HA data from external providers and use DRS to perform remediation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_enabled ComputeCluster#proactive_ha_enabled}
        '''
        result = self._values.get("proactive_ha_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def proactive_ha_moderate_remediation(self) -> typing.Optional[builtins.str]:
        '''The configured remediation for moderately degraded hosts.

        Can be one of MaintenanceMode or QuarantineMode. Note that this cannot be set to MaintenanceMode when proactive_ha_severe_remediation is set to QuarantineMode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_moderate_remediation ComputeCluster#proactive_ha_moderate_remediation}
        '''
        result = self._values.get("proactive_ha_moderate_remediation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proactive_ha_provider_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of IDs for health update providers configured for this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_provider_ids ComputeCluster#proactive_ha_provider_ids}
        '''
        result = self._values.get("proactive_ha_provider_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def proactive_ha_severe_remediation(self) -> typing.Optional[builtins.str]:
        '''The configured remediation for severely degraded hosts.

        Can be one of MaintenanceMode or QuarantineMode. Note that this cannot be set to QuarantineMode when proactive_ha_moderate_remediation is set to MaintenanceMode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#proactive_ha_severe_remediation ComputeCluster#proactive_ha_severe_remediation}
        '''
        result = self._values.get("proactive_ha_severe_remediation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tag IDs to apply to this object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#tags ComputeCluster#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vsan_compression_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the vSAN compression service is enabled for the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_compression_enabled ComputeCluster#vsan_compression_enabled}
        '''
        result = self._values.get("vsan_compression_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vsan_dedup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the vSAN deduplication service is enabled for the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_dedup_enabled ComputeCluster#vsan_dedup_enabled}
        '''
        result = self._values.get("vsan_dedup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vsan_disk_group(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeClusterVsanDiskGroup"]]]:
        '''vsan_disk_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_disk_group ComputeCluster#vsan_disk_group}
        '''
        result = self._values.get("vsan_disk_group")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeClusterVsanDiskGroup"]]], result)

    @builtins.property
    def vsan_dit_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the vSAN data-in-transit encryption is enabled for the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_dit_encryption_enabled ComputeCluster#vsan_dit_encryption_enabled}
        '''
        result = self._values.get("vsan_dit_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vsan_dit_rekey_interval(self) -> typing.Optional[jsii.Number]:
        '''When vsan_dit_encryption_enabled is enabled, sets the rekey interval of data-in-transit encryption (in minutes).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_dit_rekey_interval ComputeCluster#vsan_dit_rekey_interval}
        '''
        result = self._values.get("vsan_dit_rekey_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vsan_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the vSAN service is enabled for the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_enabled ComputeCluster#vsan_enabled}
        '''
        result = self._values.get("vsan_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vsan_network_diagnostic_mode_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the vSAN network diagnostic mode is enabled for the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_network_diagnostic_mode_enabled ComputeCluster#vsan_network_diagnostic_mode_enabled}
        '''
        result = self._values.get("vsan_network_diagnostic_mode_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vsan_performance_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the vSAN performance service is enabled for the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_performance_enabled ComputeCluster#vsan_performance_enabled}
        '''
        result = self._values.get("vsan_performance_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vsan_remote_datastore_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The managed object IDs of the vSAN datastore to be mounted on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_remote_datastore_ids ComputeCluster#vsan_remote_datastore_ids}
        '''
        result = self._values.get("vsan_remote_datastore_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vsan_unmap_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the vSAN unmap service is enabled for the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_unmap_enabled ComputeCluster#vsan_unmap_enabled}
        '''
        result = self._values.get("vsan_unmap_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vsan_verbose_mode_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the vSAN verbose mode is enabled for the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#vsan_verbose_mode_enabled ComputeCluster#vsan_verbose_mode_enabled}
        '''
        result = self._values.get("vsan_verbose_mode_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-vsphere.computeCluster.ComputeClusterVsanDiskGroup",
    jsii_struct_bases=[],
    name_mapping={"cache": "cache", "storage": "storage"},
)
class ComputeClusterVsanDiskGroup:
    def __init__(
        self,
        *,
        cache: typing.Optional[builtins.str] = None,
        storage: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cache: Cache disk. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#cache ComputeCluster#cache}
        :param storage: List of storage disks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#storage ComputeCluster#storage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37899114184fa43bc6c16e3efb10cca75a149a58f9051d79e71ed70ae5e86a0)
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache is not None:
            self._values["cache"] = cache
        if storage is not None:
            self._values["storage"] = storage

    @builtins.property
    def cache(self) -> typing.Optional[builtins.str]:
        '''Cache disk.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#cache ComputeCluster#cache}
        '''
        result = self._values.get("cache")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of storage disks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/compute_cluster#storage ComputeCluster#storage}
        '''
        result = self._values.get("storage")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeClusterVsanDiskGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeClusterVsanDiskGroupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vsphere.computeCluster.ComputeClusterVsanDiskGroupList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb5ff69ac5c32824777c4d1c1790b4ee9bb0d364936a881a5127f3ec900c21a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ComputeClusterVsanDiskGroupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f568a34e33ede41746dad59ba37e4784d93c831c3633d55b25cc491a36021bfc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeClusterVsanDiskGroupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9f9b3c73666581ec6332266330c5e1897281e8fb2de45fd29e88efd3472887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c25ff1b5ace376d9c3f8e5d8346ac624c5a193701c81fe6c797f87e81eb585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbccd4021f8b0937c96c8f71f6f59e9a1819c60f33205ba3b5acc56b95d74f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeClusterVsanDiskGroup]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeClusterVsanDiskGroup]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeClusterVsanDiskGroup]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c1e641f49bee2bae2e1c654fbd8c7acd22e9432d8342995966608459304cf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ComputeClusterVsanDiskGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vsphere.computeCluster.ComputeClusterVsanDiskGroupOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9964b7b792598a6bba59478e5c0fcfdb40958c774adfaf6af95485a50c9be69)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCache")
    def reset_cache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCache", []))

    @jsii.member(jsii_name="resetStorage")
    def reset_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorage", []))

    @builtins.property
    @jsii.member(jsii_name="cacheInput")
    def cache_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cache"))

    @cache.setter
    def cache(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4274eacf5d8502480aefe3391c57ac6152de938cdc684619bf636afa0b1b271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cache", value)

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "storage"))

    @storage.setter
    def storage(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f993bddac46c29e3b078b5eb4623137a12745fdbecf7645f07e080778b881658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storage", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeClusterVsanDiskGroup]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeClusterVsanDiskGroup]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeClusterVsanDiskGroup]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9838ff3ab571a389a5846269125b5667df0c518d6990a7075836dc56c7287b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ComputeCluster",
    "ComputeClusterConfig",
    "ComputeClusterVsanDiskGroup",
    "ComputeClusterVsanDiskGroupList",
    "ComputeClusterVsanDiskGroupOutputReference",
]

publication.publish()

def _typecheckingstub__d6d9ec692d92b24a65224aed0e724338f0cd7313cfd48925db94cc279dff4065(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    datacenter_id: builtins.str,
    name: builtins.str,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    dpm_automation_level: typing.Optional[builtins.str] = None,
    dpm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dpm_threshold: typing.Optional[jsii.Number] = None,
    drs_advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    drs_automation_level: typing.Optional[builtins.str] = None,
    drs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drs_enable_predictive_drs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drs_enable_vm_overrides: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drs_migration_threshold: typing.Optional[jsii.Number] = None,
    drs_scale_descendants_shares: typing.Optional[builtins.str] = None,
    folder: typing.Optional[builtins.str] = None,
    force_evacuate_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ha_admission_control_failover_host_system_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ha_admission_control_host_failure_tolerance: typing.Optional[jsii.Number] = None,
    ha_admission_control_performance_tolerance: typing.Optional[jsii.Number] = None,
    ha_admission_control_policy: typing.Optional[builtins.str] = None,
    ha_admission_control_resource_percentage_auto_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ha_admission_control_resource_percentage_cpu: typing.Optional[jsii.Number] = None,
    ha_admission_control_resource_percentage_memory: typing.Optional[jsii.Number] = None,
    ha_admission_control_slot_policy_explicit_cpu: typing.Optional[jsii.Number] = None,
    ha_admission_control_slot_policy_explicit_memory: typing.Optional[jsii.Number] = None,
    ha_admission_control_slot_policy_use_explicit_size: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ha_advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ha_datastore_apd_recovery_action: typing.Optional[builtins.str] = None,
    ha_datastore_apd_response: typing.Optional[builtins.str] = None,
    ha_datastore_apd_response_delay: typing.Optional[jsii.Number] = None,
    ha_datastore_pdl_response: typing.Optional[builtins.str] = None,
    ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ha_heartbeat_datastore_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ha_heartbeat_datastore_policy: typing.Optional[builtins.str] = None,
    ha_host_isolation_response: typing.Optional[builtins.str] = None,
    ha_host_monitoring: typing.Optional[builtins.str] = None,
    ha_vm_component_protection: typing.Optional[builtins.str] = None,
    ha_vm_dependency_restart_condition: typing.Optional[builtins.str] = None,
    ha_vm_failure_interval: typing.Optional[jsii.Number] = None,
    ha_vm_maximum_failure_window: typing.Optional[jsii.Number] = None,
    ha_vm_maximum_resets: typing.Optional[jsii.Number] = None,
    ha_vm_minimum_uptime: typing.Optional[jsii.Number] = None,
    ha_vm_monitoring: typing.Optional[builtins.str] = None,
    ha_vm_restart_additional_delay: typing.Optional[jsii.Number] = None,
    ha_vm_restart_priority: typing.Optional[builtins.str] = None,
    ha_vm_restart_timeout: typing.Optional[jsii.Number] = None,
    host_cluster_exit_timeout: typing.Optional[jsii.Number] = None,
    host_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_system_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    proactive_ha_automation_level: typing.Optional[builtins.str] = None,
    proactive_ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    proactive_ha_moderate_remediation: typing.Optional[builtins.str] = None,
    proactive_ha_provider_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    proactive_ha_severe_remediation: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    vsan_compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_dedup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_disk_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeClusterVsanDiskGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vsan_dit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_dit_rekey_interval: typing.Optional[jsii.Number] = None,
    vsan_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_network_diagnostic_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_performance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_remote_datastore_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vsan_unmap_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_verbose_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c476472cf56c38050ef7fc3b5230f0b5932ce7fa283d87dd7fb05a0a75d9632a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeClusterVsanDiskGroup, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c986ac1347f1ac017672faf4123302fbbc7bce9b1164f0f14ed96458b25f43(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c343c1448f143a69b31c958b864d46dfddae7974f9fffa7df6c369b35cbbe8a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d33189b0374fbe3c2be40cec4db145710ca7ad94a7f2dc253a10657bda8bfb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707352eec66304de0f2eadee9af4e003a76f57c1a5844539ecf64daf68db8487(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c1e774067ea40929ffabdb358793ea7ea3e26473c32a91f227b6bfe6e12fa2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7187a17eb296c36237433c401fd3c8c76fb683d591e0768d8bd87b604ff60a27(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c839fa263f8ebb3a27de8e5dcb7f1a7031e999bdd63ba0158e81f2ed4c03100(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9887b6cdef2e9ad2dd5dfef89d9dde3015a42b4612446af8d61b7af185635a1f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7b74ee1e1bd5e7f9535b23068964aa958cabdfd5e50d14f098f2f6d51110d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2192ea7f018c7d0ece28876fa8efcb1d8ac23c80c15fffdef28c9d197b84df(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b0454732bc285dbaba92a81b31de5d49b2a9fc33fd89469d7a19d8b4ad4db9b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c26eda8cdc5f00bf916026350c44e5382ce2a2dfe0f9c15a6e16d50dccbe22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf7eb82a5a878358836d5e18a0656728c42043482bd19bbb0c8a2df859d9c10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dae9d17db92f75826a81710df799736ab4f90e72a766b98ada366a823a534cd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad265b6c2347b64d68e538f074ee0361326396fad9af93c84c333a36d656fe1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1442bc28bb0e33d2cd42b40d648d4ea33d482585b47f3bf1dd22b5412075c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb9be7f1d7dcf6c08708b2721537dd3c621f97ed479291c080a074637b049e1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd432a71f5e280fcf4bb2504eca535920f46365f47a9d7e737fd224aa0f3bfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ffc69951522f724a25389f97e9f5d8a838d793f3e3901d0146bfaa897814b5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e845b1b7b14e35a31eb54099f21ae7139a0925255ca7acecb5828a9a939e0f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837205521ec9eb6c2b2d34008dd5f85dcfdac37c17f1bea5768dd38872a88fcd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73d6f69e3b0ac9e3e25e6c1cde284c79214cfa8bdb94cd141af90d454993e33(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ad6dcf8ece606f787014482ff21bdbb8a7df3c41d0f93ada2b9ad2b52022f9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224d04a8970ad94372dcc80236e730c519e1678eafa90981e12eeea8c200c4b1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce3dcc6e54f9ee00e27730c3e2bb3a12b83232fdae5fb4efe55b4ae414f7641(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f6bec720ca52fba92522906b15e26ada26fbe9cd218a02b3bece35ee63ddfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e83ccf5ff27f38a6147a63c5b8c851884abae02fc238d71eb5c87d23ec604e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e84ca52dd6b15213fbfbe4773663b7605f55623db4d788eb6146fc00f9e595(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02dba7880be945dd467836edb4f141029712d75f436f4adbdd97ae867f08aa12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec3f28fd9011c7afbc9445c14abd9c8d55aee5a3b7ab7abd9e0b158e53e9bc9a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08179ce56a36cf203292fe7280b4a23967e48f0bfa7f2c6a1062b4ea0284937(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99378c4b8de7eabbb20c1942243269c53c07081fada387a184dca0825febd01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd5b3106f8bdf4c1ac37cceeb32315af12fde1d17ff188cff9f3ffc182f2917(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ada4ab30bc7f6b407ce7ac7ed6ee2d50720af9abfb56d3071eb80825d968159(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf0761e0463e08af0bab58c4213fdbe6dcb23134d714163affe04c5958b0500(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616328225b77065904ea66e6cc68e56355968f6e120208a9b77f65f35ce4f2a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c6ff7617b7a2b7afd5cb3ddaa5637b97296ee0d9644a827d855187e25cf8b0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880cd1d984000531a36f9143c7a5935a830d7ec4182ca2b190d9cd5193ebe6ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3369252caca237d8aaa106287e47b52a3e802bdfe88136cccd42e11908940943(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a42eb2ed30e4cb4bd3665d074a3d6f5e7844bdb3fe3564e86c8e54cfe1a259(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db82a70df820c72696906e66a61fb9304b651605f7d2c48afe64386ec9ce5c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c43aa4deb2fc8affe6d8f89a7894d2b51240ca859ccb1479f864a1a1fe8a93f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848a31618ecc15ab26a82251da2f6d3ad8eac851cb096fc491d2f1f9a5e0098f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a306ec95f458fe3e6f547ddf6365625d07c410a272b93fe31726baa1748d53d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9da73662d1bbdd5a4ffdc9b55b716922288ed0e03955ae61fa629eac06b1cfb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3cff929d67a6c645cfedc6e9824560ac3256ddb2cb1fa5b8c8a1094c320047(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8750e6171d665b35361bbfc971bd57b887940bb2a0e78bf6f0ae2c41fa97c7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f80285c58a96bccbb67d68fe192d828ca65a97bd328decad4863cfb6ceca2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__031c54b8f7314c12c4ae3444934e5f6bb9500bd7bb062fef339ade8fd406682d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867680882efc9a70a2a980dbd2dd65d2ac0fe1c1b2a3a723c081fe1b69486d43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58a25b734f4d8da20846ee2d80d87acf9400fc3228458b325c1734724d4eaff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7fc159385fc109ae43145d351440ea3ca5417f8c60ca61b1a1048c4f7cd6d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb51707ae0e856f0874b53cc29c282cdde062aeeae3d6c19bab027020cb8ad50(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5feaef7eb6df7bd000f7fc5d7d913c482c73beb1783b6c1693e16cd6d30580f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71eea758dd8974e4ff9b243c975eb1971d0c3cf231a6d245cc486141cd4f5ee(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f64f42159cf18562bf8c143c116674beb576752c669c76f190c15ba7ab8f68(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360a441f446fb66a4faa7d22541ac5194186cb257ca1a32f413d63c24c64a8f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e182f82aa76ab9b046ebf2c15467f72cf9d8fcd4f282a913c5b0ba9caeb9b016(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbc412e832ad297036276355a55954e48e2f66bde71aa50b7a56ff94c167e0d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34281f63f4288e9443883af3acb9fb2f9f912a0bf900b78416165238651ec61a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9f0cb111783efabd48c4ec43e221e79ff7bd14385df60b6b4424c6c32e6b9b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ce6cdef835ccba366174f8abd9d30580ca1411612eb24f353dedd1685572ee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e9f8dabf13df8b03bb59960f7e22963af7011ac32099ecc67c53ad8c76411c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5d736336237ed230b16335abb4faa51f4c6ca2cc68e03cf2feb036dbb14ebc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd4e3dc12850519ce445812a521e8bca0c8c103de7ef9ef661abc5e70cbafa7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998fa1202162dcf9606c49257684397a1340e5033d8a826820908621f584b2df(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    datacenter_id: builtins.str,
    name: builtins.str,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    dpm_automation_level: typing.Optional[builtins.str] = None,
    dpm_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dpm_threshold: typing.Optional[jsii.Number] = None,
    drs_advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    drs_automation_level: typing.Optional[builtins.str] = None,
    drs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drs_enable_predictive_drs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drs_enable_vm_overrides: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    drs_migration_threshold: typing.Optional[jsii.Number] = None,
    drs_scale_descendants_shares: typing.Optional[builtins.str] = None,
    folder: typing.Optional[builtins.str] = None,
    force_evacuate_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ha_admission_control_failover_host_system_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ha_admission_control_host_failure_tolerance: typing.Optional[jsii.Number] = None,
    ha_admission_control_performance_tolerance: typing.Optional[jsii.Number] = None,
    ha_admission_control_policy: typing.Optional[builtins.str] = None,
    ha_admission_control_resource_percentage_auto_compute: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ha_admission_control_resource_percentage_cpu: typing.Optional[jsii.Number] = None,
    ha_admission_control_resource_percentage_memory: typing.Optional[jsii.Number] = None,
    ha_admission_control_slot_policy_explicit_cpu: typing.Optional[jsii.Number] = None,
    ha_admission_control_slot_policy_explicit_memory: typing.Optional[jsii.Number] = None,
    ha_admission_control_slot_policy_use_explicit_size: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ha_advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ha_datastore_apd_recovery_action: typing.Optional[builtins.str] = None,
    ha_datastore_apd_response: typing.Optional[builtins.str] = None,
    ha_datastore_apd_response_delay: typing.Optional[jsii.Number] = None,
    ha_datastore_pdl_response: typing.Optional[builtins.str] = None,
    ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ha_heartbeat_datastore_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ha_heartbeat_datastore_policy: typing.Optional[builtins.str] = None,
    ha_host_isolation_response: typing.Optional[builtins.str] = None,
    ha_host_monitoring: typing.Optional[builtins.str] = None,
    ha_vm_component_protection: typing.Optional[builtins.str] = None,
    ha_vm_dependency_restart_condition: typing.Optional[builtins.str] = None,
    ha_vm_failure_interval: typing.Optional[jsii.Number] = None,
    ha_vm_maximum_failure_window: typing.Optional[jsii.Number] = None,
    ha_vm_maximum_resets: typing.Optional[jsii.Number] = None,
    ha_vm_minimum_uptime: typing.Optional[jsii.Number] = None,
    ha_vm_monitoring: typing.Optional[builtins.str] = None,
    ha_vm_restart_additional_delay: typing.Optional[jsii.Number] = None,
    ha_vm_restart_priority: typing.Optional[builtins.str] = None,
    ha_vm_restart_timeout: typing.Optional[jsii.Number] = None,
    host_cluster_exit_timeout: typing.Optional[jsii.Number] = None,
    host_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    host_system_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    proactive_ha_automation_level: typing.Optional[builtins.str] = None,
    proactive_ha_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    proactive_ha_moderate_remediation: typing.Optional[builtins.str] = None,
    proactive_ha_provider_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    proactive_ha_severe_remediation: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    vsan_compression_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_dedup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_disk_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeClusterVsanDiskGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vsan_dit_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_dit_rekey_interval: typing.Optional[jsii.Number] = None,
    vsan_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_network_diagnostic_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_performance_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_remote_datastore_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vsan_unmap_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vsan_verbose_mode_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37899114184fa43bc6c16e3efb10cca75a149a58f9051d79e71ed70ae5e86a0(
    *,
    cache: typing.Optional[builtins.str] = None,
    storage: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5ff69ac5c32824777c4d1c1790b4ee9bb0d364936a881a5127f3ec900c21a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f568a34e33ede41746dad59ba37e4784d93c831c3633d55b25cc491a36021bfc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9f9b3c73666581ec6332266330c5e1897281e8fb2de45fd29e88efd3472887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c25ff1b5ace376d9c3f8e5d8346ac624c5a193701c81fe6c797f87e81eb585(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbccd4021f8b0937c96c8f71f6f59e9a1819c60f33205ba3b5acc56b95d74f44(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c1e641f49bee2bae2e1c654fbd8c7acd22e9432d8342995966608459304cf7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeClusterVsanDiskGroup]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9964b7b792598a6bba59478e5c0fcfdb40958c774adfaf6af95485a50c9be69(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4274eacf5d8502480aefe3391c57ac6152de938cdc684619bf636afa0b1b271(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f993bddac46c29e3b078b5eb4623137a12745fdbecf7645f07e080778b881658(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9838ff3ab571a389a5846269125b5667df0c518d6990a7075836dc56c7287b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeClusterVsanDiskGroup]],
) -> None:
    """Type checking stubs"""
    pass
