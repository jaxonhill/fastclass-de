# fmt: off
from enum import Enum
import requests
from bs4 import BeautifulSoup, Tag
import pprint

TEST_SUBJECTS = [
    "A E",
    "ART",
    "ENS",
]


# Exceptions
class MaintenanceException(Exception):
    "Raised when mySDSU is undergoing maintenance"
    pass


class InvalidCookieException(Exception):
    "Raised when a cookie is not set correctly, or doesn't exist"
    pass


class CatalogDownException(Exception):
    "Raised when the catalog page with the subject codes is down for some reason"
    pass


# Enums
class RequestStatus(Enum):
    SUCCESS = "success"
    TOO_MANY_RESULTS = "too_many_results"
    NO_RESULTS = "no_results"


class RequestURL(Enum):
    START = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL/search"
    BASE = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL"
    SPRING_2024_CATALOG_SUBJECT_CODES = "https://catalog.sdsu.edu/content.php?catoid=9&navoid=776"


class SemesterCode(Enum):
    SPRING_2024 = "2243"


class SoupSelectors(Enum):
    CATALOG_SUBJECT_OPTIONS = "#courseprefix option"


# Classes
class Cookies:
    def __init__(self) -> None:
        self.CSDPRD_PSJSESSIONID = None
        self.PS_TOKEN = None
        self.PS_TOKENEXPIRE = None
        self.TS0193b50d = None
        self.TS01efa3ea = None
        self.make_request_to_set_cookies()

    def make_request_to_set_cookies(self) -> None:
        try:
            r = requests.get(RequestURL.START.value, timeout=20)
        except:
            raise MaintenanceException

        try:
            cookies = dict(r.cookies.items())
            self.CSDPRD_PSJSESSIONID = cookies["CSDPRD-PSJSESSIONID"]
            self.PS_TOKEN = cookies["PS_TOKEN"]
            self.PS_TOKENEXPIRE = cookies["PS_TOKENEXPIRE"]
            self.TS0193b50d = cookies["TS0193b50d"]
            self.TS01efa3ea = cookies["TS01efa3ea"]
        except:
            raise InvalidCookieException


def get_subject_codes(url: str) -> set[str]:
    try:
        r = requests.get(url)
    except:
        raise CatalogDownException

    soup = BeautifulSoup(r.text, "html.parser")
    # Get dropdown options (remove first one, as it is a "Select value" type of option)
    option_tags = soup.select(SoupSelectors.CATALOG_SUBJECT_OPTIONS.value)[1:]
    return {tag["value"].strip() for tag in option_tags}


def main():
    # NOTE: Set current semester code here and respective catalog subject code url
    semester_code = SemesterCode.SPRING_2024.value
    catalog_subject_codes_url = RequestURL.SPRING_2024_CATALOG_SUBJECT_CODES.value

    try:
        subject_codes: set[str] = get_subject_codes(catalog_subject_codes_url)
    except CatalogDownException:
        print("ERROR: SDSU Catalog is down. Subject codes unavailable.")
        return
    except Exception:
        print("ERROR: Something wrong with subject code dropdown.")
        return

    # IC_State_Num will be incremented after successful requests on class search pages
    IC_State_Num = 1

    # Set cookie values needed for every request
    try:
        cookies: Cookies = Cookies()
        IC_State_Num += 1
    except MaintenanceException:
        print("ERROR: mySDSU is under maintenance")
        return
    except InvalidCookieException:
        print("ERROR: Cookies were set incorrectly")
        return

    # {"subject_code": {"url1", "url2"}}
    subject_codes_and_course_options: dict[str, set[str]] = dict()
    pprint.pprint(subject_codes)


if __name__ == "__main__":
    main()
