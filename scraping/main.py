# Imports
import requests
from bs4 import BeautifulSoup
import time

# Constants
START_URL: str = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL/search"
BASE_API_URL: str = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL"
FALL_2023_SEMESTER_CODE: str = "2237"
SPRING_2024_SEMESTER_CODE: str = "2243"
SUBJECT_COURSE_LI_TAG_CLASS: str = "psc_rowact"

# NOTE: CHANGE/UPDATE THESE WHEN SCRAPING FOR A DIFFERENT SEMESTER
CURRENT_SEMESTER_CODE: str = FALL_2023_SEMESTER_CODE
SPRING_2024_SUBJECT_CODES: list[str] = [
    "ECON",
    "A E",
    "A S",
    "ACCTG",
    "AFRAS",
    "AMIND",
    "ANTH",
    "ARAB",
    "ARP",
]

# TODO: THIS HAS THE REAL SUBJECT CODES, COPY AND PASTE TO SPRING 2024 ONCE DONE WITH TESTING
PLACEHOLDER: list[str] = [
    "A E",
    "A S",
    "ACCTG",
    "AFRAS",
    "AMIND",
    "ANTH",
    "ARAB",
    "ARP",
    "ART",
    "ASIAN",
    "ASTR",
    "AUD",
    "B A",
    "BDA",
    "BIOL",
    "BIOMI",
    "BQS",
    "BRAZ",
    "C P",
    "CAL",
    "CCS",
    "CFD",
    "CHEM",
    "CHIN",
    "CINTS",
    "CIV E",
    "CJ",
    "CLASS",
    "COMM",
    "COMP",
    "COMPE",
    "CON E",
    "CS",
    "CSP",
    "DANCE",
    "DLE",
    "DPT",
    "E E",
    "ECL",
    "ECON",
    "ED",
    "EDL",
    "ENGR",
    "ENS",
    "ENV E",
    "ENV S",
    "EUROP",
    "FILIP",
    "FIN",
    "FRENC",
    "GEN S",
    "GEOG",
    "GEOL",
    "GERMN",
    "GERO",
    "H SEC",
    "HEBRW",
    "HHS",
    "HIST",
    "HONOR",
    "HTM",
    "HUM",
    "I B",
    "INT S",
    "ISCOR",
    "ITAL",
    "JAPAN",
    "JMS",
    "JS",
    "KOR",
    "LATAM",
    "LCS",
    "LDT",
    "LEAD",
    "LGBT",
    "LIB S",
    "LING",
    "M BIO",
    "M E",
    "M S E",
    "MALAS",
    "MATH",
    "MGT",
    "MIL S",
    "MIS",
    "MKTG",
    "MTHED",
    "MUSIC",
    "N SCI",
    "NAV S",
    "NURS",
    "NUTR",
    "OCEAN",
    "P A",
    "P H",
    "PERS",
    "PHIL",
    "PHYS",
    "POL S",
    "PORT",
    "PSFA",
    "PSY",
    "R A",
    "REL S",
    "RTM",
    "RUSSN",
    "RWS",
    "SCI",
    "SLHS",
    "SOC",
    "SOCSI",
    "SPAN",
    "SPED",
    "STAT",
    "STS",
    "SUSTN",
    "SWORK",
    "TE",
    "TFM",
    "THEA",
    "WMNST",
]


