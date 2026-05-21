#!/usr/bin/env bash
# Maestro vault — engineering invariants (CI + local).
# Keep in sync with 02-projects/maestro/engineering-invariants.md
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail() {
  echo "::error::$1"
  echo "FAILED: $1" >&2
  exit 1
}

pass() {
  echo "OK: $1"
}

# INV-MAESTRO-001
if [[ ! -f 03-agents/workflows/invariant-sentinel.md ]]; then
  fail "INV-MAESTRO-001 missing 03-agents/workflows/invariant-sentinel.md"
fi
pass "INV-MAESTRO-001 invariant-sentinel workflow present"

# INV-MAESTRO-002
if ! git grep -q 'workflows/invariant-sentinel.md' -- 03-agents/agent-routing.md 2>/dev/null; then
  fail "INV-MAESTRO-002 agent-routing.md must reference workflows/invariant-sentinel.md"
fi
pass "INV-MAESTRO-002 agent-routing references invariant-sentinel"

# INV-MAESTRO-003
if [[ ! -f 05-templates/engineering-invariants.md ]]; then
  fail "INV-MAESTRO-003 missing 05-templates/engineering-invariants.md"
fi
pass "INV-MAESTRO-003 engineering-invariants template present"

# INV-MAESTRO-004 — frontmatter name (first 20 lines)
if ! head -n 20 03-agents/workflows/invariant-sentinel.md | grep -q '^name: invariant-sentinel'; then
  fail "INV-MAESTRO-004 invariant-sentinel.md must contain frontmatter line: name: invariant-sentinel"
fi
pass "INV-MAESTRO-004 invariant-sentinel frontmatter name"

# INV-MAESTRO-005 — PEM / private key material in tracked content
# Match common PEM headers only (avoid matching the word "private" in prose loosely).
# Exclude this script and docs files that legitimately reference the pattern.
if git grep -nE 'BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|BEGIN PRIVATE KEY-----' \
    -- . \
    ':!scripts/invariants-check.sh' \
    ':!02-projects/maestro/engineering-invariants.md' \
    ':!05-templates/engineering-invariants.md' \
    >/tmp/inv-pem.txt 2>/dev/null && [[ -s /tmp/inv-pem.txt ]]; then
  cat /tmp/inv-pem.txt >&2
  fail "INV-MAESTRO-005 PEM private key block detected in tracked files"
fi
pass "INV-MAESTRO-005 no PEM private key blocks in git-tracked files"

echo ""
echo "All Maestro engineering invariants passed."
