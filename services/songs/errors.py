class SongWithNameAlreadyExists(Exception):
    def __str__(self):
        return "Song with the following name already exists"
