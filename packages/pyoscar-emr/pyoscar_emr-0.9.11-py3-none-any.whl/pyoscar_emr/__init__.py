from .oscar import OscarAPI
from .appointment_status import AppointmentStatus
from .ontario_health_card import OntarioHealthCard
from .response_type import ResponseType
from .endpoints import APIEndpoints, APIEndpoint

if __name__ == "__main__":
    from .util.get_oauth_creds import main as get_oauth_creds

    get_oauth_creds()
