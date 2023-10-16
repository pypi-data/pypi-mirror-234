'''
# `spotinst_ocean_aks_np`

Refer to the Terraform Registory for docs: [`spotinst_ocean_aks_np`](https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np).
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


class OceanAksNp(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNp",
):
    '''Represents a {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np spotinst_ocean_aks_np}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        aks_cluster_name: builtins.str,
        aks_infrastructure_resource_group_name: builtins.str,
        aks_region: builtins.str,
        aks_resource_group_name: builtins.str,
        availability_zones: typing.Sequence[builtins.str],
        name: builtins.str,
        autoscaler: typing.Optional[typing.Union["OceanAksNpAutoscaler", typing.Dict[builtins.str, typing.Any]]] = None,
        controller_cluster_id: typing.Optional[builtins.str] = None,
        enable_node_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fallback_to_ondemand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filters: typing.Optional[typing.Union["OceanAksNpFilters", typing.Dict[builtins.str, typing.Any]]] = None,
        headrooms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksNpHeadrooms", typing.Dict[builtins.str, typing.Any]]]]] = None,
        health: typing.Optional[typing.Union["OceanAksNpHealth", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kubernetes_version: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_count: typing.Optional[jsii.Number] = None,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
        min_count: typing.Optional[jsii.Number] = None,
        os_disk_size_gb: typing.Optional[jsii.Number] = None,
        os_disk_type: typing.Optional[builtins.str] = None,
        os_sku: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        scheduling: typing.Optional[typing.Union["OceanAksNpScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        spot_percentage: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksNpTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np spotinst_ocean_aks_np} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param aks_cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#aks_cluster_name OceanAksNp#aks_cluster_name}.
        :param aks_infrastructure_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#aks_infrastructure_resource_group_name OceanAksNp#aks_infrastructure_resource_group_name}.
        :param aks_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#aks_region OceanAksNp#aks_region}.
        :param aks_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#aks_resource_group_name OceanAksNp#aks_resource_group_name}.
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#availability_zones OceanAksNp#availability_zones}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#name OceanAksNp#name}.
        :param autoscaler: autoscaler block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#autoscaler OceanAksNp#autoscaler}
        :param controller_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#controller_cluster_id OceanAksNp#controller_cluster_id}.
        :param enable_node_public_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#enable_node_public_ip OceanAksNp#enable_node_public_ip}.
        :param fallback_to_ondemand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#fallback_to_ondemand OceanAksNp#fallback_to_ondemand}.
        :param filters: filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#filters OceanAksNp#filters}
        :param headrooms: headrooms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#headrooms OceanAksNp#headrooms}
        :param health: health block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#health OceanAksNp#health}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#id OceanAksNp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubernetes_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#kubernetes_version OceanAksNp#kubernetes_version}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#labels OceanAksNp#labels}.
        :param max_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_count OceanAksNp#max_count}.
        :param max_pods_per_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_pods_per_node OceanAksNp#max_pods_per_node}.
        :param min_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#min_count OceanAksNp#min_count}.
        :param os_disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#os_disk_size_gb OceanAksNp#os_disk_size_gb}.
        :param os_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#os_disk_type OceanAksNp#os_disk_type}.
        :param os_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#os_sku OceanAksNp#os_sku}.
        :param os_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#os_type OceanAksNp#os_type}.
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#scheduling OceanAksNp#scheduling}
        :param spot_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#spot_percentage OceanAksNp#spot_percentage}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#tags OceanAksNp#tags}.
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#taints OceanAksNp#taints}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__898ccbb93cd7b1a458d7f489d68c3366490a1abc47b94a9d60566b0529018fed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OceanAksNpConfig(
            aks_cluster_name=aks_cluster_name,
            aks_infrastructure_resource_group_name=aks_infrastructure_resource_group_name,
            aks_region=aks_region,
            aks_resource_group_name=aks_resource_group_name,
            availability_zones=availability_zones,
            name=name,
            autoscaler=autoscaler,
            controller_cluster_id=controller_cluster_id,
            enable_node_public_ip=enable_node_public_ip,
            fallback_to_ondemand=fallback_to_ondemand,
            filters=filters,
            headrooms=headrooms,
            health=health,
            id=id,
            kubernetes_version=kubernetes_version,
            labels=labels,
            max_count=max_count,
            max_pods_per_node=max_pods_per_node,
            min_count=min_count,
            os_disk_size_gb=os_disk_size_gb,
            os_disk_type=os_disk_type,
            os_sku=os_sku,
            os_type=os_type,
            scheduling=scheduling,
            spot_percentage=spot_percentage,
            tags=tags,
            taints=taints,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAutoscaler")
    def put_autoscaler(
        self,
        *,
        autoscale_down: typing.Optional[typing.Union["OceanAksNpAutoscalerAutoscaleDown", typing.Dict[builtins.str, typing.Any]]] = None,
        autoscale_headroom: typing.Optional[typing.Union["OceanAksNpAutoscalerAutoscaleHeadroom", typing.Dict[builtins.str, typing.Any]]] = None,
        autoscale_is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_limits: typing.Optional[typing.Union["OceanAksNpAutoscalerResourceLimits", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscale_down: autoscale_down block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#autoscale_down OceanAksNp#autoscale_down}
        :param autoscale_headroom: autoscale_headroom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#autoscale_headroom OceanAksNp#autoscale_headroom}
        :param autoscale_is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#autoscale_is_enabled OceanAksNp#autoscale_is_enabled}.
        :param resource_limits: resource_limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#resource_limits OceanAksNp#resource_limits}
        '''
        value = OceanAksNpAutoscaler(
            autoscale_down=autoscale_down,
            autoscale_headroom=autoscale_headroom,
            autoscale_is_enabled=autoscale_is_enabled,
            resource_limits=resource_limits,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscaler", [value]))

    @jsii.member(jsii_name="putFilters")
    def put_filters(
        self,
        *,
        architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_series: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_memory_gib: typing.Optional[jsii.Number] = None,
        max_vcpu: typing.Optional[jsii.Number] = None,
        min_memory_gib: typing.Optional[jsii.Number] = None,
        min_vcpu: typing.Optional[jsii.Number] = None,
        series: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param architectures: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#architectures OceanAksNp#architectures}.
        :param exclude_series: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#exclude_series OceanAksNp#exclude_series}.
        :param max_memory_gib: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_memory_gib OceanAksNp#max_memory_gib}.
        :param max_vcpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_vcpu OceanAksNp#max_vcpu}.
        :param min_memory_gib: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#min_memory_gib OceanAksNp#min_memory_gib}.
        :param min_vcpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#min_vcpu OceanAksNp#min_vcpu}.
        :param series: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#series OceanAksNp#series}.
        '''
        value = OceanAksNpFilters(
            architectures=architectures,
            exclude_series=exclude_series,
            max_memory_gib=max_memory_gib,
            max_vcpu=max_vcpu,
            min_memory_gib=min_memory_gib,
            min_vcpu=min_vcpu,
            series=series,
        )

        return typing.cast(None, jsii.invoke(self, "putFilters", [value]))

    @jsii.member(jsii_name="putHeadrooms")
    def put_headrooms(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksNpHeadrooms", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__284c374fcc23f7877c2e31bfa73cdbeb548c9a186476cd657442a94547da0842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeadrooms", [value]))

    @jsii.member(jsii_name="putHealth")
    def put_health(self, *, grace_period: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param grace_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#grace_period OceanAksNp#grace_period}.
        '''
        value = OceanAksNpHealth(grace_period=grace_period)

        return typing.cast(None, jsii.invoke(self, "putHealth", [value]))

    @jsii.member(jsii_name="putScheduling")
    def put_scheduling(
        self,
        *,
        shutdown_hours: typing.Optional[typing.Union["OceanAksNpSchedulingShutdownHours", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param shutdown_hours: shutdown_hours block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#shutdown_hours OceanAksNp#shutdown_hours}
        '''
        value = OceanAksNpScheduling(shutdown_hours=shutdown_hours)

        return typing.cast(None, jsii.invoke(self, "putScheduling", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksNpTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52fcc7c22e4bac75dfaf5872709d568cac573e3dd5764f65ad904b1247fd2db3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaints", [value]))

    @jsii.member(jsii_name="resetAutoscaler")
    def reset_autoscaler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaler", []))

    @jsii.member(jsii_name="resetControllerClusterId")
    def reset_controller_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControllerClusterId", []))

    @jsii.member(jsii_name="resetEnableNodePublicIp")
    def reset_enable_node_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableNodePublicIp", []))

    @jsii.member(jsii_name="resetFallbackToOndemand")
    def reset_fallback_to_ondemand(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFallbackToOndemand", []))

    @jsii.member(jsii_name="resetFilters")
    def reset_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilters", []))

    @jsii.member(jsii_name="resetHeadrooms")
    def reset_headrooms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeadrooms", []))

    @jsii.member(jsii_name="resetHealth")
    def reset_health(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealth", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKubernetesVersion")
    def reset_kubernetes_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetesVersion", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaxCount")
    def reset_max_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxCount", []))

    @jsii.member(jsii_name="resetMaxPodsPerNode")
    def reset_max_pods_per_node(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxPodsPerNode", []))

    @jsii.member(jsii_name="resetMinCount")
    def reset_min_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCount", []))

    @jsii.member(jsii_name="resetOsDiskSizeGb")
    def reset_os_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDiskSizeGb", []))

    @jsii.member(jsii_name="resetOsDiskType")
    def reset_os_disk_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDiskType", []))

    @jsii.member(jsii_name="resetOsSku")
    def reset_os_sku(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsSku", []))

    @jsii.member(jsii_name="resetOsType")
    def reset_os_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsType", []))

    @jsii.member(jsii_name="resetScheduling")
    def reset_scheduling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduling", []))

    @jsii.member(jsii_name="resetSpotPercentage")
    def reset_spot_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpotPercentage", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTaints")
    def reset_taints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaints", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="autoscaler")
    def autoscaler(self) -> "OceanAksNpAutoscalerOutputReference":
        return typing.cast("OceanAksNpAutoscalerOutputReference", jsii.get(self, "autoscaler"))

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(self) -> "OceanAksNpFiltersOutputReference":
        return typing.cast("OceanAksNpFiltersOutputReference", jsii.get(self, "filters"))

    @builtins.property
    @jsii.member(jsii_name="headrooms")
    def headrooms(self) -> "OceanAksNpHeadroomsList":
        return typing.cast("OceanAksNpHeadroomsList", jsii.get(self, "headrooms"))

    @builtins.property
    @jsii.member(jsii_name="health")
    def health(self) -> "OceanAksNpHealthOutputReference":
        return typing.cast("OceanAksNpHealthOutputReference", jsii.get(self, "health"))

    @builtins.property
    @jsii.member(jsii_name="scheduling")
    def scheduling(self) -> "OceanAksNpSchedulingOutputReference":
        return typing.cast("OceanAksNpSchedulingOutputReference", jsii.get(self, "scheduling"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(self) -> "OceanAksNpTaintsList":
        return typing.cast("OceanAksNpTaintsList", jsii.get(self, "taints"))

    @builtins.property
    @jsii.member(jsii_name="aksClusterNameInput")
    def aks_cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aksClusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="aksInfrastructureResourceGroupNameInput")
    def aks_infrastructure_resource_group_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aksInfrastructureResourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="aksRegionInput")
    def aks_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aksRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="aksResourceGroupNameInput")
    def aks_resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aksResourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscalerInput")
    def autoscaler_input(self) -> typing.Optional["OceanAksNpAutoscaler"]:
        return typing.cast(typing.Optional["OceanAksNpAutoscaler"], jsii.get(self, "autoscalerInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZonesInput")
    def availability_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="controllerClusterIdInput")
    def controller_cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controllerClusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enableNodePublicIpInput")
    def enable_node_public_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableNodePublicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="fallbackToOndemandInput")
    def fallback_to_ondemand_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fallbackToOndemandInput"))

    @builtins.property
    @jsii.member(jsii_name="filtersInput")
    def filters_input(self) -> typing.Optional["OceanAksNpFilters"]:
        return typing.cast(typing.Optional["OceanAksNpFilters"], jsii.get(self, "filtersInput"))

    @builtins.property
    @jsii.member(jsii_name="headroomsInput")
    def headrooms_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksNpHeadrooms"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksNpHeadrooms"]]], jsii.get(self, "headroomsInput"))

    @builtins.property
    @jsii.member(jsii_name="healthInput")
    def health_input(self) -> typing.Optional["OceanAksNpHealth"]:
        return typing.cast(typing.Optional["OceanAksNpHealth"], jsii.get(self, "healthInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesVersionInput")
    def kubernetes_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxCountInput")
    def max_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNodeInput")
    def max_pods_per_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPodsPerNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="minCountInput")
    def min_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskSizeGbInput")
    def os_disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "osDiskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="osDiskTypeInput")
    def os_disk_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osDiskTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="osSkuInput")
    def os_sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osSkuInput"))

    @builtins.property
    @jsii.member(jsii_name="osTypeInput")
    def os_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulingInput")
    def scheduling_input(self) -> typing.Optional["OceanAksNpScheduling"]:
        return typing.cast(typing.Optional["OceanAksNpScheduling"], jsii.get(self, "schedulingInput"))

    @builtins.property
    @jsii.member(jsii_name="spotPercentageInput")
    def spot_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spotPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksNpTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksNpTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="aksClusterName")
    def aks_cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aksClusterName"))

    @aks_cluster_name.setter
    def aks_cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a5844e745d3dc3bc50168b6d11d932a24790b381febdd79aa3acdba95594ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aksClusterName", value)

    @builtins.property
    @jsii.member(jsii_name="aksInfrastructureResourceGroupName")
    def aks_infrastructure_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aksInfrastructureResourceGroupName"))

    @aks_infrastructure_resource_group_name.setter
    def aks_infrastructure_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea69ad8644dd89aa463fc85d07e524019a06a1cc120da1e5987046a167466f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aksInfrastructureResourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="aksRegion")
    def aks_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aksRegion"))

    @aks_region.setter
    def aks_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ec4fefd2f1d7c22a01397d06dae7fd932b7d24c5aed9becabb675f4a845d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aksRegion", value)

    @builtins.property
    @jsii.member(jsii_name="aksResourceGroupName")
    def aks_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aksResourceGroupName"))

    @aks_resource_group_name.setter
    def aks_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6179ec6fb80c523d3bbccb2b6580f1f29112d47edae838bd46f35883dbc7999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aksResourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__277c847b46190413d77cdd0ec9934c355c98b40f731ac2beba195207710617de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZones", value)

    @builtins.property
    @jsii.member(jsii_name="controllerClusterId")
    def controller_cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controllerClusterId"))

    @controller_cluster_id.setter
    def controller_cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37accc031cfce63d2dede6fb5e99addd1ffafe921af10c1d3bded64a9f38de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controllerClusterId", value)

    @builtins.property
    @jsii.member(jsii_name="enableNodePublicIp")
    def enable_node_public_ip(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableNodePublicIp"))

    @enable_node_public_ip.setter
    def enable_node_public_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44df0c8a8822bc1dcd738c59f5a3909445fb3aec5820edabc5722192d5a098ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableNodePublicIp", value)

    @builtins.property
    @jsii.member(jsii_name="fallbackToOndemand")
    def fallback_to_ondemand(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fallbackToOndemand"))

    @fallback_to_ondemand.setter
    def fallback_to_ondemand(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7b35b0a5c743235e1ae0ff043dc3e570e58168eb4e23805c4af0d49d26b1e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fallbackToOndemand", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d260296295b25370fc455d1d4c9a607901c5cf42dacfb779bcb1e0557886d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="kubernetesVersion")
    def kubernetes_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kubernetesVersion"))

    @kubernetes_version.setter
    def kubernetes_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f205fc97059e2e675db7cd66935260bb789b418a7ef2c5000f834971da7bade1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kubernetesVersion", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3021f2aa21020ec377f6d47e7e39dca0e27337a2fb5afa335f86be5f073cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="maxCount")
    def max_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxCount"))

    @max_count.setter
    def max_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47778ca946ad4ccfe14cfe5ae2a85cfc6c161788aed5f8697d1e4718505439ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxCount", value)

    @builtins.property
    @jsii.member(jsii_name="maxPodsPerNode")
    def max_pods_per_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPodsPerNode"))

    @max_pods_per_node.setter
    def max_pods_per_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88419e6c825defaa4ac92fe1c20480259588dc45277611521e2a183eae035a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPodsPerNode", value)

    @builtins.property
    @jsii.member(jsii_name="minCount")
    def min_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minCount"))

    @min_count.setter
    def min_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87ed622c0b11d0f2b346ba0ec6761aba7c644142354bfcc76466be4f28f1469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCount", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b336cc34e01b20430edee7becd47c00b9fd1e4f8dce0b2d9d4f5944aee8b153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="osDiskSizeGb")
    def os_disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "osDiskSizeGb"))

    @os_disk_size_gb.setter
    def os_disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5297b4865bb4041d494b256e9a6a1ca46517024b5172258ef6a2adce38ce5bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDiskSizeGb", value)

    @builtins.property
    @jsii.member(jsii_name="osDiskType")
    def os_disk_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osDiskType"))

    @os_disk_type.setter
    def os_disk_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e34a9a6875fb6e0b20bd147f857ece0bffef93a279e097c559567a1dddef51d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDiskType", value)

    @builtins.property
    @jsii.member(jsii_name="osSku")
    def os_sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osSku"))

    @os_sku.setter
    def os_sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338e5f41b3606d67e98979a8864305bbbe7e85e06153bc623a1c7529c0c3fea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osSku", value)

    @builtins.property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osType"))

    @os_type.setter
    def os_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a405be31d799aaa7a83bbb92dabe9622e3cfbc1cbfe473d34a12036422aa9abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osType", value)

    @builtins.property
    @jsii.member(jsii_name="spotPercentage")
    def spot_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "spotPercentage"))

    @spot_percentage.setter
    def spot_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a17ecd73e9618bd166376ebe256e68840e49d45a403e6fcbabf779f0417e2a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "spotPercentage", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f840978c379636cb42b7cfb9b618103389df7c9747536fdc06b6cede3362a1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpAutoscaler",
    jsii_struct_bases=[],
    name_mapping={
        "autoscale_down": "autoscaleDown",
        "autoscale_headroom": "autoscaleHeadroom",
        "autoscale_is_enabled": "autoscaleIsEnabled",
        "resource_limits": "resourceLimits",
    },
)
class OceanAksNpAutoscaler:
    def __init__(
        self,
        *,
        autoscale_down: typing.Optional[typing.Union["OceanAksNpAutoscalerAutoscaleDown", typing.Dict[builtins.str, typing.Any]]] = None,
        autoscale_headroom: typing.Optional[typing.Union["OceanAksNpAutoscalerAutoscaleHeadroom", typing.Dict[builtins.str, typing.Any]]] = None,
        autoscale_is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_limits: typing.Optional[typing.Union["OceanAksNpAutoscalerResourceLimits", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param autoscale_down: autoscale_down block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#autoscale_down OceanAksNp#autoscale_down}
        :param autoscale_headroom: autoscale_headroom block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#autoscale_headroom OceanAksNp#autoscale_headroom}
        :param autoscale_is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#autoscale_is_enabled OceanAksNp#autoscale_is_enabled}.
        :param resource_limits: resource_limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#resource_limits OceanAksNp#resource_limits}
        '''
        if isinstance(autoscale_down, dict):
            autoscale_down = OceanAksNpAutoscalerAutoscaleDown(**autoscale_down)
        if isinstance(autoscale_headroom, dict):
            autoscale_headroom = OceanAksNpAutoscalerAutoscaleHeadroom(**autoscale_headroom)
        if isinstance(resource_limits, dict):
            resource_limits = OceanAksNpAutoscalerResourceLimits(**resource_limits)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd5b84fed7b90a6e8df57726b3376ad4897744a5f1d3df74f1742a1eba4d2eb)
            check_type(argname="argument autoscale_down", value=autoscale_down, expected_type=type_hints["autoscale_down"])
            check_type(argname="argument autoscale_headroom", value=autoscale_headroom, expected_type=type_hints["autoscale_headroom"])
            check_type(argname="argument autoscale_is_enabled", value=autoscale_is_enabled, expected_type=type_hints["autoscale_is_enabled"])
            check_type(argname="argument resource_limits", value=resource_limits, expected_type=type_hints["resource_limits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autoscale_down is not None:
            self._values["autoscale_down"] = autoscale_down
        if autoscale_headroom is not None:
            self._values["autoscale_headroom"] = autoscale_headroom
        if autoscale_is_enabled is not None:
            self._values["autoscale_is_enabled"] = autoscale_is_enabled
        if resource_limits is not None:
            self._values["resource_limits"] = resource_limits

    @builtins.property
    def autoscale_down(self) -> typing.Optional["OceanAksNpAutoscalerAutoscaleDown"]:
        '''autoscale_down block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#autoscale_down OceanAksNp#autoscale_down}
        '''
        result = self._values.get("autoscale_down")
        return typing.cast(typing.Optional["OceanAksNpAutoscalerAutoscaleDown"], result)

    @builtins.property
    def autoscale_headroom(
        self,
    ) -> typing.Optional["OceanAksNpAutoscalerAutoscaleHeadroom"]:
        '''autoscale_headroom block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#autoscale_headroom OceanAksNp#autoscale_headroom}
        '''
        result = self._values.get("autoscale_headroom")
        return typing.cast(typing.Optional["OceanAksNpAutoscalerAutoscaleHeadroom"], result)

    @builtins.property
    def autoscale_is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#autoscale_is_enabled OceanAksNp#autoscale_is_enabled}.'''
        result = self._values.get("autoscale_is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def resource_limits(self) -> typing.Optional["OceanAksNpAutoscalerResourceLimits"]:
        '''resource_limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#resource_limits OceanAksNp#resource_limits}
        '''
        result = self._values.get("resource_limits")
        return typing.cast(typing.Optional["OceanAksNpAutoscalerResourceLimits"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNpAutoscaler(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpAutoscalerAutoscaleDown",
    jsii_struct_bases=[],
    name_mapping={"max_scale_down_percentage": "maxScaleDownPercentage"},
)
class OceanAksNpAutoscalerAutoscaleDown:
    def __init__(
        self,
        *,
        max_scale_down_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scale_down_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_scale_down_percentage OceanAksNp#max_scale_down_percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90025a750dab1d36f316beb5c4d4bc277fb2fece46d0c095beee1b058f490a97)
            check_type(argname="argument max_scale_down_percentage", value=max_scale_down_percentage, expected_type=type_hints["max_scale_down_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_scale_down_percentage is not None:
            self._values["max_scale_down_percentage"] = max_scale_down_percentage

    @builtins.property
    def max_scale_down_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_scale_down_percentage OceanAksNp#max_scale_down_percentage}.'''
        result = self._values.get("max_scale_down_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNpAutoscalerAutoscaleDown(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksNpAutoscalerAutoscaleDownOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpAutoscalerAutoscaleDownOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e323dc3d55845c8138edb6fa0ed07b64348d49458e8d173ad68cf23277bd56f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxScaleDownPercentage")
    def reset_max_scale_down_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxScaleDownPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="maxScaleDownPercentageInput")
    def max_scale_down_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxScaleDownPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="maxScaleDownPercentage")
    def max_scale_down_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxScaleDownPercentage"))

    @max_scale_down_percentage.setter
    def max_scale_down_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e211cc7941a4f9d530dab9597943bd8cc3102383b1020c7ea5938be4144edea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxScaleDownPercentage", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksNpAutoscalerAutoscaleDown]:
        return typing.cast(typing.Optional[OceanAksNpAutoscalerAutoscaleDown], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OceanAksNpAutoscalerAutoscaleDown],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694925ba377ee2297c478fa7de17a6028ae390c9b028bdb0ef21a8bbaf61cb13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpAutoscalerAutoscaleHeadroom",
    jsii_struct_bases=[],
    name_mapping={"automatic": "automatic"},
)
class OceanAksNpAutoscalerAutoscaleHeadroom:
    def __init__(
        self,
        *,
        automatic: typing.Optional[typing.Union["OceanAksNpAutoscalerAutoscaleHeadroomAutomatic", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param automatic: automatic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#automatic OceanAksNp#automatic}
        '''
        if isinstance(automatic, dict):
            automatic = OceanAksNpAutoscalerAutoscaleHeadroomAutomatic(**automatic)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f3500b9c60d85bcf43c8bfb06f8a67e246dfe5c2c75f4a0cf43faa35e91db9d)
            check_type(argname="argument automatic", value=automatic, expected_type=type_hints["automatic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automatic is not None:
            self._values["automatic"] = automatic

    @builtins.property
    def automatic(
        self,
    ) -> typing.Optional["OceanAksNpAutoscalerAutoscaleHeadroomAutomatic"]:
        '''automatic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#automatic OceanAksNp#automatic}
        '''
        result = self._values.get("automatic")
        return typing.cast(typing.Optional["OceanAksNpAutoscalerAutoscaleHeadroomAutomatic"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNpAutoscalerAutoscaleHeadroom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpAutoscalerAutoscaleHeadroomAutomatic",
    jsii_struct_bases=[],
    name_mapping={"percentage": "percentage"},
)
class OceanAksNpAutoscalerAutoscaleHeadroomAutomatic:
    def __init__(self, *, percentage: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#percentage OceanAksNp#percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14a6682d5e28cfd7d5d2788a7f90a30240c46435e6bd6e853722b0c11de95fa6)
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if percentage is not None:
            self._values["percentage"] = percentage

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#percentage OceanAksNp#percentage}.'''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNpAutoscalerAutoscaleHeadroomAutomatic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksNpAutoscalerAutoscaleHeadroomAutomaticOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpAutoscalerAutoscaleHeadroomAutomaticOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b7cb40a358c82222c6e38ba5aa9b9f55f00ba74337ecd6896e5d1a62874cc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPercentage")
    def reset_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="percentageInput")
    def percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentageInput"))

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9164955a5ae0aada1ca6cee1a1ee85d69ad7c4686e4005350b5be4899038b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OceanAksNpAutoscalerAutoscaleHeadroomAutomatic]:
        return typing.cast(typing.Optional[OceanAksNpAutoscalerAutoscaleHeadroomAutomatic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OceanAksNpAutoscalerAutoscaleHeadroomAutomatic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59fbba227f6bd247ed11b119bc5e54ce48f5b9c7aec7d0646366479d2f94fc2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksNpAutoscalerAutoscaleHeadroomOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpAutoscalerAutoscaleHeadroomOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0919e878c242a679f4ee67c299f7c4bb7af254bbad557c02a1273830852f338)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutomatic")
    def put_automatic(self, *, percentage: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#percentage OceanAksNp#percentage}.
        '''
        value = OceanAksNpAutoscalerAutoscaleHeadroomAutomatic(percentage=percentage)

        return typing.cast(None, jsii.invoke(self, "putAutomatic", [value]))

    @jsii.member(jsii_name="resetAutomatic")
    def reset_automatic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomatic", []))

    @builtins.property
    @jsii.member(jsii_name="automatic")
    def automatic(
        self,
    ) -> OceanAksNpAutoscalerAutoscaleHeadroomAutomaticOutputReference:
        return typing.cast(OceanAksNpAutoscalerAutoscaleHeadroomAutomaticOutputReference, jsii.get(self, "automatic"))

    @builtins.property
    @jsii.member(jsii_name="automaticInput")
    def automatic_input(
        self,
    ) -> typing.Optional[OceanAksNpAutoscalerAutoscaleHeadroomAutomatic]:
        return typing.cast(typing.Optional[OceanAksNpAutoscalerAutoscaleHeadroomAutomatic], jsii.get(self, "automaticInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksNpAutoscalerAutoscaleHeadroom]:
        return typing.cast(typing.Optional[OceanAksNpAutoscalerAutoscaleHeadroom], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OceanAksNpAutoscalerAutoscaleHeadroom],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c244f9824c5e7cb48ea4637399431e5bc70474602ca5922ee474962451c71e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksNpAutoscalerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpAutoscalerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7b3548c7c7a2d7cf9ed3738e3162adc17b8b3086567472ad6ad6854c948256)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscaleDown")
    def put_autoscale_down(
        self,
        *,
        max_scale_down_percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_scale_down_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_scale_down_percentage OceanAksNp#max_scale_down_percentage}.
        '''
        value = OceanAksNpAutoscalerAutoscaleDown(
            max_scale_down_percentage=max_scale_down_percentage
        )

        return typing.cast(None, jsii.invoke(self, "putAutoscaleDown", [value]))

    @jsii.member(jsii_name="putAutoscaleHeadroom")
    def put_autoscale_headroom(
        self,
        *,
        automatic: typing.Optional[typing.Union[OceanAksNpAutoscalerAutoscaleHeadroomAutomatic, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param automatic: automatic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#automatic OceanAksNp#automatic}
        '''
        value = OceanAksNpAutoscalerAutoscaleHeadroom(automatic=automatic)

        return typing.cast(None, jsii.invoke(self, "putAutoscaleHeadroom", [value]))

    @jsii.member(jsii_name="putResourceLimits")
    def put_resource_limits(
        self,
        *,
        max_memory_gib: typing.Optional[jsii.Number] = None,
        max_vcpu: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_memory_gib: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_memory_gib OceanAksNp#max_memory_gib}.
        :param max_vcpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_vcpu OceanAksNp#max_vcpu}.
        '''
        value = OceanAksNpAutoscalerResourceLimits(
            max_memory_gib=max_memory_gib, max_vcpu=max_vcpu
        )

        return typing.cast(None, jsii.invoke(self, "putResourceLimits", [value]))

    @jsii.member(jsii_name="resetAutoscaleDown")
    def reset_autoscale_down(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaleDown", []))

    @jsii.member(jsii_name="resetAutoscaleHeadroom")
    def reset_autoscale_headroom(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaleHeadroom", []))

    @jsii.member(jsii_name="resetAutoscaleIsEnabled")
    def reset_autoscale_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscaleIsEnabled", []))

    @jsii.member(jsii_name="resetResourceLimits")
    def reset_resource_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceLimits", []))

    @builtins.property
    @jsii.member(jsii_name="autoscaleDown")
    def autoscale_down(self) -> OceanAksNpAutoscalerAutoscaleDownOutputReference:
        return typing.cast(OceanAksNpAutoscalerAutoscaleDownOutputReference, jsii.get(self, "autoscaleDown"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleHeadroom")
    def autoscale_headroom(
        self,
    ) -> OceanAksNpAutoscalerAutoscaleHeadroomOutputReference:
        return typing.cast(OceanAksNpAutoscalerAutoscaleHeadroomOutputReference, jsii.get(self, "autoscaleHeadroom"))

    @builtins.property
    @jsii.member(jsii_name="resourceLimits")
    def resource_limits(self) -> "OceanAksNpAutoscalerResourceLimitsOutputReference":
        return typing.cast("OceanAksNpAutoscalerResourceLimitsOutputReference", jsii.get(self, "resourceLimits"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleDownInput")
    def autoscale_down_input(
        self,
    ) -> typing.Optional[OceanAksNpAutoscalerAutoscaleDown]:
        return typing.cast(typing.Optional[OceanAksNpAutoscalerAutoscaleDown], jsii.get(self, "autoscaleDownInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleHeadroomInput")
    def autoscale_headroom_input(
        self,
    ) -> typing.Optional[OceanAksNpAutoscalerAutoscaleHeadroom]:
        return typing.cast(typing.Optional[OceanAksNpAutoscalerAutoscaleHeadroom], jsii.get(self, "autoscaleHeadroomInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleIsEnabledInput")
    def autoscale_is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoscaleIsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceLimitsInput")
    def resource_limits_input(
        self,
    ) -> typing.Optional["OceanAksNpAutoscalerResourceLimits"]:
        return typing.cast(typing.Optional["OceanAksNpAutoscalerResourceLimits"], jsii.get(self, "resourceLimitsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoscaleIsEnabled")
    def autoscale_is_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoscaleIsEnabled"))

    @autoscale_is_enabled.setter
    def autoscale_is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da55f0718b621653af224776827ca6681da47a8b7520c55d829dfaf411c63382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoscaleIsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksNpAutoscaler]:
        return typing.cast(typing.Optional[OceanAksNpAutoscaler], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OceanAksNpAutoscaler]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1648c48e96a0709637e03dddcca11e4292b34ea0ae7e40867a72cc2e85b66e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpAutoscalerResourceLimits",
    jsii_struct_bases=[],
    name_mapping={"max_memory_gib": "maxMemoryGib", "max_vcpu": "maxVcpu"},
)
class OceanAksNpAutoscalerResourceLimits:
    def __init__(
        self,
        *,
        max_memory_gib: typing.Optional[jsii.Number] = None,
        max_vcpu: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_memory_gib: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_memory_gib OceanAksNp#max_memory_gib}.
        :param max_vcpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_vcpu OceanAksNp#max_vcpu}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5a0c123b4007faf87d6c403994a74c1db5f68aedd37c6754116ad94e1164fd)
            check_type(argname="argument max_memory_gib", value=max_memory_gib, expected_type=type_hints["max_memory_gib"])
            check_type(argname="argument max_vcpu", value=max_vcpu, expected_type=type_hints["max_vcpu"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_memory_gib is not None:
            self._values["max_memory_gib"] = max_memory_gib
        if max_vcpu is not None:
            self._values["max_vcpu"] = max_vcpu

    @builtins.property
    def max_memory_gib(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_memory_gib OceanAksNp#max_memory_gib}.'''
        result = self._values.get("max_memory_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_vcpu(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_vcpu OceanAksNp#max_vcpu}.'''
        result = self._values.get("max_vcpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNpAutoscalerResourceLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksNpAutoscalerResourceLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpAutoscalerResourceLimitsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71cbffbd897e11688fd174fd8ed556b1888ea72e313351b955cab1461248eec7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxMemoryGib")
    def reset_max_memory_gib(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxMemoryGib", []))

    @jsii.member(jsii_name="resetMaxVcpu")
    def reset_max_vcpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxVcpu", []))

    @builtins.property
    @jsii.member(jsii_name="maxMemoryGibInput")
    def max_memory_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxMemoryGibInput"))

    @builtins.property
    @jsii.member(jsii_name="maxVcpuInput")
    def max_vcpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxVcpuInput"))

    @builtins.property
    @jsii.member(jsii_name="maxMemoryGib")
    def max_memory_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxMemoryGib"))

    @max_memory_gib.setter
    def max_memory_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14ca6f83844bc92b5506d7a61488a3b988fb9b002111e37c86faf65b58dec24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxMemoryGib", value)

    @builtins.property
    @jsii.member(jsii_name="maxVcpu")
    def max_vcpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxVcpu"))

    @max_vcpu.setter
    def max_vcpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b89ad8c1aa30471337199f6611e44ca026982358d6a0c5d6a9cb325ce4469b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxVcpu", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksNpAutoscalerResourceLimits]:
        return typing.cast(typing.Optional[OceanAksNpAutoscalerResourceLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OceanAksNpAutoscalerResourceLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bda71648bd77cd9febd4bf4fe53060c188279f266968f16f74a65d6b6e348bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "aks_cluster_name": "aksClusterName",
        "aks_infrastructure_resource_group_name": "aksInfrastructureResourceGroupName",
        "aks_region": "aksRegion",
        "aks_resource_group_name": "aksResourceGroupName",
        "availability_zones": "availabilityZones",
        "name": "name",
        "autoscaler": "autoscaler",
        "controller_cluster_id": "controllerClusterId",
        "enable_node_public_ip": "enableNodePublicIp",
        "fallback_to_ondemand": "fallbackToOndemand",
        "filters": "filters",
        "headrooms": "headrooms",
        "health": "health",
        "id": "id",
        "kubernetes_version": "kubernetesVersion",
        "labels": "labels",
        "max_count": "maxCount",
        "max_pods_per_node": "maxPodsPerNode",
        "min_count": "minCount",
        "os_disk_size_gb": "osDiskSizeGb",
        "os_disk_type": "osDiskType",
        "os_sku": "osSku",
        "os_type": "osType",
        "scheduling": "scheduling",
        "spot_percentage": "spotPercentage",
        "tags": "tags",
        "taints": "taints",
    },
)
class OceanAksNpConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        aks_cluster_name: builtins.str,
        aks_infrastructure_resource_group_name: builtins.str,
        aks_region: builtins.str,
        aks_resource_group_name: builtins.str,
        availability_zones: typing.Sequence[builtins.str],
        name: builtins.str,
        autoscaler: typing.Optional[typing.Union[OceanAksNpAutoscaler, typing.Dict[builtins.str, typing.Any]]] = None,
        controller_cluster_id: typing.Optional[builtins.str] = None,
        enable_node_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        fallback_to_ondemand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filters: typing.Optional[typing.Union["OceanAksNpFilters", typing.Dict[builtins.str, typing.Any]]] = None,
        headrooms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksNpHeadrooms", typing.Dict[builtins.str, typing.Any]]]]] = None,
        health: typing.Optional[typing.Union["OceanAksNpHealth", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kubernetes_version: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_count: typing.Optional[jsii.Number] = None,
        max_pods_per_node: typing.Optional[jsii.Number] = None,
        min_count: typing.Optional[jsii.Number] = None,
        os_disk_size_gb: typing.Optional[jsii.Number] = None,
        os_disk_type: typing.Optional[builtins.str] = None,
        os_sku: typing.Optional[builtins.str] = None,
        os_type: typing.Optional[builtins.str] = None,
        scheduling: typing.Optional[typing.Union["OceanAksNpScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        spot_percentage: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OceanAksNpTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param aks_cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#aks_cluster_name OceanAksNp#aks_cluster_name}.
        :param aks_infrastructure_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#aks_infrastructure_resource_group_name OceanAksNp#aks_infrastructure_resource_group_name}.
        :param aks_region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#aks_region OceanAksNp#aks_region}.
        :param aks_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#aks_resource_group_name OceanAksNp#aks_resource_group_name}.
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#availability_zones OceanAksNp#availability_zones}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#name OceanAksNp#name}.
        :param autoscaler: autoscaler block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#autoscaler OceanAksNp#autoscaler}
        :param controller_cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#controller_cluster_id OceanAksNp#controller_cluster_id}.
        :param enable_node_public_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#enable_node_public_ip OceanAksNp#enable_node_public_ip}.
        :param fallback_to_ondemand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#fallback_to_ondemand OceanAksNp#fallback_to_ondemand}.
        :param filters: filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#filters OceanAksNp#filters}
        :param headrooms: headrooms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#headrooms OceanAksNp#headrooms}
        :param health: health block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#health OceanAksNp#health}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#id OceanAksNp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubernetes_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#kubernetes_version OceanAksNp#kubernetes_version}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#labels OceanAksNp#labels}.
        :param max_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_count OceanAksNp#max_count}.
        :param max_pods_per_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_pods_per_node OceanAksNp#max_pods_per_node}.
        :param min_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#min_count OceanAksNp#min_count}.
        :param os_disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#os_disk_size_gb OceanAksNp#os_disk_size_gb}.
        :param os_disk_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#os_disk_type OceanAksNp#os_disk_type}.
        :param os_sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#os_sku OceanAksNp#os_sku}.
        :param os_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#os_type OceanAksNp#os_type}.
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#scheduling OceanAksNp#scheduling}
        :param spot_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#spot_percentage OceanAksNp#spot_percentage}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#tags OceanAksNp#tags}.
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#taints OceanAksNp#taints}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(autoscaler, dict):
            autoscaler = OceanAksNpAutoscaler(**autoscaler)
        if isinstance(filters, dict):
            filters = OceanAksNpFilters(**filters)
        if isinstance(health, dict):
            health = OceanAksNpHealth(**health)
        if isinstance(scheduling, dict):
            scheduling = OceanAksNpScheduling(**scheduling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9bab4f3e98d3b0cba441a02e1e4220b0e83e9de8e80d93eb0348c9802bbac4b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument aks_cluster_name", value=aks_cluster_name, expected_type=type_hints["aks_cluster_name"])
            check_type(argname="argument aks_infrastructure_resource_group_name", value=aks_infrastructure_resource_group_name, expected_type=type_hints["aks_infrastructure_resource_group_name"])
            check_type(argname="argument aks_region", value=aks_region, expected_type=type_hints["aks_region"])
            check_type(argname="argument aks_resource_group_name", value=aks_resource_group_name, expected_type=type_hints["aks_resource_group_name"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument autoscaler", value=autoscaler, expected_type=type_hints["autoscaler"])
            check_type(argname="argument controller_cluster_id", value=controller_cluster_id, expected_type=type_hints["controller_cluster_id"])
            check_type(argname="argument enable_node_public_ip", value=enable_node_public_ip, expected_type=type_hints["enable_node_public_ip"])
            check_type(argname="argument fallback_to_ondemand", value=fallback_to_ondemand, expected_type=type_hints["fallback_to_ondemand"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument headrooms", value=headrooms, expected_type=type_hints["headrooms"])
            check_type(argname="argument health", value=health, expected_type=type_hints["health"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kubernetes_version", value=kubernetes_version, expected_type=type_hints["kubernetes_version"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument max_count", value=max_count, expected_type=type_hints["max_count"])
            check_type(argname="argument max_pods_per_node", value=max_pods_per_node, expected_type=type_hints["max_pods_per_node"])
            check_type(argname="argument min_count", value=min_count, expected_type=type_hints["min_count"])
            check_type(argname="argument os_disk_size_gb", value=os_disk_size_gb, expected_type=type_hints["os_disk_size_gb"])
            check_type(argname="argument os_disk_type", value=os_disk_type, expected_type=type_hints["os_disk_type"])
            check_type(argname="argument os_sku", value=os_sku, expected_type=type_hints["os_sku"])
            check_type(argname="argument os_type", value=os_type, expected_type=type_hints["os_type"])
            check_type(argname="argument scheduling", value=scheduling, expected_type=type_hints["scheduling"])
            check_type(argname="argument spot_percentage", value=spot_percentage, expected_type=type_hints["spot_percentage"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aks_cluster_name": aks_cluster_name,
            "aks_infrastructure_resource_group_name": aks_infrastructure_resource_group_name,
            "aks_region": aks_region,
            "aks_resource_group_name": aks_resource_group_name,
            "availability_zones": availability_zones,
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
        if autoscaler is not None:
            self._values["autoscaler"] = autoscaler
        if controller_cluster_id is not None:
            self._values["controller_cluster_id"] = controller_cluster_id
        if enable_node_public_ip is not None:
            self._values["enable_node_public_ip"] = enable_node_public_ip
        if fallback_to_ondemand is not None:
            self._values["fallback_to_ondemand"] = fallback_to_ondemand
        if filters is not None:
            self._values["filters"] = filters
        if headrooms is not None:
            self._values["headrooms"] = headrooms
        if health is not None:
            self._values["health"] = health
        if id is not None:
            self._values["id"] = id
        if kubernetes_version is not None:
            self._values["kubernetes_version"] = kubernetes_version
        if labels is not None:
            self._values["labels"] = labels
        if max_count is not None:
            self._values["max_count"] = max_count
        if max_pods_per_node is not None:
            self._values["max_pods_per_node"] = max_pods_per_node
        if min_count is not None:
            self._values["min_count"] = min_count
        if os_disk_size_gb is not None:
            self._values["os_disk_size_gb"] = os_disk_size_gb
        if os_disk_type is not None:
            self._values["os_disk_type"] = os_disk_type
        if os_sku is not None:
            self._values["os_sku"] = os_sku
        if os_type is not None:
            self._values["os_type"] = os_type
        if scheduling is not None:
            self._values["scheduling"] = scheduling
        if spot_percentage is not None:
            self._values["spot_percentage"] = spot_percentage
        if tags is not None:
            self._values["tags"] = tags
        if taints is not None:
            self._values["taints"] = taints

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
    def aks_cluster_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#aks_cluster_name OceanAksNp#aks_cluster_name}.'''
        result = self._values.get("aks_cluster_name")
        assert result is not None, "Required property 'aks_cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aks_infrastructure_resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#aks_infrastructure_resource_group_name OceanAksNp#aks_infrastructure_resource_group_name}.'''
        result = self._values.get("aks_infrastructure_resource_group_name")
        assert result is not None, "Required property 'aks_infrastructure_resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aks_region(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#aks_region OceanAksNp#aks_region}.'''
        result = self._values.get("aks_region")
        assert result is not None, "Required property 'aks_region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aks_resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#aks_resource_group_name OceanAksNp#aks_resource_group_name}.'''
        result = self._values.get("aks_resource_group_name")
        assert result is not None, "Required property 'aks_resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def availability_zones(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#availability_zones OceanAksNp#availability_zones}.'''
        result = self._values.get("availability_zones")
        assert result is not None, "Required property 'availability_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#name OceanAksNp#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autoscaler(self) -> typing.Optional[OceanAksNpAutoscaler]:
        '''autoscaler block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#autoscaler OceanAksNp#autoscaler}
        '''
        result = self._values.get("autoscaler")
        return typing.cast(typing.Optional[OceanAksNpAutoscaler], result)

    @builtins.property
    def controller_cluster_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#controller_cluster_id OceanAksNp#controller_cluster_id}.'''
        result = self._values.get("controller_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_node_public_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#enable_node_public_ip OceanAksNp#enable_node_public_ip}.'''
        result = self._values.get("enable_node_public_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def fallback_to_ondemand(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#fallback_to_ondemand OceanAksNp#fallback_to_ondemand}.'''
        result = self._values.get("fallback_to_ondemand")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filters(self) -> typing.Optional["OceanAksNpFilters"]:
        '''filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#filters OceanAksNp#filters}
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional["OceanAksNpFilters"], result)

    @builtins.property
    def headrooms(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksNpHeadrooms"]]]:
        '''headrooms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#headrooms OceanAksNp#headrooms}
        '''
        result = self._values.get("headrooms")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksNpHeadrooms"]]], result)

    @builtins.property
    def health(self) -> typing.Optional["OceanAksNpHealth"]:
        '''health block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#health OceanAksNp#health}
        '''
        result = self._values.get("health")
        return typing.cast(typing.Optional["OceanAksNpHealth"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#id OceanAksNp#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubernetes_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#kubernetes_version OceanAksNp#kubernetes_version}.'''
        result = self._values.get("kubernetes_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#labels OceanAksNp#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_count OceanAksNp#max_count}.'''
        result = self._values.get("max_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_pods_per_node(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_pods_per_node OceanAksNp#max_pods_per_node}.'''
        result = self._values.get("max_pods_per_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#min_count OceanAksNp#min_count}.'''
        result = self._values.get("min_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def os_disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#os_disk_size_gb OceanAksNp#os_disk_size_gb}.'''
        result = self._values.get("os_disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def os_disk_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#os_disk_type OceanAksNp#os_disk_type}.'''
        result = self._values.get("os_disk_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#os_sku OceanAksNp#os_sku}.'''
        result = self._values.get("os_sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#os_type OceanAksNp#os_type}.'''
        result = self._values.get("os_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduling(self) -> typing.Optional["OceanAksNpScheduling"]:
        '''scheduling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#scheduling OceanAksNp#scheduling}
        '''
        result = self._values.get("scheduling")
        return typing.cast(typing.Optional["OceanAksNpScheduling"], result)

    @builtins.property
    def spot_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#spot_percentage OceanAksNp#spot_percentage}.'''
        result = self._values.get("spot_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#tags OceanAksNp#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksNpTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#taints OceanAksNp#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OceanAksNpTaints"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpFilters",
    jsii_struct_bases=[],
    name_mapping={
        "architectures": "architectures",
        "exclude_series": "excludeSeries",
        "max_memory_gib": "maxMemoryGib",
        "max_vcpu": "maxVcpu",
        "min_memory_gib": "minMemoryGib",
        "min_vcpu": "minVcpu",
        "series": "series",
    },
)
class OceanAksNpFilters:
    def __init__(
        self,
        *,
        architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_series: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_memory_gib: typing.Optional[jsii.Number] = None,
        max_vcpu: typing.Optional[jsii.Number] = None,
        min_memory_gib: typing.Optional[jsii.Number] = None,
        min_vcpu: typing.Optional[jsii.Number] = None,
        series: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param architectures: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#architectures OceanAksNp#architectures}.
        :param exclude_series: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#exclude_series OceanAksNp#exclude_series}.
        :param max_memory_gib: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_memory_gib OceanAksNp#max_memory_gib}.
        :param max_vcpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_vcpu OceanAksNp#max_vcpu}.
        :param min_memory_gib: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#min_memory_gib OceanAksNp#min_memory_gib}.
        :param min_vcpu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#min_vcpu OceanAksNp#min_vcpu}.
        :param series: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#series OceanAksNp#series}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a9f7ac92271595654997c1c567d2192601f5aa35699adec679624356c181ab)
            check_type(argname="argument architectures", value=architectures, expected_type=type_hints["architectures"])
            check_type(argname="argument exclude_series", value=exclude_series, expected_type=type_hints["exclude_series"])
            check_type(argname="argument max_memory_gib", value=max_memory_gib, expected_type=type_hints["max_memory_gib"])
            check_type(argname="argument max_vcpu", value=max_vcpu, expected_type=type_hints["max_vcpu"])
            check_type(argname="argument min_memory_gib", value=min_memory_gib, expected_type=type_hints["min_memory_gib"])
            check_type(argname="argument min_vcpu", value=min_vcpu, expected_type=type_hints["min_vcpu"])
            check_type(argname="argument series", value=series, expected_type=type_hints["series"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architectures is not None:
            self._values["architectures"] = architectures
        if exclude_series is not None:
            self._values["exclude_series"] = exclude_series
        if max_memory_gib is not None:
            self._values["max_memory_gib"] = max_memory_gib
        if max_vcpu is not None:
            self._values["max_vcpu"] = max_vcpu
        if min_memory_gib is not None:
            self._values["min_memory_gib"] = min_memory_gib
        if min_vcpu is not None:
            self._values["min_vcpu"] = min_vcpu
        if series is not None:
            self._values["series"] = series

    @builtins.property
    def architectures(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#architectures OceanAksNp#architectures}.'''
        result = self._values.get("architectures")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclude_series(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#exclude_series OceanAksNp#exclude_series}.'''
        result = self._values.get("exclude_series")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_memory_gib(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_memory_gib OceanAksNp#max_memory_gib}.'''
        result = self._values.get("max_memory_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_vcpu(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#max_vcpu OceanAksNp#max_vcpu}.'''
        result = self._values.get("max_vcpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_memory_gib(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#min_memory_gib OceanAksNp#min_memory_gib}.'''
        result = self._values.get("min_memory_gib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_vcpu(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#min_vcpu OceanAksNp#min_vcpu}.'''
        result = self._values.get("min_vcpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def series(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#series OceanAksNp#series}.'''
        result = self._values.get("series")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNpFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksNpFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpFiltersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3d5c6b23f914408dcab4cd492a9e2c57a0dfc473c15cc81e6fed9569e4a885)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArchitectures")
    def reset_architectures(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchitectures", []))

    @jsii.member(jsii_name="resetExcludeSeries")
    def reset_exclude_series(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeSeries", []))

    @jsii.member(jsii_name="resetMaxMemoryGib")
    def reset_max_memory_gib(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxMemoryGib", []))

    @jsii.member(jsii_name="resetMaxVcpu")
    def reset_max_vcpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxVcpu", []))

    @jsii.member(jsii_name="resetMinMemoryGib")
    def reset_min_memory_gib(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinMemoryGib", []))

    @jsii.member(jsii_name="resetMinVcpu")
    def reset_min_vcpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinVcpu", []))

    @jsii.member(jsii_name="resetSeries")
    def reset_series(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeries", []))

    @builtins.property
    @jsii.member(jsii_name="architecturesInput")
    def architectures_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "architecturesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeSeriesInput")
    def exclude_series_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeSeriesInput"))

    @builtins.property
    @jsii.member(jsii_name="maxMemoryGibInput")
    def max_memory_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxMemoryGibInput"))

    @builtins.property
    @jsii.member(jsii_name="maxVcpuInput")
    def max_vcpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxVcpuInput"))

    @builtins.property
    @jsii.member(jsii_name="minMemoryGibInput")
    def min_memory_gib_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minMemoryGibInput"))

    @builtins.property
    @jsii.member(jsii_name="minVcpuInput")
    def min_vcpu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minVcpuInput"))

    @builtins.property
    @jsii.member(jsii_name="seriesInput")
    def series_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "seriesInput"))

    @builtins.property
    @jsii.member(jsii_name="architectures")
    def architectures(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "architectures"))

    @architectures.setter
    def architectures(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c742c1c4d9379baf6663ee29e90347b76841893ec7c21d5f0c078681e63b322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architectures", value)

    @builtins.property
    @jsii.member(jsii_name="excludeSeries")
    def exclude_series(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeSeries"))

    @exclude_series.setter
    def exclude_series(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c859c25dae8d7f829f8a4c7a10d8f95ea10064ef8ec38c26a9b7ec99c89146)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeSeries", value)

    @builtins.property
    @jsii.member(jsii_name="maxMemoryGib")
    def max_memory_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxMemoryGib"))

    @max_memory_gib.setter
    def max_memory_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7e75e2b21793f5c4a71c261dcd0e2f3c8c247bb5e8055027755fd8929fec3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxMemoryGib", value)

    @builtins.property
    @jsii.member(jsii_name="maxVcpu")
    def max_vcpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxVcpu"))

    @max_vcpu.setter
    def max_vcpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c124113da710685d1046267a1bef2d22b3f6c4960033e838db3f969d0c94544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxVcpu", value)

    @builtins.property
    @jsii.member(jsii_name="minMemoryGib")
    def min_memory_gib(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minMemoryGib"))

    @min_memory_gib.setter
    def min_memory_gib(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7006276093120f973474fc0cd23738284fa202900d8a7f7cdff0cf99fc52cbb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minMemoryGib", value)

    @builtins.property
    @jsii.member(jsii_name="minVcpu")
    def min_vcpu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minVcpu"))

    @min_vcpu.setter
    def min_vcpu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f9842d5ec88efa702799bf7305f81cdd9657e6343aeefea4a229a40d027493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minVcpu", value)

    @builtins.property
    @jsii.member(jsii_name="series")
    def series(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "series"))

    @series.setter
    def series(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2fa2a5a1c3686a833a5af9341349061e311b0645695207344c40eb87ab3e64e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "series", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksNpFilters]:
        return typing.cast(typing.Optional[OceanAksNpFilters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OceanAksNpFilters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31bd0fc5a502010cec257c33953fdf09d6f9013fd19fca25907e25d7b91be82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpHeadrooms",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_per_unit": "cpuPerUnit",
        "gpu_per_unit": "gpuPerUnit",
        "memory_per_unit": "memoryPerUnit",
        "num_of_units": "numOfUnits",
    },
)
class OceanAksNpHeadrooms:
    def __init__(
        self,
        *,
        cpu_per_unit: typing.Optional[jsii.Number] = None,
        gpu_per_unit: typing.Optional[jsii.Number] = None,
        memory_per_unit: typing.Optional[jsii.Number] = None,
        num_of_units: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_per_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#cpu_per_unit OceanAksNp#cpu_per_unit}.
        :param gpu_per_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#gpu_per_unit OceanAksNp#gpu_per_unit}.
        :param memory_per_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#memory_per_unit OceanAksNp#memory_per_unit}.
        :param num_of_units: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#num_of_units OceanAksNp#num_of_units}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f8750b24926f1ba765bf3f4bae5f9a952c815a93d08ba5ab409373a843371b)
            check_type(argname="argument cpu_per_unit", value=cpu_per_unit, expected_type=type_hints["cpu_per_unit"])
            check_type(argname="argument gpu_per_unit", value=gpu_per_unit, expected_type=type_hints["gpu_per_unit"])
            check_type(argname="argument memory_per_unit", value=memory_per_unit, expected_type=type_hints["memory_per_unit"])
            check_type(argname="argument num_of_units", value=num_of_units, expected_type=type_hints["num_of_units"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_per_unit is not None:
            self._values["cpu_per_unit"] = cpu_per_unit
        if gpu_per_unit is not None:
            self._values["gpu_per_unit"] = gpu_per_unit
        if memory_per_unit is not None:
            self._values["memory_per_unit"] = memory_per_unit
        if num_of_units is not None:
            self._values["num_of_units"] = num_of_units

    @builtins.property
    def cpu_per_unit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#cpu_per_unit OceanAksNp#cpu_per_unit}.'''
        result = self._values.get("cpu_per_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gpu_per_unit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#gpu_per_unit OceanAksNp#gpu_per_unit}.'''
        result = self._values.get("gpu_per_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_per_unit(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#memory_per_unit OceanAksNp#memory_per_unit}.'''
        result = self._values.get("memory_per_unit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def num_of_units(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#num_of_units OceanAksNp#num_of_units}.'''
        result = self._values.get("num_of_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNpHeadrooms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksNpHeadroomsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpHeadroomsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5c950d5f3f70655493d9d9c052fe216c9f66fcc7e611665d994f76175adb2fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OceanAksNpHeadroomsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddd81aaf8bb9776ce0913f2849cc0a6d8850205e7945e73eb68e7cd06190a2e3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksNpHeadroomsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974e4e6b976d69c90b5f86b11bfe4d68b5d80dc9e4861f115816562c61596d8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8066f1a1deb87058e4059c1959e90872007b95885d9438a3f8ce29bd6f4915f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__deaf9d4b8b9ae52192fc3601c0951f8914b64eb56931429524cd80ff38e28ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNpHeadrooms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNpHeadrooms]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNpHeadrooms]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930213753fd0fffc740533f09448e92002d97f00bf6f641ec3f39a8a3806a535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksNpHeadroomsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpHeadroomsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0ff8aa121081ccb41ad6c5fc8d3ea6631df992c898121214ebf3e687e08f17d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCpuPerUnit")
    def reset_cpu_per_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuPerUnit", []))

    @jsii.member(jsii_name="resetGpuPerUnit")
    def reset_gpu_per_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpuPerUnit", []))

    @jsii.member(jsii_name="resetMemoryPerUnit")
    def reset_memory_per_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryPerUnit", []))

    @jsii.member(jsii_name="resetNumOfUnits")
    def reset_num_of_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumOfUnits", []))

    @builtins.property
    @jsii.member(jsii_name="cpuPerUnitInput")
    def cpu_per_unit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuPerUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuPerUnitInput")
    def gpu_per_unit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gpuPerUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryPerUnitInput")
    def memory_per_unit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryPerUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="numOfUnitsInput")
    def num_of_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numOfUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuPerUnit")
    def cpu_per_unit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuPerUnit"))

    @cpu_per_unit.setter
    def cpu_per_unit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32475492fd397e67799604b757dd5b65aaac594140765ddbe0d8fb11ed5bcbe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuPerUnit", value)

    @builtins.property
    @jsii.member(jsii_name="gpuPerUnit")
    def gpu_per_unit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gpuPerUnit"))

    @gpu_per_unit.setter
    def gpu_per_unit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14959e319a974453ba22c4bc44072e335bd6d76e7eeb1dd1119a6378f4e4c1be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuPerUnit", value)

    @builtins.property
    @jsii.member(jsii_name="memoryPerUnit")
    def memory_per_unit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryPerUnit"))

    @memory_per_unit.setter
    def memory_per_unit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4aa00243509d7b4f1b0dd8329bd3517aae69bcdb204a1c47df019bff2c3b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryPerUnit", value)

    @builtins.property
    @jsii.member(jsii_name="numOfUnits")
    def num_of_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numOfUnits"))

    @num_of_units.setter
    def num_of_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856e5ad14de0acec5e7d139d2a8b96fc92c5ae52d209d7c616ede8873891bf0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numOfUnits", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OceanAksNpHeadrooms]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OceanAksNpHeadrooms]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OceanAksNpHeadrooms]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0561065072d4a65c55dd2068d56986da11a509b67366f7fa28ac74525134cfd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpHealth",
    jsii_struct_bases=[],
    name_mapping={"grace_period": "gracePeriod"},
)
class OceanAksNpHealth:
    def __init__(self, *, grace_period: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param grace_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#grace_period OceanAksNp#grace_period}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0446171353b1dda6da14d9676f214aa866da2a98185290415005f5b979db2eb7)
            check_type(argname="argument grace_period", value=grace_period, expected_type=type_hints["grace_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grace_period is not None:
            self._values["grace_period"] = grace_period

    @builtins.property
    def grace_period(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#grace_period OceanAksNp#grace_period}.'''
        result = self._values.get("grace_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNpHealth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksNpHealthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpHealthOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7aedccee9ce43e6ed6a3722e435b998ea72bcfb5ec8f247f3156ec79e8f40a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGracePeriod")
    def reset_grace_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGracePeriod", []))

    @builtins.property
    @jsii.member(jsii_name="gracePeriodInput")
    def grace_period_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gracePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="gracePeriod")
    def grace_period(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gracePeriod"))

    @grace_period.setter
    def grace_period(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913de7f1851a455383aaeebdae3597173c9cceb7381a5d37852b0b1bad8f04a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gracePeriod", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksNpHealth]:
        return typing.cast(typing.Optional[OceanAksNpHealth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OceanAksNpHealth]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf340db4cbe5a708e17e8e299156919e448f4418f16a733c27fa1313b55df2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpScheduling",
    jsii_struct_bases=[],
    name_mapping={"shutdown_hours": "shutdownHours"},
)
class OceanAksNpScheduling:
    def __init__(
        self,
        *,
        shutdown_hours: typing.Optional[typing.Union["OceanAksNpSchedulingShutdownHours", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param shutdown_hours: shutdown_hours block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#shutdown_hours OceanAksNp#shutdown_hours}
        '''
        if isinstance(shutdown_hours, dict):
            shutdown_hours = OceanAksNpSchedulingShutdownHours(**shutdown_hours)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d20ebe1bf5190dc49c807ca036b51189ee29c47672aba96614a263fd410910)
            check_type(argname="argument shutdown_hours", value=shutdown_hours, expected_type=type_hints["shutdown_hours"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if shutdown_hours is not None:
            self._values["shutdown_hours"] = shutdown_hours

    @builtins.property
    def shutdown_hours(self) -> typing.Optional["OceanAksNpSchedulingShutdownHours"]:
        '''shutdown_hours block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#shutdown_hours OceanAksNp#shutdown_hours}
        '''
        result = self._values.get("shutdown_hours")
        return typing.cast(typing.Optional["OceanAksNpSchedulingShutdownHours"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNpScheduling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksNpSchedulingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpSchedulingOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b23839593ae1052707b8b8b15a603e7cd9124c4d6717d97ec9d541fdaccdff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putShutdownHours")
    def put_shutdown_hours(
        self,
        *,
        time_windows: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param time_windows: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#time_windows OceanAksNp#time_windows}.
        :param is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#is_enabled OceanAksNp#is_enabled}.
        '''
        value = OceanAksNpSchedulingShutdownHours(
            time_windows=time_windows, is_enabled=is_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putShutdownHours", [value]))

    @jsii.member(jsii_name="resetShutdownHours")
    def reset_shutdown_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShutdownHours", []))

    @builtins.property
    @jsii.member(jsii_name="shutdownHours")
    def shutdown_hours(self) -> "OceanAksNpSchedulingShutdownHoursOutputReference":
        return typing.cast("OceanAksNpSchedulingShutdownHoursOutputReference", jsii.get(self, "shutdownHours"))

    @builtins.property
    @jsii.member(jsii_name="shutdownHoursInput")
    def shutdown_hours_input(
        self,
    ) -> typing.Optional["OceanAksNpSchedulingShutdownHours"]:
        return typing.cast(typing.Optional["OceanAksNpSchedulingShutdownHours"], jsii.get(self, "shutdownHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksNpScheduling]:
        return typing.cast(typing.Optional[OceanAksNpScheduling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OceanAksNpScheduling]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42efce885b277ff0467b937bbf380f852367148461159c02ec153066704117d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpSchedulingShutdownHours",
    jsii_struct_bases=[],
    name_mapping={"time_windows": "timeWindows", "is_enabled": "isEnabled"},
)
class OceanAksNpSchedulingShutdownHours:
    def __init__(
        self,
        *,
        time_windows: typing.Sequence[builtins.str],
        is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param time_windows: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#time_windows OceanAksNp#time_windows}.
        :param is_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#is_enabled OceanAksNp#is_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45995a95327fe7c1d819054ab0a424f8ca422d0b9989cab007cac55904f55d20)
            check_type(argname="argument time_windows", value=time_windows, expected_type=type_hints["time_windows"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "time_windows": time_windows,
        }
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled

    @builtins.property
    def time_windows(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#time_windows OceanAksNp#time_windows}.'''
        result = self._values.get("time_windows")
        assert result is not None, "Required property 'time_windows' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#is_enabled OceanAksNp#is_enabled}.'''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNpSchedulingShutdownHours(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksNpSchedulingShutdownHoursOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpSchedulingShutdownHoursOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da2f3033c6c0996a552559a0b6b2dc185633de63eb50d3ab1530eca4263504b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIsEnabled")
    def reset_is_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="isEnabledInput")
    def is_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="timeWindowsInput")
    def time_windows_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "timeWindowsInput"))

    @builtins.property
    @jsii.member(jsii_name="isEnabled")
    def is_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isEnabled"))

    @is_enabled.setter
    def is_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbe117480707862ebd505639ed8d82ae9744065320b96e68870882b86dd58c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="timeWindows")
    def time_windows(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "timeWindows"))

    @time_windows.setter
    def time_windows(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1989117ce19416a2c34b64619e9eed1082a3c3788410b48d8909672540868a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeWindows", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OceanAksNpSchedulingShutdownHours]:
        return typing.cast(typing.Optional[OceanAksNpSchedulingShutdownHours], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OceanAksNpSchedulingShutdownHours],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e4b92d6508fea86858f2a4cfdc5363c175f45496e7ee7f02dd5a3e7789fae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpTaints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class OceanAksNpTaints:
    def __init__(
        self,
        *,
        effect: builtins.str,
        key: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param effect: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#effect OceanAksNp#effect}.
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#key OceanAksNp#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#value OceanAksNp#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6405863ddb06d92e42ec8b68ae430bf71f9a78bd1de8330ebbcddc3ca14513e0)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "effect": effect,
            "key": key,
            "value": value,
        }

    @builtins.property
    def effect(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#effect OceanAksNp#effect}.'''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#key OceanAksNp#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/spotinst/spotinst/1.144.0/docs/resources/ocean_aks_np#value OceanAksNp#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OceanAksNpTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OceanAksNpTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bccda8cff8cd35b59025ec8505ae5fef9bfa67836a9cd38cf0f2f53a737987d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OceanAksNpTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95f7d63d51367ba18f9f7d56ba2e32e41750219476e19d2ed683779fc4256a1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OceanAksNpTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75766fdebefc353d55778a076ee6e4f138f125e5f72271728bf2434a85cad83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__632b24880a1a359914183f1c3a99b8b8707d6466d37f1084522e41e32743e5e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd76d67d3386fe6c4659ed18f908692fc1a8437689f5a219ff90eb46ecc201d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNpTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNpTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNpTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c763e184885cbbe077123246e2b44527a3a7ea4fe0301a3cdfa6785f665af98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OceanAksNpTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.oceanAksNp.OceanAksNpTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34ba3872921f82627c72bff53a3eece25ceeb53d9cb5bf35255f53df547da01b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="effectInput")
    def effect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdae04ccbf75d107ac77c7b8c396f84d8867842e85ac8217f6093f7bdcbdbbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aadbec3dcbf826a8c26fa439ed539ef2f4cfe6b707a11d13a6c34bd18530b53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__269fb8f3eac05193692e73d537ce2f5cab783d3e2acf3abfbe8214f97e39f5ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OceanAksNpTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OceanAksNpTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OceanAksNpTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c1159b06026c1f8e7afbe40fa9df934025ce9377970e157eaa9cf002e9c6fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "OceanAksNp",
    "OceanAksNpAutoscaler",
    "OceanAksNpAutoscalerAutoscaleDown",
    "OceanAksNpAutoscalerAutoscaleDownOutputReference",
    "OceanAksNpAutoscalerAutoscaleHeadroom",
    "OceanAksNpAutoscalerAutoscaleHeadroomAutomatic",
    "OceanAksNpAutoscalerAutoscaleHeadroomAutomaticOutputReference",
    "OceanAksNpAutoscalerAutoscaleHeadroomOutputReference",
    "OceanAksNpAutoscalerOutputReference",
    "OceanAksNpAutoscalerResourceLimits",
    "OceanAksNpAutoscalerResourceLimitsOutputReference",
    "OceanAksNpConfig",
    "OceanAksNpFilters",
    "OceanAksNpFiltersOutputReference",
    "OceanAksNpHeadrooms",
    "OceanAksNpHeadroomsList",
    "OceanAksNpHeadroomsOutputReference",
    "OceanAksNpHealth",
    "OceanAksNpHealthOutputReference",
    "OceanAksNpScheduling",
    "OceanAksNpSchedulingOutputReference",
    "OceanAksNpSchedulingShutdownHours",
    "OceanAksNpSchedulingShutdownHoursOutputReference",
    "OceanAksNpTaints",
    "OceanAksNpTaintsList",
    "OceanAksNpTaintsOutputReference",
]

publication.publish()

def _typecheckingstub__898ccbb93cd7b1a458d7f489d68c3366490a1abc47b94a9d60566b0529018fed(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    aks_cluster_name: builtins.str,
    aks_infrastructure_resource_group_name: builtins.str,
    aks_region: builtins.str,
    aks_resource_group_name: builtins.str,
    availability_zones: typing.Sequence[builtins.str],
    name: builtins.str,
    autoscaler: typing.Optional[typing.Union[OceanAksNpAutoscaler, typing.Dict[builtins.str, typing.Any]]] = None,
    controller_cluster_id: typing.Optional[builtins.str] = None,
    enable_node_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fallback_to_ondemand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filters: typing.Optional[typing.Union[OceanAksNpFilters, typing.Dict[builtins.str, typing.Any]]] = None,
    headrooms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksNpHeadrooms, typing.Dict[builtins.str, typing.Any]]]]] = None,
    health: typing.Optional[typing.Union[OceanAksNpHealth, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kubernetes_version: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_count: typing.Optional[jsii.Number] = None,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
    min_count: typing.Optional[jsii.Number] = None,
    os_disk_size_gb: typing.Optional[jsii.Number] = None,
    os_disk_type: typing.Optional[builtins.str] = None,
    os_sku: typing.Optional[builtins.str] = None,
    os_type: typing.Optional[builtins.str] = None,
    scheduling: typing.Optional[typing.Union[OceanAksNpScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    spot_percentage: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksNpTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__284c374fcc23f7877c2e31bfa73cdbeb548c9a186476cd657442a94547da0842(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksNpHeadrooms, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fcc7c22e4bac75dfaf5872709d568cac573e3dd5764f65ad904b1247fd2db3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksNpTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a5844e745d3dc3bc50168b6d11d932a24790b381febdd79aa3acdba95594ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea69ad8644dd89aa463fc85d07e524019a06a1cc120da1e5987046a167466f62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ec4fefd2f1d7c22a01397d06dae7fd932b7d24c5aed9becabb675f4a845d80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6179ec6fb80c523d3bbccb2b6580f1f29112d47edae838bd46f35883dbc7999(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277c847b46190413d77cdd0ec9934c355c98b40f731ac2beba195207710617de(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37accc031cfce63d2dede6fb5e99addd1ffafe921af10c1d3bded64a9f38de0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44df0c8a8822bc1dcd738c59f5a3909445fb3aec5820edabc5722192d5a098ae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7b35b0a5c743235e1ae0ff043dc3e570e58168eb4e23805c4af0d49d26b1e0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d260296295b25370fc455d1d4c9a607901c5cf42dacfb779bcb1e0557886d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f205fc97059e2e675db7cd66935260bb789b418a7ef2c5000f834971da7bade1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3021f2aa21020ec377f6d47e7e39dca0e27337a2fb5afa335f86be5f073cb6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47778ca946ad4ccfe14cfe5ae2a85cfc6c161788aed5f8697d1e4718505439ca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88419e6c825defaa4ac92fe1c20480259588dc45277611521e2a183eae035a71(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87ed622c0b11d0f2b346ba0ec6761aba7c644142354bfcc76466be4f28f1469(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b336cc34e01b20430edee7becd47c00b9fd1e4f8dce0b2d9d4f5944aee8b153(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5297b4865bb4041d494b256e9a6a1ca46517024b5172258ef6a2adce38ce5bc6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e34a9a6875fb6e0b20bd147f857ece0bffef93a279e097c559567a1dddef51d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338e5f41b3606d67e98979a8864305bbbe7e85e06153bc623a1c7529c0c3fea9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a405be31d799aaa7a83bbb92dabe9622e3cfbc1cbfe473d34a12036422aa9abb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a17ecd73e9618bd166376ebe256e68840e49d45a403e6fcbabf779f0417e2a1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f840978c379636cb42b7cfb9b618103389df7c9747536fdc06b6cede3362a1c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd5b84fed7b90a6e8df57726b3376ad4897744a5f1d3df74f1742a1eba4d2eb(
    *,
    autoscale_down: typing.Optional[typing.Union[OceanAksNpAutoscalerAutoscaleDown, typing.Dict[builtins.str, typing.Any]]] = None,
    autoscale_headroom: typing.Optional[typing.Union[OceanAksNpAutoscalerAutoscaleHeadroom, typing.Dict[builtins.str, typing.Any]]] = None,
    autoscale_is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource_limits: typing.Optional[typing.Union[OceanAksNpAutoscalerResourceLimits, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90025a750dab1d36f316beb5c4d4bc277fb2fece46d0c095beee1b058f490a97(
    *,
    max_scale_down_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e323dc3d55845c8138edb6fa0ed07b64348d49458e8d173ad68cf23277bd56f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e211cc7941a4f9d530dab9597943bd8cc3102383b1020c7ea5938be4144edea9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694925ba377ee2297c478fa7de17a6028ae390c9b028bdb0ef21a8bbaf61cb13(
    value: typing.Optional[OceanAksNpAutoscalerAutoscaleDown],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f3500b9c60d85bcf43c8bfb06f8a67e246dfe5c2c75f4a0cf43faa35e91db9d(
    *,
    automatic: typing.Optional[typing.Union[OceanAksNpAutoscalerAutoscaleHeadroomAutomatic, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a6682d5e28cfd7d5d2788a7f90a30240c46435e6bd6e853722b0c11de95fa6(
    *,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b7cb40a358c82222c6e38ba5aa9b9f55f00ba74337ecd6896e5d1a62874cc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9164955a5ae0aada1ca6cee1a1ee85d69ad7c4686e4005350b5be4899038b9d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59fbba227f6bd247ed11b119bc5e54ce48f5b9c7aec7d0646366479d2f94fc2e(
    value: typing.Optional[OceanAksNpAutoscalerAutoscaleHeadroomAutomatic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0919e878c242a679f4ee67c299f7c4bb7af254bbad557c02a1273830852f338(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c244f9824c5e7cb48ea4637399431e5bc70474602ca5922ee474962451c71e(
    value: typing.Optional[OceanAksNpAutoscalerAutoscaleHeadroom],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7b3548c7c7a2d7cf9ed3738e3162adc17b8b3086567472ad6ad6854c948256(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da55f0718b621653af224776827ca6681da47a8b7520c55d829dfaf411c63382(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1648c48e96a0709637e03dddcca11e4292b34ea0ae7e40867a72cc2e85b66e8(
    value: typing.Optional[OceanAksNpAutoscaler],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5a0c123b4007faf87d6c403994a74c1db5f68aedd37c6754116ad94e1164fd(
    *,
    max_memory_gib: typing.Optional[jsii.Number] = None,
    max_vcpu: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71cbffbd897e11688fd174fd8ed556b1888ea72e313351b955cab1461248eec7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14ca6f83844bc92b5506d7a61488a3b988fb9b002111e37c86faf65b58dec24(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b89ad8c1aa30471337199f6611e44ca026982358d6a0c5d6a9cb325ce4469b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bda71648bd77cd9febd4bf4fe53060c188279f266968f16f74a65d6b6e348bb(
    value: typing.Optional[OceanAksNpAutoscalerResourceLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bab4f3e98d3b0cba441a02e1e4220b0e83e9de8e80d93eb0348c9802bbac4b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    aks_cluster_name: builtins.str,
    aks_infrastructure_resource_group_name: builtins.str,
    aks_region: builtins.str,
    aks_resource_group_name: builtins.str,
    availability_zones: typing.Sequence[builtins.str],
    name: builtins.str,
    autoscaler: typing.Optional[typing.Union[OceanAksNpAutoscaler, typing.Dict[builtins.str, typing.Any]]] = None,
    controller_cluster_id: typing.Optional[builtins.str] = None,
    enable_node_public_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    fallback_to_ondemand: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filters: typing.Optional[typing.Union[OceanAksNpFilters, typing.Dict[builtins.str, typing.Any]]] = None,
    headrooms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksNpHeadrooms, typing.Dict[builtins.str, typing.Any]]]]] = None,
    health: typing.Optional[typing.Union[OceanAksNpHealth, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kubernetes_version: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_count: typing.Optional[jsii.Number] = None,
    max_pods_per_node: typing.Optional[jsii.Number] = None,
    min_count: typing.Optional[jsii.Number] = None,
    os_disk_size_gb: typing.Optional[jsii.Number] = None,
    os_disk_type: typing.Optional[builtins.str] = None,
    os_sku: typing.Optional[builtins.str] = None,
    os_type: typing.Optional[builtins.str] = None,
    scheduling: typing.Optional[typing.Union[OceanAksNpScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    spot_percentage: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OceanAksNpTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a9f7ac92271595654997c1c567d2192601f5aa35699adec679624356c181ab(
    *,
    architectures: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_series: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_memory_gib: typing.Optional[jsii.Number] = None,
    max_vcpu: typing.Optional[jsii.Number] = None,
    min_memory_gib: typing.Optional[jsii.Number] = None,
    min_vcpu: typing.Optional[jsii.Number] = None,
    series: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3d5c6b23f914408dcab4cd492a9e2c57a0dfc473c15cc81e6fed9569e4a885(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c742c1c4d9379baf6663ee29e90347b76841893ec7c21d5f0c078681e63b322(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c859c25dae8d7f829f8a4c7a10d8f95ea10064ef8ec38c26a9b7ec99c89146(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7e75e2b21793f5c4a71c261dcd0e2f3c8c247bb5e8055027755fd8929fec3c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c124113da710685d1046267a1bef2d22b3f6c4960033e838db3f969d0c94544(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7006276093120f973474fc0cd23738284fa202900d8a7f7cdff0cf99fc52cbb6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f9842d5ec88efa702799bf7305f81cdd9657e6343aeefea4a229a40d027493(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fa2a5a1c3686a833a5af9341349061e311b0645695207344c40eb87ab3e64e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31bd0fc5a502010cec257c33953fdf09d6f9013fd19fca25907e25d7b91be82(
    value: typing.Optional[OceanAksNpFilters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f8750b24926f1ba765bf3f4bae5f9a952c815a93d08ba5ab409373a843371b(
    *,
    cpu_per_unit: typing.Optional[jsii.Number] = None,
    gpu_per_unit: typing.Optional[jsii.Number] = None,
    memory_per_unit: typing.Optional[jsii.Number] = None,
    num_of_units: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c950d5f3f70655493d9d9c052fe216c9f66fcc7e611665d994f76175adb2fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddd81aaf8bb9776ce0913f2849cc0a6d8850205e7945e73eb68e7cd06190a2e3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974e4e6b976d69c90b5f86b11bfe4d68b5d80dc9e4861f115816562c61596d8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8066f1a1deb87058e4059c1959e90872007b95885d9438a3f8ce29bd6f4915f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deaf9d4b8b9ae52192fc3601c0951f8914b64eb56931429524cd80ff38e28ef0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930213753fd0fffc740533f09448e92002d97f00bf6f641ec3f39a8a3806a535(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNpHeadrooms]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ff8aa121081ccb41ad6c5fc8d3ea6631df992c898121214ebf3e687e08f17d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32475492fd397e67799604b757dd5b65aaac594140765ddbe0d8fb11ed5bcbe8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14959e319a974453ba22c4bc44072e335bd6d76e7eeb1dd1119a6378f4e4c1be(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4aa00243509d7b4f1b0dd8329bd3517aae69bcdb204a1c47df019bff2c3b6f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856e5ad14de0acec5e7d139d2a8b96fc92c5ae52d209d7c616ede8873891bf0c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0561065072d4a65c55dd2068d56986da11a509b67366f7fa28ac74525134cfd8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OceanAksNpHeadrooms]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0446171353b1dda6da14d9676f214aa866da2a98185290415005f5b979db2eb7(
    *,
    grace_period: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7aedccee9ce43e6ed6a3722e435b998ea72bcfb5ec8f247f3156ec79e8f40a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913de7f1851a455383aaeebdae3597173c9cceb7381a5d37852b0b1bad8f04a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf340db4cbe5a708e17e8e299156919e448f4418f16a733c27fa1313b55df2b(
    value: typing.Optional[OceanAksNpHealth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d20ebe1bf5190dc49c807ca036b51189ee29c47672aba96614a263fd410910(
    *,
    shutdown_hours: typing.Optional[typing.Union[OceanAksNpSchedulingShutdownHours, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b23839593ae1052707b8b8b15a603e7cd9124c4d6717d97ec9d541fdaccdff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42efce885b277ff0467b937bbf380f852367148461159c02ec153066704117d8(
    value: typing.Optional[OceanAksNpScheduling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45995a95327fe7c1d819054ab0a424f8ca422d0b9989cab007cac55904f55d20(
    *,
    time_windows: typing.Sequence[builtins.str],
    is_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da2f3033c6c0996a552559a0b6b2dc185633de63eb50d3ab1530eca4263504b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbe117480707862ebd505639ed8d82ae9744065320b96e68870882b86dd58c9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1989117ce19416a2c34b64619e9eed1082a3c3788410b48d8909672540868a7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e4b92d6508fea86858f2a4cfdc5363c175f45496e7ee7f02dd5a3e7789fae5(
    value: typing.Optional[OceanAksNpSchedulingShutdownHours],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6405863ddb06d92e42ec8b68ae430bf71f9a78bd1de8330ebbcddc3ca14513e0(
    *,
    effect: builtins.str,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bccda8cff8cd35b59025ec8505ae5fef9bfa67836a9cd38cf0f2f53a737987d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95f7d63d51367ba18f9f7d56ba2e32e41750219476e19d2ed683779fc4256a1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75766fdebefc353d55778a076ee6e4f138f125e5f72271728bf2434a85cad83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632b24880a1a359914183f1c3a99b8b8707d6466d37f1084522e41e32743e5e0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd76d67d3386fe6c4659ed18f908692fc1a8437689f5a219ff90eb46ecc201d7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c763e184885cbbe077123246e2b44527a3a7ea4fe0301a3cdfa6785f665af98(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OceanAksNpTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ba3872921f82627c72bff53a3eece25ceeb53d9cb5bf35255f53df547da01b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdae04ccbf75d107ac77c7b8c396f84d8867842e85ac8217f6093f7bdcbdbbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aadbec3dcbf826a8c26fa439ed539ef2f4cfe6b707a11d13a6c34bd18530b53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__269fb8f3eac05193692e73d537ce2f5cab783d3e2acf3abfbe8214f97e39f5ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c1159b06026c1f8e7afbe40fa9df934025ce9377970e157eaa9cf002e9c6fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OceanAksNpTaints]],
) -> None:
    """Type checking stubs"""
    pass
