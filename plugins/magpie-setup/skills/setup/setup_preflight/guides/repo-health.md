<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

# 🐦 Magpie here — your repository-health sidekick

A one-minute tour, then straight back to what you asked for.

## 🔄 The typical flow

1. 🏃 **Audit CI runners** for outdated labels — *"audit our CI runners"*
2. 🔒 **Check workflows** for security risks — *"audit workflow security"*
3. 📦 **Audit dependencies** for vulnerabilities and license obligations — *"audit dependencies"*
4. 📜 **Check compliance** across LICENSE and NOTICE — *"check license compliance"*
5. 🧪 **Triage flaky tests** to separate flakes from regressions — *"find flaky tests"*
6. 🛠️ **Draft a fix** for an audit finding — *"draft a fix for this finding"*

The six audit skills report findings without modifying project files.
`dependency-license-audit` checks dependency license obligations.
`audit-finding-fix` prepares fixes; `--draft-pr` additionally requires explicit approval.

## ⚙️ Configure it

Some skills need project-specific settings:

- ⚙️ **Audit policy** — `repo-health-config.md` for dependency, workflow-security, license-compliance and flaky-test audits
- 🛠️ **Fix workflow** — `fix-workflow.md` and `runtime-invocation.md` for `audit-finding-fix`
- 📋 **Other audits** — CI runner and dependency-license audits have no required config

Configure personally with `/magpie-setup:setup config`.
Project adoption with `/magpie-setup:setup adopt` is a maintainer decision.

## 💬 Just ask

Talk to Magpie in plain language:

- *"find obsolete CI runner labels"*
- *"check GitHub Actions permissions and triggers"*
- *"audit dependency vulnerabilities and licenses"*
- *"check LICENSE and NOTICE compliance"*
- *"investigate flaky tests in CI"*
- *"draft a tested fix for this audit finding"*

## 🎨 Make it yours

Describe the checks or reporting style you prefer:

- *"use our project's flaky-test thresholds"*
- *"focus workflow security findings on high-risk triggers"*

Review proposed configuration or override changes before applying them.
Useful elsewhere? Ask *"upstream this change to Magpie"* to prepare a contribution for review.

<!-- welcome footer: generated from guides/_footer.md -->
