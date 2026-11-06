# Intel AMT KVM recovery on a Gigabyte Q670 motherboard

[Documentación completa en español](README.md)

This is a documented recovery of an owner's **Gigabyte Q670M D3H DDR4 rev. 1.1, BIOS F34a**, running **Intel CSME Corporate H 16.1.30.2255**.

The original objective was KVM without a local consent PIN. Enhanced privacy prevented disabling consent. During investigation, an incomplete modification of ME runtime data left CSME uninitialized and devices, including the NVMe drive, disappeared. Recovery restored the owner's original ME data first. A subsequent MFIT reconstruction changed privacy to Default while preserving the native signed code and all other flash regions.

## Confirmed outcome

- Proxmox, the NVMe drive and integrated Ethernet recovered.
- A normal boot with physical FDO removed reported CSME working state 5, operating mode 0, initialization complete and error 0.
- Read-only WS-Man queries returned PrivacyLevel=0 and OptInRequired=0.
- The owner confirmed working MeshCommander Small and Medium web applications hosted by AMT.
- Uploading an index.htm at the storage root is described; automatic entry from the bare / URL was not explicitly confirmed.

See the [sanitized evidence record](evidence/case-study.json). Manual MEBx setup was performed, but ProvisioningMode=1 is not presented as independent proof of Admin Control Mode. A CurrentControlMode query was not retained.

## What worked

1. Obtain and retain the owner's own known-good backup.
2. Temporarily assert the PCH flash-descriptor override strap through an accessible audio-codec connection.
3. Verify override permissions and obtain two identical complete 32 MiB reads.
4. Restore the original ME region and verify that all other regions remain unchanged.
5. Use compatible MFIT 16.1 with a matching factory MFS/EFS base and the unit's complete configuration.
6. Build Enhanced and Default controls, inspect differences, then preserve the original code/layout and transplant only the reviewed MDAT data interval.
7. Re-decompose the candidate, verify configuration and code preservation, write only required sectors, and read back the entire SPI.
8. Remove the physical override with power disconnected, boot normally, configure MEBx, and measure the effective policy.

The [detailed MFIT account](docs/03-mfit-default.md) gives the exact region boundaries of this unit and the distinction between the factory-build comparison and the larger runtime-data reset. These offsets are not a cross-platform recipe.

## Physical FDO used in this case

The accessible codec was a Realtek ALC897. A 2 kΩ resistor connected the identified pin 9 DVDDIO point to pin 5 HDA_SDO; DVDDIO measured approximately 3.43 V. Pin numbering, voltage and signal routing must be established for the actual board before using such a connection. Connections were prepared and removed with the PSU disconnected.

The successful override boot showed FDOPSS=0 and FRACC=0xffff. The final normal boot showed FDOPSS=1 and FRACC=0x4acf. AMT functionality was assessed after removing FDO.

See [the recovery account](docs/02-fdo-recuperacion.md), including why the audio chip was relevant and why desoldering the main WSON flash was unnecessary.

## MeshCommander inside AMT 16.1

The owner wanted the browser application served from AMT's own IP, independently of the host OS.

Download the [official Small or Medium build](https://github.com/Ylianst/MeshCommander/tree/master/output), keep it compressed, rename it to fwm.htm.gz, and upload it through normal MeshCommander's Web Applications feature. Check that the destination filename and HTML MIME type are correct. Add a link, open AMT over HTTPS/16993, select Web Applications Links and test KVM.

For a homepage replacement, the documented method uses index.htm.gz with Vendor, Application and Link empty, producing /amt-storage/index.htm. Preserve a separately working application and test the file URL and bare / URL independently.

Read the [full web application guide](docs/04-meshcommander-web.md). It distinguishes total storage capacity from upload-size problems, and working 16.1.30 installations from later builds where WebUI may be disabled. The relevant upstream discussion is [MeshCommander issue #99](https://github.com/Ylianst/MeshCommander/issues/99).

## Failed approaches worth avoiding

Changing only the OEM privacy byte and its CRC did not update initialized runtime policy. Partial unprovisioning did not solve privacy and changed networking. Selective MFS edits did not produce a working solution; copying factory MFS alone broke initialization. Clearing CMOS did not restore ME data. Removing recovery assertions would have hidden failed preconditions.

Read [the chronology](docs/05-cronologia.md) before repeating any of these experiments.

## Scope, tooling and privacy

This repository provides original documentation and a **read-only offline image comparator**, not a universal flasher. Reinitializing ME data can reset AMT provisioning and affect PTT/TPM-backed state. Preserve the needed recovery material before intervening.

No proprietary Intel tools, full SPI images, credentials, MAC addresses, UUIDs, or private network addresses are redistributed. Obtain compatible manufacturer firmware and authorized tools separately. Do not use another unit's dump as a replacement for your own.

The comparison utility checks changes against the recorded layout; it does not validate Intel signatures, compatible hardware, manufacturing settings or bootability.

[References and credits](docs/06-referencias.md). Original content by **alexflcl**, prepared with Codex assistance. [MIT license](LICENSE).
