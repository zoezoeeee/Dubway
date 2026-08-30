import argparse
import hashlib
import json
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile


API_DIRECTORY = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIRECTORY = API_DIRECTORY / "data" / "gtfs"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Download and extract stops.txt from an NTA static GTFS archive."
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Current static GTFS archive URL copied from the NTA developer portal.",
    )
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=DEFAULT_OUTPUT_DIRECTORY,
        help=f"Directory for generated data (default: {DEFAULT_OUTPUT_DIRECTORY}).",
    )
    return parser.parse_args()


def get_stops_member(archive: ZipFile) -> str:
    matches = [
        member
        for member in archive.namelist()
        if Path(member).name.lower() == "stops.txt"
    ]

    if len(matches) != 1:
        raise RuntimeError("The GTFS archive must contain exactly one stops.txt file.")

    return matches[0]


def main():
    arguments = parse_arguments()
    output_directory = arguments.output_directory

    with urlopen(arguments.url, timeout=60) as response:
        archive_bytes = response.read()

    with ZipFile(BytesIO(archive_bytes)) as archive:
        stops_member = get_stops_member(archive)
        stops_bytes = archive.read(stops_member)

    output_directory.mkdir(parents=True, exist_ok=True)
    stops_path = output_directory / "stops.txt"
    metadata_path = output_directory / "metadata.json"

    stops_path.write_bytes(stops_bytes)
    metadata_path.write_text(
        json.dumps(
            {
                "source_url": arguments.url,
                "downloaded_at": datetime.now(timezone.utc).isoformat(),
                "archive_sha256": hashlib.sha256(archive_bytes).hexdigest(),
                "stops_sha256": hashlib.sha256(stops_bytes).hexdigest(),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {stops_path}")
    print(f"Wrote {metadata_path}")


if __name__ == "__main__":
    main()
