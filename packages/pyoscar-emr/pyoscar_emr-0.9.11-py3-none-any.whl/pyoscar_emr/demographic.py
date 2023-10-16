from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from xml.etree import ElementTree

import re

from .ontario_health_card import OntarioHealthCard


class PatientStatus(Enum):
    ACTIVE = 1
    INACTIVE = 2
    DECEASED = 3
    MOVED = 4
    FIRED = 5
    UNKNOWN = 6


class EnrollmentStatus(Enum):
    ENROLLED = 1
    NOT_ENROLLED = 2
    TERMINATED = 3
    FEE_FOR_SERVICE = 4
    UNKNOWN = 5


def convert_key_to_patient_status(key: str) -> PatientStatus:
    mapping = {
        "AC": PatientStatus.ACTIVE,
        "IN": PatientStatus.INACTIVE,
        "DE": PatientStatus.DECEASED,
        "MO": PatientStatus.MOVED,
        "FI": PatientStatus.FIRED,
    }

    return mapping.get(key, PatientStatus.UNKNOWN)


def convert_key_to_enrollment_status(key: str) -> EnrollmentStatus:
    mapping = {
        "EN": EnrollmentStatus.ENROLLED,
        "NE": EnrollmentStatus.NOT_ENROLLED,
        "TE": EnrollmentStatus.TERMINATED,
        "FS": EnrollmentStatus.FEE_FOR_SERVICE,
    }

    return mapping.get(key, EnrollmentStatus.UNKNOWN)


@dataclass
class Demographic:
    """
    A class representing a demographic (patient) in the OSCAR EMR system.
    """

    first_name: str
    last_name: str
    id: int
    date_of_birth: datetime
    sex: str

    address: str
    city: str
    province: str
    postal_code: str

    health_card: OntarioHealthCard

    phone_numbers: list[str]
    email: str

    patient_status: PatientStatus
    enrollment_status: EnrollmentStatus

    @staticmethod
    def from_dict(raw_data: dict):
        """
        Create an instance of Demographic from the raw status information from the OSCAR REST API.

        Parameters
        --------------
        raw_info : dict
            the json object for a demographic from the OSCAR REST API
        """

        birth_year = raw_data.get("dobYear", 1970)
        birth_month = raw_data.get("dobMonth", 1)
        birth_day = raw_data.get("dobDay", 1)
        date_of_birth = datetime.strptime(
            f"{birth_year}-{birth_month}-{birth_day}", "%Y-%m-%d"
        )

        hin = raw_data.get("hin", "")
        ver = raw_data.get("ver", "")

        health_card = None
        if "" not in [hin, ver]:
            health_card = OntarioHealthCard(hin, ver)

        # Get all possible phone numbers
        tmp_extra_number = [
            prop for prop in raw_data["extras"] if prop["key"] == "demo_cell"
        ]
        tmp_phone_numbers: list[str] = [
            raw_data["phone"],
            raw_data["alternativePhone"],
            tmp_extra_number[0]["value"] if len(tmp_extra_number) != 0 else "",
        ]
        phone_numbers = [
            re.sub("[^0-9]", "", phone_number)
            for phone_number in tmp_phone_numbers
            if phone_number != ""
        ]

        # Extract address data if it exists
        address = ""
        city = ""
        province = ""
        postal_code = ""
        if "address" in raw_data:
            address = raw_data["address"]["address"]
            city = raw_data["address"]["city"]
            province = raw_data["address"]["province"]
            postal_code = raw_data["address"]["postal"]

        patient_status = convert_key_to_patient_status(
            raw_data.get("patientStatus", "")
        )
        enrollment_status = convert_key_to_enrollment_status(
            raw_data.get("rosterStatus", "")
        )

        return Demographic(
            first_name=raw_data["firstName"],
            last_name=raw_data["lastName"],
            id=raw_data["demographicNo"],
            date_of_birth=date_of_birth,
            sex=raw_data["sex"],
            address=address,
            city=city,
            province=province,
            postal_code=postal_code,
            health_card=health_card,
            phone_numbers=phone_numbers,
            email=raw_data["email"],
            patient_status=patient_status,
            enrollment_status=enrollment_status,
        )

    @staticmethod
    def from_xml(raw_xml: ElementTree.Element):
        """
        Create an instance of Demographic using XML from the OSCAR REST API.

        Parameters
        --------------
        raw_xml : dict
            the XML data for a demographic from the OSCAR REST API
        """

        assert (
            raw_xml.get("{http://www.w3.org/2001/XMLSchema-instance}type")
            == "demographicTo1"
        ), "XML element is not of correct type"

        first_name = raw_xml.find(".//firstName").text
        last_name = raw_xml.find(".//lastName").text
        demographic_id = int(raw_xml.find(".//demographicNo").text)

        birth_date = raw_xml.find(".//dateOfBirth").text
        sex = node.text if ((node := raw_xml.find(".//sex")) != None) else ""

        address = node.text if ((node := raw_xml.find(".//address")) != None) else ""
        city = node.text if ((node := raw_xml.find(".//city")) != None) else ""
        province = node.text if ((node := raw_xml.find(".//province")) != None) else ""
        postal_code = node.text if ((node := raw_xml.find(".//postal")) != None) else ""

        hin = raw_xml.find(".//hin").text
        ver = raw_xml.find(".//ver").text
        health_card = None
        if "" not in [hin, ver]:
            health_card = OntarioHealthCard(hin, ver)

        phone_numbers = [num] if (num := raw_xml.find(".//phone").text) != None else []
        email = node.text if ((node := raw_xml.find(".//email")) != None) else ""

        patient_status = convert_key_to_patient_status(
            node.text if ((node := raw_xml.find(".//patientStatus")) != None) else ""
        )

        roster_status_text = (
            node.text if ((node := raw_xml.find(".//rosterStatus")) != None) else ""
        )
        enrollment_status = EnrollmentStatus.UNKNOWN
        if roster_status_text == "RO":
            enrollment_status = EnrollmentStatus.ENROLLED

        date_of_birth = datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S%z")

        return Demographic(
            first_name=first_name,
            last_name=last_name,
            id=demographic_id,
            date_of_birth=date_of_birth,
            sex=sex,
            address=address,
            city=city,
            province=province,
            postal_code=postal_code,
            health_card=health_card,
            phone_numbers=phone_numbers,
            email=email,
            patient_status=patient_status,
            enrollment_status=enrollment_status,
        )
