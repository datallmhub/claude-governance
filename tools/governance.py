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
ENTERPRISE_DOMAIN = "enterprise"
RISK_POLICY = "RISK-001"
BASELINE_POLICY = "ENT-001"
UNCLASSIFIED = ("HIGH", "Unclassified path — extend the tiers of RISK-001")
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
        if policy["domain"] == ENTERPRISE_DOMAIN and not domains:
            continue
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


def policy_by_id(policy_id):
    for policy in load_policies([ENTERPRISE_DOMAIN]):
        if policy["id"] == policy_id:
            return policy
    raise CheckError(f"policy {policy_id} not found in policies/{ENTERPRISE_DOMAIN}/")


def classify(paths, tiers):
    """Classify each path into the first matching tier; the change takes the highest one."""
    order = [tier["level"] for tier in tiers]
    per_level = {}
    for path in paths:
        for tier in tiers:
            if matches_any(path, tier["paths"]):
                per_level.setdefault((tier["level"], tier["reason"]), []).append(path)
                break
        else:
            per_level.setdefault(UNCLASSIFIED, []).append(path)

    if not per_level:
        return "LOW", "No file in scope", {}
    ranked = sorted(per_level, key=lambda key: order.index(key[0]) if key[0] in order else -1)
    level, reason = ranked[0]
    return level, reason, per_level


def run_controls(policy, level, paths):
    """Evaluate each control the matrix requires at this risk level."""
    catalogue = policy["controls"]
    detectors = {
        detector["id"]: (candidate, detector)
        for candidate in load_policies()
        for detector in candidate.get("detect") or []
    }

    controls = []
    for name in policy["matrix"][level]:
        control = catalogue[name]
        record = {"name": name, "title": control["title"], "verify": control["verify"]}
        if control["verify"] == "detectors":
            findings = []
            for detector_id in control["detectors"]:
                if detector_id not in detectors:
                    raise CheckError(f"{name}: unknown detector {detector_id}")
                owner, detector = detectors[detector_id]
                detector_findings, _ = scan(owner, detector, paths)
                findings += detector_findings
            record["findings"] = findings
            record["status"] = "FAIL" if findings else "PASS"
        else:
            record["evidence"] = control.get("evidence", "")
            record["status"] = "REQUIRED"
        controls.append(record)
    return controls


def assess(paths):
    policy = policy_by_id(RISK_POLICY)
    level, reason, per_level = classify(paths, policy["tiers"])
    controls = run_controls(policy, level, paths)
    if any(control["status"] == "FAIL" for control in controls):
        decision = "BLOCK"
    elif any(control["status"] == "REQUIRED" for control in controls):
        decision = "ESCALATE"
    else:
        decision = "PASS"
    return {
        "risk": level,
        "reason": reason,
        "decision": decision,
        "controls": controls,
        "files": {f"{key[0]}": sorted(value) for key, value in per_level.items()},
    }


def render_risk(assessment, scanned):
    lines = ["", "Change Risk Assessment", "-" * 60, ""]
    lines.append(f"Risk: {assessment['risk']} — {assessment['reason']}")
    lines.append("")
    width = max(len(control["title"]) for control in assessment["controls"])
    for control in assessment["controls"]:
        suffix = ""
        if control["status"] == "FAIL":
            suffix = f"  {len(control['findings'])} finding(s)"
        elif control["status"] == "REQUIRED":
            suffix = f"  evidence: {control['evidence']}"
        lines.append(f"  {control['title']:<{width + 2}}{control['status']:<9}{suffix}")
    for control in assessment["controls"]:
        for finding in control.get("findings") or []:
            lines.append(
                f"    {finding['file']}:{finding['line']}  [{finding['detector']}] {finding['message']}"
            )
    lines += ["", f"{len(scanned)} file(s) scanned", f"Decision: {assessment['decision']}", ""]
    return "\n".join(lines)


def gh(*args):
    """Call the GitHub CLI, returning None when it is absent, unauthenticated or failing."""
    try:
        result = subprocess.run(
            ["gh", *args], cwd=ROOT, capture_output=True, text=True, check=False
        )
    except FileNotFoundError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout


