# fmt: off
from enum import Enum
import requests
from bs4 import BeautifulSoup, Tag
import lxml
import re
import pprint


TEST_SUBJECTS = {
    "A E",
    "ART",
    "ENS",
    "RANDO"
}


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


class RequestFailedException(Exception):
    "Raised when a request fails"
    pass


# Enums
class RequestStatus(Enum):
    SUCCESS = "success"
    TOO_MANY_RESULTS = "too_many_results"
    NO_RESULTS = "no_results"


class RequestURL(Enum):
    START = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL/search"
    BASE_API = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL"
    SPRING_2024_CATALOG_SUBJECT_CODES = "https://catalog.sdsu.edu/content.php?catoid=9&navoid=776"


class SemesterCode(Enum):
    SPRING_2024 = "2243"


class SoupSelectors(Enum):
    CATALOG_SUBJECT_OPTIONS = "#courseprefix option"
    SUBJECT_COURSE_OPTION_LI = ".psc_rowact"
    RED_FONT = 'font[color="red"]'


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


class Dispatcher:
    def __init__(self, semester_code: str, catalog_subject_codes_url: str) -> None:
        # NOTE: Change what params you init with for different semesters
        self.__semester_code: str = semester_code
        self.__catalog_subject_codes_url: str = catalog_subject_codes_url

        # Common state between all requests
        self.__IC_State_Num: int = 0
        self.__cookies: Cookies | None = None
    
    def initCookies(self):
        self.__cookies = Cookies()
        self.__IC_State_Num += 1

    def get_subject_codes(self) -> set[str]:
        try:
            r = requests.get(self.__catalog_subject_codes_url)
        except:
            raise CatalogDownException

        soup = BeautifulSoup(r.text, "html.parser")
        # Get dropdown options (remove first one, as it is a "Select value" type of option)
        option_tags = soup.select(SoupSelectors.CATALOG_SUBJECT_OPTIONS.value)[1:]
        return {tag["value"].strip() for tag in option_tags}

    def get_course_option_urls_for_subject(self, subject_code: str, course_number: str = "") -> set[str]:
        # TODO: Delete later
        print(f"Searching:\t{subject_code} {course_number}")

        # Make initial request to load options with various filters (will be deleted later)
        initial_subject_page_params = {
            "Page": "SSR_CLSRCH_ES_FL",
            "SEARCH_GROUP": "SSR_CLASS_SEARCH_LFF",
            "SEARCH_TEXT": "%",
            "ES_INST": "SDCMP",
            "ES_STRM": self.__semester_code,
            "ES_ADV": "Y",
            "ES_SUB": subject_code,
            "ES_CNBR": course_number,
            "ES_LNAME": "",
            "KeywordsOP": "CT",
            "SubjectOP": "EQ",
            "CatalogNbrOP": "CT",
            "LastNameOP": "CT",
            "GBLSRCH": "PTSF_GBLSRCH_FLUID",
        }
        initial_subject_page_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Cookie": f"TS01efa3ea={self.__cookies.TS01efa3ea}; TS0193b50d={self.__cookies.TS0193b50d}; lcsrftoken=ILDjEucplLUuMuHwYAM5XPoDPqQXD6swi2BOQ0wCK9Q=; CSDPRD-PSJSESSIONID={self.__cookies.CSDPRD_PSJSESSIONID}; PS_LASTSITE=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/; ExpirePage=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/; PS_TokenSite=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/?CSDPRD-PSJSESSIONID; PS_LOGINLIST=https://cmsweb.cms.sdsu.edu/CSDPRD; SignOnDefault=; ps_theme=node:SA portal:EMPLOYEE theme_id:SD_DEFAULT_THEME_FLUID css:DEFAULT_THEME_FLUID css_f:SD_PT_BRAND_FLUID_TEMPLATE_857 accessibility:N macroset:SD_PT_DEFAULT_MACROSET_857 formfactor:3 piamode:2; PS_TOKEN={self.__cookies.PS_TOKEN}; PS_DEVICEFEATURES=width:1920 height:1200 pixelratio:1.100000023841858 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; psback=%22%22url%22%3A%22https%3A%2F%2Fcmsweb.cms.sdsu.edu%2Fpsc%2FCSDPRD%2FEMPLOYEE%2FSA%2Fc%2FSSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL%3Fpage%3DSSR_CLSRCH_MAIN_FL%22%20%22label%22%3A%22Class%20Search%20and%20Enroll%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fcmsweb.cms.sdsu.edu%2Fpsc%2FCSDPRD%2FEMPLOYEE%2FSA%22%22; PS_TOKENEXPIRE={self.__cookies.PS_TOKENEXPIRE}",
            "Host": "cmsweb.cms.sdsu.edu",
            # TODO: MAYBE CHANGE
            "Referer": "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL?ICType=Panel&ICElementNum=0&ICStateNum=3&ICResubmit=1&ICAJAX=1&",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
        }
        try:
            r = requests.get(
                RequestURL.BASE_API.value, 
                params=initial_subject_page_params, 
                headers=initial_subject_page_headers
            )
        except:
            raise RequestFailedException
        finally:   
            self.__IC_State_Num += 1
        
        # Check that there are course options for this subject
        html: str = r.text
        soup = BeautifulSoup(html, "html.parser")
        course_option_li_elements: list[Tag] = soup.select(SoupSelectors.SUBJECT_COURSE_OPTION_LI.value)
        
        # If there are no course options, return an empty set
        if not course_option_li_elements:
            return set()

        # Make second request to delete the "Open Classes" filter
        remove_open_classes_filter_params = {
            "ICAJAX": "1",
            "ICNAVTYPEDROPDOWN": "0",
            "ICType": "Panel",
            "ICElementNum": "0",
            "ICStateNum": str(self.__IC_State_Num),
            "ICAction": "PTS_BREADCRUMB_PTS_IMG$0",
            "ICModelCancel": "0",
            "ICXPos": "0",
            "ICYPos": "0",
            "ResponsetoDiffFrame": "-1",
            "TargetFrameName": "None",
            "FacetPath": "None",
            "ICFocus": "",
            "ICSaveWarningFilter": "1",
            "ICChanged": "0",
            "ICSkipPending": "0",
            "ICAutoSave": "0",
            "ICResubmit": "0",
            "ICSID": "fQC1+uEeNnxtdL5Tvp98oCaneVK8A+/r5VRNwecwU7o=",
            "ICActionPrompt": "false",
            "ICBcDomData": f"*C~UnknownValue~EMPLOYEE~SA~SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL~SSR_CLSRCH_MAIN_FL~Class Search~UnknownValue~UnknownValue~https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL?~UnknownValue*C~UnknownValue~EMPLOYEE~SA~SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL~SSR_CLSRCH_ES_FL~Class Search Results~UnknownValue~UnknownValue~https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL?SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM={self.__semester_code}&ES_ADV=Y&ES_SUB={subject_code}&ES_CNBR={course_number}&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID&SEARCH_TYPE=SEARCHAGAIN~UnknownValue",
            "ICDNDSrc": "",
            "ICPanelHelpUrl": "",
            "ICPanelName": "",
            "ICPanelControlStyle": "pst_side2-disabled pst_side1-fixed pst_side2-hidden pst_panel-mode",
            "ICFind": "",
            "ICAddCount": "",
            "ICChart": '{ "aChHDP": [], "aChTp": [],"aChPTF": [] }',
            "PTS_FCTCHT_DATA": "",
            "PTS_TREEFACETCHG": "",
            "ICAppClsData": "",
            "win0hdrdivPT_SYSACT_HELP": "psc_hidden",
        }
        remove_open_classes_filter_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            # NOTE: I think if you add a Content-Length parameter, the whole thing breaks somehow?
            # Content-Length: 1495
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": f"PS_DEVICEFEATURES=width:1920 height:1200 pixelratio:1.100000023841858 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; TS01efa3ea={self.__cookies.TS01efa3ea}; TS0193b50d={self.__cookies.TS0193b50d}; CSDPRD-PSJSESSIONID={self.__cookies.CSDPRD_PSJSESSIONID}; ExpirePage=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/; PS_LOGINLIST=https://cmsweb.cms.sdsu.edu/CSDPRD; PS_TOKEN={self.__cookies.PS_TOKEN}; PS_TokenSite=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/?CSDPRD-PSJSESSIONID; SignOnDefault=; PS_LASTSITE=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/; ps_theme=node:SA portal:EMPLOYEE theme_id:SD_DEFAULT_THEME_FLUID css:DEFAULT_THEME_FLUID css_f:SD_PT_BRAND_FLUID_TEMPLATE_857 accessibility:N macroset:SD_PT_DEFAULT_MACROSET_857 formfactor:3 piamode:2; PS_TOKENEXPIRE={self.__cookies.PS_TOKENEXPIRE}; psback=%22%22url%22%3A%22https%3A%2F%2Fcmsweb.cms.sdsu.edu%2Fpsc%2FCSDPRD%2FEMPLOYEE%2FSA%2Fc%2FSSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL%3Fpage%3DSSR_CLSRCH_ES_FL%22%20%22label%22%3A%22Class%20Search%20Results%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fcmsweb.cms.sdsu.edu%2Fpsc%2FCSDPRD%2FEMPLOYEE%2FSA%22%22",
            "Host": "cmsweb.cms.sdsu.edu",
            "Origin": "https://cmsweb.cms.sdsu.edu",
            "Referer": f"https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL?Page=SSR_CLSRCH_ES_FL&SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM={self.__semester_code}&ES_ADV=Y&ES_SUB={subject_code}&ES_CNBR={course_number}&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
        }
        try: 
            r = requests.post(
                RequestURL.BASE_API.value,
                params=remove_open_classes_filter_params,
                headers=remove_open_classes_filter_headers,
            )
        except:
            raise RequestFailedException
        finally:
            self.__IC_State_Num += 1
        
        # Create empty set of course options that will get added to / returned
        course_options: set[str] = set()

        # Create soup from returned XML and see if there is red font indicating > 75 course options
        unfiltered_course_options_xml: str = r.text
        soup = BeautifulSoup(unfiltered_course_options_xml, "lxml")
        red_text_element: Tag | None = soup.select_one(SoupSelectors.RED_FONT.value)

        # If there are too many classes on one page, further refine using recursion
        if red_text_element:
            for i in range (0, 10):
                # Get options from recursive call
                current_options: set[str] = self.get_course_option_urls_for_subject(
                    subject_code, course_number + f"{i}"
                )
                # Add them to the course options you already have
                course_options = course_options.union(current_options)
            return course_options
        else:
            # Get all course options
            course_option_li_elements: list[Tag] = soup.select(SoupSelectors.SUBJECT_COURSE_OPTION_LI.value)

            # Define regex to get the URL out of the "onclick" attribute
            pattern = r"\('([^']*)'\)"

            # Loop through the course options and add the URLs to the set
            for course_option_li in course_option_li_elements:
                anchor_tag = course_option_li.find("a")
                match = re.search(pattern, anchor_tag["href"])
                if match:
                    course_options.add(match.group(1))
    
        return course_options
    

