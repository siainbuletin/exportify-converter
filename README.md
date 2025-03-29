[#](#.md) Exportify CSV to M3U Converter

Scope: create a reliable Spotify (and other sources converter) to input playlists to a centralised repository. (Ideal: load everything into beets, using a framework like `beets-yapl`).

Converter forked from `po-trottier/exportify-converter` relies on [Onthespot](https://github.com/casualsnek/onthespot) metadata to create M3U playlist files from [Exportify](https://github.com/watsonbox/exportify) CSV files.

The converter will read through your music library and look for the Spotify ID in the MP3 ID3 tags. It will then match the Spotify ID found in your CSV file to a local MP3 file found on your local disk.

## dependencies of the converter

- Git
- Python 3.10
- https://python-poetry.org/

---

# Installation

- Clone the repository
- Restore the dependencies using `poetry install`

---

## Usage

- see the docs / typst source to understand the inner functionality
TODO: add literate documentation on the parts of code.

- Run the `converter.py` script using poetry:
  ```py
  poetry run python .\exportify_converter\converter.py -h
  ```

- Modify the converter's settings by editing the [`settings.json`](./exportify_converter/settings.json) file.

---
# To Do
- need to figure out path handling for the songs
  - could be done relative to a NAS unit
- change the music ID to something like AcoustID
