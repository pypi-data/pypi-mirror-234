class ExperimentNotFoundError(Exception):
    experiment_id: str

    def __init__(self, experiment_id: str):
        self.experiment_id = experiment_id
        self.message = f"Experiment with id {experiment_id} was not found."
        super().__init__(self.message)


class InvalidExperimentPromptData(Exception):
    def __init__(self, response_message: str):
        self.message = (
            f"Failed to run the experiment due to the invalid request parameters. "
            f"Response message: {response_message}"
        )
        super().__init__(self.message)
