import * as cheerio from "cheerio";

// Constants
const AUDIT_REQUIREMENTS_DIV_SELECTOR: string = "#auditRequirements";
const UNFULFILLED_REQUIREMENT_CLASS_SELECTOR: string = ".Status_NO";
const MAIN_REQUIREMENT_TITLE_TEXT_SELECTOR: string =
	"div.reqHeaderTable > div.reqText > div.reqTitle";
const SUBREQUIREMENT_DIV_SELECTOR: string = ".subrequirement";

export default function runScrapeEvaluation(htmlContent: string) {
	// Load the HTML
	const $ = cheerio.load(htmlContent);

	// Find the main div that contains all other audit requirement divs as children
	const mainDiv$ = $(`div${AUDIT_REQUIREMENTS_DIV_SELECTOR}`);

	// Get unfulfilled main requirements divs (.children only gets direct children)
	const unfulfilledMainRequirementsDivs = mainDiv$.children(
		UNFULFILLED_REQUIREMENT_CLASS_SELECTOR
	);

	// Go through each main requirement and get the title (replace <br> tags with " | ")
	unfulfilledMainRequirementsDivs.each((i, div) => {
		const mainRequirementTitle = $(div)
			.find(MAIN_REQUIREMENT_TITLE_TEXT_SELECTOR)
			.html()!
			.replace(/<br\s*\/?>/g, " | ");

		console.log(mainRequirementTitle);

		// For each main requirement, get all the subrequirements that are incomplete
		let subrequirementDivs = $(div)
			.find(`div${SUBREQUIREMENT_DIV_SELECTOR}`)
			.has("div.subreqPretext > span.Status_NO");

		// Loop through each subrequirement
		subrequirementDivs.each((j, div) => {
			// Get the title of the subrequirement
			const subrequirementTitle: string | undefined =
				$(div).attr("pseudo");
			console.log(subrequirementTitle);

			// Get what the student "needs" to fulfill the requirement
			const subrequirementNeeds: string | undefined = $(div)
				.find("table.subreqNeeds")
				.text()
				.split(/\s+/) // Fix weird formatting
				.filter(Boolean)
				.join(" ");
			console.log(subrequirementNeeds);
			console.log(" ");
		});

		console.log(" ");
		console.log("##########");
		console.log(" ");
	});
}
