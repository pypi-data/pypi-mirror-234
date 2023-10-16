'''
# `google_bigquery_analytics_hub_listing`

Refer to the Terraform Registory for docs: [`google_bigquery_analytics_hub_listing`](https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing).
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


class GoogleBigqueryAnalyticsHubListing(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListing",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing google_bigquery_analytics_hub_listing}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bigquery_dataset: typing.Union["GoogleBigqueryAnalyticsHubListingBigqueryDataset", typing.Dict[builtins.str, typing.Any]],
        data_exchange_id: builtins.str,
        display_name: builtins.str,
        listing_id: builtins.str,
        location: builtins.str,
        categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        data_provider: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingDataProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[builtins.str] = None,
        icon: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        primary_contact: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingPublisher", typing.Dict[builtins.str, typing.Any]]] = None,
        request_access: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing google_bigquery_analytics_hub_listing} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bigquery_dataset: bigquery_dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#bigquery_dataset GoogleBigqueryAnalyticsHubListing#bigquery_dataset}
        :param data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#data_exchange_id GoogleBigqueryAnalyticsHubListing#data_exchange_id}
        :param display_name: Human-readable display name of the listing. The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#display_name GoogleBigqueryAnalyticsHubListing#display_name}
        :param listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#listing_id GoogleBigqueryAnalyticsHubListing#listing_id}
        :param location: The name of the location this data exchange listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#location GoogleBigqueryAnalyticsHubListing#location}
        :param categories: Categories of the listing. Up to two categories are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#categories GoogleBigqueryAnalyticsHubListing#categories}
        :param data_provider: data_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#data_provider GoogleBigqueryAnalyticsHubListing#data_provider}
        :param description: Short description of the listing. The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#description GoogleBigqueryAnalyticsHubListing#description}
        :param documentation: Documentation describing the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#documentation GoogleBigqueryAnalyticsHubListing#documentation}
        :param icon: Base64 encoded image representing the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#icon GoogleBigqueryAnalyticsHubListing#icon}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#id GoogleBigqueryAnalyticsHubListing#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param primary_contact: Email or URL of the primary point of contact of the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#project GoogleBigqueryAnalyticsHubListing#project}.
        :param publisher: publisher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#publisher GoogleBigqueryAnalyticsHubListing#publisher}
        :param request_access: Email or URL of the request access of the listing. Subscribers can use this reference to request access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#request_access GoogleBigqueryAnalyticsHubListing#request_access}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#timeouts GoogleBigqueryAnalyticsHubListing#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f1f2677cbe3d7372e4162c32a922d59f80ad350f54b4f5717154c71af05ad8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleBigqueryAnalyticsHubListingConfig(
            bigquery_dataset=bigquery_dataset,
            data_exchange_id=data_exchange_id,
            display_name=display_name,
            listing_id=listing_id,
            location=location,
            categories=categories,
            data_provider=data_provider,
            description=description,
            documentation=documentation,
            icon=icon,
            id=id,
            primary_contact=primary_contact,
            project=project,
            publisher=publisher,
            request_access=request_access,
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

    @jsii.member(jsii_name="putBigqueryDataset")
    def put_bigquery_dataset(self, *, dataset: builtins.str) -> None:
        '''
        :param dataset: Resource name of the dataset source for this listing. e.g. projects/myproject/datasets/123. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#dataset GoogleBigqueryAnalyticsHubListing#dataset}
        '''
        value = GoogleBigqueryAnalyticsHubListingBigqueryDataset(dataset=dataset)

        return typing.cast(None, jsii.invoke(self, "putBigqueryDataset", [value]))

    @jsii.member(jsii_name="putDataProvider")
    def put_data_provider(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the data provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#name GoogleBigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the data provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        value = GoogleBigqueryAnalyticsHubListingDataProvider(
            name=name, primary_contact=primary_contact
        )

        return typing.cast(None, jsii.invoke(self, "putDataProvider", [value]))

    @jsii.member(jsii_name="putPublisher")
    def put_publisher(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the listing publisher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#name GoogleBigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the listing publisher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        value = GoogleBigqueryAnalyticsHubListingPublisher(
            name=name, primary_contact=primary_contact
        )

        return typing.cast(None, jsii.invoke(self, "putPublisher", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#create GoogleBigqueryAnalyticsHubListing#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#delete GoogleBigqueryAnalyticsHubListing#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#update GoogleBigqueryAnalyticsHubListing#update}.
        '''
        value = GoogleBigqueryAnalyticsHubListingTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCategories")
    def reset_categories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategories", []))

    @jsii.member(jsii_name="resetDataProvider")
    def reset_data_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProvider", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDocumentation")
    def reset_documentation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocumentation", []))

    @jsii.member(jsii_name="resetIcon")
    def reset_icon(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcon", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPrimaryContact")
    def reset_primary_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContact", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPublisher")
    def reset_publisher(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublisher", []))

    @jsii.member(jsii_name="resetRequestAccess")
    def reset_request_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestAccess", []))

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
    @jsii.member(jsii_name="bigqueryDataset")
    def bigquery_dataset(
        self,
    ) -> "GoogleBigqueryAnalyticsHubListingBigqueryDatasetOutputReference":
        return typing.cast("GoogleBigqueryAnalyticsHubListingBigqueryDatasetOutputReference", jsii.get(self, "bigqueryDataset"))

    @builtins.property
    @jsii.member(jsii_name="dataProvider")
    def data_provider(
        self,
    ) -> "GoogleBigqueryAnalyticsHubListingDataProviderOutputReference":
        return typing.cast("GoogleBigqueryAnalyticsHubListingDataProviderOutputReference", jsii.get(self, "dataProvider"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> "GoogleBigqueryAnalyticsHubListingPublisherOutputReference":
        return typing.cast("GoogleBigqueryAnalyticsHubListingPublisherOutputReference", jsii.get(self, "publisher"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleBigqueryAnalyticsHubListingTimeoutsOutputReference":
        return typing.cast("GoogleBigqueryAnalyticsHubListingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDatasetInput")
    def bigquery_dataset_input(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubListingBigqueryDataset"]:
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingBigqueryDataset"], jsii.get(self, "bigqueryDatasetInput"))

    @builtins.property
    @jsii.member(jsii_name="categoriesInput")
    def categories_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "categoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataExchangeIdInput")
    def data_exchange_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataExchangeIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataProviderInput")
    def data_provider_input(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubListingDataProvider"]:
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingDataProvider"], jsii.get(self, "dataProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="documentationInput")
    def documentation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "documentationInput"))

    @builtins.property
    @jsii.member(jsii_name="iconInput")
    def icon_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iconInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="listingIdInput")
    def listing_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listingIdInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryContactInput")
    def primary_contact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryContactInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubListingPublisher"]:
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingPublisher"], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="requestAccessInput")
    def request_access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigqueryAnalyticsHubListingTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigqueryAnalyticsHubListingTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="categories")
    def categories(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "categories"))

    @categories.setter
    def categories(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c47140d8f889b0c9f274330d749b69074ba5e0c9f8aa03e9f374769e98795a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "categories", value)

    @builtins.property
    @jsii.member(jsii_name="dataExchangeId")
    def data_exchange_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataExchangeId"))

    @data_exchange_id.setter
    def data_exchange_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d06e2d312321a9ecc662ceefe6c4ca80d3d97d1ca24b63f983d2ed14941fdd7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataExchangeId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__543a5417ca58049205ebe3c11a77d18219fe46b69a03f038f87b02261c924266)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676c80bd8fcc45d14203edc3bc0c3a501d7d16d0ffa90e10e203a4b0b7dfe5df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="documentation")
    def documentation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "documentation"))

    @documentation.setter
    def documentation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8995ccf7e5c997d1aa065257604d36c1468c1791e9fe2586c43eb310de401f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentation", value)

    @builtins.property
    @jsii.member(jsii_name="icon")
    def icon(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "icon"))

    @icon.setter
    def icon(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a57bd256d505c218123a3427ef2ccab9241c824c3c228dc92e70555c1d5da2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "icon", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af712e1a318ea2d85d6badb3a2ff4ac04e9322b05144fc8c66eaf96e7f799325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="listingId")
    def listing_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "listingId"))

    @listing_id.setter
    def listing_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78516182e4643e21fe38f3948e97158ca8842e6722b8f1dd361dad1329c63ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listingId", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001eb1733bcd8934d836909fab0ee71a9e922f78ea9c62bd63a1091ed6fbd4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9fec1bc3f8bb8af1bd53476ae2203c81e77a1f6f6ce34b213040e3f81cf3e8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a269c38f8627b4120973bb3cc444986b9c07486d661e82d4c2bfbefdc308f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="requestAccess")
    def request_access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestAccess"))

    @request_access.setter
    def request_access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec38b8dcbe50f1957c7715772d946b5a3ff01149f671e2f759ba1e9ced671ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestAccess", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingBigqueryDataset",
    jsii_struct_bases=[],
    name_mapping={"dataset": "dataset"},
)
class GoogleBigqueryAnalyticsHubListingBigqueryDataset:
    def __init__(self, *, dataset: builtins.str) -> None:
        '''
        :param dataset: Resource name of the dataset source for this listing. e.g. projects/myproject/datasets/123. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#dataset GoogleBigqueryAnalyticsHubListing#dataset}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba5184b6f5dac8efba253aa46a3de2fb7d90a8c6f444fbe8dc7938f2bb1fbc8)
            check_type(argname="argument dataset", value=dataset, expected_type=type_hints["dataset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset": dataset,
        }

    @builtins.property
    def dataset(self) -> builtins.str:
        '''Resource name of the dataset source for this listing. e.g. projects/myproject/datasets/123.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#dataset GoogleBigqueryAnalyticsHubListing#dataset}
        '''
        result = self._values.get("dataset")
        assert result is not None, "Required property 'dataset' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubListingBigqueryDataset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubListingBigqueryDatasetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingBigqueryDatasetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0b29b0b17c081b01c914964a9ee6493d3c2bef13ab8e62ebe9c95688b5d093b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="datasetInput")
    def dataset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetInput"))

    @builtins.property
    @jsii.member(jsii_name="dataset")
    def dataset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataset"))

    @dataset.setter
    def dataset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e235878681bf8aed65ac945482c9d78c64f6990b8604ece55d40ded90bf6c25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataset", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryAnalyticsHubListingBigqueryDataset]:
        return typing.cast(typing.Optional[GoogleBigqueryAnalyticsHubListingBigqueryDataset], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryAnalyticsHubListingBigqueryDataset],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b5d05ec5dc40d8b6988fd480828c7218ddd81823abe8092ea64b0210e1a0ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bigquery_dataset": "bigqueryDataset",
        "data_exchange_id": "dataExchangeId",
        "display_name": "displayName",
        "listing_id": "listingId",
        "location": "location",
        "categories": "categories",
        "data_provider": "dataProvider",
        "description": "description",
        "documentation": "documentation",
        "icon": "icon",
        "id": "id",
        "primary_contact": "primaryContact",
        "project": "project",
        "publisher": "publisher",
        "request_access": "requestAccess",
        "timeouts": "timeouts",
    },
)
class GoogleBigqueryAnalyticsHubListingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bigquery_dataset: typing.Union[GoogleBigqueryAnalyticsHubListingBigqueryDataset, typing.Dict[builtins.str, typing.Any]],
        data_exchange_id: builtins.str,
        display_name: builtins.str,
        listing_id: builtins.str,
        location: builtins.str,
        categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        data_provider: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingDataProvider", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        documentation: typing.Optional[builtins.str] = None,
        icon: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        primary_contact: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        publisher: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingPublisher", typing.Dict[builtins.str, typing.Any]]] = None,
        request_access: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigqueryAnalyticsHubListingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bigquery_dataset: bigquery_dataset block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#bigquery_dataset GoogleBigqueryAnalyticsHubListing#bigquery_dataset}
        :param data_exchange_id: The ID of the data exchange. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#data_exchange_id GoogleBigqueryAnalyticsHubListing#data_exchange_id}
        :param display_name: Human-readable display name of the listing. The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#display_name GoogleBigqueryAnalyticsHubListing#display_name}
        :param listing_id: The ID of the listing. Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#listing_id GoogleBigqueryAnalyticsHubListing#listing_id}
        :param location: The name of the location this data exchange listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#location GoogleBigqueryAnalyticsHubListing#location}
        :param categories: Categories of the listing. Up to two categories are allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#categories GoogleBigqueryAnalyticsHubListing#categories}
        :param data_provider: data_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#data_provider GoogleBigqueryAnalyticsHubListing#data_provider}
        :param description: Short description of the listing. The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#description GoogleBigqueryAnalyticsHubListing#description}
        :param documentation: Documentation describing the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#documentation GoogleBigqueryAnalyticsHubListing#documentation}
        :param icon: Base64 encoded image representing the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#icon GoogleBigqueryAnalyticsHubListing#icon}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#id GoogleBigqueryAnalyticsHubListing#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param primary_contact: Email or URL of the primary point of contact of the listing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#project GoogleBigqueryAnalyticsHubListing#project}.
        :param publisher: publisher block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#publisher GoogleBigqueryAnalyticsHubListing#publisher}
        :param request_access: Email or URL of the request access of the listing. Subscribers can use this reference to request access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#request_access GoogleBigqueryAnalyticsHubListing#request_access}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#timeouts GoogleBigqueryAnalyticsHubListing#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bigquery_dataset, dict):
            bigquery_dataset = GoogleBigqueryAnalyticsHubListingBigqueryDataset(**bigquery_dataset)
        if isinstance(data_provider, dict):
            data_provider = GoogleBigqueryAnalyticsHubListingDataProvider(**data_provider)
        if isinstance(publisher, dict):
            publisher = GoogleBigqueryAnalyticsHubListingPublisher(**publisher)
        if isinstance(timeouts, dict):
            timeouts = GoogleBigqueryAnalyticsHubListingTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b367299b584303edcf955004e12a3ce60a97c165fef439299e059ab9e25c76a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bigquery_dataset", value=bigquery_dataset, expected_type=type_hints["bigquery_dataset"])
            check_type(argname="argument data_exchange_id", value=data_exchange_id, expected_type=type_hints["data_exchange_id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument listing_id", value=listing_id, expected_type=type_hints["listing_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument categories", value=categories, expected_type=type_hints["categories"])
            check_type(argname="argument data_provider", value=data_provider, expected_type=type_hints["data_provider"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument documentation", value=documentation, expected_type=type_hints["documentation"])
            check_type(argname="argument icon", value=icon, expected_type=type_hints["icon"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument primary_contact", value=primary_contact, expected_type=type_hints["primary_contact"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
            check_type(argname="argument request_access", value=request_access, expected_type=type_hints["request_access"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bigquery_dataset": bigquery_dataset,
            "data_exchange_id": data_exchange_id,
            "display_name": display_name,
            "listing_id": listing_id,
            "location": location,
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
        if categories is not None:
            self._values["categories"] = categories
        if data_provider is not None:
            self._values["data_provider"] = data_provider
        if description is not None:
            self._values["description"] = description
        if documentation is not None:
            self._values["documentation"] = documentation
        if icon is not None:
            self._values["icon"] = icon
        if id is not None:
            self._values["id"] = id
        if primary_contact is not None:
            self._values["primary_contact"] = primary_contact
        if project is not None:
            self._values["project"] = project
        if publisher is not None:
            self._values["publisher"] = publisher
        if request_access is not None:
            self._values["request_access"] = request_access
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
    def bigquery_dataset(self) -> GoogleBigqueryAnalyticsHubListingBigqueryDataset:
        '''bigquery_dataset block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#bigquery_dataset GoogleBigqueryAnalyticsHubListing#bigquery_dataset}
        '''
        result = self._values.get("bigquery_dataset")
        assert result is not None, "Required property 'bigquery_dataset' is missing"
        return typing.cast(GoogleBigqueryAnalyticsHubListingBigqueryDataset, result)

    @builtins.property
    def data_exchange_id(self) -> builtins.str:
        '''The ID of the data exchange.

        Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#data_exchange_id GoogleBigqueryAnalyticsHubListing#data_exchange_id}
        '''
        result = self._values.get("data_exchange_id")
        assert result is not None, "Required property 'data_exchange_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''Human-readable display name of the listing.

        The display name must contain only Unicode letters, numbers (0-9), underscores (_), dashes (-), spaces ( ), ampersands (&) and can't start or end with spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#display_name GoogleBigqueryAnalyticsHubListing#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def listing_id(self) -> builtins.str:
        '''The ID of the listing.

        Must contain only Unicode letters, numbers (0-9), underscores (_). Should not use characters that require URL-escaping, or characters outside of ASCII, spaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#listing_id GoogleBigqueryAnalyticsHubListing#listing_id}
        '''
        result = self._values.get("listing_id")
        assert result is not None, "Required property 'listing_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The name of the location this data exchange listing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#location GoogleBigqueryAnalyticsHubListing#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def categories(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Categories of the listing. Up to two categories are allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#categories GoogleBigqueryAnalyticsHubListing#categories}
        '''
        result = self._values.get("categories")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def data_provider(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubListingDataProvider"]:
        '''data_provider block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#data_provider GoogleBigqueryAnalyticsHubListing#data_provider}
        '''
        result = self._values.get("data_provider")
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingDataProvider"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Short description of the listing.

        The description must not contain Unicode non-characters and C0 and C1 control codes except tabs (HT), new lines (LF), carriage returns (CR), and page breaks (FF).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#description GoogleBigqueryAnalyticsHubListing#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def documentation(self) -> typing.Optional[builtins.str]:
        '''Documentation describing the listing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#documentation GoogleBigqueryAnalyticsHubListing#documentation}
        '''
        result = self._values.get("documentation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def icon(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded image representing the listing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#icon GoogleBigqueryAnalyticsHubListing#icon}
        '''
        result = self._values.get("icon")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#id GoogleBigqueryAnalyticsHubListing#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the primary point of contact of the listing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#project GoogleBigqueryAnalyticsHubListing#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publisher(
        self,
    ) -> typing.Optional["GoogleBigqueryAnalyticsHubListingPublisher"]:
        '''publisher block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#publisher GoogleBigqueryAnalyticsHubListing#publisher}
        '''
        result = self._values.get("publisher")
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingPublisher"], result)

    @builtins.property
    def request_access(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the request access of the listing. Subscribers can use this reference to request access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#request_access GoogleBigqueryAnalyticsHubListing#request_access}
        '''
        result = self._values.get("request_access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleBigqueryAnalyticsHubListingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#timeouts GoogleBigqueryAnalyticsHubListing#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleBigqueryAnalyticsHubListingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubListingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingDataProvider",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "primary_contact": "primaryContact"},
)
class GoogleBigqueryAnalyticsHubListingDataProvider:
    def __init__(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the data provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#name GoogleBigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the data provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a6fd7afc595083d937c8fd2af6eae161bfd7b8b442798e093deb4b6d960e57)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary_contact", value=primary_contact, expected_type=type_hints["primary_contact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if primary_contact is not None:
            self._values["primary_contact"] = primary_contact

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the data provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#name GoogleBigqueryAnalyticsHubListing#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the data provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubListingDataProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubListingDataProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingDataProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0528f306788e22964c863aebdcb350eb374fe24bbad257b3039bb8215c51ee3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrimaryContact")
    def reset_primary_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContact", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryContactInput")
    def primary_contact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryContactInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff735ac4ddc9adc7f7ceec7aa97163414d722f381dbd9a3e4b2e1fb6e30b77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0267d3df4e933f0870d0b7cc8076c0abf648c49c0c1cf8885278cf27022b637b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryAnalyticsHubListingDataProvider]:
        return typing.cast(typing.Optional[GoogleBigqueryAnalyticsHubListingDataProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryAnalyticsHubListingDataProvider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8cf04f82c031d5483df95e986049ced2c59954397c0d23ae85ce62fbded9b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingPublisher",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "primary_contact": "primaryContact"},
)
class GoogleBigqueryAnalyticsHubListingPublisher:
    def __init__(
        self,
        *,
        name: builtins.str,
        primary_contact: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Name of the listing publisher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#name GoogleBigqueryAnalyticsHubListing#name}
        :param primary_contact: Email or URL of the listing publisher. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6855c91baed0b582ed75d400bdf30f6dc374cfa623188fd8324cdf1b48dbb7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary_contact", value=primary_contact, expected_type=type_hints["primary_contact"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if primary_contact is not None:
            self._values["primary_contact"] = primary_contact

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the listing publisher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#name GoogleBigqueryAnalyticsHubListing#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def primary_contact(self) -> typing.Optional[builtins.str]:
        '''Email or URL of the listing publisher.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#primary_contact GoogleBigqueryAnalyticsHubListing#primary_contact}
        '''
        result = self._values.get("primary_contact")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubListingPublisher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubListingPublisherOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingPublisherOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__797601595df7f568440444b6bbde19522a2a2d798be1173927fd8917074c52e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrimaryContact")
    def reset_primary_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryContact", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryContactInput")
    def primary_contact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryContactInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df9310129f54ce34c18115cd0bb295aa56478f26902e7bdc7ce4781a54d7867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="primaryContact")
    def primary_contact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryContact"))

    @primary_contact.setter
    def primary_contact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99861882318dce7832326de652d0d717f974e3185bee0445068d35b01176bf0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryContact", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryAnalyticsHubListingPublisher]:
        return typing.cast(typing.Optional[GoogleBigqueryAnalyticsHubListingPublisher], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryAnalyticsHubListingPublisher],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b47b9776facae2fddbea909028572c1d0f11077ca666e00966ef30de0ded31b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleBigqueryAnalyticsHubListingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#create GoogleBigqueryAnalyticsHubListing#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#delete GoogleBigqueryAnalyticsHubListing#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#update GoogleBigqueryAnalyticsHubListing#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5097e4d0b563172304dd6c1fc502e2d4bd880701da5c2bf2e9300d0ffb10e12a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#create GoogleBigqueryAnalyticsHubListing#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#delete GoogleBigqueryAnalyticsHubListing#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_bigquery_analytics_hub_listing#update GoogleBigqueryAnalyticsHubListing#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryAnalyticsHubListingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryAnalyticsHubListingTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryAnalyticsHubListing.GoogleBigqueryAnalyticsHubListingTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbed192342f7e49d37b0a0fca04b982f226ee25e041ed5939a8e3dc1ff67dc28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ce256c167438ac30daa25309dab39812d3701aa1263061dd57409a9ae0bd3fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1af8fd02bc79208ec79f4bf8343796921809447abd5ac89ae86a21bed3a2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2c264f95b6b9bc0d5587414ec6464c200a2b532dae77edd59bb985981b652c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubListingTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubListingTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubListingTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ebc74d43b8cb89cd4f9c2933d453784491f9deb388b6a0ca3833d2ca3528a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GoogleBigqueryAnalyticsHubListing",
    "GoogleBigqueryAnalyticsHubListingBigqueryDataset",
    "GoogleBigqueryAnalyticsHubListingBigqueryDatasetOutputReference",
    "GoogleBigqueryAnalyticsHubListingConfig",
    "GoogleBigqueryAnalyticsHubListingDataProvider",
    "GoogleBigqueryAnalyticsHubListingDataProviderOutputReference",
    "GoogleBigqueryAnalyticsHubListingPublisher",
    "GoogleBigqueryAnalyticsHubListingPublisherOutputReference",
    "GoogleBigqueryAnalyticsHubListingTimeouts",
    "GoogleBigqueryAnalyticsHubListingTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__74f1f2677cbe3d7372e4162c32a922d59f80ad350f54b4f5717154c71af05ad8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bigquery_dataset: typing.Union[GoogleBigqueryAnalyticsHubListingBigqueryDataset, typing.Dict[builtins.str, typing.Any]],
    data_exchange_id: builtins.str,
    display_name: builtins.str,
    listing_id: builtins.str,
    location: builtins.str,
    categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_provider: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingDataProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[builtins.str] = None,
    icon: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    primary_contact: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    publisher: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingPublisher, typing.Dict[builtins.str, typing.Any]]] = None,
    request_access: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f3c47140d8f889b0c9f274330d749b69074ba5e0c9f8aa03e9f374769e98795a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06e2d312321a9ecc662ceefe6c4ca80d3d97d1ca24b63f983d2ed14941fdd7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__543a5417ca58049205ebe3c11a77d18219fe46b69a03f038f87b02261c924266(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676c80bd8fcc45d14203edc3bc0c3a501d7d16d0ffa90e10e203a4b0b7dfe5df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8995ccf7e5c997d1aa065257604d36c1468c1791e9fe2586c43eb310de401f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a57bd256d505c218123a3427ef2ccab9241c824c3c228dc92e70555c1d5da2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af712e1a318ea2d85d6badb3a2ff4ac04e9322b05144fc8c66eaf96e7f799325(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78516182e4643e21fe38f3948e97158ca8842e6722b8f1dd361dad1329c63ebf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001eb1733bcd8934d836909fab0ee71a9e922f78ea9c62bd63a1091ed6fbd4d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9fec1bc3f8bb8af1bd53476ae2203c81e77a1f6f6ce34b213040e3f81cf3e8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a269c38f8627b4120973bb3cc444986b9c07486d661e82d4c2bfbefdc308f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec38b8dcbe50f1957c7715772d946b5a3ff01149f671e2f759ba1e9ced671ff8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba5184b6f5dac8efba253aa46a3de2fb7d90a8c6f444fbe8dc7938f2bb1fbc8(
    *,
    dataset: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b29b0b17c081b01c914964a9ee6493d3c2bef13ab8e62ebe9c95688b5d093b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e235878681bf8aed65ac945482c9d78c64f6990b8604ece55d40ded90bf6c25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b5d05ec5dc40d8b6988fd480828c7218ddd81823abe8092ea64b0210e1a0ed(
    value: typing.Optional[GoogleBigqueryAnalyticsHubListingBigqueryDataset],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b367299b584303edcf955004e12a3ce60a97c165fef439299e059ab9e25c76a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bigquery_dataset: typing.Union[GoogleBigqueryAnalyticsHubListingBigqueryDataset, typing.Dict[builtins.str, typing.Any]],
    data_exchange_id: builtins.str,
    display_name: builtins.str,
    listing_id: builtins.str,
    location: builtins.str,
    categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_provider: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingDataProvider, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    documentation: typing.Optional[builtins.str] = None,
    icon: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    primary_contact: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    publisher: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingPublisher, typing.Dict[builtins.str, typing.Any]]] = None,
    request_access: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigqueryAnalyticsHubListingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a6fd7afc595083d937c8fd2af6eae161bfd7b8b442798e093deb4b6d960e57(
    *,
    name: builtins.str,
    primary_contact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0528f306788e22964c863aebdcb350eb374fe24bbad257b3039bb8215c51ee3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff735ac4ddc9adc7f7ceec7aa97163414d722f381dbd9a3e4b2e1fb6e30b77b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0267d3df4e933f0870d0b7cc8076c0abf648c49c0c1cf8885278cf27022b637b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8cf04f82c031d5483df95e986049ced2c59954397c0d23ae85ce62fbded9b3a(
    value: typing.Optional[GoogleBigqueryAnalyticsHubListingDataProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6855c91baed0b582ed75d400bdf30f6dc374cfa623188fd8324cdf1b48dbb7(
    *,
    name: builtins.str,
    primary_contact: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797601595df7f568440444b6bbde19522a2a2d798be1173927fd8917074c52e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df9310129f54ce34c18115cd0bb295aa56478f26902e7bdc7ce4781a54d7867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99861882318dce7832326de652d0d717f974e3185bee0445068d35b01176bf0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b47b9776facae2fddbea909028572c1d0f11077ca666e00966ef30de0ded31b(
    value: typing.Optional[GoogleBigqueryAnalyticsHubListingPublisher],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5097e4d0b563172304dd6c1fc502e2d4bd880701da5c2bf2e9300d0ffb10e12a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbed192342f7e49d37b0a0fca04b982f226ee25e041ed5939a8e3dc1ff67dc28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce256c167438ac30daa25309dab39812d3701aa1263061dd57409a9ae0bd3fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1af8fd02bc79208ec79f4bf8343796921809447abd5ac89ae86a21bed3a2bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2c264f95b6b9bc0d5587414ec6464c200a2b532dae77edd59bb985981b652c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ebc74d43b8cb89cd4f9c2933d453784491f9deb388b6a0ca3833d2ca3528a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryAnalyticsHubListingTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
