'''
# `google_dataform_repository`

Refer to the Terraform Registory for docs: [`google_dataform_repository`](https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository).
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


class GoogleDataformRepository(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepository",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository google_dataform_repository}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        git_remote_settings: typing.Optional[typing.Union["GoogleDataformRepositoryGitRemoteSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataformRepositoryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workspace_compilation_overrides: typing.Optional[typing.Union["GoogleDataformRepositoryWorkspaceCompilationOverrides", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository google_dataform_repository} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The repository's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#name GoogleDataformRepository#name}
        :param git_remote_settings: git_remote_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#git_remote_settings GoogleDataformRepository#git_remote_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#id GoogleDataformRepository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#project GoogleDataformRepository#project}.
        :param region: A reference to the region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#region GoogleDataformRepository#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#timeouts GoogleDataformRepository#timeouts}
        :param workspace_compilation_overrides: workspace_compilation_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#workspace_compilation_overrides GoogleDataformRepository#workspace_compilation_overrides}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2dbd824e559816fa9aa1a41d21f96fb5232e9bbae6a2495bc5c0d34376681af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataformRepositoryConfig(
            name=name,
            git_remote_settings=git_remote_settings,
            id=id,
            project=project,
            region=region,
            timeouts=timeouts,
            workspace_compilation_overrides=workspace_compilation_overrides,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putGitRemoteSettings")
    def put_git_remote_settings(
        self,
        *,
        authentication_token_secret_version: builtins.str,
        default_branch: builtins.str,
        url: builtins.str,
    ) -> None:
        '''
        :param authentication_token_secret_version: The name of the Secret Manager secret version to use as an authentication token for Git operations. Must be in the format projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#authentication_token_secret_version GoogleDataformRepository#authentication_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param default_branch: The Git remote's default branch name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#default_branch GoogleDataformRepository#default_branch}
        :param url: The Git remote's URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#url GoogleDataformRepository#url}
        '''
        value = GoogleDataformRepositoryGitRemoteSettings(
            authentication_token_secret_version=authentication_token_secret_version,
            default_branch=default_branch,
            url=url,
        )

        return typing.cast(None, jsii.invoke(self, "putGitRemoteSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#create GoogleDataformRepository#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#delete GoogleDataformRepository#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#update GoogleDataformRepository#update}.
        '''
        value = GoogleDataformRepositoryTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWorkspaceCompilationOverrides")
    def put_workspace_compilation_overrides(
        self,
        *,
        default_database: typing.Optional[builtins.str] = None,
        schema_suffix: typing.Optional[builtins.str] = None,
        table_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_database: Optional. The default database (Google Cloud project ID). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#default_database GoogleDataformRepository#default_database}
        :param schema_suffix: Optional. The suffix that should be appended to all schema (BigQuery dataset ID) names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#schema_suffix GoogleDataformRepository#schema_suffix}
        :param table_prefix: Optional. The prefix that should be prepended to all table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#table_prefix GoogleDataformRepository#table_prefix}
        '''
        value = GoogleDataformRepositoryWorkspaceCompilationOverrides(
            default_database=default_database,
            schema_suffix=schema_suffix,
            table_prefix=table_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putWorkspaceCompilationOverrides", [value]))

    @jsii.member(jsii_name="resetGitRemoteSettings")
    def reset_git_remote_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitRemoteSettings", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWorkspaceCompilationOverrides")
    def reset_workspace_compilation_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceCompilationOverrides", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="gitRemoteSettings")
    def git_remote_settings(
        self,
    ) -> "GoogleDataformRepositoryGitRemoteSettingsOutputReference":
        return typing.cast("GoogleDataformRepositoryGitRemoteSettingsOutputReference", jsii.get(self, "gitRemoteSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDataformRepositoryTimeoutsOutputReference":
        return typing.cast("GoogleDataformRepositoryTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workspaceCompilationOverrides")
    def workspace_compilation_overrides(
        self,
    ) -> "GoogleDataformRepositoryWorkspaceCompilationOverridesOutputReference":
        return typing.cast("GoogleDataformRepositoryWorkspaceCompilationOverridesOutputReference", jsii.get(self, "workspaceCompilationOverrides"))

    @builtins.property
    @jsii.member(jsii_name="gitRemoteSettingsInput")
    def git_remote_settings_input(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryGitRemoteSettings"]:
        return typing.cast(typing.Optional["GoogleDataformRepositoryGitRemoteSettings"], jsii.get(self, "gitRemoteSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataformRepositoryTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataformRepositoryTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceCompilationOverridesInput")
    def workspace_compilation_overrides_input(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryWorkspaceCompilationOverrides"]:
        return typing.cast(typing.Optional["GoogleDataformRepositoryWorkspaceCompilationOverrides"], jsii.get(self, "workspaceCompilationOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdab58a8336d3c636189858c8588a677dfbd052ab3c14cd40d8a49268abe669a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f4a057106a343e989703f7b4f95ba2b705fc513ca7ab7e2b71229b381e155b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71eede5c5296a69640fb97de4b79bb9c672e8cf27c8ab290f2b532f6c87b7800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744cc633499380c09cf18b996dc875cbfe006cccf23bcf66b03b1b203bb195b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryConfig",
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
        "git_remote_settings": "gitRemoteSettings",
        "id": "id",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
        "workspace_compilation_overrides": "workspaceCompilationOverrides",
    },
)
class GoogleDataformRepositoryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        git_remote_settings: typing.Optional[typing.Union["GoogleDataformRepositoryGitRemoteSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataformRepositoryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workspace_compilation_overrides: typing.Optional[typing.Union["GoogleDataformRepositoryWorkspaceCompilationOverrides", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The repository's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#name GoogleDataformRepository#name}
        :param git_remote_settings: git_remote_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#git_remote_settings GoogleDataformRepository#git_remote_settings}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#id GoogleDataformRepository#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#project GoogleDataformRepository#project}.
        :param region: A reference to the region. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#region GoogleDataformRepository#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#timeouts GoogleDataformRepository#timeouts}
        :param workspace_compilation_overrides: workspace_compilation_overrides block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#workspace_compilation_overrides GoogleDataformRepository#workspace_compilation_overrides}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(git_remote_settings, dict):
            git_remote_settings = GoogleDataformRepositoryGitRemoteSettings(**git_remote_settings)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataformRepositoryTimeouts(**timeouts)
        if isinstance(workspace_compilation_overrides, dict):
            workspace_compilation_overrides = GoogleDataformRepositoryWorkspaceCompilationOverrides(**workspace_compilation_overrides)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46292713426893130af4f48ca81b8e9914d1899beb7a04a7c673d8ef7571474b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument git_remote_settings", value=git_remote_settings, expected_type=type_hints["git_remote_settings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument workspace_compilation_overrides", value=workspace_compilation_overrides, expected_type=type_hints["workspace_compilation_overrides"])
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
        if git_remote_settings is not None:
            self._values["git_remote_settings"] = git_remote_settings
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if workspace_compilation_overrides is not None:
            self._values["workspace_compilation_overrides"] = workspace_compilation_overrides

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
        '''The repository's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#name GoogleDataformRepository#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def git_remote_settings(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryGitRemoteSettings"]:
        '''git_remote_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#git_remote_settings GoogleDataformRepository#git_remote_settings}
        '''
        result = self._values.get("git_remote_settings")
        return typing.cast(typing.Optional["GoogleDataformRepositoryGitRemoteSettings"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#id GoogleDataformRepository#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#project GoogleDataformRepository#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''A reference to the region.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#region GoogleDataformRepository#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataformRepositoryTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#timeouts GoogleDataformRepository#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataformRepositoryTimeouts"], result)

    @builtins.property
    def workspace_compilation_overrides(
        self,
    ) -> typing.Optional["GoogleDataformRepositoryWorkspaceCompilationOverrides"]:
        '''workspace_compilation_overrides block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#workspace_compilation_overrides GoogleDataformRepository#workspace_compilation_overrides}
        '''
        result = self._values.get("workspace_compilation_overrides")
        return typing.cast(typing.Optional["GoogleDataformRepositoryWorkspaceCompilationOverrides"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryGitRemoteSettings",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_token_secret_version": "authenticationTokenSecretVersion",
        "default_branch": "defaultBranch",
        "url": "url",
    },
)
class GoogleDataformRepositoryGitRemoteSettings:
    def __init__(
        self,
        *,
        authentication_token_secret_version: builtins.str,
        default_branch: builtins.str,
        url: builtins.str,
    ) -> None:
        '''
        :param authentication_token_secret_version: The name of the Secret Manager secret version to use as an authentication token for Git operations. Must be in the format projects/* /secrets/* /versions/*. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#authentication_token_secret_version GoogleDataformRepository#authentication_token_secret_version} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param default_branch: The Git remote's default branch name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#default_branch GoogleDataformRepository#default_branch}
        :param url: The Git remote's URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#url GoogleDataformRepository#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c21af2bc6bfb3bab1f9bc417185401720314c52dbfc807d5870bf1320efd6dd)
            check_type(argname="argument authentication_token_secret_version", value=authentication_token_secret_version, expected_type=type_hints["authentication_token_secret_version"])
            check_type(argname="argument default_branch", value=default_branch, expected_type=type_hints["default_branch"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authentication_token_secret_version": authentication_token_secret_version,
            "default_branch": default_branch,
            "url": url,
        }

    @builtins.property
    def authentication_token_secret_version(self) -> builtins.str:
        '''The name of the Secret Manager secret version to use as an authentication token for Git operations.

        Must be in the format projects/* /secrets/* /versions/*.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#authentication_token_secret_version GoogleDataformRepository#authentication_token_secret_version}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("authentication_token_secret_version")
        assert result is not None, "Required property 'authentication_token_secret_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_branch(self) -> builtins.str:
        '''The Git remote's default branch name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#default_branch GoogleDataformRepository#default_branch}
        '''
        result = self._values.get("default_branch")
        assert result is not None, "Required property 'default_branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The Git remote's URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#url GoogleDataformRepository#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryGitRemoteSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryGitRemoteSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryGitRemoteSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97873d5926dd2154336fe47a5fbab943469af69a4d3b88ed9fd639545b49564c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="tokenStatus")
    def token_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenStatus"))

    @builtins.property
    @jsii.member(jsii_name="authenticationTokenSecretVersionInput")
    def authentication_token_secret_version_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationTokenSecretVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBranchInput")
    def default_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationTokenSecretVersion")
    def authentication_token_secret_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationTokenSecretVersion"))

    @authentication_token_secret_version.setter
    def authentication_token_secret_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a229a599e9211b12b86b14f4f3bd35ccc1d537ccdd4e44035a0f1f4d6901538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationTokenSecretVersion", value)

    @builtins.property
    @jsii.member(jsii_name="defaultBranch")
    def default_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultBranch"))

    @default_branch.setter
    def default_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783c7f3edbc4f113d3f2f8030f9e1b541eb9fcfe76ce3f354466f2be521fcea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultBranch", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7efaa8f3af0f47c4c5aad5ec4ee382c3c57cb67dba3661479611d7a03c53a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataformRepositoryGitRemoteSettings]:
        return typing.cast(typing.Optional[GoogleDataformRepositoryGitRemoteSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataformRepositoryGitRemoteSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed0e9b2e2577a2ba5242aedfcdf814880d69c5bd7dc2f5ae13966b24bf118ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataformRepositoryTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#create GoogleDataformRepository#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#delete GoogleDataformRepository#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#update GoogleDataformRepository#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2719976fd13de943c3167e1e6739094d2ed568298a0d57656b4f8c1ca35518d5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#create GoogleDataformRepository#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#delete GoogleDataformRepository#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#update GoogleDataformRepository#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b7f381de35bc803a505908c5d40709d47da540ac9a4efa5c335cda31d3406ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__283b11723732b3f3229e899e367657cf2cfda342929ad3c7fdf312a3b32d204f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd561d679f0123739773decaee3123635124ce0ad6fb75979c5873452bf740d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091bbe88824867d0d2d464ac5c6f801cc11555cc988d1b11a03032491f5144b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9b463fb2ecd020cf23c10f44bf1c90ac3e794ac611b652fc86faec64dab9c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryWorkspaceCompilationOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "default_database": "defaultDatabase",
        "schema_suffix": "schemaSuffix",
        "table_prefix": "tablePrefix",
    },
)
class GoogleDataformRepositoryWorkspaceCompilationOverrides:
    def __init__(
        self,
        *,
        default_database: typing.Optional[builtins.str] = None,
        schema_suffix: typing.Optional[builtins.str] = None,
        table_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_database: Optional. The default database (Google Cloud project ID). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#default_database GoogleDataformRepository#default_database}
        :param schema_suffix: Optional. The suffix that should be appended to all schema (BigQuery dataset ID) names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#schema_suffix GoogleDataformRepository#schema_suffix}
        :param table_prefix: Optional. The prefix that should be prepended to all table names. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#table_prefix GoogleDataformRepository#table_prefix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cecc5f15ece6202297d034039c369da9796c3f7977e6f14fe5b93e4673192496)
            check_type(argname="argument default_database", value=default_database, expected_type=type_hints["default_database"])
            check_type(argname="argument schema_suffix", value=schema_suffix, expected_type=type_hints["schema_suffix"])
            check_type(argname="argument table_prefix", value=table_prefix, expected_type=type_hints["table_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_database is not None:
            self._values["default_database"] = default_database
        if schema_suffix is not None:
            self._values["schema_suffix"] = schema_suffix
        if table_prefix is not None:
            self._values["table_prefix"] = table_prefix

    @builtins.property
    def default_database(self) -> typing.Optional[builtins.str]:
        '''Optional. The default database (Google Cloud project ID).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#default_database GoogleDataformRepository#default_database}
        '''
        result = self._values.get("default_database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_suffix(self) -> typing.Optional[builtins.str]:
        '''Optional. The suffix that should be appended to all schema (BigQuery dataset ID) names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#schema_suffix GoogleDataformRepository#schema_suffix}
        '''
        result = self._values.get("schema_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_prefix(self) -> typing.Optional[builtins.str]:
        '''Optional. The prefix that should be prepended to all table names.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_dataform_repository#table_prefix GoogleDataformRepository#table_prefix}
        '''
        result = self._values.get("table_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataformRepositoryWorkspaceCompilationOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataformRepositoryWorkspaceCompilationOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataformRepository.GoogleDataformRepositoryWorkspaceCompilationOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6384b9c375c124f95f11e9336c92d5bbce4922619dd88f6973361b8d486f17b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultDatabase")
    def reset_default_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultDatabase", []))

    @jsii.member(jsii_name="resetSchemaSuffix")
    def reset_schema_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchemaSuffix", []))

    @jsii.member(jsii_name="resetTablePrefix")
    def reset_table_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTablePrefix", []))

    @builtins.property
    @jsii.member(jsii_name="defaultDatabaseInput")
    def default_database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultDatabaseInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaSuffixInput")
    def schema_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="tablePrefixInput")
    def table_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tablePrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDatabase")
    def default_database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultDatabase"))

    @default_database.setter
    def default_database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3279c69ac87fdabe26cef05ed908210decd1e256ea1e9223654a0ba4312b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDatabase", value)

    @builtins.property
    @jsii.member(jsii_name="schemaSuffix")
    def schema_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaSuffix"))

    @schema_suffix.setter
    def schema_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fccd0e68cdb88b87f8196a96507981f3efad94bbc9e326994243901135833e1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="tablePrefix")
    def table_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tablePrefix"))

    @table_prefix.setter
    def table_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9267a09d91c0d74eeb9d655ce38bd621c37013c8a9480927bf7bb3da611c7446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tablePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataformRepositoryWorkspaceCompilationOverrides]:
        return typing.cast(typing.Optional[GoogleDataformRepositoryWorkspaceCompilationOverrides], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataformRepositoryWorkspaceCompilationOverrides],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee928fadd0462924fe5af73d22e3f1bfb274e58b7a913f0aea24dc0332f5ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GoogleDataformRepository",
    "GoogleDataformRepositoryConfig",
    "GoogleDataformRepositoryGitRemoteSettings",
    "GoogleDataformRepositoryGitRemoteSettingsOutputReference",
    "GoogleDataformRepositoryTimeouts",
    "GoogleDataformRepositoryTimeoutsOutputReference",
    "GoogleDataformRepositoryWorkspaceCompilationOverrides",
    "GoogleDataformRepositoryWorkspaceCompilationOverridesOutputReference",
]

publication.publish()

def _typecheckingstub__b2dbd824e559816fa9aa1a41d21f96fb5232e9bbae6a2495bc5c0d34376681af(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    git_remote_settings: typing.Optional[typing.Union[GoogleDataformRepositoryGitRemoteSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataformRepositoryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workspace_compilation_overrides: typing.Optional[typing.Union[GoogleDataformRepositoryWorkspaceCompilationOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__fdab58a8336d3c636189858c8588a677dfbd052ab3c14cd40d8a49268abe669a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f4a057106a343e989703f7b4f95ba2b705fc513ca7ab7e2b71229b381e155b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71eede5c5296a69640fb97de4b79bb9c672e8cf27c8ab290f2b532f6c87b7800(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744cc633499380c09cf18b996dc875cbfe006cccf23bcf66b03b1b203bb195b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46292713426893130af4f48ca81b8e9914d1899beb7a04a7c673d8ef7571474b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    git_remote_settings: typing.Optional[typing.Union[GoogleDataformRepositoryGitRemoteSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataformRepositoryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workspace_compilation_overrides: typing.Optional[typing.Union[GoogleDataformRepositoryWorkspaceCompilationOverrides, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c21af2bc6bfb3bab1f9bc417185401720314c52dbfc807d5870bf1320efd6dd(
    *,
    authentication_token_secret_version: builtins.str,
    default_branch: builtins.str,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97873d5926dd2154336fe47a5fbab943469af69a4d3b88ed9fd639545b49564c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a229a599e9211b12b86b14f4f3bd35ccc1d537ccdd4e44035a0f1f4d6901538(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783c7f3edbc4f113d3f2f8030f9e1b541eb9fcfe76ce3f354466f2be521fcea9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7efaa8f3af0f47c4c5aad5ec4ee382c3c57cb67dba3661479611d7a03c53a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed0e9b2e2577a2ba5242aedfcdf814880d69c5bd7dc2f5ae13966b24bf118ce(
    value: typing.Optional[GoogleDataformRepositoryGitRemoteSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2719976fd13de943c3167e1e6739094d2ed568298a0d57656b4f8c1ca35518d5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7f381de35bc803a505908c5d40709d47da540ac9a4efa5c335cda31d3406ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283b11723732b3f3229e899e367657cf2cfda342929ad3c7fdf312a3b32d204f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd561d679f0123739773decaee3123635124ce0ad6fb75979c5873452bf740d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091bbe88824867d0d2d464ac5c6f801cc11555cc988d1b11a03032491f5144b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9b463fb2ecd020cf23c10f44bf1c90ac3e794ac611b652fc86faec64dab9c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataformRepositoryTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cecc5f15ece6202297d034039c369da9796c3f7977e6f14fe5b93e4673192496(
    *,
    default_database: typing.Optional[builtins.str] = None,
    schema_suffix: typing.Optional[builtins.str] = None,
    table_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6384b9c375c124f95f11e9336c92d5bbce4922619dd88f6973361b8d486f17b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3279c69ac87fdabe26cef05ed908210decd1e256ea1e9223654a0ba4312b54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccd0e68cdb88b87f8196a96507981f3efad94bbc9e326994243901135833e1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9267a09d91c0d74eeb9d655ce38bd621c37013c8a9480927bf7bb3da611c7446(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee928fadd0462924fe5af73d22e3f1bfb274e58b7a913f0aea24dc0332f5ee9(
    value: typing.Optional[GoogleDataformRepositoryWorkspaceCompilationOverrides],
) -> None:
    """Type checking stubs"""
    pass
