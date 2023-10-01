# Imports
import requests
from bs4 import BeautifulSoup
import time

# Constants
START_URL: str = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL/search"
BASE_API_URL: str = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL"
FALL_2023_SEMESTER_CODE: str = "2237"
SPRING_2024_SEMESTER_CODE: str = "2243"
ARIA_LABEL_ATTRIBUTE_TEXT_FOR_OPEN_CLASSES_BUTTON: str = (
    "Remove Open Classes Only filter"
)

# NOTE: CHANGE THIS WHEN SCRAPING FOR A DIFFERENT SEMESTER
CURRENT_SEMESTER_CODE: str = FALL_2023_SEMESTER_CODE


def main() -> None:
    (  # Get cookies unique to each session, they are needed for each request
        CSDPRD_PSJSESSIONID,
        PS_TOKEN,
        PS_TOKENEXPIRE,
        TS0193b50d,
        TS01efa3ea,
    ) = get_needed_cookie_values()

    extension: str = "BIOL"

    # Create params and headers to search for each subject
    subject_page_params = {
        "Page": "SSR_CLSRCH_ES_FL",
        "SEARCH_GROUP": "SSR_CLASS_SEARCH_LFF",
        "SEARCH_TEXT": "%",
        "ES_INST": "SDCMP",
        "ES_STRM": CURRENT_SEMESTER_CODE,
        "ES_ADV": "Y",
        "ES_SUB": extension,
        "ES_CNBR": "",
        "ES_LNAME": "",
        "KeywordsOP": "CT",
        "SubjectOP": "EQ",
        "CatalogNbrOP": "CT",
        "LastNameOP": "CT",
        "GBLSRCH": "PTSF_GBLSRCH_FLUID",
    }
    subject_page_headers = {
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

    # Make request for the subject and get the HTML
    r = requests.get(
        BASE_API_URL, params=subject_page_params, headers=subject_page_headers
    )
    original_subject_request_html: str = r.text
    soup1 = BeautifulSoup(original_subject_request_html, "html.parser")

    ###

    # Create params and headers to close the "Open Classes" option, as we want ALL classes
    open_classes_button_request_params = {
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
        "ICBcDomData": f"*C~UnknownValue~EMPLOYEE~SA~SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL~SSR_CLSRCH_MAIN_FL~Class Search~UnknownValue~UnknownValue~https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL?~UnknownValue*C~UnknownValue~EMPLOYEE~SA~SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL~SSR_CLSRCH_ES_FL~Class Search Results~UnknownValue~UnknownValue~https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL?SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM={CURRENT_SEMESTER_CODE}&ES_ADV=Y&ES_SUB={extension}&ES_CNBR=&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID&SEARCH_TYPE=SEARCHAGAIN~UnknownValue",
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
    open_classes_button_request_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        # Content-Length: 1495
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"PS_DEVICEFEATURES=width:1920 height:1200 pixelratio:1.100000023841858 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; TS01efa3ea={TS01efa3ea}; TS0193b50d={TS0193b50d}; CSDPRD-PSJSESSIONID={CSDPRD_PSJSESSIONID}; ExpirePage=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/; PS_LOGINLIST=https://cmsweb.cms.sdsu.edu/CSDPRD; PS_TOKEN={PS_TOKEN}; PS_TokenSite=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/?CSDPRD-PSJSESSIONID; SignOnDefault=; PS_LASTSITE=https://cmsweb.cms.sdsu.edu/psc/CSDPRD/; ps_theme=node:SA portal:EMPLOYEE theme_id:SD_DEFAULT_THEME_FLUID css:DEFAULT_THEME_FLUID css_f:SD_PT_BRAND_FLUID_TEMPLATE_857 accessibility:N macroset:SD_PT_DEFAULT_MACROSET_857 formfactor:3 piamode:2; PS_TOKENEXPIRE={PS_TOKENEXPIRE}; psback=%22%22url%22%3A%22https%3A%2F%2Fcmsweb.cms.sdsu.edu%2Fpsc%2FCSDPRD%2FEMPLOYEE%2FSA%2Fc%2FSSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL%3Fpage%3DSSR_CLSRCH_ES_FL%22%20%22label%22%3A%22Class%20Search%20Results%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%221%22%20%22refurl%22%3A%22https%3A%2F%2Fcmsweb.cms.sdsu.edu%2Fpsc%2FCSDPRD%2FEMPLOYEE%2FSA%22%22",
        "Host": "cmsweb.cms.sdsu.edu",
        "Origin": "https://cmsweb.cms.sdsu.edu",
        # NOTE: Consider changing referer, if broken for other subjects
        "Referer": f"https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL?Page=SSR_CLSRCH_ES_FL&SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM={CURRENT_SEMESTER_CODE}&ES_ADV=Y&ES_SUB={extension}&ES_CNBR=&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
    }

    start = time.time()
    r = requests.post(
        BASE_API_URL,
        params=open_classes_button_request_params,
        headers=open_classes_button_request_headers,
    )
    end = time.time()
    html_after_removing_open_classes_filter: str = r.text
    soup2 = BeautifulSoup(html_after_removing_open_classes_filter, "html.parser")

    element1 = soup1.find(
        "a", {"aria-label": ARIA_LABEL_ATTRIBUTE_TEXT_FOR_OPEN_CLASSES_BUTTON}
    )
    element2 = soup2.find(
        "a", {"aria-label": ARIA_LABEL_ATTRIBUTE_TEXT_FOR_OPEN_CLASSES_BUTTON}
    )

    print("\n\n")

    if element1:
        print("Wow!")

    if element1 and not element2:
        print("Worked!")

    # TODO: CHECK DIFFERENCE IN CLASSES

    # print(soup1.prettify())
    # print("\n\n\n#####\n#####\n#####\n\n\n")
    # print(soup2.prettify())

    print("FIRST HTML: " + soup1.select_one("#win0divPTS_SRCHED_KW_GB2").text)
    print("\n")
    print("SECOND HTML: " + soup2.select_one("#win0divPTS_SEARCHED_KW2").text)

    print("\n\nTIME IT TOOK: " + str((end - start)))

    # Need way to verify that the button is gone from the HTML


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
