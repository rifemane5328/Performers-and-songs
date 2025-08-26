class AlbumWithNameAlreadyExists(Exception):
    def __str__(self):
        return "Album with the following name already exists"
