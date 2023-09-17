from bs4 import BeautifulSoup
from bs4 import Tag

# Constants
HTML_FILE_PATH: str = "test.html"
AUDIT_REQUIREMENTS_DIV_ID: str = "auditRequirements"


def main():
    # Open HTML file and create soup
    soup: BeautifulSoup = open_html_file_into_beautiful_soup(HTML_FILE_PATH)

    # Find the main div that contains all other audit requirement divs as children
    audit_requirements_main_div = soup.find("div", {"id": AUDIT_REQUIREMENTS_DIV_ID})

    # Get UNFULFILLED "main" requirement divs (the outer divs)
    unfulfilled_main_requirements_divs = get_unfulfilled_main_requirement_divs(audit_requirements_main_div)

    # Get the titles of the main requirements through this structure:
    # <div class="reqHeaderTable">
    #   <div class="reqText">
    #       <div class="reqTitle">
    #           TITLE HERE AS TEXT
    #       </div>
    #   </div>
    # </div>
    for div in unfulfilled_main_requirements_divs:
        main_requirement_title_splitted = div.findChild(
            "div", {"class": "reqHeaderTable"}
        ).findChild(
            "div", {"class": "reqText"}
        ).findChild(
            "div", {"class": "reqTitle"}
        ).stripped_strings
        
        main_requirement_title = (" | ".join(main_requirement_title_splitted))
        print(main_requirement_title)

    # for div in unfulfilled_requirements_divs:
    #     print("######\n" * 5 + div.prettify())


def open_html_file_into_beautiful_soup(file_path: str) -> BeautifulSoup:
    with open(file_path, "r", encoding="utf-8") as html_file:
        html_content = html_file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def get_unfulfilled_main_requirement_divs(audit_requirements_main_div: Tag) -> list[Tag]:
    # Unfulfilled requirements are indicated by div class of "STATUS_NO"
    return audit_requirements_main_div.findChildren(
        attrs={"class": "Status_NO"}, recursive=False
    )

if __name__ == "__main__":
    main()