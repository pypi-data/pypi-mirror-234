'''
# `google_looker_instance`

Refer to the Terraform Registory for docs: [`google_looker_instance`](https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance).
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


class LookerInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance google_looker_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        admin_settings: typing.Optional[typing.Union["LookerInstanceAdminSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        consumer_network: typing.Optional[builtins.str] = None,
        deny_maintenance_period: typing.Optional[typing.Union["LookerInstanceDenyMaintenancePeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_config: typing.Optional[typing.Union["LookerInstanceEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["LookerInstanceMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_config: typing.Optional[typing.Union["LookerInstanceOauthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        platform_edition: typing.Optional[builtins.str] = None,
        private_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        reserved_range: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["LookerInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_metadata: typing.Optional[typing.Union["LookerInstanceUserMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance google_looker_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The ID of the instance or a fully qualified identifier for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#name LookerInstance#name}
        :param admin_settings: admin_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#admin_settings LookerInstance#admin_settings}
        :param consumer_network: Network name in the consumer project in the format of: projects/{project}/global/networks/{network} Note that the consumer network may be in a different GCP project than the consumer project that is hosting the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#consumer_network LookerInstance#consumer_network}
        :param deny_maintenance_period: deny_maintenance_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#deny_maintenance_period LookerInstance#deny_maintenance_period}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#encryption_config LookerInstance#encryption_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#id LookerInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#maintenance_window LookerInstance#maintenance_window}
        :param oauth_config: oauth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#oauth_config LookerInstance#oauth_config}
        :param platform_edition: Platform editions for a Looker instance. Each edition maps to a set of instance features, like its size. Must be one of these values: - LOOKER_CORE_TRIAL: trial instance - LOOKER_CORE_STANDARD: pay as you go standard instance - LOOKER_CORE_STANDARD_ANNUAL: subscription standard instance - LOOKER_CORE_ENTERPRISE_ANNUAL: subscription enterprise instance - LOOKER_CORE_EMBED_ANNUAL: subscription embed instance Default value: "LOOKER_CORE_TRIAL" Possible values: ["LOOKER_CORE_TRIAL", "LOOKER_CORE_STANDARD", "LOOKER_CORE_STANDARD_ANNUAL", "LOOKER_CORE_ENTERPRISE_ANNUAL", "LOOKER_CORE_EMBED_ANNUAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#platform_edition LookerInstance#platform_edition}
        :param private_ip_enabled: Whether private IP is enabled on the Looker instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#private_ip_enabled LookerInstance#private_ip_enabled}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#project LookerInstance#project}.
        :param public_ip_enabled: Whether public IP is enabled on the Looker instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#public_ip_enabled LookerInstance#public_ip_enabled}
        :param region: The name of the Looker region of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#region LookerInstance#region}
        :param reserved_range: Name of a reserved IP address range within the consumer network, to be used for private service access connection. User may or may not specify this in a request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#reserved_range LookerInstance#reserved_range}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#timeouts LookerInstance#timeouts}
        :param user_metadata: user_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#user_metadata LookerInstance#user_metadata}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d3e76060b6f2b181ef1d75423788a57a6238bad594d7db9201469b0e2bf413)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LookerInstanceConfig(
            name=name,
            admin_settings=admin_settings,
            consumer_network=consumer_network,
            deny_maintenance_period=deny_maintenance_period,
            encryption_config=encryption_config,
            id=id,
            maintenance_window=maintenance_window,
            oauth_config=oauth_config,
            platform_edition=platform_edition,
            private_ip_enabled=private_ip_enabled,
            project=project,
            public_ip_enabled=public_ip_enabled,
            region=region,
            reserved_range=reserved_range,
            timeouts=timeouts,
            user_metadata=user_metadata,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAdminSettings")
    def put_admin_settings(
        self,
        *,
        allowed_email_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_email_domains: Email domain allowlist for the instance. Define the email domains to which your users can deliver Looker (Google Cloud core) content. Updating this list will restart the instance. Updating the allowed email domains from terraform means the value provided will be considered as the entire list and not an amendment to the existing list of allowed email domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#allowed_email_domains LookerInstance#allowed_email_domains}
        '''
        value = LookerInstanceAdminSettings(
            allowed_email_domains=allowed_email_domains
        )

        return typing.cast(None, jsii.invoke(self, "putAdminSettings", [value]))

    @jsii.member(jsii_name="putDenyMaintenancePeriod")
    def put_deny_maintenance_period(
        self,
        *,
        end_date: typing.Union["LookerInstanceDenyMaintenancePeriodEndDate", typing.Dict[builtins.str, typing.Any]],
        start_date: typing.Union["LookerInstanceDenyMaintenancePeriodStartDate", typing.Dict[builtins.str, typing.Any]],
        time: typing.Union["LookerInstanceDenyMaintenancePeriodTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#end_date LookerInstance#end_date}
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#start_date LookerInstance#start_date}
        :param time: time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#time LookerInstance#time}
        '''
        value = LookerInstanceDenyMaintenancePeriod(
            end_date=end_date, start_date=start_date, time=time
        )

        return typing.cast(None, jsii.invoke(self, "putDenyMaintenancePeriod", [value]))

    @jsii.member(jsii_name="putEncryptionConfig")
    def put_encryption_config(
        self,
        *,
        kms_key_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_name: Name of the customer managed encryption key (CMEK) in KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#kms_key_name LookerInstance#kms_key_name}
        '''
        value = LookerInstanceEncryptionConfig(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfig", [value]))

    @jsii.member(jsii_name="putMaintenanceWindow")
    def put_maintenance_window(
        self,
        *,
        day_of_week: builtins.str,
        start_time: typing.Union["LookerInstanceMaintenanceWindowStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param day_of_week: Required. Day of the week for this MaintenanceWindow (in UTC). - MONDAY: Monday - TUESDAY: Tuesday - WEDNESDAY: Wednesday - THURSDAY: Thursday - FRIDAY: Friday - SATURDAY: Saturday - SUNDAY: Sunday Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#day_of_week LookerInstance#day_of_week}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#start_time LookerInstance#start_time}
        '''
        value = LookerInstanceMaintenanceWindow(
            day_of_week=day_of_week, start_time=start_time
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

    @jsii.member(jsii_name="putOauthConfig")
    def put_oauth_config(
        self,
        *,
        client_id: builtins.str,
        client_secret: builtins.str,
    ) -> None:
        '''
        :param client_id: The client ID for the Oauth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#client_id LookerInstance#client_id}
        :param client_secret: The client secret for the Oauth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#client_secret LookerInstance#client_secret}
        '''
        value = LookerInstanceOauthConfig(
            client_id=client_id, client_secret=client_secret
        )

        return typing.cast(None, jsii.invoke(self, "putOauthConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#create LookerInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#delete LookerInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#update LookerInstance#update}.
        '''
        value = LookerInstanceTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putUserMetadata")
    def put_user_metadata(
        self,
        *,
        additional_developer_user_count: typing.Optional[jsii.Number] = None,
        additional_standard_user_count: typing.Optional[jsii.Number] = None,
        additional_viewer_user_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param additional_developer_user_count: Number of additional Developer Users to allocate to the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#additional_developer_user_count LookerInstance#additional_developer_user_count}
        :param additional_standard_user_count: Number of additional Standard Users to allocate to the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#additional_standard_user_count LookerInstance#additional_standard_user_count}
        :param additional_viewer_user_count: Number of additional Viewer Users to allocate to the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#additional_viewer_user_count LookerInstance#additional_viewer_user_count}
        '''
        value = LookerInstanceUserMetadata(
            additional_developer_user_count=additional_developer_user_count,
            additional_standard_user_count=additional_standard_user_count,
            additional_viewer_user_count=additional_viewer_user_count,
        )

        return typing.cast(None, jsii.invoke(self, "putUserMetadata", [value]))

    @jsii.member(jsii_name="resetAdminSettings")
    def reset_admin_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminSettings", []))

    @jsii.member(jsii_name="resetConsumerNetwork")
    def reset_consumer_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerNetwork", []))

    @jsii.member(jsii_name="resetDenyMaintenancePeriod")
    def reset_deny_maintenance_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDenyMaintenancePeriod", []))

    @jsii.member(jsii_name="resetEncryptionConfig")
    def reset_encryption_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetOauthConfig")
    def reset_oauth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthConfig", []))

    @jsii.member(jsii_name="resetPlatformEdition")
    def reset_platform_edition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatformEdition", []))

    @jsii.member(jsii_name="resetPrivateIpEnabled")
    def reset_private_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIpEnabled", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPublicIpEnabled")
    def reset_public_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIpEnabled", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetReservedRange")
    def reset_reserved_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedRange", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserMetadata")
    def reset_user_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserMetadata", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="adminSettings")
    def admin_settings(self) -> "LookerInstanceAdminSettingsOutputReference":
        return typing.cast("LookerInstanceAdminSettingsOutputReference", jsii.get(self, "adminSettings"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="denyMaintenancePeriod")
    def deny_maintenance_period(
        self,
    ) -> "LookerInstanceDenyMaintenancePeriodOutputReference":
        return typing.cast("LookerInstanceDenyMaintenancePeriodOutputReference", jsii.get(self, "denyMaintenancePeriod"))

    @builtins.property
    @jsii.member(jsii_name="egressPublicIp")
    def egress_public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "egressPublicIp"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(self) -> "LookerInstanceEncryptionConfigOutputReference":
        return typing.cast("LookerInstanceEncryptionConfigOutputReference", jsii.get(self, "encryptionConfig"))

    @builtins.property
    @jsii.member(jsii_name="ingressPrivateIp")
    def ingress_private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressPrivateIp"))

    @builtins.property
    @jsii.member(jsii_name="ingressPublicIp")
    def ingress_public_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingressPublicIp"))

    @builtins.property
    @jsii.member(jsii_name="lookerUri")
    def looker_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lookerUri"))

    @builtins.property
    @jsii.member(jsii_name="lookerVersion")
    def looker_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lookerVersion"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(self) -> "LookerInstanceMaintenanceWindowOutputReference":
        return typing.cast("LookerInstanceMaintenanceWindowOutputReference", jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="oauthConfig")
    def oauth_config(self) -> "LookerInstanceOauthConfigOutputReference":
        return typing.cast("LookerInstanceOauthConfigOutputReference", jsii.get(self, "oauthConfig"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LookerInstanceTimeoutsOutputReference":
        return typing.cast("LookerInstanceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="userMetadata")
    def user_metadata(self) -> "LookerInstanceUserMetadataOutputReference":
        return typing.cast("LookerInstanceUserMetadataOutputReference", jsii.get(self, "userMetadata"))

    @builtins.property
    @jsii.member(jsii_name="adminSettingsInput")
    def admin_settings_input(self) -> typing.Optional["LookerInstanceAdminSettings"]:
        return typing.cast(typing.Optional["LookerInstanceAdminSettings"], jsii.get(self, "adminSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerNetworkInput")
    def consumer_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="denyMaintenancePeriodInput")
    def deny_maintenance_period_input(
        self,
    ) -> typing.Optional["LookerInstanceDenyMaintenancePeriod"]:
        return typing.cast(typing.Optional["LookerInstanceDenyMaintenancePeriod"], jsii.get(self, "denyMaintenancePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigInput")
    def encryption_config_input(
        self,
    ) -> typing.Optional["LookerInstanceEncryptionConfig"]:
        return typing.cast(typing.Optional["LookerInstanceEncryptionConfig"], jsii.get(self, "encryptionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional["LookerInstanceMaintenanceWindow"]:
        return typing.cast(typing.Optional["LookerInstanceMaintenanceWindow"], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthConfigInput")
    def oauth_config_input(self) -> typing.Optional["LookerInstanceOauthConfig"]:
        return typing.cast(typing.Optional["LookerInstanceOauthConfig"], jsii.get(self, "oauthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="platformEditionInput")
    def platform_edition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformEditionInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpEnabledInput")
    def private_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privateIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpEnabledInput")
    def public_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedRangeInput")
    def reserved_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "reservedRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LookerInstanceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LookerInstanceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userMetadataInput")
    def user_metadata_input(self) -> typing.Optional["LookerInstanceUserMetadata"]:
        return typing.cast(typing.Optional["LookerInstanceUserMetadata"], jsii.get(self, "userMetadataInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerNetwork")
    def consumer_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerNetwork"))

    @consumer_network.setter
    def consumer_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83bd1ebe216cc1fcfdbea6825f704566cd6e2d5b41d17111c84dcb96996bebf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerNetwork", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b0378da2a5d177ce788b6db56091ff5f746001b4e427ca649b7e07c55b3679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a943e2b8d714ac9823f73cabeba9ce1873004eff099e44c164361b5f3fa1b8d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="platformEdition")
    def platform_edition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformEdition"))

    @platform_edition.setter
    def platform_edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a849432fd10916d974edeb5b373696f759be67c14d1b81818fdc7e48386aa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformEdition", value)

    @builtins.property
    @jsii.member(jsii_name="privateIpEnabled")
    def private_ip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privateIpEnabled"))

    @private_ip_enabled.setter
    def private_ip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d9c2509f7887f721bebf658cbb67b95734f02b1a1ee1218ca5907d21dedb05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIpEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8344f896ab8d3df931e85853494b73a248e8ab508d888215da63881437303ed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="publicIpEnabled")
    def public_ip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicIpEnabled"))

    @public_ip_enabled.setter
    def public_ip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be494487ed9744e4dfe625311bbc333e94dabdda41090af22d33150648860027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicIpEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c896e0c21c417d64aefc9cb7b384decfacf806962b7c2438eb5105353ff86a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="reservedRange")
    def reserved_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reservedRange"))

    @reserved_range.setter
    def reserved_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e8aae5ec8bd44d67974da1c9d4d41e3daf09c9a62c6c9f9258f3d5e5901aa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedRange", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceAdminSettings",
    jsii_struct_bases=[],
    name_mapping={"allowed_email_domains": "allowedEmailDomains"},
)
class LookerInstanceAdminSettings:
    def __init__(
        self,
        *,
        allowed_email_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_email_domains: Email domain allowlist for the instance. Define the email domains to which your users can deliver Looker (Google Cloud core) content. Updating this list will restart the instance. Updating the allowed email domains from terraform means the value provided will be considered as the entire list and not an amendment to the existing list of allowed email domains. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#allowed_email_domains LookerInstance#allowed_email_domains}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12725d2c3c4ad8d7a175b50c5f38be43e08872786fc0560e8fa0bb4310b095c7)
            check_type(argname="argument allowed_email_domains", value=allowed_email_domains, expected_type=type_hints["allowed_email_domains"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_email_domains is not None:
            self._values["allowed_email_domains"] = allowed_email_domains

    @builtins.property
    def allowed_email_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Email domain allowlist for the instance.

        Define the email domains to which your users can deliver Looker (Google Cloud core) content.
        Updating this list will restart the instance. Updating the allowed email domains from terraform
        means the value provided will be considered as the entire list and not an amendment to the
        existing list of allowed email domains.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#allowed_email_domains LookerInstance#allowed_email_domains}
        '''
        result = self._values.get("allowed_email_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookerInstanceAdminSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LookerInstanceAdminSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceAdminSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad6f901463736aa95ffdbcfc9dfc342fd5c6ad0b5d9e7454167a4c86cb42e2c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedEmailDomains")
    def reset_allowed_email_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedEmailDomains", []))

    @builtins.property
    @jsii.member(jsii_name="allowedEmailDomainsInput")
    def allowed_email_domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedEmailDomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedEmailDomains")
    def allowed_email_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedEmailDomains"))

    @allowed_email_domains.setter
    def allowed_email_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07620bf2950f37c777ce1972e32b4b7cf34032a183a3318eb6ff59864f5fe2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedEmailDomains", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LookerInstanceAdminSettings]:
        return typing.cast(typing.Optional[LookerInstanceAdminSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LookerInstanceAdminSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d25fdc2877eff4263902e94795be7d9c90463870c2e08cde46072de3e8d4b3ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "admin_settings": "adminSettings",
        "consumer_network": "consumerNetwork",
        "deny_maintenance_period": "denyMaintenancePeriod",
        "encryption_config": "encryptionConfig",
        "id": "id",
        "maintenance_window": "maintenanceWindow",
        "oauth_config": "oauthConfig",
        "platform_edition": "platformEdition",
        "private_ip_enabled": "privateIpEnabled",
        "project": "project",
        "public_ip_enabled": "publicIpEnabled",
        "region": "region",
        "reserved_range": "reservedRange",
        "timeouts": "timeouts",
        "user_metadata": "userMetadata",
    },
)
class LookerInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        admin_settings: typing.Optional[typing.Union[LookerInstanceAdminSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        consumer_network: typing.Optional[builtins.str] = None,
        deny_maintenance_period: typing.Optional[typing.Union["LookerInstanceDenyMaintenancePeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_config: typing.Optional[typing.Union["LookerInstanceEncryptionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["LookerInstanceMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth_config: typing.Optional[typing.Union["LookerInstanceOauthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        platform_edition: typing.Optional[builtins.str] = None,
        private_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project: typing.Optional[builtins.str] = None,
        public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        region: typing.Optional[builtins.str] = None,
        reserved_range: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["LookerInstanceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_metadata: typing.Optional[typing.Union["LookerInstanceUserMetadata", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The ID of the instance or a fully qualified identifier for the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#name LookerInstance#name}
        :param admin_settings: admin_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#admin_settings LookerInstance#admin_settings}
        :param consumer_network: Network name in the consumer project in the format of: projects/{project}/global/networks/{network} Note that the consumer network may be in a different GCP project than the consumer project that is hosting the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#consumer_network LookerInstance#consumer_network}
        :param deny_maintenance_period: deny_maintenance_period block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#deny_maintenance_period LookerInstance#deny_maintenance_period}
        :param encryption_config: encryption_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#encryption_config LookerInstance#encryption_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#id LookerInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#maintenance_window LookerInstance#maintenance_window}
        :param oauth_config: oauth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#oauth_config LookerInstance#oauth_config}
        :param platform_edition: Platform editions for a Looker instance. Each edition maps to a set of instance features, like its size. Must be one of these values: - LOOKER_CORE_TRIAL: trial instance - LOOKER_CORE_STANDARD: pay as you go standard instance - LOOKER_CORE_STANDARD_ANNUAL: subscription standard instance - LOOKER_CORE_ENTERPRISE_ANNUAL: subscription enterprise instance - LOOKER_CORE_EMBED_ANNUAL: subscription embed instance Default value: "LOOKER_CORE_TRIAL" Possible values: ["LOOKER_CORE_TRIAL", "LOOKER_CORE_STANDARD", "LOOKER_CORE_STANDARD_ANNUAL", "LOOKER_CORE_ENTERPRISE_ANNUAL", "LOOKER_CORE_EMBED_ANNUAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#platform_edition LookerInstance#platform_edition}
        :param private_ip_enabled: Whether private IP is enabled on the Looker instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#private_ip_enabled LookerInstance#private_ip_enabled}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#project LookerInstance#project}.
        :param public_ip_enabled: Whether public IP is enabled on the Looker instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#public_ip_enabled LookerInstance#public_ip_enabled}
        :param region: The name of the Looker region of the instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#region LookerInstance#region}
        :param reserved_range: Name of a reserved IP address range within the consumer network, to be used for private service access connection. User may or may not specify this in a request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#reserved_range LookerInstance#reserved_range}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#timeouts LookerInstance#timeouts}
        :param user_metadata: user_metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#user_metadata LookerInstance#user_metadata}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(admin_settings, dict):
            admin_settings = LookerInstanceAdminSettings(**admin_settings)
        if isinstance(deny_maintenance_period, dict):
            deny_maintenance_period = LookerInstanceDenyMaintenancePeriod(**deny_maintenance_period)
        if isinstance(encryption_config, dict):
            encryption_config = LookerInstanceEncryptionConfig(**encryption_config)
        if isinstance(maintenance_window, dict):
            maintenance_window = LookerInstanceMaintenanceWindow(**maintenance_window)
        if isinstance(oauth_config, dict):
            oauth_config = LookerInstanceOauthConfig(**oauth_config)
        if isinstance(timeouts, dict):
            timeouts = LookerInstanceTimeouts(**timeouts)
        if isinstance(user_metadata, dict):
            user_metadata = LookerInstanceUserMetadata(**user_metadata)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e47e0e4957a1d2ae8cf0cc354c2e9bdb65db00bbe7c85ea4a60ada476c9cef78)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument admin_settings", value=admin_settings, expected_type=type_hints["admin_settings"])
            check_type(argname="argument consumer_network", value=consumer_network, expected_type=type_hints["consumer_network"])
            check_type(argname="argument deny_maintenance_period", value=deny_maintenance_period, expected_type=type_hints["deny_maintenance_period"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument oauth_config", value=oauth_config, expected_type=type_hints["oauth_config"])
            check_type(argname="argument platform_edition", value=platform_edition, expected_type=type_hints["platform_edition"])
            check_type(argname="argument private_ip_enabled", value=private_ip_enabled, expected_type=type_hints["private_ip_enabled"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument public_ip_enabled", value=public_ip_enabled, expected_type=type_hints["public_ip_enabled"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument reserved_range", value=reserved_range, expected_type=type_hints["reserved_range"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_metadata", value=user_metadata, expected_type=type_hints["user_metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if admin_settings is not None:
            self._values["admin_settings"] = admin_settings
        if consumer_network is not None:
            self._values["consumer_network"] = consumer_network
        if deny_maintenance_period is not None:
            self._values["deny_maintenance_period"] = deny_maintenance_period
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if id is not None:
            self._values["id"] = id
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if oauth_config is not None:
            self._values["oauth_config"] = oauth_config
        if platform_edition is not None:
            self._values["platform_edition"] = platform_edition
        if private_ip_enabled is not None:
            self._values["private_ip_enabled"] = private_ip_enabled
        if project is not None:
            self._values["project"] = project
        if public_ip_enabled is not None:
            self._values["public_ip_enabled"] = public_ip_enabled
        if region is not None:
            self._values["region"] = region
        if reserved_range is not None:
            self._values["reserved_range"] = reserved_range
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_metadata is not None:
            self._values["user_metadata"] = user_metadata

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
    def name(self) -> builtins.str:
        '''The ID of the instance or a fully qualified identifier for the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#name LookerInstance#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def admin_settings(self) -> typing.Optional[LookerInstanceAdminSettings]:
        '''admin_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#admin_settings LookerInstance#admin_settings}
        '''
        result = self._values.get("admin_settings")
        return typing.cast(typing.Optional[LookerInstanceAdminSettings], result)

    @builtins.property
    def consumer_network(self) -> typing.Optional[builtins.str]:
        '''Network name in the consumer project in the format of: projects/{project}/global/networks/{network} Note that the consumer network may be in a different GCP project than the consumer project that is hosting the Looker Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#consumer_network LookerInstance#consumer_network}
        '''
        result = self._values.get("consumer_network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deny_maintenance_period(
        self,
    ) -> typing.Optional["LookerInstanceDenyMaintenancePeriod"]:
        '''deny_maintenance_period block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#deny_maintenance_period LookerInstance#deny_maintenance_period}
        '''
        result = self._values.get("deny_maintenance_period")
        return typing.cast(typing.Optional["LookerInstanceDenyMaintenancePeriod"], result)

    @builtins.property
    def encryption_config(self) -> typing.Optional["LookerInstanceEncryptionConfig"]:
        '''encryption_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#encryption_config LookerInstance#encryption_config}
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional["LookerInstanceEncryptionConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#id LookerInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(self) -> typing.Optional["LookerInstanceMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#maintenance_window LookerInstance#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["LookerInstanceMaintenanceWindow"], result)

    @builtins.property
    def oauth_config(self) -> typing.Optional["LookerInstanceOauthConfig"]:
        '''oauth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#oauth_config LookerInstance#oauth_config}
        '''
        result = self._values.get("oauth_config")
        return typing.cast(typing.Optional["LookerInstanceOauthConfig"], result)

    @builtins.property
    def platform_edition(self) -> typing.Optional[builtins.str]:
        '''Platform editions for a Looker instance.

        Each edition maps to a set of instance features, like its size. Must be one of these values:

        - LOOKER_CORE_TRIAL: trial instance
        - LOOKER_CORE_STANDARD: pay as you go standard instance
        - LOOKER_CORE_STANDARD_ANNUAL: subscription standard instance
        - LOOKER_CORE_ENTERPRISE_ANNUAL: subscription enterprise instance
        - LOOKER_CORE_EMBED_ANNUAL: subscription embed instance Default value: "LOOKER_CORE_TRIAL" Possible values: ["LOOKER_CORE_TRIAL", "LOOKER_CORE_STANDARD", "LOOKER_CORE_STANDARD_ANNUAL", "LOOKER_CORE_ENTERPRISE_ANNUAL", "LOOKER_CORE_EMBED_ANNUAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#platform_edition LookerInstance#platform_edition}
        '''
        result = self._values.get("platform_edition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether private IP is enabled on the Looker instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#private_ip_enabled LookerInstance#private_ip_enabled}
        '''
        result = self._values.get("private_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#project LookerInstance#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether public IP is enabled on the Looker instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#public_ip_enabled LookerInstance#public_ip_enabled}
        '''
        result = self._values.get("public_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The name of the Looker region of the instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#region LookerInstance#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_range(self) -> typing.Optional[builtins.str]:
        '''Name of a reserved IP address range within the consumer network, to be used for private service access connection.

        User may or may not specify this in a request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#reserved_range LookerInstance#reserved_range}
        '''
        result = self._values.get("reserved_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LookerInstanceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#timeouts LookerInstance#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LookerInstanceTimeouts"], result)

    @builtins.property
    def user_metadata(self) -> typing.Optional["LookerInstanceUserMetadata"]:
        '''user_metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#user_metadata LookerInstance#user_metadata}
        '''
        result = self._values.get("user_metadata")
        return typing.cast(typing.Optional["LookerInstanceUserMetadata"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookerInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceDenyMaintenancePeriod",
    jsii_struct_bases=[],
    name_mapping={"end_date": "endDate", "start_date": "startDate", "time": "time"},
)
class LookerInstanceDenyMaintenancePeriod:
    def __init__(
        self,
        *,
        end_date: typing.Union["LookerInstanceDenyMaintenancePeriodEndDate", typing.Dict[builtins.str, typing.Any]],
        start_date: typing.Union["LookerInstanceDenyMaintenancePeriodStartDate", typing.Dict[builtins.str, typing.Any]],
        time: typing.Union["LookerInstanceDenyMaintenancePeriodTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param end_date: end_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#end_date LookerInstance#end_date}
        :param start_date: start_date block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#start_date LookerInstance#start_date}
        :param time: time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#time LookerInstance#time}
        '''
        if isinstance(end_date, dict):
            end_date = LookerInstanceDenyMaintenancePeriodEndDate(**end_date)
        if isinstance(start_date, dict):
            start_date = LookerInstanceDenyMaintenancePeriodStartDate(**start_date)
        if isinstance(time, dict):
            time = LookerInstanceDenyMaintenancePeriodTime(**time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a9e1dd972ba08bc0d572b45839e09768a177bd1d40632c3a7925ff5e63b111)
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_date": end_date,
            "start_date": start_date,
            "time": time,
        }

    @builtins.property
    def end_date(self) -> "LookerInstanceDenyMaintenancePeriodEndDate":
        '''end_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#end_date LookerInstance#end_date}
        '''
        result = self._values.get("end_date")
        assert result is not None, "Required property 'end_date' is missing"
        return typing.cast("LookerInstanceDenyMaintenancePeriodEndDate", result)

    @builtins.property
    def start_date(self) -> "LookerInstanceDenyMaintenancePeriodStartDate":
        '''start_date block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#start_date LookerInstance#start_date}
        '''
        result = self._values.get("start_date")
        assert result is not None, "Required property 'start_date' is missing"
        return typing.cast("LookerInstanceDenyMaintenancePeriodStartDate", result)

    @builtins.property
    def time(self) -> "LookerInstanceDenyMaintenancePeriodTime":
        '''time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#time LookerInstance#time}
        '''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast("LookerInstanceDenyMaintenancePeriodTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookerInstanceDenyMaintenancePeriod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceDenyMaintenancePeriodEndDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class LookerInstanceDenyMaintenancePeriodEndDate:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#day LookerInstance#day}
        :param month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#month LookerInstance#month}
        :param year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#year LookerInstance#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57562f14bed32f403136dc8a38863329665eb50db4c66b9f608037b8a8935a2)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if month is not None:
            self._values["month"] = month
        if year is not None:
            self._values["year"] = year

    @builtins.property
    def day(self) -> typing.Optional[jsii.Number]:
        '''Day of a month.

        Must be from 1 to 31 and valid for the year and month, or 0
        to specify a year by itself or a year and month where the day isn't significant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#day LookerInstance#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month(self) -> typing.Optional[jsii.Number]:
        '''Month of a year.

        Must be from 1 to 12, or 0 to specify a year without a
        month and day.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#month LookerInstance#month}
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year(self) -> typing.Optional[jsii.Number]:
        '''Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#year LookerInstance#year}
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookerInstanceDenyMaintenancePeriodEndDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LookerInstanceDenyMaintenancePeriodEndDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceDenyMaintenancePeriodEndDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeb340c2a2681a7cdb807cce4afcf8965ae8f714cdda2d6dfed681c475453a63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDay")
    def reset_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDay", []))

    @jsii.member(jsii_name="resetMonth")
    def reset_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonth", []))

    @jsii.member(jsii_name="resetYear")
    def reset_year(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYear", []))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c423c5292f5d1901f5843586c845392ae6068ecefeeac6e71967753ada439845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value)

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a33a034ee09bd8955bbe7e696e8daf6e73a8c6ebebf96e6010fbf059ee8ff598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value)

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e9b9d49f26eb12f1f69114d712aad917b589ec26fa6f040a86604722ba0a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LookerInstanceDenyMaintenancePeriodEndDate]:
        return typing.cast(typing.Optional[LookerInstanceDenyMaintenancePeriodEndDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LookerInstanceDenyMaintenancePeriodEndDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27b094d69ce2b4b5c931dff08dd516a11e36bd2b1ae4ccbdef8c2a2e0655696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LookerInstanceDenyMaintenancePeriodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceDenyMaintenancePeriodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6953a5d7131768b82497cc98e0bc38e52f1636bca88108d02d81259edeb6011c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEndDate")
    def put_end_date(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#day LookerInstance#day}
        :param month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#month LookerInstance#month}
        :param year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#year LookerInstance#year}
        '''
        value = LookerInstanceDenyMaintenancePeriodEndDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putEndDate", [value]))

    @jsii.member(jsii_name="putStartDate")
    def put_start_date(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#day LookerInstance#day}
        :param month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#month LookerInstance#month}
        :param year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#year LookerInstance#year}
        '''
        value = LookerInstanceDenyMaintenancePeriodStartDate(
            day=day, month=month, year=year
        )

        return typing.cast(None, jsii.invoke(self, "putStartDate", [value]))

    @jsii.member(jsii_name="putTime")
    def put_time(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#hours LookerInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#minutes LookerInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#nanos LookerInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#seconds LookerInstance#seconds}
        '''
        value = LookerInstanceDenyMaintenancePeriodTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(self) -> LookerInstanceDenyMaintenancePeriodEndDateOutputReference:
        return typing.cast(LookerInstanceDenyMaintenancePeriodEndDateOutputReference, jsii.get(self, "endDate"))

    @builtins.property
    @jsii.member(jsii_name="startDate")
    def start_date(
        self,
    ) -> "LookerInstanceDenyMaintenancePeriodStartDateOutputReference":
        return typing.cast("LookerInstanceDenyMaintenancePeriodStartDateOutputReference", jsii.get(self, "startDate"))

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> "LookerInstanceDenyMaintenancePeriodTimeOutputReference":
        return typing.cast("LookerInstanceDenyMaintenancePeriodTimeOutputReference", jsii.get(self, "time"))

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(
        self,
    ) -> typing.Optional[LookerInstanceDenyMaintenancePeriodEndDate]:
        return typing.cast(typing.Optional[LookerInstanceDenyMaintenancePeriodEndDate], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateInput")
    def start_date_input(
        self,
    ) -> typing.Optional["LookerInstanceDenyMaintenancePeriodStartDate"]:
        return typing.cast(typing.Optional["LookerInstanceDenyMaintenancePeriodStartDate"], jsii.get(self, "startDateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(self) -> typing.Optional["LookerInstanceDenyMaintenancePeriodTime"]:
        return typing.cast(typing.Optional["LookerInstanceDenyMaintenancePeriodTime"], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LookerInstanceDenyMaintenancePeriod]:
        return typing.cast(typing.Optional[LookerInstanceDenyMaintenancePeriod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LookerInstanceDenyMaintenancePeriod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92af4a80734fe43e872cc24ec2ac3be594cfa96bd6317632952c1a41c712fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceDenyMaintenancePeriodStartDate",
    jsii_struct_bases=[],
    name_mapping={"day": "day", "month": "month", "year": "year"},
)
class LookerInstanceDenyMaintenancePeriodStartDate:
    def __init__(
        self,
        *,
        day: typing.Optional[jsii.Number] = None,
        month: typing.Optional[jsii.Number] = None,
        year: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#day LookerInstance#day}
        :param month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#month LookerInstance#month}
        :param year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#year LookerInstance#year}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c61b7976aea10770f0a8e5b4eb6c25093abcb92f768ed53ff8880b555a2f9f5)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if month is not None:
            self._values["month"] = month
        if year is not None:
            self._values["year"] = year

    @builtins.property
    def day(self) -> typing.Optional[jsii.Number]:
        '''Day of a month.

        Must be from 1 to 31 and valid for the year and month, or 0
        to specify a year by itself or a year and month where the day isn't significant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#day LookerInstance#day}
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def month(self) -> typing.Optional[jsii.Number]:
        '''Month of a year.

        Must be from 1 to 12, or 0 to specify a year without a
        month and day.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#month LookerInstance#month}
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def year(self) -> typing.Optional[jsii.Number]:
        '''Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#year LookerInstance#year}
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookerInstanceDenyMaintenancePeriodStartDate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LookerInstanceDenyMaintenancePeriodStartDateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceDenyMaintenancePeriodStartDateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0acffaedcd36eb37b0544d7c02ec1cce1b0ebdaa6fc66d1f9f38de9929490bec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDay")
    def reset_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDay", []))

    @jsii.member(jsii_name="resetMonth")
    def reset_month(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonth", []))

    @jsii.member(jsii_name="resetYear")
    def reset_year(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYear", []))

    @builtins.property
    @jsii.member(jsii_name="dayInput")
    def day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayInput"))

    @builtins.property
    @jsii.member(jsii_name="monthInput")
    def month_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "monthInput"))

    @builtins.property
    @jsii.member(jsii_name="yearInput")
    def year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "yearInput"))

    @builtins.property
    @jsii.member(jsii_name="day")
    def day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "day"))

    @day.setter
    def day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd30992fb76331be0f5172be1a9a3ed12a7ae96968ad9173014305cbdc470490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "day", value)

    @builtins.property
    @jsii.member(jsii_name="month")
    def month(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "month"))

    @month.setter
    def month(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e189c40273a8e8982260ed68fac2e39f8122d64a71a38e25b4ddc634e7cf24e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "month", value)

    @builtins.property
    @jsii.member(jsii_name="year")
    def year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "year"))

    @year.setter
    def year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88bcaa437c12557746031823ee0ad5771ec278f5d41f93d2e51824eb858b52d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "year", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LookerInstanceDenyMaintenancePeriodStartDate]:
        return typing.cast(typing.Optional[LookerInstanceDenyMaintenancePeriodStartDate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LookerInstanceDenyMaintenancePeriodStartDate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77c5956a69d6584c807093f1dfa9bf81faa222e0127b71244537be62fee63ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceDenyMaintenancePeriodTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class LookerInstanceDenyMaintenancePeriodTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#hours LookerInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#minutes LookerInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#nanos LookerInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#seconds LookerInstance#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41c9320af50b2e26a1ccadaf5128742b4b946b9cff7c57be579a4fdb645ef847)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of day in 24 hour format. Should be from 0 to 23.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#hours LookerInstance#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#minutes LookerInstance#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#nanos LookerInstance#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time. Must normally be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#seconds LookerInstance#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookerInstanceDenyMaintenancePeriodTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LookerInstanceDenyMaintenancePeriodTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceDenyMaintenancePeriodTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74aaa90e9f1003609ed7004e7ae096354ed5bae0145046207b671096adf4274f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e42e62073a51761dac2d2deea569b71dabd064f2e727df2eea03ea2bad5680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value)

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3467f2c460fb4b1855d27f24bfab85d1548d59e45c924ac5a7df536a57f7957d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value)

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba18d17b3beb3a4d9dce3895cf66c42145e444fb7dad135492ffc5d868cf442e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value)

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__680a3185424ba826a78f1ef546555b591432e278d568a0c972ebb574a018b55c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LookerInstanceDenyMaintenancePeriodTime]:
        return typing.cast(typing.Optional[LookerInstanceDenyMaintenancePeriodTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LookerInstanceDenyMaintenancePeriodTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4461c88158818e7e55b1bf92f5484d67cc7311ef7f31d2d902c28d870161bdef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceEncryptionConfig",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class LookerInstanceEncryptionConfig:
    def __init__(self, *, kms_key_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_name: Name of the customer managed encryption key (CMEK) in KMS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#kms_key_name LookerInstance#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af08b54eba613425423390b3df6b26eb9500dff8c23ff21fec2837ff920829c1)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''Name of the customer managed encryption key (CMEK) in KMS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#kms_key_name LookerInstance#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookerInstanceEncryptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LookerInstanceEncryptionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceEncryptionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a6b77c0a4e1e81997b715f99aead9bef1cdb401df491523b4affb720be0544b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameVersion")
    def kms_key_name_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyNameVersion"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyState")
    def kms_key_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyState"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd64a2eb24816e9edbfe3f1bf482f5885dffca68c1fa2dd721c29911decaa3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LookerInstanceEncryptionConfig]:
        return typing.cast(typing.Optional[LookerInstanceEncryptionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LookerInstanceEncryptionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71b2644ad89203c0f31878356a5054b7b054927ddadd8b364a626c999aa5c7f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={"day_of_week": "dayOfWeek", "start_time": "startTime"},
)
class LookerInstanceMaintenanceWindow:
    def __init__(
        self,
        *,
        day_of_week: builtins.str,
        start_time: typing.Union["LookerInstanceMaintenanceWindowStartTime", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param day_of_week: Required. Day of the week for this MaintenanceWindow (in UTC). - MONDAY: Monday - TUESDAY: Tuesday - WEDNESDAY: Wednesday - THURSDAY: Thursday - FRIDAY: Friday - SATURDAY: Saturday - SUNDAY: Sunday Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#day_of_week LookerInstance#day_of_week}
        :param start_time: start_time block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#start_time LookerInstance#start_time}
        '''
        if isinstance(start_time, dict):
            start_time = LookerInstanceMaintenanceWindowStartTime(**start_time)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7b7e74507a9b3e6f5b461df119a2ff35a7e253b72ddd095f186809daf572c7)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "day_of_week": day_of_week,
            "start_time": start_time,
        }

    @builtins.property
    def day_of_week(self) -> builtins.str:
        '''Required. Day of the week for this MaintenanceWindow (in UTC).

        - MONDAY: Monday
        - TUESDAY: Tuesday
        - WEDNESDAY: Wednesday
        - THURSDAY: Thursday
        - FRIDAY: Friday
        - SATURDAY: Saturday
        - SUNDAY: Sunday Possible values: ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#day_of_week LookerInstance#day_of_week}
        '''
        result = self._values.get("day_of_week")
        assert result is not None, "Required property 'day_of_week' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> "LookerInstanceMaintenanceWindowStartTime":
        '''start_time block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#start_time LookerInstance#start_time}
        '''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast("LookerInstanceMaintenanceWindowStartTime", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookerInstanceMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LookerInstanceMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e60c60b6810ebd19efc6ef9489177920960dbe3d8d934b534d2f55fda7d6f032)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putStartTime")
    def put_start_time(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#hours LookerInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#minutes LookerInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#nanos LookerInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#seconds LookerInstance#seconds}
        '''
        value = LookerInstanceMaintenanceWindowStartTime(
            hours=hours, minutes=minutes, nanos=nanos, seconds=seconds
        )

        return typing.cast(None, jsii.invoke(self, "putStartTime", [value]))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> "LookerInstanceMaintenanceWindowStartTimeOutputReference":
        return typing.cast("LookerInstanceMaintenanceWindowStartTimeOutputReference", jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(
        self,
    ) -> typing.Optional["LookerInstanceMaintenanceWindowStartTime"]:
        return typing.cast(typing.Optional["LookerInstanceMaintenanceWindowStartTime"], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b622dc82ababcd2042a3687a4778550a373e9015fbc28278a698559657a3c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LookerInstanceMaintenanceWindow]:
        return typing.cast(typing.Optional[LookerInstanceMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LookerInstanceMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7660004a872f34a245b0517b8b0865a3cad065d158a6ff35adb405e2b4744a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceMaintenanceWindowStartTime",
    jsii_struct_bases=[],
    name_mapping={
        "hours": "hours",
        "minutes": "minutes",
        "nanos": "nanos",
        "seconds": "seconds",
    },
)
class LookerInstanceMaintenanceWindowStartTime:
    def __init__(
        self,
        *,
        hours: typing.Optional[jsii.Number] = None,
        minutes: typing.Optional[jsii.Number] = None,
        nanos: typing.Optional[jsii.Number] = None,
        seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param hours: Hours of day in 24 hour format. Should be from 0 to 23. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#hours LookerInstance#hours}
        :param minutes: Minutes of hour of day. Must be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#minutes LookerInstance#minutes}
        :param nanos: Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#nanos LookerInstance#nanos}
        :param seconds: Seconds of minutes of the time. Must normally be from 0 to 59. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#seconds LookerInstance#seconds}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccededa6381d68848ee6dcf0ba8611d88427ae08f3872c028e7aff6af1d90d8e)
            check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
            check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            check_type(argname="argument nanos", value=nanos, expected_type=type_hints["nanos"])
            check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hours is not None:
            self._values["hours"] = hours
        if minutes is not None:
            self._values["minutes"] = minutes
        if nanos is not None:
            self._values["nanos"] = nanos
        if seconds is not None:
            self._values["seconds"] = seconds

    @builtins.property
    def hours(self) -> typing.Optional[jsii.Number]:
        '''Hours of day in 24 hour format. Should be from 0 to 23.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#hours LookerInstance#hours}
        '''
        result = self._values.get("hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minutes(self) -> typing.Optional[jsii.Number]:
        '''Minutes of hour of day. Must be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#minutes LookerInstance#minutes}
        '''
        result = self._values.get("minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nanos(self) -> typing.Optional[jsii.Number]:
        '''Fractions of seconds in nanoseconds. Must be from 0 to 999,999,999.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#nanos LookerInstance#nanos}
        '''
        result = self._values.get("nanos")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds(self) -> typing.Optional[jsii.Number]:
        '''Seconds of minutes of the time. Must normally be from 0 to 59.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#seconds LookerInstance#seconds}
        '''
        result = self._values.get("seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookerInstanceMaintenanceWindowStartTime(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LookerInstanceMaintenanceWindowStartTimeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceMaintenanceWindowStartTimeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__676ac5e5556535f2f8bfa4f75e9182501fb6749fa82011f4d4390a829be0f54d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHours")
    def reset_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHours", []))

    @jsii.member(jsii_name="resetMinutes")
    def reset_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinutes", []))

    @jsii.member(jsii_name="resetNanos")
    def reset_nanos(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanos", []))

    @jsii.member(jsii_name="resetSeconds")
    def reset_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="hoursInput")
    def hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minutesInput")
    def minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minutesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanosInput")
    def nanos_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanosInput"))

    @builtins.property
    @jsii.member(jsii_name="secondsInput")
    def seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "secondsInput"))

    @builtins.property
    @jsii.member(jsii_name="hours")
    def hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hours"))

    @hours.setter
    def hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d222f3dd65d31f9c697fe210db69b5febcc436f2948a9d094d8789187ed71313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hours", value)

    @builtins.property
    @jsii.member(jsii_name="minutes")
    def minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minutes"))

    @minutes.setter
    def minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cab15d073c1bfae724ee460f71ddf1fb91afe400657c0784272fa52fb75f63fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minutes", value)

    @builtins.property
    @jsii.member(jsii_name="nanos")
    def nanos(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanos"))

    @nanos.setter
    def nanos(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7857d59ff131c42218738675da483308830c3de8495acba96ae678d3ae40357)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanos", value)

    @builtins.property
    @jsii.member(jsii_name="seconds")
    def seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "seconds"))

    @seconds.setter
    def seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2c899c2373efdc84115b87bde832c4a00bfefa45c253aacdb1b0523f5c76dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "seconds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LookerInstanceMaintenanceWindowStartTime]:
        return typing.cast(typing.Optional[LookerInstanceMaintenanceWindowStartTime], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LookerInstanceMaintenanceWindowStartTime],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1a920352183d0aad18c3d701920e44956e2785721dfbe63d4b8bb70cbb81af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceOauthConfig",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId", "client_secret": "clientSecret"},
)
class LookerInstanceOauthConfig:
    def __init__(self, *, client_id: builtins.str, client_secret: builtins.str) -> None:
        '''
        :param client_id: The client ID for the Oauth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#client_id LookerInstance#client_id}
        :param client_secret: The client secret for the Oauth config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#client_secret LookerInstance#client_secret}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a300ea5d6574ee4fd17597456d6fb271019964b8e1800d5495d6cf367b5df8)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret": client_secret,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The client ID for the Oauth config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#client_id LookerInstance#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> builtins.str:
        '''The client secret for the Oauth config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#client_secret LookerInstance#client_secret}
        '''
        result = self._values.get("client_secret")
        assert result is not None, "Required property 'client_secret' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookerInstanceOauthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LookerInstanceOauthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceOauthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e33699521e5fd8fd00e2d577e45a863cca9f425d93b954c47fc7f631671f9744)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb1846cc5a7622eab5be99093e0a61238e9dfaf6df84a3a1e879c6e0f0d1476e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19660fb64775f7c261722b9ce8e6a24a6d84645fc58fc60981eca11488cfe1b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LookerInstanceOauthConfig]:
        return typing.cast(typing.Optional[LookerInstanceOauthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LookerInstanceOauthConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f2328cba0415ac69affb7ab7308d91b9c0a9562dd34306b90bfa4bbaa2757c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class LookerInstanceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#create LookerInstance#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#delete LookerInstance#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#update LookerInstance#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e62c085539e1235b9a6740481fb925d697ee7fa30062780403a727ee335ebe)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#create LookerInstance#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#delete LookerInstance#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#update LookerInstance#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookerInstanceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LookerInstanceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bbfdaa7d2a8a11cb3c9643c6711a13e78000affa5e287586b96fdb629891b96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcec16e0e8af88f4019b734378822aa739ceb9321132fa29fa3c6ef65dff7bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c34a9320114bd6506603b6a3e1a9b29c700be5ce23a8efa86ef30bc2e84d2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975e8bb8ee7e838f817545fccb5a2bf31fd96b442f328636a1406f3436a2151b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LookerInstanceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LookerInstanceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LookerInstanceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b4d060074269863cacbcfe48c4d7c740314b8e66f27373eada27d9a48cbf354)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceUserMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "additional_developer_user_count": "additionalDeveloperUserCount",
        "additional_standard_user_count": "additionalStandardUserCount",
        "additional_viewer_user_count": "additionalViewerUserCount",
    },
)
class LookerInstanceUserMetadata:
    def __init__(
        self,
        *,
        additional_developer_user_count: typing.Optional[jsii.Number] = None,
        additional_standard_user_count: typing.Optional[jsii.Number] = None,
        additional_viewer_user_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param additional_developer_user_count: Number of additional Developer Users to allocate to the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#additional_developer_user_count LookerInstance#additional_developer_user_count}
        :param additional_standard_user_count: Number of additional Standard Users to allocate to the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#additional_standard_user_count LookerInstance#additional_standard_user_count}
        :param additional_viewer_user_count: Number of additional Viewer Users to allocate to the Looker Instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#additional_viewer_user_count LookerInstance#additional_viewer_user_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b33bc1ae78a59fda32d126d1d21463bdefbc31a8208f6ad22976c7b0d7834a)
            check_type(argname="argument additional_developer_user_count", value=additional_developer_user_count, expected_type=type_hints["additional_developer_user_count"])
            check_type(argname="argument additional_standard_user_count", value=additional_standard_user_count, expected_type=type_hints["additional_standard_user_count"])
            check_type(argname="argument additional_viewer_user_count", value=additional_viewer_user_count, expected_type=type_hints["additional_viewer_user_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_developer_user_count is not None:
            self._values["additional_developer_user_count"] = additional_developer_user_count
        if additional_standard_user_count is not None:
            self._values["additional_standard_user_count"] = additional_standard_user_count
        if additional_viewer_user_count is not None:
            self._values["additional_viewer_user_count"] = additional_viewer_user_count

    @builtins.property
    def additional_developer_user_count(self) -> typing.Optional[jsii.Number]:
        '''Number of additional Developer Users to allocate to the Looker Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#additional_developer_user_count LookerInstance#additional_developer_user_count}
        '''
        result = self._values.get("additional_developer_user_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def additional_standard_user_count(self) -> typing.Optional[jsii.Number]:
        '''Number of additional Standard Users to allocate to the Looker Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#additional_standard_user_count LookerInstance#additional_standard_user_count}
        '''
        result = self._values.get("additional_standard_user_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def additional_viewer_user_count(self) -> typing.Optional[jsii.Number]:
        '''Number of additional Viewer Users to allocate to the Looker Instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/looker_instance#additional_viewer_user_count LookerInstance#additional_viewer_user_count}
        '''
        result = self._values.get("additional_viewer_user_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LookerInstanceUserMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LookerInstanceUserMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.lookerInstance.LookerInstanceUserMetadataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b69eaae217483e15cee65a6208ef1949e8ba72b36834e7a46711c97638517c39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalDeveloperUserCount")
    def reset_additional_developer_user_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalDeveloperUserCount", []))

    @jsii.member(jsii_name="resetAdditionalStandardUserCount")
    def reset_additional_standard_user_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalStandardUserCount", []))

    @jsii.member(jsii_name="resetAdditionalViewerUserCount")
    def reset_additional_viewer_user_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalViewerUserCount", []))

    @builtins.property
    @jsii.member(jsii_name="additionalDeveloperUserCountInput")
    def additional_developer_user_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "additionalDeveloperUserCountInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalStandardUserCountInput")
    def additional_standard_user_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "additionalStandardUserCountInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalViewerUserCountInput")
    def additional_viewer_user_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "additionalViewerUserCountInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalDeveloperUserCount")
    def additional_developer_user_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "additionalDeveloperUserCount"))

    @additional_developer_user_count.setter
    def additional_developer_user_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579dd437b0affd87b5da367cbf4fed8cd747a015e1dd05ee6a9134fa61468a32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalDeveloperUserCount", value)

    @builtins.property
    @jsii.member(jsii_name="additionalStandardUserCount")
    def additional_standard_user_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "additionalStandardUserCount"))

    @additional_standard_user_count.setter
    def additional_standard_user_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf4e232d63cdfe2810267baac13dd3ce65f9673efc7cb852a8392ac42a2665c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalStandardUserCount", value)

    @builtins.property
    @jsii.member(jsii_name="additionalViewerUserCount")
    def additional_viewer_user_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "additionalViewerUserCount"))

    @additional_viewer_user_count.setter
    def additional_viewer_user_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6542cdff5258b3c44e650c5bbcd14846d7535b1a1d2ffd108dfa2536b70946fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalViewerUserCount", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LookerInstanceUserMetadata]:
        return typing.cast(typing.Optional[LookerInstanceUserMetadata], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LookerInstanceUserMetadata],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e644d9ec9d43e08abb1e17542554c7d1decf8e50199171e2da934cc5d3375c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "LookerInstance",
    "LookerInstanceAdminSettings",
    "LookerInstanceAdminSettingsOutputReference",
    "LookerInstanceConfig",
    "LookerInstanceDenyMaintenancePeriod",
    "LookerInstanceDenyMaintenancePeriodEndDate",
    "LookerInstanceDenyMaintenancePeriodEndDateOutputReference",
    "LookerInstanceDenyMaintenancePeriodOutputReference",
    "LookerInstanceDenyMaintenancePeriodStartDate",
    "LookerInstanceDenyMaintenancePeriodStartDateOutputReference",
    "LookerInstanceDenyMaintenancePeriodTime",
    "LookerInstanceDenyMaintenancePeriodTimeOutputReference",
    "LookerInstanceEncryptionConfig",
    "LookerInstanceEncryptionConfigOutputReference",
    "LookerInstanceMaintenanceWindow",
    "LookerInstanceMaintenanceWindowOutputReference",
    "LookerInstanceMaintenanceWindowStartTime",
    "LookerInstanceMaintenanceWindowStartTimeOutputReference",
    "LookerInstanceOauthConfig",
    "LookerInstanceOauthConfigOutputReference",
    "LookerInstanceTimeouts",
    "LookerInstanceTimeoutsOutputReference",
    "LookerInstanceUserMetadata",
    "LookerInstanceUserMetadataOutputReference",
]

publication.publish()

def _typecheckingstub__e7d3e76060b6f2b181ef1d75423788a57a6238bad594d7db9201469b0e2bf413(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    admin_settings: typing.Optional[typing.Union[LookerInstanceAdminSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    consumer_network: typing.Optional[builtins.str] = None,
    deny_maintenance_period: typing.Optional[typing.Union[LookerInstanceDenyMaintenancePeriod, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_config: typing.Optional[typing.Union[LookerInstanceEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[LookerInstanceMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth_config: typing.Optional[typing.Union[LookerInstanceOauthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    platform_edition: typing.Optional[builtins.str] = None,
    private_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    reserved_range: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[LookerInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_metadata: typing.Optional[typing.Union[LookerInstanceUserMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__83bd1ebe216cc1fcfdbea6825f704566cd6e2d5b41d17111c84dcb96996bebf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b0378da2a5d177ce788b6db56091ff5f746001b4e427ca649b7e07c55b3679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a943e2b8d714ac9823f73cabeba9ce1873004eff099e44c164361b5f3fa1b8d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a849432fd10916d974edeb5b373696f759be67c14d1b81818fdc7e48386aa3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d9c2509f7887f721bebf658cbb67b95734f02b1a1ee1218ca5907d21dedb05(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8344f896ab8d3df931e85853494b73a248e8ab508d888215da63881437303ed2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be494487ed9744e4dfe625311bbc333e94dabdda41090af22d33150648860027(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c896e0c21c417d64aefc9cb7b384decfacf806962b7c2438eb5105353ff86a50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e8aae5ec8bd44d67974da1c9d4d41e3daf09c9a62c6c9f9258f3d5e5901aa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12725d2c3c4ad8d7a175b50c5f38be43e08872786fc0560e8fa0bb4310b095c7(
    *,
    allowed_email_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6f901463736aa95ffdbcfc9dfc342fd5c6ad0b5d9e7454167a4c86cb42e2c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07620bf2950f37c777ce1972e32b4b7cf34032a183a3318eb6ff59864f5fe2a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25fdc2877eff4263902e94795be7d9c90463870c2e08cde46072de3e8d4b3ea(
    value: typing.Optional[LookerInstanceAdminSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e47e0e4957a1d2ae8cf0cc354c2e9bdb65db00bbe7c85ea4a60ada476c9cef78(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    admin_settings: typing.Optional[typing.Union[LookerInstanceAdminSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    consumer_network: typing.Optional[builtins.str] = None,
    deny_maintenance_period: typing.Optional[typing.Union[LookerInstanceDenyMaintenancePeriod, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_config: typing.Optional[typing.Union[LookerInstanceEncryptionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[LookerInstanceMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth_config: typing.Optional[typing.Union[LookerInstanceOauthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    platform_edition: typing.Optional[builtins.str] = None,
    private_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project: typing.Optional[builtins.str] = None,
    public_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    region: typing.Optional[builtins.str] = None,
    reserved_range: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[LookerInstanceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_metadata: typing.Optional[typing.Union[LookerInstanceUserMetadata, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a9e1dd972ba08bc0d572b45839e09768a177bd1d40632c3a7925ff5e63b111(
    *,
    end_date: typing.Union[LookerInstanceDenyMaintenancePeriodEndDate, typing.Dict[builtins.str, typing.Any]],
    start_date: typing.Union[LookerInstanceDenyMaintenancePeriodStartDate, typing.Dict[builtins.str, typing.Any]],
    time: typing.Union[LookerInstanceDenyMaintenancePeriodTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57562f14bed32f403136dc8a38863329665eb50db4c66b9f608037b8a8935a2(
    *,
    day: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    year: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb340c2a2681a7cdb807cce4afcf8965ae8f714cdda2d6dfed681c475453a63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c423c5292f5d1901f5843586c845392ae6068ecefeeac6e71967753ada439845(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a33a034ee09bd8955bbe7e696e8daf6e73a8c6ebebf96e6010fbf059ee8ff598(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e9b9d49f26eb12f1f69114d712aad917b589ec26fa6f040a86604722ba0a4c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27b094d69ce2b4b5c931dff08dd516a11e36bd2b1ae4ccbdef8c2a2e0655696(
    value: typing.Optional[LookerInstanceDenyMaintenancePeriodEndDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6953a5d7131768b82497cc98e0bc38e52f1636bca88108d02d81259edeb6011c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92af4a80734fe43e872cc24ec2ac3be594cfa96bd6317632952c1a41c712fd3(
    value: typing.Optional[LookerInstanceDenyMaintenancePeriod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c61b7976aea10770f0a8e5b4eb6c25093abcb92f768ed53ff8880b555a2f9f5(
    *,
    day: typing.Optional[jsii.Number] = None,
    month: typing.Optional[jsii.Number] = None,
    year: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0acffaedcd36eb37b0544d7c02ec1cce1b0ebdaa6fc66d1f9f38de9929490bec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd30992fb76331be0f5172be1a9a3ed12a7ae96968ad9173014305cbdc470490(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e189c40273a8e8982260ed68fac2e39f8122d64a71a38e25b4ddc634e7cf24e7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88bcaa437c12557746031823ee0ad5771ec278f5d41f93d2e51824eb858b52d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77c5956a69d6584c807093f1dfa9bf81faa222e0127b71244537be62fee63ff(
    value: typing.Optional[LookerInstanceDenyMaintenancePeriodStartDate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c9320af50b2e26a1ccadaf5128742b4b946b9cff7c57be579a4fdb645ef847(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74aaa90e9f1003609ed7004e7ae096354ed5bae0145046207b671096adf4274f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e42e62073a51761dac2d2deea569b71dabd064f2e727df2eea03ea2bad5680(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3467f2c460fb4b1855d27f24bfab85d1548d59e45c924ac5a7df536a57f7957d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba18d17b3beb3a4d9dce3895cf66c42145e444fb7dad135492ffc5d868cf442e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680a3185424ba826a78f1ef546555b591432e278d568a0c972ebb574a018b55c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4461c88158818e7e55b1bf92f5484d67cc7311ef7f31d2d902c28d870161bdef(
    value: typing.Optional[LookerInstanceDenyMaintenancePeriodTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af08b54eba613425423390b3df6b26eb9500dff8c23ff21fec2837ff920829c1(
    *,
    kms_key_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6b77c0a4e1e81997b715f99aead9bef1cdb401df491523b4affb720be0544b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd64a2eb24816e9edbfe3f1bf482f5885dffca68c1fa2dd721c29911decaa3f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b2644ad89203c0f31878356a5054b7b054927ddadd8b364a626c999aa5c7f6(
    value: typing.Optional[LookerInstanceEncryptionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7b7e74507a9b3e6f5b461df119a2ff35a7e253b72ddd095f186809daf572c7(
    *,
    day_of_week: builtins.str,
    start_time: typing.Union[LookerInstanceMaintenanceWindowStartTime, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60c60b6810ebd19efc6ef9489177920960dbe3d8d934b534d2f55fda7d6f032(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b622dc82ababcd2042a3687a4778550a373e9015fbc28278a698559657a3c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7660004a872f34a245b0517b8b0865a3cad065d158a6ff35adb405e2b4744a(
    value: typing.Optional[LookerInstanceMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccededa6381d68848ee6dcf0ba8611d88427ae08f3872c028e7aff6af1d90d8e(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
    nanos: typing.Optional[jsii.Number] = None,
    seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676ac5e5556535f2f8bfa4f75e9182501fb6749fa82011f4d4390a829be0f54d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d222f3dd65d31f9c697fe210db69b5febcc436f2948a9d094d8789187ed71313(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab15d073c1bfae724ee460f71ddf1fb91afe400657c0784272fa52fb75f63fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7857d59ff131c42218738675da483308830c3de8495acba96ae678d3ae40357(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2c899c2373efdc84115b87bde832c4a00bfefa45c253aacdb1b0523f5c76dd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1a920352183d0aad18c3d701920e44956e2785721dfbe63d4b8bb70cbb81af(
    value: typing.Optional[LookerInstanceMaintenanceWindowStartTime],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a300ea5d6574ee4fd17597456d6fb271019964b8e1800d5495d6cf367b5df8(
    *,
    client_id: builtins.str,
    client_secret: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33699521e5fd8fd00e2d577e45a863cca9f425d93b954c47fc7f631671f9744(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb1846cc5a7622eab5be99093e0a61238e9dfaf6df84a3a1e879c6e0f0d1476e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19660fb64775f7c261722b9ce8e6a24a6d84645fc58fc60981eca11488cfe1b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f2328cba0415ac69affb7ab7308d91b9c0a9562dd34306b90bfa4bbaa2757c(
    value: typing.Optional[LookerInstanceOauthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e62c085539e1235b9a6740481fb925d697ee7fa30062780403a727ee335ebe(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bbfdaa7d2a8a11cb3c9643c6711a13e78000affa5e287586b96fdb629891b96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcec16e0e8af88f4019b734378822aa739ceb9321132fa29fa3c6ef65dff7bd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c34a9320114bd6506603b6a3e1a9b29c700be5ce23a8efa86ef30bc2e84d2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975e8bb8ee7e838f817545fccb5a2bf31fd96b442f328636a1406f3436a2151b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b4d060074269863cacbcfe48c4d7c740314b8e66f27373eada27d9a48cbf354(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LookerInstanceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b33bc1ae78a59fda32d126d1d21463bdefbc31a8208f6ad22976c7b0d7834a(
    *,
    additional_developer_user_count: typing.Optional[jsii.Number] = None,
    additional_standard_user_count: typing.Optional[jsii.Number] = None,
    additional_viewer_user_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69eaae217483e15cee65a6208ef1949e8ba72b36834e7a46711c97638517c39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579dd437b0affd87b5da367cbf4fed8cd747a015e1dd05ee6a9134fa61468a32(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf4e232d63cdfe2810267baac13dd3ce65f9673efc7cb852a8392ac42a2665c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6542cdff5258b3c44e650c5bbcd14846d7535b1a1d2ffd108dfa2536b70946fa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e644d9ec9d43e08abb1e17542554c7d1decf8e50199171e2da934cc5d3375c(
    value: typing.Optional[LookerInstanceUserMetadata],
) -> None:
    """Type checking stubs"""
    pass
