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

"""Tests for the harness-neutral audit-any subcommand."""

from __future__ import annotations

import json
from pathlib import Path

from permission_audit.cli import main


def _claude_settings(path: Path, allow: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"permissions": {"allow": allow}}, indent=2) + "\n",
        encoding="utf-8",
    )


def _opencode_config(path: Path, permission: object) -> None:
    path.write_text(
        json.dumps({"permission": permission}, indent=2) + "\n",
        encoding="utf-8",
    )


def test_no_settings_files_exits_zero(tmp_path, capsys):
    rc = main(["audit-any", "--dir", str(tmp_path)])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert out["detected_harnesses"] == []
    assert out["results"] == []
    assert out["has_forbidden"] is False


def test_only_claude_code_clean(tmp_path, capsys):
    _claude_settings(tmp_path / ".claude" / "settings.json", ["Bash(lychee *)"])
    rc = main(["audit-any", "--dir", str(tmp_path), "--families", ""])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert out["detected_harnesses"] == ["claude-code"]
    assert out["has_forbidden"] is False
    assert out["results"][0]["forbidden"] == []


def test_claude_code_forbidden_exits_nonzero(tmp_path, capsys):
    _claude_settings(tmp_path / ".claude" / "settings.json", ["Bash(uv run *)"])
    rc = main(["audit-any", "--dir", str(tmp_path)])
    out = json.loads(capsys.readouterr().out)
    assert rc == 1
    assert out["has_forbidden"] is True
    assert out["results"][0]["forbidden"][0]["pattern"] == "Bash(uv run *)"


def test_only_opencode_clean(tmp_path, capsys):
    _opencode_config(tmp_path / "opencode.json", {"bash": {"*": "ask"}})
    rc = main(["audit-any", "--dir", str(tmp_path)])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert out["detected_harnesses"] == ["opencode"]
    assert out["has_forbidden"] is False
    # OpenCode results have no missing_recommended key
    assert "forbidden" in out["results"][0]


def test_opencode_forbidden_exits_nonzero(tmp_path, capsys):
    _opencode_config(tmp_path / "opencode.json", "allow")
    rc = main(["audit-any", "--dir", str(tmp_path)])
    out = json.loads(capsys.readouterr().out)
    assert rc == 1
    assert out["has_forbidden"] is True
    assert out["results"][0]["forbidden"][0]["kind"] == "blanket-allow"


def test_both_harnesses_detected(tmp_path, capsys):
    _claude_settings(tmp_path / ".claude" / "settings.json", ["Bash(lychee *)"])
    _opencode_config(tmp_path / "opencode.json", {"bash": {"*": "ask"}})
    rc = main(["audit-any", "--dir", str(tmp_path)])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert set(out["detected_harnesses"]) == {"claude-code", "opencode"}
    assert len(out["results"]) == 2


def test_both_harnesses_one_forbidden(tmp_path, capsys):
    _claude_settings(tmp_path / ".claude" / "settings.json", ["Bash(lychee *)"])
    _opencode_config(tmp_path / "opencode.json", "allow")
    rc = main(["audit-any", "--dir", str(tmp_path)])
    out = json.loads(capsys.readouterr().out)
    assert rc == 1
    assert out["has_forbidden"] is True


def test_claude_local_settings_detected_separately(tmp_path, capsys):
    _claude_settings(tmp_path / ".claude" / "settings.json", [])
    _claude_settings(tmp_path / ".claude" / "settings.local.json", ["Bash(uv run *)"])
    rc = main(["audit-any", "--dir", str(tmp_path)])
    out = json.loads(capsys.readouterr().out)
    assert rc == 1
    assert "claude-code" in out["detected_harnesses"]
    assert "claude-code-local" in out["detected_harnesses"]
    # Only the local file has the forbidden entry
    local_result = next(r for r in out["results"] if r["harness"] == "claude-code-local")
    assert len(local_result["forbidden"]) == 1


def test_dir_defaults_to_cwd_and_respects_explicit_dir(tmp_path, capsys):
    # Explicitly setting --dir should let us point at any directory
    _claude_settings(tmp_path / ".claude" / "settings.json", [])
    rc = main(["audit-any", "--dir", str(tmp_path), "--families", ""])
    out = json.loads(capsys.readouterr().out)
    assert out["dir"] == str(tmp_path)
    assert rc == 0


def test_families_scoping_passed_through_to_claude_audit(tmp_path, capsys):
    # With no families, only the default "" bucket is checked.
    # "Bash(lychee *)" is in the "" bucket; with it present, no missing_recommended.
    _claude_settings(tmp_path / ".claude" / "settings.json", ["Bash(lychee *)"])
    rc = main(["audit-any", "--dir", str(tmp_path), "--families", ""])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert out["results"][0]["missing_recommended"] == []
