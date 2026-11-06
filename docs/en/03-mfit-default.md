# 3. Rebuild Default with MFIT while preserving the original code

[Español](../03-mfit-default.md) · [English home](../../README.en.md)

This is the case-specific stage that made the privacy change effective. It requires a valid backup from your own unit, exact partition identification and compatible tools. An image from another unit does not necessarily preserve your keys, configuration and manufacturing data.

**This is also the privacy-change stage for a working motherboard.** The [main workflow](00-change-privacy-level.md) orders the steps from Enhanced through the final KVM test. We used a restored dump because our unit had previously failed; a working unit should use its own working backup.

## Observed region map

All intervals here are half-open: the start is included and the end is excluded.

| Region | SPI start | SPI end |
| --- | --- | --- |
| Descriptor | 0x0000000 | 0x0001000 |
| GbE | 0x0001000 | 0x0003000 |
| ME | 0x0003000 | 0x0766000 |
| Region 9 / Device Expansion 2 | 0x0766000 | 0x1000000 |
| BIOS | 0x1000000 | 0x2000000 |

Region 9 returned a read error before FDO. It later became fully readable. **Do not fill an inaccessible region with FF on the assumption that it is empty.**

Within this case's ME region, the candidate's MDAT area was bounded by the relative interval **0x1ca000..0x34f000**, corresponding to absolute SPI addresses **0x1cd000..0x352000**. These boundaries belong to this layout and are not a template for other versions.

## Tool and factory source

We used Intel Modular Flash Image Tool **16.1.25.2091**, supplied locally by the owner. The Windows executable's Authenticode signature was verified as valid, with Intel Corporation as signer.

The official **F32 image for the same motherboard** was examined as the factory data source. Its native ME code matched the original code from our unit. F34a was also examined, but the available official image contained another ME variant and was not used as a complete replacement.

Matching BIOS version labels and board names do not establish that two ME regions are interchangeable. Components, version, SKU, region map and contents were compared.

## Why changing one byte was insufficient

The OEM/FITC configuration was only one representation of the policy. Policy files with integrity metadata were observed in initialized MFS data. Changing the OEM byte and its CRC did not, by itself, update AMT's effective state.

MFIT also warned that PrivacyLvl was read-only when rebuilding an already initialized image. The control and Default builds were identical, so that attempt was discarded.

We did not forge HMACs or treat a correct CRC as valid authentication of MFS files.

## Procedure that produced the working result

1. **Decompose the working dump from our own unit** with MFIT and save its complete configuration and components. Ours was a restored dump; a healthy board uses its own working backup.
2. **Decompose official F32** and locate its factory ME Sub Partition, containing the uninitialized MFS/EFS data together.
3. Prepare a working configuration that retains our own settings and components while using that factory data base as MeRegionFile.
4. Generate two control images from the same base: Enhanced and Default. The only functional setting changed was:

~~~text
CsePlugin:AmtProvisioningNvars:PrivacyLevel#RedirectionPrivSecLevel
Enhanced -> Default
~~~

5. Compare both builds. Five bytes differed: four CRC bytes and one policy byte. On our SPI, these were at 0x34500c..0x345010 and 0x345440. This comparison was between **the two factory-based builds**; it does not mean the patch applied to the live state consisted of five bytes.
6. Assemble the final candidate by preserving the original ME prefix and suffix and taking only **MDAT** from the Default output. MFIT had also changed twelve bytes outside MDAT; those changes were not retained.
7. Decompose the final candidate again. All non-path configuration values matched the original except Enhanced -> Default; the only different binary component was the ME data subpartition.
8. Compare signed code and layout against the original. ME Analyzer was used as an independent check, accounting for its limitations on this generation.
9. Obtain two new identical full backups immediately before writing, prepare the list of differing sectors, and verify that all fall inside the permitted data area.
10. Write only the 116 required data sectors and read the whole SPI again, checking the expected result and preservation of everything outside ME.

Reinitializing data loses previous AMT provisioning and can affect PTT/TPM state. This reset had been authorized before the intervention. Do not assume credentials or TPM-sealed objects will be preserved; have recovery keys and other required recovery material available first.

## Using MFIT's interface

The tool version used supports decomposition, configuration loading, setting overrides and rebuilding:

~~~powershell
.\mfit.exe --help
.\mfit.exe --decompose .\own-spi.bin --saveconfig .\own-config.xml
~~~

After preparing and reviewing an XML configuration using your own components and a compatible factory data base, the rebuild syntax is:

~~~powershell
.\mfit.exe --decompose .\own-spi.bin --loadconfig .\prepared-config.xml --setvalues "CsePlugin:AmtProvisioningNvars:PrivacyLevel#RedirectionPrivSecLevel=Default" --build .\review-only.bin --saveconfig .\review-config.xml
~~~

This example shows tool syntax; it does not prepare the XML or check compatibility. **review-only.bin is an output for inspection, not an instruction to program the entire flash.** Our applied candidate was assembled selectively as described in step 6.

XML files can contain unit-specific configuration and local paths. This repository does not provide a generic manufacturing XML or a ready-to-use flasher for other units.

## Static validation and boot

ME Analyzer reported an EFS table warning. The same warning appeared when analyzing the official F32 source. Valid code signatures were preserved, and the analyzer's limitation was acknowledged. None of these static checks replaced a boot test.

After writing, FDO was removed with power disconnected and the system was booted normally. BIOS/MEBx became accessible, a password was configured, networking was activated and opt-in was disabled. **PrivacyLevel=0 and OptInRequired=0** were then measured.

During that first boot, freshly generated data becomes initialized. The hash of the entire ME region may therefore legitimately change afterward. Review which area changed and check health and effective policy rather than relying only on a whole-region hash.
