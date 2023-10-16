from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OntarioHealthCard:
    """
    A class that represents an Ontario Health Card.

    Attributes
    ------------
    number : str
        The health card number. Kept as a string since there is no point as keeping it as a number, and to easily combine with version code.
    ver : str
        The version code of the health card. Can either be 0, 1, or 2 characters depending on the type of health card.
    """

    number: str
    ver: str

    def __str__(self):
        return self.number + self.ver


@dataclass(frozen=True)
class OntarioHealthCardStatus:
    """
    A class that represents the validation status of an Ontario Health Card.

    Attributes
    ------------
    valid : bool
        Whether the health card is valid / non-expired or not.
    code : int
        The response code from the validation service.
    expiration_date : datetime.datetime
        The expiration date of the health card.
    """

    valid: bool
    code: int
    expiration_date: datetime
