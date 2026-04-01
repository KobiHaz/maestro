# Skill Template — Creating Skills in Maestro

> **Template and guide** for creating new skills. Use when adding a new skill to `03-agents/skills/`.

---

## 📋 Overview

AI models are powerful generalists but don't know your specific project context or your team's standards. Loading every rule or tool into the context window leads to "tool bloat," higher costs, latency, and confusion.

**Maestro Skills** solve this through **Progressive Disclosure**. A Skill is a package of specialized knowledge that remains dormant until needed. This information is only loaded when your specific request matches the skill's description.

---

## 📁 Structure and Scope

Skills are folder-based packages. In Maestro:

| Scope | Path | Description |
| ----- | ---- | ----------- |
| **Vault** | `03-agents/skills/` | Available across the workspace |

### Skill Directory Structure

```
my-skill/
├── my-skill.md     # (Required) Metadata & instructions. Named after folder.
├── scripts/        # (Optional) Python or Bash scripts
├── references/     # (Optional) Text, documentation, templates
└── assets/         # (Optional) Images or logos
```

> **Naming:** The main skill file is `{skill-name}.md` (e.g. `code-review-checklist/code-review-checklist.md`). This ensures clear labels in Obsidian's graph view.

---

## 🔍 Example 1: Code Review Skill

This is an instruction-only skill; you only need the main skill file.

### Step 1: Create the directory

```bash
mkdir -p 03-agents/skills/code-review
```

### Step 2: Create the skill file

**`03-agents/skills/code-review/code-review.md`**:

```markdown
---
name: code-review
description: Reviews code changes for bugs, style issues, and best practices. Use when reviewing PRs or checking code quality.
allowed-tools: Read, Glob, Grep
---

# Code Review Skill

When reviewing code, follow these steps:

## Review checklist

1. **Correctness**: Does the code do what it's supposed to?
2. **Edge cases**: Are error conditions handled?
3. **Style**: Does it follow project conventions?
4. **Performance**: Are there obvious inefficiencies?

## How to provide feedback

- Be specific about what needs to change
- Explain why, not just what
- Suggest alternatives when possible
```

> **Note:** The skill file contains metadata (name, description, allowed-tools) in frontmatter, followed by the instructions.

### Try it out

Create a file `demo_bad_code.py` and prompt: `review the @demo_bad_code.py file`

The agent will identify the `code-review` skill, load the information, and follow the instructions.

---

## 📄 Example 2: License Header Skill

This skill uses a reference file in the `resources/` directory.

### Step 1: Create the directory

```bash
mkdir -p 03-agents/skills/license-header-adder/resources
```

### Step 2: Create the template file

**`03-agents/skills/license-header-adder/resources/HEADER.txt`**:

```
/*
 * Copyright (c) 2026 YOUR_COMPANY_NAME LLC.
 * All rights reserved.
 * This code is proprietary and confidential.
 */
```

### Step 3: Create the skill file

**`03-agents/skills/license-header-adder/license-header-adder.md`**:

```markdown
---
name: license-header-adder
description: Adds the standard corporate license header to new source files.
allowed-tools: Read, Write, Edit
---

# License Header Adder

This skill ensures that all new source files have the correct copyright header.

## Instructions

1. **Read the Template**: Read the content of `resources/HEADER.txt`.
2. **Apply to File**: When creating a new file, prepend this exact content.
3. **Adapt Syntax**:
   - For C-style languages (Java, TS), keep the `/* */` block.
   - For Python/Shell, convert to `#` comments.
```

### Try it out

**Prompt**: `Create a new Python script named data_processor.py that prints 'Hello World'.`

The agent will read the template, convert the comments to Python style, and add it to the top of the file.

---

## 🎯 Conclusion

By creating Skills, you transform a general AI model into an expert for your project:

- ✅ Systematize best practices
- ✅ Adhere to code review rules
- ✅ Automatically add license headers
- ✅ The agent automatically knows how to work with your team

Instead of constantly reminding the AI to "remember to add the license" or "fix the commit format," the agent will do it automatically.
