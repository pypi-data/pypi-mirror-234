from klu.common.errors import BaseKluError


class FeedbackNotFoundError(BaseKluError):
    feedback_id: int

    def __init__(self, feedback_id: int):
        self.feedback_id = feedback_id
        self.message = f"Feedback with id {feedback_id} was not found."
        super().__init__(self.message)
