# This project demonstrates dictionary concepts:
# - Lookup tables, nested dictionaries, counting patterns
# - Aggregation, filtering, sorting with lambda
# - Helper functions, file I/O, data processing

# ===== PART 1: Load Music Library from File =====
# Global constant to make conversions easier
SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60
# Global music library dictionary
music_library: dict[str, dict[str, any]] = {}


def load_music(filename: str) -> dict[str, dict]:
    """
    Load music library from a text file

    File format (pipe-delimited):
    Title|Artist|Duration(seconds)|Genre

    Returns dictionary with song titles as keys and nested dicts as values
    """
    music_library.clear()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            # Read file line by line
            for line in file:
                line = line.strip()
                if not line:
                    continue
                # Split each line by '|' and strip whitespace
                # Convert title to title case using .title()
                parts = line.split('|')
                parts[0].title()
                # Validate data (check for 4 parts, valid duration)
                if len(parts) == 4:
                    music_library[parts[0].title()] = {
                        "artist": parts[1],
                        "duration": int(parts[2]),
                        "genre": parts[3],
                        "play count": 0
                    }

            print(
                f"✅ Successfully loaded {len(music_library)} songs from {filename}")
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found!")
        print("Make sure the file is in the same folder as this script.")
    except Exception as e:
        print(f"❌ Error loading file: {e}")

    return music_library


def seconds_to_mmss(total_seconds: int) -> str:
    """Convert seconds to MM:SS format"""
    # Use SECONDS_IN_MINUTE constant
    # Handle negative numbers

    # Use // for minutes and % for seconds
    mins = abs(int(total_seconds)) // SECONDS_IN_MINUTE
    secs = abs(int(total_seconds)) % SECONDS_IN_MINUTE

    # Format seconds with leading zero if needed (:02d)
    mins_secs = f"{mins}:{secs:02d}"
    return mins_secs


def display_library() -> None:
    """Display all songs with their info and play counts"""

    # Print header with asterisks
    print("*" * 10, "MUSIC LIBRARY", "*" * 10)
    for song, value in music_library.items():
        # Print each value in music_library
        print(f"Title: {song}")
        print(f"\tartist: {value["artist"]:<20}", end="")
        print(f"duration: {seconds_to_mmss(value["duration"]):<10}\t", end="")
        print(f"genre: {value["genre"]:<10}", end="")

        # Check for play count, print "not played yet" if play count is below 1
        if value["play count"] > 0:
            print(f"\tplay count: {value["play count"]}")
        else:
            print(f"\tplay count: not played yet")



# ===== PART 2: Play Tracker =====
def play_song(song_title: str) -> None:
    """Play a song and increment its play count"""
    # Convert user input to title case to match dictionary keys
    titleSong = song_title.title()

    # Validate song exists (check if in music_library)
    if titleSong in music_library:
        for song, value in music_library.items():
            if song == titleSong:
                # Display "Now playing" message
                print(f"Now playing: {song} - {value["artist"]}")
                # Increment play count
                value["play count"] += 1
            else:
                continue


def get_played_songs() -> dict[str, dict]:
    """Get dictionary of songs that have been played

    HELPER FUNCTION - Returns data, doesn't display
    Returns: {song_title: full_song_data} for songs with play count > 0

    """
    # Use dictionary comprehension to filter
    # Return songs where data["play count"] > 0
    # Return the FULL data dict, not just the play count
    played_songs = {song: value for song, value in music_library.items() if value["play count"] > 0}
    return played_songs


def show_play_history() -> None:
    """Display all songs that have been played, sorted by play count"""
    # Get data using helper function: get_played_songs()
    # Check if empty (no songs played yet)
    if not get_played_songs():
        print("Nothing here")
        return

    # Sort by play count
    sorted_songs = sorted(
        get_played_songs().items(),
        key=lambda item: item[1]["play count"],
        reverse=True
    )
    # Display formatted results
    for song, value in sorted_songs:
        print(f"{song} - {value["play count"]} plays" if value[
        "play count"] > 1 else f"{song} - {value["play count"]} play")


# ===== PART 3: Statistics =====
def calculate_total_listening_time() -> tuple[int, int, int]:
    """Calculate total listening time, return (hours, minutes, seconds)"""

    # REUSE get_played_songs() helper function
    total_seconds = 0
    for song, value in get_played_songs().items():
        total_seconds += (value["play count"] * value["duration"])

    # Convert total_seconds to hours, minutes, seconds:
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    tuple_listening_time = (hours, minutes, seconds)
    return (
        f"Total listening time: {tuple_listening_time[0]} hours, {tuple_listening_time[1]} minutes, {tuple_listening_time[2]} seconds")


