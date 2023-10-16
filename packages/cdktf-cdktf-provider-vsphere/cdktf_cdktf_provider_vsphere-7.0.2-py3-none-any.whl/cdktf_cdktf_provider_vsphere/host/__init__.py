'''
# `vsphere_host`

Refer to the Terraform Registory for docs: [`vsphere_host`](https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host).
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


class Host(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vsphere.host.Host",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host vsphere_host}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        hostname: builtins.str,
        password: builtins.str,
        username: builtins.str,
        cluster: typing.Optional[builtins.str] = None,
        cluster_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        datacenter: typing.Optional[builtins.str] = None,
        force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
        lockdown: typing.Optional[builtins.str] = None,
        maintenance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        thumbprint: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host vsphere_host} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param hostname: FQDN or IP address of the host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#hostname Host#hostname}
        :param password: Password of the administration account of the host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#password Host#password}
        :param username: Username of the administration account of the host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#username Host#username}
        :param cluster: ID of the vSphere cluster the host will belong to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#cluster Host#cluster}
        :param cluster_managed: Must be set if host is a member of a managed compute_cluster resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#cluster_managed Host#cluster_managed}
        :param connected: Set the state of the host. If set to false then the host will be asked to disconnect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#connected Host#connected}
        :param custom_attributes: A list of custom attributes to set on this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#custom_attributes Host#custom_attributes}
        :param datacenter: ID of the vSphere datacenter the host will belong to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#datacenter Host#datacenter}
        :param force: Force add the host to the vSphere inventory even if it's already managed by a different vCenter Server instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#force Host#force}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#id Host#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param license: License key that will be applied to this host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#license Host#license}
        :param lockdown: Set the host's lockdown status. Default is disabled. Valid options are 'disabled', 'normal', 'strict'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#lockdown Host#lockdown}
        :param maintenance: Set the host's maintenance mode. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#maintenance Host#maintenance}
        :param tags: A list of tag IDs to apply to this object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#tags Host#tags}
        :param thumbprint: Host's certificate SHA-1 thumbprint. If not set then the CA that signed the host's certificate must be trusted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#thumbprint Host#thumbprint}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18656f2bce55e9eb067beb47951917f71009e8a54839905a64a063ce5611d366)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HostConfig(
            hostname=hostname,
            password=password,
            username=username,
            cluster=cluster,
            cluster_managed=cluster_managed,
            connected=connected,
            custom_attributes=custom_attributes,
            datacenter=datacenter,
            force=force,
            id=id,
            license=license,
            lockdown=lockdown,
            maintenance=maintenance,
            tags=tags,
            thumbprint=thumbprint,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetCluster")
    def reset_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCluster", []))

    @jsii.member(jsii_name="resetClusterManaged")
    def reset_cluster_managed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterManaged", []))

    @jsii.member(jsii_name="resetConnected")
    def reset_connected(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnected", []))

    @jsii.member(jsii_name="resetCustomAttributes")
    def reset_custom_attributes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomAttributes", []))

    @jsii.member(jsii_name="resetDatacenter")
    def reset_datacenter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatacenter", []))

    @jsii.member(jsii_name="resetForce")
    def reset_force(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForce", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLicense")
    def reset_license(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicense", []))

    @jsii.member(jsii_name="resetLockdown")
    def reset_lockdown(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLockdown", []))

    @jsii.member(jsii_name="resetMaintenance")
    def reset_maintenance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenance", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetThumbprint")
    def reset_thumbprint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThumbprint", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterManagedInput")
    def cluster_managed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clusterManagedInput"))

    @builtins.property
    @jsii.member(jsii_name="connectedInput")
    def connected_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "connectedInput"))

    @builtins.property
    @jsii.member(jsii_name="customAttributesInput")
    def custom_attributes_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "customAttributesInput"))

    @builtins.property
    @jsii.member(jsii_name="datacenterInput")
    def datacenter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datacenterInput"))

    @builtins.property
    @jsii.member(jsii_name="forceInput")
    def force_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseInput")
    def license_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseInput"))

    @builtins.property
    @jsii.member(jsii_name="lockdownInput")
    def lockdown_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lockdownInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceInput")
    def maintenance_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "maintenanceInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="thumbprintInput")
    def thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ae23185c4b164fa5caf37e8e4b1837d6c21c574074aaed36f76ca42551b71c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value)

    @builtins.property
    @jsii.member(jsii_name="clusterManaged")
    def cluster_managed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clusterManaged"))

    @cluster_managed.setter
    def cluster_managed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15b567c94b54dbee0dfdb3bf440d4dd9c794e704ffdef1b46176a07ce7ddf4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterManaged", value)

    @builtins.property
    @jsii.member(jsii_name="connected")
    def connected(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "connected"))

    @connected.setter
    def connected(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33283475422b342868979da570a10f398a65dff50b47753ca3d2d2bf62b78720)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connected", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__ba7050dff28aa22cacaf2f1f31ec9dc41e257bd2ccc53371b619287da977a5f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="datacenter")
    def datacenter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datacenter"))

    @datacenter.setter
    def datacenter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8a16c1d3c290cafdc00b1e512b42aff8daa961961d3db08de383cf56eaa5d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datacenter", value)

    @builtins.property
    @jsii.member(jsii_name="force")
    def force(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "force"))

    @force.setter
    def force(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848ef7aa26ea97b467f84931dbc2aec8c00bb1e94edae9bb2fac128555de1f95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "force", value)

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b56bf89d96eed7e70fdfda3a06ddae67e325fe70e3be6ea49fca18d13596c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722a4132e51ca38aa4ad983a4caf5d5e820239bde04a0f89375f94656a4b3e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="license")
    def license(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "license"))

    @license.setter
    def license(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eeae5a5d7cd7ab5fb0c8679c98fa9f11271081601e870da3265b48a6a30fea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "license", value)

    @builtins.property
    @jsii.member(jsii_name="lockdown")
    def lockdown(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lockdown"))

    @lockdown.setter
    def lockdown(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a658533825a21aa287defd85c5195c27cae0ffda63adc2333525ef5cf57b18ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lockdown", value)

    @builtins.property
    @jsii.member(jsii_name="maintenance")
    def maintenance(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "maintenance"))

    @maintenance.setter
    def maintenance(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2231c4494c6d04b160868e358d41f327816e2a15e351c66e041501e2b8672241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenance", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39951c2a9439e0fe784575b006260bea839e2004f2e9114a13af26d0f96cf6e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ec46c6f242a273c70a902123b2348e5c996e77a5206c6b1d2990ed7a162a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @thumbprint.setter
    def thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f13cf599b236b2961ecce667030e74017c4c3a9cc90ddf73aa51a02f84971e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbprint", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc85a8ec8948a1119a52bdbb259bddc2479b9a2b8753725d602bbc62a209d7da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vsphere.host.HostConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "hostname": "hostname",
        "password": "password",
        "username": "username",
        "cluster": "cluster",
        "cluster_managed": "clusterManaged",
        "connected": "connected",
        "custom_attributes": "customAttributes",
        "datacenter": "datacenter",
        "force": "force",
        "id": "id",
        "license": "license",
        "lockdown": "lockdown",
        "maintenance": "maintenance",
        "tags": "tags",
        "thumbprint": "thumbprint",
    },
)
class HostConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        hostname: builtins.str,
        password: builtins.str,
        username: builtins.str,
        cluster: typing.Optional[builtins.str] = None,
        cluster_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        datacenter: typing.Optional[builtins.str] = None,
        force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
        lockdown: typing.Optional[builtins.str] = None,
        maintenance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        thumbprint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param hostname: FQDN or IP address of the host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#hostname Host#hostname}
        :param password: Password of the administration account of the host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#password Host#password}
        :param username: Username of the administration account of the host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#username Host#username}
        :param cluster: ID of the vSphere cluster the host will belong to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#cluster Host#cluster}
        :param cluster_managed: Must be set if host is a member of a managed compute_cluster resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#cluster_managed Host#cluster_managed}
        :param connected: Set the state of the host. If set to false then the host will be asked to disconnect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#connected Host#connected}
        :param custom_attributes: A list of custom attributes to set on this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#custom_attributes Host#custom_attributes}
        :param datacenter: ID of the vSphere datacenter the host will belong to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#datacenter Host#datacenter}
        :param force: Force add the host to the vSphere inventory even if it's already managed by a different vCenter Server instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#force Host#force}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#id Host#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param license: License key that will be applied to this host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#license Host#license}
        :param lockdown: Set the host's lockdown status. Default is disabled. Valid options are 'disabled', 'normal', 'strict'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#lockdown Host#lockdown}
        :param maintenance: Set the host's maintenance mode. Default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#maintenance Host#maintenance}
        :param tags: A list of tag IDs to apply to this object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#tags Host#tags}
        :param thumbprint: Host's certificate SHA-1 thumbprint. If not set then the CA that signed the host's certificate must be trusted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#thumbprint Host#thumbprint}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a580e90e332f6218a0bbcd037feafe747086bd89743b8a299c1b96f2e80e7c61)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument cluster_managed", value=cluster_managed, expected_type=type_hints["cluster_managed"])
            check_type(argname="argument connected", value=connected, expected_type=type_hints["connected"])
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
            check_type(argname="argument datacenter", value=datacenter, expected_type=type_hints["datacenter"])
            check_type(argname="argument force", value=force, expected_type=type_hints["force"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
            check_type(argname="argument lockdown", value=lockdown, expected_type=type_hints["lockdown"])
            check_type(argname="argument maintenance", value=maintenance, expected_type=type_hints["maintenance"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument thumbprint", value=thumbprint, expected_type=type_hints["thumbprint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hostname": hostname,
            "password": password,
            "username": username,
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
        if cluster is not None:
            self._values["cluster"] = cluster
        if cluster_managed is not None:
            self._values["cluster_managed"] = cluster_managed
        if connected is not None:
            self._values["connected"] = connected
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if datacenter is not None:
            self._values["datacenter"] = datacenter
        if force is not None:
            self._values["force"] = force
        if id is not None:
            self._values["id"] = id
        if license is not None:
            self._values["license"] = license
        if lockdown is not None:
            self._values["lockdown"] = lockdown
        if maintenance is not None:
            self._values["maintenance"] = maintenance
        if tags is not None:
            self._values["tags"] = tags
        if thumbprint is not None:
            self._values["thumbprint"] = thumbprint

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
    def hostname(self) -> builtins.str:
        '''FQDN or IP address of the host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#hostname Host#hostname}
        '''
        result = self._values.get("hostname")
        assert result is not None, "Required property 'hostname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Password of the administration account of the host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#password Host#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username of the administration account of the host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#username Host#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster(self) -> typing.Optional[builtins.str]:
        '''ID of the vSphere cluster the host will belong to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#cluster Host#cluster}
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_managed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Must be set if host is a member of a managed compute_cluster resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#cluster_managed Host#cluster_managed}
        '''
        result = self._values.get("cluster_managed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def connected(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set the state of the host. If set to false then the host will be asked to disconnect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#connected Host#connected}
        '''
        result = self._values.get("connected")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def custom_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A list of custom attributes to set on this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#custom_attributes Host#custom_attributes}
        '''
        result = self._values.get("custom_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def datacenter(self) -> typing.Optional[builtins.str]:
        '''ID of the vSphere datacenter the host will belong to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#datacenter Host#datacenter}
        '''
        result = self._values.get("datacenter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Force add the host to the vSphere inventory even if it's already managed by a different vCenter Server instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#force Host#force}
        '''
        result = self._values.get("force")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#id Host#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''License key that will be applied to this host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#license Host#license}
        '''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lockdown(self) -> typing.Optional[builtins.str]:
        '''Set the host's lockdown status. Default is disabled. Valid options are 'disabled', 'normal', 'strict'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#lockdown Host#lockdown}
        '''
        result = self._values.get("lockdown")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set the host's maintenance mode. Default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#maintenance Host#maintenance}
        '''
        result = self._values.get("maintenance")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of tag IDs to apply to this object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#tags Host#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def thumbprint(self) -> typing.Optional[builtins.str]:
        '''Host's certificate SHA-1 thumbprint. If not set then the CA that signed the host's certificate must be trusted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vsphere/2.5.0/docs/resources/host#thumbprint Host#thumbprint}
        '''
        result = self._values.get("thumbprint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Host",
    "HostConfig",
]

