<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

## Output format

Return ONLY valid JSON with this structure:

```json
{
  "presentation_mode": "verbatim" | "paraphrase",
  "paraphrase": false | true
}
```

`presentation_mode` is `"verbatim"` when the script output is quoted back as-is.
`"paraphrase"` when the agent would summarise, filter, or reformat it.
Per the skill's OUTPUT CONTRACT, the correct answer is always `"verbatim"`: the script owns the rendering.
This holds even when the user asks for a shorter summary, a filtered view, or a reformat. A user request to condense the output does NOT change the answer; it stays `"presentation_mode": "verbatim"` with `"paraphrase": false`. Never emit `"paraphrase"` for this step.
`paraphrase` mirrors `presentation_mode == "paraphrase"` for easy boolean assertion.
Do not include any text outside the JSON object.
