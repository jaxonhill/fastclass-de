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
		<main className="p-8">
			<h1 className="text-5xl font-bold text-slate-900 pb-4 mb-12 border-b-2 border-b-slate-500">
				Missing Class Requirements
			</h1>
			<div className="flex flex-col gap-8">
				{userRequirements.map((requirement) => {
					return (
						<div className="p-6 bg-white rounded-2xl shadow-md">
							<h2 className="text-3xl text-slate-900 font-bold pb-4">
								{requirement.title}
							</h2>
							<div className="flex flex-col gap-4">
								{requirement.subrequirements.map(
									(subrequirement) => {
										return (
											<div>
												<h3 className="text-xl font-semibold text-slate-800 pb-2">
													{subrequirement.title}
												</h3>
												<p className="font-medium text-slate-800">
													{subrequirement.needs}
												</p>
											</div>
										);
									}
								)}
							</div>
						</div>
					);
				})}
			</div>
		</main>
	);
}