def gh_api(endpoint):
    """Read an endpoint. A 404 means the control is absent, not unreadable."""
    try:
        result = subprocess.run(
            ["gh", "api", endpoint], cwd=ROOT, capture_output=True, text=True, check=False
        )
    except FileNotFoundError:
        return "unreadable", "the GitHub CLI is not installed"
    output = result.stdout + result.stderr
    if "HTTP 404" in output or '"status":"404"' in output:
        return "absent", "not configured"
    if "HTTP 401" in output or "HTTP 403" in output:
        return "unreadable", "insufficient permission on this repository"
    if result.returncode != 0 or not result.stdout.strip():
        return "unreadable", f"cannot read {endpoint}"
    try:
        return "ok", json.loads(result.stdout)
    except json.JSONDecodeError:
        return "unreadable", f"unexpected response from {endpoint}"


def dotted(payload, path):
    for key in path.split("."):
        if not isinstance(payload, dict) or key not in payload:
            return None
        payload = payload[key]
    return payload


def expectation_met(actual, expected):
    if actual is None:
        return False
    if expected.startswith(">="):
        return isinstance(actual, (int, float)) and actual >= float(expected[2:])
    if expected.startswith("=="):
        return str(actual).lower() == expected[2:].strip().lower()
    if expected.startswith("contains:"):
        needle = expected.split(":", 1)[1]
        return any(needle in str(item) for item in actual) if isinstance(actual, list) else False
    if expected == "exists":
        return True
    raise CheckError(f"unsupported expectation '{expected}'")


def check_baseline():
    policy = policy_by_id(BASELINE_POLICY)
    context = gh("repo", "view", "--json", "nameWithOwner,defaultBranchRef")
    repo, default_branch = None, None
    if context:
        parsed = json.loads(context)
        repo = parsed.get("nameWithOwner")
        default_branch = (parsed.get("defaultBranchRef") or {}).get("name")

    results = []
    for control in policy["controls"]:
        record = {"id": control["id"], "title": control["title"], "verify": control["verify"]}
        if control["verify"] == "manual":
            record["status"] = "ATTEST"
            record["detail"] = control.get("evidence", "")
            results.append(record)
            continue
        if not repo:
            record["status"] = "UNVERIFIED"
            record["detail"] = "GitHub CLI unavailable or not authenticated"
            results.append(record)
            continue
        endpoint = control["endpoint"].format(repo=repo, default_branch=default_branch or "main")
        outcome, data = gh_api(endpoint)
        if outcome == "absent":
            record["status"] = "FAIL"
            record["detail"] = control["remediation"]
            record["failed_expectations"] = sorted(control["expect"])
            results.append(record)
            continue
        if outcome == "unreadable":
            record["status"] = "UNVERIFIED"
            record["detail"] = data
            results.append(record)
            continue
        failed = [
            field for field, expected in control["expect"].items()
            if not expectation_met(dotted(data, field), expected)
        ]
        record["status"] = "FAIL" if failed else "PASS"
        record["detail"] = control["remediation"] if failed else ""
        record["failed_expectations"] = failed
        results.append(record)

    if any(record["status"] == "FAIL" for record in results):
        decision = "BLOCK"
    elif any(record["status"] == "UNVERIFIED" for record in results):
        decision = "UNVERIFIED"
    else:
        decision = "PASS"
    return {"repository": repo, "decision": decision, "controls": results}


def render_baseline(baseline):
    lines = ["", "Platform Governance Baseline", "-" * 60, ""]
    lines.append(f"Repository: {baseline['repository'] or 'unknown'}")
    lines.append("")
    width = max(len(control["title"]) for control in baseline["controls"])
    for control in baseline["controls"]:
        lines.append(f"  {control['title']:<{width + 2}}{control['status']:<11}{control.get('detail', '')}")
    lines += ["", f"Decision: {baseline['decision']}", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["check", "report", "risk", "baseline"])
    parser.add_argument("--changed", action="store_true", help="only files changed against the base ref")
    parser.add_argument("--base", help="base ref for --changed (default: origin/main, then main)")
    parser.add_argument("--domain", action="append", help="limit to a policy domain, repeatable")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    try:
        if args.command == "baseline":
            baseline = check_baseline()
            print(json.dumps(baseline, indent=2) if args.format == "json" else render_baseline(baseline))
            return 1 if baseline["decision"] == "BLOCK" else 0

        paths = changed_files(args.base) if args.changed else tracked_files()

        if args.command == "risk":
            assessment = assess(paths)
            if args.format == "json":
                print(json.dumps({**assessment, "scanned": len(paths)}, indent=2))
            else:
                print(render_risk(assessment, paths))
            return 1 if assessment["decision"] == "BLOCK" else 0

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
