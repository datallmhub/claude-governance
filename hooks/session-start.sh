#!/bin/bash
# Injects active governance stack summary at session start.
# Reads .claude-governance in the project root to determine the active stack.

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
GOVERNANCE_FILE="$PROJECT_DIR/.claude-governance"

if ! command -v jq >/dev/null 2>&1; then
  jq -cn '{"priority": "INFO", "message": "claude-governance: jq is required but not found. Install it with `brew install jq` or `apt-get install jq`."}'
  exit 0
fi

if [ ! -f "$GOVERNANCE_FILE" ]; then
  jq -cn '{"priority": "INFO", "message": "claude-governance: no active stack found in this project. Run /setup to initialize governance for your stack."}'
  exit 0
fi

STACK=$(cat "$GOVERNANCE_FILE" | tr -d '[:space:]')

jq -cn \
  --arg stack "$STACK" \
  '{
    priority: "IMPORTANT",
    message: ("claude-governance active — stack: " + $stack + "\n\nRules loaded automatically from CLAUDE.md and .claude/rules/.\nAvailable commands: /gov-check · /scaffold · /security-review · /new-migration\n\nCRITICAL rules in effect:\n- Every repository query must filter by organizationId (from JWT, never from request)\n- Always use publicId (UUID) in URLs — never expose internal id (Long)\n- Controller → Service → Repository. No layer skipping.\n- No secrets in code. No unbounded List<T> on collection endpoints.")
  }'
