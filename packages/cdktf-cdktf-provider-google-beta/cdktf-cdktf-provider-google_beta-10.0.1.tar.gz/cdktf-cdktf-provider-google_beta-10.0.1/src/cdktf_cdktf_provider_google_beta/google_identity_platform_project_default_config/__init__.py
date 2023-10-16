'''
# `google_identity_platform_project_default_config`

Refer to the Terraform Registory for docs: [`google_identity_platform_project_default_config`](https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config).
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


class GoogleIdentityPlatformProjectDefaultConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfig",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config google_identity_platform_project_default_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        sign_in: typing.Optional[typing.Union["GoogleIdentityPlatformProjectDefaultConfigSignIn", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleIdentityPlatformProjectDefaultConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config google_identity_platform_project_default_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#id GoogleIdentityPlatformProjectDefaultConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#project GoogleIdentityPlatformProjectDefaultConfig#project}.
        :param sign_in: sign_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#sign_in GoogleIdentityPlatformProjectDefaultConfig#sign_in}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#timeouts GoogleIdentityPlatformProjectDefaultConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab8493d692e4243e4e74b19ce49dce3f80e5130f318a0a2223086180993bb93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleIdentityPlatformProjectDefaultConfigConfig(
            id=id,
            project=project,
            sign_in=sign_in,
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

    @jsii.member(jsii_name="putSignIn")
    def put_sign_in(
        self,
        *,
        allow_duplicate_emails: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        anonymous: typing.Optional[typing.Union["GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous", typing.Dict[builtins.str, typing.Any]]] = None,
        email: typing.Optional[typing.Union["GoogleIdentityPlatformProjectDefaultConfigSignInEmail", typing.Dict[builtins.str, typing.Any]]] = None,
        phone_number: typing.Optional[typing.Union["GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_duplicate_emails: Whether to allow more than one account to have the same email. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#allow_duplicate_emails GoogleIdentityPlatformProjectDefaultConfig#allow_duplicate_emails}
        :param anonymous: anonymous block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#anonymous GoogleIdentityPlatformProjectDefaultConfig#anonymous}
        :param email: email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#email GoogleIdentityPlatformProjectDefaultConfig#email}
        :param phone_number: phone_number block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#phone_number GoogleIdentityPlatformProjectDefaultConfig#phone_number}
        '''
        value = GoogleIdentityPlatformProjectDefaultConfigSignIn(
            allow_duplicate_emails=allow_duplicate_emails,
            anonymous=anonymous,
            email=email,
            phone_number=phone_number,
        )

        return typing.cast(None, jsii.invoke(self, "putSignIn", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#create GoogleIdentityPlatformProjectDefaultConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#delete GoogleIdentityPlatformProjectDefaultConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#update GoogleIdentityPlatformProjectDefaultConfig#update}.
        '''
        value = GoogleIdentityPlatformProjectDefaultConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSignIn")
    def reset_sign_in(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignIn", []))

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
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="signIn")
    def sign_in(
        self,
    ) -> "GoogleIdentityPlatformProjectDefaultConfigSignInOutputReference":
        return typing.cast("GoogleIdentityPlatformProjectDefaultConfigSignInOutputReference", jsii.get(self, "signIn"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleIdentityPlatformProjectDefaultConfigTimeoutsOutputReference":
        return typing.cast("GoogleIdentityPlatformProjectDefaultConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="signInInput")
    def sign_in_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformProjectDefaultConfigSignIn"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformProjectDefaultConfigSignIn"], jsii.get(self, "signInInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIdentityPlatformProjectDefaultConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleIdentityPlatformProjectDefaultConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4819c244bd15eb9629ea52be4bf87f37216a7196361af31fa092a6edddfc5469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dab9dac65c21ef1df67c586fa84c057d409682738cd5e2a5e4f2f3458615404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "project": "project",
        "sign_in": "signIn",
        "timeouts": "timeouts",
    },
)
class GoogleIdentityPlatformProjectDefaultConfigConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        sign_in: typing.Optional[typing.Union["GoogleIdentityPlatformProjectDefaultConfigSignIn", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleIdentityPlatformProjectDefaultConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#id GoogleIdentityPlatformProjectDefaultConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#project GoogleIdentityPlatformProjectDefaultConfig#project}.
        :param sign_in: sign_in block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#sign_in GoogleIdentityPlatformProjectDefaultConfig#sign_in}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#timeouts GoogleIdentityPlatformProjectDefaultConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(sign_in, dict):
            sign_in = GoogleIdentityPlatformProjectDefaultConfigSignIn(**sign_in)
        if isinstance(timeouts, dict):
            timeouts = GoogleIdentityPlatformProjectDefaultConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b920786dca08736e90697e1efd09cd17168145fedf6b2d574b6e92eee251ac9b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument sign_in", value=sign_in, expected_type=type_hints["sign_in"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if sign_in is not None:
            self._values["sign_in"] = sign_in
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
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#id GoogleIdentityPlatformProjectDefaultConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#project GoogleIdentityPlatformProjectDefaultConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sign_in(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformProjectDefaultConfigSignIn"]:
        '''sign_in block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#sign_in GoogleIdentityPlatformProjectDefaultConfig#sign_in}
        '''
        result = self._values.get("sign_in")
        return typing.cast(typing.Optional["GoogleIdentityPlatformProjectDefaultConfigSignIn"], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformProjectDefaultConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#timeouts GoogleIdentityPlatformProjectDefaultConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleIdentityPlatformProjectDefaultConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformProjectDefaultConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigSignIn",
    jsii_struct_bases=[],
    name_mapping={
        "allow_duplicate_emails": "allowDuplicateEmails",
        "anonymous": "anonymous",
        "email": "email",
        "phone_number": "phoneNumber",
    },
)
class GoogleIdentityPlatformProjectDefaultConfigSignIn:
    def __init__(
        self,
        *,
        allow_duplicate_emails: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        anonymous: typing.Optional[typing.Union["GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous", typing.Dict[builtins.str, typing.Any]]] = None,
        email: typing.Optional[typing.Union["GoogleIdentityPlatformProjectDefaultConfigSignInEmail", typing.Dict[builtins.str, typing.Any]]] = None,
        phone_number: typing.Optional[typing.Union["GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_duplicate_emails: Whether to allow more than one account to have the same email. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#allow_duplicate_emails GoogleIdentityPlatformProjectDefaultConfig#allow_duplicate_emails}
        :param anonymous: anonymous block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#anonymous GoogleIdentityPlatformProjectDefaultConfig#anonymous}
        :param email: email block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#email GoogleIdentityPlatformProjectDefaultConfig#email}
        :param phone_number: phone_number block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#phone_number GoogleIdentityPlatformProjectDefaultConfig#phone_number}
        '''
        if isinstance(anonymous, dict):
            anonymous = GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous(**anonymous)
        if isinstance(email, dict):
            email = GoogleIdentityPlatformProjectDefaultConfigSignInEmail(**email)
        if isinstance(phone_number, dict):
            phone_number = GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber(**phone_number)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb77073c489892d485944b3a3a567b5fd894402c86ba7f63b2f1a76b3c5d3db)
            check_type(argname="argument allow_duplicate_emails", value=allow_duplicate_emails, expected_type=type_hints["allow_duplicate_emails"])
            check_type(argname="argument anonymous", value=anonymous, expected_type=type_hints["anonymous"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_duplicate_emails is not None:
            self._values["allow_duplicate_emails"] = allow_duplicate_emails
        if anonymous is not None:
            self._values["anonymous"] = anonymous
        if email is not None:
            self._values["email"] = email
        if phone_number is not None:
            self._values["phone_number"] = phone_number

    @builtins.property
    def allow_duplicate_emails(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow more than one account to have the same email.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#allow_duplicate_emails GoogleIdentityPlatformProjectDefaultConfig#allow_duplicate_emails}
        '''
        result = self._values.get("allow_duplicate_emails")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def anonymous(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous"]:
        '''anonymous block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#anonymous GoogleIdentityPlatformProjectDefaultConfig#anonymous}
        '''
        result = self._values.get("anonymous")
        return typing.cast(typing.Optional["GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous"], result)

    @builtins.property
    def email(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformProjectDefaultConfigSignInEmail"]:
        '''email block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#email GoogleIdentityPlatformProjectDefaultConfig#email}
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional["GoogleIdentityPlatformProjectDefaultConfigSignInEmail"], result)

    @builtins.property
    def phone_number(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber"]:
        '''phone_number block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#phone_number GoogleIdentityPlatformProjectDefaultConfig#phone_number}
        '''
        result = self._values.get("phone_number")
        return typing.cast(typing.Optional["GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformProjectDefaultConfigSignIn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether anonymous user auth is enabled for the project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#enabled GoogleIdentityPlatformProjectDefaultConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb7e1e114c7614d3a76b12763773465cdce2eff3cb10bb7f35447b78eace914)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether anonymous user auth is enabled for the project or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#enabled GoogleIdentityPlatformProjectDefaultConfig#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformProjectDefaultConfigSignInAnonymousOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigSignInAnonymousOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf6aaf40e3e411223ef2e8f7bf80e184cfdf60cec7497ebd5a04eb2e42315eb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c15338a349da2f1005ba17a9bfff603c8377ccbdc02c897b93b5174b887b4085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8e47c1cd76736d1b2e2df16f878b1eb959c8df31ba288ca3a5bcca15c56b61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigSignInEmail",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "password_required": "passwordRequired"},
)
class GoogleIdentityPlatformProjectDefaultConfigSignInEmail:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether email auth is enabled for the project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#enabled GoogleIdentityPlatformProjectDefaultConfig#enabled}
        :param password_required: Whether a password is required for email auth or not. If true, both an email and password must be provided to sign in. If false, a user may sign in via either email/password or email link. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#password_required GoogleIdentityPlatformProjectDefaultConfig#password_required}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49a061acddd16bc4d6cb2ab8817e5831ce537777c574fd9c4c93dd0a4b79372f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument password_required", value=password_required, expected_type=type_hints["password_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if password_required is not None:
            self._values["password_required"] = password_required

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether email auth is enabled for the project or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#enabled GoogleIdentityPlatformProjectDefaultConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether a password is required for email auth or not.

        If true, both an email and
        password must be provided to sign in. If false, a user may sign in via either
        email/password or email link.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#password_required GoogleIdentityPlatformProjectDefaultConfig#password_required}
        '''
        result = self._values.get("password_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformProjectDefaultConfigSignInEmail(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformProjectDefaultConfigSignInEmailOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigSignInEmailOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d0fd81b08eb664d0e8c7a9652ee8bfb2150c0b06fdc5dd3623af1b5ab5b4f18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetPasswordRequired")
    def reset_password_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordRequired", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordRequiredInput")
    def password_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a9d14032b95dde9b75eaed13d290c725452879fb7aee63a922bf6a73dafc5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="passwordRequired")
    def password_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordRequired"))

    @password_required.setter
    def password_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__449cf09484b3ad27e48752e7f1c186ec6512feb36b7522750513e850add6f6bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordRequired", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInEmail]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInEmail], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInEmail],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be18078e37c6cddaed185e8357480cd4268f8c183d2efe3a8efa32cd8a022d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigSignInHashConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleIdentityPlatformProjectDefaultConfigSignInHashConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformProjectDefaultConfigSignInHashConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformProjectDefaultConfigSignInHashConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigSignInHashConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f8b97e219edac65fb411c1e4ea9eff7fd024ed697c347f782e0a51cf258da62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleIdentityPlatformProjectDefaultConfigSignInHashConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e18ffd4cfc95c3929fe009918a437b323ab986eb1e41b8b549fb34c0cfdacf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleIdentityPlatformProjectDefaultConfigSignInHashConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1d84ae48edc43f500437a14f20b9b1f4e883a44273ef7aafcb4b6f01401e24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bfc0f4cca27d11bdad0c306f8b3636f875c46ae92b535ddd8cb410bfa669267)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16562f7657d352bd89ce65c3b5c9c52d13ced276afd6454223316cc4f3e56d58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class GoogleIdentityPlatformProjectDefaultConfigSignInHashConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigSignInHashConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d5f032f898c1877f4f771aaef40b0e78b79e467ce1dc8b30a515ceb65f4b4f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="algorithm")
    def algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "algorithm"))

    @builtins.property
    @jsii.member(jsii_name="memoryCost")
    def memory_cost(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryCost"))

    @builtins.property
    @jsii.member(jsii_name="rounds")
    def rounds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rounds"))

    @builtins.property
    @jsii.member(jsii_name="saltSeparator")
    def salt_separator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "saltSeparator"))

    @builtins.property
    @jsii.member(jsii_name="signerKey")
    def signer_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "signerKey"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInHashConfig]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInHashConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInHashConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7baade2e9fa6058cddd5585a7c6b62a623e5cd4115edf17d1390286f286127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GoogleIdentityPlatformProjectDefaultConfigSignInOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigSignInOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2db8660ae05c463fbfc067f335168e54c5226b2f66f56136a911247bf485f442)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnonymous")
    def put_anonymous(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Whether anonymous user auth is enabled for the project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#enabled GoogleIdentityPlatformProjectDefaultConfig#enabled}
        '''
        value = GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous(
            enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putAnonymous", [value]))

    @jsii.member(jsii_name="putEmail")
    def put_email(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether email auth is enabled for the project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#enabled GoogleIdentityPlatformProjectDefaultConfig#enabled}
        :param password_required: Whether a password is required for email auth or not. If true, both an email and password must be provided to sign in. If false, a user may sign in via either email/password or email link. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#password_required GoogleIdentityPlatformProjectDefaultConfig#password_required}
        '''
        value = GoogleIdentityPlatformProjectDefaultConfigSignInEmail(
            enabled=enabled, password_required=password_required
        )

        return typing.cast(None, jsii.invoke(self, "putEmail", [value]))

    @jsii.member(jsii_name="putPhoneNumber")
    def put_phone_number(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        test_phone_numbers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: Whether phone number auth is enabled for the project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#enabled GoogleIdentityPlatformProjectDefaultConfig#enabled}
        :param test_phone_numbers: A map of <test phone number, fake code> that can be used for phone auth testing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#test_phone_numbers GoogleIdentityPlatformProjectDefaultConfig#test_phone_numbers}
        '''
        value = GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber(
            enabled=enabled, test_phone_numbers=test_phone_numbers
        )

        return typing.cast(None, jsii.invoke(self, "putPhoneNumber", [value]))

    @jsii.member(jsii_name="resetAllowDuplicateEmails")
    def reset_allow_duplicate_emails(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowDuplicateEmails", []))

    @jsii.member(jsii_name="resetAnonymous")
    def reset_anonymous(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnonymous", []))

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetPhoneNumber")
    def reset_phone_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhoneNumber", []))

    @builtins.property
    @jsii.member(jsii_name="anonymous")
    def anonymous(
        self,
    ) -> GoogleIdentityPlatformProjectDefaultConfigSignInAnonymousOutputReference:
        return typing.cast(GoogleIdentityPlatformProjectDefaultConfigSignInAnonymousOutputReference, jsii.get(self, "anonymous"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(
        self,
    ) -> GoogleIdentityPlatformProjectDefaultConfigSignInEmailOutputReference:
        return typing.cast(GoogleIdentityPlatformProjectDefaultConfigSignInEmailOutputReference, jsii.get(self, "email"))

    @builtins.property
    @jsii.member(jsii_name="hashConfig")
    def hash_config(
        self,
    ) -> GoogleIdentityPlatformProjectDefaultConfigSignInHashConfigList:
        return typing.cast(GoogleIdentityPlatformProjectDefaultConfigSignInHashConfigList, jsii.get(self, "hashConfig"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(
        self,
    ) -> "GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumberOutputReference":
        return typing.cast("GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumberOutputReference", jsii.get(self, "phoneNumber"))

    @builtins.property
    @jsii.member(jsii_name="allowDuplicateEmailsInput")
    def allow_duplicate_emails_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowDuplicateEmailsInput"))

    @builtins.property
    @jsii.member(jsii_name="anonymousInput")
    def anonymous_input(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous], jsii.get(self, "anonymousInput"))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInEmail]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInEmail], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(
        self,
    ) -> typing.Optional["GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber"]:
        return typing.cast(typing.Optional["GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber"], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="allowDuplicateEmails")
    def allow_duplicate_emails(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowDuplicateEmails"))

    @allow_duplicate_emails.setter
    def allow_duplicate_emails(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__346e6c0db4ab08ed6333fe115a5dcd247667332d6647ab21d90153b3129b5a45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowDuplicateEmails", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignIn]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignIn], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignIn],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62cf883f01d24727853c0ac2001f55f25f8f4828037de10a3f14f373999d2594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "test_phone_numbers": "testPhoneNumbers"},
)
class GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        test_phone_numbers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param enabled: Whether phone number auth is enabled for the project or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#enabled GoogleIdentityPlatformProjectDefaultConfig#enabled}
        :param test_phone_numbers: A map of <test phone number, fake code> that can be used for phone auth testing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#test_phone_numbers GoogleIdentityPlatformProjectDefaultConfig#test_phone_numbers}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8113388f0e733c60a9ffe3f16ce6b601cf740d592fe0d4ee9b6d34b09ccfcc9d)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument test_phone_numbers", value=test_phone_numbers, expected_type=type_hints["test_phone_numbers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if test_phone_numbers is not None:
            self._values["test_phone_numbers"] = test_phone_numbers

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether phone number auth is enabled for the project or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#enabled GoogleIdentityPlatformProjectDefaultConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def test_phone_numbers(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of <test phone number, fake code> that can be used for phone auth testing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#test_phone_numbers GoogleIdentityPlatformProjectDefaultConfig#test_phone_numbers}
        '''
        result = self._values.get("test_phone_numbers")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumberOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumberOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a808e27b4915d516d1c17d58a4b22116f9ef18ca98fc436fdfda4c3875b09d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetTestPhoneNumbers")
    def reset_test_phone_numbers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestPhoneNumbers", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="testPhoneNumbersInput")
    def test_phone_numbers_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "testPhoneNumbersInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0937d4e8f50856a4cb628cac0382f3b70a9e38fa6491d1684a7c28949004bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="testPhoneNumbers")
    def test_phone_numbers(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "testPhoneNumbers"))

    @test_phone_numbers.setter
    def test_phone_numbers(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d53e233c0d08bce03d684b3ecd1e78af90241a20f1d9b61caa449121961a01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testPhoneNumbers", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber]:
        return typing.cast(typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9f9a0a9720deda11b11894e38478d1ccb86f4dc2980acc9002bdc8ac04bca1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleIdentityPlatformProjectDefaultConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#create GoogleIdentityPlatformProjectDefaultConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#delete GoogleIdentityPlatformProjectDefaultConfig#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#update GoogleIdentityPlatformProjectDefaultConfig#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10272196d925772b67932f5fb9e51ae7705a150724564b940132025eaac99886)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#create GoogleIdentityPlatformProjectDefaultConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#delete GoogleIdentityPlatformProjectDefaultConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_identity_platform_project_default_config#update GoogleIdentityPlatformProjectDefaultConfig#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleIdentityPlatformProjectDefaultConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleIdentityPlatformProjectDefaultConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleIdentityPlatformProjectDefaultConfig.GoogleIdentityPlatformProjectDefaultConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2340058c64ad58d171f8a196814a0b48eae649b3a32a4c3564178067be75b7d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e9c4a82ef0996afd5b69f95c31cb530383a33cbb40d3fa3f6699bb13784ac56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46cb6b9df3414d89c0376a3e1900105015d8859fe1aab0d40ff914595687dfcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5adb50b68439b6645a3c632f159ec3d35fea1ae8a8e845fc0bd44c8a5d7122e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformProjectDefaultConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformProjectDefaultConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformProjectDefaultConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383cf968d2f1db86e15c7ecc7de178556394a46b05c22be0e5b9d05a6c8f11f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GoogleIdentityPlatformProjectDefaultConfig",
    "GoogleIdentityPlatformProjectDefaultConfigConfig",
    "GoogleIdentityPlatformProjectDefaultConfigSignIn",
    "GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous",
    "GoogleIdentityPlatformProjectDefaultConfigSignInAnonymousOutputReference",
    "GoogleIdentityPlatformProjectDefaultConfigSignInEmail",
    "GoogleIdentityPlatformProjectDefaultConfigSignInEmailOutputReference",
    "GoogleIdentityPlatformProjectDefaultConfigSignInHashConfig",
    "GoogleIdentityPlatformProjectDefaultConfigSignInHashConfigList",
    "GoogleIdentityPlatformProjectDefaultConfigSignInHashConfigOutputReference",
    "GoogleIdentityPlatformProjectDefaultConfigSignInOutputReference",
    "GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber",
    "GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumberOutputReference",
    "GoogleIdentityPlatformProjectDefaultConfigTimeouts",
    "GoogleIdentityPlatformProjectDefaultConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3ab8493d692e4243e4e74b19ce49dce3f80e5130f318a0a2223086180993bb93(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    sign_in: typing.Optional[typing.Union[GoogleIdentityPlatformProjectDefaultConfigSignIn, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleIdentityPlatformProjectDefaultConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__4819c244bd15eb9629ea52be4bf87f37216a7196361af31fa092a6edddfc5469(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dab9dac65c21ef1df67c586fa84c057d409682738cd5e2a5e4f2f3458615404(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b920786dca08736e90697e1efd09cd17168145fedf6b2d574b6e92eee251ac9b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    sign_in: typing.Optional[typing.Union[GoogleIdentityPlatformProjectDefaultConfigSignIn, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleIdentityPlatformProjectDefaultConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb77073c489892d485944b3a3a567b5fd894402c86ba7f63b2f1a76b3c5d3db(
    *,
    allow_duplicate_emails: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    anonymous: typing.Optional[typing.Union[GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous, typing.Dict[builtins.str, typing.Any]]] = None,
    email: typing.Optional[typing.Union[GoogleIdentityPlatformProjectDefaultConfigSignInEmail, typing.Dict[builtins.str, typing.Any]]] = None,
    phone_number: typing.Optional[typing.Union[GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb7e1e114c7614d3a76b12763773465cdce2eff3cb10bb7f35447b78eace914(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6aaf40e3e411223ef2e8f7bf80e184cfdf60cec7497ebd5a04eb2e42315eb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c15338a349da2f1005ba17a9bfff603c8377ccbdc02c897b93b5174b887b4085(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8e47c1cd76736d1b2e2df16f878b1eb959c8df31ba288ca3a5bcca15c56b61(
    value: typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInAnonymous],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a061acddd16bc4d6cb2ab8817e5831ce537777c574fd9c4c93dd0a4b79372f(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0fd81b08eb664d0e8c7a9652ee8bfb2150c0b06fdc5dd3623af1b5ab5b4f18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a9d14032b95dde9b75eaed13d290c725452879fb7aee63a922bf6a73dafc5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449cf09484b3ad27e48752e7f1c186ec6512feb36b7522750513e850add6f6bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be18078e37c6cddaed185e8357480cd4268f8c183d2efe3a8efa32cd8a022d9(
    value: typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInEmail],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f8b97e219edac65fb411c1e4ea9eff7fd024ed697c347f782e0a51cf258da62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e18ffd4cfc95c3929fe009918a437b323ab986eb1e41b8b549fb34c0cfdacf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1d84ae48edc43f500437a14f20b9b1f4e883a44273ef7aafcb4b6f01401e24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bfc0f4cca27d11bdad0c306f8b3636f875c46ae92b535ddd8cb410bfa669267(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16562f7657d352bd89ce65c3b5c9c52d13ced276afd6454223316cc4f3e56d58(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5f032f898c1877f4f771aaef40b0e78b79e467ce1dc8b30a515ceb65f4b4f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7baade2e9fa6058cddd5585a7c6b62a623e5cd4115edf17d1390286f286127(
    value: typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInHashConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db8660ae05c463fbfc067f335168e54c5226b2f66f56136a911247bf485f442(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346e6c0db4ab08ed6333fe115a5dcd247667332d6647ab21d90153b3129b5a45(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cf883f01d24727853c0ac2001f55f25f8f4828037de10a3f14f373999d2594(
    value: typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignIn],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8113388f0e733c60a9ffe3f16ce6b601cf740d592fe0d4ee9b6d34b09ccfcc9d(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    test_phone_numbers: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a808e27b4915d516d1c17d58a4b22116f9ef18ca98fc436fdfda4c3875b09d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0937d4e8f50856a4cb628cac0382f3b70a9e38fa6491d1684a7c28949004bc5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d53e233c0d08bce03d684b3ecd1e78af90241a20f1d9b61caa449121961a01(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f9a0a9720deda11b11894e38478d1ccb86f4dc2980acc9002bdc8ac04bca1f(
    value: typing.Optional[GoogleIdentityPlatformProjectDefaultConfigSignInPhoneNumber],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10272196d925772b67932f5fb9e51ae7705a150724564b940132025eaac99886(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2340058c64ad58d171f8a196814a0b48eae649b3a32a4c3564178067be75b7d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9c4a82ef0996afd5b69f95c31cb530383a33cbb40d3fa3f6699bb13784ac56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cb6b9df3414d89c0376a3e1900105015d8859fe1aab0d40ff914595687dfcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5adb50b68439b6645a3c632f159ec3d35fea1ae8a8e845fc0bd44c8a5d7122e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383cf968d2f1db86e15c7ecc7de178556394a46b05c22be0e5b9d05a6c8f11f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleIdentityPlatformProjectDefaultConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
