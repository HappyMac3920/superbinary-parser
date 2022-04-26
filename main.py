import argparse
import os
import pathlib

from super_binary import SuperBinary

parser = argparse.ArgumentParser(
    description="Extracts a FOTA within a SuperBinary container."
)
parser.add_argument(
    "source",
    help='Path to the SuperBinary. Typically called "FirmwareUpdate.uarp".',
    type=argparse.FileType("rb"),
)
parser.add_argument(
    "output_dir",
    help='The directory to save payloads to.',
    type=pathlib.Path,
)
parser.add_argument(
    "--extract-payloads",
    help="Whether to decompress the FOTA.",
    action=argparse.BooleanOptionalAction,
    default=True,
)
parser.add_argument(
    "--decompresss-fota",
    help="Whether to decompress the FOTA.",
    action=argparse.BooleanOptionalAction,
)
parser.add_argument(
    "--extract-rofs",
    "--extract-sounds",
    help="If set, extracts the ROFS partition to the output directory under 'files'.",
    type=argparse.BooleanOptionalAction,
)
args = parser.parse_args()
print(args)
super_binary = SuperBinary(args.source)

# Ensure our payload directory can be written to.
payload_dir = args.output_dir
payload_dir.mkdir(parents=True, exist_ok=True)

# Write out payloads if desired.
if args.extract_payloads:
    for payload in super_binary.payloads:
        name = payload.get_tag() + ".bin"
        path = payload_dir / name
        # Write!
        with open(path, 'wb') as f:
            f.write(payload.payload)


print(super_binary.get_tag(b"FOTA"))