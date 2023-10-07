class ActionNotFoundError(Exception):
    action_id: str

    def __init__(self, action_id: str):
        self.action_id = action_id
        self.message = f"Action with id {action_id} was not found."
        super().__init__(self.message)


class InvalidActionPromptData(Exception):
    def __init__(self, response_message: str):
        self.message = (
            f"Failed to run the action due to the invalid request parameters. "
            f"Response message: {response_message}"
        )
        super().__init__(self.message)
