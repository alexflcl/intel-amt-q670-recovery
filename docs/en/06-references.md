# 6. Technical references and credits

[Español](../06-referencias.md) · [English home](../../README.en.md)

## Intel and the motherboard manufacturer

- [Gigabyte Q670M D3H DDR4 BIOS support](https://www.gigabyte.com/Motherboard/Q670M-D3H-DDR4-rev-10/support): the public portal consulted lists rev. 1.0; our PCB was marked rev. 1.1. Check with the manufacturer which package applies to the actual unit before using an image.
- [Intel AMT_GeneralSettings](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/HTMLDocuments/WS-Management_Class_Reference/AMT_GeneralSettings.htm): privacy and network-setting semantics.
- [Intel IPS_OptInService](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/HTMLDocuments/WS-Management_Class_Reference/IPS_OptInService.htm): user consent.
- [Intel IPS_HostBasedSetupService](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/HTMLDocuments/WS-Management_Class_Reference/IPS_HostBasedSetupService.htm): control mode and provisioning.
- [Intel 600 Series PCH, Pin Straps](https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/intel-600-series-chipset-family-platform-controller-hub-pch-datasheet-volume/004/pin-straps/): Flash Descriptor Security Override strap.
- [Intel: Adding Custom Web Applications](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/WordDocuments/addingcustomwebapplications.htm).
- [Intel: Accessing Custom Web Applications](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/WordDocuments/accessingcustomwebapplications.htm).
- [Intel: AMT architecture](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/WordDocuments/hardwareplatformarchitecture1.htm).

## Projects used or consulted

- [MeshCommander, Ylian Saint-Hilaire and contributors](https://github.com/Ylianst/MeshCommander).
- [Builds for AMT hosting](https://github.com/Ylianst/MeshCommander/tree/master/output).
- [MeshCommander #99: installation on recent firmware](https://github.com/Ylianst/MeshCommander/issues/99). Includes experiences from jsastriawan, jontywigster, joshtrichards and other participants. These are observations from their systems, not a universal Intel specification.
- [Comment on /amt-storage/index.htm](https://github.com/Ylianst/MeshCommander/issues/99#issuecomment-2091734449).
- [Comment on index.htm without Vendor/App](https://github.com/Ylianst/MeshCommander/issues/99#issuecomment-2574134892).
- [ME Analyzer, by plutomaniac](https://github.com/platomav/MEAnalyzer): an analysis aid, with limited coverage of some CSME 16 structures.
- [FreeBSD: interpreting ME status registers](https://cgit.freebsd.org/src/commit/?id=8e5e2c391059eaa0280a32b951e3ab1fac278364): a primary code reference for state/mode/error interpretation.

Third-party trademarks, tools and firmware retain their respective licenses. This repository does not redistribute their executables or the system's SPI images.

## Contributing another case

For a correction or a new case, include:

1. Exact board, PCB revision, BIOS and CSME version.
2. Initial symptom and whether CSME was healthy.
3. Reading method and which regions were verified.
4. Changes applied and readback verification.
5. Privacy/opt-in values and a real KVM test.
6. Web application version and relative URL used, without a private IP address.

Keep measured results, owner-reported outcomes and hypotheses clearly distinguished.
