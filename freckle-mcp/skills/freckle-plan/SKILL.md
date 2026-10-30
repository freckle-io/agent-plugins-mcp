---
name: freckle-plan
description: "Plan a Freckle build: turn a sales call, transcript, meeting notes, a Slack thread or a loose idea into a build spec and plan before anything is built. Use it for \"build this\" or \"set this up\" asks, even when Freckle is not named."
---

# Plan a Freckle build

Turn the ask into a short plan before building anything. Write it even without the tools, turning each gap (such as which rows) into a question.

## Understand the ask
- Read what the plan needs, once: the ask and its files, the Workspace and credit balance, existing Workbooks, Workflows and rows, and the drafts of saved workflows you would reuse.
- Capture every agreed point: must-haves, matching and dedupe rules, schedules, and warnings mentioned in passing. Each must-have becomes a step the build meets exactly.
- Build only the current phase; later phases and undecided choices are questions. Every data point mentioned gets a column; when unsure, keep it and ask.
- ICP: keep the user's criteria in their words; a cheaper proxy is a question. A persona list mixing levels and functions means those levels in those functions. When people per company is unstated, ask and recommend 3.
- Creating CRM records always takes two steps: match (any one identifier, domain or URL or company name, counts) and re-check the CRM right before each create; create only on no match.

## Design for coverage
- Aim for the most rows ending with a correct value, and never drop or filter rows to finish faster. Misses stay honest misses.
- Recover missing identifiers first (a live domain, a LinkedIn URL) with their own waterfall, rejoin, then run later steps once for every row.
- For the top N people, search each seniority level separately and fill slots from the top down, each slot with its own columns.
- Reuse what exists: values the Dataset already has, saved workflows and waterfalls (connect them to the Dataset that holds their fields), and the user's Workbook. Treat given rows as real.

## Waterfalls
- Ordered providers, each running only when the one before missed. Keep the user's order; otherwise the most accurate for the objective, cheapest among equals.
- A value a provider already returned (Apollo's email) is the first rung. Validate every found email and phone inside the waterfall, so a bad value falls through to the next provider.
- Gate each rung on this objective's previous miss: wire a provider's `not_found` and `onFailure` straight to the next rung; gate a provider without cases (Apollo returning `[]`) with a `code` node's `config.cases`. Every paid step sits inside its gate.
- End every waterfall except contact info with its own Research Agent; a contact-info waterfall ends at its last structured provider and emits the miss.
- Rejoin branches at the first shared value with one collector `code` node, and decide what it emits when every provider misses.
- A gate on another workflow's result matches the exact values that workflow emits (`Tier 1`, not `1`) and its success status; anything else takes the skip path.

## Node choices
- Apollo Find People: `apolloFindPeopleBasic` (free) unless the deliverable needs fields only enriched search reveals.
- `decision` (free) for judgment calls on row data (tiers, categories, yes/no), with the user's full rules in the question; exact numeric cutoffs go to `code`.
- `researchAgent` looks things up and drafts text, but finds no emails or phones; give it a concrete question and the fields to fill.
- Push to Dataset needs its destination Dataset in the same Workbook.

## Approve
Present one message: the flow in plain words naming each reused workflow, the cost the server estimates against the balance, at most four questions each with a recommended answer, and one approval ask saying what approval starts. A reply that leaves choices to you approves your recommendations; a change request gets a revised plan and a new ask. Once approved, build with [BUILD.md](../freckle/BUILD.md) in the same turn, using only the providers the plan names.
