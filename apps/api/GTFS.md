## Source and attribution

Download the current archive from the [NTA GTFS developer portal](https://developer.nationaltransport.ie/GTFS).
The NTA's GTFS fair usage policy describes the data as CC BY 4.0 and requires
public-facing attribution to the NTA, a source link, and an "as is" disclaimer.

Use this attribution in the product where static GTFS data is displayed:

> Transport data © National Transport Authority. Provided as is.

## Refreshing local data

1. Open the NTA GTFS portal and copy the current static GTFS archive URL.
2. From `apps/api`, run:

   ```bash
   python scripts/fetch_static_gtfs.py --url "PASTE_CURRENT_ARCHIVE_URL_HERE"
   ```

3. The script writes these ignored local files:

   ```text
   data/gtfs/stops.txt
   data/gtfs/metadata.json
   ```

4. `metadata.json` records the source URL, retrieval time, and SHA-256 hashes.
   Inspect it when reporting or reproducing a data issue.

5. Run a lookup to verify the imported feed:

   ```bash
   python find_stop_id.py 842
   ```

Refresh static GTFS before releasing any change that depends on stop, route, or
trip identifiers. Do not combine an old static feed with current realtime data.