def main():
    # NOTE: Set current semester code here and respective catalog subject code url
    dispatcher = Dispatcher(SemesterCode.SPRING_2024.value, RequestURL.SPRING_2024_CATALOG_SUBJECT_CODES.value)

    # Get the subject codes
    try:
        subject_codes: set[str] = dispatcher.get_subject_codes()
    except CatalogDownException:
        print("ERROR: SDSU Catalog is down. Subject codes unavailable.")
        return
    except Exception:
        print("ERROR: Something wrong with subject code dropdown.")
        return

    # TODO: DELETE THIS, THIS IS JUST FOR TESTING
    subject_codes = TEST_SUBJECTS

    # Initialize cookie values needed for every request
    try:
        dispatcher.initCookies()
    except MaintenanceException:
        print("ERROR: mySDSU is under maintenance")
        return
    except InvalidCookieException:
        print("ERROR: Cookies were set incorrectly")
        return

    # {"subject_code": {"url1", "url2"}}
    subject_codes_and_course_options: dict[str, set[str]] = dict()
    
    # Iterate through the subject codes and create the dictionary with course option url sets as values
    for sub_code in subject_codes:
        subject_codes_and_course_options[sub_code] = dispatcher.get_course_option_urls_for_subject(sub_code)

    # TODO:
    # Iterate through the dictionary items so you have keys and values
    # Make requests for the class options for each course option url you have in the set
    # Get name of class, description, and then the individual class options on the page and all their attributes
    # Append all this info to a deeply nested dictionary (create helper functions to create the structure and clean data if necessary)
    # {
    #   "ENS": [
    #       {
    #           "number": "100",
    #           "title": "Fundamentals of Weight Lifting",
    #           "description": "Learn basics of barbell weight training and proper nutrition.",
    #           "class_options": [
    #               "professors": ["Arnold S", "Lifter Bob"],
    #               "times": [
    #                   {
    #                       "Monday": {
    #                           "start_time": ISO_FORMAT,
    #                           "end_time": ISO_FORMAT
    #                       },
    #                       "Wednesday": {
    #                           "start_time": ISO_FORMAT,
    #                           "end_time": ISO_FORMAT
    #                       }
    #                   },
    #                   {
    #                       "Tuesday": {
    #                           "start_time": ISO_FORMAT,
    #                           "end_time": ISO_FORMAT
    #                       },
    #                       "Thursday": {
    #                           "start_time": ISO_FORMAT,
    #                           "end_time": ISO_FORMAT
    #                       }
    #                   },
    #               ],
    #               "rooms": ["Room 1", "Gym 5"], 
    #           ]
    #       },
    #       {},
    #   ]
    # }


    pprint.pprint(subject_codes_and_course_options)

if __name__ == "__main__":
    main()
