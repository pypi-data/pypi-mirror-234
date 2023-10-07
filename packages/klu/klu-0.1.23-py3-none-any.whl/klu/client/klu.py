from klu.action.client import ActionsClient
from klu.app.client import AppsClient
from klu.context.client import ContextClient
from klu.data.client import DataClient
from klu.experiment.client import ExperimentClient
from klu.feedback.client import FeedbackClient
from klu.finetune.client import FineTunesClient
from klu.model.client import ModelsClient
from klu.session.client import SessionClient
from klu.workspace.client import WorkspaceClient


class Klu:
    def __init__(self, api_key: str):
        self.data = DataClient(api_key)
        self.models = ModelsClient(api_key)
        self.actions = ActionsClient(api_key)
        self.context = ContextClient(api_key)
        self.sessions = SessionClient(api_key)
        self.workspace = WorkspaceClient(api_key)
        self.finetune = FineTunesClient(api_key)
        self.experiments = ExperimentClient(api_key)
        self.apps = AppsClient(api_key)
        self.feedback = FeedbackClient(api_key)
