from dataclasses import dataclass
from datetime import datetime

from re import findall


@dataclass(frozen=True)
class Note:
    """
    A class representing a note in the OSCAR EMR system.
    """

    id: int

    observation_date: datetime
    update_date: datetime

    is_invoice: bool
    is_encounter_form: bool

    content: str

    # All of the raw JSON info, accessible for access since
    # a lot of the keys aren't attributes in this class
    # (deemed unnecessary / looks to have no info on current OSCAR
    # instance, but may be another story for another instance)
    raw_data: dict

    @staticmethod
    def from_dict(raw_data: dict):
        """
        Create an instance of Note from the raw information from the OSCAR REST API.

        Parameters
        --------------
        raw_info : dict
            the json object for a note from the OSCAR REST API
        """

        # Ensure data is not corrupt / invalid
        REQUIRED_KEYS = [
            "noteId",
            "observationDate",
            "updateDate",
            "note",
            "invoice",
            "encounterForm",
        ]
        for key in REQUIRED_KEYS:
            assert key in raw_data, f"Note data is corrupt, does not have key {key}"

        # These dates are given in milliseconds
        observation_date = datetime.fromtimestamp(
            int(raw_data["observationDate"]) / 1000
        )
        update_date = datetime.fromtimestamp(int(raw_data["updateDate"]) / 1000)

        is_invoice = bool(raw_data["invoice"])
        is_encounter_form = bool(raw_data["encounterForm"])
        assert not (
            is_invoice and is_encounter_form
        ), "Note data is corrupt, cannot be both invoice and encounter"

        return Note(
            id=int(raw_data["noteId"]),
            observation_date=observation_date,
            update_date=update_date,
            content=raw_data["note"],
            raw_data=raw_data,
            is_invoice=is_invoice,
            is_encounter_form=is_encounter_form,
        )

    @staticmethod
    def from_content(content: str):
        """
        Create an instance of Note just through the content. This only exists to allow one to
        easily create a note with content and have the EMR fill in the rest, and shouldn't really
        be used anywhere else.

        Parameters
        --------------
        content : str
            the text content of the note
        """

        return Note(
            id=0,
            observation_date=datetime.now(),
            update_date=datetime.now(),
            is_invoice=False,
            is_encounter_form=False,
            content=content,
            raw_data={}
        )


@dataclass(frozen=True)
class InvoiceNote(Note):
    """
    A class representing an invoice note in the OSCAR EMR system.
    """

    billing_codes: list[str]
    provider_id: int

    @staticmethod
    def from_dict(raw_data: dict):
        """
        Create an instance of InvoiceNote from the raw information from the OSCAR REST API.

        Parameters
        --------------
        raw_info : dict
            the json object for a note from the OSCAR REST API
        """

        # Ensure data is not corrupt / invalid
        REQUIRED_KEYS = [
            "noteId",
            "observationDate",
            "updateDate",
            "providerNo",
            "note",
            "invoice",
        ]
        for key in REQUIRED_KEYS:
            assert key in raw_data, f"Note data is corrupt, does not have key {key}"

        # Doing an explicit comparison since it needs to just be "True",
        # not a random truthy value
        assert raw_data["invoice"] == True, "Raw data does not represent an invoice"

        # These dates are given in milliseconds
        observation_date = datetime.fromtimestamp(
            int(raw_data["observationDate"]) / 1000
        )
        update_date = datetime.fromtimestamp(int(raw_data["updateDate"]) / 1000)

        # Ensure that note is of correct format (or more specifically, has the correct keywords)
        assert (
            " billed by " in raw_data["note"]
        ), "Note does not include billing code info"

        # Extract billing codes from note
        billing_codes = findall(r"[A-Z][0-9]{3}[AB]", raw_data["note"])

        return InvoiceNote(
            id=int(raw_data["noteId"]),
            observation_date=observation_date,
            update_date=update_date,
            provider_id=int(raw_data["providerNo"]),
            content=raw_data["note"],
            raw_data=raw_data,
            is_encounter_form=False,
            is_invoice=True,
            billing_codes=billing_codes,
        )