publication.publish()

def _typecheckingstub__18656f2bce55e9eb067beb47951917f71009e8a54839905a64a063ce5611d366(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    hostname: builtins.str,
    password: builtins.str,
    username: builtins.str,
    cluster: typing.Optional[builtins.str] = None,
    cluster_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    datacenter: typing.Optional[builtins.str] = None,
    force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    license: typing.Optional[builtins.str] = None,
    lockdown: typing.Optional[builtins.str] = None,
    maintenance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    thumbprint: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__c2ae23185c4b164fa5caf37e8e4b1837d6c21c574074aaed36f76ca42551b71c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15b567c94b54dbee0dfdb3bf440d4dd9c794e704ffdef1b46176a07ce7ddf4a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33283475422b342868979da570a10f398a65dff50b47753ca3d2d2bf62b78720(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7050dff28aa22cacaf2f1f31ec9dc41e257bd2ccc53371b619287da977a5f5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8a16c1d3c290cafdc00b1e512b42aff8daa961961d3db08de383cf56eaa5d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848ef7aa26ea97b467f84931dbc2aec8c00bb1e94edae9bb2fac128555de1f95(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b56bf89d96eed7e70fdfda3a06ddae67e325fe70e3be6ea49fca18d13596c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722a4132e51ca38aa4ad983a4caf5d5e820239bde04a0f89375f94656a4b3e37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eeae5a5d7cd7ab5fb0c8679c98fa9f11271081601e870da3265b48a6a30fea2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a658533825a21aa287defd85c5195c27cae0ffda63adc2333525ef5cf57b18ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2231c4494c6d04b160868e358d41f327816e2a15e351c66e041501e2b8672241(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39951c2a9439e0fe784575b006260bea839e2004f2e9114a13af26d0f96cf6e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ec46c6f242a273c70a902123b2348e5c996e77a5206c6b1d2990ed7a162a6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f13cf599b236b2961ecce667030e74017c4c3a9cc90ddf73aa51a02f84971e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc85a8ec8948a1119a52bdbb259bddc2479b9a2b8753725d602bbc62a209d7da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a580e90e332f6218a0bbcd037feafe747086bd89743b8a299c1b96f2e80e7c61(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostname: builtins.str,
    password: builtins.str,
    username: builtins.str,
    cluster: typing.Optional[builtins.str] = None,
    cluster_managed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connected: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    datacenter: typing.Optional[builtins.str] = None,
    force: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    license: typing.Optional[builtins.str] = None,
    lockdown: typing.Optional[builtins.str] = None,
    maintenance: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    thumbprint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
