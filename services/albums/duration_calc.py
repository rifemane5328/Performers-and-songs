def parse_song_length(song_length: str) -> int:
    try:
        minutes, seconds = map(int, song_length.split(":"))
        if minutes < 0 or seconds < 0 or seconds >= 60:
            raise ValueError("Invalid song length")
        return minutes * 60 + seconds
    except ValueError:
        raise ValueError(f"Invalid duration format: {song_length}")


def convert_song_length(seconds: int) -> str:
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02d}"


def calculate_album_duration(songs_durations: list[str]) -> str:
    total_seconds = sum(parse_song_length(song) for song in songs_durations)
    return convert_song_length(total_seconds)
