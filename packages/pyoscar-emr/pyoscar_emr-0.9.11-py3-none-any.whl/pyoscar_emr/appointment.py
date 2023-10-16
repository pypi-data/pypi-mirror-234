from dataclasses import dataclass
from datetime import datetime

from .appointment_status import AppointmentStatus
from .demographic import Demographic


@dataclass
class Appointment:
    """
    A class representing an appointment in the OSCAR EMR system.
    """

    name: str
    reason: str
    notes: str

    start_time: datetime
    end_time: datetime

    status: AppointmentStatus
    demographic: Demographic

    creator: str
    provider_id: int

    id: int

    @staticmethod
    def from_dict(raw_data: dict, status: AppointmentStatus, demographic: Demographic):
        """
        Create an instance of Appointment from the raw status information from the OSCAR REST API.

        Parameters
        --------------
        raw_info : dict
            the json object for an appointment from the OSCAR REST API
        status : AppointmentStatus
            the status of the appointment. This is a separate parameter as the necessary data to make this object cannot be made only using raw_data.
        demographic : Demographic
            the demographic associated with this appointment. This is a separate parameter as the necessary data to make this object cannot be made only using raw_data.
        """

        start_time = datetime.strptime(
            f"{raw_data.get('appointmentDate', '1970-01-01')} {raw_data.get('startTime', '12:00:00')}",
            "%Y-%m-%d %H:%M:%S",
        )
        end_time = datetime.strptime(
            f"{raw_data.get('appointmentDate', '1970-01-01')} {raw_data.get('endTime', '12:30:00')}",
            "%Y-%m-%d %H:%M:%S",
        )

        return Appointment(
            name=raw_data.get("name", ""),
            reason=raw_data.get("reason", ""),
            notes=raw_data.get("notes", ""),
            start_time=start_time,
            end_time=end_time,
            status=status,
            demographic=demographic,
            creator=raw_data.get("creator", ""),
            provider_id=int(raw_data.get("providerNo", 0)),
            id=raw_data.get("id", 0),
        )
