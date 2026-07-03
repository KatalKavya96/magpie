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

from __future__ import annotations

import json
from pathlib import Path

from spec_inventory import (
    build_inventory,
    compact_metadata_value,
    first_description_line,
    format_json,
    format_markdown,
    parse_frontmatter,
    parse_project_scripts,
    validation_commands,
)


def test_parse_frontmatter_handles_block_scalars_and_comments() -> None:
    text = """<!-- SPDX-License-Identifier: Apache-2.0 -->

---
name: magpie-example
mode: Triage
description: |
  First line.
  Second line.
capability: capability:triage
license: Apache-2.0
---
"""

    fm = parse_frontmatter(text)

    assert fm["name"] == "magpie-example"
    assert fm["mode"] == "Triage"
    assert fm["description"] == "First line.\nSecond line."
    assert fm["capability"] == "capability:triage"


def test_validation_commands_extracts_non_comment_lines() -> None:
    text = """---
title: Example
status: experimental
kind: feature
mode: infra
---

## Validation

```bash
# comment
bash -n tools/spec-loop/loop.sh
uv run --project tools/spec-validator spec-validate
```
"""

    assert validation_commands(text, 2) == [
        "bash -n tools/spec-loop/loop.sh",
        "uv run --project tools/spec-validator spec-validate",
    ]


def test_first_description_line_skips_blank_lines() -> None:
    assert first_description_line("\n\n  Useful sentence.\nMore.") == "Useful sentence."


def test_compact_metadata_value_handles_yaml_list() -> None:
    assert compact_metadata_value("- capability:triage\n- capability:review") == (
        "capability:triage, capability:review"
    )


def test_parse_project_scripts_only_reads_scripts_table() -> None:
    pyproject = """[project]
name = "example"
version = "0.1.0"

[project.scripts]
example-tool = "example:main"

[tool.ruff]
line-length = 100
"""

    assert parse_project_scripts(pyproject) == ["example-tool"]


def test_build_inventory_summarizes_specs_skills_and_tools(tmp_path: Path) -> None:
    specs_dir = tmp_path / "tools" / "spec-loop" / "specs"
    specs_dir.mkdir(parents=True)
    (specs_dir / "example.md").write_text(
        """<!-- SPDX-License-Identifier: Apache-2.0 -->

---
title: Example Spec
status: experimental
kind: feature
mode: infra
source: tests
acceptance:
  - It works.
---

# Example Spec

## What it does

Thing.

## Where it lives

- `tools/example/`

## Behaviour & contract

Thing.

## Out of scope

Thing.

## Acceptance criteria

1. Thing.

## Validation

```bash
uv run --project tools/example pytest
```

## Known gaps

- Needs more tests.
"""
    )
    (specs_dir / "README.md").write_text("# skip\n")

    skill_dir = tmp_path / "skills" / "example"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        """---
name: magpie-example
mode: Triage
description: |
  Summarize an example.
capability: capability:triage
license: Apache-2.0
---
"""
    )

    tool_dir = tmp_path / "tools" / "example"
    tool_dir.mkdir(parents=True)
    (tool_dir / "pyproject.toml").write_text(
        """[project.scripts]
example-tool = "example:main"
"""
    )
    (tool_dir / "tests").mkdir()

    inventory = build_inventory(tmp_path, max_where=2, max_validation=2, max_gaps=2)

    assert inventory.specs[0].title == "Example Spec"
    assert inventory.specs[0].where == ["`tools/example/`"]
    assert inventory.specs[0].validation == ["uv run --project tools/example pytest"]
    assert inventory.specs[0].known_gaps == ["Needs more tests."]
    assert inventory.skills[0].name == "magpie-example"
    assert inventory.skills[0].capability == "capability:triage"
    assert inventory.tools[0].path == "tools/example"
    assert inventory.tools[0].scripts == ["example-tool"]


def test_formatters_emit_markdown_and_json(tmp_path: Path) -> None:
    specs_dir = tmp_path / "tools" / "spec-loop" / "specs"
    specs_dir.mkdir(parents=True)
    (specs_dir / "example.md").write_text(
        """---
title: Example
status: stable
kind: feature
mode: infra
source: tests
acceptance:
  - It works.
---

## Where it lives
- `tools/example/`
## Validation
```bash
bash -n tools/example/run.sh
```
## Known gaps
- None.
"""
    )
    (tmp_path / "skills").mkdir()
    (tmp_path / "tools" / "example").mkdir(parents=True)
    (tmp_path / "tools" / "example" / "README.md").write_text("# Example\n")

    inventory = build_inventory(tmp_path, max_where=1, max_validation=1, max_gaps=1)
    markdown = format_markdown(inventory)
    brief_markdown = format_markdown(inventory, brief=True)
    parsed = json.loads(format_json(inventory))

    assert "Compact repository inventory" in markdown
    assert "`tools/spec-loop/specs/example.md`" in markdown
    assert "Example" in brief_markdown
    assert parsed["specs"][0]["title"] == "Example"
