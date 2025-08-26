class AlbumWithNameAlreadyExists(Exception):
    def __str__(self):
        return "Album with the following name already exists"


class AlbumNotFound(Exception):
    def __str__(self):
        return "Album not found"
