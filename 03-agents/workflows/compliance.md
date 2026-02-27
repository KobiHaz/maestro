---
name: compliance
description: Healthcare compliance audit. Scans the site for Banned keywords, missing disclaimers, and structural issues.
---

# Healthcare Compliance Audit Workflow

This workflow activates the `compliance-auditor` agent to verify the site against healthcare regulations.

## Steps

1. **Verify Agent**
   - Check if `compliance-auditor` is active and rules are loaded.

2. **Run Scanner**
   - Invoke `compliance-auditor` agent from `03-agents/specialists/`.
   - If script present: `python 03-agents/skills/compliance-audit/scripts/compliance_checker.py .` (or project path)
   - Otherwise: compliance-auditor performs manual audit.

3. **Analyze Findings**
   - The agent reviews the script output.
   - Categorize issues into Critical (Stop-ship) vs Warming (Fix soon).

4. **Recommendation**
   - Suggest specific text replacements for flagged items.
   - Identify missing files (e.g., Privacy Policy page).

## Usage
Run `/compliance` to start the audit.
