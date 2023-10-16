from dataclasses import dataclass


@dataclass(frozen=True)
class AppointmentStatus:
    """
    A class representing the status of an appointment.
    """

    active: bool
    color: str
    description: str
    editable: bool
    short_letters: str
    key: str
    id: int
    signed: bool

    @staticmethod
    def from_dict(raw_data: dict):
        """
        Create an instance of AppointmentStatus from the raw status information from the OSCAR REST API.

        Parameters
        --------------
        raw_data : dict
            the json object for an appointment status from the OSCAR REST API
        """

        # Check whether signed by looking at last character
        signed = False
        key = raw_data.get("status", "?")
        if len(key) > 1 and key[-1] == "S":
            signed = True
            key = key[:-1]

        return AppointmentStatus(
            active=bool(raw_data.get("active", 0)),
            color=raw_data.get("color", "#000000"),
            description=raw_data.get("description", "?"),
            editable=bool(raw_data.get("editable", 0)),
            short_letters=raw_data.get("shortLetters", "?"),
            key=key,
            id=raw_data.get("id", 0),
            signed=signed,
        )

    def __str__(self):
        return self.description
