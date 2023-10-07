class HaiqvValueError(Exception):
    def __init__(self, error: dict):
        self.error = error

    def __str__(self):
        return str(self.error)

    def get_error(self):
        return self.error