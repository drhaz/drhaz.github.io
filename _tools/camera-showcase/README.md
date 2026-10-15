# Camera showcase generator

Source for the static page at `/camera-showcase/`. Jekyll ignores this folder because its name starts with an underscore.

- `targets.py`: the target lists (galaxies, star-forming galaxies, dust clouds). Each entry is a name, a SIMBAD-resolvable identifier or `"hh mm ss ±dd mm ss"`, a size note and a one-line description.
- `fetch2.py`: resolves the coordinates, downloads 40′ cutouts from CDS hips2fits, and computes the monthly dark-time visibility at the five LCO 1-m sites. It writes one 7-panel strip per field (colour, u, g, r, i, z, Y) and `targets.json`. Each band falls back from survey to survey; panels that use a stand-in survey are flagged in red.
- `credits.py`: survey acknowledgements and references.
- `build2.py`: renders the page, the CSV and `IMAGE_CREDITS.txt`.

## Regenerate

```bash
python3 -m venv venv && ./venv/bin/pip install numpy astropy pillow requests
mkdir -p /tmp/charts
./venv/bin/python fetch2.py /tmp/charts            # all fields; cached per field in /tmp/charts/<slug>.json
./venv/bin/python fetch2.py /tmp/charts G05 D17    # refetch only these fields
./venv/bin/python build2.py /tmp/charts ../../camera-showcase/index.html --standalone
cp /tmp/charts/[GSD][0-9][0-9].jpg ../../camera-showcase/charts/
```

Run the commands from this folder. Field IDs (`G05`, `S18`, `D21`, …) are the list prefix plus the position in that list. If you insert entries in the middle of a list, later IDs shift, so refetch everything after the insertion point.
