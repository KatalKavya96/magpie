# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Tests for Grok Build's PreToolUse adapter."""

from __future__ import annotations

import io
import json
import os
import subprocess
from pathlib import Path

import pytest

import agent_guard


def _feed(monkeypatch: pytest.MonkeyPatch, payload: object) -> None:
    text = payload if isinstance(payload, str) else json.dumps(payload)
    monkeypatch.setattr("sys.stdin", io.StringIO(text))


def _event(
    command: str,
    *,
    tool_name: str = "run_terminal_command",
    cwd: object = ".",
) -> dict[str, object]:
    return {
        "hookEventName": "pre_tool_use",
        "hook_event_name": "PreToolUse",
        "sessionId": "test-session",
        "cwd": cwd,
        "workspaceRoot": ".",
        "permissionMode": "default",
        "toolName": tool_name,
        "toolInput": {"command": command},
    }


def test_denied_command_emits_exact_grok_decision(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        agent_guard,
        "dispatch",
        lambda command, cwd=None: "blocked by test",
    )
    _feed(monkeypatch, _event("git push"))

    assert agent_guard.grok_main() == agent_guard.DENY_EXIT

    captured = capsys.readouterr()
    assert captured.out == '{"decision": "deny", "reason": "blocked by test"}\n'
    assert captured.err == ""


def test_allowed_command_emits_exact_grok_decision(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(agent_guard, "dispatch", lambda command, cwd=None: None)
    _feed(monkeypatch, _event("git status"))

    assert agent_guard.grok_main() == agent_guard.ALLOW_EXIT

    captured = capsys.readouterr()
    assert captured.out == '{"decision": "allow"}\n'
    assert captured.err == ""


@pytest.mark.parametrize(
    "tool_name",
    ["run_terminal_command", "run_terminal_cmd"],
)
def test_shell_tool_aliases_reach_dispatch(
    monkeypatch: pytest.MonkeyPatch,
    tool_name: str,
) -> None:
    seen: list[tuple[str, str | None]] = []

    def fake_dispatch(command: str, cwd: str | None = None) -> str | None:
        seen.append((command, cwd))
        return None

    monkeypatch.setattr(agent_guard, "dispatch", fake_dispatch)
    _feed(
        monkeypatch,
        _event("git status", tool_name=tool_name, cwd="/repo"),
    )

    assert agent_guard.grok_main() == agent_guard.ALLOW_EXIT
    assert seen == [("git status", "/repo")]


@pytest.mark.parametrize("cwd", [None, [], 42])
def test_invalid_or_missing_cwd_forwards_none(
    monkeypatch: pytest.MonkeyPatch,
    cwd: object,
) -> None:
    seen: list[str | None] = []

    def fake_dispatch(command: str, cwd: str | None = None) -> str | None:
        seen.append(cwd)
        return None

    monkeypatch.setattr(agent_guard, "dispatch", fake_dispatch)

    event = _event("git status", cwd=cwd)
    if cwd is None:
        event.pop("cwd")

    _feed(monkeypatch, event)

    assert agent_guard.grok_main() == agent_guard.ALLOW_EXIT
    assert seen == [None]


@pytest.mark.parametrize(
    "payload",
    [
        "not JSON",
        "[]",
        "null",
        json.dumps(
            {
                "toolName": "read_file",
                "toolInput": {"path": "README.md"},
            }
        ),
        json.dumps({"toolName": "run_terminal_command"}),
        json.dumps(
            {
                "toolName": "run_terminal_command",
                "toolInput": [],
            }
        ),
        json.dumps(
            {
                "toolName": "run_terminal_command",
                "toolInput": {},
            }
        ),
        json.dumps(
            {
                "toolName": "run_terminal_command",
                "toolInput": {"command": None},
            }
        ),
        json.dumps(
            {
                "toolName": "run_terminal_command",
                "toolInput": {"command": 42},
            }
        ),
    ],
)
def test_irrelevant_or_malformed_event_fails_open_silently(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    payload: str,
) -> None:
    def unexpected_dispatch(*args: object) -> None:
        pytest.fail("Malformed or irrelevant Grok event reached dispatch")

    monkeypatch.setattr(agent_guard, "dispatch", unexpected_dispatch)
    _feed(monkeypatch, payload)

    assert agent_guard.grok_main() == agent_guard.ALLOW_EXIT
    assert capsys.readouterr() == ("", "")


def test_cli_routes_grok_flag_to_adapter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(agent_guard, "grok_main", lambda: 37)

    assert agent_guard.cli(["--grok"]) == 37


def test_default_invocation_remains_claude(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GROK_HOOK_EVENT", "pre_tool_use")
    monkeypatch.setattr(agent_guard, "main", lambda: 41)
    monkeypatch.setattr(
        agent_guard,
        "grok_main",
        lambda: pytest.fail("Explicit --grok is required"),
    )

    assert agent_guard.cli([]) == 41


def test_project_hook_runs_grok_adapter_end_to_end() -> None:
    """The committed Grok hook must invoke this adapter, not the tool command."""
    repo_root = Path(agent_guard.__file__).resolve().parents[4]
    hook_file = repo_root / ".grok" / "hooks" / "magpie-agent-guard.json"

    config = json.loads(hook_file.read_text())
    groups = config["hooks"]["PreToolUse"]

    assert len(groups) == 1
    assert groups[0]["matcher"] == "^(run_terminal_command|run_terminal_cmd)$"

    handlers = groups[0]["hooks"]
    assert len(handlers) == 1

    handler = handlers[0]
    assert handler["type"] == "command"
    assert handler["timeout"] == 30
    assert handler["command"].endswith('tools/agent-guard/src/agent_guard/__init__.py" --grok')

    event = _event(
        "git commit -m 'x\\n\\nCo-Authored-By: A <a@b.c>'",
        cwd=str(repo_root),
    )

    result = subprocess.run(
        handler["command"],
        shell=True,
        cwd=repo_root,
        env={
            **os.environ,
            "GROK_WORKSPACE_ROOT": str(repo_root),
        },
        input=json.dumps(event),
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == agent_guard.DENY_EXIT
    assert result.stderr == ""

    response = json.loads(result.stdout)
    assert response["decision"] == "deny"
    assert "commit-trailer" in response["reason"]
