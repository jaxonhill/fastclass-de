// Imports
import puppeteer from "puppeteer";

// Constants
const START_URL: string = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_MAIN_FL.GBL/search";
const BASE_API_URL: string = "https://cmsweb.cms.sdsu.edu/psc/CSDPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CLSRCH_ES_FL.GBL";
const SPRING_2024_SEMESTER_CODE: string = "2243";

// NOTE: CHANGE THIS WHEN SCRAPING FOR A DIFFERENT SEMESTER
const CURRENT_SEMESTER_CODE: string = SPRING_2024_SEMESTER_CODE;

const formatMemoryUsage = (data) => `${Math.round(data / 1024 / 1024 * 100) / 100} MB`;

(async () => {

    // Launch the browser and go to the home page
    const browser = await puppeteer.launch({
        headless: false,
    });
    const page = await browser.newPage();
    await page.setViewport({width: 1920, height: 1080});
    await page.goto(START_URL);

    for (let i = 0; i < 15; i++) {
        let newPage = await browser.newPage();
        await newPage.goto(START_URL);
    }

    const memoryData = process.memoryUsage();

    const memoryUsage = {
    rss: `${formatMemoryUsage(memoryData.rss)} -> Resident Set Size - total memory allocated for the process execution`,
    heapTotal: `${formatMemoryUsage(memoryData.heapTotal)} -> total size of the allocated heap`,
    heapUsed: `${formatMemoryUsage(memoryData.heapUsed)} -> actual memory used during the execution`,
    external: `${formatMemoryUsage(memoryData.external)} -> V8 external memory`,
    };

    browser.close();

    console.log(memoryUsage);

    return

    // Go to the subject page
    const extension: string = "ACCTG";
    await page.goto(BASE_API_URL + `?Page=SSR_CLSRCH_ES_FL&SEARCH_GROUP=SSR_CLASS_SEARCH_LFF&SEARCH_TEXT=%&ES_INST=SDCMP&ES_STRM=${CURRENT_SEMESTER_CODE}&ES_ADV=Y&ES_SUB=${extension}&ES_CNBR=&ES_LNAME=&KeywordsOP=CT&SubjectOP=EQ&CatalogNbrOP=CT&LastNameOP=CT&GBLSRCH=PTSF_GBLSRCH_FLUID`);

    // Find "Open Classes button"
    let element = await page.waitForSelector(String.raw`#PTS_BREADCRUMB_PTS_IMG\$0`);
    console.log((element) ? "Element here" : "Element not here");


    
    // Execute JavaScript to get rid of the button
    await page.evaluate("submitAction_win0(document.win0, 'PTS_BREADCRUMB_PTS_IMG$0');");
    element = await page.waitForSelector(String.raw`#PTS_BREADCRUMB_PTS_IMG\$0`);
    console.log((element) ? "Element here now" : "Element not here now");

    await browser.close()

})();