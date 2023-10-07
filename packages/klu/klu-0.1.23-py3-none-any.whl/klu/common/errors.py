from typing import Optional


class BaseKluError(Exception):
    __suppress_context__ = True


class IdNotProvidedError(BaseKluError):
    def __init__(self):
        self.message = f"Received invalid parameters. id cannot be None. Please, provide a valid id."
        super().__init__(self.message)


class InstanceRelationshipNotFoundError(BaseKluError):
    def __init__(self, instance_name: str, message: str):
        self.message = f"One of the relationships for new {instance_name} was not found. Message from server: {message}"
        super().__init__(self.message)


class InstanceNotFoundError(BaseKluError):
    def __init__(self, instance_name: str, instance_id: str):
        self.message = f"{instance_name} with id {instance_id} was not found."
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class UnknownKluError(BaseKluError):
    def __init__(self, error_message: Exception):
        self.message = f"Unknown error in Klu SDK. Please contact the support team."

        if error_message:
            self.message = f"{self.message}\nError message: {str(error_message)}"

        super().__init__(self.message)


class UnknownKluAPIError(BaseKluError):
    def __init__(self, status: int, message: str):
        self.message = (
            f"Unknown error in Klu API.\nstatus_code: {status},\nmessage: {message}"
        )
        super().__init__(self.message)


class UnauthorizedError(BaseKluError):
    def __init__(self):
        self.message = (
            f"Wrong credentials used to access the API. "
            f"Please, check you set the correct API key or contact the support team."
        )
        super().__init__(self.message)


class InvalidApiMethodUsedError(BaseKluError):
    def __init__(self, status: int, message: str):
        self.message = (
            "Invalid API method used. This is the result of internal programming error."
            f"Please, contact Klu support team so we could fix this.\nstatus_code: {status},\nmessage: {message}"
        )
        super().__init__(self.message)


class InvalidDataSent(BaseKluError):
    def __init__(self, status: int, message: str):
        self.message = (
            "Invalid model data was sent for creation or update. This is most likely the result of internal error."
            f"Please, contact Klu support team so we could fix this.\nstatus_code: {status},\nmessage: {message}"
        )
        super().__init__(self.message)


class BadRequestAPIError(BaseKluError):
    def __init__(self, status: int, message: str):
        self.message = (
            f"BadRequest error in Klu API.\nstatus_code: {status},\nmessage: {message}"
        )
        super().__init__(self.message)


class InvalidUpdateParamsError(BaseKluError):
    def __init__(self):
        self.message = "No update params have been provided. At least one of parameters should be sent."
        super().__init__(self.message)


class NotSupportedError(BaseKluError):
    def __init__(self):
        self.message = "This method is not supported"
        super().__init__(self.message)
