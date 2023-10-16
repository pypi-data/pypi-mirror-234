'''
# `google_gke_hub_feature_membership`

Refer to the Terraform Registory for docs: [`google_gke_hub_feature_membership`](https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership).
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


class GoogleGkeHubFeatureMembership(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembership",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership google_gke_hub_feature_membership}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        feature: builtins.str,
        location: builtins.str,
        membership: builtins.str,
        configmanagement: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagement", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        mesh: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership google_gke_hub_feature_membership} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param feature: The name of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#feature GoogleGkeHubFeatureMembership#feature}
        :param location: The location of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#location GoogleGkeHubFeatureMembership#location}
        :param membership: The name of the membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#membership GoogleGkeHubFeatureMembership#membership}
        :param configmanagement: configmanagement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#configmanagement GoogleGkeHubFeatureMembership#configmanagement}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#id GoogleGkeHubFeatureMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mesh: mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#mesh GoogleGkeHubFeatureMembership#mesh}
        :param project: The project of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#project GoogleGkeHubFeatureMembership#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#timeouts GoogleGkeHubFeatureMembership#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0b329ce2d05634c944e2255fda1d2c15cbf151adf11be93d9c4d1405e05220)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleGkeHubFeatureMembershipConfig(
            feature=feature,
            location=location,
            membership=membership,
            configmanagement=configmanagement,
            id=id,
            mesh=mesh,
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

    @jsii.member(jsii_name="putConfigmanagement")
    def put_configmanagement(
        self,
        *,
        binauthz: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementBinauthz", typing.Dict[builtins.str, typing.Any]]] = None,
        config_sync: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementConfigSync", typing.Dict[builtins.str, typing.Any]]] = None,
        hierarchy_controller: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_controller: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementPolicyController", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param binauthz: binauthz block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#binauthz GoogleGkeHubFeatureMembership#binauthz}
        :param config_sync: config_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#config_sync GoogleGkeHubFeatureMembership#config_sync}
        :param hierarchy_controller: hierarchy_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#hierarchy_controller GoogleGkeHubFeatureMembership#hierarchy_controller}
        :param policy_controller: policy_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#policy_controller GoogleGkeHubFeatureMembership#policy_controller}
        :param version: Optional. Version of ACM to install. Defaults to the latest version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#version GoogleGkeHubFeatureMembership#version}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagement(
            binauthz=binauthz,
            config_sync=config_sync,
            hierarchy_controller=hierarchy_controller,
            policy_controller=policy_controller,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putConfigmanagement", [value]))

    @jsii.member(jsii_name="putMesh")
    def put_mesh(
        self,
        *,
        control_plane: typing.Optional[builtins.str] = None,
        management: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control_plane: **DEPRECATED** Whether to automatically manage Service Mesh control planes. Possible values: CONTROL_PLANE_MANAGEMENT_UNSPECIFIED, AUTOMATIC, MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#control_plane GoogleGkeHubFeatureMembership#control_plane}
        :param management: Whether to automatically manage Service Mesh. Possible values: MANAGEMENT_UNSPECIFIED, MANAGEMENT_AUTOMATIC, MANAGEMENT_MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#management GoogleGkeHubFeatureMembership#management}
        '''
        value = GoogleGkeHubFeatureMembershipMesh(
            control_plane=control_plane, management=management
        )

        return typing.cast(None, jsii.invoke(self, "putMesh", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#create GoogleGkeHubFeatureMembership#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#delete GoogleGkeHubFeatureMembership#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#update GoogleGkeHubFeatureMembership#update}.
        '''
        value = GoogleGkeHubFeatureMembershipTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConfigmanagement")
    def reset_configmanagement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigmanagement", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMesh")
    def reset_mesh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMesh", []))

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
    @jsii.member(jsii_name="configmanagement")
    def configmanagement(
        self,
    ) -> "GoogleGkeHubFeatureMembershipConfigmanagementOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipConfigmanagementOutputReference", jsii.get(self, "configmanagement"))

    @builtins.property
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> "GoogleGkeHubFeatureMembershipMeshOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipMeshOutputReference", jsii.get(self, "mesh"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleGkeHubFeatureMembershipTimeoutsOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="configmanagementInput")
    def configmanagement_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagement"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagement"], jsii.get(self, "configmanagementInput"))

    @builtins.property
    @jsii.member(jsii_name="featureInput")
    def feature_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "featureInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="membershipInput")
    def membership_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "membershipInput"))

    @builtins.property
    @jsii.member(jsii_name="meshInput")
    def mesh_input(self) -> typing.Optional["GoogleGkeHubFeatureMembershipMesh"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipMesh"], jsii.get(self, "meshInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeHubFeatureMembershipTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleGkeHubFeatureMembershipTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="feature")
    def feature(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "feature"))

    @feature.setter
    def feature(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62872bdfceafad454f1f77b15f0c4cc026f50a42b15c1ba4ae1e073493d445cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "feature", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0958d3b43f6eeee77da3758cde573467dcc5caf896edce568f597a324e95a596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026490971551372bb2b4367c899e7d13d507691fcd381768b3818da3e4687d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="membership")
    def membership(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "membership"))

    @membership.setter
    def membership(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b83bed14422792af7953f5b45e04cf6f355b207c43f6d8e8c84d5f3625b5217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "membership", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf9355e466a5d9bc98e79e3e26b9069d4848147b9de0e5c7e2116507a9f86f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "feature": "feature",
        "location": "location",
        "membership": "membership",
        "configmanagement": "configmanagement",
        "id": "id",
        "mesh": "mesh",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleGkeHubFeatureMembershipConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        feature: builtins.str,
        location: builtins.str,
        membership: builtins.str,
        configmanagement: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagement", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        mesh: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param feature: The name of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#feature GoogleGkeHubFeatureMembership#feature}
        :param location: The location of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#location GoogleGkeHubFeatureMembership#location}
        :param membership: The name of the membership. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#membership GoogleGkeHubFeatureMembership#membership}
        :param configmanagement: configmanagement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#configmanagement GoogleGkeHubFeatureMembership#configmanagement}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#id GoogleGkeHubFeatureMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mesh: mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#mesh GoogleGkeHubFeatureMembership#mesh}
        :param project: The project of the feature. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#project GoogleGkeHubFeatureMembership#project}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#timeouts GoogleGkeHubFeatureMembership#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(configmanagement, dict):
            configmanagement = GoogleGkeHubFeatureMembershipConfigmanagement(**configmanagement)
        if isinstance(mesh, dict):
            mesh = GoogleGkeHubFeatureMembershipMesh(**mesh)
        if isinstance(timeouts, dict):
            timeouts = GoogleGkeHubFeatureMembershipTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc454f576b0fc2b00803677a901ef7a86701247db18f878efe02b250d0b540e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument feature", value=feature, expected_type=type_hints["feature"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument membership", value=membership, expected_type=type_hints["membership"])
            check_type(argname="argument configmanagement", value=configmanagement, expected_type=type_hints["configmanagement"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mesh", value=mesh, expected_type=type_hints["mesh"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "feature": feature,
            "location": location,
            "membership": membership,
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
        if configmanagement is not None:
            self._values["configmanagement"] = configmanagement
        if id is not None:
            self._values["id"] = id
        if mesh is not None:
            self._values["mesh"] = mesh
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
    def feature(self) -> builtins.str:
        '''The name of the feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#feature GoogleGkeHubFeatureMembership#feature}
        '''
        result = self._values.get("feature")
        assert result is not None, "Required property 'feature' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#location GoogleGkeHubFeatureMembership#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def membership(self) -> builtins.str:
        '''The name of the membership.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#membership GoogleGkeHubFeatureMembership#membership}
        '''
        result = self._values.get("membership")
        assert result is not None, "Required property 'membership' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configmanagement(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagement"]:
        '''configmanagement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#configmanagement GoogleGkeHubFeatureMembership#configmanagement}
        '''
        result = self._values.get("configmanagement")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagement"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#id GoogleGkeHubFeatureMembership#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mesh(self) -> typing.Optional["GoogleGkeHubFeatureMembershipMesh"]:
        '''mesh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#mesh GoogleGkeHubFeatureMembership#mesh}
        '''
        result = self._values.get("mesh")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipMesh"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project of the feature.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#project GoogleGkeHubFeatureMembership#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleGkeHubFeatureMembershipTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#timeouts GoogleGkeHubFeatureMembership#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagement",
    jsii_struct_bases=[],
    name_mapping={
        "binauthz": "binauthz",
        "config_sync": "configSync",
        "hierarchy_controller": "hierarchyController",
        "policy_controller": "policyController",
        "version": "version",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagement:
    def __init__(
        self,
        *,
        binauthz: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementBinauthz", typing.Dict[builtins.str, typing.Any]]] = None,
        config_sync: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementConfigSync", typing.Dict[builtins.str, typing.Any]]] = None,
        hierarchy_controller: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController", typing.Dict[builtins.str, typing.Any]]] = None,
        policy_controller: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementPolicyController", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param binauthz: binauthz block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#binauthz GoogleGkeHubFeatureMembership#binauthz}
        :param config_sync: config_sync block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#config_sync GoogleGkeHubFeatureMembership#config_sync}
        :param hierarchy_controller: hierarchy_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#hierarchy_controller GoogleGkeHubFeatureMembership#hierarchy_controller}
        :param policy_controller: policy_controller block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#policy_controller GoogleGkeHubFeatureMembership#policy_controller}
        :param version: Optional. Version of ACM to install. Defaults to the latest version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#version GoogleGkeHubFeatureMembership#version}
        '''
        if isinstance(binauthz, dict):
            binauthz = GoogleGkeHubFeatureMembershipConfigmanagementBinauthz(**binauthz)
        if isinstance(config_sync, dict):
            config_sync = GoogleGkeHubFeatureMembershipConfigmanagementConfigSync(**config_sync)
        if isinstance(hierarchy_controller, dict):
            hierarchy_controller = GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController(**hierarchy_controller)
        if isinstance(policy_controller, dict):
            policy_controller = GoogleGkeHubFeatureMembershipConfigmanagementPolicyController(**policy_controller)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673cdaf2b6ede0f68164ef94e08c87a8859b1245ac5838d1574e6f62dd273404)
            check_type(argname="argument binauthz", value=binauthz, expected_type=type_hints["binauthz"])
            check_type(argname="argument config_sync", value=config_sync, expected_type=type_hints["config_sync"])
            check_type(argname="argument hierarchy_controller", value=hierarchy_controller, expected_type=type_hints["hierarchy_controller"])
            check_type(argname="argument policy_controller", value=policy_controller, expected_type=type_hints["policy_controller"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if binauthz is not None:
            self._values["binauthz"] = binauthz
        if config_sync is not None:
            self._values["config_sync"] = config_sync
        if hierarchy_controller is not None:
            self._values["hierarchy_controller"] = hierarchy_controller
        if policy_controller is not None:
            self._values["policy_controller"] = policy_controller
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def binauthz(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementBinauthz"]:
        '''binauthz block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#binauthz GoogleGkeHubFeatureMembership#binauthz}
        '''
        result = self._values.get("binauthz")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementBinauthz"], result)

    @builtins.property
    def config_sync(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementConfigSync"]:
        '''config_sync block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#config_sync GoogleGkeHubFeatureMembership#config_sync}
        '''
        result = self._values.get("config_sync")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementConfigSync"], result)

    @builtins.property
    def hierarchy_controller(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController"]:
        '''hierarchy_controller block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#hierarchy_controller GoogleGkeHubFeatureMembership#hierarchy_controller}
        '''
        result = self._values.get("hierarchy_controller")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController"], result)

    @builtins.property
    def policy_controller(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementPolicyController"]:
        '''policy_controller block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#policy_controller GoogleGkeHubFeatureMembership#policy_controller}
        '''
        result = self._values.get("policy_controller")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementPolicyController"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Optional. Version of ACM to install. Defaults to the latest version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#version GoogleGkeHubFeatureMembership#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementBinauthz",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GoogleGkeHubFeatureMembershipConfigmanagementBinauthz:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether binauthz is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04225f057deab844c0cb925b29cad3893f701acf41f98f3132d42c2afb3ef3a)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether binauthz is enabled in this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementBinauthz(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipConfigmanagementBinauthzOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementBinauthzOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ccaf84a28f547aa26e9ab25245859391b3a22e96a645ceffe71511cd995c2c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5e4c12084bc62c3dc923dc0158909a8b392638774937a49a714438d0209db909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b76c6c4faf5a0f9077c6b3fbdc82feef33b6cd96a01b492887650117f2bc726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSync",
    jsii_struct_bases=[],
    name_mapping={
        "git": "git",
        "oci": "oci",
        "prevent_drift": "preventDrift",
        "source_format": "sourceFormat",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagementConfigSync:
    def __init__(
        self,
        *,
        git: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit", typing.Dict[builtins.str, typing.Any]]] = None,
        oci: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci", typing.Dict[builtins.str, typing.Any]]] = None,
        prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#git GoogleGkeHubFeatureMembership#git}
        :param oci: oci block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#oci GoogleGkeHubFeatureMembership#oci}
        :param prevent_drift: Set to true to enable the Config Sync admission webhook to prevent drifts. If set to ``false``, disables the Config Sync admission webhook and does not prevent drifts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#prevent_drift GoogleGkeHubFeatureMembership#prevent_drift}
        :param source_format: Specifies whether the Config Sync Repo is in "hierarchical" or "unstructured" mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#source_format GoogleGkeHubFeatureMembership#source_format}
        '''
        if isinstance(git, dict):
            git = GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit(**git)
        if isinstance(oci, dict):
            oci = GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci(**oci)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b061211c1a2c8d4fad557434b81bcefd5bade26fbd8ea7552b2fea3b03ed06)
            check_type(argname="argument git", value=git, expected_type=type_hints["git"])
            check_type(argname="argument oci", value=oci, expected_type=type_hints["oci"])
            check_type(argname="argument prevent_drift", value=prevent_drift, expected_type=type_hints["prevent_drift"])
            check_type(argname="argument source_format", value=source_format, expected_type=type_hints["source_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if git is not None:
            self._values["git"] = git
        if oci is not None:
            self._values["oci"] = oci
        if prevent_drift is not None:
            self._values["prevent_drift"] = prevent_drift
        if source_format is not None:
            self._values["source_format"] = source_format

    @builtins.property
    def git(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit"]:
        '''git block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#git GoogleGkeHubFeatureMembership#git}
        '''
        result = self._values.get("git")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit"], result)

    @builtins.property
    def oci(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci"]:
        '''oci block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#oci GoogleGkeHubFeatureMembership#oci}
        '''
        result = self._values.get("oci")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci"], result)

    @builtins.property
    def prevent_drift(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true to enable the Config Sync admission webhook to prevent drifts.

        If set to ``false``, disables the Config Sync admission webhook and does not prevent drifts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#prevent_drift GoogleGkeHubFeatureMembership#prevent_drift}
        '''
        result = self._values.get("prevent_drift")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source_format(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the Config Sync Repo is in "hierarchical" or "unstructured" mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#source_format GoogleGkeHubFeatureMembership#source_format}
        '''
        result = self._values.get("source_format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementConfigSync(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit",
    jsii_struct_bases=[],
    name_mapping={
        "gcp_service_account_email": "gcpServiceAccountEmail",
        "https_proxy": "httpsProxy",
        "policy_dir": "policyDir",
        "secret_type": "secretType",
        "sync_branch": "syncBranch",
        "sync_repo": "syncRepo",
        "sync_rev": "syncRev",
        "sync_wait_secs": "syncWaitSecs",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit:
    def __init__(
        self,
        *,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        secret_type: typing.Optional[builtins.str] = None,
        sync_branch: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_rev: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gcp_service_account_email: The GCP Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#gcp_service_account_email GoogleGkeHubFeatureMembership#gcp_service_account_email}
        :param https_proxy: URL for the HTTPS proxy to be used when communicating with the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#https_proxy GoogleGkeHubFeatureMembership#https_proxy}
        :param policy_dir: The path within the Git repository that represents the top level of the repo to sync. Default: the root directory of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#policy_dir GoogleGkeHubFeatureMembership#policy_dir}
        :param secret_type: Type of secret configured for access to the Git repo. Must be one of ssh, cookiefile, gcenode, token, gcpserviceaccount or none. The validation of this is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#secret_type GoogleGkeHubFeatureMembership#secret_type}
        :param sync_branch: The branch of the repository to sync from. Default: master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_branch GoogleGkeHubFeatureMembership#sync_branch}
        :param sync_repo: The URL of the Git repository to use as the source of truth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_repo GoogleGkeHubFeatureMembership#sync_repo}
        :param sync_rev: Git revision (tag or hash) to check out. Default HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_rev GoogleGkeHubFeatureMembership#sync_rev}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_wait_secs GoogleGkeHubFeatureMembership#sync_wait_secs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522bb8107583a9bd504bbc0a88d70d193e145ce1e06bde67bb83c4e49c978ef0)
            check_type(argname="argument gcp_service_account_email", value=gcp_service_account_email, expected_type=type_hints["gcp_service_account_email"])
            check_type(argname="argument https_proxy", value=https_proxy, expected_type=type_hints["https_proxy"])
            check_type(argname="argument policy_dir", value=policy_dir, expected_type=type_hints["policy_dir"])
            check_type(argname="argument secret_type", value=secret_type, expected_type=type_hints["secret_type"])
            check_type(argname="argument sync_branch", value=sync_branch, expected_type=type_hints["sync_branch"])
            check_type(argname="argument sync_repo", value=sync_repo, expected_type=type_hints["sync_repo"])
            check_type(argname="argument sync_rev", value=sync_rev, expected_type=type_hints["sync_rev"])
            check_type(argname="argument sync_wait_secs", value=sync_wait_secs, expected_type=type_hints["sync_wait_secs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gcp_service_account_email is not None:
            self._values["gcp_service_account_email"] = gcp_service_account_email
        if https_proxy is not None:
            self._values["https_proxy"] = https_proxy
        if policy_dir is not None:
            self._values["policy_dir"] = policy_dir
        if secret_type is not None:
            self._values["secret_type"] = secret_type
        if sync_branch is not None:
            self._values["sync_branch"] = sync_branch
        if sync_repo is not None:
            self._values["sync_repo"] = sync_repo
        if sync_rev is not None:
            self._values["sync_rev"] = sync_rev
        if sync_wait_secs is not None:
            self._values["sync_wait_secs"] = sync_wait_secs

    @builtins.property
    def gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The GCP Service Account Email used for auth when secretType is gcpServiceAccount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#gcp_service_account_email GoogleGkeHubFeatureMembership#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_proxy(self) -> typing.Optional[builtins.str]:
        '''URL for the HTTPS proxy to be used when communicating with the Git repo.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#https_proxy GoogleGkeHubFeatureMembership#https_proxy}
        '''
        result = self._values.get("https_proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_dir(self) -> typing.Optional[builtins.str]:
        '''The path within the Git repository that represents the top level of the repo to sync.

        Default: the root directory of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#policy_dir GoogleGkeHubFeatureMembership#policy_dir}
        '''
        result = self._values.get("policy_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_type(self) -> typing.Optional[builtins.str]:
        '''Type of secret configured for access to the Git repo.

        Must be one of ssh, cookiefile, gcenode, token, gcpserviceaccount or none. The validation of this is case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#secret_type GoogleGkeHubFeatureMembership#secret_type}
        '''
        result = self._values.get("secret_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_branch(self) -> typing.Optional[builtins.str]:
        '''The branch of the repository to sync from. Default: master.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_branch GoogleGkeHubFeatureMembership#sync_branch}
        '''
        result = self._values.get("sync_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_repo(self) -> typing.Optional[builtins.str]:
        '''The URL of the Git repository to use as the source of truth.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_repo GoogleGkeHubFeatureMembership#sync_repo}
        '''
        result = self._values.get("sync_repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_rev(self) -> typing.Optional[builtins.str]:
        '''Git revision (tag or hash) to check out. Default HEAD.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_rev GoogleGkeHubFeatureMembership#sync_rev}
        '''
        result = self._values.get("sync_rev")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_wait_secs(self) -> typing.Optional[builtins.str]:
        '''Period in seconds between consecutive syncs. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_wait_secs GoogleGkeHubFeatureMembership#sync_wait_secs}
        '''
        result = self._values.get("sync_wait_secs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__87d2da75bf48b92eba5bc3158a896ab3aebe0b6716c430da291f45da5ca95500)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGcpServiceAccountEmail")
    def reset_gcp_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpServiceAccountEmail", []))

    @jsii.member(jsii_name="resetHttpsProxy")
    def reset_https_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsProxy", []))

    @jsii.member(jsii_name="resetPolicyDir")
    def reset_policy_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyDir", []))

    @jsii.member(jsii_name="resetSecretType")
    def reset_secret_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretType", []))

    @jsii.member(jsii_name="resetSyncBranch")
    def reset_sync_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncBranch", []))

    @jsii.member(jsii_name="resetSyncRepo")
    def reset_sync_repo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncRepo", []))

    @jsii.member(jsii_name="resetSyncRev")
    def reset_sync_rev(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncRev", []))

    @jsii.member(jsii_name="resetSyncWaitSecs")
    def reset_sync_wait_secs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncWaitSecs", []))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmailInput")
    def gcp_service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpServiceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsProxyInput")
    def https_proxy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpsProxyInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDirInput")
    def policy_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDirInput"))

    @builtins.property
    @jsii.member(jsii_name="secretTypeInput")
    def secret_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="syncBranchInput")
    def sync_branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncBranchInput"))

    @builtins.property
    @jsii.member(jsii_name="syncRepoInput")
    def sync_repo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncRepoInput"))

    @builtins.property
    @jsii.member(jsii_name="syncRevInput")
    def sync_rev_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncRevInput"))

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecsInput")
    def sync_wait_secs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncWaitSecsInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmail")
    def gcp_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccountEmail"))

    @gcp_service_account_email.setter
    def gcp_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbb743348fc43111f1567ac0610ac3d6dff9c7562083a1fc22943e5738383831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value)

    @builtins.property
    @jsii.member(jsii_name="httpsProxy")
    def https_proxy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpsProxy"))

    @https_proxy.setter
    def https_proxy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d9469d57214be7b6f662759aed696b58cdbb99d64a7cd04642f72aa8f7e48f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsProxy", value)

    @builtins.property
    @jsii.member(jsii_name="policyDir")
    def policy_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDir"))

    @policy_dir.setter
    def policy_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2963c67df0ee74ee7e84e5973f998ae53a4503f4f6739ec2d7a4f3ab327b561d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDir", value)

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f10700065e46b3ec1e8fb174b913a6a51decfb8075e09350db7020ce779d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value)

    @builtins.property
    @jsii.member(jsii_name="syncBranch")
    def sync_branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncBranch"))

    @sync_branch.setter
    def sync_branch(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26675f5523359c070f8fb775fb18716fd8fa2f3bb6f13578e7910464ff8cf46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncBranch", value)

    @builtins.property
    @jsii.member(jsii_name="syncRepo")
    def sync_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRepo"))

    @sync_repo.setter
    def sync_repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d85c9e8df10282a54068d6e9935b4ec4caa701f7d43f3515a6c31179ded0c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRepo", value)

    @builtins.property
    @jsii.member(jsii_name="syncRev")
    def sync_rev(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRev"))

    @sync_rev.setter
    def sync_rev(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd4b0761bbbc1158b733837e824c1e7a4570d2f0a7c1b6c60eb484a99b7ea593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRev", value)

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecs")
    def sync_wait_secs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncWaitSecs"))

    @sync_wait_secs.setter
    def sync_wait_secs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20512acf91ddba89927c8fc325bed1d5210bef80b857d393761002e3ec7b3478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncWaitSecs", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773106aa5a71f1fe66e70ded79460931dd2e73ccfdc2eb289cebe3a02344181e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci",
    jsii_struct_bases=[],
    name_mapping={
        "gcp_service_account_email": "gcpServiceAccountEmail",
        "policy_dir": "policyDir",
        "secret_type": "secretType",
        "sync_repo": "syncRepo",
        "sync_wait_secs": "syncWaitSecs",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci:
    def __init__(
        self,
        *,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        secret_type: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gcp_service_account_email: The GCP Service Account Email used for auth when secret_type is gcpserviceaccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#gcp_service_account_email GoogleGkeHubFeatureMembership#gcp_service_account_email}
        :param policy_dir: The absolute path of the directory that contains the local resources. Default: the root directory of the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#policy_dir GoogleGkeHubFeatureMembership#policy_dir}
        :param secret_type: Type of secret configured for access to the OCI Image. Must be one of gcenode, gcpserviceaccount or none. The validation of this is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#secret_type GoogleGkeHubFeatureMembership#secret_type}
        :param sync_repo: The OCI image repository URL for the package to sync from. e.g. LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME/PACKAGE_NAME. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_repo GoogleGkeHubFeatureMembership#sync_repo}
        :param sync_wait_secs: Period in seconds(int64 format) between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_wait_secs GoogleGkeHubFeatureMembership#sync_wait_secs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd4d5eb981ba65901bf2946568f738edde7b90817be9020c2d38418cd25d01f)
            check_type(argname="argument gcp_service_account_email", value=gcp_service_account_email, expected_type=type_hints["gcp_service_account_email"])
            check_type(argname="argument policy_dir", value=policy_dir, expected_type=type_hints["policy_dir"])
            check_type(argname="argument secret_type", value=secret_type, expected_type=type_hints["secret_type"])
            check_type(argname="argument sync_repo", value=sync_repo, expected_type=type_hints["sync_repo"])
            check_type(argname="argument sync_wait_secs", value=sync_wait_secs, expected_type=type_hints["sync_wait_secs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gcp_service_account_email is not None:
            self._values["gcp_service_account_email"] = gcp_service_account_email
        if policy_dir is not None:
            self._values["policy_dir"] = policy_dir
        if secret_type is not None:
            self._values["secret_type"] = secret_type
        if sync_repo is not None:
            self._values["sync_repo"] = sync_repo
        if sync_wait_secs is not None:
            self._values["sync_wait_secs"] = sync_wait_secs

    @builtins.property
    def gcp_service_account_email(self) -> typing.Optional[builtins.str]:
        '''The GCP Service Account Email used for auth when secret_type is gcpserviceaccount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#gcp_service_account_email GoogleGkeHubFeatureMembership#gcp_service_account_email}
        '''
        result = self._values.get("gcp_service_account_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_dir(self) -> typing.Optional[builtins.str]:
        '''The absolute path of the directory that contains the local resources. Default: the root directory of the image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#policy_dir GoogleGkeHubFeatureMembership#policy_dir}
        '''
        result = self._values.get("policy_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_type(self) -> typing.Optional[builtins.str]:
        '''Type of secret configured for access to the OCI Image.

        Must be one of gcenode, gcpserviceaccount or none. The validation of this is case-sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#secret_type GoogleGkeHubFeatureMembership#secret_type}
        '''
        result = self._values.get("secret_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_repo(self) -> typing.Optional[builtins.str]:
        '''The OCI image repository URL for the package to sync from. e.g. LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME/PACKAGE_NAME.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_repo GoogleGkeHubFeatureMembership#sync_repo}
        '''
        result = self._values.get("sync_repo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sync_wait_secs(self) -> typing.Optional[builtins.str]:
        '''Period in seconds(int64 format) between consecutive syncs. Default: 15.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_wait_secs GoogleGkeHubFeatureMembership#sync_wait_secs}
        '''
        result = self._values.get("sync_wait_secs")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb2849418628ccfb2315571f2ff3f65c91f264460f538a3471a4e3f4d3806b8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGcpServiceAccountEmail")
    def reset_gcp_service_account_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcpServiceAccountEmail", []))

    @jsii.member(jsii_name="resetPolicyDir")
    def reset_policy_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyDir", []))

    @jsii.member(jsii_name="resetSecretType")
    def reset_secret_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretType", []))

    @jsii.member(jsii_name="resetSyncRepo")
    def reset_sync_repo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncRepo", []))

    @jsii.member(jsii_name="resetSyncWaitSecs")
    def reset_sync_wait_secs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncWaitSecs", []))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmailInput")
    def gcp_service_account_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gcpServiceAccountEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="policyDirInput")
    def policy_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDirInput"))

    @builtins.property
    @jsii.member(jsii_name="secretTypeInput")
    def secret_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="syncRepoInput")
    def sync_repo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncRepoInput"))

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecsInput")
    def sync_wait_secs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "syncWaitSecsInput"))

    @builtins.property
    @jsii.member(jsii_name="gcpServiceAccountEmail")
    def gcp_service_account_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gcpServiceAccountEmail"))

    @gcp_service_account_email.setter
    def gcp_service_account_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d26efccc73bba21b697ee9259baf0a47590ce24598b91d24e26432f6e138d23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gcpServiceAccountEmail", value)

    @builtins.property
    @jsii.member(jsii_name="policyDir")
    def policy_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyDir"))

    @policy_dir.setter
    def policy_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b53a90aef8f2e04c657e158d6c39cef10c94fae202cd25f6d11646dcfa752d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDir", value)

    @builtins.property
    @jsii.member(jsii_name="secretType")
    def secret_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretType"))

    @secret_type.setter
    def secret_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7730f004cd7fc4ddaf529723d942e4e3f338e517b9c49b29508bf437703c845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretType", value)

    @builtins.property
    @jsii.member(jsii_name="syncRepo")
    def sync_repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncRepo"))

    @sync_repo.setter
    def sync_repo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75328af60c0d1afdb7dc6a3726b7d260638544163a94af3c192edf3608a921d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRepo", value)

    @builtins.property
    @jsii.member(jsii_name="syncWaitSecs")
    def sync_wait_secs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncWaitSecs"))

    @sync_wait_secs.setter
    def sync_wait_secs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfce158029b7637a2d734e6c6a3803f140be001093c1e21cde805cee0a0a26e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncWaitSecs", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca09f24f1ec363bb702596d30042fb19469408b7209e0e101c36a22c14e33ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__047282ccb356309cbe5ace85f01c64af12fb2abe45d58b180e6101e731aa4aca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGit")
    def put_git(
        self,
        *,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        https_proxy: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        secret_type: typing.Optional[builtins.str] = None,
        sync_branch: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_rev: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gcp_service_account_email: The GCP Service Account Email used for auth when secretType is gcpServiceAccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#gcp_service_account_email GoogleGkeHubFeatureMembership#gcp_service_account_email}
        :param https_proxy: URL for the HTTPS proxy to be used when communicating with the Git repo. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#https_proxy GoogleGkeHubFeatureMembership#https_proxy}
        :param policy_dir: The path within the Git repository that represents the top level of the repo to sync. Default: the root directory of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#policy_dir GoogleGkeHubFeatureMembership#policy_dir}
        :param secret_type: Type of secret configured for access to the Git repo. Must be one of ssh, cookiefile, gcenode, token, gcpserviceaccount or none. The validation of this is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#secret_type GoogleGkeHubFeatureMembership#secret_type}
        :param sync_branch: The branch of the repository to sync from. Default: master. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_branch GoogleGkeHubFeatureMembership#sync_branch}
        :param sync_repo: The URL of the Git repository to use as the source of truth. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_repo GoogleGkeHubFeatureMembership#sync_repo}
        :param sync_rev: Git revision (tag or hash) to check out. Default HEAD. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_rev GoogleGkeHubFeatureMembership#sync_rev}
        :param sync_wait_secs: Period in seconds between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_wait_secs GoogleGkeHubFeatureMembership#sync_wait_secs}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit(
            gcp_service_account_email=gcp_service_account_email,
            https_proxy=https_proxy,
            policy_dir=policy_dir,
            secret_type=secret_type,
            sync_branch=sync_branch,
            sync_repo=sync_repo,
            sync_rev=sync_rev,
            sync_wait_secs=sync_wait_secs,
        )

        return typing.cast(None, jsii.invoke(self, "putGit", [value]))

    @jsii.member(jsii_name="putOci")
    def put_oci(
        self,
        *,
        gcp_service_account_email: typing.Optional[builtins.str] = None,
        policy_dir: typing.Optional[builtins.str] = None,
        secret_type: typing.Optional[builtins.str] = None,
        sync_repo: typing.Optional[builtins.str] = None,
        sync_wait_secs: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param gcp_service_account_email: The GCP Service Account Email used for auth when secret_type is gcpserviceaccount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#gcp_service_account_email GoogleGkeHubFeatureMembership#gcp_service_account_email}
        :param policy_dir: The absolute path of the directory that contains the local resources. Default: the root directory of the image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#policy_dir GoogleGkeHubFeatureMembership#policy_dir}
        :param secret_type: Type of secret configured for access to the OCI Image. Must be one of gcenode, gcpserviceaccount or none. The validation of this is case-sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#secret_type GoogleGkeHubFeatureMembership#secret_type}
        :param sync_repo: The OCI image repository URL for the package to sync from. e.g. LOCATION-docker.pkg.dev/PROJECT_ID/REPOSITORY_NAME/PACKAGE_NAME. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_repo GoogleGkeHubFeatureMembership#sync_repo}
        :param sync_wait_secs: Period in seconds(int64 format) between consecutive syncs. Default: 15. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#sync_wait_secs GoogleGkeHubFeatureMembership#sync_wait_secs}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci(
            gcp_service_account_email=gcp_service_account_email,
            policy_dir=policy_dir,
            secret_type=secret_type,
            sync_repo=sync_repo,
            sync_wait_secs=sync_wait_secs,
        )

        return typing.cast(None, jsii.invoke(self, "putOci", [value]))

    @jsii.member(jsii_name="resetGit")
    def reset_git(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGit", []))

    @jsii.member(jsii_name="resetOci")
    def reset_oci(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOci", []))

    @jsii.member(jsii_name="resetPreventDrift")
    def reset_prevent_drift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreventDrift", []))

    @jsii.member(jsii_name="resetSourceFormat")
    def reset_source_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFormat", []))

    @builtins.property
    @jsii.member(jsii_name="git")
    def git(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference, jsii.get(self, "git"))

    @builtins.property
    @jsii.member(jsii_name="oci")
    def oci(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference, jsii.get(self, "oci"))

    @builtins.property
    @jsii.member(jsii_name="gitInput")
    def git_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit], jsii.get(self, "gitInput"))

    @builtins.property
    @jsii.member(jsii_name="ociInput")
    def oci_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci], jsii.get(self, "ociInput"))

    @builtins.property
    @jsii.member(jsii_name="preventDriftInput")
    def prevent_drift_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preventDriftInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFormatInput")
    def source_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="preventDrift")
    def prevent_drift(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preventDrift"))

    @prevent_drift.setter
    def prevent_drift(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6820a5620129cc3c93a53c4f2c95b355b437da49af19691c8c7a73ebd973a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preventDrift", value)

    @builtins.property
    @jsii.member(jsii_name="sourceFormat")
    def source_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFormat"))

    @source_format.setter
    def source_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4094b68a0609037532af69c466ae51b836b2075f358d9f79aaae1bdce2bf32b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFormat", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd25ad1da63bf090cd3f39600fd52aa32f34ba770e0cfd2925de4788e79444dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "enable_hierarchical_resource_quota": "enableHierarchicalResourceQuota",
        "enable_pod_tree_labels": "enablePodTreeLabels",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_hierarchical_resource_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_pod_tree_labels: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether Hierarchy Controller is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        :param enable_hierarchical_resource_quota: Whether hierarchical resource quota is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enable_hierarchical_resource_quota GoogleGkeHubFeatureMembership#enable_hierarchical_resource_quota}
        :param enable_pod_tree_labels: Whether pod tree labels are enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enable_pod_tree_labels GoogleGkeHubFeatureMembership#enable_pod_tree_labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa8cd921ea3bccd5713a7ce72e5d069f79f3e1ef2c002146d20f255cd94856b2)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_hierarchical_resource_quota", value=enable_hierarchical_resource_quota, expected_type=type_hints["enable_hierarchical_resource_quota"])
            check_type(argname="argument enable_pod_tree_labels", value=enable_pod_tree_labels, expected_type=type_hints["enable_pod_tree_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_hierarchical_resource_quota is not None:
            self._values["enable_hierarchical_resource_quota"] = enable_hierarchical_resource_quota
        if enable_pod_tree_labels is not None:
            self._values["enable_pod_tree_labels"] = enable_pod_tree_labels

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Hierarchy Controller is enabled in this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_hierarchical_resource_quota(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether hierarchical resource quota is enabled in this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enable_hierarchical_resource_quota GoogleGkeHubFeatureMembership#enable_hierarchical_resource_quota}
        '''
        result = self._values.get("enable_hierarchical_resource_quota")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_pod_tree_labels(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether pod tree labels are enabled in this cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enable_pod_tree_labels GoogleGkeHubFeatureMembership#enable_pod_tree_labels}
        '''
        result = self._values.get("enable_pod_tree_labels")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b95d561d2e336ffaff77ab4e4abcd5597bdb153ca78a17a7417abf9193e9c34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEnableHierarchicalResourceQuota")
    def reset_enable_hierarchical_resource_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableHierarchicalResourceQuota", []))

    @jsii.member(jsii_name="resetEnablePodTreeLabels")
    def reset_enable_pod_tree_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnablePodTreeLabels", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enableHierarchicalResourceQuotaInput")
    def enable_hierarchical_resource_quota_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableHierarchicalResourceQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePodTreeLabelsInput")
    def enable_pod_tree_labels_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePodTreeLabelsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2197ebc77aebabbccb3b8117d0e11c8d5ca89434746a96d6dfb4149aa52a22fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="enableHierarchicalResourceQuota")
    def enable_hierarchical_resource_quota(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableHierarchicalResourceQuota"))

    @enable_hierarchical_resource_quota.setter
    def enable_hierarchical_resource_quota(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c92b3cd9d85efc171ddd92e9f274aa042c8b5919bcb1fcb706263105896271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableHierarchicalResourceQuota", value)

    @builtins.property
    @jsii.member(jsii_name="enablePodTreeLabels")
    def enable_pod_tree_labels(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePodTreeLabels"))

    @enable_pod_tree_labels.setter
    def enable_pod_tree_labels(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db5495bf3427f1eb8f1b60c4064b199b2c1986767d547367c2318f836e47b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePodTreeLabels", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752b4e6199457f99c63eb48bfee9c7bd347d9c7cf04203c4e7dcb5ef3edf0d42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GoogleGkeHubFeatureMembershipConfigmanagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82b4f920a39c7b1c45a712235cbffd0082b5858b473f040eef0da90f1f32730f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBinauthz")
    def put_binauthz(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether binauthz is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementBinauthz(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putBinauthz", [value]))

    @jsii.member(jsii_name="putConfigSync")
    def put_config_sync(
        self,
        *,
        git: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit, typing.Dict[builtins.str, typing.Any]]] = None,
        oci: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci, typing.Dict[builtins.str, typing.Any]]] = None,
        prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source_format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param git: git block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#git GoogleGkeHubFeatureMembership#git}
        :param oci: oci block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#oci GoogleGkeHubFeatureMembership#oci}
        :param prevent_drift: Set to true to enable the Config Sync admission webhook to prevent drifts. If set to ``false``, disables the Config Sync admission webhook and does not prevent drifts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#prevent_drift GoogleGkeHubFeatureMembership#prevent_drift}
        :param source_format: Specifies whether the Config Sync Repo is in "hierarchical" or "unstructured" mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#source_format GoogleGkeHubFeatureMembership#source_format}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementConfigSync(
            git=git, oci=oci, prevent_drift=prevent_drift, source_format=source_format
        )

        return typing.cast(None, jsii.invoke(self, "putConfigSync", [value]))

    @jsii.member(jsii_name="putHierarchyController")
    def put_hierarchy_controller(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_hierarchical_resource_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_pod_tree_labels: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether Hierarchy Controller is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        :param enable_hierarchical_resource_quota: Whether hierarchical resource quota is enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enable_hierarchical_resource_quota GoogleGkeHubFeatureMembership#enable_hierarchical_resource_quota}
        :param enable_pod_tree_labels: Whether pod tree labels are enabled in this cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enable_pod_tree_labels GoogleGkeHubFeatureMembership#enable_pod_tree_labels}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController(
            enabled=enabled,
            enable_hierarchical_resource_quota=enable_hierarchical_resource_quota,
            enable_pod_tree_labels=enable_pod_tree_labels,
        )

        return typing.cast(None, jsii.invoke(self, "putHierarchyController", [value]))

    @jsii.member(jsii_name="putPolicyController")
    def put_policy_controller(
        self,
        *,
        audit_interval_seconds: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        template_library_installed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param audit_interval_seconds: Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#audit_interval_seconds GoogleGkeHubFeatureMembership#audit_interval_seconds}
        :param enabled: Enables the installation of Policy Controller. If false, the rest of PolicyController fields take no effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#exemptable_namespaces GoogleGkeHubFeatureMembership#exemptable_namespaces}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#log_denies_enabled GoogleGkeHubFeatureMembership#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#monitoring GoogleGkeHubFeatureMembership#monitoring}
        :param mutation_enabled: Enable or disable mutation in policy controller. If true, mutation CRDs, webhook and controller deployment will be deployed to the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#mutation_enabled GoogleGkeHubFeatureMembership#mutation_enabled}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#referential_rules_enabled GoogleGkeHubFeatureMembership#referential_rules_enabled}
        :param template_library_installed: Installs the default template library along with Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#template_library_installed GoogleGkeHubFeatureMembership#template_library_installed}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementPolicyController(
            audit_interval_seconds=audit_interval_seconds,
            enabled=enabled,
            exemptable_namespaces=exemptable_namespaces,
            log_denies_enabled=log_denies_enabled,
            monitoring=monitoring,
            mutation_enabled=mutation_enabled,
            referential_rules_enabled=referential_rules_enabled,
            template_library_installed=template_library_installed,
        )

        return typing.cast(None, jsii.invoke(self, "putPolicyController", [value]))

    @jsii.member(jsii_name="resetBinauthz")
    def reset_binauthz(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinauthz", []))

    @jsii.member(jsii_name="resetConfigSync")
    def reset_config_sync(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigSync", []))

    @jsii.member(jsii_name="resetHierarchyController")
    def reset_hierarchy_controller(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHierarchyController", []))

    @jsii.member(jsii_name="resetPolicyController")
    def reset_policy_controller(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyController", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="binauthz")
    def binauthz(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementBinauthzOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementBinauthzOutputReference, jsii.get(self, "binauthz"))

    @builtins.property
    @jsii.member(jsii_name="configSync")
    def config_sync(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference, jsii.get(self, "configSync"))

    @builtins.property
    @jsii.member(jsii_name="hierarchyController")
    def hierarchy_controller(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference, jsii.get(self, "hierarchyController"))

    @builtins.property
    @jsii.member(jsii_name="policyController")
    def policy_controller(
        self,
    ) -> "GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference":
        return typing.cast("GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference", jsii.get(self, "policyController"))

    @builtins.property
    @jsii.member(jsii_name="binauthzInput")
    def binauthz_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz], jsii.get(self, "binauthzInput"))

    @builtins.property
    @jsii.member(jsii_name="configSyncInput")
    def config_sync_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync], jsii.get(self, "configSyncInput"))

    @builtins.property
    @jsii.member(jsii_name="hierarchyControllerInput")
    def hierarchy_controller_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController], jsii.get(self, "hierarchyControllerInput"))

    @builtins.property
    @jsii.member(jsii_name="policyControllerInput")
    def policy_controller_input(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementPolicyController"]:
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementPolicyController"], jsii.get(self, "policyControllerInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3bb65c10d9a5d4a130a3fbf44656c5548601ed2e3192c184a5ab253ee3dd47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagement]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagement],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba0472bf1aab5e3e538c38efaa57adb346fe186ce6b354a3ad40d47f191762e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementPolicyController",
    jsii_struct_bases=[],
    name_mapping={
        "audit_interval_seconds": "auditIntervalSeconds",
        "enabled": "enabled",
        "exemptable_namespaces": "exemptableNamespaces",
        "log_denies_enabled": "logDeniesEnabled",
        "monitoring": "monitoring",
        "mutation_enabled": "mutationEnabled",
        "referential_rules_enabled": "referentialRulesEnabled",
        "template_library_installed": "templateLibraryInstalled",
    },
)
class GoogleGkeHubFeatureMembershipConfigmanagementPolicyController:
    def __init__(
        self,
        *,
        audit_interval_seconds: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
        log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monitoring: typing.Optional[typing.Union["GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring", typing.Dict[builtins.str, typing.Any]]] = None,
        mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        template_library_installed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param audit_interval_seconds: Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#audit_interval_seconds GoogleGkeHubFeatureMembership#audit_interval_seconds}
        :param enabled: Enables the installation of Policy Controller. If false, the rest of PolicyController fields take no effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        :param exemptable_namespaces: The set of namespaces that are excluded from Policy Controller checks. Namespaces do not need to currently exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#exemptable_namespaces GoogleGkeHubFeatureMembership#exemptable_namespaces}
        :param log_denies_enabled: Logs all denies and dry run failures. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#log_denies_enabled GoogleGkeHubFeatureMembership#log_denies_enabled}
        :param monitoring: monitoring block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#monitoring GoogleGkeHubFeatureMembership#monitoring}
        :param mutation_enabled: Enable or disable mutation in policy controller. If true, mutation CRDs, webhook and controller deployment will be deployed to the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#mutation_enabled GoogleGkeHubFeatureMembership#mutation_enabled}
        :param referential_rules_enabled: Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#referential_rules_enabled GoogleGkeHubFeatureMembership#referential_rules_enabled}
        :param template_library_installed: Installs the default template library along with Policy Controller. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#template_library_installed GoogleGkeHubFeatureMembership#template_library_installed}
        '''
        if isinstance(monitoring, dict):
            monitoring = GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring(**monitoring)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e638940c8c715fbc156b9b6355555ffdf29a8dbafe84a8590b4b2147cf3f148)
            check_type(argname="argument audit_interval_seconds", value=audit_interval_seconds, expected_type=type_hints["audit_interval_seconds"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument exemptable_namespaces", value=exemptable_namespaces, expected_type=type_hints["exemptable_namespaces"])
            check_type(argname="argument log_denies_enabled", value=log_denies_enabled, expected_type=type_hints["log_denies_enabled"])
            check_type(argname="argument monitoring", value=monitoring, expected_type=type_hints["monitoring"])
            check_type(argname="argument mutation_enabled", value=mutation_enabled, expected_type=type_hints["mutation_enabled"])
            check_type(argname="argument referential_rules_enabled", value=referential_rules_enabled, expected_type=type_hints["referential_rules_enabled"])
            check_type(argname="argument template_library_installed", value=template_library_installed, expected_type=type_hints["template_library_installed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audit_interval_seconds is not None:
            self._values["audit_interval_seconds"] = audit_interval_seconds
        if enabled is not None:
            self._values["enabled"] = enabled
        if exemptable_namespaces is not None:
            self._values["exemptable_namespaces"] = exemptable_namespaces
        if log_denies_enabled is not None:
            self._values["log_denies_enabled"] = log_denies_enabled
        if monitoring is not None:
            self._values["monitoring"] = monitoring
        if mutation_enabled is not None:
            self._values["mutation_enabled"] = mutation_enabled
        if referential_rules_enabled is not None:
            self._values["referential_rules_enabled"] = referential_rules_enabled
        if template_library_installed is not None:
            self._values["template_library_installed"] = template_library_installed

    @builtins.property
    def audit_interval_seconds(self) -> typing.Optional[builtins.str]:
        '''Sets the interval for Policy Controller Audit Scans (in seconds). When set to 0, this disables audit functionality altogether.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#audit_interval_seconds GoogleGkeHubFeatureMembership#audit_interval_seconds}
        '''
        result = self._values.get("audit_interval_seconds")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the installation of Policy Controller. If false, the rest of PolicyController fields take no effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#enabled GoogleGkeHubFeatureMembership#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exemptable_namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The set of namespaces that are excluded from Policy Controller checks.

        Namespaces do not need to currently exist on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#exemptable_namespaces GoogleGkeHubFeatureMembership#exemptable_namespaces}
        '''
        result = self._values.get("exemptable_namespaces")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def log_denies_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Logs all denies and dry run failures.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#log_denies_enabled GoogleGkeHubFeatureMembership#log_denies_enabled}
        '''
        result = self._values.get("log_denies_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monitoring(
        self,
    ) -> typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring"]:
        '''monitoring block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#monitoring GoogleGkeHubFeatureMembership#monitoring}
        '''
        result = self._values.get("monitoring")
        return typing.cast(typing.Optional["GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring"], result)

    @builtins.property
    def mutation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable or disable mutation in policy controller.

        If true, mutation CRDs, webhook and controller deployment will be deployed to the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#mutation_enabled GoogleGkeHubFeatureMembership#mutation_enabled}
        '''
        result = self._values.get("mutation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def referential_rules_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables the ability to use Constraint Templates that reference to objects other than the object currently being evaluated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#referential_rules_enabled GoogleGkeHubFeatureMembership#referential_rules_enabled}
        '''
        result = self._values.get("referential_rules_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def template_library_installed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Installs the default template library along with Policy Controller.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#template_library_installed GoogleGkeHubFeatureMembership#template_library_installed}
        '''
        result = self._values.get("template_library_installed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementPolicyController(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring",
    jsii_struct_bases=[],
    name_mapping={"backends": "backends"},
)
class GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring:
    def __init__(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#backends GoogleGkeHubFeatureMembership#backends}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c46b4eed8b3413d8a103dc814d01a3a1e8910f46d714d75809d0ca0523497962)
            check_type(argname="argument backends", value=backends, expected_type=type_hints["backends"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backends is not None:
            self._values["backends"] = backends

    @builtins.property
    def backends(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#backends GoogleGkeHubFeatureMembership#backends}
        '''
        result = self._values.get("backends")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2828c9499ab339bd608500255c84bcfd7fd04f31afaddbdbe646da4aa14e5046)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackends")
    def reset_backends(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackends", []))

    @builtins.property
    @jsii.member(jsii_name="backendsInput")
    def backends_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "backendsInput"))

    @builtins.property
    @jsii.member(jsii_name="backends")
    def backends(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "backends"))

    @backends.setter
    def backends(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08114d8c1874c0b70da8028a3219f781ab9475f10d7e8de9227925615bd09f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backends", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56aae9e90a6d26a7fd64323d3d1ea5dac4645f6b63fd85eaf34c9ca2572625fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d01a6308da6a2ea089b19c438f90175ae8e7723c5eb3c027bedb9de60b7c2d1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMonitoring")
    def put_monitoring(
        self,
        *,
        backends: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param backends: Specifies the list of backends Policy Controller will export to. Specifying an empty value ``[]`` disables metrics export. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#backends GoogleGkeHubFeatureMembership#backends}
        '''
        value = GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring(
            backends=backends
        )

        return typing.cast(None, jsii.invoke(self, "putMonitoring", [value]))

    @jsii.member(jsii_name="resetAuditIntervalSeconds")
    def reset_audit_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuditIntervalSeconds", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetExemptableNamespaces")
    def reset_exemptable_namespaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExemptableNamespaces", []))

    @jsii.member(jsii_name="resetLogDeniesEnabled")
    def reset_log_denies_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogDeniesEnabled", []))

    @jsii.member(jsii_name="resetMonitoring")
    def reset_monitoring(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitoring", []))

    @jsii.member(jsii_name="resetMutationEnabled")
    def reset_mutation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMutationEnabled", []))

    @jsii.member(jsii_name="resetReferentialRulesEnabled")
    def reset_referential_rules_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferentialRulesEnabled", []))

    @jsii.member(jsii_name="resetTemplateLibraryInstalled")
    def reset_template_library_installed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateLibraryInstalled", []))

    @builtins.property
    @jsii.member(jsii_name="monitoring")
    def monitoring(
        self,
    ) -> GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference:
        return typing.cast(GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference, jsii.get(self, "monitoring"))

    @builtins.property
    @jsii.member(jsii_name="auditIntervalSecondsInput")
    def audit_interval_seconds_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "auditIntervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="exemptableNamespacesInput")
    def exemptable_namespaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exemptableNamespacesInput"))

    @builtins.property
    @jsii.member(jsii_name="logDeniesEnabledInput")
    def log_denies_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logDeniesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="monitoringInput")
    def monitoring_input(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring], jsii.get(self, "monitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="mutationEnabledInput")
    def mutation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mutationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="referentialRulesEnabledInput")
    def referential_rules_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "referentialRulesEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="templateLibraryInstalledInput")
    def template_library_installed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "templateLibraryInstalledInput"))

    @builtins.property
    @jsii.member(jsii_name="auditIntervalSeconds")
    def audit_interval_seconds(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "auditIntervalSeconds"))

    @audit_interval_seconds.setter
    def audit_interval_seconds(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f6bd92abe8eda74a1dc751933ccc9f78e8709b1f4e4280dca9f6d1f33712181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditIntervalSeconds", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__07510763f8e532dc8cd31e94f893b0d360a679d33a1a80d195a7dbd6384181e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="exemptableNamespaces")
    def exemptable_namespaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exemptableNamespaces"))

    @exemptable_namespaces.setter
    def exemptable_namespaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb109ff29bbfd1e2769227f6f49ff3799f8e4b6b6fe60602c98096cbacdf1d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exemptableNamespaces", value)

    @builtins.property
    @jsii.member(jsii_name="logDeniesEnabled")
    def log_denies_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logDeniesEnabled"))

    @log_denies_enabled.setter
    def log_denies_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf4e7fef3f5b42771685f38994fc5b6b15f94ef04791fb108714f466ea1e454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logDeniesEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="mutationEnabled")
    def mutation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mutationEnabled"))

    @mutation_enabled.setter
    def mutation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__969da8e1b8fe0675c96fb33e5b7b1ebc7b4f232aa2dc6c37060c2779fac5cd67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mutationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="referentialRulesEnabled")
    def referential_rules_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "referentialRulesEnabled"))

    @referential_rules_enabled.setter
    def referential_rules_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43448b9f005e2e7d89e24f3359225cd8c2ada459f7a6525b1daf8fc31bb3d341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referentialRulesEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="templateLibraryInstalled")
    def template_library_installed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "templateLibraryInstalled"))

    @template_library_installed.setter
    def template_library_installed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e39b1e0b78621b7cc569d326f553aa1e47d9e8a7d1fbf024c24e100b04f57c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateLibraryInstalled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyController]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyController], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyController],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2481b1b520b71b8e2947e25b676f3a045438237afb75341ccf06fc510c022778)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipMesh",
    jsii_struct_bases=[],
    name_mapping={"control_plane": "controlPlane", "management": "management"},
)
class GoogleGkeHubFeatureMembershipMesh:
    def __init__(
        self,
        *,
        control_plane: typing.Optional[builtins.str] = None,
        management: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param control_plane: **DEPRECATED** Whether to automatically manage Service Mesh control planes. Possible values: CONTROL_PLANE_MANAGEMENT_UNSPECIFIED, AUTOMATIC, MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#control_plane GoogleGkeHubFeatureMembership#control_plane}
        :param management: Whether to automatically manage Service Mesh. Possible values: MANAGEMENT_UNSPECIFIED, MANAGEMENT_AUTOMATIC, MANAGEMENT_MANUAL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#management GoogleGkeHubFeatureMembership#management}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35e02410be6366371ef684ffe9ad2f718f113946d1bc8b099a10b00600d23a1f)
            check_type(argname="argument control_plane", value=control_plane, expected_type=type_hints["control_plane"])
            check_type(argname="argument management", value=management, expected_type=type_hints["management"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if control_plane is not None:
            self._values["control_plane"] = control_plane
        if management is not None:
            self._values["management"] = management

    @builtins.property
    def control_plane(self) -> typing.Optional[builtins.str]:
        '''**DEPRECATED** Whether to automatically manage Service Mesh control planes. Possible values: CONTROL_PLANE_MANAGEMENT_UNSPECIFIED, AUTOMATIC, MANUAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#control_plane GoogleGkeHubFeatureMembership#control_plane}
        '''
        result = self._values.get("control_plane")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def management(self) -> typing.Optional[builtins.str]:
        '''Whether to automatically manage Service Mesh. Possible values: MANAGEMENT_UNSPECIFIED, MANAGEMENT_AUTOMATIC, MANAGEMENT_MANUAL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#management GoogleGkeHubFeatureMembership#management}
        '''
        result = self._values.get("management")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipMesh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipMeshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipMeshOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8eb914b84ea122ed7e2712b07b2d9c9dc3377791756040d6200068806301255a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetControlPlane")
    def reset_control_plane(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControlPlane", []))

    @jsii.member(jsii_name="resetManagement")
    def reset_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagement", []))

    @builtins.property
    @jsii.member(jsii_name="controlPlaneInput")
    def control_plane_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controlPlaneInput"))

    @builtins.property
    @jsii.member(jsii_name="managementInput")
    def management_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managementInput"))

    @builtins.property
    @jsii.member(jsii_name="controlPlane")
    def control_plane(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controlPlane"))

    @control_plane.setter
    def control_plane(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31b4aa8e522d7506c6d54156d51c99d9ae3748fbd75621af8ac842067742c71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controlPlane", value)

    @builtins.property
    @jsii.member(jsii_name="management")
    def management(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "management"))

    @management.setter
    def management(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b460959e6130a0c71d2f8528cb9c26edf5ce367d138d479c25b81755396e4188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "management", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleGkeHubFeatureMembershipMesh]:
        return typing.cast(typing.Optional[GoogleGkeHubFeatureMembershipMesh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleGkeHubFeatureMembershipMesh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c6346e3d79f710d4f7a24211fe3f852ca4f2bee64a5ddec97aa54abd564be0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleGkeHubFeatureMembershipTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#create GoogleGkeHubFeatureMembership#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#delete GoogleGkeHubFeatureMembership#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#update GoogleGkeHubFeatureMembership#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a5bb553abd7a22c1eef52885c45e32a464c3d13a2cb9ba05c35244e50d82ec)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#create GoogleGkeHubFeatureMembership#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#delete GoogleGkeHubFeatureMembership#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_gke_hub_feature_membership#update GoogleGkeHubFeatureMembership#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleGkeHubFeatureMembershipTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleGkeHubFeatureMembershipTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleGkeHubFeatureMembership.GoogleGkeHubFeatureMembershipTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6273023536f4923ee7de0139f5a5d0a048595de0f1fc0c33bdc0358d195a6d09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e53abf0c160bc0d17541f80358f0e22eb774c20d3233f32a9a9292b64601753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c1edb8d698cb137a7065b80e72ac3c9e83d23fa0f17931b0409683e6426131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d939169d09167475d5a307fac867b82315cd395870ce355147b21116e755a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848039da9a6a00355ba120a472de2b78fe7cc7bea4c93809f6064fe0eedbaed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GoogleGkeHubFeatureMembership",
    "GoogleGkeHubFeatureMembershipConfig",
    "GoogleGkeHubFeatureMembershipConfigmanagement",
    "GoogleGkeHubFeatureMembershipConfigmanagementBinauthz",
    "GoogleGkeHubFeatureMembershipConfigmanagementBinauthzOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSync",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGitOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOciOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController",
    "GoogleGkeHubFeatureMembershipConfigmanagementHierarchyControllerOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementPolicyController",
    "GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring",
    "GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoringOutputReference",
    "GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerOutputReference",
    "GoogleGkeHubFeatureMembershipMesh",
    "GoogleGkeHubFeatureMembershipMeshOutputReference",
    "GoogleGkeHubFeatureMembershipTimeouts",
    "GoogleGkeHubFeatureMembershipTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bb0b329ce2d05634c944e2255fda1d2c15cbf151adf11be93d9c4d1405e05220(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    feature: builtins.str,
    location: builtins.str,
    membership: builtins.str,
    configmanagement: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagement, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    mesh: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipMesh, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__62872bdfceafad454f1f77b15f0c4cc026f50a42b15c1ba4ae1e073493d445cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0958d3b43f6eeee77da3758cde573467dcc5caf896edce568f597a324e95a596(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026490971551372bb2b4367c899e7d13d507691fcd381768b3818da3e4687d8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b83bed14422792af7953f5b45e04cf6f355b207c43f6d8e8c84d5f3625b5217(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf9355e466a5d9bc98e79e3e26b9069d4848147b9de0e5c7e2116507a9f86f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc454f576b0fc2b00803677a901ef7a86701247db18f878efe02b250d0b540e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    feature: builtins.str,
    location: builtins.str,
    membership: builtins.str,
    configmanagement: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagement, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    mesh: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipMesh, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673cdaf2b6ede0f68164ef94e08c87a8859b1245ac5838d1574e6f62dd273404(
    *,
    binauthz: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz, typing.Dict[builtins.str, typing.Any]]] = None,
    config_sync: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync, typing.Dict[builtins.str, typing.Any]]] = None,
    hierarchy_controller: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController, typing.Dict[builtins.str, typing.Any]]] = None,
    policy_controller: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementPolicyController, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04225f057deab844c0cb925b29cad3893f701acf41f98f3132d42c2afb3ef3a(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ccaf84a28f547aa26e9ab25245859391b3a22e96a645ceffe71511cd995c2c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4c12084bc62c3dc923dc0158909a8b392638774937a49a714438d0209db909(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b76c6c4faf5a0f9077c6b3fbdc82feef33b6cd96a01b492887650117f2bc726(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementBinauthz],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b061211c1a2c8d4fad557434b81bcefd5bade26fbd8ea7552b2fea3b03ed06(
    *,
    git: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit, typing.Dict[builtins.str, typing.Any]]] = None,
    oci: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci, typing.Dict[builtins.str, typing.Any]]] = None,
    prevent_drift: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522bb8107583a9bd504bbc0a88d70d193e145ce1e06bde67bb83c4e49c978ef0(
    *,
    gcp_service_account_email: typing.Optional[builtins.str] = None,
    https_proxy: typing.Optional[builtins.str] = None,
    policy_dir: typing.Optional[builtins.str] = None,
    secret_type: typing.Optional[builtins.str] = None,
    sync_branch: typing.Optional[builtins.str] = None,
    sync_repo: typing.Optional[builtins.str] = None,
    sync_rev: typing.Optional[builtins.str] = None,
    sync_wait_secs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d2da75bf48b92eba5bc3158a896ab3aebe0b6716c430da291f45da5ca95500(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb743348fc43111f1567ac0610ac3d6dff9c7562083a1fc22943e5738383831(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d9469d57214be7b6f662759aed696b58cdbb99d64a7cd04642f72aa8f7e48f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2963c67df0ee74ee7e84e5973f998ae53a4503f4f6739ec2d7a4f3ab327b561d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f10700065e46b3ec1e8fb174b913a6a51decfb8075e09350db7020ce779d4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26675f5523359c070f8fb775fb18716fd8fa2f3bb6f13578e7910464ff8cf46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d85c9e8df10282a54068d6e9935b4ec4caa701f7d43f3515a6c31179ded0c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd4b0761bbbc1158b733837e824c1e7a4570d2f0a7c1b6c60eb484a99b7ea593(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20512acf91ddba89927c8fc325bed1d5210bef80b857d393761002e3ec7b3478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773106aa5a71f1fe66e70ded79460931dd2e73ccfdc2eb289cebe3a02344181e(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncGit],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd4d5eb981ba65901bf2946568f738edde7b90817be9020c2d38418cd25d01f(
    *,
    gcp_service_account_email: typing.Optional[builtins.str] = None,
    policy_dir: typing.Optional[builtins.str] = None,
    secret_type: typing.Optional[builtins.str] = None,
    sync_repo: typing.Optional[builtins.str] = None,
    sync_wait_secs: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2849418628ccfb2315571f2ff3f65c91f264460f538a3471a4e3f4d3806b8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d26efccc73bba21b697ee9259baf0a47590ce24598b91d24e26432f6e138d23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b53a90aef8f2e04c657e158d6c39cef10c94fae202cd25f6d11646dcfa752d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7730f004cd7fc4ddaf529723d942e4e3f338e517b9c49b29508bf437703c845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75328af60c0d1afdb7dc6a3726b7d260638544163a94af3c192edf3608a921d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfce158029b7637a2d734e6c6a3803f140be001093c1e21cde805cee0a0a26e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca09f24f1ec363bb702596d30042fb19469408b7209e0e101c36a22c14e33ff5(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSyncOci],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047282ccb356309cbe5ace85f01c64af12fb2abe45d58b180e6101e731aa4aca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6820a5620129cc3c93a53c4f2c95b355b437da49af19691c8c7a73ebd973a6d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4094b68a0609037532af69c466ae51b836b2075f358d9f79aaae1bdce2bf32b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd25ad1da63bf090cd3f39600fd52aa32f34ba770e0cfd2925de4788e79444dd(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementConfigSync],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8cd921ea3bccd5713a7ce72e5d069f79f3e1ef2c002146d20f255cd94856b2(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_hierarchical_resource_quota: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_pod_tree_labels: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b95d561d2e336ffaff77ab4e4abcd5597bdb153ca78a17a7417abf9193e9c34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2197ebc77aebabbccb3b8117d0e11c8d5ca89434746a96d6dfb4149aa52a22fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c92b3cd9d85efc171ddd92e9f274aa042c8b5919bcb1fcb706263105896271(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db5495bf3427f1eb8f1b60c4064b199b2c1986767d547367c2318f836e47b5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752b4e6199457f99c63eb48bfee9c7bd347d9c7cf04203c4e7dcb5ef3edf0d42(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementHierarchyController],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b4f920a39c7b1c45a712235cbffd0082b5858b473f040eef0da90f1f32730f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3bb65c10d9a5d4a130a3fbf44656c5548601ed2e3192c184a5ab253ee3dd47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0472bf1aab5e3e538c38efaa57adb346fe186ce6b354a3ad40d47f191762e9(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e638940c8c715fbc156b9b6355555ffdf29a8dbafe84a8590b4b2147cf3f148(
    *,
    audit_interval_seconds: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exemptable_namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    log_denies_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monitoring: typing.Optional[typing.Union[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring, typing.Dict[builtins.str, typing.Any]]] = None,
    mutation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    referential_rules_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    template_library_installed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46b4eed8b3413d8a103dc814d01a3a1e8910f46d714d75809d0ca0523497962(
    *,
    backends: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2828c9499ab339bd608500255c84bcfd7fd04f31afaddbdbe646da4aa14e5046(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08114d8c1874c0b70da8028a3219f781ab9475f10d7e8de9227925615bd09f75(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56aae9e90a6d26a7fd64323d3d1ea5dac4645f6b63fd85eaf34c9ca2572625fa(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyControllerMonitoring],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01a6308da6a2ea089b19c438f90175ae8e7723c5eb3c027bedb9de60b7c2d1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6bd92abe8eda74a1dc751933ccc9f78e8709b1f4e4280dca9f6d1f33712181(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07510763f8e532dc8cd31e94f893b0d360a679d33a1a80d195a7dbd6384181e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb109ff29bbfd1e2769227f6f49ff3799f8e4b6b6fe60602c98096cbacdf1d88(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf4e7fef3f5b42771685f38994fc5b6b15f94ef04791fb108714f466ea1e454(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969da8e1b8fe0675c96fb33e5b7b1ebc7b4f232aa2dc6c37060c2779fac5cd67(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43448b9f005e2e7d89e24f3359225cd8c2ada459f7a6525b1daf8fc31bb3d341(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e39b1e0b78621b7cc569d326f553aa1e47d9e8a7d1fbf024c24e100b04f57c8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2481b1b520b71b8e2947e25b676f3a045438237afb75341ccf06fc510c022778(
    value: typing.Optional[GoogleGkeHubFeatureMembershipConfigmanagementPolicyController],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35e02410be6366371ef684ffe9ad2f718f113946d1bc8b099a10b00600d23a1f(
    *,
    control_plane: typing.Optional[builtins.str] = None,
    management: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb914b84ea122ed7e2712b07b2d9c9dc3377791756040d6200068806301255a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31b4aa8e522d7506c6d54156d51c99d9ae3748fbd75621af8ac842067742c71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b460959e6130a0c71d2f8528cb9c26edf5ce367d138d479c25b81755396e4188(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c6346e3d79f710d4f7a24211fe3f852ca4f2bee64a5ddec97aa54abd564be0(
    value: typing.Optional[GoogleGkeHubFeatureMembershipMesh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a5bb553abd7a22c1eef52885c45e32a464c3d13a2cb9ba05c35244e50d82ec(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6273023536f4923ee7de0139f5a5d0a048595de0f1fc0c33bdc0358d195a6d09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e53abf0c160bc0d17541f80358f0e22eb774c20d3233f32a9a9292b64601753(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c1edb8d698cb137a7065b80e72ac3c9e83d23fa0f17931b0409683e6426131(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d939169d09167475d5a307fac867b82315cd395870ce355147b21116e755a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848039da9a6a00355ba120a472de2b78fe7cc7bea4c93809f6064fe0eedbaed4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleGkeHubFeatureMembershipTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
