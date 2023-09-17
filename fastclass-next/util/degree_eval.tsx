import * as cheerio from "cheerio";

// Constants
const AUDIT_REQUIREMENTS_DIV_ID: string = "auditRequirements";
const UNFULFILLED_REQUIREMENT_CLASS_SELECTOR: string = ".Status_NO";
const MAIN_REQUIREMENT_TITLE_TEXT_SELECTOR: string =
	"div.reqHeaderTable > div.reqText > div.reqTitle";

export default function runScrapeEvaluation(htmlContent: string) {
	const $ = cheerio.load(htmlContent);

	// Find the main div that contains all other audit requirement divs as children
	const mainDiv$ = $(`div#${AUDIT_REQUIREMENTS_DIV_ID}`);

	// Get unfulfilled main requirements divs
	const unfulfilled_main_requirements_divs = mainDiv$.children(
		UNFULFILLED_REQUIREMENT_CLASS_SELECTOR
	);

	// Go through each main requirement and get the title (replace <br> tags with " | ")
	unfulfilled_main_requirements_divs.each((i, div) => {
		const mainRequirementTitle = $(div)
			.find(MAIN_REQUIREMENT_TITLE_TEXT_SELECTOR)
			.html()!
			.replace(/<br\s*\/?>/g, " | ");

		console.log(mainRequirementTitle);
	});
}
