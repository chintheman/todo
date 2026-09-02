# Obsidian: The Life-Changing Use Cases
*What power users actually build on top of a plain folder of Markdown — and what changes when they do.*

## ⚡ TL;DR — the 5 biggest

1. **Your notes become a queryable database** — [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) and the core [Bases](https://obsidian.md/help/bases) plugin turn scattered notes into live dashboards you never maintain by hand.
2. **Your vault becomes an AI's long-term memory** — [Local REST API + MCP server](https://github.com/coddingtonbear/obsidian-local-rest-api) lets agents read *and write* your vault directly.
3. **Semantic retrieval beats folders** — [Smart Connections](https://smartconnections.app/) embeds every note locally and surfaces the ones you forgot you wrote.
4. **Notes you actually remember** — [Spaced Repetition](https://stephenmwangi.com/obsidian-spaced-repetition/) reviews flashcards *and whole notes* (FSRS/SM-2) in-vault.
5. **Writing gets easier over time** — atomic [evergreen notes](https://notes.andymatuschak.org/z2hQEhqWkdRLL9JUwfawZZx) plus [Maps of Content](https://www.linkingyourthinking.com/) mean essays and specs get *assembled*, not written from zero.

## 🧭 The Use Cases (grouped)

### Second brain & capture
- **Frictionless web capture** — the official [Obsidian Web Clipper](https://obsidian.md/help/web-clipper) saves any page or selection into your vault as Markdown, with per-site templates and natural-language extraction prompts. Life-changing because the gap between "I should save this" and "it's filed correctly" drops to one keystroke.
  - **For Chin:** replaces the front half of your link-ingest scripts on mobile, and its templates can pre-fill your Phase-1 frontmatter.
- **The inbox that empties itself** — a [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) query over `00 - Inbox` sorted by age, pinned to your homepage. An inbox you can *see decaying* gets processed; one you must remember to open doesn't.

### Thinking & writing
- **Evergreen / atomic notes** — one note = one concept, titled as a claim, in your own words ([Matuschak](https://notes.andymatuschak.org/z2hQEhqWkdRLL9JUwfawZZx)). Concept-factored notes create surprise links across books and domains you'd never have spotted, so writing compounds instead of resetting each project.
- **Maps of Content (MOCs)** — Nick Milo's [Linking Your Thinking](https://www.linkingyourthinking.com/): a hand-curated index note that acts as a "workbench" for a cluster of ideas, created at the *mental squeeze point* (when a topic overloads you). Structure without folders — one note can live in many maps, or none.
  - **For Chin:** your `concepts/` layer is already atomic; MOCs are the missing Phase-4 artifact. One MOC per active area beats one giant index.
- **Canvas for visual thinking** — the infinite canvas stores as [JSON Canvas](https://jsoncanvas.org/), an open MIT format with Python/Go/Rust/TS libraries. Spatial arrangement surfaces structure linear notes hide — except the boxes are *your real notes* and the file is parseable by your own scripts.

### Learning that sticks
- **Spaced repetition in-vault** — [Obsidian Spaced Repetition](https://stephenmwangi.com/obsidian-spaced-repetition/) supports inline `Q::A` cards, multi-line cards and clozes, scheduled with FSRS or SM-2, with all state in plaintext. You stop re-reading and start retrieving; the note from six months ago stays *in your head*, not just on disk.
- **Note-level review, not just flashcards** — the same plugin can review *whole notes* on a schedule, a resurfacing engine for your best ideas. Cheaper than making cards, and it fights note-graveyard rot.
  - **For Chin:** tag ~30 concept notes `#flashcards`, review 10 min/day. CCA-F material is exactly this use case.

### Knowledge work
- **Dataview as a query layer** — DQL (SQL-ish), DataviewJS and inline `key:: value` fields turn frontmatter into a live vault-wide index ([docs](https://blacksmithgu.github.io/obsidian-dataview/)). Every "where did I write about X / what's still open" question becomes a saved query instead of a search-and-scroll.
- **Bases: notes as a real database** — core [Bases](https://obsidian.md/help/bases) (Obsidian 1.9+) gives table/card/list views over any note set, with property filters and formula columns, backed by plain YAML. It's *core*, so no plugin-abandonment risk.
  - **For Chin:** Bases is enabled in your vault and unused. `entities/` is a database pretending to be files — one Base over it is a 10-minute win.
- **Backlinks as thinking tools** — the point isn't the pretty graph; it's opening a concept note and seeing every context it ever appeared in.

### Life admin & personal CRM
- **Tasks that live with their context** — [Tasks](https://publish.obsidian.md/tasks/) turns Markdown checkboxes into queryable objects with due dates, priorities, recurrence and dependencies. Tasks stay attached to the note that explains *why* — no more contextless todo app.
- **Personal CRM from links you already make** — a note per person + `last_contact::` field + a [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) query for "haven't spoken in 90 days". Every meeting note that `[[mentions]]` them auto-builds their history via backlinks. Relationships get maintained by a system, not by guilt.
- **Journaling + habits** — daily notes with two tracked properties (`mood::`, `sleep::`) become a queryable longitudinal record of your life. Nobody regrets this at year five.

### AI-powered Obsidian
- **Semantic search over everything you've written** — [Smart Connections](https://smartconnections.app/) embeds your vault with a zero-config *local* model, shows related notes in a sidebar, and offers RAG chat grounded in your notes. Retrieval stops depending on you recalling the right keyword.
- **Agents with read/write access to your vault** — [Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) exposes a bearer-authenticated REST API *and* a built-in MCP server at `https://127.0.0.1:27124/mcp/`, so Claude Code, Cursor or any Streamable-HTTP MCP client can list, read, search, append and patch notes. Your second brain becomes an agent's working memory *and* output target.
  - **For Chin:** highest-leverage single install — Hermes writing Phase-2 concept notes directly, schema enforced in code, not prompts.

### Publishing
- **Obsidian Publish** — official vault-as-website hosting with hover previews and graph, $8/mo per site, custom domain ([obsidian.md/publish](https://obsidian.md/publish)). Zero-maintenance note-to-public.
- **Quartz (free)** — [jackyzha0/quartz](https://github.com/jackyzha0/quartz) builds a digital garden from your Markdown; point it at a folder, push to GitHub, Actions deploys. *Publishing changes how you write* — notes someone might read get finished.

## ✅ Quick-start actions

1. `[P0]` Install **Local REST API**, point Claude Code at its MCP endpoint — **Benefit:** agents read/write your vault natively. **Why:** 1,478 notes, zero community plugins — biggest unlock for an agent builder.
2. `[P0]` Build one **Base** over `entities/` (table view, filter by type) — **Benefit:** a real database view of people/orgs in ~10 min. **Why:** Bases is already enabled and unused.
3. `[P0]` Install **Dataview**; add inbox-age and "concepts with no backlinks" queries to `index.md` — **Benefit:** orphans and stale inbox items become visible. **Why:** your pipeline has no feedback loop showing where it stalls.
4. `[P1]` Install **Smart Connections** and let it index — **Benefit:** semantic retrieval + RAG chat over 1,478 notes. **Why:** keyword search stops scaling past ~1k notes.
5. `[P1]` Install **Spaced Repetition**, tag 30 concept notes `#flashcards` — **Benefit:** CCA-F material survives to recall. **Why:** re-reading doesn't work.
6. `[P1]` Add one **MOC** per active area, created at the squeeze point — **Benefit:** the synthesis layer your pipeline lacks. **Why:** atomic notes and links exist; curated workbench notes don't.
7. `[P2]` Install **Tasks**, migrate open items into the notes explaining them — **Benefit:** tasks carry context. **Why:** only worth it once dashboards exist.
8. `[P2]` Publish a curated subset with **Quartz** — **Benefit:** public writing forces finishing. **Why:** highest-effort, most-optional item here.

## 📚 Sources

- [Obsidian Web Clipper — official help](https://obsidian.md/help/web-clipper)
- [Evergreen notes should be concept-oriented — Andy Matuschak](https://notes.andymatuschak.org/z2hQEhqWkdRLL9JUwfawZZx)
- [Linking Your Thinking (Maps of Content) — Nick Milo](https://www.linkingyourthinking.com/)
- [JSON Canvas — open infinite-canvas format](https://jsoncanvas.org/)
- [Obsidian Spaced Repetition — docs](https://stephenmwangi.com/obsidian-spaced-repetition/)
- [Dataview — official docs](https://blacksmithgu.github.io/obsidian-dataview/)
- [Bases — Obsidian help](https://obsidian.md/help/bases)
- [Tasks — official docs](https://publish.obsidian.md/tasks/)
- [Smart Connections](https://smartconnections.app/)
- [Obsidian Local REST API + MCP server](https://github.com/coddingtonbear/obsidian-local-rest-api)
- [Obsidian Publish](https://obsidian.md/publish)
- [Quartz — digital garden SSG](https://github.com/jackyzha0/quartz)