def get_genre_breakdown() -> dict[str, int]:
    """Return dictionary of genre: total_plays"""

    # REUSE get_played_songs() helper function
    # Need to create a NEW dictionary by grouping
    genre_dict = {}
    for song, value, in get_played_songs().items():
        genre = value["genre"]
        total_plays = value["play count"]

        # Loop through played songs, group by genre, sum play counts
        if genre in genre_dict:
            genre_dict[genre] += total_plays
        else:
            genre_dict[genre] = total_plays

    for genre, plays in genre_dict.items():
        print(f"{genre}: {plays} plays")


def calculate_average_song_length() -> float:
    """Return average song duration in seconds"""
    total_sum = 0
    # Sum all song durations from music_library
    for song, value in music_library.items():
        total_sum += value["duration"]

    # Divide by number of songs
    avg = (total_sum / len(music_library))
    return (f"Average Song Length: {avg:.2f} seconds")


def show_listening_stats() -> None:
    """Display all statistics in a nice format"""
    # Call calculate_total_listening_time() and display
    # Call calculate_average_song_length(), convert to MM:SS, and display
    # Call get_genre_breakdown() and display each genre with play count
    print("\n📊 LISTENING STATS\n━━━━━━━━━━━━━━━━━━━━━━")
    print(calculate_total_listening_time())
    print(calculate_average_song_length())
    get_genre_breakdown()


# ===== PART 4: Top Charts =====
def get_top_artist() -> tuple[str, int]:
    """Find artist with most total plays across all their songs

    HELPER FUNCTION - Returns data for use in show_top_charts()
    Returns: (artist_name, total_plays)

    Process:
    1. Loop through played songs
    2. Group by artist - create dict of {artist: total_plays}
    3. Find the max artist
    4. Return tuple of (artist_name, play_count)
    """

    grouped_artists = {}
    for song, value, in get_played_songs().items():
        artist = value["artist"]
        total_plays = value["play count"]
        grouped_artists[artist] = grouped_artists.get(artist, 0) + total_plays

    top_artist = max(grouped_artists.items(), key=lambda item: item[1])
    print(f"Top Artist: {top_artist[0]} ({top_artist[1]} total plays)")


def get_most_played_song() -> str:
    """Find and return the title of the most played song"""
    # Get played songs
    # Find song with highest play count
    # Return song title
    most_played = max(get_played_songs().items(), key=lambda item: item[1]["play count"])
    return f"Most Played: {most_played[0]} ({most_played[1]["play count"]} plays)"


def get_least_played_song() -> str:
    """Find and return the title of the least played song"""
    # Get played songs
    # Find song with lowest play count
    # Return song title
    least_played = min(get_played_songs().items(), key=lambda item: item[1]["play count"])
    return f"Least Played: {least_played[0]} ({least_played[1]["play count"]} plays)"


def songs_ranked_by_play_count() -> list[tuple[str, int]]:
    """Return list of (song, play_count) tuples sorted by play count"""

    # Sort by play count using sorted() with lambda
    sorted_songs = sorted(
        get_played_songs().items(),
        key=lambda item: item[1]["play count"],
        reverse=True
    )

    # Get played songs
    play_count_songs = []
    for song, value in sorted_songs:
        play_count_songs.append((song, value["play count"]))

    # Return list of tuples: [(song_title, play_count), ...]
    print(f"All Songs (Most to Least Played):")
    for song, value in sorted_songs:
        print(f"{song} - {value["artist"]}: {value["play count"]} plays")


def show_top_charts() -> None:
    """Display most/least played songs, top artist, and rankings"""

    print("\n🏆 YOUR TOP CHARTS\n━━━━━━━━━━━━━━━━━━━━━━")
    # Use get_top_artist() to get (artist, plays) tuple

    # Display all results in formatted output

    # Use get_most_played_song() to get most played
    print(get_most_played_song())
    # Use get_least_played_song() to get least played
    print(get_least_played_song())
    print()

    get_top_artist()
    print()
    # Use songs_ranked_by_play_count() to get ranked list
    songs_ranked_by_play_count()



# ===== MAIN PROGRAM =====
def main() -> None:
    # Load the music library
    load_music("songs_1998_txt.txt")

    print("🎵 MUSIC PLAYLIST ANALYZER 🎵")

    while True:
        print("\n[1] View Library")
        print("[2] Play Song")
        print("[3] Play History")
        print("[4] Listening Stats")
        print("[5] Top Charts")
        print("[6] Quit")

        choice = input("\nChoice: ")

        if choice == "1":
            display_library()
        elif choice == "2":
            song = input("What song do you want to play? ").strip().title()
            play_song(song)
        elif choice == "3":
            show_play_history()
        elif choice == "4":
            show_listening_stats()
        elif choice == "5":
            show_top_charts()
        elif choice == "6":
            break
        else:
            print(f"{choice} is not a valid option")
            continue


if __name__ == "__main__":
    main()
