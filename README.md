# Exportify CSV to M3U Converter

This converter relies on [Onthespot](https://github.com/casualsnek/onthespot) metadata to create M3U playlist files from [Exportify](https://github.com/watsonbox/exportify) CSV files.

The converter will read through your music library and look for the Spotify ID in the MP3 ID3 tags. It will then match the Spotify ID found in your CSV file to a local MP3 file found on your local disk.

## Requirements

- Git
- Python 3.10
- [Poetry](https://python-poetry.org/)

## Installation

- Clone the repository
- Restore the dependencies using `poetry install`

## Usage

- Run the `converter.py` script using poetry:
  ```py
  poetry run python .\exportify_converter\converter.py -h
  ```

- Modify the converter's settings by editing the [`settings.json`](./exportify_converter/settings.json) file.
