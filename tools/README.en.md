# Offline image comparison

[Español](README.md) · [English home](../README.en.md)

Requires Python 3. It installs no packages and opens no physical devices. It accepts only complete 32 MiB files with an Intel descriptor signature and regions matching the published case.

~~~sh
python tools/check_q670_images.py before.bin candidate.bin
~~~

JSON output goes to stdout and includes:

- Hashes of both files and whether they are identical.
- Number of differing bytes and 4 KiB sectors.
- SPI addresses of the affected sectors.
- Whether everything outside ME is identical.
- Whether everything outside the documented MDAT interval is identical.

Exit codes:

| Code | Meaning |
| --- | --- |
| 0 | No changes observed outside MDAT; includes identical images |
| 1 | Changes exist outside MDAT |
| 2 | Rejected input or read failure |

**A zero exit code only checks where differences occur.** It does not check MFS/EFS authentication, Intel signatures, CPU/PCH compatibility, manufacturing policy, factory-source compatibility or bootability. Data inside MDAT may be wrong even when everything else is identical.

When comparing two backup reads, also require identical=true. Two identical reads can still be incomplete or reflect a failed state; a valid acquisition method and a known previous backup are also needed.

The program does not save its report. Before sharing output, review its contents and the source of the images. Do not upload before.bin or candidate.bin to GitHub.

While preparing this publication, the tool was run against the archived restored backup and candidate: it found 382,236 differing bytes in 116 sectors, all within MDAT, with everything outside ME identical. An additional one-bit BIOS change was also checked and detected as a difference outside the permitted area.
