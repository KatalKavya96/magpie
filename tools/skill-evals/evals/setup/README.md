<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

# setup evals

Behavioral evals for the `setup` skill.

## Suites (9 cases total)

| Suite | Step | Cases | What it covers |
|---|---|---|---|
| step-verify-drift | verify.md § Check 3 (drift) | 5 | clean, method/URL mismatch, ref mismatch, svn-zip SHA-512 mismatch, local lock missing |
| step-overrides-surface | overrides.md § Step 0b | 4 | adopted no flag (offer choice), --local flag (personal), not adopted (personal only), both surfaces exist |

## Run

```bash
# All cases
uv run --project tools/skill-evals skill-eval \
    tools/skill-evals/evals/setup/

# Single suite
uv run --project tools/skill-evals skill-eval \
    tools/skill-evals/evals/setup/step-verify-drift/fixtures/

# Single case
uv run --project tools/skill-evals skill-eval \
    tools/skill-evals/evals/setup/step-verify-drift/fixtures/case-1-clean
```

## Notes

- `step-verify-drift` cases are fully auto-comparable: all three output
  fields (`status`, `severity`, `remediation`) are enumerated strings.
- `step-overrides-surface` tests the new `--local` flag and personal-
  vs-shared surface selection introduced by the `magpie-local-convention`
  work item.  The default surface when the repo is adopted and no flag is
  passed is `"offer-choice"`; `override_path` reports the personal default.
