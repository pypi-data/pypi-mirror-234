'''
# `google_datastream_stream`

Refer to the Terraform Registory for docs: [`google_datastream_stream`](https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream).
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


class DatastreamStream(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStream",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream google_datastream_stream}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination_config: typing.Union["DatastreamStreamDestinationConfig", typing.Dict[builtins.str, typing.Any]],
        display_name: builtins.str,
        location: builtins.str,
        source_config: typing.Union["DatastreamStreamSourceConfig", typing.Dict[builtins.str, typing.Any]],
        stream_id: builtins.str,
        backfill_all: typing.Optional[typing.Union["DatastreamStreamBackfillAll", typing.Dict[builtins.str, typing.Any]]] = None,
        backfill_none: typing.Optional[typing.Union["DatastreamStreamBackfillNone", typing.Dict[builtins.str, typing.Any]]] = None,
        customer_managed_encryption_key: typing.Optional[builtins.str] = None,
        desired_state: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DatastreamStreamTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream google_datastream_stream} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination_config: destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#destination_config DatastreamStream#destination_config}
        :param display_name: Display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#display_name DatastreamStream#display_name}
        :param location: The name of the location this stream is located in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#location DatastreamStream#location}
        :param source_config: source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#source_config DatastreamStream#source_config}
        :param stream_id: The stream identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#stream_id DatastreamStream#stream_id}
        :param backfill_all: backfill_all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#backfill_all DatastreamStream#backfill_all}
        :param backfill_none: backfill_none block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#backfill_none DatastreamStream#backfill_none}
        :param customer_managed_encryption_key: A reference to a KMS encryption key. If provided, it will be used to encrypt the data. If left blank, data will be encrypted using an internal Stream-specific encryption key provisioned through KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#customer_managed_encryption_key DatastreamStream#customer_managed_encryption_key}
        :param desired_state: Desired state of the Stream. Set this field to 'RUNNING' to start the stream, and 'PAUSED' to pause the stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#desired_state DatastreamStream#desired_state}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#id DatastreamStream#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#labels DatastreamStream#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#project DatastreamStream#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#timeouts DatastreamStream#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c3ae3a9775ec6a2f34ba62bb34fac9132ef80c080cb4f5fc8bb6686d10ac590)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DatastreamStreamConfig(
            destination_config=destination_config,
            display_name=display_name,
            location=location,
            source_config=source_config,
            stream_id=stream_id,
            backfill_all=backfill_all,
            backfill_none=backfill_none,
            customer_managed_encryption_key=customer_managed_encryption_key,
            desired_state=desired_state,
            id=id,
            labels=labels,
            project=project,
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

    @jsii.member(jsii_name="putBackfillAll")
    def put_backfill_all(
        self,
        *,
        mysql_excluded_objects: typing.Optional[typing.Union["DatastreamStreamBackfillAllMysqlExcludedObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle_excluded_objects: typing.Optional[typing.Union["DatastreamStreamBackfillAllOracleExcludedObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql_excluded_objects: typing.Optional[typing.Union["DatastreamStreamBackfillAllPostgresqlExcludedObjects", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param mysql_excluded_objects: mysql_excluded_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_excluded_objects DatastreamStream#mysql_excluded_objects}
        :param oracle_excluded_objects: oracle_excluded_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_excluded_objects DatastreamStream#oracle_excluded_objects}
        :param postgresql_excluded_objects: postgresql_excluded_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_excluded_objects DatastreamStream#postgresql_excluded_objects}
        '''
        value = DatastreamStreamBackfillAll(
            mysql_excluded_objects=mysql_excluded_objects,
            oracle_excluded_objects=oracle_excluded_objects,
            postgresql_excluded_objects=postgresql_excluded_objects,
        )

        return typing.cast(None, jsii.invoke(self, "putBackfillAll", [value]))

    @jsii.member(jsii_name="putBackfillNone")
    def put_backfill_none(self) -> None:
        value = DatastreamStreamBackfillNone()

        return typing.cast(None, jsii.invoke(self, "putBackfillNone", [value]))

    @jsii.member(jsii_name="putDestinationConfig")
    def put_destination_config(
        self,
        *,
        destination_connection_profile: builtins.str,
        bigquery_destination_config: typing.Optional[typing.Union["DatastreamStreamDestinationConfigBigqueryDestinationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_destination_config: typing.Optional[typing.Union["DatastreamStreamDestinationConfigGcsDestinationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param destination_connection_profile: Destination connection profile resource. Format: projects/{project}/locations/{location}/connectionProfiles/{name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#destination_connection_profile DatastreamStream#destination_connection_profile}
        :param bigquery_destination_config: bigquery_destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#bigquery_destination_config DatastreamStream#bigquery_destination_config}
        :param gcs_destination_config: gcs_destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#gcs_destination_config DatastreamStream#gcs_destination_config}
        '''
        value = DatastreamStreamDestinationConfig(
            destination_connection_profile=destination_connection_profile,
            bigquery_destination_config=bigquery_destination_config,
            gcs_destination_config=gcs_destination_config,
        )

        return typing.cast(None, jsii.invoke(self, "putDestinationConfig", [value]))

    @jsii.member(jsii_name="putSourceConfig")
    def put_source_config(
        self,
        *,
        source_connection_profile: builtins.str,
        mysql_source_config: typing.Optional[typing.Union["DatastreamStreamSourceConfigMysqlSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle_source_config: typing.Optional[typing.Union["DatastreamStreamSourceConfigOracleSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql_source_config: typing.Optional[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param source_connection_profile: Source connection profile resource. Format: projects/{project}/locations/{location}/connectionProfiles/{name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#source_connection_profile DatastreamStream#source_connection_profile}
        :param mysql_source_config: mysql_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_source_config DatastreamStream#mysql_source_config}
        :param oracle_source_config: oracle_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_source_config DatastreamStream#oracle_source_config}
        :param postgresql_source_config: postgresql_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_source_config DatastreamStream#postgresql_source_config}
        '''
        value = DatastreamStreamSourceConfig(
            source_connection_profile=source_connection_profile,
            mysql_source_config=mysql_source_config,
            oracle_source_config=oracle_source_config,
            postgresql_source_config=postgresql_source_config,
        )

        return typing.cast(None, jsii.invoke(self, "putSourceConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#create DatastreamStream#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#delete DatastreamStream#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#update DatastreamStream#update}.
        '''
        value = DatastreamStreamTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBackfillAll")
    def reset_backfill_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackfillAll", []))

    @jsii.member(jsii_name="resetBackfillNone")
    def reset_backfill_none(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackfillNone", []))

    @jsii.member(jsii_name="resetCustomerManagedEncryptionKey")
    def reset_customer_managed_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerManagedEncryptionKey", []))

    @jsii.member(jsii_name="resetDesiredState")
    def reset_desired_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDesiredState", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="backfillAll")
    def backfill_all(self) -> "DatastreamStreamBackfillAllOutputReference":
        return typing.cast("DatastreamStreamBackfillAllOutputReference", jsii.get(self, "backfillAll"))

    @builtins.property
    @jsii.member(jsii_name="backfillNone")
    def backfill_none(self) -> "DatastreamStreamBackfillNoneOutputReference":
        return typing.cast("DatastreamStreamBackfillNoneOutputReference", jsii.get(self, "backfillNone"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfig")
    def destination_config(self) -> "DatastreamStreamDestinationConfigOutputReference":
        return typing.cast("DatastreamStreamDestinationConfigOutputReference", jsii.get(self, "destinationConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="sourceConfig")
    def source_config(self) -> "DatastreamStreamSourceConfigOutputReference":
        return typing.cast("DatastreamStreamSourceConfigOutputReference", jsii.get(self, "sourceConfig"))

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
    def timeouts(self) -> "DatastreamStreamTimeoutsOutputReference":
        return typing.cast("DatastreamStreamTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="backfillAllInput")
    def backfill_all_input(self) -> typing.Optional["DatastreamStreamBackfillAll"]:
        return typing.cast(typing.Optional["DatastreamStreamBackfillAll"], jsii.get(self, "backfillAllInput"))

    @builtins.property
    @jsii.member(jsii_name="backfillNoneInput")
    def backfill_none_input(self) -> typing.Optional["DatastreamStreamBackfillNone"]:
        return typing.cast(typing.Optional["DatastreamStreamBackfillNone"], jsii.get(self, "backfillNoneInput"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedEncryptionKeyInput")
    def customer_managed_encryption_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerManagedEncryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfigInput")
    def destination_config_input(
        self,
    ) -> typing.Optional["DatastreamStreamDestinationConfig"]:
        return typing.cast(typing.Optional["DatastreamStreamDestinationConfig"], jsii.get(self, "destinationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceConfigInput")
    def source_config_input(self) -> typing.Optional["DatastreamStreamSourceConfig"]:
        return typing.cast(typing.Optional["DatastreamStreamSourceConfig"], jsii.get(self, "sourceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="streamIdInput")
    def stream_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DatastreamStreamTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DatastreamStreamTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedEncryptionKey")
    def customer_managed_encryption_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerManagedEncryptionKey"))

    @customer_managed_encryption_key.setter
    def customer_managed_encryption_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4036af7d4997077ed9ef564c0f1c741942d81794bc5f2f2e42aaa87939e5b13a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerManagedEncryptionKey", value)

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52394fe12c454915c68b7f5c0e1158a297c28bf8edc5470752d8d03bdadb3ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075bf1e3249baeb8aa177ed19b3f502beb142b110c60b7139a705093ce1b0a7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07f951eeadca73ea4a620fa2306732bbea40433c714d9c7f9ff106a61a7faead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aef205b5c5ab66f32171c7535e21c4e68b81ebab105a33f1ff35977ad01202a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf79e1cbe57e9eb4ed393c90fd467db45153af81195ed412bfacee8feaa28a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643d9836b9fc11f1901e2a2838ff876acef8280f6554dd37d2d02fa890104d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="streamId")
    def stream_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streamId"))

    @stream_id.setter
    def stream_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283627036b55d75a53badb063b8cbdcac874d10da468b6abae149456f4ed27d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAll",
    jsii_struct_bases=[],
    name_mapping={
        "mysql_excluded_objects": "mysqlExcludedObjects",
        "oracle_excluded_objects": "oracleExcludedObjects",
        "postgresql_excluded_objects": "postgresqlExcludedObjects",
    },
)
class DatastreamStreamBackfillAll:
    def __init__(
        self,
        *,
        mysql_excluded_objects: typing.Optional[typing.Union["DatastreamStreamBackfillAllMysqlExcludedObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle_excluded_objects: typing.Optional[typing.Union["DatastreamStreamBackfillAllOracleExcludedObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql_excluded_objects: typing.Optional[typing.Union["DatastreamStreamBackfillAllPostgresqlExcludedObjects", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param mysql_excluded_objects: mysql_excluded_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_excluded_objects DatastreamStream#mysql_excluded_objects}
        :param oracle_excluded_objects: oracle_excluded_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_excluded_objects DatastreamStream#oracle_excluded_objects}
        :param postgresql_excluded_objects: postgresql_excluded_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_excluded_objects DatastreamStream#postgresql_excluded_objects}
        '''
        if isinstance(mysql_excluded_objects, dict):
            mysql_excluded_objects = DatastreamStreamBackfillAllMysqlExcludedObjects(**mysql_excluded_objects)
        if isinstance(oracle_excluded_objects, dict):
            oracle_excluded_objects = DatastreamStreamBackfillAllOracleExcludedObjects(**oracle_excluded_objects)
        if isinstance(postgresql_excluded_objects, dict):
            postgresql_excluded_objects = DatastreamStreamBackfillAllPostgresqlExcludedObjects(**postgresql_excluded_objects)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__548fd10e905731875c7b597865e08230b888f6d65781f1f9e58cc54902b013a8)
            check_type(argname="argument mysql_excluded_objects", value=mysql_excluded_objects, expected_type=type_hints["mysql_excluded_objects"])
            check_type(argname="argument oracle_excluded_objects", value=oracle_excluded_objects, expected_type=type_hints["oracle_excluded_objects"])
            check_type(argname="argument postgresql_excluded_objects", value=postgresql_excluded_objects, expected_type=type_hints["postgresql_excluded_objects"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mysql_excluded_objects is not None:
            self._values["mysql_excluded_objects"] = mysql_excluded_objects
        if oracle_excluded_objects is not None:
            self._values["oracle_excluded_objects"] = oracle_excluded_objects
        if postgresql_excluded_objects is not None:
            self._values["postgresql_excluded_objects"] = postgresql_excluded_objects

    @builtins.property
    def mysql_excluded_objects(
        self,
    ) -> typing.Optional["DatastreamStreamBackfillAllMysqlExcludedObjects"]:
        '''mysql_excluded_objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_excluded_objects DatastreamStream#mysql_excluded_objects}
        '''
        result = self._values.get("mysql_excluded_objects")
        return typing.cast(typing.Optional["DatastreamStreamBackfillAllMysqlExcludedObjects"], result)

    @builtins.property
    def oracle_excluded_objects(
        self,
    ) -> typing.Optional["DatastreamStreamBackfillAllOracleExcludedObjects"]:
        '''oracle_excluded_objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_excluded_objects DatastreamStream#oracle_excluded_objects}
        '''
        result = self._values.get("oracle_excluded_objects")
        return typing.cast(typing.Optional["DatastreamStreamBackfillAllOracleExcludedObjects"], result)

    @builtins.property
    def postgresql_excluded_objects(
        self,
    ) -> typing.Optional["DatastreamStreamBackfillAllPostgresqlExcludedObjects"]:
        '''postgresql_excluded_objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_excluded_objects DatastreamStream#postgresql_excluded_objects}
        '''
        result = self._values.get("postgresql_excluded_objects")
        return typing.cast(typing.Optional["DatastreamStreamBackfillAllPostgresqlExcludedObjects"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAll(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllMysqlExcludedObjects",
    jsii_struct_bases=[],
    name_mapping={"mysql_databases": "mysqlDatabases"},
)
class DatastreamStreamBackfillAllMysqlExcludedObjects:
    def __init__(
        self,
        *,
        mysql_databases: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param mysql_databases: mysql_databases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_databases DatastreamStream#mysql_databases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c73ea13a69e84cb5c059ba0260ae859d8c602b57e97a85cc24ad93dfc88b5f)
            check_type(argname="argument mysql_databases", value=mysql_databases, expected_type=type_hints["mysql_databases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mysql_databases": mysql_databases,
        }

    @builtins.property
    def mysql_databases(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases"]]:
        '''mysql_databases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_databases DatastreamStream#mysql_databases}
        '''
        result = self._values.get("mysql_databases")
        assert result is not None, "Required property 'mysql_databases' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAllMysqlExcludedObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "mysql_tables": "mysqlTables"},
)
class DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases:
    def __init__(
        self,
        *,
        database: builtins.str,
        mysql_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param database: Database name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#database DatastreamStream#database}
        :param mysql_tables: mysql_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_tables DatastreamStream#mysql_tables}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13410b2bfcca2c97647224c4a67319d908e9d319c6a9237cc85a4e41f55b548f)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument mysql_tables", value=mysql_tables, expected_type=type_hints["mysql_tables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
        }
        if mysql_tables is not None:
            self._values["mysql_tables"] = mysql_tables

    @builtins.property
    def database(self) -> builtins.str:
        '''Database name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#database DatastreamStream#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mysql_tables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables"]]]:
        '''mysql_tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_tables DatastreamStream#mysql_tables}
        '''
        result = self._values.get("mysql_tables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea67c8ef97a0bde8fc840322d14b0b15cad0751a347171e7dc7803d39cec09bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e433a44dd8df3a9cadc62af5b456b9bc010f04b3ba73bafaf04a805db07586db)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3201f4411b84a193a6646dd047aa80f26f7dde220aef2aef705c5287e252e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3c44068e63d483ac615dac0b8b6f39ba7905423e373797afbe8cc55e6cd75e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28ae6f5b98dab77299fa101efba9a44e8d9bd7f7ad9211e91cba088aa6c700ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aebbfa9a89be0456ea53147d93d92bf800659d380f16345317d1f06cc039aa0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables",
    jsii_struct_bases=[],
    name_mapping={"table": "table", "mysql_columns": "mysqlColumns"},
)
class DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables:
    def __init__(
        self,
        *,
        table: builtins.str,
        mysql_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param table: Table name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        :param mysql_columns: mysql_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_columns DatastreamStream#mysql_columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c949b7e6ad7f4b38807ff06c703f595dfd880a47c4b1d04b04a3915dec77355a)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument mysql_columns", value=mysql_columns, expected_type=type_hints["mysql_columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if mysql_columns is not None:
            self._values["mysql_columns"] = mysql_columns

    @builtins.property
    def table(self) -> builtins.str:
        '''Table name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mysql_columns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns"]]]:
        '''mysql_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_columns DatastreamStream#mysql_columns}
        '''
        result = self._values.get("mysql_columns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e065db95f692750c0a4063feef0b9379251d390020ae9aa8597c39b18492722e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71340320398dcd9797361c897dd802615c2838318ad836b9a8a7a371389ce73)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fae007e595a16d2276fc86cc2a375a7ac4c4e4fdf0b5e9c3807728d0312608d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f42f8dee5cb9de65146de9913d0470c79954bff38cb9237b2821934c9d38ba3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09927ad10009415e1a205ef82c502175614a7e64824510e9b69fbf9eec02feb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0487084e9cacd7c8d5ac7a0aa828f1cf005979ca02f03bd6ac2db3f9e309f1c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns",
    jsii_struct_bases=[],
    name_mapping={
        "collation": "collation",
        "column": "column",
        "data_type": "dataType",
        "nullable": "nullable",
        "ordinal_position": "ordinalPosition",
        "primary_key": "primaryKey",
    },
)
class DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns:
    def __init__(
        self,
        *,
        collation: typing.Optional[builtins.str] = None,
        column: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ordinal_position: typing.Optional[jsii.Number] = None,
        primary_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param collation: Column collation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#collation DatastreamStream#collation}
        :param column: Column name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        :param data_type: The MySQL data type. Full data types list can be found here: https://dev.mysql.com/doc/refman/8.0/en/data-types.html. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        :param nullable: Whether or not the column can accept a null value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#nullable DatastreamStream#nullable}
        :param ordinal_position: The ordinal position of the column in the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#ordinal_position DatastreamStream#ordinal_position}
        :param primary_key: Whether or not the column represents a primary key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#primary_key DatastreamStream#primary_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358f467e5b0f4377a34511fe2df79cd3ce7c42608d71ea9bc665657743281de9)
            check_type(argname="argument collation", value=collation, expected_type=type_hints["collation"])
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument nullable", value=nullable, expected_type=type_hints["nullable"])
            check_type(argname="argument ordinal_position", value=ordinal_position, expected_type=type_hints["ordinal_position"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if collation is not None:
            self._values["collation"] = collation
        if column is not None:
            self._values["column"] = column
        if data_type is not None:
            self._values["data_type"] = data_type
        if nullable is not None:
            self._values["nullable"] = nullable
        if ordinal_position is not None:
            self._values["ordinal_position"] = ordinal_position
        if primary_key is not None:
            self._values["primary_key"] = primary_key

    @builtins.property
    def collation(self) -> typing.Optional[builtins.str]:
        '''Column collation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#collation DatastreamStream#collation}
        '''
        result = self._values.get("collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def column(self) -> typing.Optional[builtins.str]:
        '''Column name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        '''
        result = self._values.get("column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''The MySQL data type. Full data types list can be found here: https://dev.mysql.com/doc/refman/8.0/en/data-types.html.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nullable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the column can accept a null value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#nullable DatastreamStream#nullable}
        '''
        result = self._values.get("nullable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ordinal_position(self) -> typing.Optional[jsii.Number]:
        '''The ordinal position of the column in the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#ordinal_position DatastreamStream#ordinal_position}
        '''
        result = self._values.get("ordinal_position")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the column represents a primary key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#primary_key DatastreamStream#primary_key}
        '''
        result = self._values.get("primary_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__154f8dbef744b6d64d4b273c1aee6e622e76745c185fc129b20166f1d3b1983d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__713d5e717689a63ec3720f83c87565cadea875f763aa9cc85738d05e657e219d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa9e390d9ad10ccedd8763652c1adc0808202e386abbe93d623f621504e76ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9301374e73e0c50562a61bc71b8dd7a070d34619dda616483dea5909e9f46f98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91c7b000f7d51a6d417fbacbfba2f039c7d7c3eb9281b41955951acec133650c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5df9305e59f038bfd61176fa4734ffa910d0bf7dee993b79f7d55c7529c3a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f018984efb7d263d0ffcb99493054e866b0c5304311041e893283f901e4a6c5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCollation")
    def reset_collation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollation", []))

    @jsii.member(jsii_name="resetColumn")
    def reset_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumn", []))

    @jsii.member(jsii_name="resetDataType")
    def reset_data_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataType", []))

    @jsii.member(jsii_name="resetNullable")
    def reset_nullable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullable", []))

    @jsii.member(jsii_name="resetOrdinalPosition")
    def reset_ordinal_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrdinalPosition", []))

    @jsii.member(jsii_name="resetPrimaryKey")
    def reset_primary_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryKey", []))

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "length"))

    @builtins.property
    @jsii.member(jsii_name="collationInput")
    def collation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collationInput"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypeInput")
    def data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nullableInput")
    def nullable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nullableInput"))

    @builtins.property
    @jsii.member(jsii_name="ordinalPositionInput")
    def ordinal_position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ordinalPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeyInput")
    def primary_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="collation")
    def collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collation"))

    @collation.setter
    def collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70a552d16c9eeee74bbdd4efdd9298e085ed23856eae9264a8b1de5d65bc128c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collation", value)

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "column"))

    @column.setter
    def column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef3bcf0cf613c3945de3f7f965b20939420613dbf0bda0a777109acd57296b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ccd286da9f0d1f1989f8eff655c80e6b67fe37f7ff035a8f81704b1c1948fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="nullable")
    def nullable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nullable"))

    @nullable.setter
    def nullable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42f8e7181c09785a11ef026e085afe5bbd15bce5111673479bccb9c3566cc49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullable", value)

    @builtins.property
    @jsii.member(jsii_name="ordinalPosition")
    def ordinal_position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ordinalPosition"))

    @ordinal_position.setter
    def ordinal_position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097daa092a18ee02bf8669de9bd114d35e6fadb3ea65a486cabfd5b2425b3f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ordinalPosition", value)

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4cd8ea957cbc5045edf6e2553556a3e684a0ab60fb1a5fa3c7c003e727ee3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e079a8c2bf48a82f26ea7ebb4307d6a05b485fc96ce3f041b43af86038484f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87a74c6f0174c2f917092188e7a5baac1b4376e817d30c3ddac8bfdd08ace52b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMysqlColumns")
    def put_mysql_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9d4d13b08ecd8dfe67092ac6f87dde17666a854de010456318e3bdd9e068bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysqlColumns", [value]))

    @jsii.member(jsii_name="resetMysqlColumns")
    def reset_mysql_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlColumns", []))

    @builtins.property
    @jsii.member(jsii_name="mysqlColumns")
    def mysql_columns(
        self,
    ) -> DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumnsList:
        return typing.cast(DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumnsList, jsii.get(self, "mysqlColumns"))

    @builtins.property
    @jsii.member(jsii_name="mysqlColumnsInput")
    def mysql_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns]]], jsii.get(self, "mysqlColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f0e90b83d1fa5fa9212c0d7bb6231593356596ff82ad67b135f440e2c462282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de0b4e25f18b8e00271d40dc319fa34c7902a7c2c0ad6fd321f7f236706f10f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f5f8347e6725fe1f7f0267f7c851ffb9628cb21ac0e30564b95091505abfc30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMysqlTables")
    def put_mysql_tables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f814fec22f6e810871992154543a73b1af75cbbc27447a3fe884a5a80fb50c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysqlTables", [value]))

    @jsii.member(jsii_name="resetMysqlTables")
    def reset_mysql_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlTables", []))

    @builtins.property
    @jsii.member(jsii_name="mysqlTables")
    def mysql_tables(
        self,
    ) -> DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesList:
        return typing.cast(DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesList, jsii.get(self, "mysqlTables"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlTablesInput")
    def mysql_tables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables]]], jsii.get(self, "mysqlTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3151b274792b3f93fe09adbe180c158913e6bd5db0b114d7f42e9a220f02a568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7388148daab50b0ac722ba039b4763c332b0cf752fb7ecd0b82947dc468abe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamBackfillAllMysqlExcludedObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllMysqlExcludedObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f1d7a4d992a763ac519977aaaad6c758ee59d5bab019a7a7745a4616285a28d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMysqlDatabases")
    def put_mysql_databases(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931bbf966cb9ba2aae819fbebe1786809f88f7da77ce8346aaffbdcfad968a76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysqlDatabases", [value]))

    @builtins.property
    @jsii.member(jsii_name="mysqlDatabases")
    def mysql_databases(
        self,
    ) -> DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesList:
        return typing.cast(DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesList, jsii.get(self, "mysqlDatabases"))

    @builtins.property
    @jsii.member(jsii_name="mysqlDatabasesInput")
    def mysql_databases_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases]]], jsii.get(self, "mysqlDatabasesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamBackfillAllMysqlExcludedObjects]:
        return typing.cast(typing.Optional[DatastreamStreamBackfillAllMysqlExcludedObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamBackfillAllMysqlExcludedObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811433edaf8b7400da4083dd0803cdd680452b065b43ce1320c11977ab1cc96f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllOracleExcludedObjects",
    jsii_struct_bases=[],
    name_mapping={"oracle_schemas": "oracleSchemas"},
)
class DatastreamStreamBackfillAllOracleExcludedObjects:
    def __init__(
        self,
        *,
        oracle_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param oracle_schemas: oracle_schemas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_schemas DatastreamStream#oracle_schemas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52841f107f2901aed8657e6d83ecd50347ad8033afa7608787869317a9404e84)
            check_type(argname="argument oracle_schemas", value=oracle_schemas, expected_type=type_hints["oracle_schemas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oracle_schemas": oracle_schemas,
        }

    @builtins.property
    def oracle_schemas(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas"]]:
        '''oracle_schemas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_schemas DatastreamStream#oracle_schemas}
        '''
        result = self._values.get("oracle_schemas")
        assert result is not None, "Required property 'oracle_schemas' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAllOracleExcludedObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas",
    jsii_struct_bases=[],
    name_mapping={"schema": "schema", "oracle_tables": "oracleTables"},
)
class DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas:
    def __init__(
        self,
        *,
        schema: builtins.str,
        oracle_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param schema: Schema name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema DatastreamStream#schema}
        :param oracle_tables: oracle_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_tables DatastreamStream#oracle_tables}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd4c08a9f3b5ad8460edfca3f7a1b7d1afffd9086a76a540f6a0d44ba83090b)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument oracle_tables", value=oracle_tables, expected_type=type_hints["oracle_tables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema": schema,
        }
        if oracle_tables is not None:
            self._values["oracle_tables"] = oracle_tables

    @builtins.property
    def schema(self) -> builtins.str:
        '''Schema name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema DatastreamStream#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oracle_tables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables"]]]:
        '''oracle_tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_tables DatastreamStream#oracle_tables}
        '''
        result = self._values.get("oracle_tables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79b730e1c71b3d87311c7d6e18f194c7b92727ab9013b980ce066c20ceeb195a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c38f1129acd1f802d161834b127dff5511d9274793b93a7339ad22df7c9d0dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd09e5cf8228cfb704103b56fa935016916c13a3720f7c5a0d624e991afe05a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0c358908b37412b7eeaaf4391bcd8f0639b6ae2ab10ae432f528556a7579fef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0178be83df611c9f9d4e3620e0325a5204db08445243d5c32db345e4aa9d4d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8516cb522db34e652278d419ed5c8c8d73f2ceb8396840414a6ea84d47e9aa63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables",
    jsii_struct_bases=[],
    name_mapping={"table": "table", "oracle_columns": "oracleColumns"},
)
class DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables:
    def __init__(
        self,
        *,
        table: builtins.str,
        oracle_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param table: Table name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        :param oracle_columns: oracle_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_columns DatastreamStream#oracle_columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d6e5fd7422aa55104fff2e8bd7a46cdfb59e556c32cba3834202b15f50f8fad)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument oracle_columns", value=oracle_columns, expected_type=type_hints["oracle_columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if oracle_columns is not None:
            self._values["oracle_columns"] = oracle_columns

    @builtins.property
    def table(self) -> builtins.str:
        '''Table name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oracle_columns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns"]]]:
        '''oracle_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_columns DatastreamStream#oracle_columns}
        '''
        result = self._values.get("oracle_columns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b601d2c5879f402a0f0af8f32fde94cb7d97c0e7b6fcfc44d0400bd7b1f9368)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe2d2a1750b59df90fecb23008d497068e2681a6556df293a4576b3d1e9617e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221165e97b7f1cfaab37a2f8114648611153e7e2533817cb1fe14ee71beadbbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0780eb9549db2b16ec6411b4a414a188205bdcf10f4c8f761be5f0c18211985d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21a5d7db789059655cc63684fd9cc2b0a60b8b421b5cc716120649a09e05c666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be4a8dfc23cafff0057053b2818a5db1e1bbb5d18919e9e12b98927ae00d224e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns",
    jsii_struct_bases=[],
    name_mapping={"column": "column", "data_type": "dataType"},
)
class DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns:
    def __init__(
        self,
        *,
        column: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column: Column name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        :param data_type: The Oracle data type. Full data types list can be found here: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6180aa03e8588ed9b998f6efddb3ea71242d914242ab52fbb62859344c922b86)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column is not None:
            self._values["column"] = column
        if data_type is not None:
            self._values["data_type"] = data_type

    @builtins.property
    def column(self) -> typing.Optional[builtins.str]:
        '''Column name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        '''
        result = self._values.get("column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''The Oracle data type. Full data types list can be found here: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f96ab2af89fe82e13e2618ceb77fae34f255d26b210edfded1f673dfc8b1725)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb98c67d7153e6a46a49fb3e128845124be743fc02b472fc8d637d9a83f4d97)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db03e6756fdc892ded71af92b1d8dcec8c8bb3ecc246034669d24485d6608fe8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d41f3bf440f4f1744a43c9ea7da7c63e9f6ced42fc2ef520ae1a9c6f02d27bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cecf0a0710927b872b4671b43df83560ff52917e6d85bfe8b8886066eae4a2de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcde6766fd17cbf1bc355d4b9e85ba292fad4a44bb9b6e39b6dc4fa55f5fa02b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e717b10e4a0340f61a74762e1f694b2dcda7958a943e00da21284498701dbfa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetColumn")
    def reset_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumn", []))

    @jsii.member(jsii_name="resetDataType")
    def reset_data_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataType", []))

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "length"))

    @builtins.property
    @jsii.member(jsii_name="nullable")
    def nullable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "nullable"))

    @builtins.property
    @jsii.member(jsii_name="ordinalPosition")
    def ordinal_position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ordinalPosition"))

    @builtins.property
    @jsii.member(jsii_name="precision")
    def precision(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precision"))

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "primaryKey"))

    @builtins.property
    @jsii.member(jsii_name="scale")
    def scale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scale"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypeInput")
    def data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "column"))

    @column.setter
    def column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489b4bd1c3dcccee0bcc7eaea45211034532a13eff1cb863fc4ee8e62bb03b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08279d3ce3e352e760b9f3c0e6fb6c61808901c8f96666f27b8ae26b88ca57f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00ef7590783646406570c2cd5497558d376a91c651285790776f0431fd23846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db7d3b45930bf61a809ca9a4520c09604ef3300bce2cdd2e27209c968602d389)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putOracleColumns")
    def put_oracle_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d95ce9e328cae540a5475f8dc661f64120261cfb4ee494ab0e4d95c7ba15f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOracleColumns", [value]))

    @jsii.member(jsii_name="resetOracleColumns")
    def reset_oracle_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracleColumns", []))

    @builtins.property
    @jsii.member(jsii_name="oracleColumns")
    def oracle_columns(
        self,
    ) -> DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumnsList:
        return typing.cast(DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumnsList, jsii.get(self, "oracleColumns"))

    @builtins.property
    @jsii.member(jsii_name="oracleColumnsInput")
    def oracle_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns]]], jsii.get(self, "oracleColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b01affeee65683f918cc0495d19037bca6da50345d62121f3e9c53bd631a12de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0957ea6c2099733147a731e6706eb8c70302512e3c0f28f85e95013b4979f268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8a6c8678ab8ea6e85611fd5f16e42fc7138f31006eef3ff96ebef0aa53dc7ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putOracleTables")
    def put_oracle_tables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8155c19b5637412b8082acce6c37d407af21301ef8e768af1eb577f104abac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOracleTables", [value]))

    @jsii.member(jsii_name="resetOracleTables")
    def reset_oracle_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracleTables", []))

    @builtins.property
    @jsii.member(jsii_name="oracleTables")
    def oracle_tables(
        self,
    ) -> DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesList:
        return typing.cast(DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesList, jsii.get(self, "oracleTables"))

    @builtins.property
    @jsii.member(jsii_name="oracleTablesInput")
    def oracle_tables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables]]], jsii.get(self, "oracleTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c8f07606f3b0fe32f7948b686a3527c1ac821feb0e31ba8c1487b5c8c15ef9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0346b7769948dfb8faf4ed88fc5d7fffbf9c366c551b7b458354814c8f58cf03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamBackfillAllOracleExcludedObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllOracleExcludedObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c56e72c4b87c7e975fc8d7fe6236ced1cf9d249ca9d0372b050fae435f77e2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOracleSchemas")
    def put_oracle_schemas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3104458a1514472f120a6dc45e490d9d9f6ca896252b02cf906aed81ae8a86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOracleSchemas", [value]))

    @builtins.property
    @jsii.member(jsii_name="oracleSchemas")
    def oracle_schemas(
        self,
    ) -> DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasList:
        return typing.cast(DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasList, jsii.get(self, "oracleSchemas"))

    @builtins.property
    @jsii.member(jsii_name="oracleSchemasInput")
    def oracle_schemas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas]]], jsii.get(self, "oracleSchemasInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamBackfillAllOracleExcludedObjects]:
        return typing.cast(typing.Optional[DatastreamStreamBackfillAllOracleExcludedObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamBackfillAllOracleExcludedObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__869aabaa7ffdcaa3cfdda51ef3e63dc256c8f0e282655311636f024ec823cdad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamBackfillAllOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f2165189e7c8f1b458755c804ed55962f85c000ded00d4c56f68f9f3bcf3eb1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMysqlExcludedObjects")
    def put_mysql_excluded_objects(
        self,
        *,
        mysql_databases: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param mysql_databases: mysql_databases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_databases DatastreamStream#mysql_databases}
        '''
        value = DatastreamStreamBackfillAllMysqlExcludedObjects(
            mysql_databases=mysql_databases
        )

        return typing.cast(None, jsii.invoke(self, "putMysqlExcludedObjects", [value]))

    @jsii.member(jsii_name="putOracleExcludedObjects")
    def put_oracle_excluded_objects(
        self,
        *,
        oracle_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param oracle_schemas: oracle_schemas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_schemas DatastreamStream#oracle_schemas}
        '''
        value = DatastreamStreamBackfillAllOracleExcludedObjects(
            oracle_schemas=oracle_schemas
        )

        return typing.cast(None, jsii.invoke(self, "putOracleExcludedObjects", [value]))

    @jsii.member(jsii_name="putPostgresqlExcludedObjects")
    def put_postgresql_excluded_objects(
        self,
        *,
        postgresql_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param postgresql_schemas: postgresql_schemas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_schemas DatastreamStream#postgresql_schemas}
        '''
        value = DatastreamStreamBackfillAllPostgresqlExcludedObjects(
            postgresql_schemas=postgresql_schemas
        )

        return typing.cast(None, jsii.invoke(self, "putPostgresqlExcludedObjects", [value]))

    @jsii.member(jsii_name="resetMysqlExcludedObjects")
    def reset_mysql_excluded_objects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlExcludedObjects", []))

    @jsii.member(jsii_name="resetOracleExcludedObjects")
    def reset_oracle_excluded_objects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracleExcludedObjects", []))

    @jsii.member(jsii_name="resetPostgresqlExcludedObjects")
    def reset_postgresql_excluded_objects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresqlExcludedObjects", []))

    @builtins.property
    @jsii.member(jsii_name="mysqlExcludedObjects")
    def mysql_excluded_objects(
        self,
    ) -> DatastreamStreamBackfillAllMysqlExcludedObjectsOutputReference:
        return typing.cast(DatastreamStreamBackfillAllMysqlExcludedObjectsOutputReference, jsii.get(self, "mysqlExcludedObjects"))

    @builtins.property
    @jsii.member(jsii_name="oracleExcludedObjects")
    def oracle_excluded_objects(
        self,
    ) -> DatastreamStreamBackfillAllOracleExcludedObjectsOutputReference:
        return typing.cast(DatastreamStreamBackfillAllOracleExcludedObjectsOutputReference, jsii.get(self, "oracleExcludedObjects"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlExcludedObjects")
    def postgresql_excluded_objects(
        self,
    ) -> "DatastreamStreamBackfillAllPostgresqlExcludedObjectsOutputReference":
        return typing.cast("DatastreamStreamBackfillAllPostgresqlExcludedObjectsOutputReference", jsii.get(self, "postgresqlExcludedObjects"))

    @builtins.property
    @jsii.member(jsii_name="mysqlExcludedObjectsInput")
    def mysql_excluded_objects_input(
        self,
    ) -> typing.Optional[DatastreamStreamBackfillAllMysqlExcludedObjects]:
        return typing.cast(typing.Optional[DatastreamStreamBackfillAllMysqlExcludedObjects], jsii.get(self, "mysqlExcludedObjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="oracleExcludedObjectsInput")
    def oracle_excluded_objects_input(
        self,
    ) -> typing.Optional[DatastreamStreamBackfillAllOracleExcludedObjects]:
        return typing.cast(typing.Optional[DatastreamStreamBackfillAllOracleExcludedObjects], jsii.get(self, "oracleExcludedObjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlExcludedObjectsInput")
    def postgresql_excluded_objects_input(
        self,
    ) -> typing.Optional["DatastreamStreamBackfillAllPostgresqlExcludedObjects"]:
        return typing.cast(typing.Optional["DatastreamStreamBackfillAllPostgresqlExcludedObjects"], jsii.get(self, "postgresqlExcludedObjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DatastreamStreamBackfillAll]:
        return typing.cast(typing.Optional[DatastreamStreamBackfillAll], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamBackfillAll],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5097bf84b7756c5e909c8358f325e4cc1c90362407525d463c71a947058c4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllPostgresqlExcludedObjects",
    jsii_struct_bases=[],
    name_mapping={"postgresql_schemas": "postgresqlSchemas"},
)
class DatastreamStreamBackfillAllPostgresqlExcludedObjects:
    def __init__(
        self,
        *,
        postgresql_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param postgresql_schemas: postgresql_schemas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_schemas DatastreamStream#postgresql_schemas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a44a84d805c486bcce836837e5e3b6e5c71eb27c894f3f86e12e0e4a10918402)
            check_type(argname="argument postgresql_schemas", value=postgresql_schemas, expected_type=type_hints["postgresql_schemas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "postgresql_schemas": postgresql_schemas,
        }

    @builtins.property
    def postgresql_schemas(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas"]]:
        '''postgresql_schemas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_schemas DatastreamStream#postgresql_schemas}
        '''
        result = self._values.get("postgresql_schemas")
        assert result is not None, "Required property 'postgresql_schemas' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAllPostgresqlExcludedObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamBackfillAllPostgresqlExcludedObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllPostgresqlExcludedObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18d193e63a6456924ddd6ebeaf1e10b8e6172fb03c7a36235a89684ee580ba9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostgresqlSchemas")
    def put_postgresql_schemas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5339414b6165e4bbae405e61c1e04bc62a2947807fd8f3a84191915855a3c5b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostgresqlSchemas", [value]))

    @builtins.property
    @jsii.member(jsii_name="postgresqlSchemas")
    def postgresql_schemas(
        self,
    ) -> "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasList":
        return typing.cast("DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasList", jsii.get(self, "postgresqlSchemas"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlSchemasInput")
    def postgresql_schemas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas"]]], jsii.get(self, "postgresqlSchemasInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamBackfillAllPostgresqlExcludedObjects]:
        return typing.cast(typing.Optional[DatastreamStreamBackfillAllPostgresqlExcludedObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamBackfillAllPostgresqlExcludedObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__254351ab6a7759c2179a6ea2bab099c63244ca754b27f5241f170a74994ea22e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas",
    jsii_struct_bases=[],
    name_mapping={"schema": "schema", "postgresql_tables": "postgresqlTables"},
)
class DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas:
    def __init__(
        self,
        *,
        schema: builtins.str,
        postgresql_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param schema: Database name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema DatastreamStream#schema}
        :param postgresql_tables: postgresql_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_tables DatastreamStream#postgresql_tables}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df8dc73a481bee6b7964b79f757d11e83823496223a34981f463a4cf6e79456)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument postgresql_tables", value=postgresql_tables, expected_type=type_hints["postgresql_tables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema": schema,
        }
        if postgresql_tables is not None:
            self._values["postgresql_tables"] = postgresql_tables

    @builtins.property
    def schema(self) -> builtins.str:
        '''Database name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema DatastreamStream#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postgresql_tables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables"]]]:
        '''postgresql_tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_tables DatastreamStream#postgresql_tables}
        '''
        result = self._values.get("postgresql_tables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7d56235ed2088958ea8c3451888e566f4f2d110ee0c3ebfeb29ad7ad4ddc584)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11fd39cc07b3833c49e5c2a1b85143bcde2b5c9d81e5a900bcdc531e2838c8f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c8ef4372afb1ac7c0961bebc56e337fbf100540bc7c90cf45029ff9ca302c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b46de3f2533f76f63b416ccdea2c5f48d439e063252f25fdacca87ffe3f275f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e09ce28567d48d53e9a98cd34a8b9b84dd48c3e7c79166e3976d9d2c7ba9c19f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857a0b75341a2930edf5b697dfee8f37da9eb5997d83d07e46013d21fb9d3668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac354a35a65f18e1f09a228a0090b838790a8d3ea570e113dea82dba47c7b3fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPostgresqlTables")
    def put_postgresql_tables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed8db8077edd3df844e7f2a9697d1c649bbd53167262c0a232bf77ff7900482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostgresqlTables", [value]))

    @jsii.member(jsii_name="resetPostgresqlTables")
    def reset_postgresql_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresqlTables", []))

    @builtins.property
    @jsii.member(jsii_name="postgresqlTables")
    def postgresql_tables(
        self,
    ) -> "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesList":
        return typing.cast("DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesList", jsii.get(self, "postgresqlTables"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlTablesInput")
    def postgresql_tables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables"]]], jsii.get(self, "postgresqlTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24cee6080160f8ce254f6881577a90050147bfc60656b23c6fbe0f54bc3f422a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc3004bc21f83e386c87081400d9180d9ff84833997649c90bbbdc9f18ce4b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables",
    jsii_struct_bases=[],
    name_mapping={"table": "table", "postgresql_columns": "postgresqlColumns"},
)
class DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables:
    def __init__(
        self,
        *,
        table: builtins.str,
        postgresql_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param table: Table name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        :param postgresql_columns: postgresql_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_columns DatastreamStream#postgresql_columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0895eb06a7e0758e0a81197c2088b2bfab18a75e235f1152f8f4bdc5d1af89)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument postgresql_columns", value=postgresql_columns, expected_type=type_hints["postgresql_columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if postgresql_columns is not None:
            self._values["postgresql_columns"] = postgresql_columns

    @builtins.property
    def table(self) -> builtins.str:
        '''Table name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postgresql_columns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns"]]]:
        '''postgresql_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_columns DatastreamStream#postgresql_columns}
        '''
        result = self._values.get("postgresql_columns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73e95e0645f052681248d5f6cc5094ea5f95b7f8de8ff3465d234f60bf4042a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642c17323e5280f2ee99185d2b50e23b7add47646f081bc4842a7ffbb73ebd7a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edcd5f836cc42fe03c692f748fc2d920d5932755ddc314336be058230ea684c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d5eeca4447782fad94dcb91015e095041bd52e956ca9dd6c407ef9f2f61f52a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b599079b0745008056cef2bf2c77bfc173240f26b61dc3d2f85e480f6c578bc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c3349a6f844f806dcb04667db73c0d4ca6c84ce0bb984fe2e395b831b95191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1892a8ca0dc0b58b4ff6af8064b15bd4559caccd93f4647b71af0d8e30c9ec7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPostgresqlColumns")
    def put_postgresql_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceba9c3502f3560119783ac581c7b6ed48cad64f8568c6e4cc10c625b550de03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostgresqlColumns", [value]))

    @jsii.member(jsii_name="resetPostgresqlColumns")
    def reset_postgresql_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresqlColumns", []))

    @builtins.property
    @jsii.member(jsii_name="postgresqlColumns")
    def postgresql_columns(
        self,
    ) -> "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList":
        return typing.cast("DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList", jsii.get(self, "postgresqlColumns"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlColumnsInput")
    def postgresql_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns"]]], jsii.get(self, "postgresqlColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5fe1aaeec0dfc894679a8d067bc8f2e2761a7ec03843f8de7819762bd2ebd17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34625c3cc8fdf881fe83f3c0811e35ce077ccd80c6cb30cc70dd8489927e3e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "data_type": "dataType",
        "nullable": "nullable",
        "ordinal_position": "ordinalPosition",
        "primary_key": "primaryKey",
    },
)
class DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns:
    def __init__(
        self,
        *,
        column: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ordinal_position: typing.Optional[jsii.Number] = None,
        primary_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param column: Column name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        :param data_type: The PostgreSQL data type. Full data types list can be found here: https://www.postgresql.org/docs/current/datatype.html. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        :param nullable: Whether or not the column can accept a null value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#nullable DatastreamStream#nullable}
        :param ordinal_position: The ordinal position of the column in the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#ordinal_position DatastreamStream#ordinal_position}
        :param primary_key: Whether or not the column represents a primary key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#primary_key DatastreamStream#primary_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6463b08efcf4f8acf83305a38b96396d3a21da2198ee85184519a76045993efe)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument nullable", value=nullable, expected_type=type_hints["nullable"])
            check_type(argname="argument ordinal_position", value=ordinal_position, expected_type=type_hints["ordinal_position"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column is not None:
            self._values["column"] = column
        if data_type is not None:
            self._values["data_type"] = data_type
        if nullable is not None:
            self._values["nullable"] = nullable
        if ordinal_position is not None:
            self._values["ordinal_position"] = ordinal_position
        if primary_key is not None:
            self._values["primary_key"] = primary_key

    @builtins.property
    def column(self) -> typing.Optional[builtins.str]:
        '''Column name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        '''
        result = self._values.get("column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''The PostgreSQL data type. Full data types list can be found here: https://www.postgresql.org/docs/current/datatype.html.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nullable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the column can accept a null value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#nullable DatastreamStream#nullable}
        '''
        result = self._values.get("nullable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ordinal_position(self) -> typing.Optional[jsii.Number]:
        '''The ordinal position of the column in the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#ordinal_position DatastreamStream#ordinal_position}
        '''
        result = self._values.get("ordinal_position")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the column represents a primary key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#primary_key DatastreamStream#primary_key}
        '''
        result = self._values.get("primary_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7218819eda5b9a7f7f7e44a80cb3e0e13028356373d6f41d59b04004bccbf214)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d9323b07a975fc21e6a0daee1d5e5a4cc882edea83fed3ef9a577285c07002)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572ebff2009111e875933582601c2a38fb018cf539d9b6cb3724050e7bc3da32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be69216e886a8be1bbe37eb47125134f68fbe7712b235469ef7c0dd071a786dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5beca11f8221e40508b6082b1dd689a96688d04b16d196d75e10de608b83080c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb02e7e5662cd9edd62463b927799f0ffde5141d2d0949dc56976a5d73425d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f543bf9cbfc914823e6469ca15226d83225e8ee9984684c8099a23956e44eff6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetColumn")
    def reset_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumn", []))

    @jsii.member(jsii_name="resetDataType")
    def reset_data_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataType", []))

    @jsii.member(jsii_name="resetNullable")
    def reset_nullable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullable", []))

    @jsii.member(jsii_name="resetOrdinalPosition")
    def reset_ordinal_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrdinalPosition", []))

    @jsii.member(jsii_name="resetPrimaryKey")
    def reset_primary_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryKey", []))

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "length"))

    @builtins.property
    @jsii.member(jsii_name="precision")
    def precision(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precision"))

    @builtins.property
    @jsii.member(jsii_name="scale")
    def scale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scale"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypeInput")
    def data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nullableInput")
    def nullable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nullableInput"))

    @builtins.property
    @jsii.member(jsii_name="ordinalPositionInput")
    def ordinal_position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ordinalPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeyInput")
    def primary_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "column"))

    @column.setter
    def column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17b561141aa360019b953cb434356f3dfe360978276c1888f4a0e496cbdd45f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2e8a03f99750b80d586c143d765355ed78d4379b1cbb16899641ca6ddd00bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="nullable")
    def nullable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nullable"))

    @nullable.setter
    def nullable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d67651ef84ce3863e6b8dbc30be73f92e014f372b0892c003535af3ac55bae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullable", value)

    @builtins.property
    @jsii.member(jsii_name="ordinalPosition")
    def ordinal_position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ordinalPosition"))

    @ordinal_position.setter
    def ordinal_position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088f45ef4903a052a86ca7276f66eda9910525fae8c5b559c39c22df9e3b8b04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ordinalPosition", value)

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34fb414017282c760c6995b124b06445e6f0b81b4bf1ed455292cec3525167e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28ec56985ad7b5c5a334fcd6b700d3969c032094ec1c2d67f5e656907c81a9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillNone",
    jsii_struct_bases=[],
    name_mapping={},
)
class DatastreamStreamBackfillNone:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamBackfillNone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamBackfillNoneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamBackfillNoneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fe33cc0ef94cf2a41dd327fc0be0593dc211e9743a24827b5ee773542c7a8c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DatastreamStreamBackfillNone]:
        return typing.cast(typing.Optional[DatastreamStreamBackfillNone], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamBackfillNone],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af34f772ce61a51e2c5569138f820502f4470ede6042b4080b30aef00600f8a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destination_config": "destinationConfig",
        "display_name": "displayName",
        "location": "location",
        "source_config": "sourceConfig",
        "stream_id": "streamId",
        "backfill_all": "backfillAll",
        "backfill_none": "backfillNone",
        "customer_managed_encryption_key": "customerManagedEncryptionKey",
        "desired_state": "desiredState",
        "id": "id",
        "labels": "labels",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class DatastreamStreamConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destination_config: typing.Union["DatastreamStreamDestinationConfig", typing.Dict[builtins.str, typing.Any]],
        display_name: builtins.str,
        location: builtins.str,
        source_config: typing.Union["DatastreamStreamSourceConfig", typing.Dict[builtins.str, typing.Any]],
        stream_id: builtins.str,
        backfill_all: typing.Optional[typing.Union[DatastreamStreamBackfillAll, typing.Dict[builtins.str, typing.Any]]] = None,
        backfill_none: typing.Optional[typing.Union[DatastreamStreamBackfillNone, typing.Dict[builtins.str, typing.Any]]] = None,
        customer_managed_encryption_key: typing.Optional[builtins.str] = None,
        desired_state: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DatastreamStreamTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destination_config: destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#destination_config DatastreamStream#destination_config}
        :param display_name: Display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#display_name DatastreamStream#display_name}
        :param location: The name of the location this stream is located in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#location DatastreamStream#location}
        :param source_config: source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#source_config DatastreamStream#source_config}
        :param stream_id: The stream identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#stream_id DatastreamStream#stream_id}
        :param backfill_all: backfill_all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#backfill_all DatastreamStream#backfill_all}
        :param backfill_none: backfill_none block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#backfill_none DatastreamStream#backfill_none}
        :param customer_managed_encryption_key: A reference to a KMS encryption key. If provided, it will be used to encrypt the data. If left blank, data will be encrypted using an internal Stream-specific encryption key provisioned through KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#customer_managed_encryption_key DatastreamStream#customer_managed_encryption_key}
        :param desired_state: Desired state of the Stream. Set this field to 'RUNNING' to start the stream, and 'PAUSED' to pause the stream. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#desired_state DatastreamStream#desired_state}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#id DatastreamStream#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#labels DatastreamStream#labels}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#project DatastreamStream#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#timeouts DatastreamStream#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destination_config, dict):
            destination_config = DatastreamStreamDestinationConfig(**destination_config)
        if isinstance(source_config, dict):
            source_config = DatastreamStreamSourceConfig(**source_config)
        if isinstance(backfill_all, dict):
            backfill_all = DatastreamStreamBackfillAll(**backfill_all)
        if isinstance(backfill_none, dict):
            backfill_none = DatastreamStreamBackfillNone(**backfill_none)
        if isinstance(timeouts, dict):
            timeouts = DatastreamStreamTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010b9566f8020e188444914b63cda5178f17cff35ec3ccd2e68861aaf3a93e42)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination_config", value=destination_config, expected_type=type_hints["destination_config"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument source_config", value=source_config, expected_type=type_hints["source_config"])
            check_type(argname="argument stream_id", value=stream_id, expected_type=type_hints["stream_id"])
            check_type(argname="argument backfill_all", value=backfill_all, expected_type=type_hints["backfill_all"])
            check_type(argname="argument backfill_none", value=backfill_none, expected_type=type_hints["backfill_none"])
            check_type(argname="argument customer_managed_encryption_key", value=customer_managed_encryption_key, expected_type=type_hints["customer_managed_encryption_key"])
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_config": destination_config,
            "display_name": display_name,
            "location": location,
            "source_config": source_config,
            "stream_id": stream_id,
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
        if backfill_all is not None:
            self._values["backfill_all"] = backfill_all
        if backfill_none is not None:
            self._values["backfill_none"] = backfill_none
        if customer_managed_encryption_key is not None:
            self._values["customer_managed_encryption_key"] = customer_managed_encryption_key
        if desired_state is not None:
            self._values["desired_state"] = desired_state
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if project is not None:
            self._values["project"] = project
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
    def destination_config(self) -> "DatastreamStreamDestinationConfig":
        '''destination_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#destination_config DatastreamStream#destination_config}
        '''
        result = self._values.get("destination_config")
        assert result is not None, "Required property 'destination_config' is missing"
        return typing.cast("DatastreamStreamDestinationConfig", result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#display_name DatastreamStream#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this stream is located in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#location DatastreamStream#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_config(self) -> "DatastreamStreamSourceConfig":
        '''source_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#source_config DatastreamStream#source_config}
        '''
        result = self._values.get("source_config")
        assert result is not None, "Required property 'source_config' is missing"
        return typing.cast("DatastreamStreamSourceConfig", result)

    @builtins.property
    def stream_id(self) -> builtins.str:
        '''The stream identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#stream_id DatastreamStream#stream_id}
        '''
        result = self._values.get("stream_id")
        assert result is not None, "Required property 'stream_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backfill_all(self) -> typing.Optional[DatastreamStreamBackfillAll]:
        '''backfill_all block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#backfill_all DatastreamStream#backfill_all}
        '''
        result = self._values.get("backfill_all")
        return typing.cast(typing.Optional[DatastreamStreamBackfillAll], result)

    @builtins.property
    def backfill_none(self) -> typing.Optional[DatastreamStreamBackfillNone]:
        '''backfill_none block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#backfill_none DatastreamStream#backfill_none}
        '''
        result = self._values.get("backfill_none")
        return typing.cast(typing.Optional[DatastreamStreamBackfillNone], result)

    @builtins.property
    def customer_managed_encryption_key(self) -> typing.Optional[builtins.str]:
        '''A reference to a KMS encryption key.

        If provided, it will be used to encrypt the data. If left blank, data
        will be encrypted using an internal Stream-specific encryption key provisioned through KMS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#customer_managed_encryption_key DatastreamStream#customer_managed_encryption_key}
        '''
        result = self._values.get("customer_managed_encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def desired_state(self) -> typing.Optional[builtins.str]:
        '''Desired state of the Stream.

        Set this field to 'RUNNING' to start the stream, and 'PAUSED' to pause the stream.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#desired_state DatastreamStream#desired_state}
        '''
        result = self._values.get("desired_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#id DatastreamStream#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#labels DatastreamStream#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#project DatastreamStream#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DatastreamStreamTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#timeouts DatastreamStream#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DatastreamStreamTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "destination_connection_profile": "destinationConnectionProfile",
        "bigquery_destination_config": "bigqueryDestinationConfig",
        "gcs_destination_config": "gcsDestinationConfig",
    },
)
class DatastreamStreamDestinationConfig:
    def __init__(
        self,
        *,
        destination_connection_profile: builtins.str,
        bigquery_destination_config: typing.Optional[typing.Union["DatastreamStreamDestinationConfigBigqueryDestinationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs_destination_config: typing.Optional[typing.Union["DatastreamStreamDestinationConfigGcsDestinationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param destination_connection_profile: Destination connection profile resource. Format: projects/{project}/locations/{location}/connectionProfiles/{name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#destination_connection_profile DatastreamStream#destination_connection_profile}
        :param bigquery_destination_config: bigquery_destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#bigquery_destination_config DatastreamStream#bigquery_destination_config}
        :param gcs_destination_config: gcs_destination_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#gcs_destination_config DatastreamStream#gcs_destination_config}
        '''
        if isinstance(bigquery_destination_config, dict):
            bigquery_destination_config = DatastreamStreamDestinationConfigBigqueryDestinationConfig(**bigquery_destination_config)
        if isinstance(gcs_destination_config, dict):
            gcs_destination_config = DatastreamStreamDestinationConfigGcsDestinationConfig(**gcs_destination_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f00248466cff6f376a67121eae26291d4773ff89be51d7e77bcce5aef3e183c)
            check_type(argname="argument destination_connection_profile", value=destination_connection_profile, expected_type=type_hints["destination_connection_profile"])
            check_type(argname="argument bigquery_destination_config", value=bigquery_destination_config, expected_type=type_hints["bigquery_destination_config"])
            check_type(argname="argument gcs_destination_config", value=gcs_destination_config, expected_type=type_hints["gcs_destination_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_connection_profile": destination_connection_profile,
        }
        if bigquery_destination_config is not None:
            self._values["bigquery_destination_config"] = bigquery_destination_config
        if gcs_destination_config is not None:
            self._values["gcs_destination_config"] = gcs_destination_config

    @builtins.property
    def destination_connection_profile(self) -> builtins.str:
        '''Destination connection profile resource. Format: projects/{project}/locations/{location}/connectionProfiles/{name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#destination_connection_profile DatastreamStream#destination_connection_profile}
        '''
        result = self._values.get("destination_connection_profile")
        assert result is not None, "Required property 'destination_connection_profile' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bigquery_destination_config(
        self,
    ) -> typing.Optional["DatastreamStreamDestinationConfigBigqueryDestinationConfig"]:
        '''bigquery_destination_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#bigquery_destination_config DatastreamStream#bigquery_destination_config}
        '''
        result = self._values.get("bigquery_destination_config")
        return typing.cast(typing.Optional["DatastreamStreamDestinationConfigBigqueryDestinationConfig"], result)

    @builtins.property
    def gcs_destination_config(
        self,
    ) -> typing.Optional["DatastreamStreamDestinationConfigGcsDestinationConfig"]:
        '''gcs_destination_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#gcs_destination_config DatastreamStream#gcs_destination_config}
        '''
        result = self._values.get("gcs_destination_config")
        return typing.cast(typing.Optional["DatastreamStreamDestinationConfigGcsDestinationConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigBigqueryDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "data_freshness": "dataFreshness",
        "single_target_dataset": "singleTargetDataset",
        "source_hierarchy_datasets": "sourceHierarchyDatasets",
    },
)
class DatastreamStreamDestinationConfigBigqueryDestinationConfig:
    def __init__(
        self,
        *,
        data_freshness: typing.Optional[builtins.str] = None,
        single_target_dataset: typing.Optional[typing.Union["DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset", typing.Dict[builtins.str, typing.Any]]] = None,
        source_hierarchy_datasets: typing.Optional[typing.Union["DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param data_freshness: The guaranteed data freshness (in seconds) when querying tables created by the stream. Editing this field will only affect new tables created in the future, but existing tables will not be impacted. Lower values mean that queries will return fresher data, but may result in higher cost. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Defaults to 900s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_freshness DatastreamStream#data_freshness}
        :param single_target_dataset: single_target_dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#single_target_dataset DatastreamStream#single_target_dataset}
        :param source_hierarchy_datasets: source_hierarchy_datasets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#source_hierarchy_datasets DatastreamStream#source_hierarchy_datasets}
        '''
        if isinstance(single_target_dataset, dict):
            single_target_dataset = DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset(**single_target_dataset)
        if isinstance(source_hierarchy_datasets, dict):
            source_hierarchy_datasets = DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets(**source_hierarchy_datasets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d3281f73805ef674d65a156cd694bf3f6a088663f008143e968719408b4685)
            check_type(argname="argument data_freshness", value=data_freshness, expected_type=type_hints["data_freshness"])
            check_type(argname="argument single_target_dataset", value=single_target_dataset, expected_type=type_hints["single_target_dataset"])
            check_type(argname="argument source_hierarchy_datasets", value=source_hierarchy_datasets, expected_type=type_hints["source_hierarchy_datasets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_freshness is not None:
            self._values["data_freshness"] = data_freshness
        if single_target_dataset is not None:
            self._values["single_target_dataset"] = single_target_dataset
        if source_hierarchy_datasets is not None:
            self._values["source_hierarchy_datasets"] = source_hierarchy_datasets

    @builtins.property
    def data_freshness(self) -> typing.Optional[builtins.str]:
        '''The guaranteed data freshness (in seconds) when querying tables created by the stream.

        Editing this field will only affect new tables created in the future, but existing tables
        will not be impacted. Lower values mean that queries will return fresher data, but may result in higher cost.
        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Defaults to 900s.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_freshness DatastreamStream#data_freshness}
        '''
        result = self._values.get("data_freshness")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def single_target_dataset(
        self,
    ) -> typing.Optional["DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset"]:
        '''single_target_dataset block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#single_target_dataset DatastreamStream#single_target_dataset}
        '''
        result = self._values.get("single_target_dataset")
        return typing.cast(typing.Optional["DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset"], result)

    @builtins.property
    def source_hierarchy_datasets(
        self,
    ) -> typing.Optional["DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets"]:
        '''source_hierarchy_datasets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#source_hierarchy_datasets DatastreamStream#source_hierarchy_datasets}
        '''
        result = self._values.get("source_hierarchy_datasets")
        return typing.cast(typing.Optional["DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamDestinationConfigBigqueryDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamDestinationConfigBigqueryDestinationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigBigqueryDestinationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7a8b609b22768f789ea3611aa0ef25787c5d73f4a59a9be4ef77efa3c492a81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSingleTargetDataset")
    def put_single_target_dataset(self, *, dataset_id: builtins.str) -> None:
        '''
        :param dataset_id: Dataset ID in the format projects/{project}/datasets/{dataset_id} or {project}:{dataset_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#dataset_id DatastreamStream#dataset_id}
        '''
        value = DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset(
            dataset_id=dataset_id
        )

        return typing.cast(None, jsii.invoke(self, "putSingleTargetDataset", [value]))

    @jsii.member(jsii_name="putSourceHierarchyDatasets")
    def put_source_hierarchy_datasets(
        self,
        *,
        dataset_template: typing.Union["DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param dataset_template: dataset_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#dataset_template DatastreamStream#dataset_template}
        '''
        value = DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets(
            dataset_template=dataset_template
        )

        return typing.cast(None, jsii.invoke(self, "putSourceHierarchyDatasets", [value]))

    @jsii.member(jsii_name="resetDataFreshness")
    def reset_data_freshness(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataFreshness", []))

    @jsii.member(jsii_name="resetSingleTargetDataset")
    def reset_single_target_dataset(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSingleTargetDataset", []))

    @jsii.member(jsii_name="resetSourceHierarchyDatasets")
    def reset_source_hierarchy_datasets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceHierarchyDatasets", []))

    @builtins.property
    @jsii.member(jsii_name="singleTargetDataset")
    def single_target_dataset(
        self,
    ) -> "DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDatasetOutputReference":
        return typing.cast("DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDatasetOutputReference", jsii.get(self, "singleTargetDataset"))

    @builtins.property
    @jsii.member(jsii_name="sourceHierarchyDatasets")
    def source_hierarchy_datasets(
        self,
    ) -> "DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsOutputReference":
        return typing.cast("DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsOutputReference", jsii.get(self, "sourceHierarchyDatasets"))

    @builtins.property
    @jsii.member(jsii_name="dataFreshnessInput")
    def data_freshness_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataFreshnessInput"))

    @builtins.property
    @jsii.member(jsii_name="singleTargetDatasetInput")
    def single_target_dataset_input(
        self,
    ) -> typing.Optional["DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset"]:
        return typing.cast(typing.Optional["DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset"], jsii.get(self, "singleTargetDatasetInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceHierarchyDatasetsInput")
    def source_hierarchy_datasets_input(
        self,
    ) -> typing.Optional["DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets"]:
        return typing.cast(typing.Optional["DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets"], jsii.get(self, "sourceHierarchyDatasetsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataFreshness")
    def data_freshness(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataFreshness"))

    @data_freshness.setter
    def data_freshness(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b7da575aade1c71be6745c30a44eae934f6539e34ccd51a86b8facf00d5060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataFreshness", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfig]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10290314eb6f6d825712b6b3207d7da992e62e51fc0be399239f7e7d53e2f846)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset",
    jsii_struct_bases=[],
    name_mapping={"dataset_id": "datasetId"},
)
class DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset:
    def __init__(self, *, dataset_id: builtins.str) -> None:
        '''
        :param dataset_id: Dataset ID in the format projects/{project}/datasets/{dataset_id} or {project}:{dataset_id}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#dataset_id DatastreamStream#dataset_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e44dd24643e8aa60468a62619c2ae48ae367e05d23c573afcfa2a6d3a4c91dd)
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
        }

    @builtins.property
    def dataset_id(self) -> builtins.str:
        '''Dataset ID in the format projects/{project}/datasets/{dataset_id} or {project}:{dataset_id}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#dataset_id DatastreamStream#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDatasetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDatasetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__441adf3b7f63f750260d12b3416082c5faf64d5c7e1832c2a1046cb0a48d5538)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51999bc75c9b0fd3a12023b18a370bbc03175387133548ee3a57791a877640d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__268f1df491bfb370cbc33b522997f6031a2165748ce5ce4e0e09666537abd721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets",
    jsii_struct_bases=[],
    name_mapping={"dataset_template": "datasetTemplate"},
)
class DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets:
    def __init__(
        self,
        *,
        dataset_template: typing.Union["DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param dataset_template: dataset_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#dataset_template DatastreamStream#dataset_template}
        '''
        if isinstance(dataset_template, dict):
            dataset_template = DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate(**dataset_template)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d309147145fe77e14e6be2ec7f8089a10173d914dfbdb30bdc6fed0fd183a299)
            check_type(argname="argument dataset_template", value=dataset_template, expected_type=type_hints["dataset_template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_template": dataset_template,
        }

    @builtins.property
    def dataset_template(
        self,
    ) -> "DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate":
        '''dataset_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#dataset_template DatastreamStream#dataset_template}
        '''
        result = self._values.get("dataset_template")
        assert result is not None, "Required property 'dataset_template' is missing"
        return typing.cast("DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "dataset_id_prefix": "datasetIdPrefix",
        "kms_key_name": "kmsKeyName",
    },
)
class DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate:
    def __init__(
        self,
        *,
        location: builtins.str,
        dataset_id_prefix: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: The geographic location where the dataset should reside. See https://cloud.google.com/bigquery/docs/locations for supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#location DatastreamStream#location}
        :param dataset_id_prefix: If supplied, every created dataset will have its name prefixed by the provided value. The prefix and name will be separated by an underscore. i.e. _. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#dataset_id_prefix DatastreamStream#dataset_id_prefix}
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table. The BigQuery Service Account associated with your project requires access to this encryption key. i.e. projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{cryptoKey}. See https://cloud.google.com/bigquery/docs/customer-managed-encryption for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#kms_key_name DatastreamStream#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21923ae44eb0f0bb463b3690f3b8ab6ee48575a23420bfc03244d26df8ce50fc)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument dataset_id_prefix", value=dataset_id_prefix, expected_type=type_hints["dataset_id_prefix"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
        }
        if dataset_id_prefix is not None:
            self._values["dataset_id_prefix"] = dataset_id_prefix
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def location(self) -> builtins.str:
        '''The geographic location where the dataset should reside. See https://cloud.google.com/bigquery/docs/locations for supported locations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#location DatastreamStream#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dataset_id_prefix(self) -> typing.Optional[builtins.str]:
        '''If supplied, every created dataset will have its name prefixed by the provided value.

        The prefix and name will be separated by an underscore. i.e. _.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#dataset_id_prefix DatastreamStream#dataset_id_prefix}
        '''
        result = self._values.get("dataset_id_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table.

        The BigQuery Service Account associated with your project requires access to this
        encryption key. i.e. projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{cryptoKey}.
        See https://cloud.google.com/bigquery/docs/customer-managed-encryption for more information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#kms_key_name DatastreamStream#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f3e1a71a02260fed7254d25a21729daa348bde759c05a201e378a1427397ba5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDatasetIdPrefix")
    def reset_dataset_id_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatasetIdPrefix", []))

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @builtins.property
    @jsii.member(jsii_name="datasetIdPrefixInput")
    def dataset_id_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetIdPrefix")
    def dataset_id_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetIdPrefix"))

    @dataset_id_prefix.setter
    def dataset_id_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12137ad883f1e8198a7e8a9d33112667f3a9d542fe239263ff41c443ac959f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetIdPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2910e29339383be80b9bf3b4860a08c50c3fbf66efb48048711d4a03177ae393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f6a99aaed1e86235d35130b250c4ef94bbb8b532409fcb8b414027c2e8f90f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d649ea10fa687d496860280b0eb24cd52cc782d27783590f0680bfa4689aa1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57dd2ede080c713c2f1230e7c848e67a25284bcfc9dddcff5c0399b99b877959)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDatasetTemplate")
    def put_dataset_template(
        self,
        *,
        location: builtins.str,
        dataset_id_prefix: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: The geographic location where the dataset should reside. See https://cloud.google.com/bigquery/docs/locations for supported locations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#location DatastreamStream#location}
        :param dataset_id_prefix: If supplied, every created dataset will have its name prefixed by the provided value. The prefix and name will be separated by an underscore. i.e. _. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#dataset_id_prefix DatastreamStream#dataset_id_prefix}
        :param kms_key_name: Describes the Cloud KMS encryption key that will be used to protect destination BigQuery table. The BigQuery Service Account associated with your project requires access to this encryption key. i.e. projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{cryptoKey}. See https://cloud.google.com/bigquery/docs/customer-managed-encryption for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#kms_key_name DatastreamStream#kms_key_name}
        '''
        value = DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate(
            location=location,
            dataset_id_prefix=dataset_id_prefix,
            kms_key_name=kms_key_name,
        )

        return typing.cast(None, jsii.invoke(self, "putDatasetTemplate", [value]))

    @builtins.property
    @jsii.member(jsii_name="datasetTemplate")
    def dataset_template(
        self,
    ) -> DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplateOutputReference:
        return typing.cast(DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplateOutputReference, jsii.get(self, "datasetTemplate"))

    @builtins.property
    @jsii.member(jsii_name="datasetTemplateInput")
    def dataset_template_input(
        self,
    ) -> typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate], jsii.get(self, "datasetTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca05e8ee9521ac9812e47448dd7ed280d2aded497ee45b96dd7daca59deabbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigGcsDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "avro_file_format": "avroFileFormat",
        "file_rotation_interval": "fileRotationInterval",
        "file_rotation_mb": "fileRotationMb",
        "json_file_format": "jsonFileFormat",
        "path": "path",
    },
)
class DatastreamStreamDestinationConfigGcsDestinationConfig:
    def __init__(
        self,
        *,
        avro_file_format: typing.Optional[typing.Union["DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        file_rotation_interval: typing.Optional[builtins.str] = None,
        file_rotation_mb: typing.Optional[jsii.Number] = None,
        json_file_format: typing.Optional[typing.Union["DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param avro_file_format: avro_file_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#avro_file_format DatastreamStream#avro_file_format}
        :param file_rotation_interval: The maximum duration for which new events are added before a file is closed and a new file is created. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Defaults to 900s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#file_rotation_interval DatastreamStream#file_rotation_interval}
        :param file_rotation_mb: The maximum file size to be saved in the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#file_rotation_mb DatastreamStream#file_rotation_mb}
        :param json_file_format: json_file_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#json_file_format DatastreamStream#json_file_format}
        :param path: Path inside the Cloud Storage bucket to write data to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#path DatastreamStream#path}
        '''
        if isinstance(avro_file_format, dict):
            avro_file_format = DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat(**avro_file_format)
        if isinstance(json_file_format, dict):
            json_file_format = DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat(**json_file_format)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6fe7bc7051957d6ef5b4a2c8ba1b43b7844b9948287f7a5f36e8a41e8cc412)
            check_type(argname="argument avro_file_format", value=avro_file_format, expected_type=type_hints["avro_file_format"])
            check_type(argname="argument file_rotation_interval", value=file_rotation_interval, expected_type=type_hints["file_rotation_interval"])
            check_type(argname="argument file_rotation_mb", value=file_rotation_mb, expected_type=type_hints["file_rotation_mb"])
            check_type(argname="argument json_file_format", value=json_file_format, expected_type=type_hints["json_file_format"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if avro_file_format is not None:
            self._values["avro_file_format"] = avro_file_format
        if file_rotation_interval is not None:
            self._values["file_rotation_interval"] = file_rotation_interval
        if file_rotation_mb is not None:
            self._values["file_rotation_mb"] = file_rotation_mb
        if json_file_format is not None:
            self._values["json_file_format"] = json_file_format
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def avro_file_format(
        self,
    ) -> typing.Optional["DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat"]:
        '''avro_file_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#avro_file_format DatastreamStream#avro_file_format}
        '''
        result = self._values.get("avro_file_format")
        return typing.cast(typing.Optional["DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat"], result)

    @builtins.property
    def file_rotation_interval(self) -> typing.Optional[builtins.str]:
        '''The maximum duration for which new events are added before a file is closed and a new file is created.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Defaults to 900s.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#file_rotation_interval DatastreamStream#file_rotation_interval}
        '''
        result = self._values.get("file_rotation_interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_rotation_mb(self) -> typing.Optional[jsii.Number]:
        '''The maximum file size to be saved in the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#file_rotation_mb DatastreamStream#file_rotation_mb}
        '''
        result = self._values.get("file_rotation_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def json_file_format(
        self,
    ) -> typing.Optional["DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat"]:
        '''json_file_format block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#json_file_format DatastreamStream#json_file_format}
        '''
        result = self._values.get("json_file_format")
        return typing.cast(typing.Optional["DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path inside the Cloud Storage bucket to write data to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#path DatastreamStream#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamDestinationConfigGcsDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat",
    jsii_struct_bases=[],
    name_mapping={},
)
class DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53992334d0a36b22747670910ec781eeb695714367669655fdf9bf4af1963833)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afaa1094b2bf96eb2aaa9a004fc98a4308a6190a94060ab74654bb2b416c437a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat",
    jsii_struct_bases=[],
    name_mapping={
        "compression": "compression",
        "schema_file_format": "schemaFileFormat",
    },
)
class DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat:
    def __init__(
        self,
        *,
        compression: typing.Optional[builtins.str] = None,
        schema_file_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compression: Compression of the loaded JSON file. Possible values: ["NO_COMPRESSION", "GZIP"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#compression DatastreamStream#compression}
        :param schema_file_format: The schema file format along JSON data files. Possible values: ["NO_SCHEMA_FILE", "AVRO_SCHEMA_FILE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema_file_format DatastreamStream#schema_file_format}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c14e2cab90478a730fd4d9ac6ca6c8d7ba3f67ff802f4dcd2d5c9c08fb9803)
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument schema_file_format", value=schema_file_format, expected_type=type_hints["schema_file_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compression is not None:
            self._values["compression"] = compression
        if schema_file_format is not None:
            self._values["schema_file_format"] = schema_file_format

    @builtins.property
    def compression(self) -> typing.Optional[builtins.str]:
        '''Compression of the loaded JSON file. Possible values: ["NO_COMPRESSION", "GZIP"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#compression DatastreamStream#compression}
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_file_format(self) -> typing.Optional[builtins.str]:
        '''The schema file format along JSON data files. Possible values: ["NO_SCHEMA_FILE", "AVRO_SCHEMA_FILE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema_file_format DatastreamStream#schema_file_format}
        '''
        result = self._values.get("schema_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormatOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormatOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03cf334b7c9b733612b8ea0e5a5a7807c143ca675f4524c8a5e0e7755406bd56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCompression")
    def reset_compression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompression", []))

    @jsii.member(jsii_name="resetSchemaFileFormat")
    def reset_schema_file_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaFileFormat", []))

    @builtins.property
    @jsii.member(jsii_name="compressionInput")
    def compression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaFileFormatInput")
    def schema_file_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaFileFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ded649c1e18a3afe723a46d8ef0cf7b3bd23261d1183fd169e1f378122c2eef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value)

    @builtins.property
    @jsii.member(jsii_name="schemaFileFormat")
    def schema_file_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaFileFormat"))

    @schema_file_format.setter
    def schema_file_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4267f271d814121eca55dad65d9c3869f72e7c0df0c37798d71a0517c8e56d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaFileFormat", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69a0efe2299c605431235b27746ddef41abdcec0e56eac6382ae8204a6a451f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamDestinationConfigGcsDestinationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigGcsDestinationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db9a6d5e7f6df721016eecca5688540ca539f31acd6bda59a8493f4c20acd453)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAvroFileFormat")
    def put_avro_file_format(self) -> None:
        value = DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat()

        return typing.cast(None, jsii.invoke(self, "putAvroFileFormat", [value]))

    @jsii.member(jsii_name="putJsonFileFormat")
    def put_json_file_format(
        self,
        *,
        compression: typing.Optional[builtins.str] = None,
        schema_file_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compression: Compression of the loaded JSON file. Possible values: ["NO_COMPRESSION", "GZIP"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#compression DatastreamStream#compression}
        :param schema_file_format: The schema file format along JSON data files. Possible values: ["NO_SCHEMA_FILE", "AVRO_SCHEMA_FILE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema_file_format DatastreamStream#schema_file_format}
        '''
        value = DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat(
            compression=compression, schema_file_format=schema_file_format
        )

        return typing.cast(None, jsii.invoke(self, "putJsonFileFormat", [value]))

    @jsii.member(jsii_name="resetAvroFileFormat")
    def reset_avro_file_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvroFileFormat", []))

    @jsii.member(jsii_name="resetFileRotationInterval")
    def reset_file_rotation_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileRotationInterval", []))

    @jsii.member(jsii_name="resetFileRotationMb")
    def reset_file_rotation_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileRotationMb", []))

    @jsii.member(jsii_name="resetJsonFileFormat")
    def reset_json_file_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJsonFileFormat", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="avroFileFormat")
    def avro_file_format(
        self,
    ) -> DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormatOutputReference:
        return typing.cast(DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormatOutputReference, jsii.get(self, "avroFileFormat"))

    @builtins.property
    @jsii.member(jsii_name="jsonFileFormat")
    def json_file_format(
        self,
    ) -> DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormatOutputReference:
        return typing.cast(DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormatOutputReference, jsii.get(self, "jsonFileFormat"))

    @builtins.property
    @jsii.member(jsii_name="avroFileFormatInput")
    def avro_file_format_input(
        self,
    ) -> typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat], jsii.get(self, "avroFileFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="fileRotationIntervalInput")
    def file_rotation_interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileRotationIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="fileRotationMbInput")
    def file_rotation_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fileRotationMbInput"))

    @builtins.property
    @jsii.member(jsii_name="jsonFileFormatInput")
    def json_file_format_input(
        self,
    ) -> typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat], jsii.get(self, "jsonFileFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="fileRotationInterval")
    def file_rotation_interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileRotationInterval"))

    @file_rotation_interval.setter
    def file_rotation_interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97148b45365aadc2e39b6e2e4fccc374cdbca79b05f3f52571e08319d4ee9036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileRotationInterval", value)

    @builtins.property
    @jsii.member(jsii_name="fileRotationMb")
    def file_rotation_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fileRotationMb"))

    @file_rotation_mb.setter
    def file_rotation_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae1649d074402474b5d7bd00712aabfc874730cfff03823ae354457233f2608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileRotationMb", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f182119df80ece606c9383959c86ab83e4448a8f8744859baad283fd405e45d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfig]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f01a9c52ede76f92056982b7da315f974384e0fb43ded2f1d40f4d8e1832207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamDestinationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamDestinationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f46069e1a4d2de7a3c29ede9cae6610ea00fcde99ec2ae63eab68dc303a751c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBigqueryDestinationConfig")
    def put_bigquery_destination_config(
        self,
        *,
        data_freshness: typing.Optional[builtins.str] = None,
        single_target_dataset: typing.Optional[typing.Union[DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset, typing.Dict[builtins.str, typing.Any]]] = None,
        source_hierarchy_datasets: typing.Optional[typing.Union[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param data_freshness: The guaranteed data freshness (in seconds) when querying tables created by the stream. Editing this field will only affect new tables created in the future, but existing tables will not be impacted. Lower values mean that queries will return fresher data, but may result in higher cost. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Defaults to 900s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_freshness DatastreamStream#data_freshness}
        :param single_target_dataset: single_target_dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#single_target_dataset DatastreamStream#single_target_dataset}
        :param source_hierarchy_datasets: source_hierarchy_datasets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#source_hierarchy_datasets DatastreamStream#source_hierarchy_datasets}
        '''
        value = DatastreamStreamDestinationConfigBigqueryDestinationConfig(
            data_freshness=data_freshness,
            single_target_dataset=single_target_dataset,
            source_hierarchy_datasets=source_hierarchy_datasets,
        )

        return typing.cast(None, jsii.invoke(self, "putBigqueryDestinationConfig", [value]))

    @jsii.member(jsii_name="putGcsDestinationConfig")
    def put_gcs_destination_config(
        self,
        *,
        avro_file_format: typing.Optional[typing.Union[DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat, typing.Dict[builtins.str, typing.Any]]] = None,
        file_rotation_interval: typing.Optional[builtins.str] = None,
        file_rotation_mb: typing.Optional[jsii.Number] = None,
        json_file_format: typing.Optional[typing.Union[DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat, typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param avro_file_format: avro_file_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#avro_file_format DatastreamStream#avro_file_format}
        :param file_rotation_interval: The maximum duration for which new events are added before a file is closed and a new file is created. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Defaults to 900s. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#file_rotation_interval DatastreamStream#file_rotation_interval}
        :param file_rotation_mb: The maximum file size to be saved in the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#file_rotation_mb DatastreamStream#file_rotation_mb}
        :param json_file_format: json_file_format block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#json_file_format DatastreamStream#json_file_format}
        :param path: Path inside the Cloud Storage bucket to write data to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#path DatastreamStream#path}
        '''
        value = DatastreamStreamDestinationConfigGcsDestinationConfig(
            avro_file_format=avro_file_format,
            file_rotation_interval=file_rotation_interval,
            file_rotation_mb=file_rotation_mb,
            json_file_format=json_file_format,
            path=path,
        )

        return typing.cast(None, jsii.invoke(self, "putGcsDestinationConfig", [value]))

    @jsii.member(jsii_name="resetBigqueryDestinationConfig")
    def reset_bigquery_destination_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryDestinationConfig", []))

    @jsii.member(jsii_name="resetGcsDestinationConfig")
    def reset_gcs_destination_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcsDestinationConfig", []))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDestinationConfig")
    def bigquery_destination_config(
        self,
    ) -> DatastreamStreamDestinationConfigBigqueryDestinationConfigOutputReference:
        return typing.cast(DatastreamStreamDestinationConfigBigqueryDestinationConfigOutputReference, jsii.get(self, "bigqueryDestinationConfig"))

    @builtins.property
    @jsii.member(jsii_name="gcsDestinationConfig")
    def gcs_destination_config(
        self,
    ) -> DatastreamStreamDestinationConfigGcsDestinationConfigOutputReference:
        return typing.cast(DatastreamStreamDestinationConfigGcsDestinationConfigOutputReference, jsii.get(self, "gcsDestinationConfig"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDestinationConfigInput")
    def bigquery_destination_config_input(
        self,
    ) -> typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfig]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfig], jsii.get(self, "bigqueryDestinationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationConnectionProfileInput")
    def destination_connection_profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationConnectionProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsDestinationConfigInput")
    def gcs_destination_config_input(
        self,
    ) -> typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfig]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfig], jsii.get(self, "gcsDestinationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationConnectionProfile")
    def destination_connection_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationConnectionProfile"))

    @destination_connection_profile.setter
    def destination_connection_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c51932c7c579a452dfb4bd688f68fa8208002be445062eda4e86430be29b96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationConnectionProfile", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DatastreamStreamDestinationConfig]:
        return typing.cast(typing.Optional[DatastreamStreamDestinationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamDestinationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c94d7479b7d04eadd4b49a8a517d1d766123d5a712238cd25314c50439da47d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "source_connection_profile": "sourceConnectionProfile",
        "mysql_source_config": "mysqlSourceConfig",
        "oracle_source_config": "oracleSourceConfig",
        "postgresql_source_config": "postgresqlSourceConfig",
    },
)
class DatastreamStreamSourceConfig:
    def __init__(
        self,
        *,
        source_connection_profile: builtins.str,
        mysql_source_config: typing.Optional[typing.Union["DatastreamStreamSourceConfigMysqlSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        oracle_source_config: typing.Optional[typing.Union["DatastreamStreamSourceConfigOracleSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        postgresql_source_config: typing.Optional[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param source_connection_profile: Source connection profile resource. Format: projects/{project}/locations/{location}/connectionProfiles/{name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#source_connection_profile DatastreamStream#source_connection_profile}
        :param mysql_source_config: mysql_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_source_config DatastreamStream#mysql_source_config}
        :param oracle_source_config: oracle_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_source_config DatastreamStream#oracle_source_config}
        :param postgresql_source_config: postgresql_source_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_source_config DatastreamStream#postgresql_source_config}
        '''
        if isinstance(mysql_source_config, dict):
            mysql_source_config = DatastreamStreamSourceConfigMysqlSourceConfig(**mysql_source_config)
        if isinstance(oracle_source_config, dict):
            oracle_source_config = DatastreamStreamSourceConfigOracleSourceConfig(**oracle_source_config)
        if isinstance(postgresql_source_config, dict):
            postgresql_source_config = DatastreamStreamSourceConfigPostgresqlSourceConfig(**postgresql_source_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995aa3d40c0014eb42472704f6e2a586227929c23daf612b5bc02630f522ee9c)
            check_type(argname="argument source_connection_profile", value=source_connection_profile, expected_type=type_hints["source_connection_profile"])
            check_type(argname="argument mysql_source_config", value=mysql_source_config, expected_type=type_hints["mysql_source_config"])
            check_type(argname="argument oracle_source_config", value=oracle_source_config, expected_type=type_hints["oracle_source_config"])
            check_type(argname="argument postgresql_source_config", value=postgresql_source_config, expected_type=type_hints["postgresql_source_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_connection_profile": source_connection_profile,
        }
        if mysql_source_config is not None:
            self._values["mysql_source_config"] = mysql_source_config
        if oracle_source_config is not None:
            self._values["oracle_source_config"] = oracle_source_config
        if postgresql_source_config is not None:
            self._values["postgresql_source_config"] = postgresql_source_config

    @builtins.property
    def source_connection_profile(self) -> builtins.str:
        '''Source connection profile resource. Format: projects/{project}/locations/{location}/connectionProfiles/{name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#source_connection_profile DatastreamStream#source_connection_profile}
        '''
        result = self._values.get("source_connection_profile")
        assert result is not None, "Required property 'source_connection_profile' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mysql_source_config(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigMysqlSourceConfig"]:
        '''mysql_source_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_source_config DatastreamStream#mysql_source_config}
        '''
        result = self._values.get("mysql_source_config")
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigMysqlSourceConfig"], result)

    @builtins.property
    def oracle_source_config(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigOracleSourceConfig"]:
        '''oracle_source_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_source_config DatastreamStream#oracle_source_config}
        '''
        result = self._values.get("oracle_source_config")
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigOracleSourceConfig"], result)

    @builtins.property
    def postgresql_source_config(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigPostgresqlSourceConfig"]:
        '''postgresql_source_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_source_config DatastreamStream#postgresql_source_config}
        '''
        result = self._values.get("postgresql_source_config")
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigPostgresqlSourceConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_objects": "excludeObjects",
        "include_objects": "includeObjects",
        "max_concurrent_backfill_tasks": "maxConcurrentBackfillTasks",
        "max_concurrent_cdc_tasks": "maxConcurrentCdcTasks",
    },
)
class DatastreamStreamSourceConfigMysqlSourceConfig:
    def __init__(
        self,
        *,
        exclude_objects: typing.Optional[typing.Union["DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        include_objects: typing.Optional[typing.Union["DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        max_concurrent_backfill_tasks: typing.Optional[jsii.Number] = None,
        max_concurrent_cdc_tasks: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exclude_objects: exclude_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#exclude_objects DatastreamStream#exclude_objects}
        :param include_objects: include_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#include_objects DatastreamStream#include_objects}
        :param max_concurrent_backfill_tasks: Maximum number of concurrent backfill tasks. The number should be non negative. If not set (or set to 0), the system's default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_backfill_tasks DatastreamStream#max_concurrent_backfill_tasks}
        :param max_concurrent_cdc_tasks: Maximum number of concurrent CDC tasks. The number should be non negative. If not set (or set to 0), the system's default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_cdc_tasks DatastreamStream#max_concurrent_cdc_tasks}
        '''
        if isinstance(exclude_objects, dict):
            exclude_objects = DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects(**exclude_objects)
        if isinstance(include_objects, dict):
            include_objects = DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects(**include_objects)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03986ed8942ca5af140f857a63fa4f9bf36dc4bc0034824c870a09ee77f3377f)
            check_type(argname="argument exclude_objects", value=exclude_objects, expected_type=type_hints["exclude_objects"])
            check_type(argname="argument include_objects", value=include_objects, expected_type=type_hints["include_objects"])
            check_type(argname="argument max_concurrent_backfill_tasks", value=max_concurrent_backfill_tasks, expected_type=type_hints["max_concurrent_backfill_tasks"])
            check_type(argname="argument max_concurrent_cdc_tasks", value=max_concurrent_cdc_tasks, expected_type=type_hints["max_concurrent_cdc_tasks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_objects is not None:
            self._values["exclude_objects"] = exclude_objects
        if include_objects is not None:
            self._values["include_objects"] = include_objects
        if max_concurrent_backfill_tasks is not None:
            self._values["max_concurrent_backfill_tasks"] = max_concurrent_backfill_tasks
        if max_concurrent_cdc_tasks is not None:
            self._values["max_concurrent_cdc_tasks"] = max_concurrent_cdc_tasks

    @builtins.property
    def exclude_objects(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects"]:
        '''exclude_objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#exclude_objects DatastreamStream#exclude_objects}
        '''
        result = self._values.get("exclude_objects")
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects"], result)

    @builtins.property
    def include_objects(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects"]:
        '''include_objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#include_objects DatastreamStream#include_objects}
        '''
        result = self._values.get("include_objects")
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects"], result)

    @builtins.property
    def max_concurrent_backfill_tasks(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of concurrent backfill tasks.

        The number should be non negative.
        If not set (or set to 0), the system's default value will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_backfill_tasks DatastreamStream#max_concurrent_backfill_tasks}
        '''
        result = self._values.get("max_concurrent_backfill_tasks")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_concurrent_cdc_tasks(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of concurrent CDC tasks.

        The number should be non negative.
        If not set (or set to 0), the system's default value will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_cdc_tasks DatastreamStream#max_concurrent_cdc_tasks}
        '''
        result = self._values.get("max_concurrent_cdc_tasks")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigMysqlSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects",
    jsii_struct_bases=[],
    name_mapping={"mysql_databases": "mysqlDatabases"},
)
class DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects:
    def __init__(
        self,
        *,
        mysql_databases: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param mysql_databases: mysql_databases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_databases DatastreamStream#mysql_databases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8924ba08b53e76420d1040aea7107d9f8f4a35a42d203306a4dc5eef847746)
            check_type(argname="argument mysql_databases", value=mysql_databases, expected_type=type_hints["mysql_databases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mysql_databases": mysql_databases,
        }

    @builtins.property
    def mysql_databases(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases"]]:
        '''mysql_databases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_databases DatastreamStream#mysql_databases}
        '''
        result = self._values.get("mysql_databases")
        assert result is not None, "Required property 'mysql_databases' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "mysql_tables": "mysqlTables"},
)
class DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases:
    def __init__(
        self,
        *,
        database: builtins.str,
        mysql_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param database: Database name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#database DatastreamStream#database}
        :param mysql_tables: mysql_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_tables DatastreamStream#mysql_tables}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47003e7f3dfe4568bdfbecbecdfeca8cc5c1dc824fd507147bcf69d0e11c8907)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument mysql_tables", value=mysql_tables, expected_type=type_hints["mysql_tables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
        }
        if mysql_tables is not None:
            self._values["mysql_tables"] = mysql_tables

    @builtins.property
    def database(self) -> builtins.str:
        '''Database name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#database DatastreamStream#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mysql_tables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables"]]]:
        '''mysql_tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_tables DatastreamStream#mysql_tables}
        '''
        result = self._values.get("mysql_tables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ad30ac80003dfb56e29240af179446ad988b2d56141cc9ac9173a417b271330)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e3be48b4d7ea91ea507468b666eb92e908b90eaa4b72909e6e563ba639959a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d098f2c688f84fafc6dd0afd35bf6d5c61a2a9469a607a83c9f3adea7ec6a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af2024f15ee7b08a23d14347a6bf4886348cdd4fe08b134d84d142af2d64b50b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87c0d3373e4a860d69ba9b1b96343c0a1a37400cad0c26a35d9976a03a2abbcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2195e2190f719cbe019609d3ec53f80debd66c7511eec9350b50efae0d491363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables",
    jsii_struct_bases=[],
    name_mapping={"table": "table", "mysql_columns": "mysqlColumns"},
)
class DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables:
    def __init__(
        self,
        *,
        table: builtins.str,
        mysql_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param table: Table name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        :param mysql_columns: mysql_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_columns DatastreamStream#mysql_columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36fef275c6ec7b8d609cafa0d2641bd263c44a10bc7249473f713a05683ba4f4)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument mysql_columns", value=mysql_columns, expected_type=type_hints["mysql_columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if mysql_columns is not None:
            self._values["mysql_columns"] = mysql_columns

    @builtins.property
    def table(self) -> builtins.str:
        '''Table name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mysql_columns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns"]]]:
        '''mysql_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_columns DatastreamStream#mysql_columns}
        '''
        result = self._values.get("mysql_columns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69c33a987c9a7ecb67924cb1032a96cc931edf369e360ae95e58e1551d69b163)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2137ca458d7db27e59eaa11790cf81f0760027a1075e78cbd3fd912b7fdbfe53)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b152c3de915d6fc96d08112f4da3d2632e4a1feb8ed9a6e739b1e322d056eba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9761d0c70fb470dda84cafcf21d16c981695392477d4566b2b58631c6a17a85c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e35fc4adff6fe3aeb36b4c144ff1bef8d8bfec907ca5fe8808db292d4698d710)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3b7e194a1b17a44374dff58788f3134ef276f1b232460d9f088bc36c194fbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns",
    jsii_struct_bases=[],
    name_mapping={
        "collation": "collation",
        "column": "column",
        "data_type": "dataType",
        "nullable": "nullable",
        "ordinal_position": "ordinalPosition",
        "primary_key": "primaryKey",
    },
)
class DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns:
    def __init__(
        self,
        *,
        collation: typing.Optional[builtins.str] = None,
        column: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ordinal_position: typing.Optional[jsii.Number] = None,
        primary_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param collation: Column collation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#collation DatastreamStream#collation}
        :param column: Column name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        :param data_type: The MySQL data type. Full data types list can be found here: https://dev.mysql.com/doc/refman/8.0/en/data-types.html. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        :param nullable: Whether or not the column can accept a null value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#nullable DatastreamStream#nullable}
        :param ordinal_position: The ordinal position of the column in the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#ordinal_position DatastreamStream#ordinal_position}
        :param primary_key: Whether or not the column represents a primary key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#primary_key DatastreamStream#primary_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1d840e397f01a70c2cddb58c957e80c59d39fb16bbea2a1c04910d8abb0218)
            check_type(argname="argument collation", value=collation, expected_type=type_hints["collation"])
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument nullable", value=nullable, expected_type=type_hints["nullable"])
            check_type(argname="argument ordinal_position", value=ordinal_position, expected_type=type_hints["ordinal_position"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if collation is not None:
            self._values["collation"] = collation
        if column is not None:
            self._values["column"] = column
        if data_type is not None:
            self._values["data_type"] = data_type
        if nullable is not None:
            self._values["nullable"] = nullable
        if ordinal_position is not None:
            self._values["ordinal_position"] = ordinal_position
        if primary_key is not None:
            self._values["primary_key"] = primary_key

    @builtins.property
    def collation(self) -> typing.Optional[builtins.str]:
        '''Column collation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#collation DatastreamStream#collation}
        '''
        result = self._values.get("collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def column(self) -> typing.Optional[builtins.str]:
        '''Column name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        '''
        result = self._values.get("column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''The MySQL data type. Full data types list can be found here: https://dev.mysql.com/doc/refman/8.0/en/data-types.html.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nullable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the column can accept a null value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#nullable DatastreamStream#nullable}
        '''
        result = self._values.get("nullable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ordinal_position(self) -> typing.Optional[jsii.Number]:
        '''The ordinal position of the column in the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#ordinal_position DatastreamStream#ordinal_position}
        '''
        result = self._values.get("ordinal_position")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the column represents a primary key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#primary_key DatastreamStream#primary_key}
        '''
        result = self._values.get("primary_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b934e1cd2f1b6e46749d3a3ee4ea123a5feab018bcbd9e1dc3d82577fc52b54d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b0462a33c37e557fcf3c2fd74887a5508dff56bcde35fa593f04f4b8607580c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b5fb04fe528246556f11f40ffb8e2ce0da1af40d4741f1ba0bc113654bb796)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30ff55614afd8ecea5a474c3db78ec06d5d81fc6e8371a0cc4fb16372f124bf1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad32f42f77fac61d1715b212cb332883b311819b8cd438d36beb15bde86030dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9320334886970de6c5ea55c48a2818daa32156be2f9f75dd5e042a36ad100d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bc27762ed3847a2a4997c6417d746b2344e6ce7b9e40d4295c780394da67d35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCollation")
    def reset_collation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollation", []))

    @jsii.member(jsii_name="resetColumn")
    def reset_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumn", []))

    @jsii.member(jsii_name="resetDataType")
    def reset_data_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataType", []))

    @jsii.member(jsii_name="resetNullable")
    def reset_nullable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullable", []))

    @jsii.member(jsii_name="resetOrdinalPosition")
    def reset_ordinal_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrdinalPosition", []))

    @jsii.member(jsii_name="resetPrimaryKey")
    def reset_primary_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryKey", []))

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "length"))

    @builtins.property
    @jsii.member(jsii_name="collationInput")
    def collation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collationInput"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypeInput")
    def data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nullableInput")
    def nullable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nullableInput"))

    @builtins.property
    @jsii.member(jsii_name="ordinalPositionInput")
    def ordinal_position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ordinalPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeyInput")
    def primary_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="collation")
    def collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collation"))

    @collation.setter
    def collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10c35f21ec76d9b9b6f802e3565c8ba67ffd07a03db61a1a05cab01b31b5cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collation", value)

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "column"))

    @column.setter
    def column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e84862d7e010156638f260885c74211c45e9be7238c8249465e6db2a06d368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a4831ac66409ce770fc99b6de33638206edf8c50979ecf8d0cc42c7b84f450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="nullable")
    def nullable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nullable"))

    @nullable.setter
    def nullable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600dbdaafece9c5dbfc122b3a1509faf6dc3db4dd21050d0da9936f77db7d0e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullable", value)

    @builtins.property
    @jsii.member(jsii_name="ordinalPosition")
    def ordinal_position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ordinalPosition"))

    @ordinal_position.setter
    def ordinal_position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96f73fe59063cff45a5fabe46cc5ef9301038e2ca51363160acfdd6ff6a518a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ordinalPosition", value)

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64b2a7fe0df84f84031671b52e419f6be035d371a5bfd7fa6e4eed2354f0730f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2f92998ae8b6c8fd59179b9167917d5e06e3da0bf7f6a17d89c1a9d34958d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74c7edf517db15210471252d18fb4c0295e1f6d17ac794c71b59dad9fa34cde3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMysqlColumns")
    def put_mysql_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2a0c2eed43d5a92c7dd35f9d3b898447ed32f9260596e554f0bf82139dabb27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysqlColumns", [value]))

    @jsii.member(jsii_name="resetMysqlColumns")
    def reset_mysql_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlColumns", []))

    @builtins.property
    @jsii.member(jsii_name="mysqlColumns")
    def mysql_columns(
        self,
    ) -> DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsList:
        return typing.cast(DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsList, jsii.get(self, "mysqlColumns"))

    @builtins.property
    @jsii.member(jsii_name="mysqlColumnsInput")
    def mysql_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]], jsii.get(self, "mysqlColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a802aba7a80609e781d874483717985a77c791a6d610d086e56342e5ebdfea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a3c95f2945ef79610f226e7de8f82f4dd6c488b2cdea201b5adee9eb165a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__339d0233b5e3939582ec717c6235f70b3bcfce5011c933d1fa7b7b221a1b3f98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMysqlTables")
    def put_mysql_tables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e753886968f6ad8529639aad8ba094d4d936e8fb59d04017d16679362ce906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysqlTables", [value]))

    @jsii.member(jsii_name="resetMysqlTables")
    def reset_mysql_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlTables", []))

    @builtins.property
    @jsii.member(jsii_name="mysqlTables")
    def mysql_tables(
        self,
    ) -> DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesList:
        return typing.cast(DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesList, jsii.get(self, "mysqlTables"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlTablesInput")
    def mysql_tables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables]]], jsii.get(self, "mysqlTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ddba99321e758ecfffe491c01f502472c59352bb67f1530bbaea001f0a7062)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e753e427d29d0ade6f4009149848849060b763be17e45608a15cca438775be09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93d8c032e45bf0ac57ac3d0979da5b6ffe8c1f99b09476d82280a9af84df9c6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMysqlDatabases")
    def put_mysql_databases(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc57f764ac9d739ecc943fad16909c32b76e6c97dea9a5df494ab6c104e29123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysqlDatabases", [value]))

    @builtins.property
    @jsii.member(jsii_name="mysqlDatabases")
    def mysql_databases(
        self,
    ) -> DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesList:
        return typing.cast(DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesList, jsii.get(self, "mysqlDatabases"))

    @builtins.property
    @jsii.member(jsii_name="mysqlDatabasesInput")
    def mysql_databases_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases]]], jsii.get(self, "mysqlDatabasesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b7210b8484ca8aea5f7a6f1596f56ef4c03fe2c76a48dee6597741f3c6ff5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects",
    jsii_struct_bases=[],
    name_mapping={"mysql_databases": "mysqlDatabases"},
)
class DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects:
    def __init__(
        self,
        *,
        mysql_databases: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param mysql_databases: mysql_databases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_databases DatastreamStream#mysql_databases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40db11a5bb1c2aca7472fd834428a2203489803a28b44b1e4962ad4ab1b66159)
            check_type(argname="argument mysql_databases", value=mysql_databases, expected_type=type_hints["mysql_databases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mysql_databases": mysql_databases,
        }

    @builtins.property
    def mysql_databases(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases"]]:
        '''mysql_databases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_databases DatastreamStream#mysql_databases}
        '''
        result = self._values.get("mysql_databases")
        assert result is not None, "Required property 'mysql_databases' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases",
    jsii_struct_bases=[],
    name_mapping={"database": "database", "mysql_tables": "mysqlTables"},
)
class DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases:
    def __init__(
        self,
        *,
        database: builtins.str,
        mysql_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param database: Database name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#database DatastreamStream#database}
        :param mysql_tables: mysql_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_tables DatastreamStream#mysql_tables}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff4d778c3932f51b621c3ff1675a74882c85bb24341f2bf1594c06d9c82f36f)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument mysql_tables", value=mysql_tables, expected_type=type_hints["mysql_tables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
        }
        if mysql_tables is not None:
            self._values["mysql_tables"] = mysql_tables

    @builtins.property
    def database(self) -> builtins.str:
        '''Database name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#database DatastreamStream#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mysql_tables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables"]]]:
        '''mysql_tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_tables DatastreamStream#mysql_tables}
        '''
        result = self._values.get("mysql_tables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ade2a69c288d1345efb3bb511b247830dfd4432c1cd9cbefcabf6c9078c58dc5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264cc6b382219d468fd08c237199dbe2f9c342a7f5890d61df2f62ee150f6ee4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43dfcfbaa01fb883388f2b178ba7a5408a426f709176123962218ff85fdb5262)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a3c66c27ba53c72edcb3b6f85cf2f84f3bd4afd152aa8d8bbdce895bca382e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__824badd6fb7e5f770535729d1e915a227b98a14597f969bc12aaf2635f49b992)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec8b65c0e93aeb7913ed2a822757e31ec88018bc0633b32238f9b6ad54df3bab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables",
    jsii_struct_bases=[],
    name_mapping={"table": "table", "mysql_columns": "mysqlColumns"},
)
class DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables:
    def __init__(
        self,
        *,
        table: builtins.str,
        mysql_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param table: Table name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        :param mysql_columns: mysql_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_columns DatastreamStream#mysql_columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f8c103e5beb0d973e5d209018bdb2893707dc54045bf4164625d73468a4327)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument mysql_columns", value=mysql_columns, expected_type=type_hints["mysql_columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if mysql_columns is not None:
            self._values["mysql_columns"] = mysql_columns

    @builtins.property
    def table(self) -> builtins.str:
        '''Table name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mysql_columns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns"]]]:
        '''mysql_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_columns DatastreamStream#mysql_columns}
        '''
        result = self._values.get("mysql_columns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f2ae67802bc4d46269f15e251ca61b00cd7e6cc4c72696f5ef1e117bd0b9351)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba47fc823bc86f85b46f3c7d66c7ef36e848bf6a8f9d4e4e4ec74485144daaa4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c60478bf9cf99a40bd62622ba84b3b4844306f809ead2f0c86eb8fe301fc9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72e164afb7b4632e6e21ba9fe40e4060ded214f779343520f8ae627e64f6c416)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4fba8425facced2e35d16bc08d9f9df4a3cfe6e09828f27fbfdcbf3a5ec6751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811d23977ea46d8bb808a32e998c0cdeec1202920f1232c14e3d4e536d8f9934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns",
    jsii_struct_bases=[],
    name_mapping={
        "collation": "collation",
        "column": "column",
        "data_type": "dataType",
        "nullable": "nullable",
        "ordinal_position": "ordinalPosition",
        "primary_key": "primaryKey",
    },
)
class DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns:
    def __init__(
        self,
        *,
        collation: typing.Optional[builtins.str] = None,
        column: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ordinal_position: typing.Optional[jsii.Number] = None,
        primary_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param collation: Column collation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#collation DatastreamStream#collation}
        :param column: Column name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        :param data_type: The MySQL data type. Full data types list can be found here: https://dev.mysql.com/doc/refman/8.0/en/data-types.html. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        :param nullable: Whether or not the column can accept a null value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#nullable DatastreamStream#nullable}
        :param ordinal_position: The ordinal position of the column in the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#ordinal_position DatastreamStream#ordinal_position}
        :param primary_key: Whether or not the column represents a primary key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#primary_key DatastreamStream#primary_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6b2437de5afb4d3d3062eedf288787c94f774d386adc5570fd611e7a929e190)
            check_type(argname="argument collation", value=collation, expected_type=type_hints["collation"])
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument nullable", value=nullable, expected_type=type_hints["nullable"])
            check_type(argname="argument ordinal_position", value=ordinal_position, expected_type=type_hints["ordinal_position"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if collation is not None:
            self._values["collation"] = collation
        if column is not None:
            self._values["column"] = column
        if data_type is not None:
            self._values["data_type"] = data_type
        if nullable is not None:
            self._values["nullable"] = nullable
        if ordinal_position is not None:
            self._values["ordinal_position"] = ordinal_position
        if primary_key is not None:
            self._values["primary_key"] = primary_key

    @builtins.property
    def collation(self) -> typing.Optional[builtins.str]:
        '''Column collation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#collation DatastreamStream#collation}
        '''
        result = self._values.get("collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def column(self) -> typing.Optional[builtins.str]:
        '''Column name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        '''
        result = self._values.get("column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''The MySQL data type. Full data types list can be found here: https://dev.mysql.com/doc/refman/8.0/en/data-types.html.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nullable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the column can accept a null value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#nullable DatastreamStream#nullable}
        '''
        result = self._values.get("nullable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ordinal_position(self) -> typing.Optional[jsii.Number]:
        '''The ordinal position of the column in the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#ordinal_position DatastreamStream#ordinal_position}
        '''
        result = self._values.get("ordinal_position")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the column represents a primary key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#primary_key DatastreamStream#primary_key}
        '''
        result = self._values.get("primary_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37248826856ca9dfb4e91cb36937cd1b038e5edac9cce3f3be797f674e6933ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c227d69d63e5037e72560f8cfe9e7b04578befbe5130eed9150a61b587d3a0f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c1f9241ec90839a4e9c7459608fec5eb625c2fb68430051ad1689fdad8eb56)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25ca7dd00f97fbe18a2c49875f68a9eae6a6255a559ad69db9a3ee209ef6192b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__473f5e905f2848a2ccb19b790fd4c15eea0c52576954c9e7e48a8935c5db34a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b258a7501901c9867024fa4f2c4c003140669bebbfe47678087094d1c19ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2c5f7ad9b605e87fa3c703004388f9d973ac9b1e61d381ca0e122e420260396)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCollation")
    def reset_collation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollation", []))

    @jsii.member(jsii_name="resetColumn")
    def reset_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumn", []))

    @jsii.member(jsii_name="resetDataType")
    def reset_data_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataType", []))

    @jsii.member(jsii_name="resetNullable")
    def reset_nullable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullable", []))

    @jsii.member(jsii_name="resetOrdinalPosition")
    def reset_ordinal_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrdinalPosition", []))

    @jsii.member(jsii_name="resetPrimaryKey")
    def reset_primary_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryKey", []))

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "length"))

    @builtins.property
    @jsii.member(jsii_name="collationInput")
    def collation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collationInput"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypeInput")
    def data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nullableInput")
    def nullable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nullableInput"))

    @builtins.property
    @jsii.member(jsii_name="ordinalPositionInput")
    def ordinal_position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ordinalPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeyInput")
    def primary_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="collation")
    def collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collation"))

    @collation.setter
    def collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18623f5e4a5f5e41edc82a5f6793879500c107969e69faabe743ec280dd16351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collation", value)

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "column"))

    @column.setter
    def column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aed8cbdee483c61be882e1558fc23ea2e3a910b66185dfcf543429f50ddb176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812c5406870508b7dcac28e9456b090b4d1f89406cc88a2040c859c09e71567a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="nullable")
    def nullable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nullable"))

    @nullable.setter
    def nullable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aec533a8ba2c7f9ab6215ed1c075b98a28fec4443e3ca719d34ffa4e7ecfdd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullable", value)

    @builtins.property
    @jsii.member(jsii_name="ordinalPosition")
    def ordinal_position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ordinalPosition"))

    @ordinal_position.setter
    def ordinal_position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8982e4523ee32bb9d8365de4142ceb42cf0144c0a45c49e41ef9accfc902e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ordinalPosition", value)

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7726d162a19d90a4da0f120eca91dc0bb17ff7e32bd9045dda1f36ab000b80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a64b1902d4fee186b4bb8f2adde3aa0c8258831ed76e5ef9445f475913abaa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__237381b8637307cc7ee36e5718bb088f29692ac30282fe330db0d08e2e0b4532)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMysqlColumns")
    def put_mysql_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e02dfc07a981322c5b8eced3743447d9a805a9b4f8533beddfc23764b5edfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysqlColumns", [value]))

    @jsii.member(jsii_name="resetMysqlColumns")
    def reset_mysql_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlColumns", []))

    @builtins.property
    @jsii.member(jsii_name="mysqlColumns")
    def mysql_columns(
        self,
    ) -> DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsList:
        return typing.cast(DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsList, jsii.get(self, "mysqlColumns"))

    @builtins.property
    @jsii.member(jsii_name="mysqlColumnsInput")
    def mysql_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]], jsii.get(self, "mysqlColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194e3ac627639d568a0e45fb6174fdf679bf1a46f154a89120f30df44737d4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc9c4f92d7944ed623c164ccc25807fc788a1a13862f4b03cdc329bc1e5a194e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edbedda5850481069316e19fe67cce30cc1c84aa2742bdd454adc48f1f439f86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putMysqlTables")
    def put_mysql_tables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b495122f684f8a6aff9d3cacd4b489d00bc74085863a55a9cc6ed61d8016dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysqlTables", [value]))

    @jsii.member(jsii_name="resetMysqlTables")
    def reset_mysql_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlTables", []))

    @builtins.property
    @jsii.member(jsii_name="mysqlTables")
    def mysql_tables(
        self,
    ) -> DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesList:
        return typing.cast(DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesList, jsii.get(self, "mysqlTables"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlTablesInput")
    def mysql_tables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables]]], jsii.get(self, "mysqlTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b85c9f253102ec7dfb09677425de6dbdb1f44d41faf0afd71a5b30519d4668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__871843b0fb3d6e912f71a0f4656946654572899c708f26ad9164fc7e039f8b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad7739c0c903f5d4eed5b61e16a039adbae564ad438ed843c2408b9ca2174b4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMysqlDatabases")
    def put_mysql_databases(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0564a6ef5fbb63d7a0fd01455b2db2106097444d2ec9d14b5793b6facddd8242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysqlDatabases", [value]))

    @builtins.property
    @jsii.member(jsii_name="mysqlDatabases")
    def mysql_databases(
        self,
    ) -> DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesList:
        return typing.cast(DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesList, jsii.get(self, "mysqlDatabases"))

    @builtins.property
    @jsii.member(jsii_name="mysqlDatabasesInput")
    def mysql_databases_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases]]], jsii.get(self, "mysqlDatabasesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a075919af5790565e078286520be7fc44a00af876994a9d576c8d2e79ad9e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigMysqlSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigMysqlSourceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3dd658cd4fa3e196ac9065595cccd04322f9aa72e82d158c577d95074f21d5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludeObjects")
    def put_exclude_objects(
        self,
        *,
        mysql_databases: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param mysql_databases: mysql_databases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_databases DatastreamStream#mysql_databases}
        '''
        value = DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects(
            mysql_databases=mysql_databases
        )

        return typing.cast(None, jsii.invoke(self, "putExcludeObjects", [value]))

    @jsii.member(jsii_name="putIncludeObjects")
    def put_include_objects(
        self,
        *,
        mysql_databases: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param mysql_databases: mysql_databases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#mysql_databases DatastreamStream#mysql_databases}
        '''
        value = DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects(
            mysql_databases=mysql_databases
        )

        return typing.cast(None, jsii.invoke(self, "putIncludeObjects", [value]))

    @jsii.member(jsii_name="resetExcludeObjects")
    def reset_exclude_objects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeObjects", []))

    @jsii.member(jsii_name="resetIncludeObjects")
    def reset_include_objects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeObjects", []))

    @jsii.member(jsii_name="resetMaxConcurrentBackfillTasks")
    def reset_max_concurrent_backfill_tasks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentBackfillTasks", []))

    @jsii.member(jsii_name="resetMaxConcurrentCdcTasks")
    def reset_max_concurrent_cdc_tasks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentCdcTasks", []))

    @builtins.property
    @jsii.member(jsii_name="excludeObjects")
    def exclude_objects(
        self,
    ) -> DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsOutputReference:
        return typing.cast(DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsOutputReference, jsii.get(self, "excludeObjects"))

    @builtins.property
    @jsii.member(jsii_name="includeObjects")
    def include_objects(
        self,
    ) -> DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsOutputReference:
        return typing.cast(DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsOutputReference, jsii.get(self, "includeObjects"))

    @builtins.property
    @jsii.member(jsii_name="excludeObjectsInput")
    def exclude_objects_input(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects], jsii.get(self, "excludeObjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeObjectsInput")
    def include_objects_input(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects], jsii.get(self, "includeObjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentBackfillTasksInput")
    def max_concurrent_backfill_tasks_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentBackfillTasksInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentCdcTasksInput")
    def max_concurrent_cdc_tasks_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentCdcTasksInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentBackfillTasks")
    def max_concurrent_backfill_tasks(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentBackfillTasks"))

    @max_concurrent_backfill_tasks.setter
    def max_concurrent_backfill_tasks(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb969979110dea8b7d29506aad43f91e8e6c30ccd2404a2533ee0c45022bb72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentBackfillTasks", value)

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentCdcTasks")
    def max_concurrent_cdc_tasks(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentCdcTasks"))

    @max_concurrent_cdc_tasks.setter
    def max_concurrent_cdc_tasks(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b176c9e31729438ec79fb94e1db18e775b08f3ea14b518ee846998caad54c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentCdcTasks", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfig]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ff671da4949da1a3fd7811aa6a121febb36c82cdc6828d84d473f27be21b0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "drop_large_objects": "dropLargeObjects",
        "exclude_objects": "excludeObjects",
        "include_objects": "includeObjects",
        "max_concurrent_backfill_tasks": "maxConcurrentBackfillTasks",
        "max_concurrent_cdc_tasks": "maxConcurrentCdcTasks",
        "stream_large_objects": "streamLargeObjects",
    },
)
class DatastreamStreamSourceConfigOracleSourceConfig:
    def __init__(
        self,
        *,
        drop_large_objects: typing.Optional[typing.Union["DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_objects: typing.Optional[typing.Union["DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        include_objects: typing.Optional[typing.Union["DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        max_concurrent_backfill_tasks: typing.Optional[jsii.Number] = None,
        max_concurrent_cdc_tasks: typing.Optional[jsii.Number] = None,
        stream_large_objects: typing.Optional[typing.Union["DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param drop_large_objects: drop_large_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#drop_large_objects DatastreamStream#drop_large_objects}
        :param exclude_objects: exclude_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#exclude_objects DatastreamStream#exclude_objects}
        :param include_objects: include_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#include_objects DatastreamStream#include_objects}
        :param max_concurrent_backfill_tasks: Maximum number of concurrent backfill tasks. The number should be non negative. If not set (or set to 0), the system's default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_backfill_tasks DatastreamStream#max_concurrent_backfill_tasks}
        :param max_concurrent_cdc_tasks: Maximum number of concurrent CDC tasks. The number should be non negative. If not set (or set to 0), the system's default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_cdc_tasks DatastreamStream#max_concurrent_cdc_tasks}
        :param stream_large_objects: stream_large_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#stream_large_objects DatastreamStream#stream_large_objects}
        '''
        if isinstance(drop_large_objects, dict):
            drop_large_objects = DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects(**drop_large_objects)
        if isinstance(exclude_objects, dict):
            exclude_objects = DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects(**exclude_objects)
        if isinstance(include_objects, dict):
            include_objects = DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects(**include_objects)
        if isinstance(stream_large_objects, dict):
            stream_large_objects = DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects(**stream_large_objects)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66eb082c94f9d5e488dafeacc11e84716441ed791053fec9533f0966c15722a)
            check_type(argname="argument drop_large_objects", value=drop_large_objects, expected_type=type_hints["drop_large_objects"])
            check_type(argname="argument exclude_objects", value=exclude_objects, expected_type=type_hints["exclude_objects"])
            check_type(argname="argument include_objects", value=include_objects, expected_type=type_hints["include_objects"])
            check_type(argname="argument max_concurrent_backfill_tasks", value=max_concurrent_backfill_tasks, expected_type=type_hints["max_concurrent_backfill_tasks"])
            check_type(argname="argument max_concurrent_cdc_tasks", value=max_concurrent_cdc_tasks, expected_type=type_hints["max_concurrent_cdc_tasks"])
            check_type(argname="argument stream_large_objects", value=stream_large_objects, expected_type=type_hints["stream_large_objects"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if drop_large_objects is not None:
            self._values["drop_large_objects"] = drop_large_objects
        if exclude_objects is not None:
            self._values["exclude_objects"] = exclude_objects
        if include_objects is not None:
            self._values["include_objects"] = include_objects
        if max_concurrent_backfill_tasks is not None:
            self._values["max_concurrent_backfill_tasks"] = max_concurrent_backfill_tasks
        if max_concurrent_cdc_tasks is not None:
            self._values["max_concurrent_cdc_tasks"] = max_concurrent_cdc_tasks
        if stream_large_objects is not None:
            self._values["stream_large_objects"] = stream_large_objects

    @builtins.property
    def drop_large_objects(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects"]:
        '''drop_large_objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#drop_large_objects DatastreamStream#drop_large_objects}
        '''
        result = self._values.get("drop_large_objects")
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects"], result)

    @builtins.property
    def exclude_objects(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects"]:
        '''exclude_objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#exclude_objects DatastreamStream#exclude_objects}
        '''
        result = self._values.get("exclude_objects")
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects"], result)

    @builtins.property
    def include_objects(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects"]:
        '''include_objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#include_objects DatastreamStream#include_objects}
        '''
        result = self._values.get("include_objects")
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects"], result)

    @builtins.property
    def max_concurrent_backfill_tasks(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of concurrent backfill tasks.

        The number should be non negative.
        If not set (or set to 0), the system's default value will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_backfill_tasks DatastreamStream#max_concurrent_backfill_tasks}
        '''
        result = self._values.get("max_concurrent_backfill_tasks")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_concurrent_cdc_tasks(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of concurrent CDC tasks.

        The number should be non negative.
        If not set (or set to 0), the system's default value will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_cdc_tasks DatastreamStream#max_concurrent_cdc_tasks}
        '''
        result = self._values.get("max_concurrent_cdc_tasks")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stream_large_objects(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects"]:
        '''stream_large_objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#stream_large_objects DatastreamStream#stream_large_objects}
        '''
        result = self._values.get("stream_large_objects")
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigOracleSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects",
    jsii_struct_bases=[],
    name_mapping={},
)
class DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dedf9a1c105f8b0ace85d2fb166699c788477fe040a97299edeac028ef1349c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f25e16b7e3f2894d0a674e0e5dec052654a654e507ec9ae6b830f7082630f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects",
    jsii_struct_bases=[],
    name_mapping={"oracle_schemas": "oracleSchemas"},
)
class DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects:
    def __init__(
        self,
        *,
        oracle_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param oracle_schemas: oracle_schemas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_schemas DatastreamStream#oracle_schemas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df7264724e2f8f734ecb03f7375a7bcf9ece7168bf24e6bbe1eb050fc7e8097c)
            check_type(argname="argument oracle_schemas", value=oracle_schemas, expected_type=type_hints["oracle_schemas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oracle_schemas": oracle_schemas,
        }

    @builtins.property
    def oracle_schemas(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas"]]:
        '''oracle_schemas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_schemas DatastreamStream#oracle_schemas}
        '''
        result = self._values.get("oracle_schemas")
        assert result is not None, "Required property 'oracle_schemas' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas",
    jsii_struct_bases=[],
    name_mapping={"schema": "schema", "oracle_tables": "oracleTables"},
)
class DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas:
    def __init__(
        self,
        *,
        schema: builtins.str,
        oracle_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param schema: Schema name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema DatastreamStream#schema}
        :param oracle_tables: oracle_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_tables DatastreamStream#oracle_tables}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3af95956f04ffa930fb3051a9dca3477324127bf73654e817d052ddc9e327bd)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument oracle_tables", value=oracle_tables, expected_type=type_hints["oracle_tables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema": schema,
        }
        if oracle_tables is not None:
            self._values["oracle_tables"] = oracle_tables

    @builtins.property
    def schema(self) -> builtins.str:
        '''Schema name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema DatastreamStream#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oracle_tables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables"]]]:
        '''oracle_tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_tables DatastreamStream#oracle_tables}
        '''
        result = self._values.get("oracle_tables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c14ee331d4c6c68d26d4b34ceff7f4f08de047e8f93c63129c8ceeedafd0c3b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c09aca6227bc2111a3634eb67415e8546c62c7c53f17e2f04b93a99e1891d60e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f176eeab4202cf5f29376d55270cd5ce31125d50da3b25ed6bb68f63cfb46eef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f1c0a0048902bc746f0202b4d19cb62006b09d01d9138b7731cc546f19955d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa6d271dc6207737838fe8eecc538d747899bd2d4a738ccb8ce5e3b93ec5bbdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b99297a2f23ea2ec019a3f7f549c0553614eb1bc5300cfde78ea4d6bbb37d829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables",
    jsii_struct_bases=[],
    name_mapping={"table": "table", "oracle_columns": "oracleColumns"},
)
class DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables:
    def __init__(
        self,
        *,
        table: builtins.str,
        oracle_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param table: Table name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        :param oracle_columns: oracle_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_columns DatastreamStream#oracle_columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8e59985faaf7a9634858fdbc3f40bca97fb97cbd9700de5b7b7a2c0759aa781)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument oracle_columns", value=oracle_columns, expected_type=type_hints["oracle_columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if oracle_columns is not None:
            self._values["oracle_columns"] = oracle_columns

    @builtins.property
    def table(self) -> builtins.str:
        '''Table name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oracle_columns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns"]]]:
        '''oracle_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_columns DatastreamStream#oracle_columns}
        '''
        result = self._values.get("oracle_columns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b244ba4e92a9932a7d6e9f7169946854b07ba91d02ba16bc98a319f3f963491)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dbdc3a296709fcbd886e019297d0c9636db309cef96eded6cc292949b90c9fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d770d503d2634261928c26d7b624b794be932f06df91f0901e332c8fa0900fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c189e328d4c1867d36419eaa2657258a07cc220930f8bb800780423bacaf2aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b711f126f0b5d5863f66f049e5b4f96928c55b522a99e7f251b8386f7c09714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a31421ae6c3e643759494d0dcc284873dda3ff2ca5af619ec4380eb9f450f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns",
    jsii_struct_bases=[],
    name_mapping={"column": "column", "data_type": "dataType"},
)
class DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns:
    def __init__(
        self,
        *,
        column: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column: Column name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        :param data_type: The Oracle data type. Full data types list can be found here: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86a0e8627a13e5003c6e5a20d23a7b765720ee25fcb19c7410da5638d2ea2398)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column is not None:
            self._values["column"] = column
        if data_type is not None:
            self._values["data_type"] = data_type

    @builtins.property
    def column(self) -> typing.Optional[builtins.str]:
        '''Column name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        '''
        result = self._values.get("column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''The Oracle data type. Full data types list can be found here: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d8f80c6538999ac1bf4df247ca0bc78a694afe2228ff269cfd7410963e4b035)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa82e47be138ef9474e4187168574246dcc46ef7129fbbb58ef8bee27ee1277e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c9d3ceede0b7d41b0544eabe42318c95d78ec1fade2d2f7e8a0b6d1f7533b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6fb660aba7e959f1fb5f32969811a7bcaec9ecd52f0d7444180d54481c40e6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94f2f543dca966365859a85fca94141c4af8a78bb39d50f5aaa8662ae5c672b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afce80fcace6b6b025f3db45f5ce847d510f47318018cf7a9198241b6f88ee41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae47d6bd6a064650dcecbd13f75f6059a2a0cef2c0ab45b32b82b0dbd93b83ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetColumn")
    def reset_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumn", []))

    @jsii.member(jsii_name="resetDataType")
    def reset_data_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataType", []))

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "length"))

    @builtins.property
    @jsii.member(jsii_name="nullable")
    def nullable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "nullable"))

    @builtins.property
    @jsii.member(jsii_name="ordinalPosition")
    def ordinal_position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ordinalPosition"))

    @builtins.property
    @jsii.member(jsii_name="precision")
    def precision(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precision"))

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "primaryKey"))

    @builtins.property
    @jsii.member(jsii_name="scale")
    def scale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scale"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypeInput")
    def data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "column"))

    @column.setter
    def column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d3098ca741fd087c190c0f6b132af060dae3474b2fdfa4b7f7def5821db8111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cd3b543a5dcb4a630aeca77cd2d1e56577d8caf8650da72883a4a520042f9ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbebe1a4dbf536dde4522bff5d3e87f70691bced1f6d19f71d9535b11a23bb31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeef71eb6dce09cff23e6bc2d26303ba1167e5395b9d51ca5adb912091dbdbfc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putOracleColumns")
    def put_oracle_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc6e22d4ca3795b2fccd936c86e8ca4ea7b1893bcc03d72572e645a0c7b8e94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOracleColumns", [value]))

    @jsii.member(jsii_name="resetOracleColumns")
    def reset_oracle_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracleColumns", []))

    @builtins.property
    @jsii.member(jsii_name="oracleColumns")
    def oracle_columns(
        self,
    ) -> DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumnsList:
        return typing.cast(DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumnsList, jsii.get(self, "oracleColumns"))

    @builtins.property
    @jsii.member(jsii_name="oracleColumnsInput")
    def oracle_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns]]], jsii.get(self, "oracleColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6366596e84f7eed71f90a445ffa1750cd50b1967b305adad975a053804f494c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48fdf7398ae4800d7c4301b786e3000fe3e43fb1630695b1e7a40bd319312a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a270e6985d7e40c797bc7aaf9609515c276e0ed06de9f52d96a459350459c168)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putOracleTables")
    def put_oracle_tables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a0a3faa79481bbca9859a5f73a140f6eeb41b654a549fd45acc53530524f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOracleTables", [value]))

    @jsii.member(jsii_name="resetOracleTables")
    def reset_oracle_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracleTables", []))

    @builtins.property
    @jsii.member(jsii_name="oracleTables")
    def oracle_tables(
        self,
    ) -> DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesList:
        return typing.cast(DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesList, jsii.get(self, "oracleTables"))

    @builtins.property
    @jsii.member(jsii_name="oracleTablesInput")
    def oracle_tables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables]]], jsii.get(self, "oracleTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bdf846f564435844623ecdb3e6c79d34f8b014ff077d1798b18c960300074c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861952d5417512b22e34e580a17b21fdb61522ac08e463be2943dbbd3ef9d6f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__03d50d163006d62e035d0f11bef96425e752c48e3ee6d25328a6ee339c2fd2a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOracleSchemas")
    def put_oracle_schemas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c928f19332207097a14d2823084320da635b7383fccdc4bfb1ff333f132941da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOracleSchemas", [value]))

    @builtins.property
    @jsii.member(jsii_name="oracleSchemas")
    def oracle_schemas(
        self,
    ) -> DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasList:
        return typing.cast(DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasList, jsii.get(self, "oracleSchemas"))

    @builtins.property
    @jsii.member(jsii_name="oracleSchemasInput")
    def oracle_schemas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas]]], jsii.get(self, "oracleSchemasInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa3e84028a28591d87bcfdece022b7a677e16e6f8f70614250b25d13a148f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects",
    jsii_struct_bases=[],
    name_mapping={"oracle_schemas": "oracleSchemas"},
)
class DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects:
    def __init__(
        self,
        *,
        oracle_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param oracle_schemas: oracle_schemas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_schemas DatastreamStream#oracle_schemas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__516e4326892830d76cb4dbc14b6f3bafd8ff65ebf477723848656fbb26a5c4dd)
            check_type(argname="argument oracle_schemas", value=oracle_schemas, expected_type=type_hints["oracle_schemas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oracle_schemas": oracle_schemas,
        }

    @builtins.property
    def oracle_schemas(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas"]]:
        '''oracle_schemas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_schemas DatastreamStream#oracle_schemas}
        '''
        result = self._values.get("oracle_schemas")
        assert result is not None, "Required property 'oracle_schemas' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas",
    jsii_struct_bases=[],
    name_mapping={"schema": "schema", "oracle_tables": "oracleTables"},
)
class DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas:
    def __init__(
        self,
        *,
        schema: builtins.str,
        oracle_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param schema: Schema name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema DatastreamStream#schema}
        :param oracle_tables: oracle_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_tables DatastreamStream#oracle_tables}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa8f93b8c7c92a2839641fa1072f9d7fa0cd1af048996626b73b213f483b81be)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument oracle_tables", value=oracle_tables, expected_type=type_hints["oracle_tables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema": schema,
        }
        if oracle_tables is not None:
            self._values["oracle_tables"] = oracle_tables

    @builtins.property
    def schema(self) -> builtins.str:
        '''Schema name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema DatastreamStream#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oracle_tables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables"]]]:
        '''oracle_tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_tables DatastreamStream#oracle_tables}
        '''
        result = self._values.get("oracle_tables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2cbfb000beee41a28642c72ce8bea5b69f8aa3d800412c4098e8437e2961d30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973887aebd270bc09eb6d8122bf444694e2ac716d08dcd0e3269c9933140dde6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df33ee5209e90dbebca60ff1c109cfc7775d013bfd7cee0fea44611b9d64afb9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1906b92b01dd6d3c847a4446a3f668b8d9e2c4542a65346739091910e01373d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fd366e369101f09638e8119eca0d05003045b8d0529e56ef9b5c52f9886327e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d29f6b07fe7b16241b50c33021a5d04ee46277d8091aa4cbc409e73730e614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables",
    jsii_struct_bases=[],
    name_mapping={"table": "table", "oracle_columns": "oracleColumns"},
)
class DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables:
    def __init__(
        self,
        *,
        table: builtins.str,
        oracle_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param table: Table name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        :param oracle_columns: oracle_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_columns DatastreamStream#oracle_columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c64bc732b152e813094b6715fd5fe81a00cc14024f7dff680edf8c722501e463)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument oracle_columns", value=oracle_columns, expected_type=type_hints["oracle_columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if oracle_columns is not None:
            self._values["oracle_columns"] = oracle_columns

    @builtins.property
    def table(self) -> builtins.str:
        '''Table name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oracle_columns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns"]]]:
        '''oracle_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_columns DatastreamStream#oracle_columns}
        '''
        result = self._values.get("oracle_columns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32f7d891e0e13cf87e0e625c6a22de14d0e4773e60aa0dc8ef9f81473d40b5de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60eec69efc016d6b982eddbba5e0db06dd68c7a7cd9640481b100b2b67557b44)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8afb6ed8fcf1bd65f104a17499713f0cc053b264513cec7cf9fca70b90f7f79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4b0d28454eb989d06344277c80aad90da0e2c4c3aafd93e86cbd8e8612b6003)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a7d3506343aa8c00182c05c90c64e7864d4d88cf255dfbda67b436d9925f204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9efcc98ae892802c17691fd17790fd590cc83c1fef5b394db215fb2b6b2e65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns",
    jsii_struct_bases=[],
    name_mapping={"column": "column", "data_type": "dataType"},
)
class DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns:
    def __init__(
        self,
        *,
        column: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column: Column name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        :param data_type: The Oracle data type. Full data types list can be found here: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5a1f56703876c5d6fe8c38e5248ab76ee659086d5747fc853c48a73a91aa18)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column is not None:
            self._values["column"] = column
        if data_type is not None:
            self._values["data_type"] = data_type

    @builtins.property
    def column(self) -> typing.Optional[builtins.str]:
        '''Column name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        '''
        result = self._values.get("column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''The Oracle data type. Full data types list can be found here: https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7ae4be4e0a222ca005624232f86d41ab7ffd15df46ffa83f2df7578c7192b97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__729dd7e7e92d47782c143f122f50918d134a6cc2f8f8ff91e930ba0723f49fb4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34da348ce04a11a4a07616ec75015c1190264bff7b4ad535b62ad5a2dacbc27a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7777ce645fa85fcb8aedb6189e5e57e5f458fc541b793ca777919224cdd2ef97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79d6708d30e0cc9a3bbc02dfe7946bd639464fb7771873908be585494a80f29c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9189d901c34736bce08f8684c9835e28a6438a4ccd18abe5f657e9f42971efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7370acfeee29348d9d8cd8a8e6a5c8018482bbd74f98bc8d9af6af5cd923c05f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetColumn")
    def reset_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumn", []))

    @jsii.member(jsii_name="resetDataType")
    def reset_data_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataType", []))

    @builtins.property
    @jsii.member(jsii_name="encoding")
    def encoding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encoding"))

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "length"))

    @builtins.property
    @jsii.member(jsii_name="nullable")
    def nullable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "nullable"))

    @builtins.property
    @jsii.member(jsii_name="ordinalPosition")
    def ordinal_position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ordinalPosition"))

    @builtins.property
    @jsii.member(jsii_name="precision")
    def precision(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precision"))

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "primaryKey"))

    @builtins.property
    @jsii.member(jsii_name="scale")
    def scale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scale"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypeInput")
    def data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "column"))

    @column.setter
    def column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5304b773ac21ec5d7b8c8e77d51a52c6f10cf12359cf9c8ea8721798aa8537e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0181dab91a59b4cc5b3be734f13d6ee4efc3da12a54828f3881645d83a29580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ff2eb35052f68fc6e740abcb5a829053101d7d86f26895de7f894635adb542)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c203d77e429514a045ccf099965680b592489aa41a78e48df85a223771d4eea7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putOracleColumns")
    def put_oracle_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4f3a037ab7b0f31e544f404d7badcfe12bdeb2bd55f8530aaddd73d0d3a03d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOracleColumns", [value]))

    @jsii.member(jsii_name="resetOracleColumns")
    def reset_oracle_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracleColumns", []))

    @builtins.property
    @jsii.member(jsii_name="oracleColumns")
    def oracle_columns(
        self,
    ) -> DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumnsList:
        return typing.cast(DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumnsList, jsii.get(self, "oracleColumns"))

    @builtins.property
    @jsii.member(jsii_name="oracleColumnsInput")
    def oracle_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns]]], jsii.get(self, "oracleColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3533dd123f0b76456846703be290b1eac81ac0e77254f94407bbc6723bbc6795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26bdcbc9e853b51532c10748e9be1f7314a633d479cf8216e5c0fa9b5a6eee24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7eacda35ed82da1716c1b9a5a50bb995abf9ffa290917a809648325d00b82f0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putOracleTables")
    def put_oracle_tables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6adca6e098fd62b4480f4f8e24087176d171d3e939d2761d05611d3c62619fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOracleTables", [value]))

    @jsii.member(jsii_name="resetOracleTables")
    def reset_oracle_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracleTables", []))

    @builtins.property
    @jsii.member(jsii_name="oracleTables")
    def oracle_tables(
        self,
    ) -> DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesList:
        return typing.cast(DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesList, jsii.get(self, "oracleTables"))

    @builtins.property
    @jsii.member(jsii_name="oracleTablesInput")
    def oracle_tables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables]]], jsii.get(self, "oracleTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__525b72ad5984924fcf93653a1a8661ae0c3a6336d827899b1c3c6eb2f2e62652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87237bc30640d91ff58ae47cf248d6bae6069e18d3c862eebfc56d33f9206fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed7d7d1d474fc71ba5617b372c9400ffba0684102f59881528bed77e2990f357)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOracleSchemas")
    def put_oracle_schemas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef837eb5998c3339d937d7a44e6b8bc1ec621141f89e9140f85e2822b14aaee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOracleSchemas", [value]))

    @builtins.property
    @jsii.member(jsii_name="oracleSchemas")
    def oracle_schemas(
        self,
    ) -> DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasList:
        return typing.cast(DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasList, jsii.get(self, "oracleSchemas"))

    @builtins.property
    @jsii.member(jsii_name="oracleSchemasInput")
    def oracle_schemas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas]]], jsii.get(self, "oracleSchemasInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba03c6342c6ac234bbb970f7129f7333a221b28c301981bde1fc01836328df4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigOracleSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0284a38daff9134ae34bee2da004caa28f5cba6f7a2c932a976c5bbfeef7c08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDropLargeObjects")
    def put_drop_large_objects(self) -> None:
        value = DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects()

        return typing.cast(None, jsii.invoke(self, "putDropLargeObjects", [value]))

    @jsii.member(jsii_name="putExcludeObjects")
    def put_exclude_objects(
        self,
        *,
        oracle_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param oracle_schemas: oracle_schemas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_schemas DatastreamStream#oracle_schemas}
        '''
        value = DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects(
            oracle_schemas=oracle_schemas
        )

        return typing.cast(None, jsii.invoke(self, "putExcludeObjects", [value]))

    @jsii.member(jsii_name="putIncludeObjects")
    def put_include_objects(
        self,
        *,
        oracle_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param oracle_schemas: oracle_schemas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#oracle_schemas DatastreamStream#oracle_schemas}
        '''
        value = DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects(
            oracle_schemas=oracle_schemas
        )

        return typing.cast(None, jsii.invoke(self, "putIncludeObjects", [value]))

    @jsii.member(jsii_name="putStreamLargeObjects")
    def put_stream_large_objects(self) -> None:
        value = DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects()

        return typing.cast(None, jsii.invoke(self, "putStreamLargeObjects", [value]))

    @jsii.member(jsii_name="resetDropLargeObjects")
    def reset_drop_large_objects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropLargeObjects", []))

    @jsii.member(jsii_name="resetExcludeObjects")
    def reset_exclude_objects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeObjects", []))

    @jsii.member(jsii_name="resetIncludeObjects")
    def reset_include_objects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeObjects", []))

    @jsii.member(jsii_name="resetMaxConcurrentBackfillTasks")
    def reset_max_concurrent_backfill_tasks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentBackfillTasks", []))

    @jsii.member(jsii_name="resetMaxConcurrentCdcTasks")
    def reset_max_concurrent_cdc_tasks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentCdcTasks", []))

    @jsii.member(jsii_name="resetStreamLargeObjects")
    def reset_stream_large_objects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreamLargeObjects", []))

    @builtins.property
    @jsii.member(jsii_name="dropLargeObjects")
    def drop_large_objects(
        self,
    ) -> DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjectsOutputReference:
        return typing.cast(DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjectsOutputReference, jsii.get(self, "dropLargeObjects"))

    @builtins.property
    @jsii.member(jsii_name="excludeObjects")
    def exclude_objects(
        self,
    ) -> DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOutputReference:
        return typing.cast(DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOutputReference, jsii.get(self, "excludeObjects"))

    @builtins.property
    @jsii.member(jsii_name="includeObjects")
    def include_objects(
        self,
    ) -> DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOutputReference:
        return typing.cast(DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOutputReference, jsii.get(self, "includeObjects"))

    @builtins.property
    @jsii.member(jsii_name="streamLargeObjects")
    def stream_large_objects(
        self,
    ) -> "DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjectsOutputReference":
        return typing.cast("DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjectsOutputReference", jsii.get(self, "streamLargeObjects"))

    @builtins.property
    @jsii.member(jsii_name="dropLargeObjectsInput")
    def drop_large_objects_input(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects], jsii.get(self, "dropLargeObjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeObjectsInput")
    def exclude_objects_input(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects], jsii.get(self, "excludeObjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeObjectsInput")
    def include_objects_input(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects], jsii.get(self, "includeObjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentBackfillTasksInput")
    def max_concurrent_backfill_tasks_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentBackfillTasksInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentCdcTasksInput")
    def max_concurrent_cdc_tasks_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentCdcTasksInput"))

    @builtins.property
    @jsii.member(jsii_name="streamLargeObjectsInput")
    def stream_large_objects_input(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects"]:
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects"], jsii.get(self, "streamLargeObjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentBackfillTasks")
    def max_concurrent_backfill_tasks(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentBackfillTasks"))

    @max_concurrent_backfill_tasks.setter
    def max_concurrent_backfill_tasks(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6af8c58123f8d8a0c8b63257339deb9a8b73e41d554341fe4515d5adc9d9c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentBackfillTasks", value)

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentCdcTasks")
    def max_concurrent_cdc_tasks(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentCdcTasks"))

    @max_concurrent_cdc_tasks.setter
    def max_concurrent_cdc_tasks(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a78fa511929ed6bc2b3ab866c19123052beac1ba8345d50ffbbc6773a8d97648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentCdcTasks", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigOracleSourceConfig]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigOracleSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamSourceConfigOracleSourceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a7fcb2fa3a21a279fd21fee2d5514bdf48d7d75fb09a0786d9c72f0f1473c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects",
    jsii_struct_bases=[],
    name_mapping={},
)
class DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__910fb5e313c4d669813b4a593e6747ab6ad76d269b30cd28faa1cab562e52c06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec0380cd31a7b9eaedd6101eafd9db4c78c28b5f7f3da800d6d9969c3f7277e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09a3549b6717770d6733410684731e269f34c59ed1d70ad04082a2cb1b372371)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMysqlSourceConfig")
    def put_mysql_source_config(
        self,
        *,
        exclude_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
        include_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
        max_concurrent_backfill_tasks: typing.Optional[jsii.Number] = None,
        max_concurrent_cdc_tasks: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param exclude_objects: exclude_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#exclude_objects DatastreamStream#exclude_objects}
        :param include_objects: include_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#include_objects DatastreamStream#include_objects}
        :param max_concurrent_backfill_tasks: Maximum number of concurrent backfill tasks. The number should be non negative. If not set (or set to 0), the system's default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_backfill_tasks DatastreamStream#max_concurrent_backfill_tasks}
        :param max_concurrent_cdc_tasks: Maximum number of concurrent CDC tasks. The number should be non negative. If not set (or set to 0), the system's default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_cdc_tasks DatastreamStream#max_concurrent_cdc_tasks}
        '''
        value = DatastreamStreamSourceConfigMysqlSourceConfig(
            exclude_objects=exclude_objects,
            include_objects=include_objects,
            max_concurrent_backfill_tasks=max_concurrent_backfill_tasks,
            max_concurrent_cdc_tasks=max_concurrent_cdc_tasks,
        )

        return typing.cast(None, jsii.invoke(self, "putMysqlSourceConfig", [value]))

    @jsii.member(jsii_name="putOracleSourceConfig")
    def put_oracle_source_config(
        self,
        *,
        drop_large_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
        include_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
        max_concurrent_backfill_tasks: typing.Optional[jsii.Number] = None,
        max_concurrent_cdc_tasks: typing.Optional[jsii.Number] = None,
        stream_large_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param drop_large_objects: drop_large_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#drop_large_objects DatastreamStream#drop_large_objects}
        :param exclude_objects: exclude_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#exclude_objects DatastreamStream#exclude_objects}
        :param include_objects: include_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#include_objects DatastreamStream#include_objects}
        :param max_concurrent_backfill_tasks: Maximum number of concurrent backfill tasks. The number should be non negative. If not set (or set to 0), the system's default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_backfill_tasks DatastreamStream#max_concurrent_backfill_tasks}
        :param max_concurrent_cdc_tasks: Maximum number of concurrent CDC tasks. The number should be non negative. If not set (or set to 0), the system's default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_cdc_tasks DatastreamStream#max_concurrent_cdc_tasks}
        :param stream_large_objects: stream_large_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#stream_large_objects DatastreamStream#stream_large_objects}
        '''
        value = DatastreamStreamSourceConfigOracleSourceConfig(
            drop_large_objects=drop_large_objects,
            exclude_objects=exclude_objects,
            include_objects=include_objects,
            max_concurrent_backfill_tasks=max_concurrent_backfill_tasks,
            max_concurrent_cdc_tasks=max_concurrent_cdc_tasks,
            stream_large_objects=stream_large_objects,
        )

        return typing.cast(None, jsii.invoke(self, "putOracleSourceConfig", [value]))

    @jsii.member(jsii_name="putPostgresqlSourceConfig")
    def put_postgresql_source_config(
        self,
        *,
        publication: builtins.str,
        replication_slot: builtins.str,
        exclude_objects: typing.Optional[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        include_objects: typing.Optional[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        max_concurrent_backfill_tasks: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param publication: The name of the publication that includes the set of all tables that are defined in the stream's include_objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#publication DatastreamStream#publication}
        :param replication_slot: The name of the logical replication slot that's configured with the pgoutput plugin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#replication_slot DatastreamStream#replication_slot}
        :param exclude_objects: exclude_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#exclude_objects DatastreamStream#exclude_objects}
        :param include_objects: include_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#include_objects DatastreamStream#include_objects}
        :param max_concurrent_backfill_tasks: Maximum number of concurrent backfill tasks. The number should be non negative. If not set (or set to 0), the system's default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_backfill_tasks DatastreamStream#max_concurrent_backfill_tasks}
        '''
        value = DatastreamStreamSourceConfigPostgresqlSourceConfig(
            publication=publication,
            replication_slot=replication_slot,
            exclude_objects=exclude_objects,
            include_objects=include_objects,
            max_concurrent_backfill_tasks=max_concurrent_backfill_tasks,
        )

        return typing.cast(None, jsii.invoke(self, "putPostgresqlSourceConfig", [value]))

    @jsii.member(jsii_name="resetMysqlSourceConfig")
    def reset_mysql_source_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlSourceConfig", []))

    @jsii.member(jsii_name="resetOracleSourceConfig")
    def reset_oracle_source_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracleSourceConfig", []))

    @jsii.member(jsii_name="resetPostgresqlSourceConfig")
    def reset_postgresql_source_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresqlSourceConfig", []))

    @builtins.property
    @jsii.member(jsii_name="mysqlSourceConfig")
    def mysql_source_config(
        self,
    ) -> DatastreamStreamSourceConfigMysqlSourceConfigOutputReference:
        return typing.cast(DatastreamStreamSourceConfigMysqlSourceConfigOutputReference, jsii.get(self, "mysqlSourceConfig"))

    @builtins.property
    @jsii.member(jsii_name="oracleSourceConfig")
    def oracle_source_config(
        self,
    ) -> DatastreamStreamSourceConfigOracleSourceConfigOutputReference:
        return typing.cast(DatastreamStreamSourceConfigOracleSourceConfigOutputReference, jsii.get(self, "oracleSourceConfig"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlSourceConfig")
    def postgresql_source_config(
        self,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigOutputReference":
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigOutputReference", jsii.get(self, "postgresqlSourceConfig"))

    @builtins.property
    @jsii.member(jsii_name="mysqlSourceConfigInput")
    def mysql_source_config_input(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfig]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfig], jsii.get(self, "mysqlSourceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="oracleSourceConfigInput")
    def oracle_source_config_input(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigOracleSourceConfig]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigOracleSourceConfig], jsii.get(self, "oracleSourceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlSourceConfigInput")
    def postgresql_source_config_input(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigPostgresqlSourceConfig"]:
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigPostgresqlSourceConfig"], jsii.get(self, "postgresqlSourceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceConnectionProfileInput")
    def source_connection_profile_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceConnectionProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceConnectionProfile")
    def source_connection_profile(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceConnectionProfile"))

    @source_connection_profile.setter
    def source_connection_profile(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0241e5b41a94a409e82cab6012190e0005a0636d4cf36be768a9f6a56556cb14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceConnectionProfile", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DatastreamStreamSourceConfig]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamSourceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac91b8aafb6713d91456fefe65121644675bbb9cb229a0456370ca2b40569268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "publication": "publication",
        "replication_slot": "replicationSlot",
        "exclude_objects": "excludeObjects",
        "include_objects": "includeObjects",
        "max_concurrent_backfill_tasks": "maxConcurrentBackfillTasks",
    },
)
class DatastreamStreamSourceConfigPostgresqlSourceConfig:
    def __init__(
        self,
        *,
        publication: builtins.str,
        replication_slot: builtins.str,
        exclude_objects: typing.Optional[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        include_objects: typing.Optional[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects", typing.Dict[builtins.str, typing.Any]]] = None,
        max_concurrent_backfill_tasks: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param publication: The name of the publication that includes the set of all tables that are defined in the stream's include_objects. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#publication DatastreamStream#publication}
        :param replication_slot: The name of the logical replication slot that's configured with the pgoutput plugin. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#replication_slot DatastreamStream#replication_slot}
        :param exclude_objects: exclude_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#exclude_objects DatastreamStream#exclude_objects}
        :param include_objects: include_objects block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#include_objects DatastreamStream#include_objects}
        :param max_concurrent_backfill_tasks: Maximum number of concurrent backfill tasks. The number should be non negative. If not set (or set to 0), the system's default value will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_backfill_tasks DatastreamStream#max_concurrent_backfill_tasks}
        '''
        if isinstance(exclude_objects, dict):
            exclude_objects = DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects(**exclude_objects)
        if isinstance(include_objects, dict):
            include_objects = DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects(**include_objects)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ae79ad53b694f7781963f400d072baa1f5d22bc5e5483bd86ba2e70599b709)
            check_type(argname="argument publication", value=publication, expected_type=type_hints["publication"])
            check_type(argname="argument replication_slot", value=replication_slot, expected_type=type_hints["replication_slot"])
            check_type(argname="argument exclude_objects", value=exclude_objects, expected_type=type_hints["exclude_objects"])
            check_type(argname="argument include_objects", value=include_objects, expected_type=type_hints["include_objects"])
            check_type(argname="argument max_concurrent_backfill_tasks", value=max_concurrent_backfill_tasks, expected_type=type_hints["max_concurrent_backfill_tasks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "publication": publication,
            "replication_slot": replication_slot,
        }
        if exclude_objects is not None:
            self._values["exclude_objects"] = exclude_objects
        if include_objects is not None:
            self._values["include_objects"] = include_objects
        if max_concurrent_backfill_tasks is not None:
            self._values["max_concurrent_backfill_tasks"] = max_concurrent_backfill_tasks

    @builtins.property
    def publication(self) -> builtins.str:
        '''The name of the publication that includes the set of all tables that are defined in the stream's include_objects.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#publication DatastreamStream#publication}
        '''
        result = self._values.get("publication")
        assert result is not None, "Required property 'publication' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replication_slot(self) -> builtins.str:
        '''The name of the logical replication slot that's configured with the pgoutput plugin.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#replication_slot DatastreamStream#replication_slot}
        '''
        result = self._values.get("replication_slot")
        assert result is not None, "Required property 'replication_slot' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclude_objects(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects"]:
        '''exclude_objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#exclude_objects DatastreamStream#exclude_objects}
        '''
        result = self._values.get("exclude_objects")
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects"], result)

    @builtins.property
    def include_objects(
        self,
    ) -> typing.Optional["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects"]:
        '''include_objects block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#include_objects DatastreamStream#include_objects}
        '''
        result = self._values.get("include_objects")
        return typing.cast(typing.Optional["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects"], result)

    @builtins.property
    def max_concurrent_backfill_tasks(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of concurrent backfill tasks.

        The number should be non
        negative. If not set (or set to 0), the system's default value will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#max_concurrent_backfill_tasks DatastreamStream#max_concurrent_backfill_tasks}
        '''
        result = self._values.get("max_concurrent_backfill_tasks")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigPostgresqlSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects",
    jsii_struct_bases=[],
    name_mapping={"postgresql_schemas": "postgresqlSchemas"},
)
class DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects:
    def __init__(
        self,
        *,
        postgresql_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param postgresql_schemas: postgresql_schemas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_schemas DatastreamStream#postgresql_schemas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a4258bf2802905d8ee887426f63927491e3fcf19a9f8d9e9c4a1021c552e9b)
            check_type(argname="argument postgresql_schemas", value=postgresql_schemas, expected_type=type_hints["postgresql_schemas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "postgresql_schemas": postgresql_schemas,
        }

    @builtins.property
    def postgresql_schemas(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas"]]:
        '''postgresql_schemas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_schemas DatastreamStream#postgresql_schemas}
        '''
        result = self._values.get("postgresql_schemas")
        assert result is not None, "Required property 'postgresql_schemas' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__331284e6bce06ba8e518bb9569a72e24af92de555d78faad1178b6cf66219eac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostgresqlSchemas")
    def put_postgresql_schemas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e3f909289a0301309f8873713bb75c4d2626f97f24ee91f33ce580c3c7eedf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostgresqlSchemas", [value]))

    @builtins.property
    @jsii.member(jsii_name="postgresqlSchemas")
    def postgresql_schemas(
        self,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasList":
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasList", jsii.get(self, "postgresqlSchemas"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlSchemasInput")
    def postgresql_schemas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas"]]], jsii.get(self, "postgresqlSchemasInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45caed9b649398bcd100e72f0da6ba0b4dc3c337f63cbdf9e29b6e9a0f56df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas",
    jsii_struct_bases=[],
    name_mapping={"schema": "schema", "postgresql_tables": "postgresqlTables"},
)
class DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas:
    def __init__(
        self,
        *,
        schema: builtins.str,
        postgresql_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param schema: Database name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema DatastreamStream#schema}
        :param postgresql_tables: postgresql_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_tables DatastreamStream#postgresql_tables}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e80d838b5d30de65ecfb3ef29147d8ca2e0e4dde6d9510dbf49004edba6a88)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument postgresql_tables", value=postgresql_tables, expected_type=type_hints["postgresql_tables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema": schema,
        }
        if postgresql_tables is not None:
            self._values["postgresql_tables"] = postgresql_tables

    @builtins.property
    def schema(self) -> builtins.str:
        '''Database name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema DatastreamStream#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postgresql_tables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables"]]]:
        '''postgresql_tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_tables DatastreamStream#postgresql_tables}
        '''
        result = self._values.get("postgresql_tables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c13ca4ea5fba74669a57949657611d0d307df8a831f1cc55a2d6e7cc45fd334f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f86d6fa0a2868416d0a9d770e74366754e45073e50c7a4af599b6643d1509c63)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea4044c76379b835b2718de9a05b4f5d3a32e54bde9d3906bab2394f7549b5a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b98b03573850b37399b98e2f4ea195208045a268343c13c51ba2a1d9714eabb4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af910725b901913c8796df10376a0a8384dada4387c8d97043aad60352d2f60c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ad272d189d797c265d529906e72c1ad5b7e43852a2326edae948a0fcd0d885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__483f3446b724d77c2b15ee3231e21c22a230d30ec9fb94d34d861ab612670618)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPostgresqlTables")
    def put_postgresql_tables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d47d159419ecd7203b1c5ff65f70063fdac0e31c4116d1805f472f9c98167b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostgresqlTables", [value]))

    @jsii.member(jsii_name="resetPostgresqlTables")
    def reset_postgresql_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresqlTables", []))

    @builtins.property
    @jsii.member(jsii_name="postgresqlTables")
    def postgresql_tables(
        self,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesList":
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesList", jsii.get(self, "postgresqlTables"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlTablesInput")
    def postgresql_tables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables"]]], jsii.get(self, "postgresqlTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e18f95ba3c41ef9bf98231c24e4793b4378421b2758643cde5f8efc5a7ca55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0927fdfb9e60d0e1ba1057b926dad9bb5c241cce5cf9b6d22123223f8aa8297)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables",
    jsii_struct_bases=[],
    name_mapping={"table": "table", "postgresql_columns": "postgresqlColumns"},
)
class DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables:
    def __init__(
        self,
        *,
        table: builtins.str,
        postgresql_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param table: Table name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        :param postgresql_columns: postgresql_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_columns DatastreamStream#postgresql_columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6af859433b95de5d81eb431dd08d705162bf8db2347d4ccc726ccf842b088d9)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument postgresql_columns", value=postgresql_columns, expected_type=type_hints["postgresql_columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if postgresql_columns is not None:
            self._values["postgresql_columns"] = postgresql_columns

    @builtins.property
    def table(self) -> builtins.str:
        '''Table name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postgresql_columns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns"]]]:
        '''postgresql_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_columns DatastreamStream#postgresql_columns}
        '''
        result = self._values.get("postgresql_columns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efd218897461e16c0f23974a580eb76abe2845d484c171984359c1ed8622b8d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a2e74c7fdd529a4d1ee7f6a64b9e6e47ddd667358f0abc84fd0148253d584ea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aebc96f946971f54129c41e5eda9e3ad1a0ebff117f09028da60eb7ffd75008)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d805893bb3235b4f9c1633d71059201d7d08ccdd7aa36a50db3d826b2b35ad8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__144731a8b2e89bda180d8919cb694996e07dbac0c0fdfaa5532f9f2b32e6d462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac46856a302b0b8bba89085e76bfe43b99f5f9c5227798064dbdda02637628f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a37eae8e46f1b45ca1fe3320a798a2565dcb12e2b16076f603238d893d2b204b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPostgresqlColumns")
    def put_postgresql_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ebe71475a122a527121571f53d72e53de7ae6e06b06a2240fcb6fd75b9f59c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostgresqlColumns", [value]))

    @jsii.member(jsii_name="resetPostgresqlColumns")
    def reset_postgresql_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresqlColumns", []))

    @builtins.property
    @jsii.member(jsii_name="postgresqlColumns")
    def postgresql_columns(
        self,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList":
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList", jsii.get(self, "postgresqlColumns"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlColumnsInput")
    def postgresql_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns"]]], jsii.get(self, "postgresqlColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae0ae20385eb902a594d35738560a9b1f74723a8d3d4c141442d8f77975018d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eee4cc65dba21c31a714e36d03dc9931d7d00d35842b60dcc3ee7c2d28523eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "data_type": "dataType",
        "nullable": "nullable",
        "ordinal_position": "ordinalPosition",
        "primary_key": "primaryKey",
    },
)
class DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns:
    def __init__(
        self,
        *,
        column: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ordinal_position: typing.Optional[jsii.Number] = None,
        primary_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param column: Column name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        :param data_type: The PostgreSQL data type. Full data types list can be found here: https://www.postgresql.org/docs/current/datatype.html. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        :param nullable: Whether or not the column can accept a null value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#nullable DatastreamStream#nullable}
        :param ordinal_position: The ordinal position of the column in the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#ordinal_position DatastreamStream#ordinal_position}
        :param primary_key: Whether or not the column represents a primary key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#primary_key DatastreamStream#primary_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__119968ae5084667a855873712f397551ee9b874d666d3cb87dba8ee65cb4ebb6)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument nullable", value=nullable, expected_type=type_hints["nullable"])
            check_type(argname="argument ordinal_position", value=ordinal_position, expected_type=type_hints["ordinal_position"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column is not None:
            self._values["column"] = column
        if data_type is not None:
            self._values["data_type"] = data_type
        if nullable is not None:
            self._values["nullable"] = nullable
        if ordinal_position is not None:
            self._values["ordinal_position"] = ordinal_position
        if primary_key is not None:
            self._values["primary_key"] = primary_key

    @builtins.property
    def column(self) -> typing.Optional[builtins.str]:
        '''Column name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        '''
        result = self._values.get("column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''The PostgreSQL data type. Full data types list can be found here: https://www.postgresql.org/docs/current/datatype.html.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nullable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the column can accept a null value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#nullable DatastreamStream#nullable}
        '''
        result = self._values.get("nullable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ordinal_position(self) -> typing.Optional[jsii.Number]:
        '''The ordinal position of the column in the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#ordinal_position DatastreamStream#ordinal_position}
        '''
        result = self._values.get("ordinal_position")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the column represents a primary key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#primary_key DatastreamStream#primary_key}
        '''
        result = self._values.get("primary_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef04a0c014385d2c209f3da6a623816a874c841481d14904d4f9187a4cfc609b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea826ec199642ee0a51c75cf6dd6ca47009abc3935decc770a26888c99c6ed72)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030b83425a2ba9486f22179c05043ad49516a4779e3b1b1e31d9ba9b9f7b599a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f09f860ea8a8a28ba3cfe8121a9e3e375a7fd8294a76c65a2c9cf2e0361f4b12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d036c99c4fae01076de4c3375a21b54f1b8cc856be8f7310ee83109229e49ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7439f5c081522846d917486d9fbd96d1d35e5775dfa441cc96542f64dc382d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__243128e00b60466a942673510ba2a3300ad883704b2f428e7c90053a57157f5f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetColumn")
    def reset_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumn", []))

    @jsii.member(jsii_name="resetDataType")
    def reset_data_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataType", []))

    @jsii.member(jsii_name="resetNullable")
    def reset_nullable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullable", []))

    @jsii.member(jsii_name="resetOrdinalPosition")
    def reset_ordinal_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrdinalPosition", []))

    @jsii.member(jsii_name="resetPrimaryKey")
    def reset_primary_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryKey", []))

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "length"))

    @builtins.property
    @jsii.member(jsii_name="precision")
    def precision(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precision"))

    @builtins.property
    @jsii.member(jsii_name="scale")
    def scale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scale"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypeInput")
    def data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nullableInput")
    def nullable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nullableInput"))

    @builtins.property
    @jsii.member(jsii_name="ordinalPositionInput")
    def ordinal_position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ordinalPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeyInput")
    def primary_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "column"))

    @column.setter
    def column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362215eb43066e56c57a2e2144e738d3eac0f00dbbd2bb37ff2821de3eedd6c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d54812ebd7719ec878053f096d4d3e52b51a4a9f3d6a02572ccd13f5faf6970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="nullable")
    def nullable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nullable"))

    @nullable.setter
    def nullable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8abf4622f951c65e3b1e59860e1ef3a9fb407297a14a0e24bd34f7bad0eed553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullable", value)

    @builtins.property
    @jsii.member(jsii_name="ordinalPosition")
    def ordinal_position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ordinalPosition"))

    @ordinal_position.setter
    def ordinal_position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de6cf4e49fde26b2289371fd8f6952f400d9cffd1497f14d9b9cabc5868118d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ordinalPosition", value)

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324ccf449e55a55c67750e18ab58674f84d3a802e68586c2a3688a948ca95309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9254610cee63395a9b11efc47dfe1833f44245614f743080f287e96a04270ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects",
    jsii_struct_bases=[],
    name_mapping={"postgresql_schemas": "postgresqlSchemas"},
)
class DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects:
    def __init__(
        self,
        *,
        postgresql_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param postgresql_schemas: postgresql_schemas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_schemas DatastreamStream#postgresql_schemas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f7adaa67649e1976351c67bcedc084b0713a4c0b17fb83475b46c2487eebf04)
            check_type(argname="argument postgresql_schemas", value=postgresql_schemas, expected_type=type_hints["postgresql_schemas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "postgresql_schemas": postgresql_schemas,
        }

    @builtins.property
    def postgresql_schemas(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas"]]:
        '''postgresql_schemas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_schemas DatastreamStream#postgresql_schemas}
        '''
        result = self._values.get("postgresql_schemas")
        assert result is not None, "Required property 'postgresql_schemas' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5afcb6b2939a8b8941d83641c5505d2c400869f467cc66c42650a262ed2e68f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPostgresqlSchemas")
    def put_postgresql_schemas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__206e6f25a281e69c94ecdf8b9f4b1caa0b9f4a8cd23bc34424f1e577c8b0c916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostgresqlSchemas", [value]))

    @builtins.property
    @jsii.member(jsii_name="postgresqlSchemas")
    def postgresql_schemas(
        self,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasList":
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasList", jsii.get(self, "postgresqlSchemas"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlSchemasInput")
    def postgresql_schemas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas"]]], jsii.get(self, "postgresqlSchemasInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7140c5c71e1c2077933fe8e2bcd0b8959e47df163fb2b6a6ac6e17ae8d83af59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas",
    jsii_struct_bases=[],
    name_mapping={"schema": "schema", "postgresql_tables": "postgresqlTables"},
)
class DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas:
    def __init__(
        self,
        *,
        schema: builtins.str,
        postgresql_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param schema: Database name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema DatastreamStream#schema}
        :param postgresql_tables: postgresql_tables block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_tables DatastreamStream#postgresql_tables}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b11c8d59487df288de0eab416f4420c68f3fc68777e379ca17e0a52ed052b6)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument postgresql_tables", value=postgresql_tables, expected_type=type_hints["postgresql_tables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema": schema,
        }
        if postgresql_tables is not None:
            self._values["postgresql_tables"] = postgresql_tables

    @builtins.property
    def schema(self) -> builtins.str:
        '''Database name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#schema DatastreamStream#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postgresql_tables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables"]]]:
        '''postgresql_tables block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_tables DatastreamStream#postgresql_tables}
        '''
        result = self._values.get("postgresql_tables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec365f7b486a7ce93037839da46cdd490779fb7b1aab14c26db7f59efbfb9838)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1151a202024a70a5339007fa7de1042605eb219bea2eb9b76aa0debcf34eb8a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d30b5ab2761e7aa153e35bd65a25770ed830942339f276fc4471012dd9d351)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f57fb51b68ec2f633c8dbb2e251fd2f8a6f273930865ec195a37930004be054)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b41036e47ba656f3839ae37757506742a9fce5ac82cf2f89f0836e3898db6c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b862ef08d82bc4a359b09d9017d11cb69c206dd3d26dc1eecd421f38e4514170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af65c7a7b829a2210cd218579cba307f37f8d79f197d608714a368d24d558c9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPostgresqlTables")
    def put_postgresql_tables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299d16d60f45da06f827cadd55b9d56b76dd2c22d309ecbb6494d930bce9216d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostgresqlTables", [value]))

    @jsii.member(jsii_name="resetPostgresqlTables")
    def reset_postgresql_tables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresqlTables", []))

    @builtins.property
    @jsii.member(jsii_name="postgresqlTables")
    def postgresql_tables(
        self,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesList":
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesList", jsii.get(self, "postgresqlTables"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlTablesInput")
    def postgresql_tables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables"]]], jsii.get(self, "postgresqlTablesInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6eff8bec242627d24ff3be25a70b30ea7fb7c5511aa4c35b50f092ba8ddb6b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5e34079ca356e37b56017b018c1ea06aea957227f84e64f837243649b4da8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables",
    jsii_struct_bases=[],
    name_mapping={"table": "table", "postgresql_columns": "postgresqlColumns"},
)
class DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables:
    def __init__(
        self,
        *,
        table: builtins.str,
        postgresql_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param table: Table name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        :param postgresql_columns: postgresql_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_columns DatastreamStream#postgresql_columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54458fd67a11ba7a7fb7bb7a52b36133b0d69d19eec2d3160e0915a5d4ec268c)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument postgresql_columns", value=postgresql_columns, expected_type=type_hints["postgresql_columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if postgresql_columns is not None:
            self._values["postgresql_columns"] = postgresql_columns

    @builtins.property
    def table(self) -> builtins.str:
        '''Table name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#table DatastreamStream#table}
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postgresql_columns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns"]]]:
        '''postgresql_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_columns DatastreamStream#postgresql_columns}
        '''
        result = self._values.get("postgresql_columns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e704c0d57a82331547113c924f94d96a053e31f59611f6c56398248b2052648)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb85a5e31393e12b2a9cbe991a97e0fc1779d968af0a56008cdda44eb7f91a2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef98fff90b91ea8d6138580e82dd68bd83982f8c58050ab7ce72ec35159510e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb57664fdfc4857cd6006388101e8ef490829b0a806d076b51592c30ee086437)
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
            type_hints = typing.get_type_hints(_typecheckingstub__997f2835f315c813b833431c010bad4397181b711866690bd353992d112dce7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e5292682b68f99e8e9f29d6049a0ad814d3e831bc1159b02bf0ef096c14f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b4476c8ccdf495c930f0ed8c2095ae099d5e875f711666a2221e98cde60869e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPostgresqlColumns")
    def put_postgresql_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e802654023a08543ccfcb5caf12e874cbab741f982ad53e987c7e1594e0c450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostgresqlColumns", [value]))

    @jsii.member(jsii_name="resetPostgresqlColumns")
    def reset_postgresql_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresqlColumns", []))

    @builtins.property
    @jsii.member(jsii_name="postgresqlColumns")
    def postgresql_columns(
        self,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList":
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList", jsii.get(self, "postgresqlColumns"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlColumnsInput")
    def postgresql_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns"]]], jsii.get(self, "postgresqlColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ddc44e9638d2dc2498dd59a07ff49b34cbc06ab41c6406a89342dfe0cafb0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0037aac2ea63309fd227cb161340b2a225d02b4342b47639a8c9d96d4379500f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "data_type": "dataType",
        "nullable": "nullable",
        "ordinal_position": "ordinalPosition",
        "primary_key": "primaryKey",
    },
)
class DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns:
    def __init__(
        self,
        *,
        column: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ordinal_position: typing.Optional[jsii.Number] = None,
        primary_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param column: Column name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        :param data_type: The PostgreSQL data type. Full data types list can be found here: https://www.postgresql.org/docs/current/datatype.html. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        :param nullable: Whether or not the column can accept a null value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#nullable DatastreamStream#nullable}
        :param ordinal_position: The ordinal position of the column in the table. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#ordinal_position DatastreamStream#ordinal_position}
        :param primary_key: Whether or not the column represents a primary key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#primary_key DatastreamStream#primary_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac103eb25ec158e91d1f472b0c3fcde897a9e317acae8ab7ff6ac6ff1fb86cc)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument nullable", value=nullable, expected_type=type_hints["nullable"])
            check_type(argname="argument ordinal_position", value=ordinal_position, expected_type=type_hints["ordinal_position"])
            check_type(argname="argument primary_key", value=primary_key, expected_type=type_hints["primary_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column is not None:
            self._values["column"] = column
        if data_type is not None:
            self._values["data_type"] = data_type
        if nullable is not None:
            self._values["nullable"] = nullable
        if ordinal_position is not None:
            self._values["ordinal_position"] = ordinal_position
        if primary_key is not None:
            self._values["primary_key"] = primary_key

    @builtins.property
    def column(self) -> typing.Optional[builtins.str]:
        '''Column name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#column DatastreamStream#column}
        '''
        result = self._values.get("column")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''The PostgreSQL data type. Full data types list can be found here: https://www.postgresql.org/docs/current/datatype.html.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#data_type DatastreamStream#data_type}
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nullable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the column can accept a null value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#nullable DatastreamStream#nullable}
        '''
        result = self._values.get("nullable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ordinal_position(self) -> typing.Optional[jsii.Number]:
        '''The ordinal position of the column in the table.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#ordinal_position DatastreamStream#ordinal_position}
        '''
        result = self._values.get("ordinal_position")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def primary_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether or not the column represents a primary key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#primary_key DatastreamStream#primary_key}
        '''
        result = self._values.get("primary_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cdd4e14779328acd034f0e48467679984e96ad0e9ec8ab874f8fc26bb5ae023)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139f380c8a2a7f11497764b9f1e4a26e7af626c615f8ca8b64c33fdb2de2561f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d331926042e584190a4b1d1ab9c0c04460d61c236801b0f34adcff6bd40436)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9957321f2b5877f34b13f78bdda36926d8e6f4c1b8eb863c47b524bed92974b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95f9672d5b80d7516ed166a52f5db3ed107c83442d4bd2194cfeb447f04acf2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5788974ded18b6418a1b3ee51c1619a216737a95bb3f399e91a453ebe9d648)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab20bfccb60c33a63f92e2f108d0ee3942f67f5c929633794ac147bac199447a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetColumn")
    def reset_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumn", []))

    @jsii.member(jsii_name="resetDataType")
    def reset_data_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataType", []))

    @jsii.member(jsii_name="resetNullable")
    def reset_nullable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullable", []))

    @jsii.member(jsii_name="resetOrdinalPosition")
    def reset_ordinal_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrdinalPosition", []))

    @jsii.member(jsii_name="resetPrimaryKey")
    def reset_primary_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryKey", []))

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "length"))

    @builtins.property
    @jsii.member(jsii_name="precision")
    def precision(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precision"))

    @builtins.property
    @jsii.member(jsii_name="scale")
    def scale(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scale"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypeInput")
    def data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nullableInput")
    def nullable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nullableInput"))

    @builtins.property
    @jsii.member(jsii_name="ordinalPositionInput")
    def ordinal_position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ordinalPositionInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryKeyInput")
    def primary_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "column"))

    @column.setter
    def column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3316fab863f6a2ae245c53cf2a26b767b6e5339e06f55ae7295a965fab5c6822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3405fb0182b8d7d5188c2db9630f62d70a4dc228b755deed333d8be7d6a3536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value)

    @builtins.property
    @jsii.member(jsii_name="nullable")
    def nullable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nullable"))

    @nullable.setter
    def nullable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500b57364f878bd70b190ad543d01439f0b66e89b5bc368d66b4a27d17dd66d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullable", value)

    @builtins.property
    @jsii.member(jsii_name="ordinalPosition")
    def ordinal_position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ordinalPosition"))

    @ordinal_position.setter
    def ordinal_position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc542fdc39eaff8adf8558a62b5bda66ac3e0546c71c4593f87457e3a1a3d95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ordinalPosition", value)

    @builtins.property
    @jsii.member(jsii_name="primaryKey")
    def primary_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "primaryKey"))

    @primary_key.setter
    def primary_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7bc5d875b9afba5e60a79a039217bfda6fc79f13749f2b73ec9e4bdc457309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025c38c00b2fb22abee7213b4c6cc19a9ff39a0e84847af80f0b5cbae17832d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatastreamStreamSourceConfigPostgresqlSourceConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamSourceConfigPostgresqlSourceConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__090a22021896a3c9f68df6b699b4023bf4798f24491f66907634a5cd6dac2be5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExcludeObjects")
    def put_exclude_objects(
        self,
        *,
        postgresql_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param postgresql_schemas: postgresql_schemas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_schemas DatastreamStream#postgresql_schemas}
        '''
        value = DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects(
            postgresql_schemas=postgresql_schemas
        )

        return typing.cast(None, jsii.invoke(self, "putExcludeObjects", [value]))

    @jsii.member(jsii_name="putIncludeObjects")
    def put_include_objects(
        self,
        *,
        postgresql_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param postgresql_schemas: postgresql_schemas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#postgresql_schemas DatastreamStream#postgresql_schemas}
        '''
        value = DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects(
            postgresql_schemas=postgresql_schemas
        )

        return typing.cast(None, jsii.invoke(self, "putIncludeObjects", [value]))

    @jsii.member(jsii_name="resetExcludeObjects")
    def reset_exclude_objects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeObjects", []))

    @jsii.member(jsii_name="resetIncludeObjects")
    def reset_include_objects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeObjects", []))

    @jsii.member(jsii_name="resetMaxConcurrentBackfillTasks")
    def reset_max_concurrent_backfill_tasks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConcurrentBackfillTasks", []))

    @builtins.property
    @jsii.member(jsii_name="excludeObjects")
    def exclude_objects(
        self,
    ) -> DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsOutputReference:
        return typing.cast(DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsOutputReference, jsii.get(self, "excludeObjects"))

    @builtins.property
    @jsii.member(jsii_name="includeObjects")
    def include_objects(
        self,
    ) -> DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsOutputReference:
        return typing.cast(DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsOutputReference, jsii.get(self, "includeObjects"))

    @builtins.property
    @jsii.member(jsii_name="excludeObjectsInput")
    def exclude_objects_input(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects], jsii.get(self, "excludeObjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeObjectsInput")
    def include_objects_input(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects], jsii.get(self, "includeObjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentBackfillTasksInput")
    def max_concurrent_backfill_tasks_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConcurrentBackfillTasksInput"))

    @builtins.property
    @jsii.member(jsii_name="publicationInput")
    def publication_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicationInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationSlotInput")
    def replication_slot_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicationSlotInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConcurrentBackfillTasks")
    def max_concurrent_backfill_tasks(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConcurrentBackfillTasks"))

    @max_concurrent_backfill_tasks.setter
    def max_concurrent_backfill_tasks(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649a3b0114c010e781ec3cdc70b02b8b3b55fcbca0ddbffc7ba821c422ab3bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConcurrentBackfillTasks", value)

    @builtins.property
    @jsii.member(jsii_name="publication")
    def publication(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publication"))

    @publication.setter
    def publication(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a9a23875cfb632cebade6e105926e406fe8044e0694f0c30fc491fdeb54b15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publication", value)

    @builtins.property
    @jsii.member(jsii_name="replicationSlot")
    def replication_slot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicationSlot"))

    @replication_slot.setter
    def replication_slot(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1afd38698baeac2a5b25401337bbcb1f4c07530c88e4b96d80f11be57246e515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationSlot", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfig]:
        return typing.cast(typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f7144d99c1126a43c10d1fd66f0e7d8a88209b24a4f3dd917c0dc6c69201d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DatastreamStreamTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#create DatastreamStream#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#delete DatastreamStream#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#update DatastreamStream#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3c43d69f12289839f31d381d72fc17e555fa583862cecacfb6539c6d58e6e9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#create DatastreamStream#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#delete DatastreamStream#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/datastream_stream#update DatastreamStream#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatastreamStreamTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatastreamStreamTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.datastreamStream.DatastreamStreamTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cac18995955222a43bb9b35c0136372f39bb89f568cf37a95aa304a07adf928)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8643526e3db645744eade7d744fa2156e3d4720ede8a3f92d13bb328ce9c950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfbc2b3312d9160fbb91182305e5ed12d586cd6f792084f07eadff56090eb376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd7cdc806265f3b7a72b6ee739412e8ca9ccb9efa8c1e3155c46a10919fe0c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__201682a522c85e6608f5a77eb390ed891ff39af25038c474f9af88101c6414a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DatastreamStream",
    "DatastreamStreamBackfillAll",
    "DatastreamStreamBackfillAllMysqlExcludedObjects",
    "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases",
    "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesList",
    "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables",
    "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesList",
    "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns",
    "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumnsList",
    "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference",
    "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesOutputReference",
    "DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesOutputReference",
    "DatastreamStreamBackfillAllMysqlExcludedObjectsOutputReference",
    "DatastreamStreamBackfillAllOracleExcludedObjects",
    "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas",
    "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasList",
    "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables",
    "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesList",
    "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns",
    "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumnsList",
    "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumnsOutputReference",
    "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOutputReference",
    "DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOutputReference",
    "DatastreamStreamBackfillAllOracleExcludedObjectsOutputReference",
    "DatastreamStreamBackfillAllOutputReference",
    "DatastreamStreamBackfillAllPostgresqlExcludedObjects",
    "DatastreamStreamBackfillAllPostgresqlExcludedObjectsOutputReference",
    "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas",
    "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasList",
    "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasOutputReference",
    "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables",
    "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesList",
    "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesOutputReference",
    "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns",
    "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList",
    "DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference",
    "DatastreamStreamBackfillNone",
    "DatastreamStreamBackfillNoneOutputReference",
    "DatastreamStreamConfig",
    "DatastreamStreamDestinationConfig",
    "DatastreamStreamDestinationConfigBigqueryDestinationConfig",
    "DatastreamStreamDestinationConfigBigqueryDestinationConfigOutputReference",
    "DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset",
    "DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDatasetOutputReference",
    "DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets",
    "DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate",
    "DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplateOutputReference",
    "DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsOutputReference",
    "DatastreamStreamDestinationConfigGcsDestinationConfig",
    "DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat",
    "DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormatOutputReference",
    "DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat",
    "DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormatOutputReference",
    "DatastreamStreamDestinationConfigGcsDestinationConfigOutputReference",
    "DatastreamStreamDestinationConfigOutputReference",
    "DatastreamStreamSourceConfig",
    "DatastreamStreamSourceConfigMysqlSourceConfig",
    "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects",
    "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases",
    "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesList",
    "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables",
    "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesList",
    "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns",
    "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsList",
    "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference",
    "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesOutputReference",
    "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesOutputReference",
    "DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsOutputReference",
    "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects",
    "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases",
    "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesList",
    "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables",
    "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesList",
    "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns",
    "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsList",
    "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumnsOutputReference",
    "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesOutputReference",
    "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesOutputReference",
    "DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsOutputReference",
    "DatastreamStreamSourceConfigMysqlSourceConfigOutputReference",
    "DatastreamStreamSourceConfigOracleSourceConfig",
    "DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects",
    "DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjectsOutputReference",
    "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects",
    "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas",
    "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasList",
    "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables",
    "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesList",
    "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns",
    "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumnsList",
    "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumnsOutputReference",
    "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOutputReference",
    "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOutputReference",
    "DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOutputReference",
    "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects",
    "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas",
    "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasList",
    "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables",
    "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesList",
    "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns",
    "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumnsList",
    "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumnsOutputReference",
    "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOutputReference",
    "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOutputReference",
    "DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOutputReference",
    "DatastreamStreamSourceConfigOracleSourceConfigOutputReference",
    "DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects",
    "DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjectsOutputReference",
    "DatastreamStreamSourceConfigOutputReference",
    "DatastreamStreamSourceConfigPostgresqlSourceConfig",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsOutputReference",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasList",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasOutputReference",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesList",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesOutputReference",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsOutputReference",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasList",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasOutputReference",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesList",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesOutputReference",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsList",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumnsOutputReference",
    "DatastreamStreamSourceConfigPostgresqlSourceConfigOutputReference",
    "DatastreamStreamTimeouts",
    "DatastreamStreamTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6c3ae3a9775ec6a2f34ba62bb34fac9132ef80c080cb4f5fc8bb6686d10ac590(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination_config: typing.Union[DatastreamStreamDestinationConfig, typing.Dict[builtins.str, typing.Any]],
    display_name: builtins.str,
    location: builtins.str,
    source_config: typing.Union[DatastreamStreamSourceConfig, typing.Dict[builtins.str, typing.Any]],
    stream_id: builtins.str,
    backfill_all: typing.Optional[typing.Union[DatastreamStreamBackfillAll, typing.Dict[builtins.str, typing.Any]]] = None,
    backfill_none: typing.Optional[typing.Union[DatastreamStreamBackfillNone, typing.Dict[builtins.str, typing.Any]]] = None,
    customer_managed_encryption_key: typing.Optional[builtins.str] = None,
    desired_state: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DatastreamStreamTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4036af7d4997077ed9ef564c0f1c741942d81794bc5f2f2e42aaa87939e5b13a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52394fe12c454915c68b7f5c0e1158a297c28bf8edc5470752d8d03bdadb3ff5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075bf1e3249baeb8aa177ed19b3f502beb142b110c60b7139a705093ce1b0a7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f951eeadca73ea4a620fa2306732bbea40433c714d9c7f9ff106a61a7faead(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef205b5c5ab66f32171c7535e21c4e68b81ebab105a33f1ff35977ad01202a1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf79e1cbe57e9eb4ed393c90fd467db45153af81195ed412bfacee8feaa28a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643d9836b9fc11f1901e2a2838ff876acef8280f6554dd37d2d02fa890104d78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283627036b55d75a53badb063b8cbdcac874d10da468b6abae149456f4ed27d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548fd10e905731875c7b597865e08230b888f6d65781f1f9e58cc54902b013a8(
    *,
    mysql_excluded_objects: typing.Optional[typing.Union[DatastreamStreamBackfillAllMysqlExcludedObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle_excluded_objects: typing.Optional[typing.Union[DatastreamStreamBackfillAllOracleExcludedObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql_excluded_objects: typing.Optional[typing.Union[DatastreamStreamBackfillAllPostgresqlExcludedObjects, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c73ea13a69e84cb5c059ba0260ae859d8c602b57e97a85cc24ad93dfc88b5f(
    *,
    mysql_databases: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13410b2bfcca2c97647224c4a67319d908e9d319c6a9237cc85a4e41f55b548f(
    *,
    database: builtins.str,
    mysql_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea67c8ef97a0bde8fc840322d14b0b15cad0751a347171e7dc7803d39cec09bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e433a44dd8df3a9cadc62af5b456b9bc010f04b3ba73bafaf04a805db07586db(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3201f4411b84a193a6646dd047aa80f26f7dde220aef2aef705c5287e252e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c44068e63d483ac615dac0b8b6f39ba7905423e373797afbe8cc55e6cd75e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ae6f5b98dab77299fa101efba9a44e8d9bd7f7ad9211e91cba088aa6c700ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aebbfa9a89be0456ea53147d93d92bf800659d380f16345317d1f06cc039aa0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c949b7e6ad7f4b38807ff06c703f595dfd880a47c4b1d04b04a3915dec77355a(
    *,
    table: builtins.str,
    mysql_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e065db95f692750c0a4063feef0b9379251d390020ae9aa8597c39b18492722e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71340320398dcd9797361c897dd802615c2838318ad836b9a8a7a371389ce73(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fae007e595a16d2276fc86cc2a375a7ac4c4e4fdf0b5e9c3807728d0312608d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f42f8dee5cb9de65146de9913d0470c79954bff38cb9237b2821934c9d38ba3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09927ad10009415e1a205ef82c502175614a7e64824510e9b69fbf9eec02feb4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0487084e9cacd7c8d5ac7a0aa828f1cf005979ca02f03bd6ac2db3f9e309f1c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358f467e5b0f4377a34511fe2df79cd3ce7c42608d71ea9bc665657743281de9(
    *,
    collation: typing.Optional[builtins.str] = None,
    column: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ordinal_position: typing.Optional[jsii.Number] = None,
    primary_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154f8dbef744b6d64d4b273c1aee6e622e76745c185fc129b20166f1d3b1983d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713d5e717689a63ec3720f83c87565cadea875f763aa9cc85738d05e657e219d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa9e390d9ad10ccedd8763652c1adc0808202e386abbe93d623f621504e76ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9301374e73e0c50562a61bc71b8dd7a070d34619dda616483dea5909e9f46f98(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c7b000f7d51a6d417fbacbfba2f039c7d7c3eb9281b41955951acec133650c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5df9305e59f038bfd61176fa4734ffa910d0bf7dee993b79f7d55c7529c3a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f018984efb7d263d0ffcb99493054e866b0c5304311041e893283f901e4a6c5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a552d16c9eeee74bbdd4efdd9298e085ed23856eae9264a8b1de5d65bc128c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef3bcf0cf613c3945de3f7f965b20939420613dbf0bda0a777109acd57296b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ccd286da9f0d1f1989f8eff655c80e6b67fe37f7ff035a8f81704b1c1948fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42f8e7181c09785a11ef026e085afe5bbd15bce5111673479bccb9c3566cc49(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097daa092a18ee02bf8669de9bd114d35e6fadb3ea65a486cabfd5b2425b3f73(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4cd8ea957cbc5045edf6e2553556a3e684a0ab60fb1a5fa3c7c003e727ee3f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e079a8c2bf48a82f26ea7ebb4307d6a05b485fc96ce3f041b43af86038484f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a74c6f0174c2f917092188e7a5baac1b4376e817d30c3ddac8bfdd08ace52b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9d4d13b08ecd8dfe67092ac6f87dde17666a854de010456318e3bdd9e068bd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTablesMysqlColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0e90b83d1fa5fa9212c0d7bb6231593356596ff82ad67b135f440e2c462282(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0b4e25f18b8e00271d40dc319fa34c7902a7c2c0ad6fd321f7f236706f10f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5f8347e6725fe1f7f0267f7c851ffb9628cb21ac0e30564b95091505abfc30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f814fec22f6e810871992154543a73b1af75cbbc27447a3fe884a5a80fb50c9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabasesMysqlTables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3151b274792b3f93fe09adbe180c158913e6bd5db0b114d7f42e9a220f02a568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7388148daab50b0ac722ba039b4763c332b0cf752fb7ecd0b82947dc468abe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1d7a4d992a763ac519977aaaad6c758ee59d5bab019a7a7745a4616285a28d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931bbf966cb9ba2aae819fbebe1786809f88f7da77ce8346aaffbdcfad968a76(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllMysqlExcludedObjectsMysqlDatabases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811433edaf8b7400da4083dd0803cdd680452b065b43ce1320c11977ab1cc96f(
    value: typing.Optional[DatastreamStreamBackfillAllMysqlExcludedObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52841f107f2901aed8657e6d83ecd50347ad8033afa7608787869317a9404e84(
    *,
    oracle_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd4c08a9f3b5ad8460edfca3f7a1b7d1afffd9086a76a540f6a0d44ba83090b(
    *,
    schema: builtins.str,
    oracle_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b730e1c71b3d87311c7d6e18f194c7b92727ab9013b980ce066c20ceeb195a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c38f1129acd1f802d161834b127dff5511d9274793b93a7339ad22df7c9d0dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd09e5cf8228cfb704103b56fa935016916c13a3720f7c5a0d624e991afe05a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c358908b37412b7eeaaf4391bcd8f0639b6ae2ab10ae432f528556a7579fef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0178be83df611c9f9d4e3620e0325a5204db08445243d5c32db345e4aa9d4d61(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8516cb522db34e652278d419ed5c8c8d73f2ceb8396840414a6ea84d47e9aa63(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6e5fd7422aa55104fff2e8bd7a46cdfb59e556c32cba3834202b15f50f8fad(
    *,
    table: builtins.str,
    oracle_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b601d2c5879f402a0f0af8f32fde94cb7d97c0e7b6fcfc44d0400bd7b1f9368(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe2d2a1750b59df90fecb23008d497068e2681a6556df293a4576b3d1e9617e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221165e97b7f1cfaab37a2f8114648611153e7e2533817cb1fe14ee71beadbbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0780eb9549db2b16ec6411b4a414a188205bdcf10f4c8f761be5f0c18211985d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21a5d7db789059655cc63684fd9cc2b0a60b8b421b5cc716120649a09e05c666(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4a8dfc23cafff0057053b2818a5db1e1bbb5d18919e9e12b98927ae00d224e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6180aa03e8588ed9b998f6efddb3ea71242d914242ab52fbb62859344c922b86(
    *,
    column: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f96ab2af89fe82e13e2618ceb77fae34f255d26b210edfded1f673dfc8b1725(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb98c67d7153e6a46a49fb3e128845124be743fc02b472fc8d637d9a83f4d97(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db03e6756fdc892ded71af92b1d8dcec8c8bb3ecc246034669d24485d6608fe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d41f3bf440f4f1744a43c9ea7da7c63e9f6ced42fc2ef520ae1a9c6f02d27bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cecf0a0710927b872b4671b43df83560ff52917e6d85bfe8b8886066eae4a2de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcde6766fd17cbf1bc355d4b9e85ba292fad4a44bb9b6e39b6dc4fa55f5fa02b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e717b10e4a0340f61a74762e1f694b2dcda7958a943e00da21284498701dbfa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489b4bd1c3dcccee0bcc7eaea45211034532a13eff1cb863fc4ee8e62bb03b8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08279d3ce3e352e760b9f3c0e6fb6c61808901c8f96666f27b8ae26b88ca57f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00ef7590783646406570c2cd5497558d376a91c651285790776f0431fd23846(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7d3b45930bf61a809ca9a4520c09604ef3300bce2cdd2e27209c968602d389(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d95ce9e328cae540a5475f8dc661f64120261cfb4ee494ab0e4d95c7ba15f7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTablesOracleColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b01affeee65683f918cc0495d19037bca6da50345d62121f3e9c53bd631a12de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0957ea6c2099733147a731e6706eb8c70302512e3c0f28f85e95013b4979f268(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a6c8678ab8ea6e85611fd5f16e42fc7138f31006eef3ff96ebef0aa53dc7ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8155c19b5637412b8082acce6c37d407af21301ef8e768af1eb577f104abac4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemasOracleTables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c8f07606f3b0fe32f7948b686a3527c1ac821feb0e31ba8c1487b5c8c15ef9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0346b7769948dfb8faf4ed88fc5d7fffbf9c366c551b7b458354814c8f58cf03(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c56e72c4b87c7e975fc8d7fe6236ced1cf9d249ca9d0372b050fae435f77e2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3104458a1514472f120a6dc45e490d9d9f6ca896252b02cf906aed81ae8a86(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllOracleExcludedObjectsOracleSchemas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869aabaa7ffdcaa3cfdda51ef3e63dc256c8f0e282655311636f024ec823cdad(
    value: typing.Optional[DatastreamStreamBackfillAllOracleExcludedObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2165189e7c8f1b458755c804ed55962f85c000ded00d4c56f68f9f3bcf3eb1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5097bf84b7756c5e909c8358f325e4cc1c90362407525d463c71a947058c4a(
    value: typing.Optional[DatastreamStreamBackfillAll],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44a84d805c486bcce836837e5e3b6e5c71eb27c894f3f86e12e0e4a10918402(
    *,
    postgresql_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d193e63a6456924ddd6ebeaf1e10b8e6172fb03c7a36235a89684ee580ba9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5339414b6165e4bbae405e61c1e04bc62a2947807fd8f3a84191915855a3c5b5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__254351ab6a7759c2179a6ea2bab099c63244ca754b27f5241f170a74994ea22e(
    value: typing.Optional[DatastreamStreamBackfillAllPostgresqlExcludedObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df8dc73a481bee6b7964b79f757d11e83823496223a34981f463a4cf6e79456(
    *,
    schema: builtins.str,
    postgresql_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d56235ed2088958ea8c3451888e566f4f2d110ee0c3ebfeb29ad7ad4ddc584(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11fd39cc07b3833c49e5c2a1b85143bcde2b5c9d81e5a900bcdc531e2838c8f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c8ef4372afb1ac7c0961bebc56e337fbf100540bc7c90cf45029ff9ca302c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b46de3f2533f76f63b416ccdea2c5f48d439e063252f25fdacca87ffe3f275f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e09ce28567d48d53e9a98cd34a8b9b84dd48c3e7c79166e3976d9d2c7ba9c19f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857a0b75341a2930edf5b697dfee8f37da9eb5997d83d07e46013d21fb9d3668(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac354a35a65f18e1f09a228a0090b838790a8d3ea570e113dea82dba47c7b3fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed8db8077edd3df844e7f2a9697d1c649bbd53167262c0a232bf77ff7900482(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24cee6080160f8ce254f6881577a90050147bfc60656b23c6fbe0f54bc3f422a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc3004bc21f83e386c87081400d9180d9ff84833997649c90bbbdc9f18ce4b6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0895eb06a7e0758e0a81197c2088b2bfab18a75e235f1152f8f4bdc5d1af89(
    *,
    table: builtins.str,
    postgresql_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e95e0645f052681248d5f6cc5094ea5f95b7f8de8ff3465d234f60bf4042a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642c17323e5280f2ee99185d2b50e23b7add47646f081bc4842a7ffbb73ebd7a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edcd5f836cc42fe03c692f748fc2d920d5932755ddc314336be058230ea684c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5eeca4447782fad94dcb91015e095041bd52e956ca9dd6c407ef9f2f61f52a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b599079b0745008056cef2bf2c77bfc173240f26b61dc3d2f85e480f6c578bc7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c3349a6f844f806dcb04667db73c0d4ca6c84ce0bb984fe2e395b831b95191(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1892a8ca0dc0b58b4ff6af8064b15bd4559caccd93f4647b71af0d8e30c9ec7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceba9c3502f3560119783ac581c7b6ed48cad64f8568c6e4cc10c625b550de03(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5fe1aaeec0dfc894679a8d067bc8f2e2761a7ec03843f8de7819762bd2ebd17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34625c3cc8fdf881fe83f3c0811e35ce077ccd80c6cb30cc70dd8489927e3e2a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6463b08efcf4f8acf83305a38b96396d3a21da2198ee85184519a76045993efe(
    *,
    column: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ordinal_position: typing.Optional[jsii.Number] = None,
    primary_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7218819eda5b9a7f7f7e44a80cb3e0e13028356373d6f41d59b04004bccbf214(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d9323b07a975fc21e6a0daee1d5e5a4cc882edea83fed3ef9a577285c07002(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572ebff2009111e875933582601c2a38fb018cf539d9b6cb3724050e7bc3da32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be69216e886a8be1bbe37eb47125134f68fbe7712b235469ef7c0dd071a786dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5beca11f8221e40508b6082b1dd689a96688d04b16d196d75e10de608b83080c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb02e7e5662cd9edd62463b927799f0ffde5141d2d0949dc56976a5d73425d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f543bf9cbfc914823e6469ca15226d83225e8ee9984684c8099a23956e44eff6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17b561141aa360019b953cb434356f3dfe360978276c1888f4a0e496cbdd45f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2e8a03f99750b80d586c143d765355ed78d4379b1cbb16899641ca6ddd00bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d67651ef84ce3863e6b8dbc30be73f92e014f372b0892c003535af3ac55bae(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088f45ef4903a052a86ca7276f66eda9910525fae8c5b559c39c22df9e3b8b04(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34fb414017282c760c6995b124b06445e6f0b81b4bf1ed455292cec3525167e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28ec56985ad7b5c5a334fcd6b700d3969c032094ec1c2d67f5e656907c81a9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamBackfillAllPostgresqlExcludedObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe33cc0ef94cf2a41dd327fc0be0593dc211e9743a24827b5ee773542c7a8c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af34f772ce61a51e2c5569138f820502f4470ede6042b4080b30aef00600f8a6(
    value: typing.Optional[DatastreamStreamBackfillNone],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010b9566f8020e188444914b63cda5178f17cff35ec3ccd2e68861aaf3a93e42(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination_config: typing.Union[DatastreamStreamDestinationConfig, typing.Dict[builtins.str, typing.Any]],
    display_name: builtins.str,
    location: builtins.str,
    source_config: typing.Union[DatastreamStreamSourceConfig, typing.Dict[builtins.str, typing.Any]],
    stream_id: builtins.str,
    backfill_all: typing.Optional[typing.Union[DatastreamStreamBackfillAll, typing.Dict[builtins.str, typing.Any]]] = None,
    backfill_none: typing.Optional[typing.Union[DatastreamStreamBackfillNone, typing.Dict[builtins.str, typing.Any]]] = None,
    customer_managed_encryption_key: typing.Optional[builtins.str] = None,
    desired_state: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DatastreamStreamTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f00248466cff6f376a67121eae26291d4773ff89be51d7e77bcce5aef3e183c(
    *,
    destination_connection_profile: builtins.str,
    bigquery_destination_config: typing.Optional[typing.Union[DatastreamStreamDestinationConfigBigqueryDestinationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs_destination_config: typing.Optional[typing.Union[DatastreamStreamDestinationConfigGcsDestinationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d3281f73805ef674d65a156cd694bf3f6a088663f008143e968719408b4685(
    *,
    data_freshness: typing.Optional[builtins.str] = None,
    single_target_dataset: typing.Optional[typing.Union[DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset, typing.Dict[builtins.str, typing.Any]]] = None,
    source_hierarchy_datasets: typing.Optional[typing.Union[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a8b609b22768f789ea3611aa0ef25787c5d73f4a59a9be4ef77efa3c492a81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b7da575aade1c71be6745c30a44eae934f6539e34ccd51a86b8facf00d5060(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10290314eb6f6d825712b6b3207d7da992e62e51fc0be399239f7e7d53e2f846(
    value: typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e44dd24643e8aa60468a62619c2ae48ae367e05d23c573afcfa2a6d3a4c91dd(
    *,
    dataset_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441adf3b7f63f750260d12b3416082c5faf64d5c7e1832c2a1046cb0a48d5538(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51999bc75c9b0fd3a12023b18a370bbc03175387133548ee3a57791a877640d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__268f1df491bfb370cbc33b522997f6031a2165748ce5ce4e0e09666537abd721(
    value: typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSingleTargetDataset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d309147145fe77e14e6be2ec7f8089a10173d914dfbdb30bdc6fed0fd183a299(
    *,
    dataset_template: typing.Union[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21923ae44eb0f0bb463b3690f3b8ab6ee48575a23420bfc03244d26df8ce50fc(
    *,
    location: builtins.str,
    dataset_id_prefix: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3e1a71a02260fed7254d25a21729daa348bde759c05a201e378a1427397ba5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12137ad883f1e8198a7e8a9d33112667f3a9d542fe239263ff41c443ac959f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2910e29339383be80b9bf3b4860a08c50c3fbf66efb48048711d4a03177ae393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f6a99aaed1e86235d35130b250c4ef94bbb8b532409fcb8b414027c2e8f90f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d649ea10fa687d496860280b0eb24cd52cc782d27783590f0680bfa4689aa1c(
    value: typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasetsDatasetTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57dd2ede080c713c2f1230e7c848e67a25284bcfc9dddcff5c0399b99b877959(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca05e8ee9521ac9812e47448dd7ed280d2aded497ee45b96dd7daca59deabbe(
    value: typing.Optional[DatastreamStreamDestinationConfigBigqueryDestinationConfigSourceHierarchyDatasets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6fe7bc7051957d6ef5b4a2c8ba1b43b7844b9948287f7a5f36e8a41e8cc412(
    *,
    avro_file_format: typing.Optional[typing.Union[DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    file_rotation_interval: typing.Optional[builtins.str] = None,
    file_rotation_mb: typing.Optional[jsii.Number] = None,
    json_file_format: typing.Optional[typing.Union[DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53992334d0a36b22747670910ec781eeb695714367669655fdf9bf4af1963833(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afaa1094b2bf96eb2aaa9a004fc98a4308a6190a94060ab74654bb2b416c437a(
    value: typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfigAvroFileFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c14e2cab90478a730fd4d9ac6ca6c8d7ba3f67ff802f4dcd2d5c9c08fb9803(
    *,
    compression: typing.Optional[builtins.str] = None,
    schema_file_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03cf334b7c9b733612b8ea0e5a5a7807c143ca675f4524c8a5e0e7755406bd56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded649c1e18a3afe723a46d8ef0cf7b3bd23261d1183fd169e1f378122c2eef7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4267f271d814121eca55dad65d9c3869f72e7c0df0c37798d71a0517c8e56d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a0efe2299c605431235b27746ddef41abdcec0e56eac6382ae8204a6a451f0(
    value: typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfigJsonFileFormat],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9a6d5e7f6df721016eecca5688540ca539f31acd6bda59a8493f4c20acd453(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97148b45365aadc2e39b6e2e4fccc374cdbca79b05f3f52571e08319d4ee9036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae1649d074402474b5d7bd00712aabfc874730cfff03823ae354457233f2608(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f182119df80ece606c9383959c86ab83e4448a8f8744859baad283fd405e45d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f01a9c52ede76f92056982b7da315f974384e0fb43ded2f1d40f4d8e1832207(
    value: typing.Optional[DatastreamStreamDestinationConfigGcsDestinationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f46069e1a4d2de7a3c29ede9cae6610ea00fcde99ec2ae63eab68dc303a751c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c51932c7c579a452dfb4bd688f68fa8208002be445062eda4e86430be29b96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c94d7479b7d04eadd4b49a8a517d1d766123d5a712238cd25314c50439da47d(
    value: typing.Optional[DatastreamStreamDestinationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995aa3d40c0014eb42472704f6e2a586227929c23daf612b5bc02630f522ee9c(
    *,
    source_connection_profile: builtins.str,
    mysql_source_config: typing.Optional[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    oracle_source_config: typing.Optional[typing.Union[DatastreamStreamSourceConfigOracleSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    postgresql_source_config: typing.Optional[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03986ed8942ca5af140f857a63fa4f9bf36dc4bc0034824c870a09ee77f3377f(
    *,
    exclude_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    include_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    max_concurrent_backfill_tasks: typing.Optional[jsii.Number] = None,
    max_concurrent_cdc_tasks: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8924ba08b53e76420d1040aea7107d9f8f4a35a42d203306a4dc5eef847746(
    *,
    mysql_databases: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47003e7f3dfe4568bdfbecbecdfeca8cc5c1dc824fd507147bcf69d0e11c8907(
    *,
    database: builtins.str,
    mysql_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad30ac80003dfb56e29240af179446ad988b2d56141cc9ac9173a417b271330(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e3be48b4d7ea91ea507468b666eb92e908b90eaa4b72909e6e563ba639959a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d098f2c688f84fafc6dd0afd35bf6d5c61a2a9469a607a83c9f3adea7ec6a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2024f15ee7b08a23d14347a6bf4886348cdd4fe08b134d84d142af2d64b50b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c0d3373e4a860d69ba9b1b96343c0a1a37400cad0c26a35d9976a03a2abbcf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2195e2190f719cbe019609d3ec53f80debd66c7511eec9350b50efae0d491363(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36fef275c6ec7b8d609cafa0d2641bd263c44a10bc7249473f713a05683ba4f4(
    *,
    table: builtins.str,
    mysql_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c33a987c9a7ecb67924cb1032a96cc931edf369e360ae95e58e1551d69b163(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2137ca458d7db27e59eaa11790cf81f0760027a1075e78cbd3fd912b7fdbfe53(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b152c3de915d6fc96d08112f4da3d2632e4a1feb8ed9a6e739b1e322d056eba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9761d0c70fb470dda84cafcf21d16c981695392477d4566b2b58631c6a17a85c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35fc4adff6fe3aeb36b4c144ff1bef8d8bfec907ca5fe8808db292d4698d710(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3b7e194a1b17a44374dff58788f3134ef276f1b232460d9f088bc36c194fbf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1d840e397f01a70c2cddb58c957e80c59d39fb16bbea2a1c04910d8abb0218(
    *,
    collation: typing.Optional[builtins.str] = None,
    column: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ordinal_position: typing.Optional[jsii.Number] = None,
    primary_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b934e1cd2f1b6e46749d3a3ee4ea123a5feab018bcbd9e1dc3d82577fc52b54d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0462a33c37e557fcf3c2fd74887a5508dff56bcde35fa593f04f4b8607580c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b5fb04fe528246556f11f40ffb8e2ce0da1af40d4741f1ba0bc113654bb796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ff55614afd8ecea5a474c3db78ec06d5d81fc6e8371a0cc4fb16372f124bf1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad32f42f77fac61d1715b212cb332883b311819b8cd438d36beb15bde86030dc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9320334886970de6c5ea55c48a2818daa32156be2f9f75dd5e042a36ad100d27(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc27762ed3847a2a4997c6417d746b2344e6ce7b9e40d4295c780394da67d35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10c35f21ec76d9b9b6f802e3565c8ba67ffd07a03db61a1a05cab01b31b5cd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e84862d7e010156638f260885c74211c45e9be7238c8249465e6db2a06d368(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a4831ac66409ce770fc99b6de33638206edf8c50979ecf8d0cc42c7b84f450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600dbdaafece9c5dbfc122b3a1509faf6dc3db4dd21050d0da9936f77db7d0e8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f73fe59063cff45a5fabe46cc5ef9301038e2ca51363160acfdd6ff6a518a7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64b2a7fe0df84f84031671b52e419f6be035d371a5bfd7fa6e4eed2354f0730f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2f92998ae8b6c8fd59179b9167917d5e06e3da0bf7f6a17d89c1a9d34958d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c7edf517db15210471252d18fb4c0295e1f6d17ac794c71b59dad9fa34cde3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a0c2eed43d5a92c7dd35f9d3b898447ed32f9260596e554f0bf82139dabb27(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTablesMysqlColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a802aba7a80609e781d874483717985a77c791a6d610d086e56342e5ebdfea4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a3c95f2945ef79610f226e7de8f82f4dd6c488b2cdea201b5adee9eb165a18(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__339d0233b5e3939582ec717c6235f70b3bcfce5011c933d1fa7b7b221a1b3f98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e753886968f6ad8529639aad8ba094d4d936e8fb59d04017d16679362ce906(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabasesMysqlTables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ddba99321e758ecfffe491c01f502472c59352bb67f1530bbaea001f0a7062(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e753e427d29d0ade6f4009149848849060b763be17e45608a15cca438775be09(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d8c032e45bf0ac57ac3d0979da5b6ffe8c1f99b09476d82280a9af84df9c6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc57f764ac9d739ecc943fad16909c32b76e6c97dea9a5df494ab6c104e29123(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjectsMysqlDatabases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b7210b8484ca8aea5f7a6f1596f56ef4c03fe2c76a48dee6597741f3c6ff5b(
    value: typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfigExcludeObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40db11a5bb1c2aca7472fd834428a2203489803a28b44b1e4962ad4ab1b66159(
    *,
    mysql_databases: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff4d778c3932f51b621c3ff1675a74882c85bb24341f2bf1594c06d9c82f36f(
    *,
    database: builtins.str,
    mysql_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade2a69c288d1345efb3bb511b247830dfd4432c1cd9cbefcabf6c9078c58dc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264cc6b382219d468fd08c237199dbe2f9c342a7f5890d61df2f62ee150f6ee4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43dfcfbaa01fb883388f2b178ba7a5408a426f709176123962218ff85fdb5262(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3c66c27ba53c72edcb3b6f85cf2f84f3bd4afd152aa8d8bbdce895bca382e5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824badd6fb7e5f770535729d1e915a227b98a14597f969bc12aaf2635f49b992(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8b65c0e93aeb7913ed2a822757e31ec88018bc0633b32238f9b6ad54df3bab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f8c103e5beb0d973e5d209018bdb2893707dc54045bf4164625d73468a4327(
    *,
    table: builtins.str,
    mysql_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2ae67802bc4d46269f15e251ca61b00cd7e6cc4c72696f5ef1e117bd0b9351(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba47fc823bc86f85b46f3c7d66c7ef36e848bf6a8f9d4e4e4ec74485144daaa4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c60478bf9cf99a40bd62622ba84b3b4844306f809ead2f0c86eb8fe301fc9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e164afb7b4632e6e21ba9fe40e4060ded214f779343520f8ae627e64f6c416(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4fba8425facced2e35d16bc08d9f9df4a3cfe6e09828f27fbfdcbf3a5ec6751(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811d23977ea46d8bb808a32e998c0cdeec1202920f1232c14e3d4e536d8f9934(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6b2437de5afb4d3d3062eedf288787c94f774d386adc5570fd611e7a929e190(
    *,
    collation: typing.Optional[builtins.str] = None,
    column: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ordinal_position: typing.Optional[jsii.Number] = None,
    primary_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37248826856ca9dfb4e91cb36937cd1b038e5edac9cce3f3be797f674e6933ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c227d69d63e5037e72560f8cfe9e7b04578befbe5130eed9150a61b587d3a0f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c1f9241ec90839a4e9c7459608fec5eb625c2fb68430051ad1689fdad8eb56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ca7dd00f97fbe18a2c49875f68a9eae6a6255a559ad69db9a3ee209ef6192b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473f5e905f2848a2ccb19b790fd4c15eea0c52576954c9e7e48a8935c5db34a2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b258a7501901c9867024fa4f2c4c003140669bebbfe47678087094d1c19ec1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c5f7ad9b605e87fa3c703004388f9d973ac9b1e61d381ca0e122e420260396(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18623f5e4a5f5e41edc82a5f6793879500c107969e69faabe743ec280dd16351(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aed8cbdee483c61be882e1558fc23ea2e3a910b66185dfcf543429f50ddb176(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812c5406870508b7dcac28e9456b090b4d1f89406cc88a2040c859c09e71567a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aec533a8ba2c7f9ab6215ed1c075b98a28fec4443e3ca719d34ffa4e7ecfdd4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8982e4523ee32bb9d8365de4142ceb42cf0144c0a45c49e41ef9accfc902e1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7726d162a19d90a4da0f120eca91dc0bb17ff7e32bd9045dda1f36ab000b80(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a64b1902d4fee186b4bb8f2adde3aa0c8258831ed76e5ef9445f475913abaa0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237381b8637307cc7ee36e5718bb088f29692ac30282fe330db0d08e2e0b4532(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e02dfc07a981322c5b8eced3743447d9a805a9b4f8533beddfc23764b5edfc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTablesMysqlColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194e3ac627639d568a0e45fb6174fdf679bf1a46f154a89120f30df44737d4bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc9c4f92d7944ed623c164ccc25807fc788a1a13862f4b03cdc329bc1e5a194e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edbedda5850481069316e19fe67cce30cc1c84aa2742bdd454adc48f1f439f86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b495122f684f8a6aff9d3cacd4b489d00bc74085863a55a9cc6ed61d8016dee(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabasesMysqlTables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b85c9f253102ec7dfb09677425de6dbdb1f44d41faf0afd71a5b30519d4668(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871843b0fb3d6e912f71a0f4656946654572899c708f26ad9164fc7e039f8b5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7739c0c903f5d4eed5b61e16a039adbae564ad438ed843c2408b9ca2174b4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0564a6ef5fbb63d7a0fd01455b2db2106097444d2ec9d14b5793b6facddd8242(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjectsMysqlDatabases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a075919af5790565e078286520be7fc44a00af876994a9d576c8d2e79ad9e0a(
    value: typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfigIncludeObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3dd658cd4fa3e196ac9065595cccd04322f9aa72e82d158c577d95074f21d5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb969979110dea8b7d29506aad43f91e8e6c30ccd2404a2533ee0c45022bb72(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b176c9e31729438ec79fb94e1db18e775b08f3ea14b518ee846998caad54c3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ff671da4949da1a3fd7811aa6a121febb36c82cdc6828d84d473f27be21b0b(
    value: typing.Optional[DatastreamStreamSourceConfigMysqlSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66eb082c94f9d5e488dafeacc11e84716441ed791053fec9533f0966c15722a(
    *,
    drop_large_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    include_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    max_concurrent_backfill_tasks: typing.Optional[jsii.Number] = None,
    max_concurrent_cdc_tasks: typing.Optional[jsii.Number] = None,
    stream_large_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dedf9a1c105f8b0ace85d2fb166699c788477fe040a97299edeac028ef1349c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f25e16b7e3f2894d0a674e0e5dec052654a654e507ec9ae6b830f7082630f8(
    value: typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigDropLargeObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7264724e2f8f734ecb03f7375a7bcf9ece7168bf24e6bbe1eb050fc7e8097c(
    *,
    oracle_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3af95956f04ffa930fb3051a9dca3477324127bf73654e817d052ddc9e327bd(
    *,
    schema: builtins.str,
    oracle_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14ee331d4c6c68d26d4b34ceff7f4f08de047e8f93c63129c8ceeedafd0c3b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c09aca6227bc2111a3634eb67415e8546c62c7c53f17e2f04b93a99e1891d60e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f176eeab4202cf5f29376d55270cd5ce31125d50da3b25ed6bb68f63cfb46eef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1c0a0048902bc746f0202b4d19cb62006b09d01d9138b7731cc546f19955d8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6d271dc6207737838fe8eecc538d747899bd2d4a738ccb8ce5e3b93ec5bbdb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99297a2f23ea2ec019a3f7f549c0553614eb1bc5300cfde78ea4d6bbb37d829(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e59985faaf7a9634858fdbc3f40bca97fb97cbd9700de5b7b7a2c0759aa781(
    *,
    table: builtins.str,
    oracle_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b244ba4e92a9932a7d6e9f7169946854b07ba91d02ba16bc98a319f3f963491(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dbdc3a296709fcbd886e019297d0c9636db309cef96eded6cc292949b90c9fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d770d503d2634261928c26d7b624b794be932f06df91f0901e332c8fa0900fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c189e328d4c1867d36419eaa2657258a07cc220930f8bb800780423bacaf2aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b711f126f0b5d5863f66f049e5b4f96928c55b522a99e7f251b8386f7c09714(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a31421ae6c3e643759494d0dcc284873dda3ff2ca5af619ec4380eb9f450f2a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a0e8627a13e5003c6e5a20d23a7b765720ee25fcb19c7410da5638d2ea2398(
    *,
    column: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d8f80c6538999ac1bf4df247ca0bc78a694afe2228ff269cfd7410963e4b035(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa82e47be138ef9474e4187168574246dcc46ef7129fbbb58ef8bee27ee1277e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c9d3ceede0b7d41b0544eabe42318c95d78ec1fade2d2f7e8a0b6d1f7533b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fb660aba7e959f1fb5f32969811a7bcaec9ecd52f0d7444180d54481c40e6f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f2f543dca966365859a85fca94141c4af8a78bb39d50f5aaa8662ae5c672b7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afce80fcace6b6b025f3db45f5ce847d510f47318018cf7a9198241b6f88ee41(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae47d6bd6a064650dcecbd13f75f6059a2a0cef2c0ab45b32b82b0dbd93b83ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3098ca741fd087c190c0f6b132af060dae3474b2fdfa4b7f7def5821db8111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd3b543a5dcb4a630aeca77cd2d1e56577d8caf8650da72883a4a520042f9ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbebe1a4dbf536dde4522bff5d3e87f70691bced1f6d19f71d9535b11a23bb31(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeef71eb6dce09cff23e6bc2d26303ba1167e5395b9d51ca5adb912091dbdbfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc6e22d4ca3795b2fccd936c86e8ca4ea7b1893bcc03d72572e645a0c7b8e94(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTablesOracleColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6366596e84f7eed71f90a445ffa1750cd50b1967b305adad975a053804f494c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fdf7398ae4800d7c4301b786e3000fe3e43fb1630695b1e7a40bd319312a66(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a270e6985d7e40c797bc7aaf9609515c276e0ed06de9f52d96a459350459c168(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a0a3faa79481bbca9859a5f73a140f6eeb41b654a549fd45acc53530524f50(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemasOracleTables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bdf846f564435844623ecdb3e6c79d34f8b014ff077d1798b18c960300074c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861952d5417512b22e34e580a17b21fdb61522ac08e463be2943dbbd3ef9d6f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d50d163006d62e035d0f11bef96425e752c48e3ee6d25328a6ee339c2fd2a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c928f19332207097a14d2823084320da635b7383fccdc4bfb1ff333f132941da(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjectsOracleSchemas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa3e84028a28591d87bcfdece022b7a677e16e6f8f70614250b25d13a148f62(
    value: typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigExcludeObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516e4326892830d76cb4dbc14b6f3bafd8ff65ebf477723848656fbb26a5c4dd(
    *,
    oracle_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8f93b8c7c92a2839641fa1072f9d7fa0cd1af048996626b73b213f483b81be(
    *,
    schema: builtins.str,
    oracle_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2cbfb000beee41a28642c72ce8bea5b69f8aa3d800412c4098e8437e2961d30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973887aebd270bc09eb6d8122bf444694e2ac716d08dcd0e3269c9933140dde6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df33ee5209e90dbebca60ff1c109cfc7775d013bfd7cee0fea44611b9d64afb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1906b92b01dd6d3c847a4446a3f668b8d9e2c4542a65346739091910e01373d3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd366e369101f09638e8119eca0d05003045b8d0529e56ef9b5c52f9886327e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d29f6b07fe7b16241b50c33021a5d04ee46277d8091aa4cbc409e73730e614(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64bc732b152e813094b6715fd5fe81a00cc14024f7dff680edf8c722501e463(
    *,
    table: builtins.str,
    oracle_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f7d891e0e13cf87e0e625c6a22de14d0e4773e60aa0dc8ef9f81473d40b5de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60eec69efc016d6b982eddbba5e0db06dd68c7a7cd9640481b100b2b67557b44(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8afb6ed8fcf1bd65f104a17499713f0cc053b264513cec7cf9fca70b90f7f79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b0d28454eb989d06344277c80aad90da0e2c4c3aafd93e86cbd8e8612b6003(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a7d3506343aa8c00182c05c90c64e7864d4d88cf255dfbda67b436d9925f204(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db9efcc98ae892802c17691fd17790fd590cc83c1fef5b394db215fb2b6b2e65(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5a1f56703876c5d6fe8c38e5248ab76ee659086d5747fc853c48a73a91aa18(
    *,
    column: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ae4be4e0a222ca005624232f86d41ab7ffd15df46ffa83f2df7578c7192b97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729dd7e7e92d47782c143f122f50918d134a6cc2f8f8ff91e930ba0723f49fb4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34da348ce04a11a4a07616ec75015c1190264bff7b4ad535b62ad5a2dacbc27a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7777ce645fa85fcb8aedb6189e5e57e5f458fc541b793ca777919224cdd2ef97(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d6708d30e0cc9a3bbc02dfe7946bd639464fb7771873908be585494a80f29c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9189d901c34736bce08f8684c9835e28a6438a4ccd18abe5f657e9f42971efc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7370acfeee29348d9d8cd8a8e6a5c8018482bbd74f98bc8d9af6af5cd923c05f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5304b773ac21ec5d7b8c8e77d51a52c6f10cf12359cf9c8ea8721798aa8537e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0181dab91a59b4cc5b3be734f13d6ee4efc3da12a54828f3881645d83a29580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ff2eb35052f68fc6e740abcb5a829053101d7d86f26895de7f894635adb542(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c203d77e429514a045ccf099965680b592489aa41a78e48df85a223771d4eea7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4f3a037ab7b0f31e544f404d7badcfe12bdeb2bd55f8530aaddd73d0d3a03d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTablesOracleColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3533dd123f0b76456846703be290b1eac81ac0e77254f94407bbc6723bbc6795(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26bdcbc9e853b51532c10748e9be1f7314a633d479cf8216e5c0fa9b5a6eee24(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eacda35ed82da1716c1b9a5a50bb995abf9ffa290917a809648325d00b82f0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adca6e098fd62b4480f4f8e24087176d171d3e939d2761d05611d3c62619fd1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemasOracleTables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525b72ad5984924fcf93653a1a8661ae0c3a6336d827899b1c3c6eb2f2e62652(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87237bc30640d91ff58ae47cf248d6bae6069e18d3c862eebfc56d33f9206fe6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7d7d1d474fc71ba5617b372c9400ffba0684102f59881528bed77e2990f357(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef837eb5998c3339d937d7a44e6b8bc1ec621141f89e9140f85e2822b14aaee(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjectsOracleSchemas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba03c6342c6ac234bbb970f7129f7333a221b28c301981bde1fc01836328df4(
    value: typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigIncludeObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0284a38daff9134ae34bee2da004caa28f5cba6f7a2c932a976c5bbfeef7c08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6af8c58123f8d8a0c8b63257339deb9a8b73e41d554341fe4515d5adc9d9c94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a78fa511929ed6bc2b3ab866c19123052beac1ba8345d50ffbbc6773a8d97648(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a7fcb2fa3a21a279fd21fee2d5514bdf48d7d75fb09a0786d9c72f0f1473c0b(
    value: typing.Optional[DatastreamStreamSourceConfigOracleSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910fb5e313c4d669813b4a593e6747ab6ad76d269b30cd28faa1cab562e52c06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec0380cd31a7b9eaedd6101eafd9db4c78c28b5f7f3da800d6d9969c3f7277e(
    value: typing.Optional[DatastreamStreamSourceConfigOracleSourceConfigStreamLargeObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a3549b6717770d6733410684731e269f34c59ed1d70ad04082a2cb1b372371(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0241e5b41a94a409e82cab6012190e0005a0636d4cf36be768a9f6a56556cb14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac91b8aafb6713d91456fefe65121644675bbb9cb229a0456370ca2b40569268(
    value: typing.Optional[DatastreamStreamSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ae79ad53b694f7781963f400d072baa1f5d22bc5e5483bd86ba2e70599b709(
    *,
    publication: builtins.str,
    replication_slot: builtins.str,
    exclude_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    include_objects: typing.Optional[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects, typing.Dict[builtins.str, typing.Any]]] = None,
    max_concurrent_backfill_tasks: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a4258bf2802905d8ee887426f63927491e3fcf19a9f8d9e9c4a1021c552e9b(
    *,
    postgresql_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331284e6bce06ba8e518bb9569a72e24af92de555d78faad1178b6cf66219eac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e3f909289a0301309f8873713bb75c4d2626f97f24ee91f33ce580c3c7eedf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45caed9b649398bcd100e72f0da6ba0b4dc3c337f63cbdf9e29b6e9a0f56df3(
    value: typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e80d838b5d30de65ecfb3ef29147d8ca2e0e4dde6d9510dbf49004edba6a88(
    *,
    schema: builtins.str,
    postgresql_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13ca4ea5fba74669a57949657611d0d307df8a831f1cc55a2d6e7cc45fd334f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86d6fa0a2868416d0a9d770e74366754e45073e50c7a4af599b6643d1509c63(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4044c76379b835b2718de9a05b4f5d3a32e54bde9d3906bab2394f7549b5a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98b03573850b37399b98e2f4ea195208045a268343c13c51ba2a1d9714eabb4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af910725b901913c8796df10376a0a8384dada4387c8d97043aad60352d2f60c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ad272d189d797c265d529906e72c1ad5b7e43852a2326edae948a0fcd0d885(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483f3446b724d77c2b15ee3231e21c22a230d30ec9fb94d34d861ab612670618(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d47d159419ecd7203b1c5ff65f70063fdac0e31c4116d1805f472f9c98167b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e18f95ba3c41ef9bf98231c24e4793b4378421b2758643cde5f8efc5a7ca55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0927fdfb9e60d0e1ba1057b926dad9bb5c241cce5cf9b6d22123223f8aa8297(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6af859433b95de5d81eb431dd08d705162bf8db2347d4ccc726ccf842b088d9(
    *,
    table: builtins.str,
    postgresql_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd218897461e16c0f23974a580eb76abe2845d484c171984359c1ed8622b8d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a2e74c7fdd529a4d1ee7f6a64b9e6e47ddd667358f0abc84fd0148253d584ea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aebc96f946971f54129c41e5eda9e3ad1a0ebff117f09028da60eb7ffd75008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d805893bb3235b4f9c1633d71059201d7d08ccdd7aa36a50db3d826b2b35ad8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144731a8b2e89bda180d8919cb694996e07dbac0c0fdfaa5532f9f2b32e6d462(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac46856a302b0b8bba89085e76bfe43b99f5f9c5227798064dbdda02637628f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37eae8e46f1b45ca1fe3320a798a2565dcb12e2b16076f603238d893d2b204b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ebe71475a122a527121571f53d72e53de7ae6e06b06a2240fcb6fd75b9f59c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae0ae20385eb902a594d35738560a9b1f74723a8d3d4c141442d8f77975018d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eee4cc65dba21c31a714e36d03dc9931d7d00d35842b60dcc3ee7c2d28523eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119968ae5084667a855873712f397551ee9b874d666d3cb87dba8ee65cb4ebb6(
    *,
    column: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ordinal_position: typing.Optional[jsii.Number] = None,
    primary_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef04a0c014385d2c209f3da6a623816a874c841481d14904d4f9187a4cfc609b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea826ec199642ee0a51c75cf6dd6ca47009abc3935decc770a26888c99c6ed72(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030b83425a2ba9486f22179c05043ad49516a4779e3b1b1e31d9ba9b9f7b599a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f09f860ea8a8a28ba3cfe8121a9e3e375a7fd8294a76c65a2c9cf2e0361f4b12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d036c99c4fae01076de4c3375a21b54f1b8cc856be8f7310ee83109229e49ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7439f5c081522846d917486d9fbd96d1d35e5775dfa441cc96542f64dc382d4a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243128e00b60466a942673510ba2a3300ad883704b2f428e7c90053a57157f5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362215eb43066e56c57a2e2144e738d3eac0f00dbbd2bb37ff2821de3eedd6c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d54812ebd7719ec878053f096d4d3e52b51a4a9f3d6a02572ccd13f5faf6970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abf4622f951c65e3b1e59860e1ef3a9fb407297a14a0e24bd34f7bad0eed553(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de6cf4e49fde26b2289371fd8f6952f400d9cffd1497f14d9b9cabc5868118d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324ccf449e55a55c67750e18ab58674f84d3a802e68586c2a3688a948ca95309(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9254610cee63395a9b11efc47dfe1833f44245614f743080f287e96a04270ca8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigExcludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7adaa67649e1976351c67bcedc084b0713a4c0b17fb83475b46c2487eebf04(
    *,
    postgresql_schemas: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afcb6b2939a8b8941d83641c5505d2c400869f467cc66c42650a262ed2e68f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206e6f25a281e69c94ecdf8b9f4b1caa0b9f4a8cd23bc34424f1e577c8b0c916(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7140c5c71e1c2077933fe8e2bcd0b8959e47df163fb2b6a6ac6e17ae8d83af59(
    value: typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b11c8d59487df288de0eab416f4420c68f3fc68777e379ca17e0a52ed052b6(
    *,
    schema: builtins.str,
    postgresql_tables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec365f7b486a7ce93037839da46cdd490779fb7b1aab14c26db7f59efbfb9838(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1151a202024a70a5339007fa7de1042605eb219bea2eb9b76aa0debcf34eb8a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d30b5ab2761e7aa153e35bd65a25770ed830942339f276fc4471012dd9d351(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f57fb51b68ec2f633c8dbb2e251fd2f8a6f273930865ec195a37930004be054(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b41036e47ba656f3839ae37757506742a9fce5ac82cf2f89f0836e3898db6c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b862ef08d82bc4a359b09d9017d11cb69c206dd3d26dc1eecd421f38e4514170(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af65c7a7b829a2210cd218579cba307f37f8d79f197d608714a368d24d558c9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299d16d60f45da06f827cadd55b9d56b76dd2c22d309ecbb6494d930bce9216d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6eff8bec242627d24ff3be25a70b30ea7fb7c5511aa4c35b50f092ba8ddb6b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5e34079ca356e37b56017b018c1ea06aea957227f84e64f837243649b4da8c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54458fd67a11ba7a7fb7bb7a52b36133b0d69d19eec2d3160e0915a5d4ec268c(
    *,
    table: builtins.str,
    postgresql_columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e704c0d57a82331547113c924f94d96a053e31f59611f6c56398248b2052648(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb85a5e31393e12b2a9cbe991a97e0fc1779d968af0a56008cdda44eb7f91a2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef98fff90b91ea8d6138580e82dd68bd83982f8c58050ab7ce72ec35159510e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb57664fdfc4857cd6006388101e8ef490829b0a806d076b51592c30ee086437(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997f2835f315c813b833431c010bad4397181b711866690bd353992d112dce7d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e5292682b68f99e8e9f29d6049a0ad814d3e831bc1159b02bf0ef096c14f17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4476c8ccdf495c930f0ed8c2095ae099d5e875f711666a2221e98cde60869e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e802654023a08543ccfcb5caf12e874cbab741f982ad53e987c7e1594e0c450(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ddc44e9638d2dc2498dd59a07ff49b34cbc06ab41c6406a89342dfe0cafb0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0037aac2ea63309fd227cb161340b2a225d02b4342b47639a8c9d96d4379500f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTables]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac103eb25ec158e91d1f472b0c3fcde897a9e317acae8ab7ff6ac6ff1fb86cc(
    *,
    column: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    nullable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ordinal_position: typing.Optional[jsii.Number] = None,
    primary_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdd4e14779328acd034f0e48467679984e96ad0e9ec8ab874f8fc26bb5ae023(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139f380c8a2a7f11497764b9f1e4a26e7af626c615f8ca8b64c33fdb2de2561f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d331926042e584190a4b1d1ab9c0c04460d61c236801b0f34adcff6bd40436(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9957321f2b5877f34b13f78bdda36926d8e6f4c1b8eb863c47b524bed92974b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f9672d5b80d7516ed166a52f5db3ed107c83442d4bd2194cfeb447f04acf2b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5788974ded18b6418a1b3ee51c1619a216737a95bb3f399e91a453ebe9d648(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab20bfccb60c33a63f92e2f108d0ee3942f67f5c929633794ac147bac199447a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3316fab863f6a2ae245c53cf2a26b767b6e5339e06f55ae7295a965fab5c6822(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3405fb0182b8d7d5188c2db9630f62d70a4dc228b755deed333d8be7d6a3536(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500b57364f878bd70b190ad543d01439f0b66e89b5bc368d66b4a27d17dd66d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc542fdc39eaff8adf8558a62b5bda66ac3e0546c71c4593f87457e3a1a3d95(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7bc5d875b9afba5e60a79a039217bfda6fc79f13749f2b73ec9e4bdc457309(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025c38c00b2fb22abee7213b4c6cc19a9ff39a0e84847af80f0b5cbae17832d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamSourceConfigPostgresqlSourceConfigIncludeObjectsPostgresqlSchemasPostgresqlTablesPostgresqlColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090a22021896a3c9f68df6b699b4023bf4798f24491f66907634a5cd6dac2be5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649a3b0114c010e781ec3cdc70b02b8b3b55fcbca0ddbffc7ba821c422ab3bd3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a9a23875cfb632cebade6e105926e406fe8044e0694f0c30fc491fdeb54b15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afd38698baeac2a5b25401337bbcb1f4c07530c88e4b96d80f11be57246e515(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7144d99c1126a43c10d1fd66f0e7d8a88209b24a4f3dd917c0dc6c69201d48(
    value: typing.Optional[DatastreamStreamSourceConfigPostgresqlSourceConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3c43d69f12289839f31d381d72fc17e555fa583862cecacfb6539c6d58e6e9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cac18995955222a43bb9b35c0136372f39bb89f568cf37a95aa304a07adf928(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8643526e3db645744eade7d744fa2156e3d4720ede8a3f92d13bb328ce9c950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfbc2b3312d9160fbb91182305e5ed12d586cd6f792084f07eadff56090eb376(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd7cdc806265f3b7a72b6ee739412e8ca9ccb9efa8c1e3155c46a10919fe0c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201682a522c85e6608f5a77eb390ed891ff39af25038c474f9af88101c6414a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatastreamStreamTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
