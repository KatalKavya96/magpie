<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

## Output format

Return ONLY valid JSON with this structure:

```json
{
  "adopted": true | false,
  "proceed": true | false,
  "drift_flag": "none" | "local-lock-absent" | "version-mismatch"
}
```

`adopted` is `true` only when `.apache-magpie.lock` (the committed lock) is present in the repo root. If the report states that `.apache-magpie.lock` is not present / absent, then `adopted` is `false` — regardless of whether the local lock or a `.apache-magpie/` snapshot directory is mentioned. The committed lock is the sole determinant of adoption.
`proceed` is `true` when, and only when, the repo is adopted. A repo that is not adopted (`adopted: false`) always has `proceed: false`, because there is no state to render and the skill stops. Drift is non-blocking: an adopted repo with drift still proceeds.
`drift_flag` is `"none"` when locks match, on self-adoption (method:local), or when the repo is not adopted (no committed lock, so there is no drift to compute); `"local-lock-absent"` when the committed lock exists but no local lock; `"version-mismatch"` when both locks exist but their ref/method/url differs.

Decide `drift_flag` in this order:
- No committed `.apache-magpie.lock` (not adopted): `drift_flag` is `"none"`. This holds even when the local lock is ALSO absent. Never report `"local-lock-absent"` for an unadopted repo; drift is only computed against a committed lock.
- Committed lock present, but no `.apache-magpie.local.lock`: `drift_flag` is `"local-lock-absent"`.
- Both locks present and their ref/method/url differ: `drift_flag` is `"version-mismatch"`.
- Both locks present and matching, or self-adoption (method:local): `drift_flag` is `"none"`.

Do not include any text outside the JSON object.
