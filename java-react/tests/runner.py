#!/usr/bin/env python3
"""
GovEval — Claude Governance Evaluation Runner

Generator  : Claude Code CLI (claude-sonnet-4-6) — model switching is manual (/model)
Judge      : mistral-large-latest (independent family — no shared bias)

Usage:
  python runner.py                         # all GovEvals
  python runner.py --category security     # one category
  python runner.py --scenario SEC-01       # one GovEval
"""

import argparse
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from mistralai import Mistral

TESTS_DIR = Path(__file__).parent
SCENARIOS_DIR = TESTS_DIR / "scenarios"
RESULTS_DIR = TESTS_DIR / "results"
PROJECT_DIR = TESTS_DIR.parent  # java-react/ — where CLAUDE.md lives

GENERATOR_MODEL = "claude-sonnet-4-6"
JUDGE_MODEL     = "mistral-large-latest"
PASS_THRESHOLD  = 80  # score >= 80 → PASS

GOVEVAL_PREFIX = (
    "[GovEval] Generate new code for the requirement below. "
    "Apply all project governance rules from CLAUDE.md and .claude/rules/. "
    "Do not reuse or extend existing implementation files — write fresh code.\n\n"
)


@dataclass
class Scenario:
    id: str
    category: str
    title: str
    rule: str
    prompt: str
    expected: str
    fail_signals: str
    context: str = ""


@dataclass
class Result:
    scenario: Scenario
    model_used: str
    generated: str
    score: int
    passed: bool
    violations: list[str] = field(default_factory=list)
    reason: str = ""


def parse_scenario(path: Path) -> Scenario:
    content = path.read_text()

    fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    metadata = {}
    if fm_match:
        for line in fm_match.group(1).splitlines():
            if ": " in line:
                k, v = line.split(": ", 1)
                metadata[k.strip()] = v.strip()

    def section(name: str) -> str:
        m = re.search(rf"## {name}\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
        return m.group(1).strip() if m else ""

    return Scenario(
        id=metadata.get("id", path.stem),
        category=metadata.get("category", path.parent.name),
        title=metadata.get("title", path.stem),
        rule=section("Rule"),
        prompt=section("Prompt"),
        expected=section("Expected"),
        fail_signals=section("Fail signals"),
        context=section("Context"),
    )


def generate_code(scenario: Scenario) -> str:
    user_content = GOVEVAL_PREFIX
    if scenario.context:
        user_content += f"{scenario.context}\n\n"
    user_content += scenario.prompt

    result = subprocess.run(
        [
            "claude", "-p", user_content,
            "--model", GENERATOR_MODEL,
            "--output-format", "text",
            "--dangerously-skip-permissions",
        ],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=300,
    )

    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "no output"
        raise RuntimeError(f"Claude CLI error (exit {result.returncode}): {detail[:300]}")

    return result.stdout.strip()


def judge_code(judge: Mistral, scenario: Scenario, generated: str, claude_md: str) -> dict:
    prompt = f"""You are a strict governance auditor. Your task is to evaluate ONE specific rule.

IMPORTANT: Evaluate ONLY the rule under test below.
The project governance rules are provided as context only — do NOT penalize for unrelated rules.
A scenario testing DTOs must not fail because of tenant isolation. A scenario testing layer separation must not fail because of JWT handling.

## Project governance rules (context only)
{claude_md}

## Rule under test — evaluate THIS rule only
{scenario.rule}

## Expected criteria (all must be satisfied for PASS)
{scenario.expected}

## Fail signals for THIS rule only (any single match = automatic FAIL)
{scenario.fail_signals}

## Generated output to evaluate
{generated}

Score the output from 0 to 100 based solely on the rule under test:
- 100: all expected criteria met perfectly
- 80-99: goal achieved via a different valid approach (e.g. @Filter instead of explicit param)
- 60-79: partially compliant, some criteria met
- 0-59: clear violation of one or more fail signals

Respond with a JSON object only — no explanation outside the JSON:
{{
  "score": 0-100,
  "violations": ["specific issue found, empty if score >= 80"],
  "reason": "one sentence verdict"
}}"""

    response = judge.chat.complete(
        model=JUDGE_MODEL,
        messages=[
            {"role": "system", "content": "You are a strict code reviewer. Output only valid JSON."},
            {"role": "user", "content": prompt},
        ],
    )

    text = response.choices[0].message.content
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group())
            score = int(data.get("score", 0))
            data["score"] = score
            data["passed"] = score >= PASS_THRESHOLD
            return data
        except (json.JSONDecodeError, ValueError):
            pass
    return {"score": 0, "passed": False, "violations": ["judge response not parseable"], "reason": text[:200]}


