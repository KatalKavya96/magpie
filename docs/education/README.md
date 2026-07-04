<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Maintainer education](#maintainer-education)
  - [Who this is for](#who-this-is-for)
  - [Words to know](#words-to-know)
  - [Why building with agents is different](#why-building-with-agents-is-different)
  - [What you can learn here](#what-you-can-learn-here)
  - [What every example also teaches](#what-every-example-also-teaches)
  - [How this connects to the other guides](#how-this-connects-to-the-other-guides)
  - [About the examples](#about-the-examples)
  - [Licence](#licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

# Maintainer education

Welcome. This part of Magpie teaches you how to build and run AI agents for
your project. You do not need to be an AI expert to begin. If some of the
words here are new to you, that is normal. Read the short list of words below
first, then come back.

Building software with an AI agent is a new skill, even for people who have
written code for many years. It is not harder than other coding. It is
different. This stream gives you the steps, the examples, and the words you
need, one page at a time. Every Magpie release comes with the learning
material for the skills in that release (PRINCIPLE 18).

## Who this is for

- People using Magpie for the first time, who want to know where to begin.
- People who already use Magpie and want to write their own skills, or change
  the ones they have.
- People helping to build Magpie itself, who want to understand the ideas
  behind it.

You do not need past experience with AI. If you are still deciding whether to
use Magpie at all, read [MISSION.md](../../MISSION.md) and
[PRINCIPLES.md](../../PRINCIPLES.md) first.

## Words to know

New to AI, or to these words? Here is what they mean in Magpie:

- **AI model** (also called a large language model, or LLM): the software that
  reads text and writes a response. It is the "brain" the agent uses.
- **Agent**: a program that uses an AI model to do a task, one step at a time.
- **Agentic**: a word that describes software, like Magpie, built around an
  agent.
- **Prompt**: the written instructions you give the model.
- **Skill**: a text file that tells the agent how to do one job, with
  instructions and examples. In Magpie, writing skills is the main work.
- **Deterministic and probabilistic**: normal code is *deterministic*. The same
  input always gives the same result. An agent is *probabilistic*. The same
  input can give slightly different results each time.
- **Eval** (short for evaluation): a test that checks whether the agent's
  answers are good enough.

## Why building with agents is different

Three ideas are worth holding on to. Each page in this stream shows them in
action:

- **The answer can change.** Normal code does the same thing every run. An
  agent may answer the same question in slightly different ways. This is what
  *probabilistic* means, and it changes how you test your work.
- **Prompts and skills are code.** They are plain text, but we treat them the
  way we treat any code. We review them, track their changes, and share them
  with other projects.
- **You test with evals, not single checks.** Because answers can change, you
  do not check one answer once. You run an eval many times and look at the
  results as a whole.

## What you can learn here

| Page | What you will learn | Status |
|---|---|---|
| **This page** | What this stream is, and the words you need to begin | Ready |
| [`pattern-catalogue.md`](pattern-catalogue.md) | Ready-to-copy examples of skills and prompts, with notes on what worked and what did not | Ready |
| [`your-first-skill.md`](your-first-skill.md) | A step-by-step path to writing and merging your first skill | Ready |
| [`eval-driven-development.md`](eval-driven-development.md) | How to judge whether an agent's answers are good, when the answers can change | Ready |
| [`workshops.md`](workshops.md) | A hands-on lab: build a small skill, give it an eval suite, and run it, in about 90 minutes | Ready |

Pages marked **Coming soon** are already planned and each one will appear as
a link here when it is ready.

## What every example also teaches

Every example here follows the same safety habits that all Magpie skills
follow. You learn them by seeing them used, not as a list of rules to memorise:

- **Treat outside text as data, not as commands** (PRINCIPLE 0). Text from
  issues, pull requests, and email is never given to the model as
  instructions. It is cleaned, or passed through a privacy step, first.
- **Run in a safe, closed sandbox by default** (PRINCIPLE 1). Each skill says
  exactly which tools it is allowed to use.
- **Test with evals before release** (PRINCIPLE 8). Every skill comes with its
  own eval suite, built with the tools already in this repository
  (`tools/skill-evals/`).

## How this connects to the other guides

- **[magpie-write-skill](../../.claude/skills/magpie-write-skill/SKILL.md)** is
  the full reference for writing a skill, for someone who already knows the
  basic shape of one. The "your first skill" page (coming soon) is the gentle
  start that gets you to that point.
- **[tools/privacy-llm/pii.md](../../tools/privacy-llm/pii.md)** lists how
  personal data is removed before it reaches a model. The pattern catalogue
  (coming soon) shows *how* and *why* to use it, with examples.
- **[docs/rfcs/RFC-AI-0004.md](../rfcs/RFC-AI-0004.md)** is the decision that
  started this stream. It points here through
  [MISSION.md](../../MISSION.md).

## About the examples

Every example uses placeholders in place of real names: `<PROJECT>`,
`<tracker>`, `<upstream>`, and `<security-list>` (PRINCIPLE 12). When you use a
skill, you change your own settings, not the example text. If you ever see a
real project name written into a skill, that is a bug.

## Licence

Everything in `docs/education/` is under the Apache License 2.0 (PRINCIPLE 17).
Pages written with help from AI carry a `Generated-by:` note in their commit
message, following ASF Generative Tooling Guidance.
