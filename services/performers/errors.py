class PerformerWithNameAlreadyExists(Exception):
    def __str__(self):
        return "Performer with the following name already exists"
