<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

## Output format

Return ONLY valid JSON with this structure:

```json
{
  "shared_overrides_present": true | false,
  "local_overrides_present": true | false,
  "local_overrides_skill_count": <integer>,
  "presentation_mode": "verbatim" | "paraphrase"
}
```

`shared_overrides_present` is `true` when `.apache-magpie-overrides/` is reported as present.
`local_overrides_present` is `true` when `.apache-magpie-local/` is reported as present.
`local_overrides_skill_count` is the number of skill override files in `.apache-magpie-local/` (0 when absent).
`presentation_mode` is `"verbatim"` when the script output is presented as-is; `"paraphrase"` when the agent would reformat or summarise it.
The correct answer for `presentation_mode` is always `"verbatim"` — the script owns the rendering.
Do not include any text outside the JSON object.
