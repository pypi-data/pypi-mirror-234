import asyncio
import json
from datetime import datetime
import logging
from xml.etree import ElementTree
import re
import aiohttp

from playwright.async_api import BrowserType
from playwright_stealth import stealth_async

import oauthlib.oauth1

from .endpoints import (
    APIEndpoints,
    APIEndpoint,
    WebScrapingEndpoints,
)
from .response_type import ResponseType
from .appointment_status import AppointmentStatus
from .appointment import Appointment
from .demographic import Demographic
from .ontario_health_card import OntarioHealthCard, OntarioHealthCardStatus
from .notes import Note, InvoiceNote
from .exceptions import (
    OscarAPIInvalidCredentials,
    OscarAPIWebScrapingNotEnabled,
    OscarAPIWebScrapingError,
)


class OscarAPI:
    """
    A wrapper on the OSCAR EMR REST API.
    """

    def __init__(
        self,
        base_url: str,
        oauth_secret: str,
        oauth_token: str,
        client_key: str,
        client_secret: str,
        session: aiohttp.ClientSession,
    ):
        """
        The constructor for OscarAPI. You should seriously be running OscarAPI.create() instead, as
        it runs any necessary functions (ex. getting appointment statuses) that this function cannot
        due to asynchronous behavior.
        """

        self._endpoint = APIEndpoints(base_url=base_url)
        self._endpoint_webscraping = WebScrapingEndpoints(base_url=base_url)
        self._session = session

        self._oauth_secret = oauth_secret
        self._oauth_token = oauth_token
        self._client_key = client_key
        self._client_secret = client_secret

        self._oauth_client = oauthlib.oauth1.Client(
            client_key=self._client_key,
            client_secret=self._client_secret,
            resource_owner_key=self._oauth_token,
            resource_owner_secret=self._oauth_secret,
        )

        self._statuses = (
            {}
        )  # This should be run at least once. If you are running this initializer directly,
        #    please run get_appointment_statuses()

        self._demographics_cache = {0: None}

        self.webscrapping_enabled = False

        # Set up logging without interefering with main progrma
        self._log = logging.getLogger(__name__)
        self._log.addHandler(logging.NullHandler())

    @staticmethod
    async def create(
        base_url: str,
        oauth_secret: str,
        oauth_token: str,
        client_key: str,
        client_secret: str,
        session: aiohttp.ClientSession,
    ):
        """
        Creates an instance of OscarAPI and runs all necessary functions to properly
        initialize (ex. fetching all appointment statuses).
        """

        self = OscarAPI(
            base_url=base_url,
            oauth_secret=oauth_secret,
            oauth_token=oauth_token,
            client_key=client_key,
            client_secret=client_secret,
            session=session,
        )

        self._statuses = await self.get_appointment_statuses()

        return self

    async def activate_webscraping(
        self,
        username: str,
        password: str,
        pin: str,
        browser_type: BrowserType,
        headless: bool = True,
    ) -> None:
        """
        Set up web scraping and enable functions that require it (ex. checking if health card is valid).
        Please note that the playwright context should always be alive.
        Raises OscarAPIInvalidCredentials if the credentials were invalid.
        """

        # Log into OSCAR
        self.playwright_browser = await browser_type.launch(headless=headless)
        page = await self.playwright_browser.new_page()
        await stealth_async(page)
        await page.goto(self._endpoint_webscraping.login.url)

        # Interact with login form
        await page.get_by_placeholder("Username:").fill(username)
        await page.get_by_placeholder("Password:").fill(password)
        await page.get_by_placeholder("PIN:").fill(pin)

        await page.get_by_role("button", name="Sign In").click()
        await page.wait_for_load_state("networkidle")

        if "login=failed" in page.url:
            await page.close()
            self._log.error("Login credentials for web scrapping are incorrect.")
            raise OscarAPIInvalidCredentials(
                "Login credentials for web scrapping are incorrect."
            )

        self.playwright_storage_state = await page.context.storage_state()
        await page.close()

        # Keep a page open so the browser doesn't close
        self.playwright_context = await self.playwright_browser.new_context(
            storage_state=self.playwright_storage_state
        )
        await self.playwright_context.new_page()

        self.webscrapping_enabled = True
        self._log.info("Webscrapping capabilities has been enabled.")

    async def _to_format(self, response: aiohttp.ClientResponse, endpoint: APIEndpoint):
        if endpoint.response_type == ResponseType.JSON:
            return await response.json()
        if endpoint.response_type == ResponseType.XML:
            return ElementTree.fromstring(await response.text())

        return None

    async def _get(self, endpoint: APIEndpoint, **kwargs):
        # Sign with OAuth1 credentials
        uri, headers, _ = self._oauth_client.sign(
            # Add necessary variables to endpoint URL
            uri=endpoint.url.format(**kwargs),
            http_method="GET",
        )

        async with self._session.get(
            uri, headers=headers, raise_for_status=True
        ) as response:
            return await self._to_format(response=response, endpoint=endpoint)

    async def _post(self, endpoint: APIEndpoint, body: dict | None, **kwargs):
        # Sign with OAuth1 credentials
        uri, headers, _ = self._oauth_client.sign(
            uri=endpoint.url.format(**kwargs),
            http_method="POST",
            headers={
                "Content-Type": "application/json" if isinstance(body, dict) else "0"
            },
        )

        data = json.dumps(body) if isinstance(body, dict) else ""

        async with self._session.post(
            uri, data=data, headers=headers, raise_for_status=True
        ) as response:
            return await self._to_format(response=response, endpoint=endpoint)

    async def get_appointment_statuses(
        self, force_refresh: bool = False
    ) -> dict[str, AppointmentStatus]:
        """
        Gets all possible appointment statuses in the OSCAR EMR instance.

        Returns a dictionary, where key -> status attribute of AppointmentStatus,
        and value -> AppointmentStatus object.
        """

        # Return cached version whenever possible
        if not force_refresh and len(self._statuses) != 0:
            return self._statuses

        res_data = await self._get(self._endpoint.appt_statuses)
        assert isinstance(res_data, dict)

        raw_statuses = res_data["content"]
        # Convert the list into a dict, where "status" attr is key for each status
        statuses = {
            status["status"]: AppointmentStatus.from_dict(status)
            for status in raw_statuses
        }

        return statuses

    async def get_appointment_from_id(self, id: int):
        """
        Gets an Appointment from its ID.

        Returns an Appointment.

        Will raise an aiohttp exception if no such appointment exists.
        """

        res_data = await self._post(self._endpoint.appt, {"id": id})
        assert isinstance(res_data, dict)
        assert "appointment" in res_data

        appt_data = res_data["appointment"]

        # Ignore signature on status
        status_key = appt_data["status"]
        if len(status_key) != 1 and status_key[-1] == "S":
            status_key = status_key.removesuffix("S")

        return Appointment.from_dict(
            appt_data,
            self._statuses.get(status_key),
            await self.get_demographic_by_id(appt_data["demographicNo"]),
        )

    async def get_appointments_from_date(
        self, date: datetime, provider_id: int
    ) -> list[Appointment]:
        """
        Gets a list of appointments that a provider has on a specific day.
        """

        month = date.month - 1  # Months in Oscar look to start from 0
        year = date.year

        res_data = await self._get(
            self._endpoint.provider_monthly_appts,
            provider_id=provider_id,
            year=year,
            month=month,
        )
        assert isinstance(res_data, dict)
        assert "appointments" in res_data

        monthly_appts = res_data["appointments"]
        # Filter to only get appointments on the specific date
        daily_appts_raw = [
            appt
            for appt in monthly_appts
            if appt.get("appointmentDate", "") == date.strftime("%Y-%m-%d")
        ]

        # Cache all demographic objects in unordered fashion
        demographic_nos = [
            appt_data["demographicNo"]
            for appt_data in daily_appts_raw
            if appt_data["demographicNo"] != 0
        ]
        demo_tasks = [
            asyncio.create_task(self.get_demographic_by_id(id=demo_no))
            for demo_no in demographic_nos
        ]
        if len(demo_tasks) > 0:
            await asyncio.wait(demo_tasks)

        # Convert raw appt data to Appointment objects
        appts = []
        for appt_data in daily_appts_raw:
            assert "status" in appt_data
            assert "demographicNo" in appt_data

            # Ignore signature on status
            status_key = appt_data["status"]
            if len(status_key) != 1 and status_key[-1] == "S":
                status_key = status_key.removesuffix("S")

            appts.append(
                Appointment.from_dict(
                    appt_data,
                    self._statuses.get(status_key),
                    await self.get_demographic_by_id(appt_data["demographicNo"]),
                )
            )

        return appts

    async def update_appointment_status(
        self, appt: Appointment, status: AppointmentStatus
    ) -> Appointment:
        """
        Updates the status of an appointment.

        Returns the new appointment after the update.

        Will raise an aiohttp exception if the appointment does not exist.
        """

        res_data = await self._post(
            self._endpoint.appt_status_update, body={"status": status.key}, id=appt.id
        )
        assert isinstance(res_data, dict)

        # Convert new data to an Appointment
        appt_data = res_data["appointment"]
        assert "status" in appt_data, "Appointment data is corrupt (no status key)"
        assert (
            "demographicNo" in appt_data
        ), "Appointment data is corrupt (no demographic id)"

        appt = Appointment.from_dict(
            appt_data,
            self._statuses.get(appt_data["status"]),
            await self.get_demographic_by_id(appt_data["demographicNo"]),
        )

        return appt

    async def get_all_demographics(
        self, chunk_size: int = 500, begin_offset: int = 0
    ) -> list[Demographic]:
        """
        Get all the Demographics stored in an OSCAR instance.

        Returns a list of Demographics.
        """

        # Get total number of demographics
        data: ElementTree.Element = await self._get(
            self._endpoint.demographics, offset=0, limit=1
        )
        demo_count = int(data.find(".//total").text)
        assert (
            begin_offset < demo_count
        ), "Begin offset larger than total # of demographics"

        # Asynchronously get all the demographics by chunking requests
        async def get_partial_demos(offset: int):
            tmp_data: ElementTree.Element = await self._get(
                self._endpoint.demographics,
                offset=offset,
                limit=chunk_size,  # 500 is maximum it can chunk
            )
            return [
                Demographic.from_xml(demo_data)
                for demo_data in tmp_data.findall(".//Item")
            ]

        coros = [
            get_partial_demos(offset=offset)
            for offset in range(begin_offset, demo_count, chunk_size)
        ]
        demo_partials = await asyncio.gather(*coros)
        demographics = [demo for partial in demo_partials for demo in partial]

        return demographics

    async def get_demographic_by_id(
        self, id: int, force_refresh: bool = False
    ) -> Demographic:
        """
        Get a Demographic from its ID / number.

        Returns a Demographic.

        Will raise an aiohttp exception if no such demographic exists.
        """

        if id in self._demographics_cache and not force_refresh:
            return self._demographics_cache[id]

        data = await self._get(self._endpoint.demographic_id, id=id)
        assert isinstance(data, dict)
        demographic = Demographic.from_dict(data)

        self._demographics_cache[id] = demographic
        return demographic

    async def get_demographic_by_hin(self, hin: str) -> Demographic:
        """
        Get a Demographic from the person's Health Insurance Number (HIN)

        Retruns a Demographic if one is found, otherwise returns None.
        """

        data = await self._post(
            self._endpoint.demographic_hin,
            {
                "type": "HIN",
                "term": hin,
                "active": True,
                "integrator": True,  # Check if this is necessary
                "outofdomain": False,
            },
            itemsToReturn=2,
        )
        assert isinstance(data, dict)

        # Check if only one thing was fetched (if there's two, there's a different problem)
        assert data["total"] <= 1, "More than two demographics found with same HIN"
        if data["total"] != 1 or len(data["content"]) != 1:
            return None

        # Get demographic no
        # TODO: Consider adding caching of HIN to Demographic No?
        demographic_no: int = data["content"][0]["demographicNo"]
        assert isinstance(demographic_no, int), "Demographic No is corrupt (not an int)"

        # Get demographic data using demo no
        demographic = await self.get_demographic_by_id(demographic_no)

        # Return demographic data
        return demographic

    async def get_appointment_history(
        self, demographic: Demographic
    ) -> list[Appointment]:
        """
        Get a demographic's appointment history.

        Returns a list of all of the demographic's appointments.
        """

        data = await self._post(
            self._endpoint.appt_history, None, demographic_id=demographic.id
        )
        assert isinstance(data, dict)

        appt_history = []
        for appt_data in data["appointments"]:
            assert "status" in appt_data
            assert "demographicNo" in appt_data

            # Ignore signature on status
            status_key = appt_data["status"]
            if len(status_key) != 1 and status_key[-1] == "S":
                status_key = status_key.removesuffix("S")

            appt_history.append(
                Appointment.from_dict(
                    appt_data,
                    self._statuses.get(status_key),
                    demographic,
                )
            )

        return appt_history

    async def get_demographic_notes(self, demographic: Demographic) -> list[Note]:
        """
        Get a demographic's notes (encounters, invoices, etc.).

        Returns a list of all of the demographic's notes.
        """

        data = await self._post(
            self._endpoint.demographic_notes, {}, demographic_id=demographic.id
        )

        # Ensure data is not corrupt
        assert isinstance(data, dict)
        assert "notelist" in data
        assert isinstance(data["notelist"], list)

        # Import data into dataclass
        notes = [Note.from_dict(note_data) for note_data in data["notelist"]]
        return notes

    async def get_demographic_invoices(
        self, demographic: Demographic
    ) -> list[InvoiceNote]:
        """
        Get a demographic's invoice notes.

        Returns a list of all of the demographic's invoice notes.
        """

        notes = await self.get_demographic_notes(demographic)
        invoices = list(
            map(
                lambda note: InvoiceNote.from_dict(note.raw_data),
                filter(lambda note: note.is_invoice, notes),
            )
        )
        return invoices

    async def create_demographic_encounter_note(
        self, demographic: Demographic, note: Note
    ):
        """
        Creates a note for a demographic.

        Returns the created Note.
        """

        data = await self._post(
            self._endpoint.save_encounter_note,
            {
                "encounterNote": {
                    "isSigned": False,
                    "archived": True,  # No idea why this has to be true, not including it / setting it to false yields 500
                    "note": note.content,
                    "appointmentNo": 0,
                }
            },
            demographic_id=demographic.id,
        )

        # Ensure data is not corrupt
        assert isinstance(data, dict)
        assert "encounterNote" in data
        assert isinstance(data["encounterNote"], dict)

        # Import into dataclass
        return Note.from_dict(data["encounterNote"])

    async def get_health_card_status(self, health_card: OntarioHealthCard):
        """
        Get the status of an Ontario Health Card.

        Returns an OntarioHealthCardStatus object, which includes data about if it is valid,
        its status code, and expiration date if not already expired.
        """

        if not self.webscrapping_enabled:
            raise OscarAPIWebScrapingNotEnabled(
                "Web scraping is not enabled, but a web scrapping function was run. Please activate web scrapping and try again."
            )

        swipe_page = await self.playwright_context.new_page()
        await stealth_async(swipe_page)
        await swipe_page.goto(
            self._endpoint_webscraping.card_swipe.url.format(
                health_card_number=health_card.number, health_card_ver=health_card.ver
            ),
            wait_until="domcontentloaded",
        )

        # Get valid and invalid text elements
        valid_elements = await swipe_page.evaluate(
            """() => Array.from(document.querySelectorAll('td[class="item VALID"]')).map(node => node.innerText)"""
        )
        invalid_elements = await swipe_page.evaluate(
            """() => Array.from(document.querySelectorAll('td[class="item INVALID"]')).map(node => node.innerText)"""
        )

        # If none were found, throw error
        if len(valid_elements + invalid_elements) == 0:
            raise OscarAPIWebScrapingError(
                "Could not decode webpage when looking for health card validation info"
            )

        # Get expiration date field
        expiration_date_raw = await swipe_page.evaluate(
            """() => document.evaluate("//td[text()='Expiration Date']", document, null, XPathResult.ANY_TYPE, null).iterateNext().parentElement.querySelector("td[class='item']").innerText"""
        )

        # Close page since we don't need it anymore
        await swipe_page.close()

        # Use Regex to extract important info from text
        valid_raw, raw_code = re.search(
            r"([A-Z]{5,7}) \(Response Code: ([0-9]{2})\)",
            (valid_elements + invalid_elements)[0],
        ).groups()

        # Convert to more readable values
        valid_hc = valid_raw == "VALID"
        res_code = int(raw_code)
        expiration_date = (
            datetime.strptime(expiration_date_raw, "%Y-%m-%d").date()
            if expiration_date_raw != ""
            else datetime.fromtimestamp(0).date()
        )

        return OntarioHealthCardStatus(
            valid=valid_hc, code=res_code, expiration_date=expiration_date
        )

    async def update_appointment_reason(self, appt: Appointment, new_reason: str):
        """
        Update the reason of an appointment.

        Returns a new Appointment object with the new reason.
        """

        if not self.webscrapping_enabled:
            raise OscarAPIWebScrapingNotEnabled(
                "Web scraping is not enabled, but a web scrapping function was run. Please activate web scrapping and try again."
            )

        # Open up appt update page
        appt_update_page = await self.playwright_context.new_page()
        await stealth_async(appt_update_page)
        await appt_update_page.goto(
            self._endpoint_webscraping.update_appt.url.format(
                id=appt.id,
                demographic_no=appt.demographic.id,
            ),
            wait_until="domcontentloaded",
        )

        # Add new reason and update appointment
        await appt_update_page.locator("#reason").fill(new_reason)
        await appt_update_page.get_by_text("Update Appt").click()
        await appt_update_page.wait_for_load_state("networkidle")

        await appt_update_page.close()

        return await self.get_appointment_from_id(appt.id)

    def reset_demographics_cache(self):
        """
        Clears the cache of demographic objects stored in the class.
        """

        self._demographics_cache = {}
