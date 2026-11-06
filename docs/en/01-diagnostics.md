# 1. Diagnosis: distinguish privacy, activation and ME failure

[Español](../01-diagnostico.md) · [English home](../../README.en.md)

## The initial symptom

AMT was available, but Enhanced privacy required local consent for KVM. Unchecking a setting in the management client did not remove a platform-enforced restriction.

The runtime property AMT_GeneralSettings.PrivacyLevel uses Default=0, Enhanced=1 and Extreme=2. Enhanced does not allow opt-in to be disabled. Query the effective policy as well as examining the manufacturing configuration in a dump. [Intel reference](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/HTMLDocuments/WS-Management_Class_Reference/AMT_GeneralSettings.htm).

An important encoding difference appeared in this case: the observed OEM/FITC configuration byte used 01 for Default and 02 for Enhanced, while WS-Man returned 0 and 1 respectively. Do not copy a number between these representations.

## What to record before modifying firmware

- Exact motherboard model, PCB revision, BIOS version and ME version/SKU.
- Whether MEBx opens and allows password, network and consent configuration.
- Which AMT ports respond and whether network access is enabled.
- The effective PrivacyLevel and whether IPS_OptInService allows OptInRequired to be changed.
- CSME state and the presence of MEI/HECI, NVMe and network devices.
- The SPI reading method and which regions are actually accessible.

On Linux, identities and devices can be collected with read-only queries:

~~~sh
sudo dmidecode -t baseboard -t bios
lspci -nn
lsblk -o NAME,SIZE,TYPE,MODEL
ls /dev/mei*
~~~

These commands do not independently check flash protection or AMT policy. Review their output before publishing it: it may include device-specific information.

## Distinguish three states

| State | What we observed or how it is checked |
| --- | --- |
| AMT is unprovisioned | May require MEBx reactivation, a password and network activation |
| AMT works with Enhanced privacy | CSME can be healthy while policy prevents disabling the PIN |
| CSME is uninitialized or in maintenance mode | MEI and other devices may be absent; this is not equivalent to a KVM client failure |

During our recovery, loading BIOS defaults, removing the CMOS battery and performing a normal reboot did not repair ME's internal data. Clearing CMOS should not be treated as equivalent to restoring MFS/EFS.

## Errors that stopped the recovery USB

Versions of the case-specific script produced:

~~~text
AssertionError
assert event['sector_count'] == 1 and not event['mtd_writeable_after_cleanup']
~~~

and:

~~~text
AssertionError: ME write override was not granted after request
~~~

These were stop conditions: the expected state or permissions did not match. Line numbers depend on the script version. These messages do not prove that the hardware granted ME write access. Removing checks or blindly repeating writes did not solve the problem.

We kept the USB and its results, read the actual flash state, and moved to a physical override whose effect could be checked.

## Measuring privacy and final verification

With CSME healthy, the classes were queried through WS-Man. A temporary LMS relay restricted to loopback, with authorized local access, was used for diagnosis while external AMT connectivity was not yet ready.

Final observed values:

~~~text
AMT_GeneralSettings.PrivacyLevel = 0
AMT_GeneralSettings.AMTNetworkEnabled = 1
IPS_OptInService.CanModifyOptInPolicy = 1
IPS_OptInService.OptInRequired = 0
IPS_OptInService.OptInState = 0
~~~

ProvisioningMode, ProvisioningState and CurrentControlMode are different properties. **ProvisioningMode=1 is not used here as proof of Admin Control Mode.** To establish ACM through software, query the corresponding control-mode property, such as IPS_HostBasedSetupService.CurrentControlMode.

A property allowing KVM does not prove that a real session works. After these queries, the owner checked operational access and confirmed that MeshCommander Small and Medium worked from the browser.
