from klu.common.errors import BaseKluError


class WorkspaceOrUserNotFoundError(BaseKluError):
    def __init__(self):
        self.message = f"User was not found Workspace for current user was not found"
        super().__init__(self.message)