def main() -> None:
    (  # Get cookies unique to each session, they are needed for each request
        CSDPRD_PSJSESSIONID,
        PS_TOKEN,
        PS_TOKENEXPIRE,
        TS0193b50d,
        TS01efa3ea,
    ) = get_needed_cookie_values()

    for subject_code in SPRING_2024_SUBJECT_CODES:
        """
        For each subject, we have to make an initial request for the course option information; however,
        these course options only display courses with "Open Classes."

        We do not want this. We want ALL classes, whether they are waitlisted, open, or closed entirely.

        Therefore, we make 2 requests. First, the initial request. Second, some sort of AJAX/XML request
        that will essentially "click" the "Open Classes" filter to close it. The API POST request now
        returns XML that contains ALL course options.

        To further clarify: You ALWAYS need to make the subject request first, then the second one.
        """

        # TODO: Need to create a way to confirm that the button is gone from the new XML
        #       or just to confirm that "Open Classes" filter is not applied

        # Create the params and headers and make initial subject page request
        subject_page_request_params = {
            "Page": "SSR_CLSRCH_ES_FL",
            "SEARCH_GROUP": "SSR_CLASS_SEARCH_LFF",
            "SEARCH_TEXT": "%",
            "ES_INST": "SDCMP",
            "ES_STRM": CURRENT_SEMESTER_CODE,
            "ES_ADV": "Y",
            "ES_SUB": subject_code,
            "ES_CNBR": "",
            "ES_LNAME": "",
            "KeywordsOP": "CT",
            "SubjectOP": "EQ",
            "CatalogNbrOP": "CT",
            "LastNameOP": "CT",
            "GBLSRCH": "PTSF_GBLSRCH_FLUID",
        }
        subject_page_request_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Cookie": f"TS01efa3ea={TS01efa3ea}; TS0193b50d={TS0193b50d}; lcsrftoken=ILDjEucplLUuMuHwYAM5XPoDPqQXD6swi2BOQ0wCK9Q=; CSDPRD-PSJSESSIONID={CSDPRD_PSJSESSIONID}; PS_LASTSITE=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/; ExpirePage=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/; PS_TokenSite=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/?CSDPRD-PSJSESSIONID; PS_LOGINLIST=https://cmsweb.cms.sdsu.edu/CSDPRD; SignOnDefault=; ps_theme=node:SA portal:EMPLOYEE theme_id:SD_DEFAULT_THEME_FLUID css:DEFAULT_THEME_FLUID css_f:SD_PT_BRAND_FLUID_TEMPLATE_857 accessibility:N macroset:SD_PT_DEFAULT_MACROSET_857 formfactor:3 piamode:2; PS_TOKEN={PS_TOKEN}; PS_DEVICEFEATURES=width:1920 height:1200 pixelratio:1.100000023841858 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; psback=%22%22url%22%3A%22https%3A%2F%2Fcmsweb.cms.sdsu.edu%2Fpsc%2FCSDPRD%2FEMPLOYEE%2FSA%2Fc%2FSSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL%3Fpage%3DSSR_CLSRCH_MAIN_FL%22%20%22label%22%3A%22Class%20Search%20and%20Enroll%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fcmsweb.cms.sdsu.edu%2Fpsc%2FCSDPRD%2FEMPLOYEE%2FSA%22%22; PS_TOKENEXPIRE={PS_TOKENEXPIRE}",
            "Host": "cmsweb.cms.sdsu.edu",
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
        r = requests.get(
            BASE_API_URL,
            params=subject_page_request_params,
            headers=subject_page_request_headers,
        )

        # Create params and headers for the second AJAX/XML request that closes the "Open Classes" filter
        display_all_course_options_request_params = {
            "ICAJAX": "1",
            "ICNAVTYPEDROPDOWN": "0",
            "ICType": "Panel",
            "ICElementNum": "0",
            "ICStateNum": "2",  # NOTE: Increases by 2 every time it is clicked
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
            "ICBcDomData": f"*C~UnknownValue~EMPLOYEE~SA~SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL~SSR_CLSRCH_MAIN_FL~Class Search~UnknownValue~UnknownValue~https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL?~UnknownValue*C~UnknownValue~EMPLOYEE~SA~SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL~SSR_CLSRCH_ES_FL~Class Search Results~UnknownValue~UnknownValue~https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL?SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM={CURRENT_SEMESTER_CODE}&ES_ADV=Y&ES_SUB={subject_code}&ES_CNBR=&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID&SEARCH_TYPE=SEARCHAGAIN~UnknownValue",
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
        display_all_course_options_request_headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            # NOTE: I think if you add a Content-Length parameter, the whole thing breaks somehow?
            # Content-Length: 1495
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": f"PS_DEVICEFEATURES=width:1920 height:1200 pixelratio:1.100000023841858 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; TS01efa3ea={TS01efa3ea}; TS0193b50d={TS0193b50d}; CSDPRD-PSJSESSIONID={CSDPRD_PSJSESSIONID}; ExpirePage=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/; PS_LOGINLIST=https://cmsweb.cms.sdsu.edu/CSDPRD; PS_TOKEN={PS_TOKEN}; PS_TokenSite=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/?CSDPRD-PSJSESSIONID; SignOnDefault=; PS_LASTSITE=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/; ps_theme=node:SA portal:EMPLOYEE theme_id:SD_DEFAULT_THEME_FLUID css:DEFAULT_THEME_FLUID css_f:SD_PT_BRAND_FLUID_TEMPLATE_857 accessibility:N macroset:SD_PT_DEFAULT_MACROSET_857 formfactor:3 piamode:2; PS_TOKENEXPIRE={PS_TOKENEXPIRE}; psback=%22%22url%22%3A%22https%3A%2F%2Fcmsweb.cms.sdsu.edu%2Fpsc%2FCSDPRD%2FEMPLOYEE%2FSA%2Fc%2FSSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL%3Fpage%3DSSR_CLSRCH_ES_FL%22%20%22label%22%3A%22Class%20Search%20Results%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fcmsweb.cms.sdsu.edu%2Fpsc%2FCSDPRD%2FEMPLOYEE%2FSA%22%22",
            "Host": "cmsweb.cms.sdsu.edu",
            "Origin": "https://cmsweb.cms.sdsu.edu",
            "Referer": f"https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL?Page=SSR_CLSRCH_ES_FL&SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM={CURRENT_SEMESTER_CODE}&ES_ADV=Y&ES_SUB={subject_code}&ES_CNBR=&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
        }

        # Make that second request and get the XML to make soup
        # TODO: FIX XML WARNING
        r = requests.post(
            BASE_API_URL,
            params=display_all_course_options_request_params,
            headers=display_all_course_options_request_headers,
        )
        all_classes_request_xml: str = r.text
        soup = BeautifulSoup(all_classes_request_xml, "html.parser")

        # ele = soup.select_one("#win0divPTS_SEARCHED_KW2")
        # print(ele.text)

        return

    # TODO: Check that there is no red font (indicating > 75 classes on the page currently)
    # NOTE: Probably best to use recursion and some kind of method here actually
    #
    #       If there is red font, then create first iteration of class number
    #           For instance, search "ENS 0" "ENS 1" "ENS 2"
    #
    #           On each one of these numbered requests, again check > 75 classes on page
    #           If there is red font again, then further refine that specific number
    #               For instance, "ENS 10" "ENS 11" "ENS 12"
    #
    #               On each one of those further numbered requests, again check > 75 classes on page
    #               If there is the red font yet again, then again further refine the number
    #                   For instance, "ENS 110" "ENS 111" "ENS 112"

    # TODO: Once there is no red font and there are class options there:
    #           Scrape the "ul" that holds the course options
    #           Each "li" in the "ul" will have a onclick="javascript:openSrchRsltURL('URL YOU NEED HERE')"
    #           Append each of those URLs to an array that is the value of a dictionary where the key is the subject code

    # END LOOP

    # START LOOP THROUGH SUBJECT DICTIONARY WITH THE ARRAY URL VALUES

    # TODO: Make "Course ID" request

    # TODO: Check that the page loaded correctly somehow

    # TODO: Check if there is a "Display n More" button
    #
    #       If there is a "Display n More" button, then make the "Display n More" request
    #       Check again for the button, if there is the button, then make request again, etc.

    # TODO: Once all classes are in the HTML:
    #           Scrape the table that holds all class options
    #           Each "tr" has certain "td"s that you want such as DAYS_TIMES, INSTRUCTOR, etc.

    #

    # END LOOP

    ###

    ###


def get_needed_cookie_values() -> list[str]:
    # Make initial request and return cookies in a dictionary
    r = requests.get(START_URL)
    cookies = dict(r.cookies.items())

    # Return only the cookie values that are unique to a new session each time
    return [
        cookies["CSDPRD-PSJSESSIONID"],
        cookies["PS_TOKEN"],
        cookies["PS_TOKENEXPIRE"],
        cookies["TS0193b50d"],
        cookies["TS01efa3ea"],
    ]


if __name__ == "__main__":
    main()
