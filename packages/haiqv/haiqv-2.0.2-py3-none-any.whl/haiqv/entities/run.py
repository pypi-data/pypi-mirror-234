class Run:
    def __init__(
            self,
            id,
            name=None,
    ):
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
