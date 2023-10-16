'''
# `google_compute_router_peer`

Refer to the Terraform Registory for docs: [`google_compute_router_peer`](https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer).
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


class GoogleComputeRouterPeer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterPeer.GoogleComputeRouterPeer",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer google_compute_router_peer}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        interface: builtins.str,
        name: builtins.str,
        peer_asn: jsii.Number,
        router: builtins.str,
        advertised_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        advertised_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRouterPeerAdvertisedIpRanges", typing.Dict[builtins.str, typing.Any]]]]] = None,
        advertised_route_priority: typing.Optional[jsii.Number] = None,
        advertise_mode: typing.Optional[builtins.str] = None,
        bfd: typing.Optional[typing.Union["GoogleComputeRouterPeerBfd", typing.Dict[builtins.str, typing.Any]]] = None,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ipv6: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        ipv6_nexthop_address: typing.Optional[builtins.str] = None,
        peer_ip_address: typing.Optional[builtins.str] = None,
        peer_ipv6_nexthop_address: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        router_appliance_instance: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRouterPeerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer google_compute_router_peer} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param interface: Name of the interface the BGP peer is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#interface GoogleComputeRouterPeer#interface}
        :param name: Name of this BGP peer. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#name GoogleComputeRouterPeer#name}
        :param peer_asn: Peer BGP Autonomous System Number (ASN). Each BGP interface may use a different value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#peer_asn GoogleComputeRouterPeer#peer_asn}
        :param router: The name of the Cloud Router in which this BgpPeer will be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#router GoogleComputeRouterPeer#router}
        :param advertised_groups: User-specified list of prefix groups to advertise in custom mode, which currently supports the following option:. - 'ALL_SUBNETS': Advertises all of the router's own VPC subnets. This excludes any routes learned for subnets that use VPC Network Peering. Note that this field can only be populated if advertiseMode is 'CUSTOM' and overrides the list defined for the router (in the "bgp" message). These groups are advertised in addition to any specified prefixes. Leave this field blank to advertise no custom groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#advertised_groups GoogleComputeRouterPeer#advertised_groups}
        :param advertised_ip_ranges: advertised_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#advertised_ip_ranges GoogleComputeRouterPeer#advertised_ip_ranges}
        :param advertised_route_priority: The priority of routes advertised to this BGP peer. Where there is more than one matching route of maximum length, the routes with the lowest priority value win. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#advertised_route_priority GoogleComputeRouterPeer#advertised_route_priority}
        :param advertise_mode: User-specified flag to indicate which mode to use for advertisement. Valid values of this enum field are: 'DEFAULT', 'CUSTOM' Default value: "DEFAULT" Possible values: ["DEFAULT", "CUSTOM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#advertise_mode GoogleComputeRouterPeer#advertise_mode}
        :param bfd: bfd block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#bfd GoogleComputeRouterPeer#bfd}
        :param enable: The status of the BGP peer connection. If set to false, any active session with the peer is terminated and all associated routing information is removed. If set to true, the peer connection can be established with routing information. The default is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#enable GoogleComputeRouterPeer#enable}
        :param enable_ipv6: Enable IPv6 traffic over BGP Peer. If not specified, it is disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#enable_ipv6 GoogleComputeRouterPeer#enable_ipv6}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#id GoogleComputeRouterPeer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address: IP address of the interface inside Google Cloud Platform. Only IPv4 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#ip_address GoogleComputeRouterPeer#ip_address}
        :param ipv6_nexthop_address: IPv6 address of the interface inside Google Cloud Platform. The address must be in the range 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64. If you do not specify the next hop addresses, Google Cloud automatically assigns unused addresses from the 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64 range for you. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#ipv6_nexthop_address GoogleComputeRouterPeer#ipv6_nexthop_address}
        :param peer_ip_address: IP address of the BGP interface outside Google Cloud Platform. Only IPv4 is supported. Required if 'ip_address' is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#peer_ip_address GoogleComputeRouterPeer#peer_ip_address}
        :param peer_ipv6_nexthop_address: IPv6 address of the BGP interface outside Google Cloud Platform. The address must be in the range 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64. If you do not specify the next hop addresses, Google Cloud automatically assigns unused addresses from the 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64 range for you. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#peer_ipv6_nexthop_address GoogleComputeRouterPeer#peer_ipv6_nexthop_address}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#project GoogleComputeRouterPeer#project}.
        :param region: Region where the router and BgpPeer reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#region GoogleComputeRouterPeer#region}
        :param router_appliance_instance: The URI of the VM instance that is used as third-party router appliances such as Next Gen Firewalls, Virtual Routers, or Router Appliances. The VM instance must be located in zones contained in the same region as this Cloud Router. The VM instance is the peer side of the BGP session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#router_appliance_instance GoogleComputeRouterPeer#router_appliance_instance}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#timeouts GoogleComputeRouterPeer#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18430f7233ea5565bf32e68a183cdfdb221c35da988e2d39159671b6c9f8a00f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleComputeRouterPeerConfig(
            interface=interface,
            name=name,
            peer_asn=peer_asn,
            router=router,
            advertised_groups=advertised_groups,
            advertised_ip_ranges=advertised_ip_ranges,
            advertised_route_priority=advertised_route_priority,
            advertise_mode=advertise_mode,
            bfd=bfd,
            enable=enable,
            enable_ipv6=enable_ipv6,
            id=id,
            ip_address=ip_address,
            ipv6_nexthop_address=ipv6_nexthop_address,
            peer_ip_address=peer_ip_address,
            peer_ipv6_nexthop_address=peer_ipv6_nexthop_address,
            project=project,
            region=region,
            router_appliance_instance=router_appliance_instance,
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

    @jsii.member(jsii_name="putAdvertisedIpRanges")
    def put_advertised_ip_ranges(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleComputeRouterPeerAdvertisedIpRanges", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c220a51c417427fde5aabc5e7585d6fb6848b065e0f71ba269484c3df9dd7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdvertisedIpRanges", [value]))

    @jsii.member(jsii_name="putBfd")
    def put_bfd(
        self,
        *,
        session_initialization_mode: builtins.str,
        min_receive_interval: typing.Optional[jsii.Number] = None,
        min_transmit_interval: typing.Optional[jsii.Number] = None,
        multiplier: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param session_initialization_mode: The BFD session initialization mode for this BGP peer. If set to 'ACTIVE', the Cloud Router will initiate the BFD session for this BGP peer. If set to 'PASSIVE', the Cloud Router will wait for the peer router to initiate the BFD session for this BGP peer. If set to 'DISABLED', BFD is disabled for this BGP peer. Possible values: ["ACTIVE", "DISABLED", "PASSIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#session_initialization_mode GoogleComputeRouterPeer#session_initialization_mode}
        :param min_receive_interval: The minimum interval, in milliseconds, between BFD control packets received from the peer router. The actual value is negotiated between the two routers and is equal to the greater of this value and the transmit interval of the other router. If set, this value must be between 1000 and 30000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#min_receive_interval GoogleComputeRouterPeer#min_receive_interval}
        :param min_transmit_interval: The minimum interval, in milliseconds, between BFD control packets transmitted to the peer router. The actual value is negotiated between the two routers and is equal to the greater of this value and the corresponding receive interval of the other router. If set, this value must be between 1000 and 30000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#min_transmit_interval GoogleComputeRouterPeer#min_transmit_interval}
        :param multiplier: The number of consecutive BFD packets that must be missed before BFD declares that a peer is unavailable. If set, the value must be a value between 5 and 16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#multiplier GoogleComputeRouterPeer#multiplier}
        '''
        value = GoogleComputeRouterPeerBfd(
            session_initialization_mode=session_initialization_mode,
            min_receive_interval=min_receive_interval,
            min_transmit_interval=min_transmit_interval,
            multiplier=multiplier,
        )

        return typing.cast(None, jsii.invoke(self, "putBfd", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#create GoogleComputeRouterPeer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#delete GoogleComputeRouterPeer#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#update GoogleComputeRouterPeer#update}.
        '''
        value = GoogleComputeRouterPeerTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdvertisedGroups")
    def reset_advertised_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertisedGroups", []))

    @jsii.member(jsii_name="resetAdvertisedIpRanges")
    def reset_advertised_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertisedIpRanges", []))

    @jsii.member(jsii_name="resetAdvertisedRoutePriority")
    def reset_advertised_route_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertisedRoutePriority", []))

    @jsii.member(jsii_name="resetAdvertiseMode")
    def reset_advertise_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertiseMode", []))

    @jsii.member(jsii_name="resetBfd")
    def reset_bfd(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBfd", []))

    @jsii.member(jsii_name="resetEnable")
    def reset_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnable", []))

    @jsii.member(jsii_name="resetEnableIpv6")
    def reset_enable_ipv6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableIpv6", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetIpv6NexthopAddress")
    def reset_ipv6_nexthop_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6NexthopAddress", []))

    @jsii.member(jsii_name="resetPeerIpAddress")
    def reset_peer_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerIpAddress", []))

    @jsii.member(jsii_name="resetPeerIpv6NexthopAddress")
    def reset_peer_ipv6_nexthop_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerIpv6NexthopAddress", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRouterApplianceInstance")
    def reset_router_appliance_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouterApplianceInstance", []))

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
    @jsii.member(jsii_name="advertisedIpRanges")
    def advertised_ip_ranges(self) -> "GoogleComputeRouterPeerAdvertisedIpRangesList":
        return typing.cast("GoogleComputeRouterPeerAdvertisedIpRangesList", jsii.get(self, "advertisedIpRanges"))

    @builtins.property
    @jsii.member(jsii_name="bfd")
    def bfd(self) -> "GoogleComputeRouterPeerBfdOutputReference":
        return typing.cast("GoogleComputeRouterPeerBfdOutputReference", jsii.get(self, "bfd"))

    @builtins.property
    @jsii.member(jsii_name="managementType")
    def management_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managementType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleComputeRouterPeerTimeoutsOutputReference":
        return typing.cast("GoogleComputeRouterPeerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="advertisedGroupsInput")
    def advertised_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "advertisedGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedIpRangesInput")
    def advertised_ip_ranges_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterPeerAdvertisedIpRanges"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleComputeRouterPeerAdvertisedIpRanges"]]], jsii.get(self, "advertisedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedRoutePriorityInput")
    def advertised_route_priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "advertisedRoutePriorityInput"))

    @builtins.property
    @jsii.member(jsii_name="advertiseModeInput")
    def advertise_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "advertiseModeInput"))

    @builtins.property
    @jsii.member(jsii_name="bfdInput")
    def bfd_input(self) -> typing.Optional["GoogleComputeRouterPeerBfd"]:
        return typing.cast(typing.Optional["GoogleComputeRouterPeerBfd"], jsii.get(self, "bfdInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInput")
    def enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInput"))

    @builtins.property
    @jsii.member(jsii_name="enableIpv6Input")
    def enable_ipv6_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableIpv6Input"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceInput")
    def interface_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6NexthopAddressInput")
    def ipv6_nexthop_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6NexthopAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="peerAsnInput")
    def peer_asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "peerAsnInput"))

    @builtins.property
    @jsii.member(jsii_name="peerIpAddressInput")
    def peer_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="peerIpv6NexthopAddressInput")
    def peer_ipv6_nexthop_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerIpv6NexthopAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="routerApplianceInstanceInput")
    def router_appliance_instance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routerApplianceInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="routerInput")
    def router_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routerInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRouterPeerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleComputeRouterPeerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedGroups")
    def advertised_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "advertisedGroups"))

    @advertised_groups.setter
    def advertised_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee91e5d40a01f8f2fb43d3a33e088e4149809e2ab4bdb97567083c9e0f8d4994)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertisedGroups", value)

    @builtins.property
    @jsii.member(jsii_name="advertisedRoutePriority")
    def advertised_route_priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "advertisedRoutePriority"))

    @advertised_route_priority.setter
    def advertised_route_priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__426135d33af555b20e7a4d1baa20ad98c3459ed1d5c90051ecd962e07265504b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertisedRoutePriority", value)

    @builtins.property
    @jsii.member(jsii_name="advertiseMode")
    def advertise_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "advertiseMode"))

    @advertise_mode.setter
    def advertise_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f501b24371a110c4a39fc1a4198286009efe9b8556cf204d51bd90ac97a9d1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertiseMode", value)

    @builtins.property
    @jsii.member(jsii_name="enable")
    def enable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enable"))

    @enable.setter
    def enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da88c66ba6810965e894876912663807d4f9ebcd70798e4512aaff0fd53236b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enable", value)

    @builtins.property
    @jsii.member(jsii_name="enableIpv6")
    def enable_ipv6(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableIpv6"))

    @enable_ipv6.setter
    def enable_ipv6(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb4c618195bbc487990c05b8687c37afe04a69a6344b88fd9f7c7b0276c76abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableIpv6", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e030fa00235402994964decaf9d0197bfcdcd2dddd8ad548806dd137215001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="interface")
    def interface(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interface"))

    @interface.setter
    def interface(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee99e64721b1d26a1243ab24b6ec298dc3e1667c08aa1da772ad3a3e8ecdd7c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interface", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7735590272cf2b6f5cca032afecbda37c68760a92f19f23f4a615c1ede5a6805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="ipv6NexthopAddress")
    def ipv6_nexthop_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6NexthopAddress"))

    @ipv6_nexthop_address.setter
    def ipv6_nexthop_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d122d6f40ebdcd7acced82458261afea6e1f05a147b5c7f5f2a018ac8bfb5eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6NexthopAddress", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c544af7f097cba3ea6e8c5b80a07153943f9c9ef6e3dcdc3192ebbcec1e78ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="peerAsn")
    def peer_asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "peerAsn"))

    @peer_asn.setter
    def peer_asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4d48731d80947d6313de74101b599085eadd3abf3a2b57e0df66233094fa0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerAsn", value)

    @builtins.property
    @jsii.member(jsii_name="peerIpAddress")
    def peer_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerIpAddress"))

    @peer_ip_address.setter
    def peer_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ea83eb1d497d594e54cf0e2c74ceab7f7d6d693d0fcde78ec1ff2b4194de09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerIpAddress", value)

    @builtins.property
    @jsii.member(jsii_name="peerIpv6NexthopAddress")
    def peer_ipv6_nexthop_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerIpv6NexthopAddress"))

    @peer_ipv6_nexthop_address.setter
    def peer_ipv6_nexthop_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacd5e1484cf05743e82526dbe7f22cf02c6cec7ae771f6c0c6210cc8a7557d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerIpv6NexthopAddress", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2ece31dcbc46511656e198560a99c385d119c46281510779825ecbfc5c01fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4e612e896e07d9f71eea9c23a2ce27421a7a6c80ec5cb69086819d9148ceea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="router")
    def router(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "router"))

    @router.setter
    def router(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d1cee514d7dcc5b36df99b93e3f0cb7719eaea1095a96ce9f8c7507dee01e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "router", value)

    @builtins.property
    @jsii.member(jsii_name="routerApplianceInstance")
    def router_appliance_instance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routerApplianceInstance"))

    @router_appliance_instance.setter
    def router_appliance_instance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27cc3b58a936d05e030c4d96c7554991fe82d972a33ff8a487870cb603970c36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routerApplianceInstance", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterPeer.GoogleComputeRouterPeerAdvertisedIpRanges",
    jsii_struct_bases=[],
    name_mapping={"range": "range", "description": "description"},
)
class GoogleComputeRouterPeerAdvertisedIpRanges:
    def __init__(
        self,
        *,
        range: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param range: The IP range to advertise. The value must be a CIDR-formatted string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#range GoogleComputeRouterPeer#range}
        :param description: User-specified description for the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#description GoogleComputeRouterPeer#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4ae52fb2da3952344bef415ef3cf3af7f4096deb7a6d8576390129538bd303)
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "range": range,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def range(self) -> builtins.str:
        '''The IP range to advertise. The value must be a CIDR-formatted string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#range GoogleComputeRouterPeer#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-specified description for the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#description GoogleComputeRouterPeer#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRouterPeerAdvertisedIpRanges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRouterPeerAdvertisedIpRangesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterPeer.GoogleComputeRouterPeerAdvertisedIpRangesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4633929bcdac79d6d7837537518004327e1640dc3c76226042c6063c29887a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleComputeRouterPeerAdvertisedIpRangesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13498d616c400bcb36922cb71d53eefca3dbfb8a675f396b378fe8b2653acd55)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleComputeRouterPeerAdvertisedIpRangesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868ced6540843f130e7fbb27ad2bd748a4720be460b4251f65eb9761ab56bd7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa3405a6a665ea1d6e3233a7147db825a0273e7a807e9b756b884bef30b98628)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f2bc16a14eaa9f2881d9ea75223530eda07a45dbea28228bacedba401e6e9d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterPeerAdvertisedIpRanges]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterPeerAdvertisedIpRanges]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterPeerAdvertisedIpRanges]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bdfd05f78e513ca5aa54147ca1e236d5243023cd27a4cf22f095fae6332903b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GoogleComputeRouterPeerAdvertisedIpRangesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterPeer.GoogleComputeRouterPeerAdvertisedIpRangesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67a65b6a06f3bd3cdcbb7782ad25f097c449c7886daa775329fce12e86369398)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc7f97d56145a7a6d855b8fb0207b0891f17c7167f0038999abe5927350f871b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "range"))

    @range.setter
    def range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__533cca9acc941f88edaa7c8f53bed8dfc0678608cf673a45a4aee448896db722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "range", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterPeerAdvertisedIpRanges]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterPeerAdvertisedIpRanges]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterPeerAdvertisedIpRanges]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a172f0cbd870f74735f3bcbb171ea0cf4eab14589e737d1898776df5cd9d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterPeer.GoogleComputeRouterPeerBfd",
    jsii_struct_bases=[],
    name_mapping={
        "session_initialization_mode": "sessionInitializationMode",
        "min_receive_interval": "minReceiveInterval",
        "min_transmit_interval": "minTransmitInterval",
        "multiplier": "multiplier",
    },
)
class GoogleComputeRouterPeerBfd:
    def __init__(
        self,
        *,
        session_initialization_mode: builtins.str,
        min_receive_interval: typing.Optional[jsii.Number] = None,
        min_transmit_interval: typing.Optional[jsii.Number] = None,
        multiplier: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param session_initialization_mode: The BFD session initialization mode for this BGP peer. If set to 'ACTIVE', the Cloud Router will initiate the BFD session for this BGP peer. If set to 'PASSIVE', the Cloud Router will wait for the peer router to initiate the BFD session for this BGP peer. If set to 'DISABLED', BFD is disabled for this BGP peer. Possible values: ["ACTIVE", "DISABLED", "PASSIVE"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#session_initialization_mode GoogleComputeRouterPeer#session_initialization_mode}
        :param min_receive_interval: The minimum interval, in milliseconds, between BFD control packets received from the peer router. The actual value is negotiated between the two routers and is equal to the greater of this value and the transmit interval of the other router. If set, this value must be between 1000 and 30000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#min_receive_interval GoogleComputeRouterPeer#min_receive_interval}
        :param min_transmit_interval: The minimum interval, in milliseconds, between BFD control packets transmitted to the peer router. The actual value is negotiated between the two routers and is equal to the greater of this value and the corresponding receive interval of the other router. If set, this value must be between 1000 and 30000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#min_transmit_interval GoogleComputeRouterPeer#min_transmit_interval}
        :param multiplier: The number of consecutive BFD packets that must be missed before BFD declares that a peer is unavailable. If set, the value must be a value between 5 and 16. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#multiplier GoogleComputeRouterPeer#multiplier}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce67722877f1dcf11836e3977e6bfeb2ab3613d39ab7e01ddf5a18a6ac0282a)
            check_type(argname="argument session_initialization_mode", value=session_initialization_mode, expected_type=type_hints["session_initialization_mode"])
            check_type(argname="argument min_receive_interval", value=min_receive_interval, expected_type=type_hints["min_receive_interval"])
            check_type(argname="argument min_transmit_interval", value=min_transmit_interval, expected_type=type_hints["min_transmit_interval"])
            check_type(argname="argument multiplier", value=multiplier, expected_type=type_hints["multiplier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "session_initialization_mode": session_initialization_mode,
        }
        if min_receive_interval is not None:
            self._values["min_receive_interval"] = min_receive_interval
        if min_transmit_interval is not None:
            self._values["min_transmit_interval"] = min_transmit_interval
        if multiplier is not None:
            self._values["multiplier"] = multiplier

    @builtins.property
    def session_initialization_mode(self) -> builtins.str:
        '''The BFD session initialization mode for this BGP peer.

        If set to 'ACTIVE', the Cloud Router will initiate the BFD session
        for this BGP peer. If set to 'PASSIVE', the Cloud Router will wait
        for the peer router to initiate the BFD session for this BGP peer.
        If set to 'DISABLED', BFD is disabled for this BGP peer. Possible values: ["ACTIVE", "DISABLED", "PASSIVE"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#session_initialization_mode GoogleComputeRouterPeer#session_initialization_mode}
        '''
        result = self._values.get("session_initialization_mode")
        assert result is not None, "Required property 'session_initialization_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def min_receive_interval(self) -> typing.Optional[jsii.Number]:
        '''The minimum interval, in milliseconds, between BFD control packets received from the peer router.

        The actual value is negotiated
        between the two routers and is equal to the greater of this value
        and the transmit interval of the other router. If set, this value
        must be between 1000 and 30000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#min_receive_interval GoogleComputeRouterPeer#min_receive_interval}
        '''
        result = self._values.get("min_receive_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_transmit_interval(self) -> typing.Optional[jsii.Number]:
        '''The minimum interval, in milliseconds, between BFD control packets transmitted to the peer router.

        The actual value is negotiated
        between the two routers and is equal to the greater of this value
        and the corresponding receive interval of the other router. If set,
        this value must be between 1000 and 30000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#min_transmit_interval GoogleComputeRouterPeer#min_transmit_interval}
        '''
        result = self._values.get("min_transmit_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def multiplier(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive BFD packets that must be missed before BFD declares that a peer is unavailable.

        If set, the value must
        be a value between 5 and 16.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#multiplier GoogleComputeRouterPeer#multiplier}
        '''
        result = self._values.get("multiplier")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRouterPeerBfd(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRouterPeerBfdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterPeer.GoogleComputeRouterPeerBfdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09282ae77464ec8d42863c0759c9dc652a8679088b59e23b926a2d143bf62f6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMinReceiveInterval")
    def reset_min_receive_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinReceiveInterval", []))

    @jsii.member(jsii_name="resetMinTransmitInterval")
    def reset_min_transmit_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTransmitInterval", []))

    @jsii.member(jsii_name="resetMultiplier")
    def reset_multiplier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultiplier", []))

    @builtins.property
    @jsii.member(jsii_name="minReceiveIntervalInput")
    def min_receive_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReceiveIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="minTransmitIntervalInput")
    def min_transmit_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minTransmitIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="multiplierInput")
    def multiplier_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "multiplierInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionInitializationModeInput")
    def session_initialization_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionInitializationModeInput"))

    @builtins.property
    @jsii.member(jsii_name="minReceiveInterval")
    def min_receive_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReceiveInterval"))

    @min_receive_interval.setter
    def min_receive_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc07752bf33ad19ed08b0266177f083d9b8c2b5e8bd90a01b5fffa6cfde0b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReceiveInterval", value)

    @builtins.property
    @jsii.member(jsii_name="minTransmitInterval")
    def min_transmit_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minTransmitInterval"))

    @min_transmit_interval.setter
    def min_transmit_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7cebc48e2f2ecbc5cf97a8194672f51033a3cb6deb9641ce6e01d5fe5cd3ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTransmitInterval", value)

    @builtins.property
    @jsii.member(jsii_name="multiplier")
    def multiplier(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "multiplier"))

    @multiplier.setter
    def multiplier(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afdea86cee968b02f176333e3cb3e5c064db2ec688983e482d1f31716bf2c4d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multiplier", value)

    @builtins.property
    @jsii.member(jsii_name="sessionInitializationMode")
    def session_initialization_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionInitializationMode"))

    @session_initialization_mode.setter
    def session_initialization_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d767c92888a711ab13f3f3cc0125ef276903c576462da14aecbf4e206d4a652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionInitializationMode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleComputeRouterPeerBfd]:
        return typing.cast(typing.Optional[GoogleComputeRouterPeerBfd], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleComputeRouterPeerBfd],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__169284d20aaba36bf20fd25b4ad34f6df27b53c6bb12aa23ecf0f1c24af5456c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterPeer.GoogleComputeRouterPeerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "interface": "interface",
        "name": "name",
        "peer_asn": "peerAsn",
        "router": "router",
        "advertised_groups": "advertisedGroups",
        "advertised_ip_ranges": "advertisedIpRanges",
        "advertised_route_priority": "advertisedRoutePriority",
        "advertise_mode": "advertiseMode",
        "bfd": "bfd",
        "enable": "enable",
        "enable_ipv6": "enableIpv6",
        "id": "id",
        "ip_address": "ipAddress",
        "ipv6_nexthop_address": "ipv6NexthopAddress",
        "peer_ip_address": "peerIpAddress",
        "peer_ipv6_nexthop_address": "peerIpv6NexthopAddress",
        "project": "project",
        "region": "region",
        "router_appliance_instance": "routerApplianceInstance",
        "timeouts": "timeouts",
    },
)
class GoogleComputeRouterPeerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        interface: builtins.str,
        name: builtins.str,
        peer_asn: jsii.Number,
        router: builtins.str,
        advertised_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        advertised_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterPeerAdvertisedIpRanges, typing.Dict[builtins.str, typing.Any]]]]] = None,
        advertised_route_priority: typing.Optional[jsii.Number] = None,
        advertise_mode: typing.Optional[builtins.str] = None,
        bfd: typing.Optional[typing.Union[GoogleComputeRouterPeerBfd, typing.Dict[builtins.str, typing.Any]]] = None,
        enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_ipv6: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        ipv6_nexthop_address: typing.Optional[builtins.str] = None,
        peer_ip_address: typing.Optional[builtins.str] = None,
        peer_ipv6_nexthop_address: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        router_appliance_instance: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleComputeRouterPeerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param interface: Name of the interface the BGP peer is associated with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#interface GoogleComputeRouterPeer#interface}
        :param name: Name of this BGP peer. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#name GoogleComputeRouterPeer#name}
        :param peer_asn: Peer BGP Autonomous System Number (ASN). Each BGP interface may use a different value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#peer_asn GoogleComputeRouterPeer#peer_asn}
        :param router: The name of the Cloud Router in which this BgpPeer will be configured. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#router GoogleComputeRouterPeer#router}
        :param advertised_groups: User-specified list of prefix groups to advertise in custom mode, which currently supports the following option:. - 'ALL_SUBNETS': Advertises all of the router's own VPC subnets. This excludes any routes learned for subnets that use VPC Network Peering. Note that this field can only be populated if advertiseMode is 'CUSTOM' and overrides the list defined for the router (in the "bgp" message). These groups are advertised in addition to any specified prefixes. Leave this field blank to advertise no custom groups. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#advertised_groups GoogleComputeRouterPeer#advertised_groups}
        :param advertised_ip_ranges: advertised_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#advertised_ip_ranges GoogleComputeRouterPeer#advertised_ip_ranges}
        :param advertised_route_priority: The priority of routes advertised to this BGP peer. Where there is more than one matching route of maximum length, the routes with the lowest priority value win. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#advertised_route_priority GoogleComputeRouterPeer#advertised_route_priority}
        :param advertise_mode: User-specified flag to indicate which mode to use for advertisement. Valid values of this enum field are: 'DEFAULT', 'CUSTOM' Default value: "DEFAULT" Possible values: ["DEFAULT", "CUSTOM"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#advertise_mode GoogleComputeRouterPeer#advertise_mode}
        :param bfd: bfd block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#bfd GoogleComputeRouterPeer#bfd}
        :param enable: The status of the BGP peer connection. If set to false, any active session with the peer is terminated and all associated routing information is removed. If set to true, the peer connection can be established with routing information. The default is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#enable GoogleComputeRouterPeer#enable}
        :param enable_ipv6: Enable IPv6 traffic over BGP Peer. If not specified, it is disabled by default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#enable_ipv6 GoogleComputeRouterPeer#enable_ipv6}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#id GoogleComputeRouterPeer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_address: IP address of the interface inside Google Cloud Platform. Only IPv4 is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#ip_address GoogleComputeRouterPeer#ip_address}
        :param ipv6_nexthop_address: IPv6 address of the interface inside Google Cloud Platform. The address must be in the range 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64. If you do not specify the next hop addresses, Google Cloud automatically assigns unused addresses from the 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64 range for you. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#ipv6_nexthop_address GoogleComputeRouterPeer#ipv6_nexthop_address}
        :param peer_ip_address: IP address of the BGP interface outside Google Cloud Platform. Only IPv4 is supported. Required if 'ip_address' is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#peer_ip_address GoogleComputeRouterPeer#peer_ip_address}
        :param peer_ipv6_nexthop_address: IPv6 address of the BGP interface outside Google Cloud Platform. The address must be in the range 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64. If you do not specify the next hop addresses, Google Cloud automatically assigns unused addresses from the 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64 range for you. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#peer_ipv6_nexthop_address GoogleComputeRouterPeer#peer_ipv6_nexthop_address}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#project GoogleComputeRouterPeer#project}.
        :param region: Region where the router and BgpPeer reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#region GoogleComputeRouterPeer#region}
        :param router_appliance_instance: The URI of the VM instance that is used as third-party router appliances such as Next Gen Firewalls, Virtual Routers, or Router Appliances. The VM instance must be located in zones contained in the same region as this Cloud Router. The VM instance is the peer side of the BGP session. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#router_appliance_instance GoogleComputeRouterPeer#router_appliance_instance}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#timeouts GoogleComputeRouterPeer#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bfd, dict):
            bfd = GoogleComputeRouterPeerBfd(**bfd)
        if isinstance(timeouts, dict):
            timeouts = GoogleComputeRouterPeerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ed39791389b9b4f003ca9e8bbc48f9ef7713edbab3a86cfc042160bacb7e82)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument interface", value=interface, expected_type=type_hints["interface"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument peer_asn", value=peer_asn, expected_type=type_hints["peer_asn"])
            check_type(argname="argument router", value=router, expected_type=type_hints["router"])
            check_type(argname="argument advertised_groups", value=advertised_groups, expected_type=type_hints["advertised_groups"])
            check_type(argname="argument advertised_ip_ranges", value=advertised_ip_ranges, expected_type=type_hints["advertised_ip_ranges"])
            check_type(argname="argument advertised_route_priority", value=advertised_route_priority, expected_type=type_hints["advertised_route_priority"])
            check_type(argname="argument advertise_mode", value=advertise_mode, expected_type=type_hints["advertise_mode"])
            check_type(argname="argument bfd", value=bfd, expected_type=type_hints["bfd"])
            check_type(argname="argument enable", value=enable, expected_type=type_hints["enable"])
            check_type(argname="argument enable_ipv6", value=enable_ipv6, expected_type=type_hints["enable_ipv6"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument ipv6_nexthop_address", value=ipv6_nexthop_address, expected_type=type_hints["ipv6_nexthop_address"])
            check_type(argname="argument peer_ip_address", value=peer_ip_address, expected_type=type_hints["peer_ip_address"])
            check_type(argname="argument peer_ipv6_nexthop_address", value=peer_ipv6_nexthop_address, expected_type=type_hints["peer_ipv6_nexthop_address"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument router_appliance_instance", value=router_appliance_instance, expected_type=type_hints["router_appliance_instance"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interface": interface,
            "name": name,
            "peer_asn": peer_asn,
            "router": router,
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
        if advertised_groups is not None:
            self._values["advertised_groups"] = advertised_groups
        if advertised_ip_ranges is not None:
            self._values["advertised_ip_ranges"] = advertised_ip_ranges
        if advertised_route_priority is not None:
            self._values["advertised_route_priority"] = advertised_route_priority
        if advertise_mode is not None:
            self._values["advertise_mode"] = advertise_mode
        if bfd is not None:
            self._values["bfd"] = bfd
        if enable is not None:
            self._values["enable"] = enable
        if enable_ipv6 is not None:
            self._values["enable_ipv6"] = enable_ipv6
        if id is not None:
            self._values["id"] = id
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if ipv6_nexthop_address is not None:
            self._values["ipv6_nexthop_address"] = ipv6_nexthop_address
        if peer_ip_address is not None:
            self._values["peer_ip_address"] = peer_ip_address
        if peer_ipv6_nexthop_address is not None:
            self._values["peer_ipv6_nexthop_address"] = peer_ipv6_nexthop_address
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if router_appliance_instance is not None:
            self._values["router_appliance_instance"] = router_appliance_instance
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
    def interface(self) -> builtins.str:
        '''Name of the interface the BGP peer is associated with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#interface GoogleComputeRouterPeer#interface}
        '''
        result = self._values.get("interface")
        assert result is not None, "Required property 'interface' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of this BGP peer.

        The name must be 1-63 characters long,
        and comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which
        means the first character must be a lowercase letter, and all
        following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#name GoogleComputeRouterPeer#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def peer_asn(self) -> jsii.Number:
        '''Peer BGP Autonomous System Number (ASN). Each BGP interface may use a different value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#peer_asn GoogleComputeRouterPeer#peer_asn}
        '''
        result = self._values.get("peer_asn")
        assert result is not None, "Required property 'peer_asn' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def router(self) -> builtins.str:
        '''The name of the Cloud Router in which this BgpPeer will be configured.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#router GoogleComputeRouterPeer#router}
        '''
        result = self._values.get("router")
        assert result is not None, "Required property 'router' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advertised_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''User-specified list of prefix groups to advertise in custom mode, which currently supports the following option:.

        - 'ALL_SUBNETS': Advertises all of the router's own VPC subnets.
          This excludes any routes learned for subnets that use VPC Network
          Peering.

        Note that this field can only be populated if advertiseMode is 'CUSTOM'
        and overrides the list defined for the router (in the "bgp" message).
        These groups are advertised in addition to any specified prefixes.
        Leave this field blank to advertise no custom groups.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#advertised_groups GoogleComputeRouterPeer#advertised_groups}
        '''
        result = self._values.get("advertised_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def advertised_ip_ranges(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterPeerAdvertisedIpRanges]]]:
        '''advertised_ip_ranges block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#advertised_ip_ranges GoogleComputeRouterPeer#advertised_ip_ranges}
        '''
        result = self._values.get("advertised_ip_ranges")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterPeerAdvertisedIpRanges]]], result)

    @builtins.property
    def advertised_route_priority(self) -> typing.Optional[jsii.Number]:
        '''The priority of routes advertised to this BGP peer.

        Where there is more than one matching route of maximum
        length, the routes with the lowest priority value win.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#advertised_route_priority GoogleComputeRouterPeer#advertised_route_priority}
        '''
        result = self._values.get("advertised_route_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def advertise_mode(self) -> typing.Optional[builtins.str]:
        '''User-specified flag to indicate which mode to use for advertisement.

        Valid values of this enum field are: 'DEFAULT', 'CUSTOM' Default value: "DEFAULT" Possible values: ["DEFAULT", "CUSTOM"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#advertise_mode GoogleComputeRouterPeer#advertise_mode}
        '''
        result = self._values.get("advertise_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bfd(self) -> typing.Optional[GoogleComputeRouterPeerBfd]:
        '''bfd block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#bfd GoogleComputeRouterPeer#bfd}
        '''
        result = self._values.get("bfd")
        return typing.cast(typing.Optional[GoogleComputeRouterPeerBfd], result)

    @builtins.property
    def enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The status of the BGP peer connection.

        If set to false, any active session
        with the peer is terminated and all associated routing information is removed.
        If set to true, the peer connection can be established with routing information.
        The default is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#enable GoogleComputeRouterPeer#enable}
        '''
        result = self._values.get("enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_ipv6(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable IPv6 traffic over BGP Peer. If not specified, it is disabled by default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#enable_ipv6 GoogleComputeRouterPeer#enable_ipv6}
        '''
        result = self._values.get("enable_ipv6")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#id GoogleComputeRouterPeer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''IP address of the interface inside Google Cloud Platform. Only IPv4 is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#ip_address GoogleComputeRouterPeer#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_nexthop_address(self) -> typing.Optional[builtins.str]:
        '''IPv6 address of the interface inside Google Cloud Platform.

        The address must be in the range 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64.
        If you do not specify the next hop addresses, Google Cloud automatically
        assigns unused addresses from the 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64 range for you.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#ipv6_nexthop_address GoogleComputeRouterPeer#ipv6_nexthop_address}
        '''
        result = self._values.get("ipv6_nexthop_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_ip_address(self) -> typing.Optional[builtins.str]:
        '''IP address of the BGP interface outside Google Cloud Platform. Only IPv4 is supported. Required if 'ip_address' is set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#peer_ip_address GoogleComputeRouterPeer#peer_ip_address}
        '''
        result = self._values.get("peer_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_ipv6_nexthop_address(self) -> typing.Optional[builtins.str]:
        '''IPv6 address of the BGP interface outside Google Cloud Platform.

        The address must be in the range 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64.
        If you do not specify the next hop addresses, Google Cloud automatically
        assigns unused addresses from the 2600:2d00:0:2::/64 or 2600:2d00:0:3::/64 range for you.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#peer_ipv6_nexthop_address GoogleComputeRouterPeer#peer_ipv6_nexthop_address}
        '''
        result = self._values.get("peer_ipv6_nexthop_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#project GoogleComputeRouterPeer#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where the router and BgpPeer reside. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#region GoogleComputeRouterPeer#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def router_appliance_instance(self) -> typing.Optional[builtins.str]:
        '''The URI of the VM instance that is used as third-party router appliances such as Next Gen Firewalls, Virtual Routers, or Router Appliances.

        The VM instance must be located in zones contained in the same region as
        this Cloud Router. The VM instance is the peer side of the BGP session.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#router_appliance_instance GoogleComputeRouterPeer#router_appliance_instance}
        '''
        result = self._values.get("router_appliance_instance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleComputeRouterPeerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#timeouts GoogleComputeRouterPeer#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleComputeRouterPeerTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRouterPeerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterPeer.GoogleComputeRouterPeerTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleComputeRouterPeerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#create GoogleComputeRouterPeer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#delete GoogleComputeRouterPeer#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#update GoogleComputeRouterPeer#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5678224788a92386c23fa06bbe6a3e8aaeca9af74e7eaffa458abdf0caefd6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#create GoogleComputeRouterPeer#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#delete GoogleComputeRouterPeer#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/5.1.0/docs/resources/google_compute_router_peer#update GoogleComputeRouterPeer#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleComputeRouterPeerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleComputeRouterPeerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleComputeRouterPeer.GoogleComputeRouterPeerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0abd51103a038635dd9e88091e7c97f6388dd12c1831988442530beecc34265e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63533324c22c24351ab43058a44ee6465875549468bc5f7e32f85c78dbe3fc57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe6ea0cd7bc9f61c07a3b9a4c5e1711aca05ca963bcde5008213bff70695b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4e50cd6097d420860b51421b5bf418524d1ffddf838815a5adfe52c77988e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterPeerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterPeerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterPeerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1281c945faa9cc69edd1ac048b7dc19049679ff3ae43735813042b0137c27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GoogleComputeRouterPeer",
    "GoogleComputeRouterPeerAdvertisedIpRanges",
    "GoogleComputeRouterPeerAdvertisedIpRangesList",
    "GoogleComputeRouterPeerAdvertisedIpRangesOutputReference",
    "GoogleComputeRouterPeerBfd",
    "GoogleComputeRouterPeerBfdOutputReference",
    "GoogleComputeRouterPeerConfig",
    "GoogleComputeRouterPeerTimeouts",
    "GoogleComputeRouterPeerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__18430f7233ea5565bf32e68a183cdfdb221c35da988e2d39159671b6c9f8a00f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    interface: builtins.str,
    name: builtins.str,
    peer_asn: jsii.Number,
    router: builtins.str,
    advertised_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    advertised_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterPeerAdvertisedIpRanges, typing.Dict[builtins.str, typing.Any]]]]] = None,
    advertised_route_priority: typing.Optional[jsii.Number] = None,
    advertise_mode: typing.Optional[builtins.str] = None,
    bfd: typing.Optional[typing.Union[GoogleComputeRouterPeerBfd, typing.Dict[builtins.str, typing.Any]]] = None,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ipv6: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    ipv6_nexthop_address: typing.Optional[builtins.str] = None,
    peer_ip_address: typing.Optional[builtins.str] = None,
    peer_ipv6_nexthop_address: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    router_appliance_instance: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRouterPeerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b8c220a51c417427fde5aabc5e7585d6fb6848b065e0f71ba269484c3df9dd7f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterPeerAdvertisedIpRanges, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee91e5d40a01f8f2fb43d3a33e088e4149809e2ab4bdb97567083c9e0f8d4994(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__426135d33af555b20e7a4d1baa20ad98c3459ed1d5c90051ecd962e07265504b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f501b24371a110c4a39fc1a4198286009efe9b8556cf204d51bd90ac97a9d1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da88c66ba6810965e894876912663807d4f9ebcd70798e4512aaff0fd53236b0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4c618195bbc487990c05b8687c37afe04a69a6344b88fd9f7c7b0276c76abb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e030fa00235402994964decaf9d0197bfcdcd2dddd8ad548806dd137215001(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee99e64721b1d26a1243ab24b6ec298dc3e1667c08aa1da772ad3a3e8ecdd7c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7735590272cf2b6f5cca032afecbda37c68760a92f19f23f4a615c1ede5a6805(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d122d6f40ebdcd7acced82458261afea6e1f05a147b5c7f5f2a018ac8bfb5eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c544af7f097cba3ea6e8c5b80a07153943f9c9ef6e3dcdc3192ebbcec1e78ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4d48731d80947d6313de74101b599085eadd3abf3a2b57e0df66233094fa0e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ea83eb1d497d594e54cf0e2c74ceab7f7d6d693d0fcde78ec1ff2b4194de09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacd5e1484cf05743e82526dbe7f22cf02c6cec7ae771f6c0c6210cc8a7557d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2ece31dcbc46511656e198560a99c385d119c46281510779825ecbfc5c01fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4e612e896e07d9f71eea9c23a2ce27421a7a6c80ec5cb69086819d9148ceea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d1cee514d7dcc5b36df99b93e3f0cb7719eaea1095a96ce9f8c7507dee01e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27cc3b58a936d05e030c4d96c7554991fe82d972a33ff8a487870cb603970c36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4ae52fb2da3952344bef415ef3cf3af7f4096deb7a6d8576390129538bd303(
    *,
    range: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4633929bcdac79d6d7837537518004327e1640dc3c76226042c6063c29887a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13498d616c400bcb36922cb71d53eefca3dbfb8a675f396b378fe8b2653acd55(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868ced6540843f130e7fbb27ad2bd748a4720be460b4251f65eb9761ab56bd7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3405a6a665ea1d6e3233a7147db825a0273e7a807e9b756b884bef30b98628(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2bc16a14eaa9f2881d9ea75223530eda07a45dbea28228bacedba401e6e9d1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bdfd05f78e513ca5aa54147ca1e236d5243023cd27a4cf22f095fae6332903b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleComputeRouterPeerAdvertisedIpRanges]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a65b6a06f3bd3cdcbb7782ad25f097c449c7886daa775329fce12e86369398(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7f97d56145a7a6d855b8fb0207b0891f17c7167f0038999abe5927350f871b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533cca9acc941f88edaa7c8f53bed8dfc0678608cf673a45a4aee448896db722(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a172f0cbd870f74735f3bcbb171ea0cf4eab14589e737d1898776df5cd9d0d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterPeerAdvertisedIpRanges]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce67722877f1dcf11836e3977e6bfeb2ab3613d39ab7e01ddf5a18a6ac0282a(
    *,
    session_initialization_mode: builtins.str,
    min_receive_interval: typing.Optional[jsii.Number] = None,
    min_transmit_interval: typing.Optional[jsii.Number] = None,
    multiplier: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09282ae77464ec8d42863c0759c9dc652a8679088b59e23b926a2d143bf62f6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc07752bf33ad19ed08b0266177f083d9b8c2b5e8bd90a01b5fffa6cfde0b9a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7cebc48e2f2ecbc5cf97a8194672f51033a3cb6deb9641ce6e01d5fe5cd3ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdea86cee968b02f176333e3cb3e5c064db2ec688983e482d1f31716bf2c4d9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d767c92888a711ab13f3f3cc0125ef276903c576462da14aecbf4e206d4a652(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169284d20aaba36bf20fd25b4ad34f6df27b53c6bb12aa23ecf0f1c24af5456c(
    value: typing.Optional[GoogleComputeRouterPeerBfd],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ed39791389b9b4f003ca9e8bbc48f9ef7713edbab3a86cfc042160bacb7e82(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    interface: builtins.str,
    name: builtins.str,
    peer_asn: jsii.Number,
    router: builtins.str,
    advertised_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    advertised_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleComputeRouterPeerAdvertisedIpRanges, typing.Dict[builtins.str, typing.Any]]]]] = None,
    advertised_route_priority: typing.Optional[jsii.Number] = None,
    advertise_mode: typing.Optional[builtins.str] = None,
    bfd: typing.Optional[typing.Union[GoogleComputeRouterPeerBfd, typing.Dict[builtins.str, typing.Any]]] = None,
    enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_ipv6: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    ipv6_nexthop_address: typing.Optional[builtins.str] = None,
    peer_ip_address: typing.Optional[builtins.str] = None,
    peer_ipv6_nexthop_address: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    router_appliance_instance: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleComputeRouterPeerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5678224788a92386c23fa06bbe6a3e8aaeca9af74e7eaffa458abdf0caefd6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abd51103a038635dd9e88091e7c97f6388dd12c1831988442530beecc34265e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63533324c22c24351ab43058a44ee6465875549468bc5f7e32f85c78dbe3fc57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe6ea0cd7bc9f61c07a3b9a4c5e1711aca05ca963bcde5008213bff70695b82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4e50cd6097d420860b51421b5bf418524d1ffddf838815a5adfe52c77988e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1281c945faa9cc69edd1ac048b7dc19049679ff3ae43735813042b0137c27a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleComputeRouterPeerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
