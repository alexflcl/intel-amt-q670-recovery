# Intel AMT on Gigabyte Q670: change PrivacyLevel, enable KVM without a PIN, and recover ME

[Español](README.md) · English — complete documentation

A real case documented on **6 November 2026**: a **Gigabyte Q670M D3H DDR4, PCB revision 1.1, BIOS F34a**, with **CSME Corporate H 16.1.30.2255**.

The objective was to use KVM without entering a consent code on the local display. **Enhanced** privacy prevented disabling that requirement. During investigation, an incomplete change to ME data left the subsystem uninitialized and devices, including NVMe, disappeared. We restored operation and rebuilt the **Default** configuration. We then hosted MeshCommander inside AMT so KVM could be opened in a browser through AMT's own IP.

**The PrivacyLevel workflow can be followed from a working motherboard.** The failure is part of this case's history and explains recovery; it is not a required step for changing policy.

➡ **[Main workflow: Enhanced → Default from a working motherboard](docs/en/00-change-privacy-level.md)**  
➡ **[ALC897 FDO connection: photo, identification, sequence and effects](docs/en/02-fdo-recovery.md)**

## Results and scope

| Check | Result |
| --- | --- |
| Proxmox, NVMe and integrated Ethernet | Recovered |
| CSME after removing FDO | Normal state, initialization complete, error 0 |
| Effective PrivacyLevel | 0, Default |
| Effective OptInRequired | 0 |
| AMTNetworkEnabled | 1 |
| MeshCommander Small and Medium hosted in AMT | Operation confirmed by the owner |
| Replace the start page with index.htm | Procedure included; automatic entry from / awaits explicit confirmation |

Final technical values are summarized in the [evidence record](evidence/case-study.json). It distinguishes system measurements, image checks and results reported by the owner.

**This case does not establish a universal method for every Q670 motherboard or every 16.1 version.** Memory addresses, flash layout and physical wiring belong to the unit studied.

## Where to start

1. **AMT works and you only want KVM from its IP:** go straight to [MeshCommander in web storage](docs/en/04-meshcommander-web.md). Privacy changes or ME reconstruction are unnecessary if your consent options are already sufficient.
2. **AMT works but the PIN cannot be disabled:** follow the [PrivacyLevel workflow](docs/en/00-change-privacy-level.md), which starts by confirming the cause.
3. **ME does not initialize or devices disappeared after a modification:** read [FDO and recovery](docs/en/02-fdo-recovery.md).
4. **You want to understand how Enhanced was changed to Default:** see [MFIT reconstruction](docs/en/03-mfit-default.md) and [the approaches that did not solve the problem](docs/en/05-timeline.md).

The [check_q670_images.py utility](tools/check_q670_images.py) compares images offline and checks which areas change. It does not write firmware or certify bootability. [English usage instructions](tools/README.en.md).

## All chapters in English

| Chapter | Contents |
| --- | --- |
| [0. Change PrivacyLevel](docs/en/00-change-privacy-level.md) | Workflow from a working motherboard, preparation and final checks |
| [1. Diagnosis](docs/en/01-diagnostics.md) | Privacy, provisioning, ME failure and observed errors |
| [2. FDO connection and recovery](docs/en/02-fdo-recovery.md) | Original wiring photo, resistor, effects and power sequence |
| [3. MFIT Default reconstruction](docs/en/03-mfit-default.md) | Region map, coherent data reconstruction and code preservation |
| [4. MeshCommander in AMT](docs/en/04-meshcommander-web.md) | Manual upload, Small/Medium, index.htm and troubleshooting |
| [5. Timeline](docs/en/05-timeline.md) | Failed attempts, lessons and levels of evidence |
| [6. References](docs/en/06-references.md) | Primary references, upstream projects and contributions |

## What made recovery possible

- Having our own ME backup from before the experiments, then obtaining two identical full SPI reads.
- Temporarily enabling Flash Descriptor Override through a boot signal accessible at the audio codec.
- Restoring our own backup first while preserving the other regions.
- Rebuilding factory MFS/EFS data together with MFIT 16.1 and our own unit's configuration.
- Keeping the original signed code and limiting the final write to the required data sectors.
- Reading the whole flash after writing and checking CSME/AMT after a normal boot without FDO.

## Equipment and tools

The case used live Linux with SSH, a second Windows computer, Intel Modular Flash Image Tool 16.1.25.2091, ME Analyzer for supplementary analysis, a soldering iron, fine wire and a 2 kΩ resistor. Supply voltage was measured with a FNIRSI 1014D oscilloscope; a multimeter is simpler for this DC measurement. Desoldering the flash and using an external programmer were unnecessary.

Obtain Intel tools and firmware from an authorized source. This repository contains original documentation and an offline comparator; third-party downloads link to their projects. Board dumps may contain keys, provisioning state and unit-specific identifiers: use your own backups and keep them out of public repositories.

## Sources and contributions

[Technical references and credits](docs/en/06-references.md). When contributing a case, include the board model, revision, BIOS, CSME version/SKU, symptom and how the result was verified. Share sanitized records without credentials, MAC addresses, UUIDs or complete flash images.

Documentation by **alexflcl**, prepared with Codex assistance from diagnosis and recovery of the owner's own system. [MIT license](LICENSE) for original repository content.
