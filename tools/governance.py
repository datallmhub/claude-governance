#!/usr/bin/env python3
"""Verify a working tree against the policies declared in policies/.

Only deterministic evaluators run here: a finding is a regex match on a file a
policy's detector targets. Severity decides the outcome — critical and high
block, medium and low warn — so the decision is reproducible on any machine.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POLICIES = ROOT / "policies"
BLOCKING = ("critical", "high")
WAIVER_RE = re.compile(r"governance:\s*allow\s+([A-Z]+-\d+\.[\w-]+)\s*[—-]\s*(\S.*)")
DEFAULT_EXCLUDES = (
    ".git/**", "policies/**", "tools/**", "**/.claude/rules/**", "**/*.md",
)


class CheckError(Exception):
    pass


def glob_to_regex(pattern):
    """Translate a glob with ** segments into an anchored regex."""
    out, index = [], 0
    while index < len(pattern):
        char = pattern[index]
        if pattern.startswith("**/", index):
            out.append("(?:.*/)?")
            index += 3
        elif char == "*":
            out.append("[^/]*")
            index += 1
        elif char == "?":
            out.append("[^/]")
            index += 1
        else:
            out.append(re.escape(char))
            index += 1
    return re.compile("".join(out) + r"\Z")


def matches_any(path, patterns):
    return any(glob_to_regex(pattern).match(path) for pattern in patterns)


def git(*args):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise CheckError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.splitlines()


def changed_files(base):
    """Files added, copied or modified against the base ref, plus uncommitted work."""
    if base is None:
        for candidate in ("origin/main", "main", "HEAD"):
            try:
                base = git("rev-parse", "--verify", "--quiet", candidate)[0]
                break
            except (CheckError, IndexError):
                continue
    paths = set(git("diff", "--name-only", "--diff-filter=ACM", base))
    paths |= set(git("diff", "--name-only", "--diff-filter=ACM", "HEAD"))
    paths |= set(git("ls-files", "--others", "--exclude-standard"))
    return sorted(paths)


def tracked_files():
    return sorted(git("ls-files"))


def load_policies(domains=None):
    if not POLICIES.is_dir():
        raise CheckError(f"no policy directory at {POLICIES}")
    import yaml  # imported here so `--help` works without the dependency

    policies = []
    for domain_dir in sorted(POLICIES.iterdir()):
        if not domain_dir.is_dir() or (domains and domain_dir.name not in domains):
            continue
        for policy_path in sorted(domain_dir.glob("*.yml")):
            policy = yaml.safe_load(policy_path.read_text())
            policy["domain"] = domain_dir.name
            policies.append(policy)
    if not policies:
        raise CheckError("no policy to evaluate")
    return policies


def scan(policy, detector, paths):
    """Return the findings and the waivers of one detector over the given paths."""
    include = detector.get("include") or ["**/*"]
    exclude = list(DEFAULT_EXCLUDES) + list(detector.get("exclude") or [])
    pattern = re.compile(detector["pattern"])
    severity = detector.get("severity", policy["severity"])
    findings, waivers = [], []

    for path in paths:
        if not matches_any(path, include) or matches_any(path, exclude):
            continue
        file_path = ROOT / path
        if not file_path.is_file():
            continue
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(lines, start=1):
            if not pattern.search(line):
                continue
            waiver = WAIVER_RE.search(line) or (
                WAIVER_RE.search(lines[number - 2]) if number > 1 else None
            )
            record = {
                "policy": policy["id"],
                "detector": detector["id"],
                "severity": severity,
                "message": detector["message"],
                "file": path,
                "line": number,
            }
            if waiver and waiver.group(1) == detector["id"]:
                record["waived_because"] = waiver.group(2).strip()
                waivers.append(record)
            else:
                findings.append(record)
    return findings, waivers


def evaluate(paths, domains=None):
    results = []
    for policy in load_policies(domains):
        if not policy.get("enforcement", {}).get("ci", False):
            continue
        detectors = policy.get("detect") or []
        findings, waivers = [], []
        for detector in detectors:
            if detector.get("evaluator") != "regex":
                raise CheckError(f"{policy['id']}: unsupported evaluator {detector.get('evaluator')}")
            detector_findings, detector_waivers = scan(policy, detector, paths)
            findings += detector_findings
            waivers += detector_waivers
        results.append({
            "id": policy["id"],
            "domain": policy["domain"],
            "title": policy["title"],
            "severity": policy["severity"],
            "automated": bool(detectors),
            "findings": findings,
            "waivers": waivers,
        })
    return results


def decide(results):
    blocking = [
        finding
        for result in results
        for finding in result["findings"]
        if finding["severity"] in BLOCKING
    ]
    warning = [
        finding
        for result in results
        for finding in result["findings"]
        if finding["severity"] not in BLOCKING
    ]
    if blocking:
        return "BLOCK"
    return "WARN" if warning else "PASS"


def status_of(result):
    if not result["automated"]:
        return "AGENT-ONLY"
    if not result["findings"]:
        return "PASS"
    return "FAIL" if any(f["severity"] in BLOCKING for f in result["findings"]) else "WARN"


def render_text(results, decision, scanned):
    width = max(len(result["title"]) for result in results)
    lines = ["", "Governance Report", "-" * (width + 24), ""]
    for result in results:
        count = len(result["findings"])
        suffix = f"  {count} finding(s)" if count else ""
        lines.append(f"{result['id']:<9}{result['title']:<{width + 2}}{status_of(result):<11}{suffix}")

    findings = [finding for result in results for finding in result["findings"]]
    if findings:
        lines.append("")
        for finding in findings:
            lines.append(
                f"  {finding['file']}:{finding['line']}  [{finding['detector']}] {finding['message']}"
            )
    waivers = [waiver for result in results for waiver in result["waivers"]]
    for waiver in waivers:
        lines.append(f"  waived {waiver['file']}:{waiver['line']}  [{waiver['detector']}] {waiver['waived_because']}")

    lines += ["", f"{len(scanned)} file(s) scanned", f"Decision: {decision}", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["check", "report"])
    parser.add_argument("--changed", action="store_true", help="only files changed against the base ref")
    parser.add_argument("--base", help="base ref for --changed (default: origin/main, then main)")
    parser.add_argument("--domain", action="append", help="limit to a policy domain, repeatable")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    try:
        paths = changed_files(args.base) if args.changed else tracked_files()
        results = evaluate(paths, args.domain)
    except CheckError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    decision = decide(results)
    if args.format == "json":
        print(json.dumps({"decision": decision, "scanned": len(paths), "policies": results}, indent=2))
    else:
        print(render_text(results, decision, paths))

    if args.command == "report":
        return 0
    return 1 if decision == "BLOCK" else 0


if __name__ == "__main__":
    sys.exit(main())
