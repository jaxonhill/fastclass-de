"use client";

import runScrapeEvaluation from "@/util/degree_eval";
import { FormEvent, useState } from "react";
import { MainRequirement } from "@/util/degree_eval";

export default function Home() {
	const [htmlContent, setHtmlContent] = useState<string>("");
	const [userRequirements, setUserRequirements] = useState<
		MainRequirement[] | undefined
	>();

	function handleSubmit(e: FormEvent<HTMLFormElement>) {
		e.preventDefault();
		const requirements: MainRequirement[] =
			runScrapeEvaluation(htmlContent);
		setUserRequirements(requirements);
	}

	return !userRequirements ? (
		<main>
			<form onSubmit={(e) => handleSubmit(e)}>
				<textarea
					cols={30}
					rows={10}
					placeholder="Paste degree evaluation HTML here"
					value={htmlContent}
					onChange={(e) => setHtmlContent(e.target.value)}
				></textarea>
				<button type="submit">Submit</button>
			</form>
		</main>
	) : (
		<main>
			<h1>Missing Class Requirements</h1>
			{userRequirements.map((requirement) => {
				return (
					<div>
						<h2 className="text-5xl">{requirement.title}</h2>
						{requirement.subrequirements.map((subrequirement) => {
							return (
								<div>
									<h3>{subrequirement.title}</h3>
									<p>{subrequirement.needs}</p>
								</div>
							);
						})}
					</div>
				);
			})}
		</main>
	);
}
