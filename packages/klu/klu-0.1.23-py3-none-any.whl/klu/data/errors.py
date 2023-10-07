from klu.common.errors import BaseKluError


class DataNotFoundError(BaseKluError):
    datum_id: int

    def __init__(self, datum_id):
        self.datum_id = datum_id
        self.message = f"Data with id {datum_id} was not found."
        super().__init__(self.message)
