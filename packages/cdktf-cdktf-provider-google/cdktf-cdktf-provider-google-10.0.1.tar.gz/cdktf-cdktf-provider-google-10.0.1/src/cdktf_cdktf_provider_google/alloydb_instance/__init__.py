'''
# `google_alloydb_instance`

Refer to the Terraform Registory for docs: [`google_alloydb_instance`](https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance).
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


class AlloydbInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance google_alloydb_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster: builtins.str,
        instance_id: builtins.str,
        instance_type: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        availability_type: typing.Optional[builtins.str] = None,
        database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        gce_zone: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        machine_config: typing.Optional[typing.Union["AlloydbInstanceMachineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        query_insights_config: typing.Optional[typing.Union["AlloydbInstanceQueryInsightsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        read_pool_config: typing.Optional[typing.Union["AlloydbInstanceReadPoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AlloydbInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance google_alloydb_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster: Identifies the alloydb cluster. Must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#cluster AlloydbInstance#cluster}
        :param instance_id: The ID of the alloydb instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#instance_id AlloydbInstance#instance_id}
        :param instance_type: The type of the instance. If the instance type is READ_POOL, provide the associated PRIMARY instance in the 'depends_on' meta-data attribute. Possible values: ["PRIMARY", "READ_POOL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#instance_type AlloydbInstance#instance_type}
        :param annotations: Annotations to allow client tools to store small amount of arbitrary data. This is distinct from labels. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#annotations AlloydbInstance#annotations}
        :param availability_type: 'Availability type of an Instance. Defaults to REGIONAL for both primary and read instances. Note that primary and read instances can have different availability types. Only READ_POOL instance supports ZONAL type. Users can't specify the zone for READ_POOL instance. Zone is automatically chosen from the list of zones in the region specified. Read pool of size 1 can only have zonal availability. Read pools with node count of 2 or more can have regional availability (nodes are present in 2 or more zones in a region).' Possible values: ["AVAILABILITY_TYPE_UNSPECIFIED", "ZONAL", "REGIONAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#availability_type AlloydbInstance#availability_type}
        :param database_flags: Database flags. Set at instance level. * They are copied from primary instance on read instance creation. * Read instances can set new or override existing flags that are relevant for reads, e.g. for enabling columnar cache on a read instance. Flags set on read instance may or may not be present on primary. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#database_flags AlloydbInstance#database_flags}
        :param display_name: User-settable and human-readable display name for the Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#display_name AlloydbInstance#display_name}
        :param gce_zone: The Compute Engine zone that the instance should serve from, per https://cloud.google.com/compute/docs/regions-zones This can ONLY be specified for ZONAL instances. If present for a REGIONAL instance, an error will be thrown. If this is absent for a ZONAL instance, instance is created in a random zone with available capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#gce_zone AlloydbInstance#gce_zone}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#id AlloydbInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the alloydb instance. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#labels AlloydbInstance#labels}
        :param machine_config: machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#machine_config AlloydbInstance#machine_config}
        :param query_insights_config: query_insights_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#query_insights_config AlloydbInstance#query_insights_config}
        :param read_pool_config: read_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#read_pool_config AlloydbInstance#read_pool_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#timeouts AlloydbInstance#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f765b873890bbf96433922dc1fea912d0f8d2ec8f3688afc26caab7e8fd9c0aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AlloydbInstanceConfig(
            cluster=cluster,
            instance_id=instance_id,
            instance_type=instance_type,
            annotations=annotations,
            availability_type=availability_type,
            database_flags=database_flags,
            display_name=display_name,
            gce_zone=gce_zone,
            id=id,
            labels=labels,
            machine_config=machine_config,
            query_insights_config=query_insights_config,
            read_pool_config=read_pool_config,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putMachineConfig")
    def put_machine_config(
        self,
        *,
        cpu_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cpu_count: The number of CPU's in the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#cpu_count AlloydbInstance#cpu_count}
        '''
        value = AlloydbInstanceMachineConfig(cpu_count=cpu_count)

        return typing.cast(None, jsii.invoke(self, "putMachineConfig", [value]))

    @jsii.member(jsii_name="putQueryInsightsConfig")
    def put_query_insights_config(
        self,
        *,
        query_plans_per_minute: typing.Optional[jsii.Number] = None,
        query_string_length: typing.Optional[jsii.Number] = None,
        record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        record_client_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param query_plans_per_minute: Number of query execution plans captured by Insights per minute for all queries combined. The default value is 5. Any integer between 0 and 20 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#query_plans_per_minute AlloydbInstance#query_plans_per_minute}
        :param query_string_length: Query string length. The default value is 1024. Any integer between 256 and 4500 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#query_string_length AlloydbInstance#query_string_length}
        :param record_application_tags: Record application tags for an instance. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#record_application_tags AlloydbInstance#record_application_tags}
        :param record_client_address: Record client address for an instance. Client address is PII information. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#record_client_address AlloydbInstance#record_client_address}
        '''
        value = AlloydbInstanceQueryInsightsConfig(
            query_plans_per_minute=query_plans_per_minute,
            query_string_length=query_string_length,
            record_application_tags=record_application_tags,
            record_client_address=record_client_address,
        )

        return typing.cast(None, jsii.invoke(self, "putQueryInsightsConfig", [value]))

    @jsii.member(jsii_name="putReadPoolConfig")
    def put_read_pool_config(
        self,
        *,
        node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param node_count: Read capacity, i.e. number of nodes in a read pool instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#node_count AlloydbInstance#node_count}
        '''
        value = AlloydbInstanceReadPoolConfig(node_count=node_count)

        return typing.cast(None, jsii.invoke(self, "putReadPoolConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#create AlloydbInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#delete AlloydbInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#update AlloydbInstance#update}.
        '''
        value = AlloydbInstanceTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetAvailabilityType")
    def reset_availability_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityType", []))

    @jsii.member(jsii_name="resetDatabaseFlags")
    def reset_database_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabaseFlags", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetGceZone")
    def reset_gce_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGceZone", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMachineConfig")
    def reset_machine_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineConfig", []))

    @jsii.member(jsii_name="resetQueryInsightsConfig")
    def reset_query_insights_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryInsightsConfig", []))

    @jsii.member(jsii_name="resetReadPoolConfig")
    def reset_read_pool_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadPoolConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="machineConfig")
    def machine_config(self) -> "AlloydbInstanceMachineConfigOutputReference":
        return typing.cast("AlloydbInstanceMachineConfigOutputReference", jsii.get(self, "machineConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="queryInsightsConfig")
    def query_insights_config(
        self,
    ) -> "AlloydbInstanceQueryInsightsConfigOutputReference":
        return typing.cast("AlloydbInstanceQueryInsightsConfigOutputReference", jsii.get(self, "queryInsightsConfig"))

    @builtins.property
    @jsii.member(jsii_name="readPoolConfig")
    def read_pool_config(self) -> "AlloydbInstanceReadPoolConfigOutputReference":
        return typing.cast("AlloydbInstanceReadPoolConfigOutputReference", jsii.get(self, "readPoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AlloydbInstanceTimeoutsOutputReference":
        return typing.cast("AlloydbInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityTypeInput")
    def availability_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterInput")
    def cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseFlagsInput")
    def database_flags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "databaseFlagsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gceZoneInput")
    def gce_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gceZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceIdInput")
    def instance_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="machineConfigInput")
    def machine_config_input(self) -> typing.Optional["AlloydbInstanceMachineConfig"]:
        return typing.cast(typing.Optional["AlloydbInstanceMachineConfig"], jsii.get(self, "machineConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInsightsConfigInput")
    def query_insights_config_input(
        self,
    ) -> typing.Optional["AlloydbInstanceQueryInsightsConfig"]:
        return typing.cast(typing.Optional["AlloydbInstanceQueryInsightsConfig"], jsii.get(self, "queryInsightsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="readPoolConfigInput")
    def read_pool_config_input(
        self,
    ) -> typing.Optional["AlloydbInstanceReadPoolConfig"]:
        return typing.cast(typing.Optional["AlloydbInstanceReadPoolConfig"], jsii.get(self, "readPoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AlloydbInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AlloydbInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa1cb9979915aca6a7c4aeb57518b12a5796b6145a5a64a20ba7fde6e597550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityType")
    def availability_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityType"))

    @availability_type.setter
    def availability_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158158519d9a8a65f38719221803f22b0703d7bf76e9846762986111669a41d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityType", value)

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cluster"))

    @cluster.setter
    def cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4285c5b746dd6b49221842687902a1fd16d86c5f3323aa1f9e75c04444ffc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cluster", value)

    @builtins.property
    @jsii.member(jsii_name="databaseFlags")
    def database_flags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "databaseFlags"))

    @database_flags.setter
    def database_flags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69172a3afd4ec3ebb8d1e95baa8c35287c8e0a2d8aff61d978256916dbb9e08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseFlags", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f69c08f4e371a59795390d38974db812ca5132568dcf7976bed28c0b7761d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="gceZone")
    def gce_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gceZone"))

    @gce_zone.setter
    def gce_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__024692bb7172b732c32dabc7eac5e3e61c8080298ee96e5e59153d60827c2031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gceZone", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69feb04cc37565f93b1e2458d4a895c9f64325b499b629c6f52332caa6d88db0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433ab37fe37b6a6f75557ec95ffd95c27cf82fd7cb300c5d18713c16ee888395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value)

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0213d387b77d2f90108f9dfee31e87e4c0440368736dbabfbad6df49074010a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5277e02c8c1938057186ca3fe735c81944512c81f6a0d17e69f4c9a464d2fceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster": "cluster",
        "instance_id": "instanceId",
        "instance_type": "instanceType",
        "annotations": "annotations",
        "availability_type": "availabilityType",
        "database_flags": "databaseFlags",
        "display_name": "displayName",
        "gce_zone": "gceZone",
        "id": "id",
        "labels": "labels",
        "machine_config": "machineConfig",
        "query_insights_config": "queryInsightsConfig",
        "read_pool_config": "readPoolConfig",
        "timeouts": "timeouts",
    },
)
class AlloydbInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster: builtins.str,
        instance_id: builtins.str,
        instance_type: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        availability_type: typing.Optional[builtins.str] = None,
        database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        gce_zone: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        machine_config: typing.Optional[typing.Union["AlloydbInstanceMachineConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        query_insights_config: typing.Optional[typing.Union["AlloydbInstanceQueryInsightsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        read_pool_config: typing.Optional[typing.Union["AlloydbInstanceReadPoolConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["AlloydbInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster: Identifies the alloydb cluster. Must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#cluster AlloydbInstance#cluster}
        :param instance_id: The ID of the alloydb instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#instance_id AlloydbInstance#instance_id}
        :param instance_type: The type of the instance. If the instance type is READ_POOL, provide the associated PRIMARY instance in the 'depends_on' meta-data attribute. Possible values: ["PRIMARY", "READ_POOL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#instance_type AlloydbInstance#instance_type}
        :param annotations: Annotations to allow client tools to store small amount of arbitrary data. This is distinct from labels. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#annotations AlloydbInstance#annotations}
        :param availability_type: 'Availability type of an Instance. Defaults to REGIONAL for both primary and read instances. Note that primary and read instances can have different availability types. Only READ_POOL instance supports ZONAL type. Users can't specify the zone for READ_POOL instance. Zone is automatically chosen from the list of zones in the region specified. Read pool of size 1 can only have zonal availability. Read pools with node count of 2 or more can have regional availability (nodes are present in 2 or more zones in a region).' Possible values: ["AVAILABILITY_TYPE_UNSPECIFIED", "ZONAL", "REGIONAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#availability_type AlloydbInstance#availability_type}
        :param database_flags: Database flags. Set at instance level. * They are copied from primary instance on read instance creation. * Read instances can set new or override existing flags that are relevant for reads, e.g. for enabling columnar cache on a read instance. Flags set on read instance may or may not be present on primary. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#database_flags AlloydbInstance#database_flags}
        :param display_name: User-settable and human-readable display name for the Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#display_name AlloydbInstance#display_name}
        :param gce_zone: The Compute Engine zone that the instance should serve from, per https://cloud.google.com/compute/docs/regions-zones This can ONLY be specified for ZONAL instances. If present for a REGIONAL instance, an error will be thrown. If this is absent for a ZONAL instance, instance is created in a random zone with available capacity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#gce_zone AlloydbInstance#gce_zone}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#id AlloydbInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the alloydb instance. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#labels AlloydbInstance#labels}
        :param machine_config: machine_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#machine_config AlloydbInstance#machine_config}
        :param query_insights_config: query_insights_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#query_insights_config AlloydbInstance#query_insights_config}
        :param read_pool_config: read_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#read_pool_config AlloydbInstance#read_pool_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#timeouts AlloydbInstance#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(machine_config, dict):
            machine_config = AlloydbInstanceMachineConfig(**machine_config)
        if isinstance(query_insights_config, dict):
            query_insights_config = AlloydbInstanceQueryInsightsConfig(**query_insights_config)
        if isinstance(read_pool_config, dict):
            read_pool_config = AlloydbInstanceReadPoolConfig(**read_pool_config)
        if isinstance(timeouts, dict):
            timeouts = AlloydbInstanceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1513728bf9a692ea14e578c6e8e3ebe350a5703568d9faa6685c56af4afcaf1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument availability_type", value=availability_type, expected_type=type_hints["availability_type"])
            check_type(argname="argument database_flags", value=database_flags, expected_type=type_hints["database_flags"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gce_zone", value=gce_zone, expected_type=type_hints["gce_zone"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument machine_config", value=machine_config, expected_type=type_hints["machine_config"])
            check_type(argname="argument query_insights_config", value=query_insights_config, expected_type=type_hints["query_insights_config"])
            check_type(argname="argument read_pool_config", value=read_pool_config, expected_type=type_hints["read_pool_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
            "instance_id": instance_id,
            "instance_type": instance_type,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if availability_type is not None:
            self._values["availability_type"] = availability_type
        if database_flags is not None:
            self._values["database_flags"] = database_flags
        if display_name is not None:
            self._values["display_name"] = display_name
        if gce_zone is not None:
            self._values["gce_zone"] = gce_zone
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if machine_config is not None:
            self._values["machine_config"] = machine_config
        if query_insights_config is not None:
            self._values["query_insights_config"] = query_insights_config
        if read_pool_config is not None:
            self._values["read_pool_config"] = read_pool_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def cluster(self) -> builtins.str:
        '''Identifies the alloydb cluster. Must be in the format 'projects/{project}/locations/{location}/clusters/{cluster_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#cluster AlloydbInstance#cluster}
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''The ID of the alloydb instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#instance_id AlloydbInstance#instance_id}
        '''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''The type of the instance.

        If the instance type is READ_POOL, provide the associated PRIMARY instance in the 'depends_on' meta-data attribute. Possible values: ["PRIMARY", "READ_POOL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#instance_type AlloydbInstance#instance_type}
        '''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations to allow client tools to store small amount of arbitrary data. This is distinct from labels.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#annotations AlloydbInstance#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def availability_type(self) -> typing.Optional[builtins.str]:
        ''''Availability type of an Instance.

        Defaults to REGIONAL for both primary and read instances.
        Note that primary and read instances can have different availability types.
        Only READ_POOL instance supports ZONAL type. Users can't specify the zone for READ_POOL instance.
        Zone is automatically chosen from the list of zones in the region specified.
        Read pool of size 1 can only have zonal availability. Read pools with node count of 2 or more
        can have regional availability (nodes are present in 2 or more zones in a region).' Possible values: ["AVAILABILITY_TYPE_UNSPECIFIED", "ZONAL", "REGIONAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#availability_type AlloydbInstance#availability_type}
        '''
        result = self._values.get("availability_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database_flags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Database flags.

        Set at instance level. * They are copied from primary instance on read instance creation. * Read instances can set new or override existing flags that are relevant for reads, e.g. for enabling columnar cache on a read instance. Flags set on read instance may or may not be present on primary.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#database_flags AlloydbInstance#database_flags}
        '''
        result = self._values.get("database_flags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User-settable and human-readable display name for the Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#display_name AlloydbInstance#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gce_zone(self) -> typing.Optional[builtins.str]:
        '''The Compute Engine zone that the instance should serve from, per https://cloud.google.com/compute/docs/regions-zones This can ONLY be specified for ZONAL instances. If present for a REGIONAL instance, an error will be thrown. If this is absent for a ZONAL instance, instance is created in a random zone with available capacity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#gce_zone AlloydbInstance#gce_zone}
        '''
        result = self._values.get("gce_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#id AlloydbInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels for the alloydb instance.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#labels AlloydbInstance#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def machine_config(self) -> typing.Optional["AlloydbInstanceMachineConfig"]:
        '''machine_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#machine_config AlloydbInstance#machine_config}
        '''
        result = self._values.get("machine_config")
        return typing.cast(typing.Optional["AlloydbInstanceMachineConfig"], result)

    @builtins.property
    def query_insights_config(
        self,
    ) -> typing.Optional["AlloydbInstanceQueryInsightsConfig"]:
        '''query_insights_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#query_insights_config AlloydbInstance#query_insights_config}
        '''
        result = self._values.get("query_insights_config")
        return typing.cast(typing.Optional["AlloydbInstanceQueryInsightsConfig"], result)

    @builtins.property
    def read_pool_config(self) -> typing.Optional["AlloydbInstanceReadPoolConfig"]:
        '''read_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#read_pool_config AlloydbInstance#read_pool_config}
        '''
        result = self._values.get("read_pool_config")
        return typing.cast(typing.Optional["AlloydbInstanceReadPoolConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AlloydbInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#timeouts AlloydbInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AlloydbInstanceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceMachineConfig",
    jsii_struct_bases=[],
    name_mapping={"cpu_count": "cpuCount"},
)
class AlloydbInstanceMachineConfig:
    def __init__(self, *, cpu_count: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param cpu_count: The number of CPU's in the VM instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#cpu_count AlloydbInstance#cpu_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae1c69322f6ed0426aaab238f3d6fe1f33698bd608cd1b6534450a776dc51bff)
            check_type(argname="argument cpu_count", value=cpu_count, expected_type=type_hints["cpu_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_count is not None:
            self._values["cpu_count"] = cpu_count

    @builtins.property
    def cpu_count(self) -> typing.Optional[jsii.Number]:
        '''The number of CPU's in the VM instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#cpu_count AlloydbInstance#cpu_count}
        '''
        result = self._values.get("cpu_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceMachineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstanceMachineConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceMachineConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6339a3d89e0aecd8dda776b93a80b321f950a484556e4d01594e51837d60162)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpuCount")
    def reset_cpu_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuCount", []))

    @builtins.property
    @jsii.member(jsii_name="cpuCountInput")
    def cpu_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuCountInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuCount")
    def cpu_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuCount"))

    @cpu_count.setter
    def cpu_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73e48c2e41ed071faf47c52884932f4bb7b8df932fdcf4e7395f28e4feb33db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuCount", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbInstanceMachineConfig]:
        return typing.cast(typing.Optional[AlloydbInstanceMachineConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbInstanceMachineConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49f69a9f7a02d3d4fc15faefa62a4fbe7a3cf1ccf6ce27dfa4ef3830ee6608d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceQueryInsightsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "query_plans_per_minute": "queryPlansPerMinute",
        "query_string_length": "queryStringLength",
        "record_application_tags": "recordApplicationTags",
        "record_client_address": "recordClientAddress",
    },
)
class AlloydbInstanceQueryInsightsConfig:
    def __init__(
        self,
        *,
        query_plans_per_minute: typing.Optional[jsii.Number] = None,
        query_string_length: typing.Optional[jsii.Number] = None,
        record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        record_client_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param query_plans_per_minute: Number of query execution plans captured by Insights per minute for all queries combined. The default value is 5. Any integer between 0 and 20 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#query_plans_per_minute AlloydbInstance#query_plans_per_minute}
        :param query_string_length: Query string length. The default value is 1024. Any integer between 256 and 4500 is considered valid. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#query_string_length AlloydbInstance#query_string_length}
        :param record_application_tags: Record application tags for an instance. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#record_application_tags AlloydbInstance#record_application_tags}
        :param record_client_address: Record client address for an instance. Client address is PII information. This flag is turned "on" by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#record_client_address AlloydbInstance#record_client_address}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d686258b4296fd9a11b228dfe1b794eee03b038e7d0d9e8375e0acd583b5e1f)
            check_type(argname="argument query_plans_per_minute", value=query_plans_per_minute, expected_type=type_hints["query_plans_per_minute"])
            check_type(argname="argument query_string_length", value=query_string_length, expected_type=type_hints["query_string_length"])
            check_type(argname="argument record_application_tags", value=record_application_tags, expected_type=type_hints["record_application_tags"])
            check_type(argname="argument record_client_address", value=record_client_address, expected_type=type_hints["record_client_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if query_plans_per_minute is not None:
            self._values["query_plans_per_minute"] = query_plans_per_minute
        if query_string_length is not None:
            self._values["query_string_length"] = query_string_length
        if record_application_tags is not None:
            self._values["record_application_tags"] = record_application_tags
        if record_client_address is not None:
            self._values["record_client_address"] = record_client_address

    @builtins.property
    def query_plans_per_minute(self) -> typing.Optional[jsii.Number]:
        '''Number of query execution plans captured by Insights per minute for all queries combined.

        The default value is 5. Any integer between 0 and 20 is considered valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#query_plans_per_minute AlloydbInstance#query_plans_per_minute}
        '''
        result = self._values.get("query_plans_per_minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def query_string_length(self) -> typing.Optional[jsii.Number]:
        '''Query string length. The default value is 1024. Any integer between 256 and 4500 is considered valid.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#query_string_length AlloydbInstance#query_string_length}
        '''
        result = self._values.get("query_string_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def record_application_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Record application tags for an instance. This flag is turned "on" by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#record_application_tags AlloydbInstance#record_application_tags}
        '''
        result = self._values.get("record_application_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def record_client_address(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Record client address for an instance. Client address is PII information. This flag is turned "on" by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#record_client_address AlloydbInstance#record_client_address}
        '''
        result = self._values.get("record_client_address")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceQueryInsightsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstanceQueryInsightsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceQueryInsightsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c3081d80b5ac08445d9e276af8b24ec751a115ced26fa32ed501647df359ed2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQueryPlansPerMinute")
    def reset_query_plans_per_minute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryPlansPerMinute", []))

    @jsii.member(jsii_name="resetQueryStringLength")
    def reset_query_string_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryStringLength", []))

    @jsii.member(jsii_name="resetRecordApplicationTags")
    def reset_record_application_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordApplicationTags", []))

    @jsii.member(jsii_name="resetRecordClientAddress")
    def reset_record_client_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecordClientAddress", []))

    @builtins.property
    @jsii.member(jsii_name="queryPlansPerMinuteInput")
    def query_plans_per_minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryPlansPerMinuteInput"))

    @builtins.property
    @jsii.member(jsii_name="queryStringLengthInput")
    def query_string_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "queryStringLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="recordApplicationTagsInput")
    def record_application_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "recordApplicationTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="recordClientAddressInput")
    def record_client_address_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "recordClientAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="queryPlansPerMinute")
    def query_plans_per_minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryPlansPerMinute"))

    @query_plans_per_minute.setter
    def query_plans_per_minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc2465597128c53ed48b45d8e804dc3c8c5f446817cf58627e74746d302c749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryPlansPerMinute", value)

    @builtins.property
    @jsii.member(jsii_name="queryStringLength")
    def query_string_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "queryStringLength"))

    @query_string_length.setter
    def query_string_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8e0d10d517a751a5e22e8db495c766b4b70570c31baf7ce30a0106c9c27809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryStringLength", value)

    @builtins.property
    @jsii.member(jsii_name="recordApplicationTags")
    def record_application_tags(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "recordApplicationTags"))

    @record_application_tags.setter
    def record_application_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8268d229a554e88fde1336ac3c2cb167b77417013e27c1c647b5f287224f1876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordApplicationTags", value)

    @builtins.property
    @jsii.member(jsii_name="recordClientAddress")
    def record_client_address(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "recordClientAddress"))

    @record_client_address.setter
    def record_client_address(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3242ac241e5195487a9a12ca8ae575c6192cbc9bc7f971c4bbed53d6bce766f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordClientAddress", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbInstanceQueryInsightsConfig]:
        return typing.cast(typing.Optional[AlloydbInstanceQueryInsightsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbInstanceQueryInsightsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca12cbb111540303c875c4559a422153cf7c73f3e6bb6201f881ba29f139069d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceReadPoolConfig",
    jsii_struct_bases=[],
    name_mapping={"node_count": "nodeCount"},
)
class AlloydbInstanceReadPoolConfig:
    def __init__(self, *, node_count: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param node_count: Read capacity, i.e. number of nodes in a read pool instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#node_count AlloydbInstance#node_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0120a17d019867a39bdd1b37caa4ef3d6a7460620cc4588de9d2820ae166113a)
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if node_count is not None:
            self._values["node_count"] = node_count

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Read capacity, i.e. number of nodes in a read pool instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#node_count AlloydbInstance#node_count}
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceReadPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstanceReadPoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceReadPoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e556805238a67471d3893e5fabd42872956bcc68346527e15a946ed38ea27f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__943318cc25fb6c6992d481fdae72284609c691c58f76ded639cbccc4eddb93fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlloydbInstanceReadPoolConfig]:
        return typing.cast(typing.Optional[AlloydbInstanceReadPoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AlloydbInstanceReadPoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6158543947f4bc9fb14030f6c3aaeba07c43666ce7eccae912e026c2bf388738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AlloydbInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#create AlloydbInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#delete AlloydbInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#update AlloydbInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92852fd79f1a1c5827f4e08118e4b8d1230621d12ab5bd3224b75cd3a0aaedcf)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#create AlloydbInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#delete AlloydbInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/alloydb_instance#update AlloydbInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlloydbInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlloydbInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.alloydbInstance.AlloydbInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af5cb81b3713f5486b0336541822b32c4dc250b959e4d0761a8ece4d1424ab7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95905f4e90d8f66e9d258da3dd09b81de67433dfda03e0b62f593f3bd3be278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9ef26d489259d7ed73010fb95d0e8fc45a13cd5be617b6a48a9313552f080a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca4553895f681f42dbf738f23a4e7a1f384184393c04956dbaee1f6706db8e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc17f01754fc0647c4f612b32f9e93a7061cac0a49fbf4f69e833d262c586c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AlloydbInstance",
    "AlloydbInstanceConfig",
    "AlloydbInstanceMachineConfig",
    "AlloydbInstanceMachineConfigOutputReference",
    "AlloydbInstanceQueryInsightsConfig",
    "AlloydbInstanceQueryInsightsConfigOutputReference",
    "AlloydbInstanceReadPoolConfig",
    "AlloydbInstanceReadPoolConfigOutputReference",
    "AlloydbInstanceTimeouts",
    "AlloydbInstanceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f765b873890bbf96433922dc1fea912d0f8d2ec8f3688afc26caab7e8fd9c0aa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster: builtins.str,
    instance_id: builtins.str,
    instance_type: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    availability_type: typing.Optional[builtins.str] = None,
    database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    gce_zone: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    machine_config: typing.Optional[typing.Union[AlloydbInstanceMachineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    query_insights_config: typing.Optional[typing.Union[AlloydbInstanceQueryInsightsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    read_pool_config: typing.Optional[typing.Union[AlloydbInstanceReadPoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AlloydbInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7fa1cb9979915aca6a7c4aeb57518b12a5796b6145a5a64a20ba7fde6e597550(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158158519d9a8a65f38719221803f22b0703d7bf76e9846762986111669a41d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4285c5b746dd6b49221842687902a1fd16d86c5f3323aa1f9e75c04444ffc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69172a3afd4ec3ebb8d1e95baa8c35287c8e0a2d8aff61d978256916dbb9e08b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f69c08f4e371a59795390d38974db812ca5132568dcf7976bed28c0b7761d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024692bb7172b732c32dabc7eac5e3e61c8080298ee96e5e59153d60827c2031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69feb04cc37565f93b1e2458d4a895c9f64325b499b629c6f52332caa6d88db0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433ab37fe37b6a6f75557ec95ffd95c27cf82fd7cb300c5d18713c16ee888395(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0213d387b77d2f90108f9dfee31e87e4c0440368736dbabfbad6df49074010a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5277e02c8c1938057186ca3fe735c81944512c81f6a0d17e69f4c9a464d2fceb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1513728bf9a692ea14e578c6e8e3ebe350a5703568d9faa6685c56af4afcaf1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster: builtins.str,
    instance_id: builtins.str,
    instance_type: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    availability_type: typing.Optional[builtins.str] = None,
    database_flags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    gce_zone: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    machine_config: typing.Optional[typing.Union[AlloydbInstanceMachineConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    query_insights_config: typing.Optional[typing.Union[AlloydbInstanceQueryInsightsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    read_pool_config: typing.Optional[typing.Union[AlloydbInstanceReadPoolConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[AlloydbInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae1c69322f6ed0426aaab238f3d6fe1f33698bd608cd1b6534450a776dc51bff(
    *,
    cpu_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6339a3d89e0aecd8dda776b93a80b321f950a484556e4d01594e51837d60162(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73e48c2e41ed071faf47c52884932f4bb7b8df932fdcf4e7395f28e4feb33db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49f69a9f7a02d3d4fc15faefa62a4fbe7a3cf1ccf6ce27dfa4ef3830ee6608d(
    value: typing.Optional[AlloydbInstanceMachineConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d686258b4296fd9a11b228dfe1b794eee03b038e7d0d9e8375e0acd583b5e1f(
    *,
    query_plans_per_minute: typing.Optional[jsii.Number] = None,
    query_string_length: typing.Optional[jsii.Number] = None,
    record_application_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    record_client_address: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3081d80b5ac08445d9e276af8b24ec751a115ced26fa32ed501647df359ed2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc2465597128c53ed48b45d8e804dc3c8c5f446817cf58627e74746d302c749(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8e0d10d517a751a5e22e8db495c766b4b70570c31baf7ce30a0106c9c27809(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8268d229a554e88fde1336ac3c2cb167b77417013e27c1c647b5f287224f1876(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3242ac241e5195487a9a12ca8ae575c6192cbc9bc7f971c4bbed53d6bce766f6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca12cbb111540303c875c4559a422153cf7c73f3e6bb6201f881ba29f139069d(
    value: typing.Optional[AlloydbInstanceQueryInsightsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0120a17d019867a39bdd1b37caa4ef3d6a7460620cc4588de9d2820ae166113a(
    *,
    node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e556805238a67471d3893e5fabd42872956bcc68346527e15a946ed38ea27f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943318cc25fb6c6992d481fdae72284609c691c58f76ded639cbccc4eddb93fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6158543947f4bc9fb14030f6c3aaeba07c43666ce7eccae912e026c2bf388738(
    value: typing.Optional[AlloydbInstanceReadPoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92852fd79f1a1c5827f4e08118e4b8d1230621d12ab5bd3224b75cd3a0aaedcf(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5cb81b3713f5486b0336541822b32c4dc250b959e4d0761a8ece4d1424ab7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95905f4e90d8f66e9d258da3dd09b81de67433dfda03e0b62f593f3bd3be278(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9ef26d489259d7ed73010fb95d0e8fc45a13cd5be617b6a48a9313552f080a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4553895f681f42dbf738f23a4e7a1f384184393c04956dbaee1f6706db8e21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc17f01754fc0647c4f612b32f9e93a7061cac0a49fbf4f69e833d262c586c39(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlloydbInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
