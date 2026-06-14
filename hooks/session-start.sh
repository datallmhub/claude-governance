#!/bin/bash
# Injects active governance stack summary at session start.
# Reads .claude-governance in the project root to determine the active stack.
# Extracts the CRITICAL section from the stack's CLAUDE.md if available.

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-${CLAUDE_PROJECT_ROOT:-$(pwd)}}"
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

# Locate the stack's CLAUDE.md — plugin install or manual copy
STACK_CLAUDE_MD=""
if [ -n "${CLAUDE_PLUGIN_ROOT}" ] && [ -f "${CLAUDE_PLUGIN_ROOT}/${STACK}/CLAUDE.md" ]; then
  STACK_CLAUDE_MD="${CLAUDE_PLUGIN_ROOT}/${STACK}/CLAUDE.md"
elif [ -f "$PROJECT_DIR/CLAUDE.md" ]; then
  STACK_CLAUDE_MD="$PROJECT_DIR/CLAUDE.md"
fi

# Extract CRITICAL section if present
CRITICAL_RULES=""
if [ -n "$STACK_CLAUDE_MD" ]; then
  CRITICAL_RULES=$(awk '/^## CRITICAL/,/^---/' "$STACK_CLAUDE_MD" 2>/dev/null \
    | grep -E '^\- \*\*' \
    | sed 's/- \*\*[^*]*\*\*: /- /' \
    | head -8)
fi

if [ -n "$CRITICAL_RULES" ]; then
  RULES_BLOCK="Critical rules in effect:
${CRITICAL_RULES}"
else
  RULES_BLOCK="Rules loaded from CLAUDE.md and .claude/rules/ — active on every file."
fi

COMMANDS="Commands: /gov-check · /scaffold · /security-review · /new-migration · /gov-eval"

jq -cn \
  --arg stack "$STACK" \
  --arg rules "$RULES_BLOCK" \
  --arg commands "$COMMANDS" \
  '{
    priority: "IMPORTANT",
    message: ("claude-governance active — stack: " + $stack + "\n\n" + $rules + "\n\n" + $commands)
  }'
