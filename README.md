# chin's Task Registry

Auto-generated from Hermes Agent's task-registry.yaml. Organized into 8 similarity clusters.

## For Zo
- **Source:** `tasks.yaml` — the canonical tasks file
- **Status field:** Zo can update `status` (active → done → paused) when checkboxes are ticked
- **Do NOT modify:** `id`, `title`, `cluster`, `priority`, `summary`, `notes` — those are the agent's domain
- **Progress reporting:** just write the `status` field back to this repo

## For the Agent (Hermes)
- Run `python3 render.py` to regenerate after registry updates
- Push updates on every change
- Read Zo's progress updates and sync back to task-registry.yaml
