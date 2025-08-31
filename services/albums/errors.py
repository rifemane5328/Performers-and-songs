class AlbumWithNameAlreadyExists(Exception):
    def __str__(self):
        return "Album with the following name already exists"


class AlbumNotFound(Exception):
    def __str__(self):
        return "Album not found"


class AlbumMustContainSongs(Exception):
    def __str__(self):
        return "Album must contain at least one song"
