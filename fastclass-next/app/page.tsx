"use client";

import runScrapeEvaluation from "@/util/degree_eval";
import { FormEvent, useState } from "react";

export default function Home() {
	const [htmlContent, setHtmlContent] = useState<string>("");

	function handleSubmit(e: FormEvent<HTMLFormElement>) {
		e.preventDefault();
		runScrapeEvaluation(htmlContent);
	}

	return (
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
	);
}
