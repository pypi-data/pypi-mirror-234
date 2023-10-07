class Experiment:
    def __init__(
            self,
            experiment_id: str,
            lifecycle_stage='',
    ):
        self._experiment_id = experiment_id
        self._lifecycle_stage = lifecycle_stage

    @property
    def experiment_id(self):
        return self._experiment_id

    @property
    def lifecycle_stage(self):
        return self._lifecycle_stage
