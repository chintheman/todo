# Zo — Task Registry Page Improvements
## chin's Labs · 0xsteamboat.me/labs

Hey Zo! Here's the feedback from the Hermes agent review of the Labs page, plus a comprehensive
feature list for making the to-do tracking seamless.

---

## YAML Source (what you're reading)

**Repo:** `github.com/chintheman/todo` → `tasks.yaml`

### YAML Structure (v2)

```yaml
cluster_order:            # ← NEW: ordered list of clusters for GROUP BY
  - emoji: 🔄
    name: Agent Orchestration & Loops
  - emoji: 📈
    name: Crypto & Quant Trading
  # ... 8 clusters total

clusters:
  - emoji: 🔄
    name: Agent Orchestration & Loops
    count: 12
    active_count: 12        # ← NEW
    delegated_count: 0      # ← NEW
    done_count: 0           # ← NEW
    items:
      - id: ...
        title: ...
        type: build|research|discuss|create
        domain: ai/ml|crypto|creative|devops|career|business|meta|general|gtm|strategy|finance
        priority: p0|p1|p2|p3
        status: active|delegated|done|paused
        summary: "..."       # ⭐ THE MOST IMPORTANT FIELD — full description
        deadline: "YYYY-MM-DD"|null  # ← already in YAML, just needs display
        notes: "..."         # file paths, GitHub links, cross-references
        source: "..."        # where it came from
        captured: "YYYY-MM-DD"
        cluster: "Agent Orchestration & Loops"

updated_at: "2026-07-18 13:48:12 SGT"  # ← NEW: use this to show freshness
total_active: 58                        # ← NEW
total_done: 0                           # ← NEW
```

---

## Priority Improvements

### 1. Task Summaries (HIGH)
**Current:** Clicking a task navigates away or opens a separate page.
**Wanted:** One line of `summary` shown directly on the **collapsed card** — between the title and the meta row — so 90% of cards are self-explanatory without clicking.

```
┌─────────────────────────────────┐
│ 🔄 Build an agent that...       │  ← title (bold)
│ An agent that does X and Y...   │  ← summary (muted, 1 line, truncated)
│ P2 · build · ai/ml · 📅 Jul 30 │  ← meta row
└─────────────────────────────────┘
```

The `summary` field in the YAML is already the right text — just needs rendering inline. If summary is empty, fall back to showing `notes` (first line) or leave the card with just title + meta (shorter cards are fine).

On click/tap: still expand to full drawer showing the complete `summary`, `notes`, `source`, `deadline`, and all other metadata.

The `summary` is the MAIN reason someone clicks — right now they see a headline but can't understand
what the task actually IS without opening GitHub.

### 2. Cluster Grouping View (HIGH)
**Current:** CATEGORY groups by `domain` (ai/ml, creative, devops, etc.)
**Wanted:** Add a third GROUP BY option: **CLUSTER**

This uses `cluster_order` at the top of the YAML for the group order, and each item's `cluster`
field for assignment. The 8 clusters are:

| Order | Emoji | Cluster Name |
|-------|-------|-------------|
| 1 | 🔄 | Agent Orchestration & Loops |
| 2 | 📈 | Crypto & Quant Trading |
| 3 | 🎨 | Creative Agency & Content |
| 4 | 🛠️ | Dev Tools & Infrastructure |
| 5 | 🧠 | AI Models & Provider Landscape |
| 6 | 💼 | Career & Content Publishing |
| 7 | 💡 | Business Ideas & Products |
| 8 | 📋 | Other Active (Delegated / Backlog) |

Also add **CLUSTER** to the filter dropdowns (alongside domain names).

### 3. Default Sort: P0 First (MEDIUM)
**Current:** Priority sort defaults to ascending (P3 → P2 → P1 → P0).
**Wanted:** Default to descending (P0 at the top). The DESC/ASC toggle is already there —
just ship with DESC as default.

### 4. Deadline Display (MEDIUM)
**Current:** Only `captured` date shows.
**Wanted:** When `deadline` field exists, show it with a visual indicator (e.g. `📅 Jul 30`)
alongside or instead of the captured date. Deadlines are action dates — they should stand out.

---

## Nice-to-Haves

### 5. Rich Indicators Per Task
- **Has notes:** Show a 📄 icon when the `notes` field is populated (indicates there's supporting docs)
- **Has source:** Show a 🔗 icon when `source` field exists
- **Delegated:** Visual distinction for `status: delegated` vs `status: active` (e.g., an arrow badge)

### 6. Stats Per Cluster
When viewing in cluster mode, show per-cluster counts:
```
🔄 Agent Orchestration & Loops (12) — 0 done · 12 active
📈 Crypto & Quant Trading (4) — 0 done · 4 active
```

### 7. Last Updated Indicator
Display `updated_at` in the header so viewers know how fresh the data is.

### 8. Done Counter
When tasks are marked done (status changes to `done` in the YAML), the stats bar should reflect:
`58 TASKS · 3 DONE · 54 ACTIVE · 1 DELEGATED`

---

## How Updates Flow

```
Hermes Agent (chin's PA) 
  → updates task-registry.yaml (SSOT)
  → runs render-todo-yaml.py
  → pushes updated tasks.yaml to GitHub
  → Zo pulls the new YAML
  → Page refreshes
```

**Zo is READ-ONLY.** No write-back needed. The page reads from GitHub and displays.
Progress updates come from the Hermes agent (chin tells the agent "mark X as done"
and the agent updates the YAML).

The REFRESH button you already have is perfect for this.

---

## Summary

| Priority | What | Effort |
|----------|------|--------|
| 🔴 HIGH | Summaries on click/tap | Medium |
| 🔴 HIGH | Cluster grouping + cluster filter | Medium |
| 🟡 MEDIUM | Default sort: P0 first | Low |
| 🟡 MEDIUM | Deadline display | Low |
| 🟢 NICE | Rich indicators (📄, 🔗) | Low |
| 🟢 NICE | Per-cluster stats | Low |
| 🟢 NICE | Last updated display | Low |
| 🟢 NICE | Done/delegated counters | Low |

Chin also wants to review the final product. Loop me in when you've made changes
and I'll re-review against the YAML.
