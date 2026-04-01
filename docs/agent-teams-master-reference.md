# Master reference: Claude Code agent teams

**Purpose:** Design and run effective multi-session agent teams in Claude Code.  
**Canonical source:** [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams) (Anthropic — English docs).  
**Last synthesized:** 2026-04-01 (from official page structure and wording; verify critical flags and version requirements against the live doc before upgrades).

---

## Executive summary

Agent teams coordinate **multiple Claude Code instances** as one unit: a **team lead** session assigns work, teammates work in **separate context windows**, and they share a **task list** and **mailbox** for messaging. This is **not** the same as **subagents** (workers inside one session that only report to the caller).

Teams are **experimental**, **off by default**, and have **known limitations** (resumption, task coordination, shutdown). Prefer them when **parallel exploration** genuinely helps; use a single session or subagents for sequential work, tight coupling, or same-file edits.

**Minimum version:** Claude Code **v2.1.32+** (`claude --version`).

---

## When to use agent teams

Strong fits:

- **Research and review** — Different angles in parallel; findings can be challenged across teammates.
- **New modules or features** — Clear ownership of separate pieces.
- **Debugging with competing hypotheses** — Parallel theories; debate-style convergence.
- **Cross-layer work** — e.g. frontend / backend / tests with separate owners.

Avoid or reconsider when:

- Work is **sequential**, **same-file**, or **highly dependent** — overhead and token cost dominate.
- **Coordination** would exceed the value of parallelism.

### Agent teams vs subagents

| Dimension | Subagents | Agent teams |
|-----------|-----------|-------------|
| Context | Own window; results return to caller | Own window; fully independent sessions |
| Communication | Only back to main agent | Teammates message each other |
| Coordination | Main agent owns everything | Shared task list + self-coordination |
| Best for | Focused tasks where only the outcome matters | Collaboration, discussion, shared planning |
| Token cost | Lower (summarized back) | Higher (each teammate is a full instance) |

**Rule of thumb:** Subagents for quick delegated workers; agent teams when teammates must **share findings, disagree, and coordinate** without everything routing through the lead.

---

## Enable agent teams

