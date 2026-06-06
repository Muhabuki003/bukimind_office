# 🤖 BUKIMIND Office — Hermes Handoff Plan

> Everything Hermes needs to keep the live virtual office (bukimind-office.pages.dev) updated with real activity. The site is already deployed. This doc is the contract.

---

## ✅ What's already done

- **App is live:** `https://bukimind-office.pages.dev` (repo: `Muhabuki003/bukimind-office`, served by Cloudflare Pages)
- The app polls a status file every 5 seconds and animates the office from it
- The app reads from: `https://raw.githubusercontent.com/Muhabuki003/bukimind-status/main/status.json`

## 🎯 What Hermes does from here

1. Make sure the `bukimind-status` repo exists with a `status.json`
2. On a schedule (cron), gather **real** signals, rewrite `status.json`, commit, and push
3. Never touch the `bukimind-office` app repo

---

## 🗂️ The two repos

| Repo | Purpose | Who writes | Cloudflare |
|---|---|---|---|
| `bukimind-office` | The app (index.html) | Am, rarely | Watches & serves |
| `bukimind-status` | Just `status.json` | **Hermes, often** | Ignores it |

Splitting them means frequent status pushes never trigger Cloudflare rebuilds (free tier = 500 builds/month) and Hermes can't break the live app.

---

## 📋 status.json schema (the contract)

Hermes must always write **valid JSON** in exactly this shape:

```json
{
  "updated": "2026-06-06T16:00:00Z",
  "agents": [
    { "id": "orchestrator", "status": "working", "task": "short task line", "output": "multi-line\\nwork log", "bubble": "optional short popup" },
    { "id": "auditor",      "status": "working", "task": "...", "output": "..." },
    { "id": "researcher",   "status": "idle",    "task": "...", "output": "..." },
    { "id": "builder",      "status": "idle",    "task": "...", "output": "..." },
    { "id": "content",      "status": "idle",    "task": "...", "output": "..." },
    { "id": "qa",           "status": "idle",    "task": "...", "output": "..." }
  ],
  "events": [
    { "agent": "AUDIT", "msg": "Found 3 dead routes" },
    { "agent": "BUILD", "msg": "2 new inquiries in inbox" }
  ],
  "metrics": {
    "tasks": 47,
    "prs": 12,
    "bars": { "loveflix": 67, "bookistudio": 34, "dropship": 0, "content": 0 }
  }
}
```

### Rules
- **Agent `id`s are fixed:** `orchestrator`, `auditor`, `researcher`, `builder`, `content`, `qa`. Never rename or add.
- **`status`** is one of: `working`, `idle`, `done`.
- **`task`** = one short line (shows under the agent).
- **`output`** = multi-line log (use `\n`). Optional inline tags allowed: `<span class="hl">`, `<span class="ok">`, `<span class="wn">`.
- **`bubble`** = optional short speech-bubble text; include it only when the agent just finished something noteworthy.
- **`events`** = keep the **last 6 only**. Each `agent` should match a display name: `BUKIMIND`, `AUDIT`, `RESEARCH`, `BUILD`, `CONTENT`, `QA`, or `SYSTEM`.
- **`bars`** values are 0–100 integers.
- Always update the `updated` ISO timestamp.

---

## 🔌 Mapping real signals → agents

Only report what's actually true. Mark everything else `idle` honestly until its integration exists.

| Agent | Real signal Hermes can read TODAY | If no signal |
|---|---|---|
| **orchestrator** | One-line summary of overall state | "Standing by" |
| **auditor** (LoveFlix) | LoveFlix repo: last commit msg, open issues, TODO count, failing checks | idle "No audit running" |
| **builder** (BookiStudio) | `founder@bookistudios.com` unread inquiries count | idle "No new inquiries" |
| **researcher** (Dropship) | *(no TikTok integration yet)* | idle "Integration pending" |
| **content** (Social) | *(no social integration yet)* | idle "Integration pending" |
| **qa** | *(runs after builder)* | idle "Awaiting build" |

