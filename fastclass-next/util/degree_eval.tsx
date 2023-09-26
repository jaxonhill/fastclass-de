import * as cheerio from "cheerio";

// Constants
const AUDIT_REQUIREMENTS_DIV_SELECTOR: string = "#auditRequirements";
const UNFULFILLED_REQUIREMENT_CLASS_SELECTOR: string = ".Status_NO";
const MAIN_REQUIREMENT_TITLE_TEXT_SELECTOR: string =
	"div.reqHeaderTable > div.reqText > div.reqTitle";
const SUBREQUIREMENT_DIV_SELECTOR: string = ".subrequirement";

// Types
export type MainRequirement = {
	title: String;
	subrequirements: SubRequirement[];
};

type SubRequirement = {
	title: String;
	status: Status;
	needs: String;
	classOptions: (Class | ClassChoice | ClassRange)[];
};

type Class = {
	department: String;
	number: String; // NOTE: This could have a letter attached to it, such as 101A -- so must be string
};

type ClassChoice = {
	choices: Class[]; // There could be a choice between more than 2 classes, so keep as an array
};

type ClassRange = {
	startClass: Class;
	endClass: Class;
};

type Status = "Complete" | "In Progress" | "Not Met" | "None";

//

export default function runScrapeEvaluation(
	htmlContent: string
): MainRequirement[] {
	// Load the HTML
	const $ = cheerio.load(htmlContent);

	// Find the main div that contains all other audit requirement divs as children
	const mainDiv$ = $(`div${AUDIT_REQUIREMENTS_DIV_SELECTOR}`);

	// Get unfulfilled main requirements divs (.children only gets direct children)
	const unfulfilledMainRequirementsDivs = mainDiv$.children(
		UNFULFILLED_REQUIREMENT_CLASS_SELECTOR
	);

	// Go through each main requirement
	unfulfilledMainRequirementsDivs.each((i, div) => {
		// Get the main requirement title (replace <br> tags with " | ")
		const mainRequirementTitle = $(div)
			.find(MAIN_REQUIREMENT_TITLE_TEXT_SELECTOR)
			.html()!
			.replace(/<br\s*\/?>/g, " | ");

		console.log(mainRequirementTitle);
		console.log("\n");

		// For each main requirement, get subrequirements
		let validSubrequirementDivs = $(div)
			.find(`div${SUBREQUIREMENT_DIV_SELECTOR}`)
			.has("div.subreqPretext > span.Status_NO") // That are incomplete
			.has("table.selectcourses td.fromcourselist tbody"); // And have classes to choose from

		// Loop through each subrequirement
		validSubrequirementDivs.each((j, div) => {
			// Get the title of the subrequirement
			const subrequirementTitle: string | undefined =
				$(div).attr("pseudo");

			// Get what the student "needs" to fulfill the requirement
			const subrequirementNeeds: string | undefined = $(div)
				.find("table.subreqNeeds")
				.text()
				.split(/\s+/) // Fix weird formatting
				.filter(Boolean)
				.join(" ");

			// Find the tableBody that has the rows of classes
			const tableBody = $(div).find(
				"table.selectcourses td.fromcourselist tbody"
			);

			// Find the td elements that hold the spans of classes
			const tableDatas = $(tableBody).find("td");

			// Loop through each td element that holds multiple spans of classes
			console.log(tableDatas);

			// TODO: Remove "+" from class numbers
		});

		console.log("#####\n\n\n\n\n");
	});

	// Create fake data to test UI
	return [
		{
			title: "*** IIA. FOUNDATIONS | NATURAL SCIENCES AND QUANTITATIVE REASONING ***",
			subrequirements: [
				{
					title: "1. Physical Sciences",
					status: "Not Met",
					needs: "NEEDS: 3 UNITS",
					classOptions: [
						{
							department: "BIOL",
							number: "101",
						},
						{
							department: "GEOL",
							number: "202",
						},
					],
				},
				{
					title: "2. Mathematics",
					status: "Not Met",
					needs: "NEEDS: 1 CLASS",
					classOptions: [
						{
							department: "MATH",
							number: "150",
						},
						{
							department: "MATH",
							number: "151",
						},
					],
				},
			],
		},
		{
			title: "*** IIC.  FOUNDATIONS - ARTS AND HUMANITIES ***",
			subrequirements: [
				{
					title: "1. Art",
					status: "Not Met",
					needs: "NEEDS: 1 CLASS",
					classOptions: [
						{
							department: "ART",
							number: "104",
						},
						{
							department: "MUSIC",
							number: "151",
						},
					],
				},
				{
					title: "2. Humanities",
					status: "Not Met",
					needs: "NEEDS: 1 CLASS",
					classOptions: [
						{
							department: "ANTH",
							number: "102",
						},
						{
							department: "HIST",
							number: "180",
						},
					],
				},
			],
		},
	];
}
