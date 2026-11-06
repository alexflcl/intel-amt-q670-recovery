# 5. Timeline and approaches we discarded

[Español](../05-cronologia.md) · [English home](../../README.en.md)

Part of this case's value is helping others avoid repeating attempts that did not address the cause.

| Stage | Observed result | Lesson |
| --- | --- | --- |
| KVM requires consent | Enhanced still enforced a PIN | A client cannot override every platform policy |
| Edit FITC/OEM only | Effective state remained Enhanced | One byte and its CRC do not synchronize initialized data |
| Partial AMT unprovisioning | Earlier provisioning/network configuration was lost; privacy was unresolved | Record networking, keys and reset scope first |
| Selectively modify or delete MFS policy files | Did not produce a working solution | Data integrity and consistency matter |
| Transplant factory MFS alone | CSME stopped initializing; devices disappeared | Preserve MFS/EFS consistency and compatibility |
| USB recovery without sufficient permissions | Assertions stopped execution | Keep checks and read actual state |
| Reboot or clear CMOS | Did not restore the ME data | CMOS and persistent CSME data are different |
| FDO through HDA_SDO | Full SPI access was verified | The codec provided access to a PCH boot signal |
| Two full backups and restoration of our own ME | Working baseline recovered; NVMe reappeared | Recover operation before changing policy |
| MFIT on initialized data | Read-only privacy setting; identical builds | Do not flash a candidate that does not make the change |
| MFIT with compatible factory MFS/EFS and our own configuration | Default candidate with original code preserved | Review complete differences and decompose again |
| Selective write and full flash readback | 116 data sectors verified; everything outside ME unchanged | A writer finishing is insufficient without readback |
| Open FDO and boot normally | ME Normal, PrivacyLevel=0 and OptInRequired=0 | Verify policy at runtime |
| MEBx password/network/options | Owner regained operational management | Rebuilding data can require reprovisioning |
| MeshCommander Firmware Loader | Failed for the owner's objective | Distinguish the loader from Web Application Hosting |
| Manual Small upload, followed by Medium | Owner confirmed operation | KVM could be served from AMT's IP |
| Replace with index.htm | Storage-root file observed in browser; automatic entry from / unconfirmed | Separate uploading the file from replacing the entry page |

There was no need to desolder M_BIOS, install another hypervisor or format drives. The failure is not attributed to a demonstrated physical fault in the NVMe.

## Evidence levels

**Measured by tools during the intervention:** identical SPI reads, bounded changes, final readback, CSME state and privacy/opt-in values.

**Confirmed by the owner:** recovered BIOS/MEBx access and normal operation; working Small and Medium web applications.

**External procedure or not yet tested here:** the 65,535-byte boundary on another installation, Large operation, automatic entry through /, a complete feature matrix for the three editions, and persistence across future BIOS updates.

Intermediate diagnostic summaries were written before the repair finished. This repository's case record reflects the final known result; an intermediate plan is not automatically treated as an executed operation.