**Metrics suggestions:**
- `tasks` → commits across your repos in the last 7 days (or a running counter)
- `prs` → open PR count on the LoveFlix repo
- `bars.loveflix` → rough % of audit todos resolved
- `bars.bookistudio` → pipeline stage of the newest inquiry
- `bars.dropship` / `bars.content` → 0 until wired

---

## 🔁 Git workflow Hermes runs each cycle

```bash
# ensure local clone exists (first run)
[ -d ~/bukimind-status ] || git clone https://github.com/Muhabuki003/bukimind-status.git ~/bukimind-status
cd ~/bukimind-status
git pull --quiet

# (Hermes writes the new status.json here)

git add status.json
git commit -m "chore: office status update"
git push --quiet
```

Cloudflare does NOT rebuild on these pushes (different repo). The office picks up the change within ~5 seconds via the raw CDN (cache-busted).

---

## ⏰ The cron job (paste into Hermes → Cron)

**Name:** `Office Status Sync`
**Frequency:** every 15 minutes (or every 5 while actively working)
**Deliver to:** (none needed — this just writes a file)

**Prompt:**
```
You maintain the BUKIMIND virtual office status feed.

1. Ensure a local clone of https://github.com/Muhabuki003/bukimind-status exists at ~/bukimind-status (clone it if missing), then `git pull`.

2. Gather REAL signals:
   - LoveFlix repo: latest commit message, open issue count, and any obvious TODO/FIXME count. This drives the "auditor" agent.
   - Check founder@bookistudios.com for unread inquiry emails. The count drives the "builder" agent.
   - Summarize overall state for the "orchestrator" agent.
   - For "researcher", "content", and "qa": mark idle with an honest "pending integration" or "awaiting build" task — do NOT invent activity.

3. Write ~/bukimind-status/status.json following EXACTLY this schema (valid JSON, fixed agent ids orchestrator/auditor/researcher/builder/content/qa, status one of working|idle|done, events = last 6 max, bars 0-100, update the ISO timestamp):
   [paste the schema block from BUKIMIND-OFFICE-HERMES.md]

4. Only report things that are actually true. If a signal is unavailable, set that agent idle with an honest task line.

5. Commit with message "chore: office status update" and push. Do not touch the bukimind-office app repo.

6. Validate the JSON parses before committing. If it doesn't parse, fix it and retry.
```

---

## 🧪 One-time setup (paste into Hermes once, before the cron)

```
Set up the BUKIMIND office status feed:

1. Create a new PUBLIC GitHub repo named "bukimind-status" under Muhabuki003 (use gh CLI or the GitHub API). If you cannot create it, tell me and I'll create it manually.

2. Clone it to ~/bukimind-status.

3. Create status.json with all six agents (orchestrator, auditor, researcher, builder, content, qa) — set orchestrator and auditor to a real current state if you can read the LoveFlix repo, set the rest to idle with honest task lines. Follow the schema in BUKIMIND-OFFICE-HERMES.md exactly.

4. Commit ("init: office status feed") and push.

5. Confirm the file is live at:
   https://raw.githubusercontent.com/Muhabuki003/bukimind-status/main/status.json
```

---

## 🚦 Verify it works

1. Open `https://bukimind-office.pages.dev` on your phone
2. Trigger the one-time setup prompt → office should switch from "Connecting to Hermes feed…" to live data within ~5s
3. Enable the cron → watch agents update every cycle (idle agents that gain real work will walk to their desks)

---

## 🔮 Next integrations (expand the feed later)

- Wire `researcher` to real TikTok trend scraping → flip dropship bar live
- Wire `content` to TikTok/IG posting API → real post counts
- Add a "report to boss" event: when an agent finishes, include a `bubble` + an `events` entry → the office animates the walk-and-report automatically
- Eventually: Hermes writes per-client status for BookiStudio so each client build shows as its own activity

---

*Built by Am Muhabuki — BUKISTUDIO. Office design inspired by Pixel Agents (MIT). All sprites original.*
