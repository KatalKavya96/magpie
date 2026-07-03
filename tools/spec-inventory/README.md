<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [spec-inventory](#spec-inventory)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
  - [Run tests](#run-tests)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

# spec-inventory

**Capability:** substrate:framework-dev + substrate:analytics

**Harness:** agnostic

A deterministic `uv` tool that emits a compact routing inventory for the
spec-loop prompts. It summarizes spec frontmatter, where-it-lives hints,
validation commands, known gaps, skill frontmatter, and tool/test
presence so agents can choose what to read next without first scanning
the whole repository.

The output is a routing aid, not proof. Prompts still require direct file
reads or code search before declaring behaviour present or absent.

## Prerequisites

- **Runtime:** Python 3.11+ run via `uv`; stdlib-only (no runtime
  dependencies). The `dev` group pulls `pytest`, `ruff`, and `mypy`.
- **CLIs:** None beyond the runtime.
- **Credentials / auth:** None.
- **Network:** Runs fully offline; reads local specs, skills, and tool
  metadata from the repository checkout.

## Usage

```bash
uv run --project tools/spec-inventory spec-inventory
uv run --project tools/spec-inventory spec-inventory --brief --max-where 1 --max-validation 1 --max-gaps 1
uv run --project tools/spec-inventory spec-inventory --json
```

## Run tests

```bash
uv run --project tools/spec-inventory --group dev pytest tools/spec-inventory/tests
```
