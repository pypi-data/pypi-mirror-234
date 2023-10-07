from klu.common.errors import BaseKluError


class UnknownModelProviderError(BaseKluError):
    guid: str

    def __init__(self, guid):
        self.guid = guid
        self.message = (
            f"An unknown model or provider {self.guid} was used. "
            "Supported providers are [OpenAI, Azure OpenAI, Anthropic, GCP, NLPCloud, Cohere, AI21 & GooseAI]"
        )
        super().__init__(self.message)
