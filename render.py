#!/usr/bin/env python3
"""Render clustered task-registry.yaml into a clean GitHub-facing YAML + HTML report.

Cluster assignments are hardcoded — this IS the categorization layer.
Run after any registry update. Outputs to ~/.hermes/data/gh-tasks.yaml

Cluster-assignment drift checking (unassigned + stale) is delegated to
personal-assistant-bot's pa_engine.check_cluster_assignment() — see
github.com/chintheman/personal-assistant-bot, skill/scripts/pa_engine.py.
"""

import sys, os, re

REGISTRY = os.path.expanduser("~/wiki/_system/task-registry.yaml")
OUTPUT = os.path.expanduser("~/.hermes/data/gh-tasks.yaml")

# personal-assistant-bot's skill directory is symlinked here once deployed
# (see that repo's setup/INSTALL.md) — import its engine's tested
# cluster-assignment-drift check instead of duplicating the logic inline.
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/personal-assistant-bot/scripts"))
from pa_engine import check_cluster_assignment

# ── Cluster definitions ──
# Every active item ID must appear in exactly one cluster.
CLUSTERS_ORDERED = [
    {
        "emoji": "🔄",
        "name": "Agent Orchestration & Loops",
        "ids": [
            "agency-agents-deep-dive",
            "vibe-coding-vs-vibe-engineering",
            "karpathy-vibe-to-agentic",
            "claude-code-loops-google-meta-ads",
            "agency-agent-pm-integration",
            "agency-agent-fa-integration",
            "agency-agent-nexus-integration",
            "agency-agent-highlights-review",
            "claude-command-cheatsheet",
            "auto-goal-orchestration-plugin",
            "tool-decision-framework",
            "profile-isolation-deep-dive",
            "anthropic-finance-agents",
            "multi-agent-orchestration-guide",
            "agentic-stack-review",
            "graph-engineering-patterns",
            "altman-self-prompting-systems",
        ],
    },
    {
        "emoji": "📈",
        "name": "Crypto & Quant Trading",
        "ids": [
            "agentic-trader",
            "tradingview-mcp-integration",
            "quant-repos-review",
            "deepseek-v4-open-source",
            "nicholascrown-macro-letter",
            "claude-code-ai-hedge-fund",
        ],
    },
    {
        "emoji": "🎨",
        "name": "Creative Agency & Content",
        "ids": [
            "ig-carousel-frameworks",
            "openmontage-video-pipeline",
            "toto-generator-refine",
            "agent-ad-network-skill",
            "arcads-stop-motion-pipeline",
            "learn-animated-websites",
            "showreel",
            "improve-graphic-design",
            "up-dog-ai-chatbot",
            "cinematic-camera-angles",
            "genrecon-3d-reconstruction",
            "unreal-engine-mcp-hermes",
            "blender-mcp-hermes",
            "claude-code-ai-content-team",
        ],
    },
    {
        "emoji": "🛠️",
        "name": "Dev Tools & Infrastructure",
        "ids": [
            "hermes-session-pruning-update",
            "oh-my-hermes-review",
            "buzz-block-review",
            "github-spec-kit-eval",
            "codebase-memory-mcp",
            "context-dev-evaluate",
            "agent-reach",
            "claude-code-v2-1-203",
            "vps-shared-memory",
            "kimi-code-evaluate",
            "safari-mcp-server",
            "omniroute-local-gateway",
            "hyperbrowser-eval",
            "openwa-eval",
            "gittrendio-discovery-feed",
            "repowise-eval",
            "i-have-adhd-claude-skill",
            "mcp-host-60-minutes",
        ],
    },
    {
        "emoji": "🧠",
        "name": "AI Models & Provider Landscape",
        "ids": [
            "glm-5-eval",
            "kyutai-pocket-tts-evaluate",
            "orca-ade",
            "anthropic-ust-claude",
            "chinese-ai-enterprise-adoption-ft",
        ],
    },
    {
        "emoji": "💼",
        "name": "Career & Content Publishing",
        "ids": [
            "ai-adoption-specialist",
            "career-advice-age-of-ai",
            "profile-review-phil-chen-framework",
            "start-substack",
        ],
    },
    {
        "emoji": "💡",
        "name": "Business Ideas & Products",
        "ids": [
            "money-making-ideas-review",
            "potential-biz-ideas-master",
            "jonathan-lok-workshop",
            "qol-second-brain-apps",
            "interior-design-agent-tools",
            "ai-influencer-monetization",
        ],
    },
    {
        "emoji": "📋",
        "name": "Other Active (Delegated / Backlog)",
        "ids": [
            "gtm-second-brain",
            "explore-smart-internet-sites",
            "rokos-basilisk-deep-dive",
            "telegram-games-exploration",
            "toto-automated-betting",
            "ai-stack-platforms-review",
            "learn-obsidian",
            "lint-rejected-cleanup",
            "lint-confidence-downgrade",
        ],
    },
]


def load_ids_with_status():
    """Parse the registry YAML robustly, returning {id: status} dict for all items."""
    import yaml

    with open(REGISTRY) as f:
        raw = f.read()

    # Remove shell-command debris (echo/grep lines)
    lines = [l for l in raw.split("\n") if not l.startswith("echo ") and not l.startswith("grep ")]
    raw = "\n".join(lines)

    data = yaml.safe_load(raw)
    tasks = data.get("tasks", [])
    out = {}
    for t in tasks:
        tid = t.get("id")
        if tid:
            out[tid] = t
    return out


