'''
# `okta_policy_device_assurance_windows`

Refer to the Terraform Registory for docs: [`okta_policy_device_assurance_windows`](https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows).
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


class PolicyDeviceAssuranceWindows(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.policyDeviceAssuranceWindows.PolicyDeviceAssuranceWindows",
):
    '''Represents a {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows okta_policy_device_assurance_windows}.'''

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
        tpsp_crowd_strike_agent_id: typing.Optional[builtins.str] = None,
        tpsp_crowd_strike_customer_id: typing.Optional[builtins.str] = None,
        tpsp_device_enrollment_domain: typing.Optional[builtins.str] = None,
        tpsp_disk_encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_key_trust_level: typing.Optional[builtins.str] = None,
        tpsp_os_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_os_version: typing.Optional[builtins.str] = None,
        tpsp_password_proctection_warning_trigger: typing.Optional[builtins.str] = None,
        tpsp_realtime_url_check_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_safe_browsing_protection_level: typing.Optional[builtins.str] = None,
        tpsp_screen_lock_secured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_secure_boot_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_site_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_third_party_blocking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_windows_machine_domain: typing.Optional[builtins.str] = None,
        tpsp_windows_user_domain: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows okta_policy_device_assurance_windows} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Policy device assurance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#name PolicyDeviceAssuranceWindows#name}
        :param disk_encryption_type: List of disk encryption type, can be ALL_INTERNAL_VOLUMES. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#disk_encryption_type PolicyDeviceAssuranceWindows#disk_encryption_type}
        :param os_version: The device os minimum version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#os_version PolicyDeviceAssuranceWindows#os_version}
        :param screenlock_type: List of screenlock type, can be BIOMETRIC or BIOMETRIC, PASSCODE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#screenlock_type PolicyDeviceAssuranceWindows#screenlock_type}
        :param secure_hardware_present: Indicates if the device constains a secure hardware functionality. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#secure_hardware_present PolicyDeviceAssuranceWindows#secure_hardware_present}
        :param third_party_signal_providers: Check to include third party signal provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#third_party_signal_providers PolicyDeviceAssuranceWindows#third_party_signal_providers}
        :param tpsp_browser_version: Third party signal provider minimum browser version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_browser_version PolicyDeviceAssuranceWindows#tpsp_browser_version}
        :param tpsp_builtin_dns_client_enabled: Third party signal provider builtin dns client enable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_builtin_dns_client_enabled PolicyDeviceAssuranceWindows#tpsp_builtin_dns_client_enabled}
        :param tpsp_chrome_remote_desktop_app_blocked: Third party signal provider chrome remote desktop app blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_chrome_remote_desktop_app_blocked PolicyDeviceAssuranceWindows#tpsp_chrome_remote_desktop_app_blocked}
        :param tpsp_crowd_strike_agent_id: Third party signal provider crowdstrike agent id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_crowd_strike_agent_id PolicyDeviceAssuranceWindows#tpsp_crowd_strike_agent_id}
        :param tpsp_crowd_strike_customer_id: Third party signal provider crowdstrike user id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_crowd_strike_customer_id PolicyDeviceAssuranceWindows#tpsp_crowd_strike_customer_id}
        :param tpsp_device_enrollment_domain: Third party signal provider device enrollment domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_device_enrollment_domain PolicyDeviceAssuranceWindows#tpsp_device_enrollment_domain}
        :param tpsp_disk_encrypted: Third party signal provider disk encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_disk_encrypted PolicyDeviceAssuranceWindows#tpsp_disk_encrypted}
        :param tpsp_key_trust_level: Third party signal provider key trust level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_key_trust_level PolicyDeviceAssuranceWindows#tpsp_key_trust_level}
        :param tpsp_os_firewall: Third party signal provider os firewall. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_os_firewall PolicyDeviceAssuranceWindows#tpsp_os_firewall}
        :param tpsp_os_version: Third party signal provider minimum os version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_os_version PolicyDeviceAssuranceWindows#tpsp_os_version}
        :param tpsp_password_proctection_warning_trigger: Third party signal provider password protection warning trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_password_proctection_warning_trigger PolicyDeviceAssuranceWindows#tpsp_password_proctection_warning_trigger}
        :param tpsp_realtime_url_check_mode: Third party signal provider realtime url check mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_realtime_url_check_mode PolicyDeviceAssuranceWindows#tpsp_realtime_url_check_mode}
        :param tpsp_safe_browsing_protection_level: Third party signal provider safe browsing protection level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_safe_browsing_protection_level PolicyDeviceAssuranceWindows#tpsp_safe_browsing_protection_level}
        :param tpsp_screen_lock_secured: Third party signal provider screen lock secure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_screen_lock_secured PolicyDeviceAssuranceWindows#tpsp_screen_lock_secured}
        :param tpsp_secure_boot_enabled: Third party signal provider secure boot enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_secure_boot_enabled PolicyDeviceAssuranceWindows#tpsp_secure_boot_enabled}
        :param tpsp_site_isolation_enabled: Third party signal provider site isolation enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_site_isolation_enabled PolicyDeviceAssuranceWindows#tpsp_site_isolation_enabled}
        :param tpsp_third_party_blocking_enabled: Third party signal provider third party blocking enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_third_party_blocking_enabled PolicyDeviceAssuranceWindows#tpsp_third_party_blocking_enabled}
        :param tpsp_windows_machine_domain: Third party signal provider windows machine domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_windows_machine_domain PolicyDeviceAssuranceWindows#tpsp_windows_machine_domain}
        :param tpsp_windows_user_domain: Third party signal provider windows user domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_windows_user_domain PolicyDeviceAssuranceWindows#tpsp_windows_user_domain}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7d91786850b20bc9873e0b9431fe03752e5fac73991d710d1c96efbcf956b7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = PolicyDeviceAssuranceWindowsConfig(
            name=name,
            disk_encryption_type=disk_encryption_type,
            os_version=os_version,
            screenlock_type=screenlock_type,
            secure_hardware_present=secure_hardware_present,
            third_party_signal_providers=third_party_signal_providers,
            tpsp_browser_version=tpsp_browser_version,
            tpsp_builtin_dns_client_enabled=tpsp_builtin_dns_client_enabled,
            tpsp_chrome_remote_desktop_app_blocked=tpsp_chrome_remote_desktop_app_blocked,
            tpsp_crowd_strike_agent_id=tpsp_crowd_strike_agent_id,
            tpsp_crowd_strike_customer_id=tpsp_crowd_strike_customer_id,
            tpsp_device_enrollment_domain=tpsp_device_enrollment_domain,
            tpsp_disk_encrypted=tpsp_disk_encrypted,
            tpsp_key_trust_level=tpsp_key_trust_level,
            tpsp_os_firewall=tpsp_os_firewall,
            tpsp_os_version=tpsp_os_version,
            tpsp_password_proctection_warning_trigger=tpsp_password_proctection_warning_trigger,
            tpsp_realtime_url_check_mode=tpsp_realtime_url_check_mode,
            tpsp_safe_browsing_protection_level=tpsp_safe_browsing_protection_level,
            tpsp_screen_lock_secured=tpsp_screen_lock_secured,
            tpsp_secure_boot_enabled=tpsp_secure_boot_enabled,
            tpsp_site_isolation_enabled=tpsp_site_isolation_enabled,
            tpsp_third_party_blocking_enabled=tpsp_third_party_blocking_enabled,
            tpsp_windows_machine_domain=tpsp_windows_machine_domain,
            tpsp_windows_user_domain=tpsp_windows_user_domain,
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

    @jsii.member(jsii_name="resetTpspCrowdStrikeAgentId")
    def reset_tpsp_crowd_strike_agent_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspCrowdStrikeAgentId", []))

    @jsii.member(jsii_name="resetTpspCrowdStrikeCustomerId")
    def reset_tpsp_crowd_strike_customer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspCrowdStrikeCustomerId", []))

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

    @jsii.member(jsii_name="resetTpspSecureBootEnabled")
    def reset_tpsp_secure_boot_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspSecureBootEnabled", []))

    @jsii.member(jsii_name="resetTpspSiteIsolationEnabled")
    def reset_tpsp_site_isolation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspSiteIsolationEnabled", []))

    @jsii.member(jsii_name="resetTpspThirdPartyBlockingEnabled")
    def reset_tpsp_third_party_blocking_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspThirdPartyBlockingEnabled", []))

    @jsii.member(jsii_name="resetTpspWindowsMachineDomain")
    def reset_tpsp_windows_machine_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspWindowsMachineDomain", []))

    @jsii.member(jsii_name="resetTpspWindowsUserDomain")
    def reset_tpsp_windows_user_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTpspWindowsUserDomain", []))

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
    @jsii.member(jsii_name="tpspCrowdStrikeAgentIdInput")
    def tpsp_crowd_strike_agent_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpspCrowdStrikeAgentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspCrowdStrikeCustomerIdInput")
    def tpsp_crowd_strike_customer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpspCrowdStrikeCustomerIdInput"))

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
    @jsii.member(jsii_name="tpspSecureBootEnabledInput")
    def tpsp_secure_boot_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tpspSecureBootEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspSiteIsolationEnabledInput")
    def tpsp_site_isolation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tpspSiteIsolationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspThirdPartyBlockingEnabledInput")
    def tpsp_third_party_blocking_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tpspThirdPartyBlockingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspWindowsMachineDomainInput")
    def tpsp_windows_machine_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpspWindowsMachineDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="tpspWindowsUserDomainInput")
    def tpsp_windows_user_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tpspWindowsUserDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="diskEncryptionType")
    def disk_encryption_type(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "diskEncryptionType"))

    @disk_encryption_type.setter
    def disk_encryption_type(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6886d3904f2651d8238535803d05b62e14fc1db8569fdd4697d5e28c7b35d2cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskEncryptionType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574476e2fe9e360b71afb47ffbbd526349e398e8d9ea3ada25d42348ca15b338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__771c761a7ebecdbe4c73e24429b02a50e1c62c2a226f6812689e749fa36b4b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value)

    @builtins.property
    @jsii.member(jsii_name="screenlockType")
    def screenlock_type(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "screenlockType"))

    @screenlock_type.setter
    def screenlock_type(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62de61f4c100642b8d578ecf81981724c4e98ed1b3283460d67ace8f3fa39063)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c361952024ad4fff4e2bacbc967936fa100569bd12f1ab4325843a2e2e0e2feb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0914459a2374dabef440ceb05bd7439a133a95196c3c1a31c8f848b522f25638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thirdPartySignalProviders", value)

    @builtins.property
    @jsii.member(jsii_name="tpspBrowserVersion")
    def tpsp_browser_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspBrowserVersion"))

    @tpsp_browser_version.setter
    def tpsp_browser_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6445598da4fa1c2e75f9e52339e17a322151c53024abb309e298d334b2d478)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5b12479a485fc50654f9bf6c0ee8bd63692aa7679f4e510b7590a0fad31d813)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3be50b86434d40e96008721db86e88905f3cd679e32c4ea5d12d27200e448aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspChromeRemoteDesktopAppBlocked", value)

    @builtins.property
    @jsii.member(jsii_name="tpspCrowdStrikeAgentId")
    def tpsp_crowd_strike_agent_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspCrowdStrikeAgentId"))

    @tpsp_crowd_strike_agent_id.setter
    def tpsp_crowd_strike_agent_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa075d624ce81ec678aacd701a170d133ad54e533b8e821e2e345f09d23510e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspCrowdStrikeAgentId", value)

    @builtins.property
    @jsii.member(jsii_name="tpspCrowdStrikeCustomerId")
    def tpsp_crowd_strike_customer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspCrowdStrikeCustomerId"))

    @tpsp_crowd_strike_customer_id.setter
    def tpsp_crowd_strike_customer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__104ae5490f5460670c2c03dc7dbd2801b97febfbd6d18290e1c85b670812a392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspCrowdStrikeCustomerId", value)

    @builtins.property
    @jsii.member(jsii_name="tpspDeviceEnrollmentDomain")
    def tpsp_device_enrollment_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspDeviceEnrollmentDomain"))

    @tpsp_device_enrollment_domain.setter
    def tpsp_device_enrollment_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b8ada7b1ec5501eac3f7850007d0506a77532e143c9207b4daf96ff051b97a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bad42606083d2280948497452babb3a764c7667b384e3bacb441edd075097e82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspDiskEncrypted", value)

    @builtins.property
    @jsii.member(jsii_name="tpspKeyTrustLevel")
    def tpsp_key_trust_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspKeyTrustLevel"))

    @tpsp_key_trust_level.setter
    def tpsp_key_trust_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0b07a33816fa1648fc300ec4144679bdcf48d418c4d55031cae43361a4aa9e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09af421714a6ee4ef467a5bfabdd365b1fdf32488708954bc331547e756b2a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspOsFirewall", value)

    @builtins.property
    @jsii.member(jsii_name="tpspOsVersion")
    def tpsp_os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspOsVersion"))

    @tpsp_os_version.setter
    def tpsp_os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ce2cb715022a59a8d9f965ef6162ef85de430807b9319b77723c516fd9ac19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspOsVersion", value)

    @builtins.property
    @jsii.member(jsii_name="tpspPasswordProctectionWarningTrigger")
    def tpsp_password_proctection_warning_trigger(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspPasswordProctectionWarningTrigger"))

    @tpsp_password_proctection_warning_trigger.setter
    def tpsp_password_proctection_warning_trigger(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b29030808ccc2d97155990fecb5c9c4139c72b3d21e5e0ce64b184af09d721c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e421f97db4d3d38976664085defb9c15f50547d8959b4b7477bc09b687907d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspRealtimeUrlCheckMode", value)

    @builtins.property
    @jsii.member(jsii_name="tpspSafeBrowsingProtectionLevel")
    def tpsp_safe_browsing_protection_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspSafeBrowsingProtectionLevel"))

    @tpsp_safe_browsing_protection_level.setter
    def tpsp_safe_browsing_protection_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a3a7fdb2f2bca39ff76f3404ca0241558715a57781ded39a151f781304e3f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca7c95ceea90fe35d8d254d78d4740e766d7caa5f0dda311c99d598be404bde7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspScreenLockSecured", value)

    @builtins.property
    @jsii.member(jsii_name="tpspSecureBootEnabled")
    def tpsp_secure_boot_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tpspSecureBootEnabled"))

    @tpsp_secure_boot_enabled.setter
    def tpsp_secure_boot_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90b9ca16e7474fccb104ba24722d27dd72c3796d1dc416abb324ca4769f4dfbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspSecureBootEnabled", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__95eb15d99afff90a2df0a4aeb051e77993dd29f159897d3b885b850bca2ac064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspSiteIsolationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="tpspThirdPartyBlockingEnabled")
    def tpsp_third_party_blocking_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tpspThirdPartyBlockingEnabled"))

    @tpsp_third_party_blocking_enabled.setter
    def tpsp_third_party_blocking_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08d25e5e4e892720364672ecd8844e2085fd363324905a7dbcce18cdfbdcca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspThirdPartyBlockingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="tpspWindowsMachineDomain")
    def tpsp_windows_machine_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspWindowsMachineDomain"))

    @tpsp_windows_machine_domain.setter
    def tpsp_windows_machine_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2bf5b10f3be22532144a57975da3f8fe0ce6537b24f1ef10be62a0076abe47b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspWindowsMachineDomain", value)

    @builtins.property
    @jsii.member(jsii_name="tpspWindowsUserDomain")
    def tpsp_windows_user_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tpspWindowsUserDomain"))

    @tpsp_windows_user_domain.setter
    def tpsp_windows_user_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__233704c38335ed8383c28139dac79d0af579cefea5de4f8abf053138e9225586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tpspWindowsUserDomain", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.policyDeviceAssuranceWindows.PolicyDeviceAssuranceWindowsConfig",
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
        "tpsp_crowd_strike_agent_id": "tpspCrowdStrikeAgentId",
        "tpsp_crowd_strike_customer_id": "tpspCrowdStrikeCustomerId",
        "tpsp_device_enrollment_domain": "tpspDeviceEnrollmentDomain",
        "tpsp_disk_encrypted": "tpspDiskEncrypted",
        "tpsp_key_trust_level": "tpspKeyTrustLevel",
        "tpsp_os_firewall": "tpspOsFirewall",
        "tpsp_os_version": "tpspOsVersion",
        "tpsp_password_proctection_warning_trigger": "tpspPasswordProctectionWarningTrigger",
        "tpsp_realtime_url_check_mode": "tpspRealtimeUrlCheckMode",
        "tpsp_safe_browsing_protection_level": "tpspSafeBrowsingProtectionLevel",
        "tpsp_screen_lock_secured": "tpspScreenLockSecured",
        "tpsp_secure_boot_enabled": "tpspSecureBootEnabled",
        "tpsp_site_isolation_enabled": "tpspSiteIsolationEnabled",
        "tpsp_third_party_blocking_enabled": "tpspThirdPartyBlockingEnabled",
        "tpsp_windows_machine_domain": "tpspWindowsMachineDomain",
        "tpsp_windows_user_domain": "tpspWindowsUserDomain",
    },
)
class PolicyDeviceAssuranceWindowsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        tpsp_crowd_strike_agent_id: typing.Optional[builtins.str] = None,
        tpsp_crowd_strike_customer_id: typing.Optional[builtins.str] = None,
        tpsp_device_enrollment_domain: typing.Optional[builtins.str] = None,
        tpsp_disk_encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_key_trust_level: typing.Optional[builtins.str] = None,
        tpsp_os_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_os_version: typing.Optional[builtins.str] = None,
        tpsp_password_proctection_warning_trigger: typing.Optional[builtins.str] = None,
        tpsp_realtime_url_check_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_safe_browsing_protection_level: typing.Optional[builtins.str] = None,
        tpsp_screen_lock_secured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_secure_boot_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_site_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_third_party_blocking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tpsp_windows_machine_domain: typing.Optional[builtins.str] = None,
        tpsp_windows_user_domain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Policy device assurance name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#name PolicyDeviceAssuranceWindows#name}
        :param disk_encryption_type: List of disk encryption type, can be ALL_INTERNAL_VOLUMES. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#disk_encryption_type PolicyDeviceAssuranceWindows#disk_encryption_type}
        :param os_version: The device os minimum version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#os_version PolicyDeviceAssuranceWindows#os_version}
        :param screenlock_type: List of screenlock type, can be BIOMETRIC or BIOMETRIC, PASSCODE. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#screenlock_type PolicyDeviceAssuranceWindows#screenlock_type}
        :param secure_hardware_present: Indicates if the device constains a secure hardware functionality. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#secure_hardware_present PolicyDeviceAssuranceWindows#secure_hardware_present}
        :param third_party_signal_providers: Check to include third party signal provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#third_party_signal_providers PolicyDeviceAssuranceWindows#third_party_signal_providers}
        :param tpsp_browser_version: Third party signal provider minimum browser version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_browser_version PolicyDeviceAssuranceWindows#tpsp_browser_version}
        :param tpsp_builtin_dns_client_enabled: Third party signal provider builtin dns client enable. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_builtin_dns_client_enabled PolicyDeviceAssuranceWindows#tpsp_builtin_dns_client_enabled}
        :param tpsp_chrome_remote_desktop_app_blocked: Third party signal provider chrome remote desktop app blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_chrome_remote_desktop_app_blocked PolicyDeviceAssuranceWindows#tpsp_chrome_remote_desktop_app_blocked}
        :param tpsp_crowd_strike_agent_id: Third party signal provider crowdstrike agent id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_crowd_strike_agent_id PolicyDeviceAssuranceWindows#tpsp_crowd_strike_agent_id}
        :param tpsp_crowd_strike_customer_id: Third party signal provider crowdstrike user id. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_crowd_strike_customer_id PolicyDeviceAssuranceWindows#tpsp_crowd_strike_customer_id}
        :param tpsp_device_enrollment_domain: Third party signal provider device enrollment domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_device_enrollment_domain PolicyDeviceAssuranceWindows#tpsp_device_enrollment_domain}
        :param tpsp_disk_encrypted: Third party signal provider disk encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_disk_encrypted PolicyDeviceAssuranceWindows#tpsp_disk_encrypted}
        :param tpsp_key_trust_level: Third party signal provider key trust level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_key_trust_level PolicyDeviceAssuranceWindows#tpsp_key_trust_level}
        :param tpsp_os_firewall: Third party signal provider os firewall. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_os_firewall PolicyDeviceAssuranceWindows#tpsp_os_firewall}
        :param tpsp_os_version: Third party signal provider minimum os version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_os_version PolicyDeviceAssuranceWindows#tpsp_os_version}
        :param tpsp_password_proctection_warning_trigger: Third party signal provider password protection warning trigger. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_password_proctection_warning_trigger PolicyDeviceAssuranceWindows#tpsp_password_proctection_warning_trigger}
        :param tpsp_realtime_url_check_mode: Third party signal provider realtime url check mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_realtime_url_check_mode PolicyDeviceAssuranceWindows#tpsp_realtime_url_check_mode}
        :param tpsp_safe_browsing_protection_level: Third party signal provider safe browsing protection level. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_safe_browsing_protection_level PolicyDeviceAssuranceWindows#tpsp_safe_browsing_protection_level}
        :param tpsp_screen_lock_secured: Third party signal provider screen lock secure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_screen_lock_secured PolicyDeviceAssuranceWindows#tpsp_screen_lock_secured}
        :param tpsp_secure_boot_enabled: Third party signal provider secure boot enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_secure_boot_enabled PolicyDeviceAssuranceWindows#tpsp_secure_boot_enabled}
        :param tpsp_site_isolation_enabled: Third party signal provider site isolation enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_site_isolation_enabled PolicyDeviceAssuranceWindows#tpsp_site_isolation_enabled}
        :param tpsp_third_party_blocking_enabled: Third party signal provider third party blocking enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_third_party_blocking_enabled PolicyDeviceAssuranceWindows#tpsp_third_party_blocking_enabled}
        :param tpsp_windows_machine_domain: Third party signal provider windows machine domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_windows_machine_domain PolicyDeviceAssuranceWindows#tpsp_windows_machine_domain}
        :param tpsp_windows_user_domain: Third party signal provider windows user domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_windows_user_domain PolicyDeviceAssuranceWindows#tpsp_windows_user_domain}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da70ff9a65370e9beb2ae8d0795ad2172372b996beea0c3cb1c2b3371f9410e2)
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
            check_type(argname="argument tpsp_crowd_strike_agent_id", value=tpsp_crowd_strike_agent_id, expected_type=type_hints["tpsp_crowd_strike_agent_id"])
            check_type(argname="argument tpsp_crowd_strike_customer_id", value=tpsp_crowd_strike_customer_id, expected_type=type_hints["tpsp_crowd_strike_customer_id"])
            check_type(argname="argument tpsp_device_enrollment_domain", value=tpsp_device_enrollment_domain, expected_type=type_hints["tpsp_device_enrollment_domain"])
            check_type(argname="argument tpsp_disk_encrypted", value=tpsp_disk_encrypted, expected_type=type_hints["tpsp_disk_encrypted"])
            check_type(argname="argument tpsp_key_trust_level", value=tpsp_key_trust_level, expected_type=type_hints["tpsp_key_trust_level"])
            check_type(argname="argument tpsp_os_firewall", value=tpsp_os_firewall, expected_type=type_hints["tpsp_os_firewall"])
            check_type(argname="argument tpsp_os_version", value=tpsp_os_version, expected_type=type_hints["tpsp_os_version"])
            check_type(argname="argument tpsp_password_proctection_warning_trigger", value=tpsp_password_proctection_warning_trigger, expected_type=type_hints["tpsp_password_proctection_warning_trigger"])
            check_type(argname="argument tpsp_realtime_url_check_mode", value=tpsp_realtime_url_check_mode, expected_type=type_hints["tpsp_realtime_url_check_mode"])
            check_type(argname="argument tpsp_safe_browsing_protection_level", value=tpsp_safe_browsing_protection_level, expected_type=type_hints["tpsp_safe_browsing_protection_level"])
            check_type(argname="argument tpsp_screen_lock_secured", value=tpsp_screen_lock_secured, expected_type=type_hints["tpsp_screen_lock_secured"])
            check_type(argname="argument tpsp_secure_boot_enabled", value=tpsp_secure_boot_enabled, expected_type=type_hints["tpsp_secure_boot_enabled"])
            check_type(argname="argument tpsp_site_isolation_enabled", value=tpsp_site_isolation_enabled, expected_type=type_hints["tpsp_site_isolation_enabled"])
            check_type(argname="argument tpsp_third_party_blocking_enabled", value=tpsp_third_party_blocking_enabled, expected_type=type_hints["tpsp_third_party_blocking_enabled"])
            check_type(argname="argument tpsp_windows_machine_domain", value=tpsp_windows_machine_domain, expected_type=type_hints["tpsp_windows_machine_domain"])
            check_type(argname="argument tpsp_windows_user_domain", value=tpsp_windows_user_domain, expected_type=type_hints["tpsp_windows_user_domain"])
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
        if tpsp_crowd_strike_agent_id is not None:
            self._values["tpsp_crowd_strike_agent_id"] = tpsp_crowd_strike_agent_id
        if tpsp_crowd_strike_customer_id is not None:
            self._values["tpsp_crowd_strike_customer_id"] = tpsp_crowd_strike_customer_id
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
        if tpsp_secure_boot_enabled is not None:
            self._values["tpsp_secure_boot_enabled"] = tpsp_secure_boot_enabled
        if tpsp_site_isolation_enabled is not None:
            self._values["tpsp_site_isolation_enabled"] = tpsp_site_isolation_enabled
        if tpsp_third_party_blocking_enabled is not None:
            self._values["tpsp_third_party_blocking_enabled"] = tpsp_third_party_blocking_enabled
        if tpsp_windows_machine_domain is not None:
            self._values["tpsp_windows_machine_domain"] = tpsp_windows_machine_domain
        if tpsp_windows_user_domain is not None:
            self._values["tpsp_windows_user_domain"] = tpsp_windows_user_domain

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#name PolicyDeviceAssuranceWindows#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_encryption_type(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of disk encryption type, can be ALL_INTERNAL_VOLUMES.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#disk_encryption_type PolicyDeviceAssuranceWindows#disk_encryption_type}
        '''
        result = self._values.get("disk_encryption_type")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def os_version(self) -> typing.Optional[builtins.str]:
        '''The device os minimum version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#os_version PolicyDeviceAssuranceWindows#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def screenlock_type(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of screenlock type, can be BIOMETRIC or BIOMETRIC, PASSCODE.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#screenlock_type PolicyDeviceAssuranceWindows#screenlock_type}
        '''
        result = self._values.get("screenlock_type")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secure_hardware_present(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if the device constains a secure hardware functionality.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#secure_hardware_present PolicyDeviceAssuranceWindows#secure_hardware_present}
        '''
        result = self._values.get("secure_hardware_present")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def third_party_signal_providers(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Check to include third party signal provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#third_party_signal_providers PolicyDeviceAssuranceWindows#third_party_signal_providers}
        '''
        result = self._values.get("third_party_signal_providers")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_browser_version(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider minimum browser version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_browser_version PolicyDeviceAssuranceWindows#tpsp_browser_version}
        '''
        result = self._values.get("tpsp_browser_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_builtin_dns_client_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider builtin dns client enable.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_builtin_dns_client_enabled PolicyDeviceAssuranceWindows#tpsp_builtin_dns_client_enabled}
        '''
        result = self._values.get("tpsp_builtin_dns_client_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_chrome_remote_desktop_app_blocked(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider chrome remote desktop app blocked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_chrome_remote_desktop_app_blocked PolicyDeviceAssuranceWindows#tpsp_chrome_remote_desktop_app_blocked}
        '''
        result = self._values.get("tpsp_chrome_remote_desktop_app_blocked")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_crowd_strike_agent_id(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider crowdstrike agent id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_crowd_strike_agent_id PolicyDeviceAssuranceWindows#tpsp_crowd_strike_agent_id}
        '''
        result = self._values.get("tpsp_crowd_strike_agent_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_crowd_strike_customer_id(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider crowdstrike user id.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_crowd_strike_customer_id PolicyDeviceAssuranceWindows#tpsp_crowd_strike_customer_id}
        '''
        result = self._values.get("tpsp_crowd_strike_customer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_device_enrollment_domain(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider device enrollment domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_device_enrollment_domain PolicyDeviceAssuranceWindows#tpsp_device_enrollment_domain}
        '''
        result = self._values.get("tpsp_device_enrollment_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_disk_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider disk encrypted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_disk_encrypted PolicyDeviceAssuranceWindows#tpsp_disk_encrypted}
        '''
        result = self._values.get("tpsp_disk_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_key_trust_level(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider key trust level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_key_trust_level PolicyDeviceAssuranceWindows#tpsp_key_trust_level}
        '''
        result = self._values.get("tpsp_key_trust_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_os_firewall(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider os firewall.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_os_firewall PolicyDeviceAssuranceWindows#tpsp_os_firewall}
        '''
        result = self._values.get("tpsp_os_firewall")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_os_version(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider minimum os version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_os_version PolicyDeviceAssuranceWindows#tpsp_os_version}
        '''
        result = self._values.get("tpsp_os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_password_proctection_warning_trigger(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Third party signal provider password protection warning trigger.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_password_proctection_warning_trigger PolicyDeviceAssuranceWindows#tpsp_password_proctection_warning_trigger}
        '''
        result = self._values.get("tpsp_password_proctection_warning_trigger")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_realtime_url_check_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider realtime url check mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_realtime_url_check_mode PolicyDeviceAssuranceWindows#tpsp_realtime_url_check_mode}
        '''
        result = self._values.get("tpsp_realtime_url_check_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_safe_browsing_protection_level(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider safe browsing protection level.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_safe_browsing_protection_level PolicyDeviceAssuranceWindows#tpsp_safe_browsing_protection_level}
        '''
        result = self._values.get("tpsp_safe_browsing_protection_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_screen_lock_secured(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider screen lock secure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_screen_lock_secured PolicyDeviceAssuranceWindows#tpsp_screen_lock_secured}
        '''
        result = self._values.get("tpsp_screen_lock_secured")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_secure_boot_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider secure boot enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_secure_boot_enabled PolicyDeviceAssuranceWindows#tpsp_secure_boot_enabled}
        '''
        result = self._values.get("tpsp_secure_boot_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_site_isolation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider site isolation enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_site_isolation_enabled PolicyDeviceAssuranceWindows#tpsp_site_isolation_enabled}
        '''
        result = self._values.get("tpsp_site_isolation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_third_party_blocking_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Third party signal provider third party blocking enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_third_party_blocking_enabled PolicyDeviceAssuranceWindows#tpsp_third_party_blocking_enabled}
        '''
        result = self._values.get("tpsp_third_party_blocking_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tpsp_windows_machine_domain(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider windows machine domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_windows_machine_domain PolicyDeviceAssuranceWindows#tpsp_windows_machine_domain}
        '''
        result = self._values.get("tpsp_windows_machine_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tpsp_windows_user_domain(self) -> typing.Optional[builtins.str]:
        '''Third party signal provider windows user domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/okta/okta/4.4.3/docs/resources/policy_device_assurance_windows#tpsp_windows_user_domain PolicyDeviceAssuranceWindows#tpsp_windows_user_domain}
        '''
        result = self._values.get("tpsp_windows_user_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyDeviceAssuranceWindowsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PolicyDeviceAssuranceWindows",
    "PolicyDeviceAssuranceWindowsConfig",
]

publication.publish()

def _typecheckingstub__9e7d91786850b20bc9873e0b9431fe03752e5fac73991d710d1c96efbcf956b7(
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
    tpsp_crowd_strike_agent_id: typing.Optional[builtins.str] = None,
    tpsp_crowd_strike_customer_id: typing.Optional[builtins.str] = None,
    tpsp_device_enrollment_domain: typing.Optional[builtins.str] = None,
    tpsp_disk_encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_key_trust_level: typing.Optional[builtins.str] = None,
    tpsp_os_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_os_version: typing.Optional[builtins.str] = None,
    tpsp_password_proctection_warning_trigger: typing.Optional[builtins.str] = None,
    tpsp_realtime_url_check_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_safe_browsing_protection_level: typing.Optional[builtins.str] = None,
    tpsp_screen_lock_secured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_secure_boot_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_site_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_third_party_blocking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_windows_machine_domain: typing.Optional[builtins.str] = None,
    tpsp_windows_user_domain: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__6886d3904f2651d8238535803d05b62e14fc1db8569fdd4697d5e28c7b35d2cb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574476e2fe9e360b71afb47ffbbd526349e398e8d9ea3ada25d42348ca15b338(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771c761a7ebecdbe4c73e24429b02a50e1c62c2a226f6812689e749fa36b4b93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62de61f4c100642b8d578ecf81981724c4e98ed1b3283460d67ace8f3fa39063(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c361952024ad4fff4e2bacbc967936fa100569bd12f1ab4325843a2e2e0e2feb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0914459a2374dabef440ceb05bd7439a133a95196c3c1a31c8f848b522f25638(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6445598da4fa1c2e75f9e52339e17a322151c53024abb309e298d334b2d478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b12479a485fc50654f9bf6c0ee8bd63692aa7679f4e510b7590a0fad31d813(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3be50b86434d40e96008721db86e88905f3cd679e32c4ea5d12d27200e448aec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa075d624ce81ec678aacd701a170d133ad54e533b8e821e2e345f09d23510e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104ae5490f5460670c2c03dc7dbd2801b97febfbd6d18290e1c85b670812a392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b8ada7b1ec5501eac3f7850007d0506a77532e143c9207b4daf96ff051b97a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad42606083d2280948497452babb3a764c7667b384e3bacb441edd075097e82(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b07a33816fa1648fc300ec4144679bdcf48d418c4d55031cae43361a4aa9e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09af421714a6ee4ef467a5bfabdd365b1fdf32488708954bc331547e756b2a5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ce2cb715022a59a8d9f965ef6162ef85de430807b9319b77723c516fd9ac19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b29030808ccc2d97155990fecb5c9c4139c72b3d21e5e0ce64b184af09d721c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e421f97db4d3d38976664085defb9c15f50547d8959b4b7477bc09b687907d11(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a3a7fdb2f2bca39ff76f3404ca0241558715a57781ded39a151f781304e3f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7c95ceea90fe35d8d254d78d4740e766d7caa5f0dda311c99d598be404bde7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b9ca16e7474fccb104ba24722d27dd72c3796d1dc416abb324ca4769f4dfbd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95eb15d99afff90a2df0a4aeb051e77993dd29f159897d3b885b850bca2ac064(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08d25e5e4e892720364672ecd8844e2085fd363324905a7dbcce18cdfbdcca2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2bf5b10f3be22532144a57975da3f8fe0ce6537b24f1ef10be62a0076abe47b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233704c38335ed8383c28139dac79d0af579cefea5de4f8abf053138e9225586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da70ff9a65370e9beb2ae8d0795ad2172372b996beea0c3cb1c2b3371f9410e2(
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
    tpsp_crowd_strike_agent_id: typing.Optional[builtins.str] = None,
    tpsp_crowd_strike_customer_id: typing.Optional[builtins.str] = None,
    tpsp_device_enrollment_domain: typing.Optional[builtins.str] = None,
    tpsp_disk_encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_key_trust_level: typing.Optional[builtins.str] = None,
    tpsp_os_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_os_version: typing.Optional[builtins.str] = None,
    tpsp_password_proctection_warning_trigger: typing.Optional[builtins.str] = None,
    tpsp_realtime_url_check_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_safe_browsing_protection_level: typing.Optional[builtins.str] = None,
    tpsp_screen_lock_secured: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_secure_boot_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_site_isolation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_third_party_blocking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tpsp_windows_machine_domain: typing.Optional[builtins.str] = None,
    tpsp_windows_user_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
