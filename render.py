#!/usr/bin/env python3
"""Render clustered task-registry.yaml into a clean GitHub-facing YAML + HTML report.

Cluster assignments are hardcoded — this IS the categorization layer.
Run after any registry update. Outputs to ~/.hermes/data/gh-tasks.yaml
"""

import sys, os, re

REGISTRY = os.path.expanduser("~/wiki/_system/task-registry.yaml")
OUTPUT = os.path.expanduser("~/.hermes/data/gh-tasks.yaml")

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
        ],
    },
    {
        "emoji": "🛠️",
        "name": "Dev Tools & Infrastructure",
        "ids": [
            "hermes-session-pruning-update",
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


def build_clustered(registry):
    """Build clustered export with all item fields Zo needs."""
    result = {"clusters": []}

    all_active_ids = set()

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

            all_active_ids.add(tid)

            # Build clean export item
            item = {}
            for field in [
                "id", "title", "type", "domain", "priority", "status",
                "summary", "deadline", "captured", "source",
                "delegated_to", "completed", "outcome", "resolution",
                "notes",
            ]:
                val = t.get(field)
                if val:
                    item[field] = val

            # Add cluster label
            item["cluster"] = cdef["name"]

            cluster["items"].append(item)

        cluster["count"] = len(cluster["items"])
        cluster["items"].sort(key=lambda x: (0 if x.get("priority") == "p0" else 1 if x.get("priority") == "p1" else 2 if x.get("priority") == "p2" else 3, x.get("title", "")))
        result["clusters"].append(cluster)

    # Check for unassigned active items
    for tid, t in registry.items():
        if t.get("status") in ("active", "delegated") and tid not in all_active_ids:
            print(f"  ❌ '{tid}' is active but NOT ASSIGNED to any cluster!", file=sys.stderr)

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


if __name__ == "__main__":
    main()
