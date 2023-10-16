from dataclasses import dataclass
from .response_type import ResponseType


@dataclass(frozen=True)
class APIEndpoint:
    url: str
    response_type: ResponseType


@dataclass(frozen=True)
class WebScrapingEndpoint:
    url: str


@dataclass()
class APIEndpoints:
    """
    A class used to store all of the endpoints that are needed for using the OSCAR REST API.
    """

    appt: APIEndpoint
    demographic_id: APIEndpoint
    demographic_hin: APIEndpoint
    appt_history: APIEndpoint
    appt_statuses: APIEndpoint
    provider_monthly_appts: APIEndpoint
    appt_status_update: APIEndpoint
    demographic_notes: APIEndpoint

    def __init__(self, base_url: str):
        self.base_url = base_url

        # GET
        self.provider_monthly_appts = APIEndpoint(
            self.base_url
            + "/oscar/ws/services/schedule/fetchMonthly/{provider_id}/{year}/{month}",
            ResponseType.JSON,
        )
        self.demographics = APIEndpoint(
            self.base_url
            + "/oscar/ws/services/demographics?offset={offset}&limit={limit}",
            ResponseType.XML,
        )
        self.demographic_id = APIEndpoint(
            self.base_url + "/oscar/ws/services/demographics/{id}",
            ResponseType.JSON,
        )
        self.demographic_hin = APIEndpoint(
            self.base_url
            + "/oscar/ws/services/demographics/search?startIndex=0&itemsToReturn={itemsToReturn}",
            ResponseType.JSON,
        )
        self.appt_statuses = APIEndpoint(
            self.base_url + "/oscar/ws/services/schedule/statuses",
            ResponseType.JSON,
        )

        # POST
        self.appt = APIEndpoint(
            self.base_url + "/oscar/ws/services/schedule/getAppointment",
            ResponseType.JSON,
        )
        self.appt_history = APIEndpoint(
            self.base_url
            + "/oscar/ws/services/schedule/{demographic_id}/appointmentHistory",
            ResponseType.JSON,
        )
        self.appt_status_update = APIEndpoint(
            self.base_url + "/oscar/ws/services/schedule/appointment/{id}/updateStatus",
            ResponseType.JSON,
        )
        self.demographic_notes = APIEndpoint(
            self.base_url + "/oscar/ws/services/notes/{demographic_id}/all",
            ResponseType.JSON,
        )
        self.save_encounter_note = APIEndpoint(
            self.base_url + "/oscar/ws/services/notes/{demographic_id}/saveIssueNote",
            ResponseType.JSON,
        )


@dataclass()
class WebScrapingEndpoints:
    """
    A class used to store all of the endpoints that are needed for interact and scrape the OSCAR EMR web interface.
    """

    login: WebScrapingEndpoint
    card_swipe: WebScrapingEndpoint
    update_appt: WebScrapingEndpoint

    def __init__(self, base_url: str):
        self.base_url = base_url

        self.login = WebScrapingEndpoint(
            self.base_url + "/oscar/index.jsp",
        )

        self.card_swipe = WebScrapingEndpoint(
            self.base_url + "/CardSwipe/?hc={health_card_number}%20{health_card_ver}",
        )

        self.update_appt = WebScrapingEndpoint(
            self.base_url
            + "/oscar/appointment/appointmentcontrol.jsp?appointment_no={id}&demographic_no={demographic_no}&displaymode=edit"
        )
