Run GovEval — the governance validation test suite.

## What this command does

Runs automated tests that verify the governance rules are actually followed.
Each scenario sends a natural prompt to the generator, then an independent judge model scores the output.

## Prerequisites

- `MISTRAL_API_KEY` environment variable must be set (judge model)
- Python 3.11+ with dependencies installed:
  ```bash
  cd <stack>/tests && pip install -r requirements.txt
  ```

## Steps

1. Read `.claude-governance` in the project root to find the active stack (e.g. `java-react`)
2. Locate `<stack>/tests/runner.py`
3. Run the appropriate command based on $ARGUMENTS:

**No arguments — run all scenarios:**
```bash
cd <stack>/tests && python runner.py
```

**Filter by category:**
```bash
cd <stack>/tests && python runner.py --category <category>
```
Available categories: `architecture`, `security`, `cost_control`, `developer_level`

**Run a single scenario:**
```bash
cd <stack>/tests && python runner.py --scenario <ID>
```
Example: `python runner.py --scenario SEC-01`

## After the run

- Results are saved to `<stack>/tests/results/<date>.md`
- Show a summary table of PASS/FAIL per scenario
- For each FAIL, show the violation and suggest which rule file to tighten

## Error handling

- If `.claude-governance` is missing: tell the user to run `/setup` first
- If `MISTRAL_API_KEY` is not set: show the exact export command to run
- If `runner.py` is not found for the active stack: inform the user that GovEval is not yet implemented for that stack and point to the open issues
