'''
# `google_artifact_registry_repository`

Refer to the Terraform Registory for docs: [`google_artifact_registry_repository`](https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository).
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


class ArtifactRegistryRepository(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepository",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository google_artifact_registry_repository}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        format: builtins.str,
        repository_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        docker_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryDockerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        maven_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryMavenConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_repository_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ArtifactRegistryRepositoryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_repository_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryVirtualRepositoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository google_artifact_registry_repository} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param format: The format of packages that are stored in the repository. Supported formats can be found `here <https://cloud.google.com/artifact-registry/docs/supported-formats>`_. You can only create alpha formats if you are a member of the `alpha user group <https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#format ArtifactRegistryRepository#format}
        :param repository_id: The last part of the repository name, for example: "repo1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_id ArtifactRegistryRepository#repository_id}
        :param description: The user-provided description of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#description ArtifactRegistryRepository#description}
        :param docker_config: docker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#docker_config ArtifactRegistryRepository#docker_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#id ArtifactRegistryRepository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: The Cloud KMS resource name of the customer managed encryption key that’s used to encrypt the contents of the Repository. Has the form: 'projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key'. This value may not be changed after the Repository has been created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#kms_key_name ArtifactRegistryRepository#kms_key_name}
        :param labels: Labels with user-defined metadata. This field may contain up to 64 entries. Label keys and values may be no longer than 63 characters. Label keys must begin with a lowercase letter and may only contain lowercase letters, numeric characters, underscores, and dashes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#labels ArtifactRegistryRepository#labels}
        :param location: The name of the location this repository is located in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#location ArtifactRegistryRepository#location}
        :param maven_config: maven_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#maven_config ArtifactRegistryRepository#maven_config}
        :param mode: The mode configures the repository to serve artifacts from different sources. Default value: "STANDARD_REPOSITORY" Possible values: ["STANDARD_REPOSITORY", "VIRTUAL_REPOSITORY", "REMOTE_REPOSITORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#mode ArtifactRegistryRepository#mode}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#project ArtifactRegistryRepository#project}.
        :param remote_repository_config: remote_repository_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#remote_repository_config ArtifactRegistryRepository#remote_repository_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#timeouts ArtifactRegistryRepository#timeouts}
        :param virtual_repository_config: virtual_repository_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#virtual_repository_config ArtifactRegistryRepository#virtual_repository_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bcd8979225c9247b853165d6a61a0418712e3dd7ba1d971f4a680f60b10baaf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ArtifactRegistryRepositoryConfig(
            format=format,
            repository_id=repository_id,
            description=description,
            docker_config=docker_config,
            id=id,
            kms_key_name=kms_key_name,
            labels=labels,
            location=location,
            maven_config=maven_config,
            mode=mode,
            project=project,
            remote_repository_config=remote_repository_config,
            timeouts=timeouts,
            virtual_repository_config=virtual_repository_config,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putDockerConfig")
    def put_docker_config(
        self,
        *,
        immutable_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param immutable_tags: The repository which enabled this flag prevents all tags from being modified, moved or deleted. This does not prevent tags from being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#immutable_tags ArtifactRegistryRepository#immutable_tags}
        '''
        value = ArtifactRegistryRepositoryDockerConfig(immutable_tags=immutable_tags)

        return typing.cast(None, jsii.invoke(self, "putDockerConfig", [value]))

    @jsii.member(jsii_name="putMavenConfig")
    def put_maven_config(
        self,
        *,
        allow_snapshot_overwrites: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        version_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_snapshot_overwrites: The repository with this flag will allow publishing the same snapshot versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#allow_snapshot_overwrites ArtifactRegistryRepository#allow_snapshot_overwrites}
        :param version_policy: Version policy defines the versions that the registry will accept. Default value: "VERSION_POLICY_UNSPECIFIED" Possible values: ["VERSION_POLICY_UNSPECIFIED", "RELEASE", "SNAPSHOT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#version_policy ArtifactRegistryRepository#version_policy}
        '''
        value = ArtifactRegistryRepositoryMavenConfig(
            allow_snapshot_overwrites=allow_snapshot_overwrites,
            version_policy=version_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putMavenConfig", [value]))

    @jsii.member(jsii_name="putRemoteRepositoryConfig")
    def put_remote_repository_config(
        self,
        *,
        apt_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        docker_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        maven_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        npm_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        python_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        yum_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt_repository: apt_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#apt_repository ArtifactRegistryRepository#apt_repository}
        :param description: The description of the remote source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#description ArtifactRegistryRepository#description}
        :param docker_repository: docker_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#docker_repository ArtifactRegistryRepository#docker_repository}
        :param maven_repository: maven_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#maven_repository ArtifactRegistryRepository#maven_repository}
        :param npm_repository: npm_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#npm_repository ArtifactRegistryRepository#npm_repository}
        :param python_repository: python_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#python_repository ArtifactRegistryRepository#python_repository}
        :param yum_repository: yum_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#yum_repository ArtifactRegistryRepository#yum_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfig(
            apt_repository=apt_repository,
            description=description,
            docker_repository=docker_repository,
            maven_repository=maven_repository,
            npm_repository=npm_repository,
            python_repository=python_repository,
            yum_repository=yum_repository,
        )

        return typing.cast(None, jsii.invoke(self, "putRemoteRepositoryConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#create ArtifactRegistryRepository#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#delete ArtifactRegistryRepository#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#update ArtifactRegistryRepository#update}.
        '''
        value = ArtifactRegistryRepositoryTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVirtualRepositoryConfig")
    def put_virtual_repository_config(
        self,
        *,
        upstream_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param upstream_policies: upstream_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#upstream_policies ArtifactRegistryRepository#upstream_policies}
        '''
        value = ArtifactRegistryRepositoryVirtualRepositoryConfig(
            upstream_policies=upstream_policies
        )

        return typing.cast(None, jsii.invoke(self, "putVirtualRepositoryConfig", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDockerConfig")
    def reset_docker_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyName")
    def reset_kms_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyName", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetMavenConfig")
    def reset_maven_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMavenConfig", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRemoteRepositoryConfig")
    def reset_remote_repository_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteRepositoryConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualRepositoryConfig")
    def reset_virtual_repository_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualRepositoryConfig", []))

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
    @jsii.member(jsii_name="dockerConfig")
    def docker_config(self) -> "ArtifactRegistryRepositoryDockerConfigOutputReference":
        return typing.cast("ArtifactRegistryRepositoryDockerConfigOutputReference", jsii.get(self, "dockerConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="mavenConfig")
    def maven_config(self) -> "ArtifactRegistryRepositoryMavenConfigOutputReference":
        return typing.cast("ArtifactRegistryRepositoryMavenConfigOutputReference", jsii.get(self, "mavenConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="remoteRepositoryConfig")
    def remote_repository_config(
        self,
    ) -> "ArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference":
        return typing.cast("ArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference", jsii.get(self, "remoteRepositoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ArtifactRegistryRepositoryTimeoutsOutputReference":
        return typing.cast("ArtifactRegistryRepositoryTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="virtualRepositoryConfig")
    def virtual_repository_config(
        self,
    ) -> "ArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference":
        return typing.cast("ArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference", jsii.get(self, "virtualRepositoryConfig"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerConfigInput")
    def docker_config_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryDockerConfig"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryDockerConfig"], jsii.get(self, "dockerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

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
    @jsii.member(jsii_name="mavenConfigInput")
    def maven_config_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryMavenConfig"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryMavenConfig"], jsii.get(self, "mavenConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteRepositoryConfigInput")
    def remote_repository_config_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfig"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfig"], jsii.get(self, "remoteRepositoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryIdInput")
    def repository_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ArtifactRegistryRepositoryTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ArtifactRegistryRepositoryTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualRepositoryConfigInput")
    def virtual_repository_config_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryVirtualRepositoryConfig"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryVirtualRepositoryConfig"], jsii.get(self, "virtualRepositoryConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2165c18d7acb1a9627989cb5defe6b690405516e3f1d4547298a0905c9cba6ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb192c76d83ad27ed556a5fdb2c8834cef53c7d066348fc3138e98c0da765f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567479c5ca63288cb191b7917c2c8c7b1a7f65455a55aa2d836fc08bfe19347f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27069919d7606a89c8c364f9b9c838bb781ac21dae4c0b0fff13fe3cb27a446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1efd52613e06a5587e0511c8d71a516d56312b5f65a9444853959e0e66909b1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97953148b3c876edd5e36efdcd6a37041ea048618cfa6633e207c3a2f08b5a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6e187ab5b4160e21cd06788db103967f2abe29800b19b393fa21d07c4ef5c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5317b275f0dad4386cf514228fffbf224db11181ffc92b16a4e3fd8df2e98316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryId")
    def repository_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryId"))

    @repository_id.setter
    def repository_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b11e57d193991945e90c037b5c5b4e93d52dda2b58aa6c02b4eb1e82e6b7942b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "format": "format",
        "repository_id": "repositoryId",
        "description": "description",
        "docker_config": "dockerConfig",
        "id": "id",
        "kms_key_name": "kmsKeyName",
        "labels": "labels",
        "location": "location",
        "maven_config": "mavenConfig",
        "mode": "mode",
        "project": "project",
        "remote_repository_config": "remoteRepositoryConfig",
        "timeouts": "timeouts",
        "virtual_repository_config": "virtualRepositoryConfig",
    },
)
class ArtifactRegistryRepositoryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        format: builtins.str,
        repository_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        docker_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryDockerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        maven_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryMavenConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        mode: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_repository_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ArtifactRegistryRepositoryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_repository_config: typing.Optional[typing.Union["ArtifactRegistryRepositoryVirtualRepositoryConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param format: The format of packages that are stored in the repository. Supported formats can be found `here <https://cloud.google.com/artifact-registry/docs/supported-formats>`_. You can only create alpha formats if you are a member of the `alpha user group <https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#format ArtifactRegistryRepository#format}
        :param repository_id: The last part of the repository name, for example: "repo1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_id ArtifactRegistryRepository#repository_id}
        :param description: The user-provided description of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#description ArtifactRegistryRepository#description}
        :param docker_config: docker_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#docker_config ArtifactRegistryRepository#docker_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#id ArtifactRegistryRepository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_name: The Cloud KMS resource name of the customer managed encryption key that’s used to encrypt the contents of the Repository. Has the form: 'projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key'. This value may not be changed after the Repository has been created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#kms_key_name ArtifactRegistryRepository#kms_key_name}
        :param labels: Labels with user-defined metadata. This field may contain up to 64 entries. Label keys and values may be no longer than 63 characters. Label keys must begin with a lowercase letter and may only contain lowercase letters, numeric characters, underscores, and dashes. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#labels ArtifactRegistryRepository#labels}
        :param location: The name of the location this repository is located in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#location ArtifactRegistryRepository#location}
        :param maven_config: maven_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#maven_config ArtifactRegistryRepository#maven_config}
        :param mode: The mode configures the repository to serve artifacts from different sources. Default value: "STANDARD_REPOSITORY" Possible values: ["STANDARD_REPOSITORY", "VIRTUAL_REPOSITORY", "REMOTE_REPOSITORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#mode ArtifactRegistryRepository#mode}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#project ArtifactRegistryRepository#project}.
        :param remote_repository_config: remote_repository_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#remote_repository_config ArtifactRegistryRepository#remote_repository_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#timeouts ArtifactRegistryRepository#timeouts}
        :param virtual_repository_config: virtual_repository_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#virtual_repository_config ArtifactRegistryRepository#virtual_repository_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(docker_config, dict):
            docker_config = ArtifactRegistryRepositoryDockerConfig(**docker_config)
        if isinstance(maven_config, dict):
            maven_config = ArtifactRegistryRepositoryMavenConfig(**maven_config)
        if isinstance(remote_repository_config, dict):
            remote_repository_config = ArtifactRegistryRepositoryRemoteRepositoryConfig(**remote_repository_config)
        if isinstance(timeouts, dict):
            timeouts = ArtifactRegistryRepositoryTimeouts(**timeouts)
        if isinstance(virtual_repository_config, dict):
            virtual_repository_config = ArtifactRegistryRepositoryVirtualRepositoryConfig(**virtual_repository_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc52ffe5420733d20d2e99ce6681ef3eba8299273d736628839f8efdc4ab70f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument repository_id", value=repository_id, expected_type=type_hints["repository_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument docker_config", value=docker_config, expected_type=type_hints["docker_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument maven_config", value=maven_config, expected_type=type_hints["maven_config"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument remote_repository_config", value=remote_repository_config, expected_type=type_hints["remote_repository_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_repository_config", value=virtual_repository_config, expected_type=type_hints["virtual_repository_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "format": format,
            "repository_id": repository_id,
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
        if description is not None:
            self._values["description"] = description
        if docker_config is not None:
            self._values["docker_config"] = docker_config
        if id is not None:
            self._values["id"] = id
        if kms_key_name is not None:
            self._values["kms_key_name"] = kms_key_name
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if maven_config is not None:
            self._values["maven_config"] = maven_config
        if mode is not None:
            self._values["mode"] = mode
        if project is not None:
            self._values["project"] = project
        if remote_repository_config is not None:
            self._values["remote_repository_config"] = remote_repository_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_repository_config is not None:
            self._values["virtual_repository_config"] = virtual_repository_config

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
    def format(self) -> builtins.str:
        '''The format of packages that are stored in the repository.

        Supported formats
        can be found `here <https://cloud.google.com/artifact-registry/docs/supported-formats>`_.
        You can only create alpha formats if you are a member of the
        `alpha user group <https://cloud.google.com/artifact-registry/docs/supported-formats#alpha-access>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#format ArtifactRegistryRepository#format}
        '''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_id(self) -> builtins.str:
        '''The last part of the repository name, for example: "repo1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_id ArtifactRegistryRepository#repository_id}
        '''
        result = self._values.get("repository_id")
        assert result is not None, "Required property 'repository_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The user-provided description of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#description ArtifactRegistryRepository#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_config(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryDockerConfig"]:
        '''docker_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#docker_config ArtifactRegistryRepository#docker_config}
        '''
        result = self._values.get("docker_config")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryDockerConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#id ArtifactRegistryRepository#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_name(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS resource name of the customer managed encryption key that’s used to encrypt the contents of the Repository.

        Has the form:
        'projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key'.
        This value may not be changed after the Repository has been created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#kms_key_name ArtifactRegistryRepository#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels with user-defined metadata.

        This field may contain up to 64 entries. Label keys and values may be no
        longer than 63 characters. Label keys must begin with a lowercase letter
        and may only contain lowercase letters, numeric characters, underscores,
        and dashes.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#labels ArtifactRegistryRepository#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The name of the location this repository is located in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#location ArtifactRegistryRepository#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maven_config(self) -> typing.Optional["ArtifactRegistryRepositoryMavenConfig"]:
        '''maven_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#maven_config ArtifactRegistryRepository#maven_config}
        '''
        result = self._values.get("maven_config")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryMavenConfig"], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode configures the repository to serve artifacts from different sources. Default value: "STANDARD_REPOSITORY" Possible values: ["STANDARD_REPOSITORY", "VIRTUAL_REPOSITORY", "REMOTE_REPOSITORY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#mode ArtifactRegistryRepository#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#project ArtifactRegistryRepository#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_repository_config(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfig"]:
        '''remote_repository_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#remote_repository_config ArtifactRegistryRepository#remote_repository_config}
        '''
        result = self._values.get("remote_repository_config")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ArtifactRegistryRepositoryTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#timeouts ArtifactRegistryRepository#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryTimeouts"], result)

    @builtins.property
    def virtual_repository_config(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryVirtualRepositoryConfig"]:
        '''virtual_repository_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#virtual_repository_config ArtifactRegistryRepository#virtual_repository_config}
        '''
        result = self._values.get("virtual_repository_config")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryVirtualRepositoryConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryDockerConfig",
    jsii_struct_bases=[],
    name_mapping={"immutable_tags": "immutableTags"},
)
class ArtifactRegistryRepositoryDockerConfig:
    def __init__(
        self,
        *,
        immutable_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param immutable_tags: The repository which enabled this flag prevents all tags from being modified, moved or deleted. This does not prevent tags from being created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#immutable_tags ArtifactRegistryRepository#immutable_tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e99d1a86a033c5197277728390e013d86ed3332415bdae6fa6c72996e795ada)
            check_type(argname="argument immutable_tags", value=immutable_tags, expected_type=type_hints["immutable_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if immutable_tags is not None:
            self._values["immutable_tags"] = immutable_tags

    @builtins.property
    def immutable_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The repository which enabled this flag prevents all tags from being modified, moved or deleted.

        This does not prevent tags from being created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#immutable_tags ArtifactRegistryRepository#immutable_tags}
        '''
        result = self._values.get("immutable_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryDockerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryDockerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryDockerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61549e21e1cf17fd350c3e0a707660a04e2ac7d7955d5154566c8df96ae9d34d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImmutableTags")
    def reset_immutable_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmutableTags", []))

    @builtins.property
    @jsii.member(jsii_name="immutableTagsInput")
    def immutable_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "immutableTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="immutableTags")
    def immutable_tags(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "immutableTags"))

    @immutable_tags.setter
    def immutable_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b90f9e6c4469065dfbc2658469cd70cc9a8f3f9845ab3289682e2eb32ae21c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "immutableTags", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ArtifactRegistryRepositoryDockerConfig]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryDockerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryDockerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b8ac8051ca177e9ded9152217518443e9751acd881dfaad616c9466ffd1de19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryMavenConfig",
    jsii_struct_bases=[],
    name_mapping={
        "allow_snapshot_overwrites": "allowSnapshotOverwrites",
        "version_policy": "versionPolicy",
    },
)
class ArtifactRegistryRepositoryMavenConfig:
    def __init__(
        self,
        *,
        allow_snapshot_overwrites: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        version_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_snapshot_overwrites: The repository with this flag will allow publishing the same snapshot versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#allow_snapshot_overwrites ArtifactRegistryRepository#allow_snapshot_overwrites}
        :param version_policy: Version policy defines the versions that the registry will accept. Default value: "VERSION_POLICY_UNSPECIFIED" Possible values: ["VERSION_POLICY_UNSPECIFIED", "RELEASE", "SNAPSHOT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#version_policy ArtifactRegistryRepository#version_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab74b67816791960f5139ec576f8259b9d8cdc969e2749b89a93b9760db53f8d)
            check_type(argname="argument allow_snapshot_overwrites", value=allow_snapshot_overwrites, expected_type=type_hints["allow_snapshot_overwrites"])
            check_type(argname="argument version_policy", value=version_policy, expected_type=type_hints["version_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_snapshot_overwrites is not None:
            self._values["allow_snapshot_overwrites"] = allow_snapshot_overwrites
        if version_policy is not None:
            self._values["version_policy"] = version_policy

    @builtins.property
    def allow_snapshot_overwrites(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The repository with this flag will allow publishing the same snapshot versions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#allow_snapshot_overwrites ArtifactRegistryRepository#allow_snapshot_overwrites}
        '''
        result = self._values.get("allow_snapshot_overwrites")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def version_policy(self) -> typing.Optional[builtins.str]:
        '''Version policy defines the versions that the registry will accept. Default value: "VERSION_POLICY_UNSPECIFIED" Possible values: ["VERSION_POLICY_UNSPECIFIED", "RELEASE", "SNAPSHOT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#version_policy ArtifactRegistryRepository#version_policy}
        '''
        result = self._values.get("version_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryMavenConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryMavenConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryMavenConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7de1f438e290e9ca124de6b15183000f784044a570a2cc8274dbb09ac85bd612)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowSnapshotOverwrites")
    def reset_allow_snapshot_overwrites(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowSnapshotOverwrites", []))

    @jsii.member(jsii_name="resetVersionPolicy")
    def reset_version_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="allowSnapshotOverwritesInput")
    def allow_snapshot_overwrites_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowSnapshotOverwritesInput"))

    @builtins.property
    @jsii.member(jsii_name="versionPolicyInput")
    def version_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="allowSnapshotOverwrites")
    def allow_snapshot_overwrites(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowSnapshotOverwrites"))

    @allow_snapshot_overwrites.setter
    def allow_snapshot_overwrites(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59457c2988da463670a580250b3df5163145aab91c25ac2c0371ed402579b347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowSnapshotOverwrites", value)

    @builtins.property
    @jsii.member(jsii_name="versionPolicy")
    def version_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionPolicy"))

    @version_policy.setter
    def version_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22571ee4ba791f992e9ab633974cdf1f60df1bf9bbe80b4988d94b0c0d23b892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ArtifactRegistryRepositoryMavenConfig]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryMavenConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryMavenConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acea51acdad5f11b8d1e2b94559f58d2fd3610fe5ae9c52c182a472573db047)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfig",
    jsii_struct_bases=[],
    name_mapping={
        "apt_repository": "aptRepository",
        "description": "description",
        "docker_repository": "dockerRepository",
        "maven_repository": "mavenRepository",
        "npm_repository": "npmRepository",
        "python_repository": "pythonRepository",
        "yum_repository": "yumRepository",
    },
)
class ArtifactRegistryRepositoryRemoteRepositoryConfig:
    def __init__(
        self,
        *,
        apt_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        docker_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        maven_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        npm_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        python_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository", typing.Dict[builtins.str, typing.Any]]] = None,
        yum_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt_repository: apt_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#apt_repository ArtifactRegistryRepository#apt_repository}
        :param description: The description of the remote source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#description ArtifactRegistryRepository#description}
        :param docker_repository: docker_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#docker_repository ArtifactRegistryRepository#docker_repository}
        :param maven_repository: maven_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#maven_repository ArtifactRegistryRepository#maven_repository}
        :param npm_repository: npm_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#npm_repository ArtifactRegistryRepository#npm_repository}
        :param python_repository: python_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#python_repository ArtifactRegistryRepository#python_repository}
        :param yum_repository: yum_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#yum_repository ArtifactRegistryRepository#yum_repository}
        '''
        if isinstance(apt_repository, dict):
            apt_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository(**apt_repository)
        if isinstance(docker_repository, dict):
            docker_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository(**docker_repository)
        if isinstance(maven_repository, dict):
            maven_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository(**maven_repository)
        if isinstance(npm_repository, dict):
            npm_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository(**npm_repository)
        if isinstance(python_repository, dict):
            python_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository(**python_repository)
        if isinstance(yum_repository, dict):
            yum_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository(**yum_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fae93b99966d690cce1c6ffdab21d23b5c33e8202a1d2602b9db7e859d8a22)
            check_type(argname="argument apt_repository", value=apt_repository, expected_type=type_hints["apt_repository"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument docker_repository", value=docker_repository, expected_type=type_hints["docker_repository"])
            check_type(argname="argument maven_repository", value=maven_repository, expected_type=type_hints["maven_repository"])
            check_type(argname="argument npm_repository", value=npm_repository, expected_type=type_hints["npm_repository"])
            check_type(argname="argument python_repository", value=python_repository, expected_type=type_hints["python_repository"])
            check_type(argname="argument yum_repository", value=yum_repository, expected_type=type_hints["yum_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apt_repository is not None:
            self._values["apt_repository"] = apt_repository
        if description is not None:
            self._values["description"] = description
        if docker_repository is not None:
            self._values["docker_repository"] = docker_repository
        if maven_repository is not None:
            self._values["maven_repository"] = maven_repository
        if npm_repository is not None:
            self._values["npm_repository"] = npm_repository
        if python_repository is not None:
            self._values["python_repository"] = python_repository
        if yum_repository is not None:
            self._values["yum_repository"] = yum_repository

    @builtins.property
    def apt_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository"]:
        '''apt_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#apt_repository ArtifactRegistryRepository#apt_repository}
        '''
        result = self._values.get("apt_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the remote source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#description ArtifactRegistryRepository#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository"]:
        '''docker_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#docker_repository ArtifactRegistryRepository#docker_repository}
        '''
        result = self._values.get("docker_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository"], result)

    @builtins.property
    def maven_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository"]:
        '''maven_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#maven_repository ArtifactRegistryRepository#maven_repository}
        '''
        result = self._values.get("maven_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository"], result)

    @builtins.property
    def npm_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository"]:
        '''npm_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#npm_repository ArtifactRegistryRepository#npm_repository}
        '''
        result = self._values.get("npm_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository"], result)

    @builtins.property
    def python_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository"]:
        '''python_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#python_repository ArtifactRegistryRepository#python_repository}
        '''
        result = self._values.get("python_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository"], result)

    @builtins.property
    def yum_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository"]:
        '''yum_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#yum_repository ArtifactRegistryRepository#yum_repository}
        '''
        result = self._values.get("yum_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository",
    jsii_struct_bases=[],
    name_mapping={"public_repository": "publicRepository"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository:
    def __init__(
        self,
        *,
        public_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_repository: public_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        if isinstance(public_repository, dict):
            public_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository(**public_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300c846a2ae5a576245ccd6b3de911bd33229cf547c147df5aedbb44346ab4f9)
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def public_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository"]:
        '''public_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c997a4738e9b06fb888c017f90b2c96d6e06b703db6860d293315757b2ff1a24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPublicRepository")
    def put_public_repository(
        self,
        *,
        repository_base: builtins.str,
        repository_path: builtins.str,
    ) -> None:
        '''
        :param repository_base: A common public repository base for Apt, e.g. '"debian/dists/buster"' Possible values: ["DEBIAN", "UBUNTU"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_base ArtifactRegistryRepository#repository_base}
        :param repository_path: Specific repository from the base. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_path ArtifactRegistryRepository#repository_path}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository(
            repository_base=repository_base, repository_path=repository_path
        )

        return typing.cast(None, jsii.invoke(self, "putPublicRepository", [value]))

    @jsii.member(jsii_name="resetPublicRepository")
    def reset_public_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicRepository", []))

    @builtins.property
    @jsii.member(jsii_name="publicRepository")
    def public_repository(
        self,
    ) -> "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference":
        return typing.cast("ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference", jsii.get(self, "publicRepository"))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository"], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51161952a1b0fd8de1c6b2ed76685c9798c76167a11d2395e72f4df60f88bbe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository",
    jsii_struct_bases=[],
    name_mapping={
        "repository_base": "repositoryBase",
        "repository_path": "repositoryPath",
    },
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository:
    def __init__(
        self,
        *,
        repository_base: builtins.str,
        repository_path: builtins.str,
    ) -> None:
        '''
        :param repository_base: A common public repository base for Apt, e.g. '"debian/dists/buster"' Possible values: ["DEBIAN", "UBUNTU"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_base ArtifactRegistryRepository#repository_base}
        :param repository_path: Specific repository from the base. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_path ArtifactRegistryRepository#repository_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c963998b6fab43e1b3024a5bc8dd6485c1f60e3efa64427639825fa7d99e63)
            check_type(argname="argument repository_base", value=repository_base, expected_type=type_hints["repository_base"])
            check_type(argname="argument repository_path", value=repository_path, expected_type=type_hints["repository_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_base": repository_base,
            "repository_path": repository_path,
        }

    @builtins.property
    def repository_base(self) -> builtins.str:
        '''A common public repository base for Apt, e.g. '"debian/dists/buster"' Possible values: ["DEBIAN", "UBUNTU"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_base ArtifactRegistryRepository#repository_base}
        '''
        result = self._values.get("repository_base")
        assert result is not None, "Required property 'repository_base' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_path(self) -> builtins.str:
        '''Specific repository from the base.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_path ArtifactRegistryRepository#repository_path}
        '''
        result = self._values.get("repository_path")
        assert result is not None, "Required property 'repository_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10a07a61e91481a6b576b846227e88a00d91917819dcfd0b0d8327225ef30cd1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="repositoryBaseInput")
    def repository_base_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryBaseInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryPathInput")
    def repository_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryPathInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryBase")
    def repository_base(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryBase"))

    @repository_base.setter
    def repository_base(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71560d243ed7a8aed1a646a375172d987be4b26ab4d10777ff8e70e297cb153b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryBase", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryPath")
    def repository_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryPath"))

    @repository_path.setter
    def repository_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92be8249b7803056c69d6384bf30dd9f6050abf802728aa51c7bb722f28f18c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryPath", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df82d7514ab8a0c3f199338399c2299520bab434b2beff38020bfb410979c41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository",
    jsii_struct_bases=[],
    name_mapping={"public_repository": "publicRepository"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository:
    def __init__(
        self,
        *,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_repository: Address of the remote repository. Default value: "DOCKER_HUB" Possible values: ["DOCKER_HUB"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397f2d79a97ae68da0790d57673a03814fd0461db9af716c54dd50bfef356c58)
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def public_repository(self) -> typing.Optional[builtins.str]:
        '''Address of the remote repository. Default value: "DOCKER_HUB" Possible values: ["DOCKER_HUB"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bb18bc31ba8a67f06f888e52d0abcac0b7f2849eb3fb0820ca336eed3e5ff0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPublicRepository")
    def reset_public_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicRepository", []))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicRepository")
    def public_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicRepository"))

    @public_repository.setter
    def public_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd180a4f130999861b9c80b55a82803cd7b6cc9c649412cf7396f3c9b296232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicRepository", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c7ca8b2e52f3ee8dfe0871595bd317928ff86f260843925bc60f9706519aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository",
    jsii_struct_bases=[],
    name_mapping={"public_repository": "publicRepository"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository:
    def __init__(
        self,
        *,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_repository: Address of the remote repository. Default value: "MAVEN_CENTRAL" Possible values: ["MAVEN_CENTRAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba38fdee2f2ce5531e776ee3b15dda1479027e1355ba0e50d6c99da468d0adf2)
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def public_repository(self) -> typing.Optional[builtins.str]:
        '''Address of the remote repository. Default value: "MAVEN_CENTRAL" Possible values: ["MAVEN_CENTRAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af0beed1640c17c515e7d2b326ead966ae9b114b1b5020f9ce3a1701856ca967)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPublicRepository")
    def reset_public_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicRepository", []))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicRepository")
    def public_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicRepository"))

    @public_repository.setter
    def public_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15edb506c93bf8df67f6bd145fd0a3c4e8931fb25143e38292853e38cffb12d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicRepository", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0967229979d8b24a2c27058db22fb49edcf98238452786dc6c4b643d6e251199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository",
    jsii_struct_bases=[],
    name_mapping={"public_repository": "publicRepository"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository:
    def __init__(
        self,
        *,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_repository: Address of the remote repository. Default value: "NPMJS" Possible values: ["NPMJS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da84ff59d29f822b2ecd0f03ece2cce30e5572ee6a0e4f053a8b8fc4543eed8e)
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def public_repository(self) -> typing.Optional[builtins.str]:
        '''Address of the remote repository. Default value: "NPMJS" Possible values: ["NPMJS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba7d1d42db8b2cbc416852b144f3b51935b5a02d2a35b43c49ba723d8449cc97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPublicRepository")
    def reset_public_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicRepository", []))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicRepository")
    def public_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicRepository"))

    @public_repository.setter
    def public_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d88a5f4effea9d3ed0c4db80cfe8cbd1db8ec5148675ceec8b9d909abcfbfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicRepository", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f04d62d80a238b32126a9986d2e62e97475407018d15b73f88ddea3a313ca739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b263eb93494647a7ef5a05f1542d8dc0c2ef71516a22738794e56db676bc4ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAptRepository")
    def put_apt_repository(
        self,
        *,
        public_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_repository: public_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository(
            public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putAptRepository", [value]))

    @jsii.member(jsii_name="putDockerRepository")
    def put_docker_repository(
        self,
        *,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_repository: Address of the remote repository. Default value: "DOCKER_HUB" Possible values: ["DOCKER_HUB"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository(
            public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putDockerRepository", [value]))

    @jsii.member(jsii_name="putMavenRepository")
    def put_maven_repository(
        self,
        *,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_repository: Address of the remote repository. Default value: "MAVEN_CENTRAL" Possible values: ["MAVEN_CENTRAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository(
            public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putMavenRepository", [value]))

    @jsii.member(jsii_name="putNpmRepository")
    def put_npm_repository(
        self,
        *,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_repository: Address of the remote repository. Default value: "NPMJS" Possible values: ["NPMJS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository(
            public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putNpmRepository", [value]))

    @jsii.member(jsii_name="putPythonRepository")
    def put_python_repository(
        self,
        *,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_repository: Address of the remote repository. Default value: "PYPI" Possible values: ["PYPI"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository(
            public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putPythonRepository", [value]))

    @jsii.member(jsii_name="putYumRepository")
    def put_yum_repository(
        self,
        *,
        public_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_repository: public_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository(
            public_repository=public_repository
        )

        return typing.cast(None, jsii.invoke(self, "putYumRepository", [value]))

    @jsii.member(jsii_name="resetAptRepository")
    def reset_apt_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAptRepository", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDockerRepository")
    def reset_docker_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerRepository", []))

    @jsii.member(jsii_name="resetMavenRepository")
    def reset_maven_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMavenRepository", []))

    @jsii.member(jsii_name="resetNpmRepository")
    def reset_npm_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNpmRepository", []))

    @jsii.member(jsii_name="resetPythonRepository")
    def reset_python_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonRepository", []))

    @jsii.member(jsii_name="resetYumRepository")
    def reset_yum_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYumRepository", []))

    @builtins.property
    @jsii.member(jsii_name="aptRepository")
    def apt_repository(
        self,
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference, jsii.get(self, "aptRepository"))

    @builtins.property
    @jsii.member(jsii_name="dockerRepository")
    def docker_repository(
        self,
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference, jsii.get(self, "dockerRepository"))

    @builtins.property
    @jsii.member(jsii_name="mavenRepository")
    def maven_repository(
        self,
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference, jsii.get(self, "mavenRepository"))

    @builtins.property
    @jsii.member(jsii_name="npmRepository")
    def npm_repository(
        self,
    ) -> ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference:
        return typing.cast(ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference, jsii.get(self, "npmRepository"))

    @builtins.property
    @jsii.member(jsii_name="pythonRepository")
    def python_repository(
        self,
    ) -> "ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference":
        return typing.cast("ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference", jsii.get(self, "pythonRepository"))

    @builtins.property
    @jsii.member(jsii_name="yumRepository")
    def yum_repository(
        self,
    ) -> "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference":
        return typing.cast("ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference", jsii.get(self, "yumRepository"))

    @builtins.property
    @jsii.member(jsii_name="aptRepositoryInput")
    def apt_repository_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository], jsii.get(self, "aptRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerRepositoryInput")
    def docker_repository_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository], jsii.get(self, "dockerRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="mavenRepositoryInput")
    def maven_repository_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository], jsii.get(self, "mavenRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="npmRepositoryInput")
    def npm_repository_input(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository], jsii.get(self, "npmRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonRepositoryInput")
    def python_repository_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository"], jsii.get(self, "pythonRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="yumRepositoryInput")
    def yum_repository_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository"], jsii.get(self, "yumRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1afb8b15d0d3fcc2add65376ff228e8a4335ba93e34ce821e01bc8255b34b217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfig]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__335e955d30d46bab332ba5170d3d45dacf675c50c7fb336b5003e7f48d39d827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository",
    jsii_struct_bases=[],
    name_mapping={"public_repository": "publicRepository"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository:
    def __init__(
        self,
        *,
        public_repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param public_repository: Address of the remote repository. Default value: "PYPI" Possible values: ["PYPI"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def391e54a01e3f1db2cd742e8080c422019f6227a3674080966e314acde5fc2)
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def public_repository(self) -> typing.Optional[builtins.str]:
        '''Address of the remote repository. Default value: "PYPI" Possible values: ["PYPI"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e70ac559643c59ff67274cfd635c7635237d98d75b7d6501734ea78874ed7fc8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPublicRepository")
    def reset_public_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicRepository", []))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="publicRepository")
    def public_repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicRepository"))

    @public_repository.setter
    def public_repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714b00dcb034202919373219bac95b7e2c0d7bc93e65bb2f04899afa5af48512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicRepository", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee424b93b167760573681b792df9ebd73f4b0f9b62314ac6aabf32f251937da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository",
    jsii_struct_bases=[],
    name_mapping={"public_repository": "publicRepository"},
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository:
    def __init__(
        self,
        *,
        public_repository: typing.Optional[typing.Union["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param public_repository: public_repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        if isinstance(public_repository, dict):
            public_repository = ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository(**public_repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0325bb5263fbf3dd1c49906424438086b215785501498497e43318f82e268502)
            check_type(argname="argument public_repository", value=public_repository, expected_type=type_hints["public_repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if public_repository is not None:
            self._values["public_repository"] = public_repository

    @builtins.property
    def public_repository(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository"]:
        '''public_repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#public_repository ArtifactRegistryRepository#public_repository}
        '''
        result = self._values.get("public_repository")
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2a679b7385c63e61781d5ba83d69f83403e966957e55e74b4b95d6f7924417e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPublicRepository")
    def put_public_repository(
        self,
        *,
        repository_base: builtins.str,
        repository_path: builtins.str,
    ) -> None:
        '''
        :param repository_base: A common public repository base for Yum. Possible values: ["CENTOS", "CENTOS_DEBUG", "CENTOS_VAULT", "CENTOS_STREAM", "ROCKY", "EPEL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_base ArtifactRegistryRepository#repository_base}
        :param repository_path: Specific repository from the base, e.g. '"8-stream/BaseOs/x86_64/os"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_path ArtifactRegistryRepository#repository_path}
        '''
        value = ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository(
            repository_base=repository_base, repository_path=repository_path
        )

        return typing.cast(None, jsii.invoke(self, "putPublicRepository", [value]))

    @jsii.member(jsii_name="resetPublicRepository")
    def reset_public_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicRepository", []))

    @builtins.property
    @jsii.member(jsii_name="publicRepository")
    def public_repository(
        self,
    ) -> "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference":
        return typing.cast("ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference", jsii.get(self, "publicRepository"))

    @builtins.property
    @jsii.member(jsii_name="publicRepositoryInput")
    def public_repository_input(
        self,
    ) -> typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository"]:
        return typing.cast(typing.Optional["ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository"], jsii.get(self, "publicRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795c783ef1a61c13463d176923e925a389ed5535752ba0b92833d82eda9c2a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository",
    jsii_struct_bases=[],
    name_mapping={
        "repository_base": "repositoryBase",
        "repository_path": "repositoryPath",
    },
)
class ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository:
    def __init__(
        self,
        *,
        repository_base: builtins.str,
        repository_path: builtins.str,
    ) -> None:
        '''
        :param repository_base: A common public repository base for Yum. Possible values: ["CENTOS", "CENTOS_DEBUG", "CENTOS_VAULT", "CENTOS_STREAM", "ROCKY", "EPEL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_base ArtifactRegistryRepository#repository_base}
        :param repository_path: Specific repository from the base, e.g. '"8-stream/BaseOs/x86_64/os"'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_path ArtifactRegistryRepository#repository_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6917a87e677c8afb340d0ae49a5a195f0973b54c79d23dddcd6e886b50d376c3)
            check_type(argname="argument repository_base", value=repository_base, expected_type=type_hints["repository_base"])
            check_type(argname="argument repository_path", value=repository_path, expected_type=type_hints["repository_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_base": repository_base,
            "repository_path": repository_path,
        }

    @builtins.property
    def repository_base(self) -> builtins.str:
        '''A common public repository base for Yum. Possible values: ["CENTOS", "CENTOS_DEBUG", "CENTOS_VAULT", "CENTOS_STREAM", "ROCKY", "EPEL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_base ArtifactRegistryRepository#repository_base}
        '''
        result = self._values.get("repository_base")
        assert result is not None, "Required property 'repository_base' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_path(self) -> builtins.str:
        '''Specific repository from the base, e.g. '"8-stream/BaseOs/x86_64/os"'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository_path ArtifactRegistryRepository#repository_path}
        '''
        result = self._values.get("repository_path")
        assert result is not None, "Required property 'repository_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb17542fcbef07b7b65e243e58c5a1d610542508aa99afe4e8d5d813ceae497a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="repositoryBaseInput")
    def repository_base_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryBaseInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryPathInput")
    def repository_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryPathInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryBase")
    def repository_base(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryBase"))

    @repository_base.setter
    def repository_base(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bc36ee6ab3fdbfee0513aa8c24c128a8fb26ef0024e75b9b0e08c8a9564b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryBase", value)

    @builtins.property
    @jsii.member(jsii_name="repositoryPath")
    def repository_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryPath"))

    @repository_path.setter
    def repository_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c74e19a498de2e28d1ef89880839d03d47e506a34485b0015961b9221eddf64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryPath", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8b46f624277ac3b2ab3654bcf833d876c15ae525ba527605900e6cbcb1f16f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ArtifactRegistryRepositoryTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#create ArtifactRegistryRepository#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#delete ArtifactRegistryRepository#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#update ArtifactRegistryRepository#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1444b73787658b044250e4edc0ea20b21f736e87083196f04e2556bd8d5c677)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#create ArtifactRegistryRepository#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#delete ArtifactRegistryRepository#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#update ArtifactRegistryRepository#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26dca7d4ae65a212ede6de83a10f5b14116f2ef75ae17d92d4dc4ffcbf2041b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d69747494000d92dc610c0eb0b57f4f3780e477255afe36ff5a0cd11cce934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12da1b37cbf109ef1a6a64d699ba5db80deefea61cce62b902f5ae18b40daff4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0cc863215ef4932536d9da06d0ed0c5b214ee89661ea8cce078c9f5a2e0e4c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f058e316f09dc0fe291c88f34ed01a42fd5633e01df8fcea67d75b0dc864c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryVirtualRepositoryConfig",
    jsii_struct_bases=[],
    name_mapping={"upstream_policies": "upstreamPolicies"},
)
class ArtifactRegistryRepositoryVirtualRepositoryConfig:
    def __init__(
        self,
        *,
        upstream_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param upstream_policies: upstream_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#upstream_policies ArtifactRegistryRepository#upstream_policies}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9906605cc83e6b5985e1d336201586b3acd778608ed073fb5afa738b5022e4)
            check_type(argname="argument upstream_policies", value=upstream_policies, expected_type=type_hints["upstream_policies"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if upstream_policies is not None:
            self._values["upstream_policies"] = upstream_policies

    @builtins.property
    def upstream_policies(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies"]]]:
        '''upstream_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#upstream_policies ArtifactRegistryRepository#upstream_policies}
        '''
        result = self._values.get("upstream_policies")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryVirtualRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b803975416b5f5d0bbc8f707317eb0ff6359f28a275081d3886f1f37207faf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putUpstreamPolicies")
    def put_upstream_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7211658b6ca71f47ae5d894f55cf62b3ea4ea89908d146f41431f5704f78721c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUpstreamPolicies", [value]))

    @jsii.member(jsii_name="resetUpstreamPolicies")
    def reset_upstream_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpstreamPolicies", []))

    @builtins.property
    @jsii.member(jsii_name="upstreamPolicies")
    def upstream_policies(
        self,
    ) -> "ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList":
        return typing.cast("ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList", jsii.get(self, "upstreamPolicies"))

    @builtins.property
    @jsii.member(jsii_name="upstreamPoliciesInput")
    def upstream_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies"]]], jsii.get(self, "upstreamPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ArtifactRegistryRepositoryVirtualRepositoryConfig]:
        return typing.cast(typing.Optional[ArtifactRegistryRepositoryVirtualRepositoryConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ArtifactRegistryRepositoryVirtualRepositoryConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2978abcfb56761c7ca06f7d4bb7b8a69988573a61452d5be424a6ba4c7b6dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "priority": "priority", "repository": "repository"},
)
class ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        repository: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The user-provided ID of the upstream policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#id ArtifactRegistryRepository#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param priority: Entries with a greater priority value take precedence in the pull order. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#priority ArtifactRegistryRepository#priority}
        :param repository: A reference to the repository resource, for example: "projects/p1/locations/us-central1/repository/repo1". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository ArtifactRegistryRepository#repository}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24574f713916965d204fbfe34b4a654ef0a2934d7c3cb3289365c70299081c42)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if priority is not None:
            self._values["priority"] = priority
        if repository is not None:
            self._values["repository"] = repository

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''The user-provided ID of the upstream policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#id ArtifactRegistryRepository#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Entries with a greater priority value take precedence in the pull order.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#priority ArtifactRegistryRepository#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''A reference to the repository resource, for example: "projects/p1/locations/us-central1/repository/repo1".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/5.1.0/docs/resources/artifact_registry_repository#repository ArtifactRegistryRepository#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a874ecabc5dd02ac4c4eaaf4bce7f7e04b7ba5d0f78e84768ed764cc25f4c872)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1660bf1a29276e875a1184bd44330514a93aa5de00ea61eeee47476691977bc0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c128da1866b80bc63bc8ad24783e82f9af92fc054f65f655ef5c1cec8620e28e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f2300e1fe2ee0d0faf4882c8e5e4dfc1802b070ccfde75d4e486342d527a6ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc1aaf8cd690ebf63ed3b7f970c37841227c1a03318793e73bd3827602c1bf92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab2f3301b37bfe8f891fb8408c56769a27b373f5934dcc3f55706fe9da1eda7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.artifactRegistryRepository.ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d61231823d0d4f3f09e5cb548418febd034e0d518e95a60b8eeddf4c4e5fa109)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f396c652930778d5065441f65480c08523b5586baeb544a5065bcaa50714b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d715394ad5be31535b01945855216ddeed98cc338263cfcd56fba9154146479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d0df23a58c6aa0e390bde702de297c92176603d8599f4831b0a801d73ff0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1951af240571932f728b60aafb545caa1f7bf153c615f505418c2221cd6bc7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ArtifactRegistryRepository",
    "ArtifactRegistryRepositoryConfig",
    "ArtifactRegistryRepositoryDockerConfig",
    "ArtifactRegistryRepositoryDockerConfigOutputReference",
    "ArtifactRegistryRepositoryMavenConfig",
    "ArtifactRegistryRepositoryMavenConfigOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfig",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryOutputReference",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository",
    "ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepositoryOutputReference",
    "ArtifactRegistryRepositoryTimeouts",
    "ArtifactRegistryRepositoryTimeoutsOutputReference",
    "ArtifactRegistryRepositoryVirtualRepositoryConfig",
    "ArtifactRegistryRepositoryVirtualRepositoryConfigOutputReference",
    "ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies",
    "ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesList",
    "ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPoliciesOutputReference",
]

publication.publish()

def _typecheckingstub__9bcd8979225c9247b853165d6a61a0418712e3dd7ba1d971f4a680f60b10baaf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    format: builtins.str,
    repository_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    docker_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryDockerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    maven_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryMavenConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_repository_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ArtifactRegistryRepositoryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_repository_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryVirtualRepositoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2165c18d7acb1a9627989cb5defe6b690405516e3f1d4547298a0905c9cba6ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb192c76d83ad27ed556a5fdb2c8834cef53c7d066348fc3138e98c0da765f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567479c5ca63288cb191b7917c2c8c7b1a7f65455a55aa2d836fc08bfe19347f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27069919d7606a89c8c364f9b9c838bb781ac21dae4c0b0fff13fe3cb27a446(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1efd52613e06a5587e0511c8d71a516d56312b5f65a9444853959e0e66909b1c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97953148b3c876edd5e36efdcd6a37041ea048618cfa6633e207c3a2f08b5a90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6e187ab5b4160e21cd06788db103967f2abe29800b19b393fa21d07c4ef5c68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5317b275f0dad4386cf514228fffbf224db11181ffc92b16a4e3fd8df2e98316(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11e57d193991945e90c037b5c5b4e93d52dda2b58aa6c02b4eb1e82e6b7942b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc52ffe5420733d20d2e99ce6681ef3eba8299273d736628839f8efdc4ab70f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    format: builtins.str,
    repository_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    docker_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryDockerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_name: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    maven_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryMavenConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    mode: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_repository_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ArtifactRegistryRepositoryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_repository_config: typing.Optional[typing.Union[ArtifactRegistryRepositoryVirtualRepositoryConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e99d1a86a033c5197277728390e013d86ed3332415bdae6fa6c72996e795ada(
    *,
    immutable_tags: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61549e21e1cf17fd350c3e0a707660a04e2ac7d7955d5154566c8df96ae9d34d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b90f9e6c4469065dfbc2658469cd70cc9a8f3f9845ab3289682e2eb32ae21c9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b8ac8051ca177e9ded9152217518443e9751acd881dfaad616c9466ffd1de19(
    value: typing.Optional[ArtifactRegistryRepositoryDockerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab74b67816791960f5139ec576f8259b9d8cdc969e2749b89a93b9760db53f8d(
    *,
    allow_snapshot_overwrites: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    version_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de1f438e290e9ca124de6b15183000f784044a570a2cc8274dbb09ac85bd612(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59457c2988da463670a580250b3df5163145aab91c25ac2c0371ed402579b347(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22571ee4ba791f992e9ab633974cdf1f60df1bf9bbe80b4988d94b0c0d23b892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acea51acdad5f11b8d1e2b94559f58d2fd3610fe5ae9c52c182a472573db047(
    value: typing.Optional[ArtifactRegistryRepositoryMavenConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fae93b99966d690cce1c6ffdab21d23b5c33e8202a1d2602b9db7e859d8a22(
    *,
    apt_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    docker_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    maven_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    npm_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    python_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository, typing.Dict[builtins.str, typing.Any]]] = None,
    yum_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300c846a2ae5a576245ccd6b3de911bd33229cf547c147df5aedbb44346ab4f9(
    *,
    public_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c997a4738e9b06fb888c017f90b2c96d6e06b703db6860d293315757b2ff1a24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51161952a1b0fd8de1c6b2ed76685c9798c76167a11d2395e72f4df60f88bbe6(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c963998b6fab43e1b3024a5bc8dd6485c1f60e3efa64427639825fa7d99e63(
    *,
    repository_base: builtins.str,
    repository_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a07a61e91481a6b576b846227e88a00d91917819dcfd0b0d8327225ef30cd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71560d243ed7a8aed1a646a375172d987be4b26ab4d10777ff8e70e297cb153b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92be8249b7803056c69d6384bf30dd9f6050abf802728aa51c7bb722f28f18c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df82d7514ab8a0c3f199338399c2299520bab434b2beff38020bfb410979c41(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigAptRepositoryPublicRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397f2d79a97ae68da0790d57673a03814fd0461db9af716c54dd50bfef356c58(
    *,
    public_repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb18bc31ba8a67f06f888e52d0abcac0b7f2849eb3fb0820ca336eed3e5ff0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd180a4f130999861b9c80b55a82803cd7b6cc9c649412cf7396f3c9b296232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c7ca8b2e52f3ee8dfe0871595bd317928ff86f260843925bc60f9706519aee(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigDockerRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba38fdee2f2ce5531e776ee3b15dda1479027e1355ba0e50d6c99da468d0adf2(
    *,
    public_repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0beed1640c17c515e7d2b326ead966ae9b114b1b5020f9ce3a1701856ca967(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15edb506c93bf8df67f6bd145fd0a3c4e8931fb25143e38292853e38cffb12d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0967229979d8b24a2c27058db22fb49edcf98238452786dc6c4b643d6e251199(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigMavenRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da84ff59d29f822b2ecd0f03ece2cce30e5572ee6a0e4f053a8b8fc4543eed8e(
    *,
    public_repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7d1d42db8b2cbc416852b144f3b51935b5a02d2a35b43c49ba723d8449cc97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d88a5f4effea9d3ed0c4db80cfe8cbd1db8ec5148675ceec8b9d909abcfbfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04d62d80a238b32126a9986d2e62e97475407018d15b73f88ddea3a313ca739(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigNpmRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b263eb93494647a7ef5a05f1542d8dc0c2ef71516a22738794e56db676bc4ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afb8b15d0d3fcc2add65376ff228e8a4335ba93e34ce821e01bc8255b34b217(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335e955d30d46bab332ba5170d3d45dacf675c50c7fb336b5003e7f48d39d827(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def391e54a01e3f1db2cd742e8080c422019f6227a3674080966e314acde5fc2(
    *,
    public_repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70ac559643c59ff67274cfd635c7635237d98d75b7d6501734ea78874ed7fc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714b00dcb034202919373219bac95b7e2c0d7bc93e65bb2f04899afa5af48512(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee424b93b167760573681b792df9ebd73f4b0f9b62314ac6aabf32f251937da(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigPythonRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0325bb5263fbf3dd1c49906424438086b215785501498497e43318f82e268502(
    *,
    public_repository: typing.Optional[typing.Union[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2a679b7385c63e61781d5ba83d69f83403e966957e55e74b4b95d6f7924417e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795c783ef1a61c13463d176923e925a389ed5535752ba0b92833d82eda9c2a78(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6917a87e677c8afb340d0ae49a5a195f0973b54c79d23dddcd6e886b50d376c3(
    *,
    repository_base: builtins.str,
    repository_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb17542fcbef07b7b65e243e58c5a1d610542508aa99afe4e8d5d813ceae497a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bc36ee6ab3fdbfee0513aa8c24c128a8fb26ef0024e75b9b0e08c8a9564b9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c74e19a498de2e28d1ef89880839d03d47e506a34485b0015961b9221eddf64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8b46f624277ac3b2ab3654bcf833d876c15ae525ba527605900e6cbcb1f16f(
    value: typing.Optional[ArtifactRegistryRepositoryRemoteRepositoryConfigYumRepositoryPublicRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1444b73787658b044250e4edc0ea20b21f736e87083196f04e2556bd8d5c677(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26dca7d4ae65a212ede6de83a10f5b14116f2ef75ae17d92d4dc4ffcbf2041b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d69747494000d92dc610c0eb0b57f4f3780e477255afe36ff5a0cd11cce934(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12da1b37cbf109ef1a6a64d699ba5db80deefea61cce62b902f5ae18b40daff4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0cc863215ef4932536d9da06d0ed0c5b214ee89661ea8cce078c9f5a2e0e4c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f058e316f09dc0fe291c88f34ed01a42fd5633e01df8fcea67d75b0dc864c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9906605cc83e6b5985e1d336201586b3acd778608ed073fb5afa738b5022e4(
    *,
    upstream_policies: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b803975416b5f5d0bbc8f707317eb0ff6359f28a275081d3886f1f37207faf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7211658b6ca71f47ae5d894f55cf62b3ea4ea89908d146f41431f5704f78721c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2978abcfb56761c7ca06f7d4bb7b8a69988573a61452d5be424a6ba4c7b6dc(
    value: typing.Optional[ArtifactRegistryRepositoryVirtualRepositoryConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24574f713916965d204fbfe34b4a654ef0a2934d7c3cb3289365c70299081c42(
    *,
    id: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    repository: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a874ecabc5dd02ac4c4eaaf4bce7f7e04b7ba5d0f78e84768ed764cc25f4c872(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1660bf1a29276e875a1184bd44330514a93aa5de00ea61eeee47476691977bc0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c128da1866b80bc63bc8ad24783e82f9af92fc054f65f655ef5c1cec8620e28e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2300e1fe2ee0d0faf4882c8e5e4dfc1802b070ccfde75d4e486342d527a6ae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1aaf8cd690ebf63ed3b7f970c37841227c1a03318793e73bd3827602c1bf92(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab2f3301b37bfe8f891fb8408c56769a27b373f5934dcc3f55706fe9da1eda7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61231823d0d4f3f09e5cb548418febd034e0d518e95a60b8eeddf4c4e5fa109(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f396c652930778d5065441f65480c08523b5586baeb544a5065bcaa50714b34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d715394ad5be31535b01945855216ddeed98cc338263cfcd56fba9154146479(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d0df23a58c6aa0e390bde702de297c92176603d8599f4831b0a801d73ff0ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1951af240571932f728b60aafb545caa1f7bf153c615f505418c2221cd6bc7eb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ArtifactRegistryRepositoryVirtualRepositoryConfigUpstreamPolicies]],
) -> None:
    """Type checking stubs"""
    pass
