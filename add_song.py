import os
import AudioModule
import DBModule

def add_song_to_database(song_path, song_id, song_name, artist, album, release_date):
    """Adds a song's fingerprint to the database."""
    pointer = AudioModule.GenerateConstellationMap(song_path, song_id, 0)
    addresses, couples = DBModule.GenerateAddressCoupleDB("SampleFingerprint.txt", song_id)
    
    try:
        fingerprint_db = DBModule.LoadHashTable("fingerprintDatabase")
    except FileNotFoundError:
        fingerprint_db = {}
    
    DBModule.AddToFingerprintTable(addresses, couples, fingerprint_db)
    DBModule.SaveHashTable(fingerprint_db, "fingerprintDatabase")
    
    # Add song metadata
    try:
        song_map = DBModule.LoadHashTable("songMap")
    except FileNotFoundError:
        song_map = {}
    
    song_map[format(song_id, '032b')] = [song_name, artist, album, release_date]
    DBModule.SaveHashTable(song_map, "songMap")
    print(f"Song '{song_name}' added to the database.")

def detect_song_from_database(audio_path):
    """Detects a song from the database and prints the result."""
    try:
        fingerprint_db = DBModule.LoadHashTable("fingerprintDatabase")
    except FileNotFoundError:
        print("Fingerprint database not found. Add songs first.")
        return
    
    pointer = AudioModule.GenerateConstellationMap(audio_path, 1, 0)
    song_metadata = DBModule.SearchDatabase(10, fingerprint_db)
    
    if song_metadata:
        print(f"Detected Song: {song_metadata[0]} by {song_metadata[1]}")
        if song_metadata[2] != "Single":
            print(f"Album: {song_metadata[2]}")
        print(f"Release Date: {song_metadata[3]}")
    else:
        print("No matching song found.")

# Example Usage
if __name__ == "__main__":
    mode = input("Enter 'add' to add a song or 'detect' to identify a song: ").strip().lower()
    if mode == 'add':
        song_path = input("Enter the path to the song (WAV file): ").strip()
        song_id = int(input("Enter a unique song ID: ").strip())
        song_name = input("Enter song name: ").strip()
        artist = input("Enter artist name: ").strip()
        album = input("Enter album name (or 'Single' if none): ").strip()
        release_date = input("Enter release date: ").strip()
        add_song_to_database(song_path, song_id, song_name, artist, album, release_date)
    elif mode == 'detect':
        audio_path = input("Enter the path to the recorded audio (WAV file): ").strip()
        detect_song_from_database(audio_path)
    else:
        print("Invalid input. Use 'add' or 'detect'.")
