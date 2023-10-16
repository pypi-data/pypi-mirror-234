'''
# `okta_policy_device_assurance_ios`

Refer to the Terraform Registory for docs: [`okta_policy_device_assurance_ios`](https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios).
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


class PolicyDeviceAssuranceIos(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyDeviceAssuranceIos.PolicyDeviceAssuranceIos",
):
    '''Represents a {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios okta_policy_device_assurance_ios}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        jailbreak: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        os_version: typing.Optional[builtins.str] = None,
        screenlock_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios okta_policy_device_assurance_ios} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Policy device assurance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios#name PolicyDeviceAssuranceIos#name}
        :param jailbreak: The device jailbreak. Only for android and iOS platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios#jailbreak PolicyDeviceAssuranceIos#jailbreak}
        :param os_version: The device os minimum version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios#os_version PolicyDeviceAssuranceIos#os_version}
        :param screenlock_type: List of screenlock type, can be BIOMETRIC or BIOMETRIC, PASSCODE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios#screenlock_type PolicyDeviceAssuranceIos#screenlock_type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77d4447df1cfe9d5e09815a7f458f8aa482bb8902fe90347388edd55ac973ac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = PolicyDeviceAssuranceIosConfig(
            name=name,
            jailbreak=jailbreak,
            os_version=os_version,
            screenlock_type=screenlock_type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetJailbreak")
    def reset_jailbreak(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJailbreak", []))

    @jsii.member(jsii_name="resetOsVersion")
    def reset_os_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsVersion", []))

    @jsii.member(jsii_name="resetScreenlockType")
    def reset_screenlock_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScreenlockType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @builtins.property
    @jsii.member(jsii_name="createdDate")
    def created_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdDate"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdate")
    def last_update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdate"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedBy")
    def last_updated_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdatedBy"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @builtins.property
    @jsii.member(jsii_name="jailbreakInput")
    def jailbreak_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "jailbreakInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="osVersionInput")
    def os_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="screenlockTypeInput")
    def screenlock_type_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "screenlockTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="jailbreak")
    def jailbreak(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "jailbreak"))

    @jailbreak.setter
    def jailbreak(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f362e52eb31217ffc349a85674768b2480e857b0adc82b67ae893d66f04de2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jailbreak", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f07d74588bf7d0e4f94be4513681042a890fe6ff85a614e17fd679dfc119203)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3a77141b067ebb350835ba1dde2d1c1ce1363af84d717a072c213795c57c0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value)

    @builtins.property
    @jsii.member(jsii_name="screenlockType")
    def screenlock_type(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "screenlockType"))

    @screenlock_type.setter
    def screenlock_type(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600672554529faf22ec05f8da30b684068470c3127860ba0c652421ac5d3ec28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "screenlockType", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyDeviceAssuranceIos.PolicyDeviceAssuranceIosConfig",
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
        "jailbreak": "jailbreak",
        "os_version": "osVersion",
        "screenlock_type": "screenlockType",
    },
)
class PolicyDeviceAssuranceIosConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        jailbreak: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        os_version: typing.Optional[builtins.str] = None,
        screenlock_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Policy device assurance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios#name PolicyDeviceAssuranceIos#name}
        :param jailbreak: The device jailbreak. Only for android and iOS platform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios#jailbreak PolicyDeviceAssuranceIos#jailbreak}
        :param os_version: The device os minimum version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios#os_version PolicyDeviceAssuranceIos#os_version}
        :param screenlock_type: List of screenlock type, can be BIOMETRIC or BIOMETRIC, PASSCODE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios#screenlock_type PolicyDeviceAssuranceIos#screenlock_type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dae91ca245005aea19dc3db658e9e51bd24fe9d695258ab8b16bbf3ef27a5f12)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument jailbreak", value=jailbreak, expected_type=type_hints["jailbreak"])
            check_type(argname="argument os_version", value=os_version, expected_type=type_hints["os_version"])
            check_type(argname="argument screenlock_type", value=screenlock_type, expected_type=type_hints["screenlock_type"])
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
        if jailbreak is not None:
            self._values["jailbreak"] = jailbreak
        if os_version is not None:
            self._values["os_version"] = os_version
        if screenlock_type is not None:
            self._values["screenlock_type"] = screenlock_type

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
        '''Policy device assurance name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios#name PolicyDeviceAssuranceIos#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jailbreak(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The device jailbreak. Only for android and iOS platform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios#jailbreak PolicyDeviceAssuranceIos#jailbreak}
        '''
        result = self._values.get("jailbreak")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def os_version(self) -> typing.Optional[builtins.str]:
        '''The device os minimum version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios#os_version PolicyDeviceAssuranceIos#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def screenlock_type(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of screenlock type, can be BIOMETRIC or BIOMETRIC, PASSCODE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_ios#screenlock_type PolicyDeviceAssuranceIos#screenlock_type}
        '''
        result = self._values.get("screenlock_type")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyDeviceAssuranceIosConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PolicyDeviceAssuranceIos",
    "PolicyDeviceAssuranceIosConfig",
]

publication.publish()

def _typecheckingstub__d77d4447df1cfe9d5e09815a7f458f8aa482bb8902fe90347388edd55ac973ac(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    jailbreak: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    os_version: typing.Optional[builtins.str] = None,
    screenlock_type: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__43f362e52eb31217ffc349a85674768b2480e857b0adc82b67ae893d66f04de2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f07d74588bf7d0e4f94be4513681042a890fe6ff85a614e17fd679dfc119203(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3a77141b067ebb350835ba1dde2d1c1ce1363af84d717a072c213795c57c0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600672554529faf22ec05f8da30b684068470c3127860ba0c652421ac5d3ec28(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae91ca245005aea19dc3db658e9e51bd24fe9d695258ab8b16bbf3ef27a5f12(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    jailbreak: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    os_version: typing.Optional[builtins.str] = None,
    screenlock_type: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
