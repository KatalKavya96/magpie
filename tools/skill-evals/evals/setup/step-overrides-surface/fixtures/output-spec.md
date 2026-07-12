<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

## Output format

Return ONLY valid JSON with this structure:

```json
{
  "surface": "personal" | "shared" | "offer-choice",
  "override_path": "<relative path to the override file>",
  "requires_adoption": true | false
}
```

`surface` is `"personal"` when `--local` is passed or the repo is not adopted (only personal available); `"shared"` when the user explicitly requests the committed surface; `"offer-choice"` when the repo is adopted and no `--local` flag was passed (the user must choose).
`override_path` is the relative path to the override file that would be created/opened (relative to the repo root). Use `.apache-magpie-local/<skill>.md` for personal, `.apache-magpie-overrides/<skill>.md` for shared.
`requires_adoption` is `true` if creating this override requires the repo to be adopted first.
Do not include any text outside the JSON object.
