# 4. MeshCommander inside AMT 16.1: KVM from the system's AMT IP

[Español](../04-meshcommander-web.md) · [English home](../../README.en.md)

If AMT already works, this stage can be performed independently of FDO and privacy reconstruction.

In this case, the owner confirmed that **Small worked**, then that **Medium worked well**. These applications are hosted by AMT's web server and remain accessible when Proxmox is not running, provided AMT has power and network connectivity. There is no need to keep MeshCentral running on another machine.

## Downloads

Use normal MeshCommander with its Web Applications section. The old Firmware Loader can fail on AMT 16.1; failure of the loader does not prove that Web Application Hosting is unusable on your version.

| File | Size displayed by GitHub | Result on our unit |
| --- | --- | --- |
| [Firmware-Small.gz](https://raw.githubusercontent.com/Ylianst/MeshCommander/master/output/Firmware-Small.gz) | 39.5 KB | Worked |
| [Firmware-Medium.gz](https://raw.githubusercontent.com/Ylianst/MeshCommander/master/output/Firmware-Medium.gz) | 59.8 KB | Worked |
| [Firmware-Large.gz](https://raw.githubusercontent.com/Ylianst/MeshCommander/master/output/Firmware-Large.gz) | 70.8 KB | Not tested |

[Official build directory](https://github.com/Ylianst/MeshCommander/tree/master/output) and [MeshCommander project](https://github.com/Ylianst/MeshCommander). Files linked to master can change; keep a local copy of the package that works for you and its SHA-256.

We did not verify a complete Small-versus-Medium feature matrix or measure a KVM performance improvement.

## Install an application with a link

1. Download Small for the first test. If it works, you can repeat with Medium.
2. Rename the compressed copy to **fwm.htm.gz** without extracting it. Show file extensions in Explorer to avoid accidentally creating a name ending in .gz.gz.
3. Open normal MeshCommander on a computer on the network and connect to AMT's current IP with your administration account. TLS uses port 16993.
4. Open **Web Applications**, select fwm.htm.gz, and check that the destination name becomes fwm.htm and the type is text/html. The upload client handles the .gz suffix; uploading extracted HTML is not an automatic substitute for this procedure.
5. In the procedure used here, Vendor and Application were left empty and a link name, such as MeshCommander, was added. If you choose your own folder, note the resulting path.
6. Upload the file and open AMT's page in the browser:

~~~text
https://<AMT-IP>:16993/
~~~

7. Under **Web Applications Links**, open MeshCommander and test a KVM session.

The Proxmox IP and the IP configured in AMT can differ. After resetting ME data, AMT may lose an earlier static configuration and return to DHCP.

[Upstream issue #99](https://github.com/Ylianst/MeshCommander/issues/99) documents this approach on 16.1.30, filename/MIME problems and later versions that disable WebUI. Not all 16.1 variants behave alike.

## Make MeshCommander the start page

The owner was given these instructions after testing Medium. A browser tab showing MeshCommander at /amt-storage/index.htm was observed; automatic opening when visiting only / was not explicitly confirmed in the account.

1. Keep the previous working application link as a fallback and retain its local .gz file.
2. Copy the Medium package that worked and rename the copy to **index.htm.gz**.
3. In Web Applications, leave **Vendor, Application and Link empty**.
4. Select the compressed copy and verify that the destination is **index.htm**, with type text/html. Keep it compressed.
5. Upload it. The special location is the root of application storage, **/amt-storage/index.htm**. This is not another application under /amt-storage/vendor/app/.
6. Test these two addresses separately, using a forced reload or a new session:

~~~text
https://<AMT-IP>:16993/amt-storage/index.htm
https://<AMT-IP>:16993/
~~~

The first checks the hosted file; the second checks whether firmware uses it as the entry page. If only the first works, retain that URL and record your version's behavior.

Replacing index without Vendor/App is described in [this upstream comment](https://github.com/Ylianst/MeshCommander/issues/99#issuecomment-2574134892). An empty Link avoids adding an unnecessary visible link; location and filename determine the replacement.

To roll back, use the external MeshCommander client and delete only the added index.htm through application management, if that operation is supported by the interface. A command that clears all storage also deletes fallback applications, so it is not equivalent to removing only index.

## Total capacity and upload limits

Intel documents up to **200 KB of shared space** for these applications/data and support for chunked HTTP transfers. That differs from the size accepted by a particular client operation. [Intel: Adding Custom Web Applications](https://software.intel.com/sites/manageability/AMT_Implementation_and_Reference_Guide/WordDocuments/addingcustomwebapplications.htm).

Issue #99 reported a practical boundary of 65,535 bytes on one AMT 16.1 upload path. Medium is below that size; Large exceeds it. We did not measure that boundary on our unit or test Large. If a larger upload fails, check size, occupied space, path, MIME type and client support before attributing the failure solely to total storage capacity.

## Distinguishing common failures

| Symptom | What to check |
| --- | --- |
| Browser downloads console or another file | Filename, extension and MIME type; use the compressed package named .htm.gz |
| Loader fails but MeshCommander connects | Try manual upload through Web Applications |
| HTTP 500 during upload | Check compression, size and storage; this error does not identify a single cause |
| Web browser access disabled / page unavailable | May indicate disabled WebUI or an incorrect path; check version and exact URL |
| File opens but KVM fails | Check KVM, consent, graphics and authentication independently of HTML hosting |
| AmtLoadWebApp is unavailable | Modern MeshCMD versions removed that action; do not assume an old guide describes your executable |

Downloading and uploading a web application does not replace a CSME security update. A firmware downgrade is not required as part of this procedure. Keep the administration interface on a management network or behind controlled private access.
