---
name: freckle
description: "How to work in Freckle through the Freckle MCP tools; read it before calling them. Use it when the user asks Freckle, or works with their Freckle Workbooks, Workflows, Datasets, Lists or Signals, to find companies or people, get work emails, phone numbers or company details, enrich or score leads or a CSV of accounts, import HubSpot or Salesforce records, push Datasets to LinkedIn, Meta or Google Ads audiences, run or change Workflows, monitor Signals for new hires, job openings or job changes, or check their Freckle account, credits and connections."
---

# Freckle through MCP

Freckle runs GTM data work: find companies and people, fill emails, phones and company facts through provider waterfalls, score and route rows, import CRM records, push ad audiences and watch Signals. Tool schemas and descriptions are authoritative for how to call things; this skill adds the GTM judgment they do not.

## Ground rules
- Call `workspace_context` first; all work happens in that Workspace. For another Workspace, pick it from `workspace_context` and call `workspace_select`; no new sign-in is needed.
- Find named targets by id or name, archived ones too, and ask when a name is ambiguous. A missing target is not permission to create a replacement.
- When a Workflow the user made or edited and a Freckle-managed (Library) one do the same job, use the user's; say which and why. Freckle-managed Workflows have a non-null `clonedFrom`.
- Do what was asked and stop there: preview, import, build, run and ongoing automation are different scopes.
- Confirm before spending credits: a plan with its cost, then a yes. That yes covers the run: show the sample; if the full run was already approved within the quoted max, continue; ask again only if the cost or scope changed, and before switching a connection to automatic.
- Building is free; build without asking. Over 100 rows, run a sample and show it before the full run, even when the user says to just run; at 100 or fewer, run without one unless the user asks.
- Report real outcomes: rows saved in the Workbook, the cost the server reports, failures and gaps as they are. A queued run is not a finished one.
- Delete or archive only the items the user names, each confirmed; never bulk-delete a Workspace's data. Deleting a Freckle account or Workspace is not available through these tools: say so and point the user to Freckle support.
- Secrets go only through the browser form `connections_setup` returns, never into chat, arguments or workflow JSON. A Dataset webhook URL is a credential: share it only with the requester.
- Talk to a GTM user: product words are fine; translate programming terms.

## Routes
- Anything to build (a call, notes, an idea): plan it with [freckle-plan](../freckle-plan/SKILL.md) first.
- Company or people lists and CRM imports: [LIST.md](LIST.md). People at companies already in a Dataset are a workflow step (Apollo people), not a list search.
- Build, run or change workflows: [BUILD.md](BUILD.md). Change a saved workflow in place rather than rebuilding it.
- Running a workflow on a schedule, keeping it fresh, "on a cron", "make it automatic", pausing one, or "when the first finishes run the second": the app's Scheduled Workflows, in [BUILD.md](BUILD.md). In your reply, call it a Scheduled Workflow ("I set up a Scheduled Workflow that…").
- Ad audiences: [ADS.md](ADS.md). Signals: [SIGNALS.md](SIGNALS.md).
- A node needs an integration the org lacks: name it and send the `connections_setup` form.

## Facts the tools do not show yet
- A run that waits in the queue for 24 hours while the Workspace has no credits is cancelled; a top-up does not revive it, so rerun those rows after topping up.
- Archived Workbooks and Datasets refuse imports and triggers; archiving a Workbook removes its Signals.
- Connections cannot be deleted and their mapping is fixed; a mapping change needs a new connection.
- A saved workflow's `id` (UUID) is what tools take; the draft's `workflowId` is only a slug.