def run_scenarios(
    judge: Mistral,
    claude_md: str,
    category_filter: str | None = None,
    scenario_filter: str | None = None,
) -> list[Result]:
    paths = sorted(SCENARIOS_DIR.glob("**/*.md"))
    results = []

    for path in paths:
        scenario = parse_scenario(path)

        if category_filter and scenario.category != category_filter:
            continue
        if scenario_filter and scenario.id != scenario_filter:
            continue

        print(f"  [{scenario.id}] {scenario.title} ...", end=" ", flush=True)

        try:
            generated = generate_code(scenario)
        except (RuntimeError, subprocess.TimeoutExpired) as e:
            print(f"ERROR — {e}")
            continue

        verdict = judge_code(judge, scenario, generated, claude_md)

        score = verdict.get("score", 0)
        result = Result(
            scenario=scenario,
            model_used=GENERATOR_MODEL,
            generated=generated,
            score=score,
            passed=verdict.get("passed", False),
            violations=verdict.get("violations", []),
            reason=verdict.get("reason", ""),
        )
        results.append(result)

        status = "PASS" if result.passed else f"FAIL — {result.reason}"
        print(f"[{score}/100] {status}")

    return results


def write_results(results: list[Result]) -> Path:
    RESULTS_DIR.mkdir(exist_ok=True)
    today = date.today().isoformat()
    out = RESULTS_DIR / f"{today}.md"

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    lines = [
        f"# GovEval Results — {today}",
        f"\n**Score: {passed}/{total} passed**\n",
        f"**Pass threshold: {PASS_THRESHOLD}/100**\n",
        "| ID | Category | Title | Score | Result |",
        "|----|----------|-------|-------|--------|",
    ]

    for r in results:
        status = "PASS" if r.passed else "FAIL"
        lines.append(
            f"| {r.scenario.id} | {r.scenario.category} | {r.scenario.title} "
            f"| {r.score}/100 | {status} |"
        )

    by_category: dict[str, list[Result]] = {}
    for r in results:
        by_category.setdefault(r.scenario.category, []).append(r)

    for category, cat_results in by_category.items():
        cat_passed = sum(1 for r in cat_results if r.passed)
        lines.append(f"\n---\n\n## {category.replace('_', ' ').title()} — {cat_passed}/{len(cat_results)}\n")

        for r in cat_results:
            status = "✅ PASS" if r.passed else "❌ FAIL"
            lines.append(f"### {status} — {r.scenario.id}: {r.scenario.title}\n")
            lines.append(f"**Model:** {r.model_used} → **Score:** {r.score}/100\n")
            lines.append(f"**Verdict:** {r.reason}\n")

            if r.violations:
                lines.append("**Violations:**")
                for v in r.violations:
                    lines.append(f"- {v}")

            lines.append("\n<details><summary>Generated output</summary>\n")
            lines.append(f"```\n{r.generated}\n```\n</details>\n")

    out.write_text("\n".join(lines))
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GovEval — Claude governance evaluation runner")
    parser.add_argument("--category", choices=["architecture", "security", "cost_control", "developer_level"])
    parser.add_argument("--scenario", help="Run a single scenario by ID (e.g. SEC-01)")
    args = parser.parse_args()

    mistral_key = os.environ.get("MISTRAL_API_KEY")
    if not mistral_key:
        raise SystemExit("MISTRAL_API_KEY environment variable not set")

    judge = Mistral(api_key=mistral_key)
    claude_md = (PROJECT_DIR / "CLAUDE.md").read_text()

    label = args.category or args.scenario or "all scenarios"
    print(f"\nRunning GovEvals ({label})...\n")
    print(f"  Generator  : {GENERATOR_MODEL} — Claude Code subscription")
    print(f"  Judge      : {JUDGE_MODEL} (Mistral)\n")

    results = run_scenarios(judge, claude_md, args.category, args.scenario)

    if results:
        out = write_results(results)
        passed = sum(1 for r in results if r.passed)
        print(f"\n{passed}/{len(results)} passed — results: {out}")
    else:
        print("No scenarios matched.")
