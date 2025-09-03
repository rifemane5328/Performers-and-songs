from typing import Optional

class SongWithNameAlreadyExists(Exception):
    def __str__(self):
        return "Song with the following name already exists"


class SongNotFound(Exception):
    def __str__(self):
        return "Song not found"


class InvalidSongDuration(Exception):
    def __init__(self, song_title: str, duration: str, album_title: str = None):
        self.album_title = album_title
        self.song_title = song_title
        self.duration = duration

    def __str__(self):
        base_msg = f"Invalid song duration '{self.duration}' "
        if self.song_title and self.album_title:
            base_msg += f"in song {self.song_title}, in album {self.album_title}"
        elif self.song_title:
            base_msg += f"in song '{self.song_title}'"
        elif self.album_title:
            base_msg += f"in album '{self.album_title}'"
        return base_msg + ". Expected format is minutes:seconds, for ex. '4:23'."
