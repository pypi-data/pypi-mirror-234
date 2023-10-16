'''
# `okta_policy_device_assurance_chromeos`

Refer to the Terraform Registory for docs: [`okta_policy_device_assurance_chromeos`](https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos).
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


class PolicyDeviceAssuranceChromeos(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyDeviceAssuranceChromeos.PolicyDeviceAssuranceChromeos",
):
    '''Represents a {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos okta_policy_device_assurance_chromeos}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        tpsp_allow_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_browser_version: typing.Optional[builtins.str] = None,
        tpsp_builtin_dns_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_chrome_remote_desktop_app_blocked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_device_enrollment_domain: typing.Optional[builtins.str] = None,
        tpsp_disk_encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_key_trust_level: typing.Optional[builtins.str] = None,
        tpsp_os_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_os_version: typing.Optional[builtins.str] = None,
        tpsp_password_proctection_warning_trigger: typing.Optional[builtins.str] = None,
        tpsp_realtime_url_check_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_safe_browsing_protection_level: typing.Optional[builtins.str] = None,
        tpsp_screen_lock_secured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_site_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos okta_policy_device_assurance_chromeos} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Policy device assurance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#name PolicyDeviceAssuranceChromeos#name}
        :param tpsp_allow_screen_lock: Third party signal provider allow screen lock. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_allow_screen_lock PolicyDeviceAssuranceChromeos#tpsp_allow_screen_lock}
        :param tpsp_browser_version: Third party signal provider minimum browser version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_browser_version PolicyDeviceAssuranceChromeos#tpsp_browser_version}
        :param tpsp_builtin_dns_client_enabled: Third party signal provider builtin dns client enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_builtin_dns_client_enabled PolicyDeviceAssuranceChromeos#tpsp_builtin_dns_client_enabled}
        :param tpsp_chrome_remote_desktop_app_blocked: Third party signal provider chrome remote desktop app blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_chrome_remote_desktop_app_blocked PolicyDeviceAssuranceChromeos#tpsp_chrome_remote_desktop_app_blocked}
        :param tpsp_device_enrollment_domain: Third party signal provider device enrollment domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_device_enrollment_domain PolicyDeviceAssuranceChromeos#tpsp_device_enrollment_domain}
        :param tpsp_disk_encrypted: Third party signal provider disk encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_disk_encrypted PolicyDeviceAssuranceChromeos#tpsp_disk_encrypted}
        :param tpsp_key_trust_level: Third party signal provider key trust level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_key_trust_level PolicyDeviceAssuranceChromeos#tpsp_key_trust_level}
        :param tpsp_os_firewall: Third party signal provider os firewall. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_os_firewall PolicyDeviceAssuranceChromeos#tpsp_os_firewall}
        :param tpsp_os_version: Third party signal provider minimum os version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_os_version PolicyDeviceAssuranceChromeos#tpsp_os_version}
        :param tpsp_password_proctection_warning_trigger: Third party signal provider password protection warning trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_password_proctection_warning_trigger PolicyDeviceAssuranceChromeos#tpsp_password_proctection_warning_trigger}
        :param tpsp_realtime_url_check_mode: Third party signal provider realtime url check mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_realtime_url_check_mode PolicyDeviceAssuranceChromeos#tpsp_realtime_url_check_mode}
        :param tpsp_safe_browsing_protection_level: Third party signal provider safe browsing protection level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_safe_browsing_protection_level PolicyDeviceAssuranceChromeos#tpsp_safe_browsing_protection_level}
        :param tpsp_screen_lock_secured: Third party signal provider screen lock secure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_screen_lock_secured PolicyDeviceAssuranceChromeos#tpsp_screen_lock_secured}
        :param tpsp_site_isolation_enabled: Third party signal provider site isolation enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_site_isolation_enabled PolicyDeviceAssuranceChromeos#tpsp_site_isolation_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5edc4180359f03dc7c8142fa34acac3bc859b3261073381dcd6233c0397073)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = PolicyDeviceAssuranceChromeosConfig(
            name=name,
            tpsp_allow_screen_lock=tpsp_allow_screen_lock,
            tpsp_browser_version=tpsp_browser_version,
            tpsp_builtin_dns_client_enabled=tpsp_builtin_dns_client_enabled,
            tpsp_chrome_remote_desktop_app_blocked=tpsp_chrome_remote_desktop_app_blocked,
            tpsp_device_enrollment_domain=tpsp_device_enrollment_domain,
            tpsp_disk_encrypted=tpsp_disk_encrypted,
            tpsp_key_trust_level=tpsp_key_trust_level,
            tpsp_os_firewall=tpsp_os_firewall,
            tpsp_os_version=tpsp_os_version,
            tpsp_password_proctection_warning_trigger=tpsp_password_proctection_warning_trigger,
            tpsp_realtime_url_check_mode=tpsp_realtime_url_check_mode,
            tpsp_safe_browsing_protection_level=tpsp_safe_browsing_protection_level,
            tpsp_screen_lock_secured=tpsp_screen_lock_secured,
            tpsp_site_isolation_enabled=tpsp_site_isolation_enabled,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetTpspAllowScreenLock")
    def reset_tpsp_allow_screen_lock(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspAllowScreenLock", []))

    @jsii.member(jsii_name="resetTpspBrowserVersion")
    def reset_tpsp_browser_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspBrowserVersion", []))

    @jsii.member(jsii_name="resetTpspBuiltinDnsClientEnabled")
    def reset_tpsp_builtin_dns_client_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspBuiltinDnsClientEnabled", []))

    @jsii.member(jsii_name="resetTpspChromeRemoteDesktopAppBlocked")
    def reset_tpsp_chrome_remote_desktop_app_blocked(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspChromeRemoteDesktopAppBlocked", []))

    @jsii.member(jsii_name="resetTpspDeviceEnrollmentDomain")
    def reset_tpsp_device_enrollment_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspDeviceEnrollmentDomain", []))

    @jsii.member(jsii_name="resetTpspDiskEncrypted")
    def reset_tpsp_disk_encrypted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspDiskEncrypted", []))

    @jsii.member(jsii_name="resetTpspKeyTrustLevel")
    def reset_tpsp_key_trust_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspKeyTrustLevel", []))

    @jsii.member(jsii_name="resetTpspOsFirewall")
    def reset_tpsp_os_firewall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspOsFirewall", []))

    @jsii.member(jsii_name="resetTpspOsVersion")
    def reset_tpsp_os_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspOsVersion", []))

    @jsii.member(jsii_name="resetTpspPasswordProctectionWarningTrigger")
    def reset_tpsp_password_proctection_warning_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspPasswordProctectionWarningTrigger", []))

    @jsii.member(jsii_name="resetTpspRealtimeUrlCheckMode")
    def reset_tpsp_realtime_url_check_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspRealtimeUrlCheckMode", []))

    @jsii.member(jsii_name="resetTpspSafeBrowsingProtectionLevel")
    def reset_tpsp_safe_browsing_protection_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspSafeBrowsingProtectionLevel", []))

    @jsii.member(jsii_name="resetTpspScreenLockSecured")
    def reset_tpsp_screen_lock_secured(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspScreenLockSecured", []))

    @jsii.member(jsii_name="resetTpspSiteIsolationEnabled")
    def reset_tpsp_site_isolation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspSiteIsolationEnabled", []))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspAllowScreenLockInput")
    def tpsp_allow_screen_lock_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tpspAllowScreenLockInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspBrowserVersionInput")
    def tpsp_browser_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpspBrowserVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspBuiltinDnsClientEnabledInput")
    def tpsp_builtin_dns_client_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tpspBuiltinDnsClientEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspChromeRemoteDesktopAppBlockedInput")
    def tpsp_chrome_remote_desktop_app_blocked_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tpspChromeRemoteDesktopAppBlockedInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspDeviceEnrollmentDomainInput")
    def tpsp_device_enrollment_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpspDeviceEnrollmentDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspDiskEncryptedInput")
    def tpsp_disk_encrypted_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tpspDiskEncryptedInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspKeyTrustLevelInput")
    def tpsp_key_trust_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpspKeyTrustLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspOsFirewallInput")
    def tpsp_os_firewall_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tpspOsFirewallInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspOsVersionInput")
    def tpsp_os_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpspOsVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspPasswordProctectionWarningTriggerInput")
    def tpsp_password_proctection_warning_trigger_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpspPasswordProctectionWarningTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspRealtimeUrlCheckModeInput")
    def tpsp_realtime_url_check_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tpspRealtimeUrlCheckModeInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspSafeBrowsingProtectionLevelInput")
    def tpsp_safe_browsing_protection_level_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpspSafeBrowsingProtectionLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspScreenLockSecuredInput")
    def tpsp_screen_lock_secured_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tpspScreenLockSecuredInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspSiteIsolationEnabledInput")
    def tpsp_site_isolation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tpspSiteIsolationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__293a950432a0ae1b274359a5abd18ec3940358e0b958478f9d8f0b74c7474952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="tpspAllowScreenLock")
    def tpsp_allow_screen_lock(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tpspAllowScreenLock"))

    @tpsp_allow_screen_lock.setter
    def tpsp_allow_screen_lock(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ffe4c7b36545131d8d81f0c269f2b423cf36c2e402d7ceddd49a71509d7e90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspAllowScreenLock", value)

    @builtins.property
    @jsii.member(jsii_name="tpspBrowserVersion")
    def tpsp_browser_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspBrowserVersion"))

    @tpsp_browser_version.setter
    def tpsp_browser_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e57563d920d9df37cfff248c90da1117b1bbdcf69d18fedbcf5456c08155c51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspBrowserVersion", value)

    @builtins.property
    @jsii.member(jsii_name="tpspBuiltinDnsClientEnabled")
    def tpsp_builtin_dns_client_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tpspBuiltinDnsClientEnabled"))

    @tpsp_builtin_dns_client_enabled.setter
    def tpsp_builtin_dns_client_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0fad50397873a7e75fda04c28b27a08abf427ab0e55d0fd4776a0ccd643d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspBuiltinDnsClientEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="tpspChromeRemoteDesktopAppBlocked")
    def tpsp_chrome_remote_desktop_app_blocked(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tpspChromeRemoteDesktopAppBlocked"))

    @tpsp_chrome_remote_desktop_app_blocked.setter
    def tpsp_chrome_remote_desktop_app_blocked(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__477bccdfd19de9f4995754f88258f99f74656d92490973bdf809b8b12738c164)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspChromeRemoteDesktopAppBlocked", value)

    @builtins.property
    @jsii.member(jsii_name="tpspDeviceEnrollmentDomain")
    def tpsp_device_enrollment_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspDeviceEnrollmentDomain"))

    @tpsp_device_enrollment_domain.setter
    def tpsp_device_enrollment_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ecd678d3c6fb360f99daf7581c9115ac1c1b9f2d171f496eb55b9a69adb34a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspDeviceEnrollmentDomain", value)

    @builtins.property
    @jsii.member(jsii_name="tpspDiskEncrypted")
    def tpsp_disk_encrypted(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tpspDiskEncrypted"))

    @tpsp_disk_encrypted.setter
    def tpsp_disk_encrypted(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1fa3c0e3075af6167cb9c070c50bc3b368c1f3ffb3913ba86efec67731d2eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspDiskEncrypted", value)

    @builtins.property
    @jsii.member(jsii_name="tpspKeyTrustLevel")
    def tpsp_key_trust_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspKeyTrustLevel"))

    @tpsp_key_trust_level.setter
    def tpsp_key_trust_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d9b0d6a6dc8f5780c93497038c35ebd084555d9c8b187eabde54fd3eb9d8d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspKeyTrustLevel", value)

    @builtins.property
    @jsii.member(jsii_name="tpspOsFirewall")
    def tpsp_os_firewall(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tpspOsFirewall"))

    @tpsp_os_firewall.setter
    def tpsp_os_firewall(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73886567046867ac198ad2d4b69bb6b444e87e8937a14ddf1c3b49ebe74dddb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspOsFirewall", value)

    @builtins.property
    @jsii.member(jsii_name="tpspOsVersion")
    def tpsp_os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspOsVersion"))

    @tpsp_os_version.setter
    def tpsp_os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d328a4a59baffeb5e45629ac8f2cdc8d0b15d304e484b4a7d7b63dedc53e50fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspOsVersion", value)

    @builtins.property
    @jsii.member(jsii_name="tpspPasswordProctectionWarningTrigger")
    def tpsp_password_proctection_warning_trigger(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspPasswordProctectionWarningTrigger"))

    @tpsp_password_proctection_warning_trigger.setter
    def tpsp_password_proctection_warning_trigger(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb0c781248345346fc6b0927a6255815ac7de97a690deae18748d4b007255d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspPasswordProctectionWarningTrigger", value)

    @builtins.property
    @jsii.member(jsii_name="tpspRealtimeUrlCheckMode")
    def tpsp_realtime_url_check_mode(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tpspRealtimeUrlCheckMode"))

    @tpsp_realtime_url_check_mode.setter
    def tpsp_realtime_url_check_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d220c3aa072d3a5ece4fc00c5756f70652a5c3819daed390716ddcedb621da8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspRealtimeUrlCheckMode", value)

    @builtins.property
    @jsii.member(jsii_name="tpspSafeBrowsingProtectionLevel")
    def tpsp_safe_browsing_protection_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspSafeBrowsingProtectionLevel"))

    @tpsp_safe_browsing_protection_level.setter
    def tpsp_safe_browsing_protection_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36445b445525a5856c8dd65a4430874a2f5205290ffa04444332f7527f9c7435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspSafeBrowsingProtectionLevel", value)

    @builtins.property
    @jsii.member(jsii_name="tpspScreenLockSecured")
    def tpsp_screen_lock_secured(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tpspScreenLockSecured"))

    @tpsp_screen_lock_secured.setter
    def tpsp_screen_lock_secured(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489809f8c0ca5279ce1a6222d9e199d64ec2c40d4cc3d93d9c16e26d3a699a9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspScreenLockSecured", value)

    @builtins.property
    @jsii.member(jsii_name="tpspSiteIsolationEnabled")
    def tpsp_site_isolation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tpspSiteIsolationEnabled"))

    @tpsp_site_isolation_enabled.setter
    def tpsp_site_isolation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85965af01c687fa3ee83e889e4303961e118806a9fbbe55aa49769766f83f8af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspSiteIsolationEnabled", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyDeviceAssuranceChromeos.PolicyDeviceAssuranceChromeosConfig",
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
        "tpsp_allow_screen_lock": "tpspAllowScreenLock",
        "tpsp_browser_version": "tpspBrowserVersion",
        "tpsp_builtin_dns_client_enabled": "tpspBuiltinDnsClientEnabled",
        "tpsp_chrome_remote_desktop_app_blocked": "tpspChromeRemoteDesktopAppBlocked",
        "tpsp_device_enrollment_domain": "tpspDeviceEnrollmentDomain",
        "tpsp_disk_encrypted": "tpspDiskEncrypted",
        "tpsp_key_trust_level": "tpspKeyTrustLevel",
        "tpsp_os_firewall": "tpspOsFirewall",
        "tpsp_os_version": "tpspOsVersion",
        "tpsp_password_proctection_warning_trigger": "tpspPasswordProctectionWarningTrigger",
        "tpsp_realtime_url_check_mode": "tpspRealtimeUrlCheckMode",
        "tpsp_safe_browsing_protection_level": "tpspSafeBrowsingProtectionLevel",
        "tpsp_screen_lock_secured": "tpspScreenLockSecured",
        "tpsp_site_isolation_enabled": "tpspSiteIsolationEnabled",
    },
)
class PolicyDeviceAssuranceChromeosConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        tpsp_allow_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_browser_version: typing.Optional[builtins.str] = None,
        tpsp_builtin_dns_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_chrome_remote_desktop_app_blocked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_device_enrollment_domain: typing.Optional[builtins.str] = None,
        tpsp_disk_encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_key_trust_level: typing.Optional[builtins.str] = None,
        tpsp_os_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_os_version: typing.Optional[builtins.str] = None,
        tpsp_password_proctection_warning_trigger: typing.Optional[builtins.str] = None,
        tpsp_realtime_url_check_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_safe_browsing_protection_level: typing.Optional[builtins.str] = None,
        tpsp_screen_lock_secured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_site_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Policy device assurance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#name PolicyDeviceAssuranceChromeos#name}
        :param tpsp_allow_screen_lock: Third party signal provider allow screen lock. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_allow_screen_lock PolicyDeviceAssuranceChromeos#tpsp_allow_screen_lock}
        :param tpsp_browser_version: Third party signal provider minimum browser version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_browser_version PolicyDeviceAssuranceChromeos#tpsp_browser_version}
        :param tpsp_builtin_dns_client_enabled: Third party signal provider builtin dns client enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_builtin_dns_client_enabled PolicyDeviceAssuranceChromeos#tpsp_builtin_dns_client_enabled}
        :param tpsp_chrome_remote_desktop_app_blocked: Third party signal provider chrome remote desktop app blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_chrome_remote_desktop_app_blocked PolicyDeviceAssuranceChromeos#tpsp_chrome_remote_desktop_app_blocked}
        :param tpsp_device_enrollment_domain: Third party signal provider device enrollment domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_device_enrollment_domain PolicyDeviceAssuranceChromeos#tpsp_device_enrollment_domain}
        :param tpsp_disk_encrypted: Third party signal provider disk encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_disk_encrypted PolicyDeviceAssuranceChromeos#tpsp_disk_encrypted}
        :param tpsp_key_trust_level: Third party signal provider key trust level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_key_trust_level PolicyDeviceAssuranceChromeos#tpsp_key_trust_level}
        :param tpsp_os_firewall: Third party signal provider os firewall. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_os_firewall PolicyDeviceAssuranceChromeos#tpsp_os_firewall}
        :param tpsp_os_version: Third party signal provider minimum os version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_os_version PolicyDeviceAssuranceChromeos#tpsp_os_version}
        :param tpsp_password_proctection_warning_trigger: Third party signal provider password protection warning trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_password_proctection_warning_trigger PolicyDeviceAssuranceChromeos#tpsp_password_proctection_warning_trigger}
        :param tpsp_realtime_url_check_mode: Third party signal provider realtime url check mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_realtime_url_check_mode PolicyDeviceAssuranceChromeos#tpsp_realtime_url_check_mode}
        :param tpsp_safe_browsing_protection_level: Third party signal provider safe browsing protection level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_safe_browsing_protection_level PolicyDeviceAssuranceChromeos#tpsp_safe_browsing_protection_level}
        :param tpsp_screen_lock_secured: Third party signal provider screen lock secure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_screen_lock_secured PolicyDeviceAssuranceChromeos#tpsp_screen_lock_secured}
        :param tpsp_site_isolation_enabled: Third party signal provider site isolation enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_site_isolation_enabled PolicyDeviceAssuranceChromeos#tpsp_site_isolation_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1923f82cb5d36baa2d0eec88799ac38a5fbaac17b4b134bf711f2326f91f2ec1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tpsp_allow_screen_lock", value=tpsp_allow_screen_lock, expected_type=type_hints["tpsp_allow_screen_lock"])
            check_type(argname="argument tpsp_browser_version", value=tpsp_browser_version, expected_type=type_hints["tpsp_browser_version"])
            check_type(argname="argument tpsp_builtin_dns_client_enabled", value=tpsp_builtin_dns_client_enabled, expected_type=type_hints["tpsp_builtin_dns_client_enabled"])
            check_type(argname="argument tpsp_chrome_remote_desktop_app_blocked", value=tpsp_chrome_remote_desktop_app_blocked, expected_type=type_hints["tpsp_chrome_remote_desktop_app_blocked"])
            check_type(argname="argument tpsp_device_enrollment_domain", value=tpsp_device_enrollment_domain, expected_type=type_hints["tpsp_device_enrollment_domain"])
            check_type(argname="argument tpsp_disk_encrypted", value=tpsp_disk_encrypted, expected_type=type_hints["tpsp_disk_encrypted"])
            check_type(argname="argument tpsp_key_trust_level", value=tpsp_key_trust_level, expected_type=type_hints["tpsp_key_trust_level"])
            check_type(argname="argument tpsp_os_firewall", value=tpsp_os_firewall, expected_type=type_hints["tpsp_os_firewall"])
            check_type(argname="argument tpsp_os_version", value=tpsp_os_version, expected_type=type_hints["tpsp_os_version"])
            check_type(argname="argument tpsp_password_proctection_warning_trigger", value=tpsp_password_proctection_warning_trigger, expected_type=type_hints["tpsp_password_proctection_warning_trigger"])
            check_type(argname="argument tpsp_realtime_url_check_mode", value=tpsp_realtime_url_check_mode, expected_type=type_hints["tpsp_realtime_url_check_mode"])
            check_type(argname="argument tpsp_safe_browsing_protection_level", value=tpsp_safe_browsing_protection_level, expected_type=type_hints["tpsp_safe_browsing_protection_level"])
            check_type(argname="argument tpsp_screen_lock_secured", value=tpsp_screen_lock_secured, expected_type=type_hints["tpsp_screen_lock_secured"])
            check_type(argname="argument tpsp_site_isolation_enabled", value=tpsp_site_isolation_enabled, expected_type=type_hints["tpsp_site_isolation_enabled"])
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
        if tpsp_allow_screen_lock is not None:
            self._values["tpsp_allow_screen_lock"] = tpsp_allow_screen_lock
        if tpsp_browser_version is not None:
            self._values["tpsp_browser_version"] = tpsp_browser_version
        if tpsp_builtin_dns_client_enabled is not None:
            self._values["tpsp_builtin_dns_client_enabled"] = tpsp_builtin_dns_client_enabled
        if tpsp_chrome_remote_desktop_app_blocked is not None:
            self._values["tpsp_chrome_remote_desktop_app_blocked"] = tpsp_chrome_remote_desktop_app_blocked
        if tpsp_device_enrollment_domain is not None:
            self._values["tpsp_device_enrollment_domain"] = tpsp_device_enrollment_domain
        if tpsp_disk_encrypted is not None:
            self._values["tpsp_disk_encrypted"] = tpsp_disk_encrypted
        if tpsp_key_trust_level is not None:
            self._values["tpsp_key_trust_level"] = tpsp_key_trust_level
        if tpsp_os_firewall is not None:
            self._values["tpsp_os_firewall"] = tpsp_os_firewall
        if tpsp_os_version is not None:
            self._values["tpsp_os_version"] = tpsp_os_version
        if tpsp_password_proctection_warning_trigger is not None:
            self._values["tpsp_password_proctection_warning_trigger"] = tpsp_password_proctection_warning_trigger
        if tpsp_realtime_url_check_mode is not None:
            self._values["tpsp_realtime_url_check_mode"] = tpsp_realtime_url_check_mode
        if tpsp_safe_browsing_protection_level is not None:
            self._values["tpsp_safe_browsing_protection_level"] = tpsp_safe_browsing_protection_level
        if tpsp_screen_lock_secured is not None:
            self._values["tpsp_screen_lock_secured"] = tpsp_screen_lock_secured
        if tpsp_site_isolation_enabled is not None:
            self._values["tpsp_site_isolation_enabled"] = tpsp_site_isolation_enabled

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#name PolicyDeviceAssuranceChromeos#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tpsp_allow_screen_lock(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider allow screen lock.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_allow_screen_lock PolicyDeviceAssuranceChromeos#tpsp_allow_screen_lock}
        '''
        result = self._values.get("tpsp_allow_screen_lock")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_browser_version(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider minimum browser version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_browser_version PolicyDeviceAssuranceChromeos#tpsp_browser_version}
        '''
        result = self._values.get("tpsp_browser_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_builtin_dns_client_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider builtin dns client enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_builtin_dns_client_enabled PolicyDeviceAssuranceChromeos#tpsp_builtin_dns_client_enabled}
        '''
        result = self._values.get("tpsp_builtin_dns_client_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_chrome_remote_desktop_app_blocked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider chrome remote desktop app blocked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_chrome_remote_desktop_app_blocked PolicyDeviceAssuranceChromeos#tpsp_chrome_remote_desktop_app_blocked}
        '''
        result = self._values.get("tpsp_chrome_remote_desktop_app_blocked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_device_enrollment_domain(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider device enrollment domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_device_enrollment_domain PolicyDeviceAssuranceChromeos#tpsp_device_enrollment_domain}
        '''
        result = self._values.get("tpsp_device_enrollment_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_disk_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider disk encrypted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_disk_encrypted PolicyDeviceAssuranceChromeos#tpsp_disk_encrypted}
        '''
        result = self._values.get("tpsp_disk_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_key_trust_level(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider key trust level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_key_trust_level PolicyDeviceAssuranceChromeos#tpsp_key_trust_level}
        '''
        result = self._values.get("tpsp_key_trust_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_os_firewall(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider os firewall.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_os_firewall PolicyDeviceAssuranceChromeos#tpsp_os_firewall}
        '''
        result = self._values.get("tpsp_os_firewall")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_os_version(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider minimum os version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_os_version PolicyDeviceAssuranceChromeos#tpsp_os_version}
        '''
        result = self._values.get("tpsp_os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_password_proctection_warning_trigger(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Third party signal provider password protection warning trigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_password_proctection_warning_trigger PolicyDeviceAssuranceChromeos#tpsp_password_proctection_warning_trigger}
        '''
        result = self._values.get("tpsp_password_proctection_warning_trigger")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_realtime_url_check_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider realtime url check mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_realtime_url_check_mode PolicyDeviceAssuranceChromeos#tpsp_realtime_url_check_mode}
        '''
        result = self._values.get("tpsp_realtime_url_check_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_safe_browsing_protection_level(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider safe browsing protection level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_safe_browsing_protection_level PolicyDeviceAssuranceChromeos#tpsp_safe_browsing_protection_level}
        '''
        result = self._values.get("tpsp_safe_browsing_protection_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_screen_lock_secured(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider screen lock secure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_screen_lock_secured PolicyDeviceAssuranceChromeos#tpsp_screen_lock_secured}
        '''
        result = self._values.get("tpsp_screen_lock_secured")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_site_isolation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider site isolation enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_chromeos#tpsp_site_isolation_enabled PolicyDeviceAssuranceChromeos#tpsp_site_isolation_enabled}
        '''
        result = self._values.get("tpsp_site_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyDeviceAssuranceChromeosConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PolicyDeviceAssuranceChromeos",
    "PolicyDeviceAssuranceChromeosConfig",
]

publication.publish()

def _typecheckingstub__0d5edc4180359f03dc7c8142fa34acac3bc859b3261073381dcd6233c0397073(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    tpsp_allow_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_browser_version: typing.Optional[builtins.str] = None,
    tpsp_builtin_dns_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_chrome_remote_desktop_app_blocked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_device_enrollment_domain: typing.Optional[builtins.str] = None,
    tpsp_disk_encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_key_trust_level: typing.Optional[builtins.str] = None,
    tpsp_os_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_os_version: typing.Optional[builtins.str] = None,
    tpsp_password_proctection_warning_trigger: typing.Optional[builtins.str] = None,
    tpsp_realtime_url_check_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_safe_browsing_protection_level: typing.Optional[builtins.str] = None,
    tpsp_screen_lock_secured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_site_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__293a950432a0ae1b274359a5abd18ec3940358e0b958478f9d8f0b74c7474952(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ffe4c7b36545131d8d81f0c269f2b423cf36c2e402d7ceddd49a71509d7e90(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e57563d920d9df37cfff248c90da1117b1bbdcf69d18fedbcf5456c08155c51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0fad50397873a7e75fda04c28b27a08abf427ab0e55d0fd4776a0ccd643d07(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477bccdfd19de9f4995754f88258f99f74656d92490973bdf809b8b12738c164(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ecd678d3c6fb360f99daf7581c9115ac1c1b9f2d171f496eb55b9a69adb34a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1fa3c0e3075af6167cb9c070c50bc3b368c1f3ffb3913ba86efec67731d2eb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d9b0d6a6dc8f5780c93497038c35ebd084555d9c8b187eabde54fd3eb9d8d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73886567046867ac198ad2d4b69bb6b444e87e8937a14ddf1c3b49ebe74dddb3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d328a4a59baffeb5e45629ac8f2cdc8d0b15d304e484b4a7d7b63dedc53e50fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb0c781248345346fc6b0927a6255815ac7de97a690deae18748d4b007255d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d220c3aa072d3a5ece4fc00c5756f70652a5c3819daed390716ddcedb621da8c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36445b445525a5856c8dd65a4430874a2f5205290ffa04444332f7527f9c7435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489809f8c0ca5279ce1a6222d9e199d64ec2c40d4cc3d93d9c16e26d3a699a9c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85965af01c687fa3ee83e889e4303961e118806a9fbbe55aa49769766f83f8af(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1923f82cb5d36baa2d0eec88799ac38a5fbaac17b4b134bf711f2326f91f2ec1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    tpsp_allow_screen_lock: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_browser_version: typing.Optional[builtins.str] = None,
    tpsp_builtin_dns_client_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_chrome_remote_desktop_app_blocked: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_device_enrollment_domain: typing.Optional[builtins.str] = None,
    tpsp_disk_encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_key_trust_level: typing.Optional[builtins.str] = None,
    tpsp_os_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_os_version: typing.Optional[builtins.str] = None,
    tpsp_password_proctection_warning_trigger: typing.Optional[builtins.str] = None,
    tpsp_realtime_url_check_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_safe_browsing_protection_level: typing.Optional[builtins.str] = None,
    tpsp_screen_lock_secured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_site_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
