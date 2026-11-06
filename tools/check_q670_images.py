#!/usr/bin/env python3
"""Read-only comparison for the recorded Q670/F34a case layout.

This checks containment of differences, not cryptographic authenticity,
manufacturing configuration, platform compatibility or bootability.
"""

import argparse
import hashlib
import json
import struct
from pathlib import Path

SPI_SIZE = 0x2000000
SECTOR = 0x1000
REGIONS = {
    0: (0x0000000, 0x0001000),
    1: (0x1000000, 0x2000000),
    2: (0x0003000, 0x0766000),
    3: (0x0001000, 0x0003000),
    9: (0x0766000, 0x1000000),
}
ME_START, ME_END = REGIONS[2]
DATA_START = ME_START + 0x1CA000
DATA_END = ME_START + 0x34F000


def read_image(path):
    # Reject incompatible input sizes before allocating the buffer.
    if path.stat().st_size != SPI_SIZE:
        raise ValueError("Expected a complete 32 MiB SPI image for this case.")
    image = path.read_bytes()
    if len(image) != SPI_SIZE:
        raise ValueError("Input size changed during the read.")
    if struct.unpack_from("<I", image, 0x10)[0] != 0x0FF0A55A:
        raise ValueError("Intel descriptor signature does not match.")
    flmap0 = struct.unpack_from("<I", image, 0x14)[0]
    region_table = ((flmap0 >> 16) & 0xFF) * 16
    if region_table < 0x20 or region_table + 40 > 0x1000:
        raise ValueError("Unexpected descriptor region-table location.")
    for index, expected in REGIONS.items():
        register = struct.unpack_from("<I", image, region_table + index * 4)[0]
        start = (register & 0x7FFF) << 12
        end = (((register >> 16) & 0x7FFF) + 1) << 12
        if (start, end) != expected:
            raise ValueError(
                f"Region {index} differs from the recorded case layout."
            )
    return image


def compare(before, after):
    changed_sectors = []
    changed_bytes = 0
    outside_data_identical = True
    for offset in range(0, SPI_SIZE, SECTOR):
        a = before[offset:offset + SECTOR]
        b = after[offset:offset + SECTOR]
        if a != b:
            changed_sectors.append(hex(offset))
            changed_bytes += sum(x != y for x, y in zip(a, b))
            if offset < DATA_START or offset + SECTOR > DATA_END:
                outside_data_identical = False
    outside_me_identical = (
        before[:ME_START] == after[:ME_START]
        and before[ME_END:] == after[ME_END:]
    )
    return {
        "case_layout_matched": True,
        "before_sha256": hashlib.sha256(before).hexdigest(),
        "after_sha256": hashlib.sha256(after).hexdigest(),
        "identical": before == after,
        "changed_bytes": changed_bytes,
        "changed_4k_sectors": len(changed_sectors),
        "changed_sector_spi_offsets": changed_sectors,
        "outside_me_identical": outside_me_identical,
        "outside_recorded_mdat_identical": outside_data_identical,
        "recorded_mdat_spi_interval": [hex(DATA_START), hex(DATA_END)],
        "bootability_or_signatures_verified": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    args = parser.parse_args()
    try:
        report = compare(read_image(args.before), read_image(args.after))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Input rejected: {exc}\n")
    print(json.dumps(report, indent=2))
    return 0 if report["outside_recorded_mdat_identical"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