Teams are disabled until you set:

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Or in **`settings.json`** (user / project scope as appropriate):

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Deep link to this section in the official doc: [Enable agent teams](https://code.claude.com/docs/en/agent-teams#enable-agent-teams).

---

## Start your first team

After enabling, describe the task and structure in **natural language** (e.g. roles, lenses, independence). The lead creates the team, spawns teammates, and coordinates.

**Example pattern (from docs):** independent perspectives (UX, architecture, devil’s advocate) on a greenfield idea — each can explore without blocking the others.

**UX:**

- Lead’s terminal lists teammates and their work.
- **Shift+Down** cycles teammates; message them directly. After the last teammate, focus wraps to the lead.
- **Ctrl+T** toggles the task list (in-process).
- **Enter** on a teammate: view session; **Escape** interrupts their current turn.

---

## Control your agent team

### Display modes

1. **In-process** — All teammates in the main terminal; **Shift+Down** to switch; works everywhere.
2. **Split panes** — One pane per teammate; requires **tmux** or **iTerm2** (with `it2` CLI + Python API enabled).

**Default `auto`:** split panes if already inside tmux; otherwise in-process.

**`tmux` setting:** split-pane mode; auto-detects tmux vs iTerm2.

**Global override** in `~/.claude.json`:

```json
{
  "teammateMode": "in-process"
}
```

**CLI override (single session):**

```bash
claude --teammate-mode in-process
```

**Split-pane prerequisites:**

- **tmux:** system package manager; see [tmux wiki](https://github.com/tmux/tmux/wiki).
- **iTerm2:** install `it2` CLI; enable **iTerm2 → Settings → General → Magic → Enable Python API**.

**Note:** Split panes are **not** supported in VS Code integrated terminal, Windows Terminal, or Ghostty (per official doc).

### Teammates and models

- Lead chooses count from the task, or you specify (e.g. “4 teammates”, “Sonnet for each”).

### Plan approval (risky / complex work)

Ask for teammates to work in **read-only plan mode** until the lead approves. Flow: teammate proposes plan → lead approves or rejects with feedback → revise → implement after approval.

Lead decides autonomously; steer with criteria in your prompt (e.g. require tests, reject schema changes).

### Direct messaging

Each teammate is a full session: you can redirect, clarify, or deepen work without going through the lead.

### Shared task list

States: **pending**, **in progress**, **completed**. **Dependencies** block claiming until prerequisites complete. **File locking** reduces claim races.

**Assignment:** lead assigns explicitly, or teammates **self-claim** after finishing work.

### Shut down and cleanup

- **Graceful teammate exit:** ask lead to shut down a teammate; teammate may accept or reject with reason.
- **Team cleanup:** ask lead to “clean up the team” — removes shared resources. **Fails if teammates still active** — shut them down first.
- **Always use the lead for cleanup** — teammates running cleanup can leave inconsistent state.

### Hooks (quality gates)

| Hook | When | Exit `2` behavior |
|------|------|---------------------|
| `TeammateIdle` | Teammate about to go idle | Send feedback; keep working |
| `TaskCreated` | Task being created | Block creation + feedback |
| `TaskCompleted` | Task marked complete | Block completion + feedback |

---

## How agent teams work (architecture)

**Starts:**

1. You ask for a team, or  
2. Claude **proposes** a team and waits for your confirmation — never creates without approval.

**Components:**

| Component | Role |
|-----------|------|
| Team lead | Creates team, spawns teammates, coordinates |
| Teammates | Separate Claude Code instances on tasks |
| Task list | Shared work queue and dependencies |
| Mailbox | Inter-agent messaging |

**Storage (local, auto-managed — do not hand-edit):**

- Team config: `~/.claude/teams/{team-name}/config.json` (runtime state, session IDs, tmux panes).
- Tasks: `~/.claude/tasks/{team-name}/`

**Subagent definitions:** Teammates can use a **subagent type** from project / user / plugin / CLI scope — same role as subagent and as teammate (e.g. `security-reviewer`).

**Permissions:** Teammates inherit the lead’s permission mode at spawn (including `--dangerously-skip-permissions`). Per-teammate modes can change **after** spawn, not at spawn.

**Context:** Each teammate loads normal project context (**CLAUDE.md**, MCP, skills) + spawn prompt. **Lead conversation history does not carry over.**

**Messaging:** `message` (one peer) vs `broadcast` (all — use sparingly; cost scales with team size).

**Tokens:** Usage scales with active teammates; expect **much higher** cost than one session.

---

## Use case patterns (from docs)

### Parallel code review

Split lenses (security, performance, tests) so one reviewer doesn’t over-focus on a single category; lead synthesizes.

### Competing hypotheses (debugging)

Explicit **debate**: teammates try to disprove each other’s theories to reduce anchoring and premature convergence.

---

## Best practices (checklist)

1. **Rich spawn prompts** — Teammates lack lead chat history; put paths, constraints, and success criteria in the spawn instruction.
2. **Team size** — Often **3–5** teammates; scale up only when parallelism clearly pays off. Aim for ~**5–6 tasks per teammate** as a rough balance.
3. **Task sizing** — Big enough to justify coordination; small enough for clear deliverables and check-ins.
4. **Wait for delegation** — If the lead implements instead of waiting, instruct: wait for teammates before proceeding.
5. **Onboarding** — Start with **research / review** before parallel implementation.
6. **File ownership** — Partition files to avoid overwrite conflicts.
7. **Steer actively** — Monitor, redirect, and synthesize; don’t let the team run unattended too long.

---

## Troubleshooting (quick reference)

| Symptom | What to try |
|---------|-------------|
| Teammates “missing” | **Shift+Down** (in-process); ensure task warrants a team; for split panes check `which tmux` or iTerm2 `it2` + Python API |
| Too many permission prompts | Pre-approve in permission settings before spawning |
| Teammate stops on error | Message them directly or spawn a replacement |
| Lead finishes early | Tell lead to continue / wait for teammates |
| Orphan tmux | `tmux ls` then `tmux kill-session -t <name>` |

---

## Limitations (experimental)

- **`/resume` and `/rewind`:** Do **not** restore in-process teammates; after resume, lead may message ghosts — instruct lead to spawn new teammates if needed.
- **Task status lag** — Stuck dependencies: verify work done; nudge lead or adjust status.
- **Slow shutdown** — Waits for in-flight tool work.
- **One team per lead session** — Clean up before starting another.
- **No nested teams** — Only the lead manages teammates.
- **Lead is fixed** — No promote-to-lead.
- **Per-teammate permissions** — Not set at spawn; only after.
- **CLAUDE.md** — Read from working directory as usual; use it to align all teammates.

---

## Related approaches

- **Subagents** — Lightweight delegation inside one session ([subagents doc](https://code.claude.com/docs/en/sub-agents)).
- **Manual parallelism** — e.g. **Git worktrees** + multiple Claude sessions without automated team coordination.

---

## Maestro vault note

This guide is about **Claude Code’s** native agent teams. In this vault, **03-agents/** defines workflows, routing, and human-facing “agents” for Cursor/Obsidian. Use this doc when configuring **Claude Code** multi-session teams; use **03-agents/agent-routing.md** and workflows for vault-side orchestration. Concepts overlap (task split, explicit boundaries, synthesis by a lead) but the tools and toggles differ.

---

## Changelog

| Date | Note |
|------|------|
| 2026-04-01 | Initial master reference from official agent-teams page TOC and body |
