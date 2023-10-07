from klu.common.errors import BaseKluError


class AppNotFoundError(BaseKluError):
    app_id: str

    def __init__(self, app_id):
        self.app_id = app_id
        self.message = f"App with id {app_id} was not found."
        super().__init__(self.message)
