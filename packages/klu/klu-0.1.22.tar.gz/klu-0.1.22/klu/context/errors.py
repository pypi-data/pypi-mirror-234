from klu.common.errors import BaseKluError


class ContextNotFoundError(BaseKluError):
    context_id: int

    def __init__(self, context_id):
        self.context_id = context_id
        self.message = f"Context with id {context_id} was not found."
        super().__init__(self.message)
