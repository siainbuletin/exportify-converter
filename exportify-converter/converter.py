import argparse
from collections import namedtuple
import csv
import json
import os
from pathlib import Path
import re

import eyed3
from tqdm import tqdm


def setup_cli():
  parser = argparse.ArgumentParser(description="Exportify to M3U8 Converter CLI")
    
  parser.add_argument("-i", "--csv_file", type=Path, required=True, help="Path to the input playlist's CSV file")
  parser.add_argument("-o", "--m3u_file", type=Path, required=True, help="Path to the output playlist's M3U file")
  parser.add_argument("-m", "--music_library", type=Path, required=True, help="Path to the music library directory")
  parser.add_argument("-f", "--force", action="store_true", help="Allow overwriting existing output playlist file")
  
  args = parser.parse_args()

  # Check if CSV file exists
  if not Path(args.csv_file).is_file or not Path(args.csv_file).exists:
      raise ValueError(f"Input playlist's CSV file {args.csv_file} does not exist.")

  # Check if M3U file does not exist
  if (Path(args.m3u_file).is_file and Path(args.m3u_file).exists) and not args.force:
      raise ValueError("Output playlist's M3U file {args.m3u_file} already exists.")

  # Check if music directory exists
  if not Path(args.music_library).is_dir or not Path(args.music_library).exists:
      raise ValueError(f"Music library directory {args.music_library} does not exist.")
      
  return args

def read_input(input_path: Path, library_path: Path, settings):
  playlist_songs = []
  library_files = {}
  total_playlist_length = -1
  
  # Extract the Spotify ID from the ID3 Tag comment
  spotify_track_id_pattern = re.compile(r"id\[spotify\.com:track:(\w+)\]")
  
  # Get all the library files (MP3)
  file_list = list(Path(library_path).rglob(settings.library.file_glob))
  for file_path in tqdm(file_list, desc="Analyzing Music Library"):
    if file_path.is_file():
      # Extract the ID3 Metadata from the file
      audio_file = eyed3.load(file_path)
      comments = audio_file.tag.comments
      if comments:
        # Try to get the spotify ID from the comment
        match = spotify_track_id_pattern.search(comments[0].text)
        if match:
          # Build the library dictionary using the ID as key and file path as value
          library_files[match.group(1)] = file_path
          
  print("="*64)
  print(f"Found {len(library_files)} Spotify songs")
  print("="*64)
  
  # Read the playlist CSV file
  with open(input_path, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
    total_playlist_length = len(rows)
    for row in tqdm(rows, "Finding Playlist Songs in Music Library"):
      # For every song in the playlist, try to find the corresponding local file
      library_file = library_files.get(row.get(settings.input.spotify_id_header))
      if library_file:
        # If the local file exists, add it to the library
        playlist_songs.append(library_file)
  
  print("="*64)
  print(f"Found {len(playlist_songs)}/{total_playlist_length} songs")
  print("="*64)
  
  return playlist_songs

def write_output(output_path: Path, playlist_songs: list[Path], settings):
  output_path = Path(output_path)
  
  # Make sure the output file can be written to and has the right suffix
  output_path.parent.mkdir(parents=True, exist_ok=True)
  if output_path.suffix != settings.output.suffix:
    output_path = Path(output_path.stem).with_suffix(settings.output.suffix)
  
  # Write the file contents
  with open(output_path, "w", encoding="UTF-8") as f:
    for song in tqdm(playlist_songs, "Writing M3U Playlist"):
      f.write(f"{os.path.relpath(song, output_path.parent)}\n")
      
  print("="*64)
  print(f"Playlist was saved at: {args.m3u_file}")
  print("="*64)

def __custom_decoder(dict_):
  # Custom decoder to build an object from the JSON file
  return namedtuple('X', dict_.keys())(*dict_.values())

# Entry point
if __name__ == "__main__":
  # Setup the CLI and validate the inputs
  args = setup_cli()
  
  # Read settings
  with open(Path(__file__).parent / "settings.json", "r") as f:
    settings = json.load(f, object_hook=__custom_decoder)
  
  # Get the song files for the input playlist
  playlist_songs = read_input(args.csv_file, args.music_library, settings)
  
  # Write the m3u file
  write_output(args.m3u_file, playlist_songs, settings)