def compute_quadrant(t, today):
    """Eisenhower quadrant from importance (priority) + urgency (flag or deadline ≤7d).

    Q1 DO-NOW     = important (p0/p1) + urgent
    Q2 SCHEDULE   = important + not urgent
    Q3 DELEGATE   = not important (p2/p3) + urgent
    Q4 BACKLOG    = not important + not urgent
    """
    from datetime import datetime

    important = t.get("priority") in ("p0", "p1")
    urgent = bool(t.get("urgent"))
    dl = t.get("deadline")
    if dl and not urgent:
        try:
            dl_date = datetime.strptime(str(dl)[:10], "%Y-%m-%d").date()
            days_left = (dl_date - today).days
            # Only deadlines today or within the next 7 days are urgent;
            # past deadlines (negative days) don't auto-flag.
            urgent = 0 <= days_left <= 7
        except (ValueError, TypeError):
            pass
    if urgent and important:
        return "Q1"
    if not urgent and important:
        return "Q2"
    if urgent and not important:
        return "Q3"
    return "Q4"


def build_clustered(registry):
    """Build clustered export with all item fields Zo needs."""
    from datetime import datetime, timezone, timedelta, date
    SGT = timezone(timedelta(hours=8))
    today = datetime.now(SGT).date()

    result = {
        "cluster_order": [],
        "clusters": [],
        "updated_at": datetime.now(SGT).strftime("%Y-%m-%d %H:%M:%S SGT"),
        "total_active": 0,
        "total_done": 0,
        "matrix_summary": {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0},
    }

    for cdef in CLUSTERS_ORDERED:
        cluster = {
            "emoji": cdef["emoji"],
            "name": cdef["name"],
            "items": [],
        }
        for tid in cdef["ids"]:
            t = registry.get(tid)
            if t is None:
                print(f"  ⚠️  ID '{tid}' not found in registry — skipping", file=sys.stderr)
                continue
            if t.get("status") not in ("active", "delegated"):
                print(f"  ⚠️  '{tid}' is '{t.get('status')}' not active — skipping", file=sys.stderr)
                continue

            # Build clean export item
            item = {}
            for field in [
                "id", "title", "type", "domain", "priority", "status",
                "summary", "deadline", "captured", "source",
                "delegated_to", "completed", "outcome", "resolution",
                "notes", "urgent",
            ]:
                val = t.get(field)
                if val:
                    item[field] = val

            # Add cluster label + Eisenhower quadrant
            item["cluster"] = cdef["name"]
            item["quadrant"] = compute_quadrant(t, today)
            result["matrix_summary"][item["quadrant"]] += 1

            cluster["items"].append(item)

        cluster["count"] = len(cluster["items"])
        cluster["items"].sort(key=lambda x: (0 if x.get("priority") == "p0" else 1 if x.get("priority") == "p1" else 2 if x.get("priority") == "p2" else 3, x.get("title", "")))

        # Track counts
        active = sum(1 for i in cluster["items"] if i.get("status") == "active")
        delegated = sum(1 for i in cluster["items"] if i.get("status") == "delegated")
        done = sum(1 for i in cluster["items"] if i.get("status") == "done")
        cluster["active_count"] = active
        cluster["delegated_count"] = delegated
        cluster["done_count"] = done
        
        result["total_active"] += active + delegated
        result["total_done"] += done

        # Add cluster order entry
        result["cluster_order"].append({
            "emoji": cdef["emoji"],
            "name": cdef["name"],
        })
        result["clusters"].append(cluster)

    # Cluster-assignment drift check — delegates to pa_engine's tested
    # function instead of the inline, one-directional check this used to
    # do. Also surfaces the "stale" direction (ids sitting in a cluster's
    # ids list that are no longer active/delegated, or missing from the
    # registry entirely) that this script never checked before.
    cluster_defs = [{"name": cdef["name"], "ids": cdef["ids"]} for cdef in CLUSTERS_ORDERED]
    drift = check_cluster_assignment(registry, cluster_defs)
    for tid in drift["unassigned"]:
        print(f"  ❌ '{tid}' is active but NOT ASSIGNED to any cluster!", file=sys.stderr)
    for tid in drift["stale"]:
        print(f"  ⚠️  '{tid}' is listed in a cluster but is not active/delegated (or missing from registry) — stale cluster entry", file=sys.stderr)

    return result


def dump_yaml(data):
    """Dump as clean YAML with nice formatting."""
    import yaml
    # Use ruamel-style block formatting for summaries
    return yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120, indent=2)


def main():
    print("Reading registry...")
    registry = load_ids_with_status()
    print(f"  {len(registry)} total items, {sum(1 for t in registry.values() if t.get('status') in ('active', 'delegated'))} active")

    print("Building clusters...")
    data = build_clustered(registry)

    total = sum(c["count"] for c in data["clusters"])
    print(f"  {total} items across {len(data['clusters'])} clusters")

    yaml_out = dump_yaml(data)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w") as f:
        f.write(yaml_out)

    print(f"✅ Written {len(yaml_out)} chars → {OUTPUT}")

    # Summary
    for c in data["clusters"]:
        p0 = sum(1 for i in c["items"] if i.get("priority") == "p0")
        p1 = sum(1 for i in c["items"] if i.get("priority") == "p1")
        p2 = sum(1 for i in c["items"] if i.get("priority") == "p2")
        p3 = sum(1 for i in c["items"] if i.get("priority") == "p3")
        parts = []
        if p0: parts.append(f"{p0}×P0")
        if p1: parts.append(f"{p1}×P1")
        if p2: parts.append(f"{p2}×P2")
        if p3: parts.append(f"{p3}×P3")
        print(f"  {c['emoji']} {c['name']}: {c['count']} ({', '.join(parts)})")

    ms = data["matrix_summary"]
    print(f"Eisenhower matrix: Q1-do {ms['Q1']} · Q2-schedule {ms['Q2']} · Q3-delegate {ms['Q3']} · Q4-backlog {ms['Q4']}")


if __name__ == "__main__":
    main()
