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
        description="Download and extract GTFS static files from an NTA archive."
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


def get_gtfs_member(archive: ZipFile, filename: str) -> str:
    matches = [
        member
        for member in archive.namelist()
        if Path(member).name.lower() == filename.lower()
    ]

    if len(matches) != 1:
        raise RuntimeError(f"The GTFS archive must contain exactly one {filename} file.")

    return matches[0]


def main():
    arguments = parse_arguments()
    output_directory = arguments.output_directory

    with urlopen(arguments.url, timeout=60) as response:
        archive_bytes = response.read()

    with ZipFile(BytesIO(archive_bytes)) as archive:
        stops_member = get_gtfs_member(archive, "stops.txt")
        routes_member = get_gtfs_member(archive, "routes.txt")

        stops_bytes = archive.read(stops_member)
        routes_bytes = archive.read(routes_member)

    output_directory.mkdir(parents=True, exist_ok=True)

    stops_path = output_directory / "stops.txt"
    routes_path = output_directory / "routes.txt"
    metadata_path = output_directory / "metadata.json"

    stops_path.write_bytes(stops_bytes)
    routes_path.write_bytes(routes_bytes)

    metadata_path.write_text(
        json.dumps(
            {
                "source_url": arguments.url,
                "downloaded_at": datetime.now(timezone.utc).isoformat(),
                "archive_sha256": hashlib.sha256(archive_bytes).hexdigest(),
                "stops_sha256": hashlib.sha256(stops_bytes).hexdigest(),
                "routes_sha256": hashlib.sha256(routes_bytes).hexdigest(),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {stops_path}")
    print(f"Wrote {routes_path}")
    print(f"Wrote {metadata_path}")


if __name__ == "__main__":
    main()