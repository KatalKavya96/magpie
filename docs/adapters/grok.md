<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Grok Build](#grok-build)
  - [Harness contract](#harness-contract)
  - [Verified runtime](#verified-runtime)
  - [Installation](#installation)
    - [Marketplace plugin](#marketplace-plugin)
    - [Framework checkout](#framework-checkout)
    - [Pinned snapshot](#pinned-snapshot)
  - [Trust and security boundary](#trust-and-security-boundary)
  - [Guard behavior](#guard-behavior)
  - [Verify](#verify)
  - [Update and uninstall](#update-and-uninstall)
  - [Known limitations](#known-limitations)
  - [Developer checks](#developer-checks)
  - [Upstream references](#upstream-references)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

<!-- SPDX-License-Identifier: Apache-2.0 -->

# Grok Build

**Capability:** platform:harness

Grok Build is supported in this PR for the deterministic Magpie action guard.
This does not add Grok spec-loop, headless-runner, or dedicated sandbox-profile support.

## Harness contract

| Surface | Grok contract | Magpie integration |
|---|---|---|
| Hook event | `PreToolUse` | `agent-guard` |
| Shell matcher | `Bash` | `.grok/hooks/magpie-agent-guard.json` or plugin hook |
| Captured shell tool | `run_terminal_command` | reads `toolInput.command` |
| Workspace path | `GROK_WORKSPACE_ROOT` | source/snapshot project hook |
| Plugin path | `GROK_PLUGIN_ROOT` | marketplace/plugin hook |
| Deny | JSON decision with reason | shared `dispatch()` result |
| Allow | exit 0 | shared `dispatch()` result |

## Verified runtime

The adapter was verified against:

`grok 1.0.46 (2765805b9442)`

A real `PreToolUse` payload captured on 2026-10-08 is retained in
`tools/agent-guard/tests/test_grok.py`.
The capture was triggered by asking Grok to run `pwd`.
The captured event reported `toolName: "run_terminal_command"` and placed the
shell command in `toolInput.command`.

## Installation

### Marketplace plugin

Grok reads Claude-compatible marketplaces, plugins, and hooks without extra compatibility setup.
When the existing `magpie-agent-guard` marketplace plugin runs under Grok,
Grok supplies `GROK_HOOK_EVENT`.
The no-argument dispatcher detects that variable and selects `grok_main()`.
The executable therefore remains inside the installed substrate plugin rather
than requiring an `.apache-magpie/` snapshot only to reach the guard.

### Framework checkout

The repository hook is:

`.grok/hooks/magpie-agent-guard.json`

It resolves the guard through `GROK_WORKSPACE_ROOT` and invokes `--grok`.

### Pinned snapshot

A snapshot adopter may install the same single Magpie-owned project hook.
Its executable path points through
`$GROK_WORKSPACE_ROOT/.apache-magpie/tools/agent-guard/`.

Magpie owns only that exact hook file.
It does not own `.grok/hooks/`, `.grok/config.toml`, unrelated hooks, or project trust.

## Trust and security boundary

Project `.grok/hooks/` entries require an explicit Grok trust decision.
Magpie must never grant or reset that trust on the operator's behalf.

The action guard is separate from Grok permissions and from the operating-system sandbox.
It inspects shell commands before execution and rejects commands that violate a
hard Magpie framework rule.
It does not turn native file tools, MCP tools, or the rest of the process into a sandbox.

## Guard behavior

For a relevant `run_terminal_command` event, the adapter passes the command and
optional string `cwd` to the harness-neutral `dispatch()` core.

A denial emits a Grok deny decision containing the shared guard reason and exits
with the guard deny code.
An allowed shell command exits 0 without emitting a decision.

Malformed input, unrelated tools, or an invalid command field are ignored and
fail open.
A missing or broken hook executable likewise does not provide protection, so
installation verification must exercise a known allow and a known denial rather
than treating configuration presence as sufficient.

## Verify

Use:

`grok inspect --json`

Confirm that exactly one intended Magpie action-guard hook is active.

For a source or snapshot project hook, verify that its command resolves to an
existing `agent_guard/__init__.py`.
For a marketplace installation, verify that the installed
`magpie-agent-guard` plugin supplies the hook and that no duplicate project hook
was added merely to reach the executable.

Then perform harmless live probes:
one command that Magpie permits and one known guard denial.
A static configuration check does not replace the live denial probe.

## Update and uninstall

Marketplace installations follow the plugin manager lifecycle.
Updating the plugin updates its bundled guard implementation.

Source and snapshot installs compare only
`.grok/hooks/magpie-agent-guard.json` with Magpie's expected shape.
A stock stale copy may be refreshed.
A hand-edited copy must be shown for review before replacement or removal.

Repository uninstall removes only the Magpie-owned project hook.
It does not uninstall a user's marketplace plugin and does not change Grok trust.

## Known limitations

This integration is action-guard only.
It does not add a Grok-specific spec-loop runner or headless execution profile.

Hook failure is fail-open, so a broken launcher can silently remove the Magpie
enforcement layer.
Verification must therefore include a real denial probe.

The tested runtime is Grok Build 1.0.46.
Future Grok hook-schema changes require a fresh runtime capture before changing
the adapter contract.

## Developer checks

`uv run --directory tools/agent-guard --group dev pytest`

`uv run --directory tools/agent-guard --group dev python -m ruff check src tests`

## Upstream references

- xAI Hooks: https://docs.x.ai/build/features/hooks
- xAI Skills, Plugins & Marketplaces: https://docs.x.ai/build/features/skills-plugins-marketplaces
- xAI Permissions: https://docs.x.ai/build/features/permissions
- xAI CLI Reference: https://docs.x.ai/build/cli/reference
