# 0. Enhanced → Default on a working motherboard

[Español](../00-cambiar-privacy-level.md) · [English home](../../README.en.md)

This workflow addresses the original goal: **change the privacy policy so that KVM can be configured without mandatory local consent**. It brings together the stages that ultimately worked on the documented unit, leaving out the unsuccessful experiments.

The entire sequence, started from scratch on a second healthy motherboard, **has not been tested as an independent case**. On our unit, the final change was made after restoring normal operation. This reordered workflow is a preparation and execution guide based on that result.

## 1. Confirm that PrivacyLevel is the cause

Query the effective policy through your management client or WS-Man.

| Result | Next step |
| --- | --- |
| PrivacyLevel=0, Default | Check control mode and consent settings; this firmware change is unnecessary |
| PrivacyLevel=1, Enhanced, and opt-in cannot be disabled | This is the scenario covered here |
| ME does not initialize or devices disappeared after a modification | Start by recovering from your own backup |
| It is unclear whether the motherboard implements AMT | Check hardware, firmware and capabilities first |

Default allows consent policy to be configured; it does not, by itself, guarantee that a system in any control mode will accept KVM without a PIN. Check control mode and opt-in configuration as well.

## 2. Prepare before working on the board

- Verify the board, PCB revision, codec, BIOS and CSME version/SKU. The documented setup is Q670M D3H DDR4 rev. 1.1, ALC897 and Corporate H 16.1.30.2255.
- Save the AMT network and access settings you will need to restore.
- Preserve recovery keys and anything needed to recover data protected by PTT/TPM: this procedure reinitializes ME data.
- Obtain compatible MFIT and a factory data source whose compatibility you can establish. Our source was official F32 with matching ME code.
- Prepare live Linux and a maintenance connection. A USB or PCIe NIC was useful for reaching Linux; it does not replace AMT's network interface.
- Save whatever you can read from the working system before modifying it. If a region is locked, record that limitation instead of inventing its contents.
- Prepare a soldering iron, fine insulated wire, a 2 kΩ resistor and measuring equipment. Read the [complete FDO wiring instructions](02-fdo-recovery.md) first.

Your rollback target is your previous working state, even if that state still uses Enhanced privacy.

## 3. Install the FDO connection with power removed

1. Shut the system down normally.
2. Physically disconnect the PSU from mains power and wait for residual power to disappear.
3. Identify pin 1 and count the ALC897 pins. Confirm the relevant signal and supply for your PCB revision.
4. For the setup used on our unit, connect **pin 9 → 2 kΩ resistor → pin 5**, using insulated wires. Leave an accessible connection that can be opened without working next to the codec again.
5. Check that solder does not bridge neighboring pins and that exposed ends cannot touch other components.

**This connection does not change PrivacyLevel.** It prepares a boot with maintenance access to the flash; changing policy requires generating and writing the appropriate data.

## 4. Boot the maintenance environment and check permissions

Boot live Linux with the connection in place. On our unit, active FDO produced FDOPSS=0 and FRACC=0xffff. See [how to verify FDO](02-fdo-recovery.md#verify-that-fdo-is-actually-active).

CSME may be in maintenance mode, with MEI/AMT unavailable during that boot. A failed KVM connection in this state does not evaluate the privacy change.

Obtain **two identical complete 32 MiB reads**, save them off the machine, and confirm the region map. These reads are the exact source for preparing and checking the intervention and for rolling back.

## 5. Prepare and review the Default candidate

Follow the [MFIT procedure](03-mfit-default.md):

1. Preserve your own unit's configuration and code.
2. Use a compatible, internally consistent factory MFS/EFS data base.
3. Build Enhanced and Default controls.
4. Retain the original code and take only the reviewed data interval.
5. Decompose the candidate again and check all configuration differences.
6. Compare complete regions and the sectors that would need to be written.

The repository's offline comparator helps check this case's region map. It does not independently validate authenticated integrity or compatibility. The sector count depends on the input images: the 116 sectors in our case are not a fixed target for other units.

When starting with a working motherboard, **there is no mandatory initial restoration stage**. Prepare the candidate from your own working backups; keep the recovery chapter as your rollback reference.

## 6. Write, verify and save the results

Our write used a case-specific executor that checked board identity, region map, permissions, source hashes, sector boundaries and readback. Scripts tied to those private images are not presented as universal flashers for other readers.

Before using a writer on your unit, establish which sectors it will modify, how it will check the source, how each write will be verified, and how a preimage can be restored after a failure. Do not replace this stage with an unchecked write of MFIT's entire output.

After writing, read the whole SPI again: it must match the expected candidate, with the other regions unchanged. Save reports, images and hashes off the machine before shutting down.

## 7. Open the FDO connection with power removed, then boot normally

Shut down the maintenance environment, unplug the PSU and open the resistor connection. Insulate the ends. Do not remove or cut the connection while powered.

Boot with the connection open. On our unit, FDOPSS returned to 1, FRACC returned to 0x4acf, and CSME entered Normal state. A normal boot is required for ME to initialize its data and for AMT to be checked.

## 8. Reprovision and verify the result

1. Enter MEBx and configure the password/network if the reconstruction reset them.
2. Enable AMT network access and configure the consent options now permitted.
3. Query **PrivacyLevel=0**, **CanModifyOptInPolicy=1** and **OptInRequired=0**.
4. Check control mode. Do not confuse ProvisioningMode with CurrentControlMode.
5. Open a **fresh KVM session** without prior consent and confirm that it works without a local code.

Hosting MeshCommander is a separate improvement, performed after AMT works: [web application guide](04-meshcommander-web.md).
