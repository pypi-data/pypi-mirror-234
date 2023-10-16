'''
# `okta_policy_device_assurance_macos`

Refer to the Terraform Registory for docs: [`okta_policy_device_assurance_macos`](https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos).
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


class PolicyDeviceAssuranceMacos(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyDeviceAssuranceMacos.PolicyDeviceAssuranceMacos",
):
    '''Represents a {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos okta_policy_device_assurance_macos}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        disk_encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_version: typing.Optional[builtins.str] = None,
        screenlock_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        secure_hardware_present: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        third_party_signal_providers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos okta_policy_device_assurance_macos} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Policy device assurance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#name PolicyDeviceAssuranceMacos#name}
        :param disk_encryption_type: List of disk encryption type, can be ALL_INTERNAL_VOLUMES. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#disk_encryption_type PolicyDeviceAssuranceMacos#disk_encryption_type}
        :param os_version: The device os minimum version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#os_version PolicyDeviceAssuranceMacos#os_version}
        :param screenlock_type: List of screenlock type, can be BIOMETRIC or BIOMETRIC, PASSCODE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#screenlock_type PolicyDeviceAssuranceMacos#screenlock_type}
        :param secure_hardware_present: Indicates if the device constains a secure hardware functionality. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#secure_hardware_present PolicyDeviceAssuranceMacos#secure_hardware_present}
        :param third_party_signal_providers: Check to include third party signal provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#third_party_signal_providers PolicyDeviceAssuranceMacos#third_party_signal_providers}
        :param tpsp_browser_version: Third party signal provider minimum browser version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_browser_version PolicyDeviceAssuranceMacos#tpsp_browser_version}
        :param tpsp_builtin_dns_client_enabled: Third party signal provider builtin dns client enable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_builtin_dns_client_enabled PolicyDeviceAssuranceMacos#tpsp_builtin_dns_client_enabled}
        :param tpsp_chrome_remote_desktop_app_blocked: Third party signal provider chrome remote desktop app blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_chrome_remote_desktop_app_blocked PolicyDeviceAssuranceMacos#tpsp_chrome_remote_desktop_app_blocked}
        :param tpsp_device_enrollment_domain: Third party signal provider device enrollment domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_device_enrollment_domain PolicyDeviceAssuranceMacos#tpsp_device_enrollment_domain}
        :param tpsp_disk_encrypted: Third party signal provider disk encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_disk_encrypted PolicyDeviceAssuranceMacos#tpsp_disk_encrypted}
        :param tpsp_key_trust_level: Third party signal provider key trust level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_key_trust_level PolicyDeviceAssuranceMacos#tpsp_key_trust_level}
        :param tpsp_os_firewall: Third party signal provider os firewall. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_os_firewall PolicyDeviceAssuranceMacos#tpsp_os_firewall}
        :param tpsp_os_version: Third party signal provider minimum os version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_os_version PolicyDeviceAssuranceMacos#tpsp_os_version}
        :param tpsp_password_proctection_warning_trigger: Third party signal provider password protection warning trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_password_proctection_warning_trigger PolicyDeviceAssuranceMacos#tpsp_password_proctection_warning_trigger}
        :param tpsp_realtime_url_check_mode: Third party signal provider realtime url check mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_realtime_url_check_mode PolicyDeviceAssuranceMacos#tpsp_realtime_url_check_mode}
        :param tpsp_safe_browsing_protection_level: Third party signal provider safe browsing protection level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_safe_browsing_protection_level PolicyDeviceAssuranceMacos#tpsp_safe_browsing_protection_level}
        :param tpsp_screen_lock_secured: Third party signal provider screen lock secure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_screen_lock_secured PolicyDeviceAssuranceMacos#tpsp_screen_lock_secured}
        :param tpsp_site_isolation_enabled: Third party signal provider site isolation enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_site_isolation_enabled PolicyDeviceAssuranceMacos#tpsp_site_isolation_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7a68428a775906dbca1da81da51e4f6cdfe0e8476cbb8ea17903f4e1fda8b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = PolicyDeviceAssuranceMacosConfig(
            name=name,
            disk_encryption_type=disk_encryption_type,
            os_version=os_version,
            screenlock_type=screenlock_type,
            secure_hardware_present=secure_hardware_present,
            third_party_signal_providers=third_party_signal_providers,
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

    @jsii.member(jsii_name="resetDiskEncryptionType")
    def reset_disk_encryption_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskEncryptionType", []))

    @jsii.member(jsii_name="resetOsVersion")
    def reset_os_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsVersion", []))

    @jsii.member(jsii_name="resetScreenlockType")
    def reset_screenlock_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScreenlockType", []))

    @jsii.member(jsii_name="resetSecureHardwarePresent")
    def reset_secure_hardware_present(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecureHardwarePresent", []))

    @jsii.member(jsii_name="resetThirdPartySignalProviders")
    def reset_third_party_signal_providers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThirdPartySignalProviders", []))

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
    @jsii.member(jsii_name="diskEncryptionTypeInput")
    def disk_encryption_type_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "diskEncryptionTypeInput"))

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
    @jsii.member(jsii_name="secureHardwarePresentInput")
    def secure_hardware_present_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secureHardwarePresentInput"))

    @builtins.property
    @jsii.member(jsii_name="thirdPartySignalProvidersInput")
    def third_party_signal_providers_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "thirdPartySignalProvidersInput"))

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
    @jsii.member(jsii_name="diskEncryptionType")
    def disk_encryption_type(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "diskEncryptionType"))

    @disk_encryption_type.setter
    def disk_encryption_type(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02288f05f99ae1d270a384f742522e1e588593367b248d9cf6686e00526df85a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b9eb8a22f5a7159ba97bdc969d9d9f73648f6c433f29ff1ddc74be41a7cf3ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d766f6a9cf6bbeaa109f4e01ffd859b5e2f88b2a4ff0837517b4e54a3b33c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value)

    @builtins.property
    @jsii.member(jsii_name="screenlockType")
    def screenlock_type(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "screenlockType"))

    @screenlock_type.setter
    def screenlock_type(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e0c0f1f400d4c55b120e80725ee73a046fc45a6abc573a233865ec949e1a20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "screenlockType", value)

    @builtins.property
    @jsii.member(jsii_name="secureHardwarePresent")
    def secure_hardware_present(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secureHardwarePresent"))

    @secure_hardware_present.setter
    def secure_hardware_present(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494bc357b4c06c759679d0862f15e3c4f03b962e3819a510ae55abb151c13145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secureHardwarePresent", value)

    @builtins.property
    @jsii.member(jsii_name="thirdPartySignalProviders")
    def third_party_signal_providers(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "thirdPartySignalProviders"))

    @third_party_signal_providers.setter
    def third_party_signal_providers(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7846715be966980f0857924a5c7197b29b49f943f6b815074ba05f82c2c1fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thirdPartySignalProviders", value)

    @builtins.property
    @jsii.member(jsii_name="tpspBrowserVersion")
    def tpsp_browser_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspBrowserVersion"))

    @tpsp_browser_version.setter
    def tpsp_browser_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88913f0f9636ee685fdfd90c708d850c84b7b14c14f872f228e75afe90a5f74d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1b87f2db1cdd0369865688c298592a3752e49d86e920d4dfb695f17647c4d97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54b936a5c1425a3100374994f5100a86b92f963db88efccf98cbb496974c7ca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspChromeRemoteDesktopAppBlocked", value)

    @builtins.property
    @jsii.member(jsii_name="tpspDeviceEnrollmentDomain")
    def tpsp_device_enrollment_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspDeviceEnrollmentDomain"))

    @tpsp_device_enrollment_domain.setter
    def tpsp_device_enrollment_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94583417d5cc729b9f1b173e8b03ff9bf49356ff8cbad9b817b16af063547c6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f09f0a7741d44c9ba8589c8a71b2281a19ab925926eed7e1e8c4474841d42318)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspDiskEncrypted", value)

    @builtins.property
    @jsii.member(jsii_name="tpspKeyTrustLevel")
    def tpsp_key_trust_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspKeyTrustLevel"))

    @tpsp_key_trust_level.setter
    def tpsp_key_trust_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2628b83c84fbd723b35c8fb369ce30bd1aeb267a66fda9bf538fe6b250889aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb58cfdd42a436baaee2984acb54c57c5ab559c401d9044750d54a9ec95795e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspOsFirewall", value)

    @builtins.property
    @jsii.member(jsii_name="tpspOsVersion")
    def tpsp_os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspOsVersion"))

    @tpsp_os_version.setter
    def tpsp_os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a790d930772dd461b4370aef7c624d8c34f2e516e50ac47a43fcede49e2915ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspOsVersion", value)

    @builtins.property
    @jsii.member(jsii_name="tpspPasswordProctectionWarningTrigger")
    def tpsp_password_proctection_warning_trigger(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspPasswordProctectionWarningTrigger"))

    @tpsp_password_proctection_warning_trigger.setter
    def tpsp_password_proctection_warning_trigger(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce336722541cdcfd5c615502eaffb4884c5bf5bda3af22276dc6f7701a0e067)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a0f0b332328291647fd8176e646eaa038f7c3dc00459ace647f466370009b18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspRealtimeUrlCheckMode", value)

    @builtins.property
    @jsii.member(jsii_name="tpspSafeBrowsingProtectionLevel")
    def tpsp_safe_browsing_protection_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspSafeBrowsingProtectionLevel"))

    @tpsp_safe_browsing_protection_level.setter
    def tpsp_safe_browsing_protection_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa041e626bc41891018fa3eb9a092a58842b69f57bd80b28b0a977fdfb045b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2f7d40bd72efcf49173581e8f1a08e15df1bd40b02f9757534b4f8d55950e9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b97ac32961c5fbbfbfc5bee06e8a0ea3e842934dd9ff3dddcb6de46538272fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspSiteIsolationEnabled", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyDeviceAssuranceMacos.PolicyDeviceAssuranceMacosConfig",
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
        "disk_encryption_type": "diskEncryptionType",
        "os_version": "osVersion",
        "screenlock_type": "screenlockType",
        "secure_hardware_present": "secureHardwarePresent",
        "third_party_signal_providers": "thirdPartySignalProviders",
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
class PolicyDeviceAssuranceMacosConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        disk_encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        os_version: typing.Optional[builtins.str] = None,
        screenlock_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        secure_hardware_present: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        third_party_signal_providers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        :param name: Policy device assurance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#name PolicyDeviceAssuranceMacos#name}
        :param disk_encryption_type: List of disk encryption type, can be ALL_INTERNAL_VOLUMES. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#disk_encryption_type PolicyDeviceAssuranceMacos#disk_encryption_type}
        :param os_version: The device os minimum version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#os_version PolicyDeviceAssuranceMacos#os_version}
        :param screenlock_type: List of screenlock type, can be BIOMETRIC or BIOMETRIC, PASSCODE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#screenlock_type PolicyDeviceAssuranceMacos#screenlock_type}
        :param secure_hardware_present: Indicates if the device constains a secure hardware functionality. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#secure_hardware_present PolicyDeviceAssuranceMacos#secure_hardware_present}
        :param third_party_signal_providers: Check to include third party signal provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#third_party_signal_providers PolicyDeviceAssuranceMacos#third_party_signal_providers}
        :param tpsp_browser_version: Third party signal provider minimum browser version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_browser_version PolicyDeviceAssuranceMacos#tpsp_browser_version}
        :param tpsp_builtin_dns_client_enabled: Third party signal provider builtin dns client enable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_builtin_dns_client_enabled PolicyDeviceAssuranceMacos#tpsp_builtin_dns_client_enabled}
        :param tpsp_chrome_remote_desktop_app_blocked: Third party signal provider chrome remote desktop app blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_chrome_remote_desktop_app_blocked PolicyDeviceAssuranceMacos#tpsp_chrome_remote_desktop_app_blocked}
        :param tpsp_device_enrollment_domain: Third party signal provider device enrollment domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_device_enrollment_domain PolicyDeviceAssuranceMacos#tpsp_device_enrollment_domain}
        :param tpsp_disk_encrypted: Third party signal provider disk encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_disk_encrypted PolicyDeviceAssuranceMacos#tpsp_disk_encrypted}
        :param tpsp_key_trust_level: Third party signal provider key trust level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_key_trust_level PolicyDeviceAssuranceMacos#tpsp_key_trust_level}
        :param tpsp_os_firewall: Third party signal provider os firewall. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_os_firewall PolicyDeviceAssuranceMacos#tpsp_os_firewall}
        :param tpsp_os_version: Third party signal provider minimum os version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_os_version PolicyDeviceAssuranceMacos#tpsp_os_version}
        :param tpsp_password_proctection_warning_trigger: Third party signal provider password protection warning trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_password_proctection_warning_trigger PolicyDeviceAssuranceMacos#tpsp_password_proctection_warning_trigger}
        :param tpsp_realtime_url_check_mode: Third party signal provider realtime url check mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_realtime_url_check_mode PolicyDeviceAssuranceMacos#tpsp_realtime_url_check_mode}
        :param tpsp_safe_browsing_protection_level: Third party signal provider safe browsing protection level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_safe_browsing_protection_level PolicyDeviceAssuranceMacos#tpsp_safe_browsing_protection_level}
        :param tpsp_screen_lock_secured: Third party signal provider screen lock secure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_screen_lock_secured PolicyDeviceAssuranceMacos#tpsp_screen_lock_secured}
        :param tpsp_site_isolation_enabled: Third party signal provider site isolation enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_site_isolation_enabled PolicyDeviceAssuranceMacos#tpsp_site_isolation_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe352167ae14e653028ab529c21f6ac90911783785ba483fc2a15095b0965a7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument disk_encryption_type", value=disk_encryption_type, expected_type=type_hints["disk_encryption_type"])
            check_type(argname="argument os_version", value=os_version, expected_type=type_hints["os_version"])
            check_type(argname="argument screenlock_type", value=screenlock_type, expected_type=type_hints["screenlock_type"])
            check_type(argname="argument secure_hardware_present", value=secure_hardware_present, expected_type=type_hints["secure_hardware_present"])
            check_type(argname="argument third_party_signal_providers", value=third_party_signal_providers, expected_type=type_hints["third_party_signal_providers"])
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
        if disk_encryption_type is not None:
            self._values["disk_encryption_type"] = disk_encryption_type
        if os_version is not None:
            self._values["os_version"] = os_version
        if screenlock_type is not None:
            self._values["screenlock_type"] = screenlock_type
        if secure_hardware_present is not None:
            self._values["secure_hardware_present"] = secure_hardware_present
        if third_party_signal_providers is not None:
            self._values["third_party_signal_providers"] = third_party_signal_providers
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#name PolicyDeviceAssuranceMacos#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_encryption_type(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of disk encryption type, can be ALL_INTERNAL_VOLUMES.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#disk_encryption_type PolicyDeviceAssuranceMacos#disk_encryption_type}
        '''
        result = self._values.get("disk_encryption_type")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def os_version(self) -> typing.Optional[builtins.str]:
        '''The device os minimum version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#os_version PolicyDeviceAssuranceMacos#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def screenlock_type(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of screenlock type, can be BIOMETRIC or BIOMETRIC, PASSCODE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#screenlock_type PolicyDeviceAssuranceMacos#screenlock_type}
        '''
        result = self._values.get("screenlock_type")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secure_hardware_present(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if the device constains a secure hardware functionality.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#secure_hardware_present PolicyDeviceAssuranceMacos#secure_hardware_present}
        '''
        result = self._values.get("secure_hardware_present")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def third_party_signal_providers(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Check to include third party signal provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#third_party_signal_providers PolicyDeviceAssuranceMacos#third_party_signal_providers}
        '''
        result = self._values.get("third_party_signal_providers")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_browser_version(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider minimum browser version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_browser_version PolicyDeviceAssuranceMacos#tpsp_browser_version}
        '''
        result = self._values.get("tpsp_browser_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_builtin_dns_client_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider builtin dns client enable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_builtin_dns_client_enabled PolicyDeviceAssuranceMacos#tpsp_builtin_dns_client_enabled}
        '''
        result = self._values.get("tpsp_builtin_dns_client_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_chrome_remote_desktop_app_blocked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider chrome remote desktop app blocked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_chrome_remote_desktop_app_blocked PolicyDeviceAssuranceMacos#tpsp_chrome_remote_desktop_app_blocked}
        '''
        result = self._values.get("tpsp_chrome_remote_desktop_app_blocked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_device_enrollment_domain(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider device enrollment domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_device_enrollment_domain PolicyDeviceAssuranceMacos#tpsp_device_enrollment_domain}
        '''
        result = self._values.get("tpsp_device_enrollment_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_disk_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider disk encrypted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_disk_encrypted PolicyDeviceAssuranceMacos#tpsp_disk_encrypted}
        '''
        result = self._values.get("tpsp_disk_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_key_trust_level(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider key trust level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_key_trust_level PolicyDeviceAssuranceMacos#tpsp_key_trust_level}
        '''
        result = self._values.get("tpsp_key_trust_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_os_firewall(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider os firewall.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_os_firewall PolicyDeviceAssuranceMacos#tpsp_os_firewall}
        '''
        result = self._values.get("tpsp_os_firewall")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_os_version(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider minimum os version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_os_version PolicyDeviceAssuranceMacos#tpsp_os_version}
        '''
        result = self._values.get("tpsp_os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_password_proctection_warning_trigger(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Third party signal provider password protection warning trigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_password_proctection_warning_trigger PolicyDeviceAssuranceMacos#tpsp_password_proctection_warning_trigger}
        '''
        result = self._values.get("tpsp_password_proctection_warning_trigger")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_realtime_url_check_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider realtime url check mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_realtime_url_check_mode PolicyDeviceAssuranceMacos#tpsp_realtime_url_check_mode}
        '''
        result = self._values.get("tpsp_realtime_url_check_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_safe_browsing_protection_level(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider safe browsing protection level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_safe_browsing_protection_level PolicyDeviceAssuranceMacos#tpsp_safe_browsing_protection_level}
        '''
        result = self._values.get("tpsp_safe_browsing_protection_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_screen_lock_secured(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider screen lock secure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_screen_lock_secured PolicyDeviceAssuranceMacos#tpsp_screen_lock_secured}
        '''
        result = self._values.get("tpsp_screen_lock_secured")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_site_isolation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider site isolation enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_macos#tpsp_site_isolation_enabled PolicyDeviceAssuranceMacos#tpsp_site_isolation_enabled}
        '''
        result = self._values.get("tpsp_site_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyDeviceAssuranceMacosConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PolicyDeviceAssuranceMacos",
    "PolicyDeviceAssuranceMacosConfig",
]

publication.publish()

def _typecheckingstub__8f7a68428a775906dbca1da81da51e4f6cdfe0e8476cbb8ea17903f4e1fda8b8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    disk_encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    os_version: typing.Optional[builtins.str] = None,
    screenlock_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    secure_hardware_present: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    third_party_signal_providers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__02288f05f99ae1d270a384f742522e1e588593367b248d9cf6686e00526df85a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b9eb8a22f5a7159ba97bdc969d9d9f73648f6c433f29ff1ddc74be41a7cf3ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d766f6a9cf6bbeaa109f4e01ffd859b5e2f88b2a4ff0837517b4e54a3b33c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e0c0f1f400d4c55b120e80725ee73a046fc45a6abc573a233865ec949e1a20(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494bc357b4c06c759679d0862f15e3c4f03b962e3819a510ae55abb151c13145(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7846715be966980f0857924a5c7197b29b49f943f6b815074ba05f82c2c1fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88913f0f9636ee685fdfd90c708d850c84b7b14c14f872f228e75afe90a5f74d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b87f2db1cdd0369865688c298592a3752e49d86e920d4dfb695f17647c4d97(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b936a5c1425a3100374994f5100a86b92f963db88efccf98cbb496974c7ca9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94583417d5cc729b9f1b173e8b03ff9bf49356ff8cbad9b817b16af063547c6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f09f0a7741d44c9ba8589c8a71b2281a19ab925926eed7e1e8c4474841d42318(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2628b83c84fbd723b35c8fb369ce30bd1aeb267a66fda9bf538fe6b250889aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb58cfdd42a436baaee2984acb54c57c5ab559c401d9044750d54a9ec95795e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a790d930772dd461b4370aef7c624d8c34f2e516e50ac47a43fcede49e2915ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce336722541cdcfd5c615502eaffb4884c5bf5bda3af22276dc6f7701a0e067(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0f0b332328291647fd8176e646eaa038f7c3dc00459ace647f466370009b18(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa041e626bc41891018fa3eb9a092a58842b69f57bd80b28b0a977fdfb045b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f7d40bd72efcf49173581e8f1a08e15df1bd40b02f9757534b4f8d55950e9f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b97ac32961c5fbbfbfc5bee06e8a0ea3e842934dd9ff3dddcb6de46538272fb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe352167ae14e653028ab529c21f6ac90911783785ba483fc2a15095b0965a7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    disk_encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    os_version: typing.Optional[builtins.str] = None,
    screenlock_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    secure_hardware_present: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    third_party_signal_providers: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
