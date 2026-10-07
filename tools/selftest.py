#!/usr/bin/env python3
"""Prove every deterministic detector fires, so a silent regex regression cannot pass CI."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import governance  # pylint: disable=wrong-import-position

VIOLATIONS = {
    "SEC-001.literal-credential": ("config.java", 'String apiKey = "sk-live-9f2b7c41aa";'),
    "SEC-002.token-in-web-storage": ("auth.ts", 'localStorage.setItem("access_token", token);'),
    "SEC-004.sql-string-interpolation": ("repo.py", 'cur.execute("SELECT * FROM t WHERE id = %s" % uid)'),
    "SEC-004.dynamic-eval": ("run.ts", "const result = eval(userInput);"),
    "SEC-005.raw-html-injection": ("view.tsx", "<div dangerouslySetInnerHTML={{ __html: body }} />"),
    "SEC-006.wildcard-origin": ("app.py", 'app.add_middleware(CORSMiddleware, allow_origins=["*"])'),
    "SEC-010.insecure-random": ("token.ts", "const nonce = Math.random().toString(36);"),
    "SEC-010.broken-hash": ("hash.py", 'digest = hashlib.md5(password.encode()).hexdigest()'),
}


def detectors():
    for policy in governance.load_policies():
        for detector in policy.get("detect") or []:
            yield policy, detector


def main():
    failures = []
    with tempfile.TemporaryDirectory() as workdir:
        original_root = governance.ROOT
        governance.ROOT = Path(workdir)
        governance.DEFAULT_EXCLUDES = (".git/**",)
        try:
            for policy, detector in detectors():
                case = VIOLATIONS.get(detector["id"])
                if case is None:
                    failures.append(f"{detector['id']}: no self-test case")
                    continue
                name, snippet = case
                (Path(workdir) / name).write_text(snippet + "\n")
                findings, _ = governance.scan(policy, detector, [name])
                if not findings:
                    failures.append(f"{detector['id']}: did not fire on its own violation")
                    continue
                clean = f"// nothing to see here\n"
                (Path(workdir) / name).write_text(clean)
                findings, _ = governance.scan(policy, detector, [name])
                if findings:
                    failures.append(f"{detector['id']}: fired on a clean file")
                    continue
                waived = f"{snippet}  // governance: allow {detector['id']} — covered by a vault lookup\n"
                (Path(workdir) / name).write_text(waived)
                findings, waivers = governance.scan(policy, detector, [name])
                if findings or not waivers:
                    failures.append(f"{detector['id']}: inline waiver not honoured")
                else:
                    print(f"{detector['id']}: fires, stays silent on clean code, honours its waiver")
        finally:
            governance.ROOT = original_root

    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
