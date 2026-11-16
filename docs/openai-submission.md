# OpenAI plugin directory submission

How `freckle-mcp/` is prepared for the OpenAI plugin directory (ChatGPT and Codex), what is still a placeholder, the steps only a Freckle owner can do, and an audit of the MCP tool annotations the review will check.

Rules followed: [Upload and submit your plugin](https://developers.openai.com/plugins/deploy/submission), [Package your plugin](https://developers.openai.com/plugins/build/plugins), [Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines), [Authentication](https://developers.openai.com/plugins/build/auth) and [Submission errors](https://developers.openai.com/plugins/deploy/submission-errors). Tool names and annotations were read from `freckle-io/next` at `origin/dev` `7ea53bcb7` (`apps/http_api/src/FullMcp`).

## Package

The package is the Codex format:

| File | Role |
| --- | --- |
| `freckle-mcp/.codex-plugin/plugin.json` | Identity, listing (`interface`), review cases and release notes (`extensions.com.openai`) |
| `freckle-mcp/.mcp.json` | The one remote MCP server, `https://next-api.freckle.io/mcp/full`, with OAuth (CIMD) |
| `freckle-mcp/skills/` | `freckle` (router plus LIST, BUILD, SIGNALS, ADS) and `freckle-plan` |
| `freckle-mcp/assets/` | `freckle-light.png` and `freckle-dark.png`, both 520×520 |
| `freckle-mcp/.claude-plugin/plugin.json` | Claude Code manifest; identity fields match the Codex manifest |

No hooks, `.app.json`, `apps`, server headers, secrets, `test_credentials` or `reviewer_instructions`.

Build the ZIP the portal takes (the plugin in one top-level folder, no sibling files):

```bash
Z=$(mktemp -d) && zip -q -r -X "$Z/freckle-mcp.zip" freckle-mcp -x '*.DS_Store' && unzip -l "$Z/freckle-mcp.zip"
```

Don't commit the ZIP. Bump `version` in both manifests for every new upload; the portal warns when a version is reused.

### MCP configuration

```json
"freckle": {
  "type": "http",
  "url": "https://next-api.freckle.io/mcp/full",
  "extensions": { "com.openai": { "auth": { "type": "oauth", "client": { "mode": "cimd" } } } }
}
```

- **`"type": "http"` stays.** The docs' Codex example omits `type` and the portable `mcp.json` uses `streamable-http`, but OpenAI's own Codex-format plugins (Figma, Notion, Linear in `openai/plugins`) use `"type": "http"`, and Claude Code reads the same file and needs it. Checked locally: Codex 0.166 installs the plugin and resolves the server as `streamable_http`; `claude mcp get` reads it as `http`; `claude plugin validate freckle-mcp` passes.
- **CIMD is right for this server.** `https://clerk.freckle.io/.well-known/oauth-authorization-server` advertises `client_id_metadata_document_supported: true`, no `registration_endpoint` (so DCR is not available), `S256` and `authorization_response_iss_parameter_supported: true`. ChatGPT should therefore use the stable redirect `https://chatgpt.com/connector_platform_oauth_redirect` and client document `https://chatgpt.com/oauth/client.json`; the portal's **MCPs** page shows the exact values.
- Clerk advertises the scopes `openid profile email public_metadata private_metadata offline_access user:org:read`. ChatGPT requests advertised OIDC scopes by default, so each must be enabled for the client.

## Review cases

All eight live in `extensions.com.openai.review.test_cases`. Every tool name was checked against the Full MCP catalog (132 tools: 119 generated as `<group>_<endpointId>` from the group contracts, minus `integrationCredentials_saveHttp`, plus 13 hand-written tools in `Server.ts`).

| # | Prompt (short) | Tools | Credits |
| --- | --- | --- | --- |
| P1 | Which Workspace, how many credits | `workspace_context`, `creditUsage_getCurrentCredits` | 0 |
| P2 | Preview VPs of Sales at US software companies, don't build | `listBuilds_getAIArkFilters`, `listBuilds_getFilterValues`, `listBuilds_previewAIArkPeople` (or Apollo `listBuilds_previewPeople`) | 0 (preview only estimates) |
| P3 | Workbook "Review Test" with 3 pasted domains, fill industry, size, HQ country | create Workbook and Dataset, `datasets_importDatasetCsv`, node lookup, `workflows_buildWorkflow`, then after a yes `datasets_triggerWorkflowDatasetConnection`, `workflowRuns_wait`, `datasets_listDatasetEntries` | A few, after a yes (for example, Apollo company enrichment is 1.04 per row) |
| P4 | Explain the "LinkedIn URL to Enriched Profile + Work Email" Workflow | `workflowNodes_listWorkflowNodes`, `workflows_getWorkflow`, `workflows_listWorkflowNodes` | 0 (explains only; the Workflow itself is up to 5.67 per row) |
| P5 | 25 US companies like gusto.com (50 to 1,000 employees), List "Review Lookalikes" | `listBuilds_getAIArkFilters`, `listBuilds_previewAIArkCompanies`, then after a yes `listBuilds_createAIArkCompanies`, `listBuilds_run`, `listBuilds_get`, `datasets_listDatasetEntries` | 0 for the preview; the quoted import cost for at most 25 companies, after a yes |
| N1 | Buy 5,000 credits and charge my card | None that change state | 0 |
| N2 | Delete my Freckle account and everything in it | None | 0 |
| N3 | Show Acme Corp's Workbooks | `workspace_context`; `workspace_select` answers 403 "You are not a member of that Workspace." | 0 |

Corrections to the 2026-11-09 draft:

- P3 now lists `workflowNodes_getWorkflowNodes` and `workflowDrafts_getDraftSyntax` (BUILD.md takes node details from one `getWorkflowNodes` call) and the run step `datasets_triggerWorkflowDatasetConnection`, which the draft left out between the build and `workflowRuns_wait`. It notes that Codex with file access uses `workflowDrafts_initDraft` and `workflows_createDraftUploadUrl` instead of `workflows_buildWorkflow`.
- P2 allows either provider: LIST.md says to recommend AI Ark or Apollo when the user names none, and Apollo's preview is `listBuilds_previewPeople`, not `previewApolloPeople`.
- P4 explains the managed `LinkedIn URL to Enriched Profile + Work Email` Workflow (`019faa02-4df6-76eb-82d1-5887fae00693`) instead of summarizing a seeded Workbook. Managed Workflows are visible in every Workspace, so the reviewer account needs no seeded data. Live definition: input `linkedin_url`; outputs `email`, `isValid`, `full_name`, `company_domain`, `emailSource`, `profile_source`, `zerobounceStatus`, `failureReason`; maximum 5.67 credits per row, 0 when nothing billable is found.
- P5 is a capped AI Ark lookalike List instead of a job-openings Signal: it is a one-off cost with nothing left running after the review, and it covers the preview, create and run path end to end.
- N2 asks to delete the account rather than "all my data": no tool deletes an account or Workspace, so that refusal is real. The `freckle` skill gained one ground rule to match: delete or archive only named items, each confirmed, never bulk-delete, and send account deletion to Freckle support. Cost confirmation, samples and secret handling are unchanged.

## Placeholders left

None.

Also worth a look: `interface.category` stays `Productivity`; `Business & Operations` may fit a GTM tool better. `brandColor` is `#6366f1`, and `publication.countries` is omitted, so no country restriction is applied.

## Steps only you can do

1. ~~**Support URL.**~~ Done: `interface.supportURL` is the Typeform support form and `author.email` is `support@freckle.io`.
2. **Reviewer account.** Create a Clerk user that signs in with email and password only: no MFA, no email or SMS code, no magic link, and no new-device verification. Give it:
   - One Workspace with about 200 credits, of which the 8 cases use fewer than 10.
   - No membership in any Workspace named Acme Corp (N3).
   - No integrations are needed.
   Run all 8 cases on it before submitting. Afterwards, archive "Review Test" and "Review Lookalikes" so a rerun starts clean.
3. ~~**Demo recording.**~~ Done: `review.demo_recording_url` is https://youtu.be/fZmI2_lisGw.
4. **Organization verification.** Complete business verification for Freckle at platform.openai.com → Settings → Organization → General, and make sure the submitter is an owner or has **Apps Management Write**.
5. **Upload the ZIP.** platform.openai.com/plugins → **Upload new or existing plugin** → choose the Freckle developer identity → upload. Fix any **Metadata & Skills** findings and wait for the skill scans (up to 2 hours).
6. **Domain verification.** In **MCPs → Connect**, copy the challenge token and serve it as plain text (the token only, no JSON) at `https://next-api.freckle.io/.well-known/openai-apps-challenge`, or at an allowed parent such as `https://freckle.io/.well-known/openai-apps-challenge`. That path currently returns 404 on `next-api`.
7. **Connect and scan.** Connect the server, sign in with OAuth, and read the scan findings. Expect the annotation gaps below to be flagged until `freckle-io/next` is fixed and redeployed, then **Rescan**.
8. **Review details and submit.** Enter the reviewer email and password, login URL and Workspace name in **Review information → Review details**. Check the imported cases, then **Submit for review** and complete the attestations.

### Risks to settle before submitting

- **Billing link.** `workspace_context` returns `plansAndBillingUrl` (`<app>/<org>/workbooks?settings=billing`), and its description tells the model to give it out when credits run low. The guidelines allow a link to an informational plans page but not to a page that starts a purchase or upgrade. If that settings view has buy or upgrade buttons, point the tool at the informational page `https://www.freckle.io/pricing` instead (a change in `freckle-io/next`). N1 already refers users to that page.
- **Annotation justifications.** The guidelines say they are no longer required, but the submission-errors page still lists `justification_required`. The **Why** column in the appendix can be pasted if the portal asks.
- **Two manifests in the ZIP.** The portal accepts `.codex-plugin/plugin.json` or `.claude-plugin/plugin.json`. The Codex one carries the listing and review fields. If the upload reports `claude_format_normalized`, the portal read the Claude manifest instead; remove `.claude-plugin/` from that ZIP and upload again.

## Annotation audit (report only; nothing in `freckle-io/next` was changed)

How the hints are emitted today:

- Effect's `McpServer` writes `readOnlyHint`, `destructiveHint`, `idempotentHint` and `openWorldHint` for every tool, falling back to its defaults: Readonly `false`, Destructive `true`, Idempotent `false`, OpenWorld `true` (`effect@4.1.2`, `src/ai/Tool.ts` and `src/ai/McpServer.ts`).
- `Catalog.withAccess(tool, 'read' | 'write')` sets only Readonly and Destructive. Generated tools are `read` when the endpoint is a GET or its guidance starts with "Validates only" (`compileWorkflowDraft`, `previewWorkflowNode`).
- Nothing in `FullMcp/` sets OpenWorld, Idempotent or Title, so every one of the 132 tools reports `openWorldHint: true`. A captured `tools/list` from the weekend eval run (`api-design/r5`) agrees.
- The older `/mcp` server already sets `Title`, `Idempotent(true)` and `OpenWorld(false)` on its reads (`apps/http_api/src/Mcp/Tools.ts`).

### Gap list

R/D/OW = `readOnlyHint` / `destructiveHint` / `openWorldHint`. 109 of 132 tools have at least one value to change; the other 23 are already right.

| Tools | Current R/D/OW | Should be | Why |
| --- | --- | --- | --- |
| `listBuilds_previewAIArkCompanies`, `listBuilds_previewAIArkPeople`, `listBuilds_previewCompanies`, `listBuilds_previewPeople` | F / T / T | **T / F** / T | Previews: nothing is created and no credits are spent (the services only estimate cost). Marked as writes, they make clients ask for a write confirmation on every preview. OpenWorld stays true for public provider data. |
| `salesforceDatasetSources_previewSoql` | F / T / T | **T / F / F** | Validates a query and previews up to 10 records from the user's own Salesforce. |
| `listBuilds_createAIArkCompanies`, `listBuilds_createAIArkPeople`, `listBuilds_createCompanies`, `listBuilds_createPeople` | F / T / T | F / **F** / T | Additive: they save a List and start no import until `listBuilds_run`. |
| `workbooks_createWorkbook`, `datasets_createWorkbookDataset`, `workflows_createWorkflow`, `workbooks_subscribeToWorkbookRunCompletion` | F / T / T | F / **F / F** | Additive writes inside the Workspace; nothing is removed or overwritten, and no credits are spent. |
| 59 read tools: every `creditUsage_*`, `workflowRuns_*` read, `workbooks_list/get*`, `datasets_list/get*`, `signals_list/get*`, `workflows_list/get*`, `workflowNodes_*`, `workflowDrafts_*`, `listBuilds_get*`, `salesforceDatasetSources_get/objects/fields/listViews`, `hubspotDatasetSources_get`, `adAudienceSyncs_list/get`, `integrationCredentials_list`, `workspace_context`, `connections_setup`, `workflowRuns_wait` | T / F / T | T / F / **F** | Bounded to the signed-in Workspace, the user's own connected accounts, or Freckle's fixed catalog. |
| 36 Workspace writes: archives, deletes, cancels, metadata and settings updates, CRM imports and schedules, `signals_pause/delete`, `adAudienceSyncs_update/delete`, `workspace_updateWorkspaceTimeZone`, `datasets_rotateDatasetWebhookSourceSecret` | F / T / T | F / T / **F** | Destructive is right; they act only on the Workspace or the user's own CRM and ad accounts. |
| `workspace_select` | F / F / T | F / F / **F** | Changes only this session's Workspace. |

Already right and worth keeping: every credit-spending or outbound tool is `F / T / T`. That covers `listBuilds_run`, `datasets_trigger…`, `datasets_rerunFailed…`, `datasets_runWorkflowDatasetConnectionEntries`, both connection policy updates, `datasets_createWorkflowDatasetConnection`, `workflowRuns_startWorkflowRun`, `workflows_buildWorkflow`, `workflows_createDraftUploadUrl`, `signals_create/reactivate/retry…`, `adAudienceSyncs_create/run…`, the row-adding Dataset tools (which start runs on an automatic connection), and `datasets_createDatasetWebhookSource`.

### Description gaps

The guidelines require descriptions that match behavior, with no hidden side effects.

1. **"May spend credits" on tools that spend nothing.** Every write without its own guidance gets `Changes state; may spend credits. Starts return IDs to poll; never retry an ambiguous start.` (59 tools). Most spend nothing:
   - **Workbooks and Workflows:** `workbooks_create/update/archive/unarchive/subscribe…/unsubscribe…`, `workflows_create/update/updateWorkflowSettings/archive/unarchive/saveWorkflowRevision`.
   - **Datasets:** `datasets_createWorkbookDataset/updateDataset/archiveDataset/deleteDataset/deleteDatasetEntries/replaceDatasetFieldCatalog/createDatasetWebhookSource/rotateDatasetWebhookSourceSecret/archiveWorkflowDatasetConnection`.
   - **Lists:** the four `listBuilds_create*` ("No import starts until you run the List").
   - **Runs:** the three `workflowRuns_cancel*`.
   - **Signals:** `signals_pause/delete…`.
   - **Ad audiences:** all four `adAudienceSyncs_*` writes (syncs are free, per ADS.md).
   - **CRM schedules:** `hubspotDatasetSources_deleteSchedule/pauseSchedule/setCheckpoint`, `salesforceDatasetSources_deleteSchedule`.
   - **Other:** `integrationCredentials_delete`, `workspace_updateWorkspaceTimeZone`.
   "Starts return IDs to poll" is also wrong for archives and deletes.
2. **Credit spend that isn't stated:**
   - `workflows_buildWorkflow` and `workflows_createDraftUploadUrl` never say that `sampleRows` runs rows that spend credits.
   - `datasets_updateWorkflowDatasetConnectionTriggerPolicy` doesn't say that switching to automatic runs pending rows.
   - `datasets_updateWorkflowDatasetConnectionRerunPolicy` doesn't say that scheduled reruns spend credits.
   - `datasets_importDatasetCsv`'s own guidance replaces the "Changes state" line entirely, and neither it nor `datasets_createCsvUploadUrl` / `datasets_waitForCsvImport` says that rows added to a Dataset with an automatic connection start runs.
   - `signals_createSignalProviderConfiguration` says only "may spend credits". It should say that it charges per finding until paused or deleted, and that a job-change Signal's first scan charges for every change found.
3. **Archive and delete effects.**
   - `workbooks_archiveWorkbook` ("Archive a Workbook.") hides that archiving removes the Workbook's Signals; the skill knows this, the tool does not say it.
   - `datasets_deleteDatasetEntries` and `integrationCredentials_delete` don't say the deletion is permanent, or, for the credential, that Workflows and syncs using it will fail.
4. **Truncated descriptions.** `firstSentence(…, 120)` keeps only the first sentence of each contract description, which drops side-effect sentences. The list previews lose "Nothing is created", and `datasets_archiveWorkflowDatasetConnection` loses "An archived connection refuses triggers and automatic runs".
5. **Spend isn't visible in the annotations.** Today every write is `destructiveHint: true`, so `workbooks_createWorkbook` looks the same as `listBuilds_run`. With the additive fixes above, `true` would mean "destructive or spends credits".
6. **Optional:** set `idempotentHint: true` on reads and a `title` on every tool, as `/mcp` already does.

Not gaps:

- `datasets_ingestDatasetWebhook` (the endpoint with its secret in the URL) is in the `datasetWebhooks` group, which isn't in `fullMcpGroups`, so the Full MCP server doesn't expose it.
- `integrationCredentials_saveHttp` is filtered out of the catalog, so secrets go only through `connections_setup`.
- The webhook-source create and rotate responses return a secret, which is their purpose; the skill treats that URL as a credential.

Suggested fix in `freckle-io/next` (not made here): replace `withAccess(read | write)` with a per-tool table `{ readOnly, destructive, openWorld }` that sets all three explicitly, treat `preview*` endpoints as reads, and write per-category guidance text instead of the one generic write line. Then deploy and **Rescan** in the portal.

### Every tool

Bold values change; "now" is what the server emits today. The **Why** column doubles as the annotation justification if the portal asks for one.

| Tool | readOnlyHint | destructiveHint | openWorldHint | Why |
| --- | --- | --- | --- | --- |
| `adAudienceSyncs_createAdAudienceSync` | false | true | true | Sends people data to an external ad platform; LinkedIn replaces its list on each run. |
| `adAudienceSyncs_deleteAdAudienceSync` | false | true | **false** (now true) | Changes or removes a sync in the Workspace; the platform audience is left in place. |
| `adAudienceSyncs_getAdAudienceSync` | true | false | **false** (now true) | Reads sync status, asking the user's own ad account while an upload is processing. |
| `adAudienceSyncs_listAdAudienceSyncs` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `adAudienceSyncs_runAdAudienceSync` | false | true | true | Sends people data to an external ad platform; LinkedIn replaces its list on each run. |
| `adAudienceSyncs_updateAdAudienceSync` | false | true | **false** (now true) | Changes or removes a sync in the Workspace; the platform audience is left in place. |
| `connections_setup` | true | false | **false** (now true) | Returns a browser form link; secrets are entered there, never through the tool. |
| `creditUsage_getCurrentCredits` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `creditUsage_getUsageByDay` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `creditUsage_getUsageByNodeInWorkbook` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `creditUsage_getUsageByNodeInWorkflow` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `creditUsage_getUsageByWorkbook` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `creditUsage_getUsageByWorkflow` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `datasets_archiveDataset` | false | true | **false** (now true) | Archives an item, so it refuses imports and triggers (an archived Workbook also loses its Signals). |
| `datasets_archiveWorkflowDatasetConnection` | false | true | **false** (now true) | Archives an item, so it refuses imports and triggers (an archived Workbook also loses its Signals). |
| `datasets_completeDatasetCsvImport` | false | true | true | Adds or changes rows; on a Dataset with an automatic connection this starts runs that spend credits. |
| `datasets_createCsvUploadUrl` | false | true | true | Adds or changes rows; on a Dataset with an automatic connection this starts runs that spend credits. |
| `datasets_createDatasetCsvImport` | false | true | true | Adds or changes rows; on a Dataset with an automatic connection this starts runs that spend credits. |
| `datasets_createDatasetEntry` | false | true | true | Adds or changes rows; on a Dataset with an automatic connection this starts runs that spend credits. |
| `datasets_createDatasetWebhookSource` | false | true | true | Creates a webhook endpoint that accepts records from any sender. |
| `datasets_createWorkbookDataset` | false | **false** (now true) | **false** (now true) | Creates a new item in the Workspace; removes or overwrites nothing and spends no credits. |
| `datasets_createWorkflowDatasetConnection` | false | true | true | Starts Workflow runs that spend credits and call data providers or user-chosen HTTP hosts; a spend cannot be undone. |
| `datasets_deleteDataset` | false | true | **false** (now true) | Deletes data or stops future work; cannot be undone. |
| `datasets_deleteDatasetEntries` | false | true | **false** (now true) | Deletes data or stops future work; cannot be undone. |
| `datasets_getDataset` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `datasets_getDatasetEntryCount` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `datasets_getDatasetEntryGridWindow` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `datasets_getDatasetSource` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `datasets_getWorkflowDatasetConnection` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `datasets_importDatasetCsv` | false | true | true | Adds or changes rows; on a Dataset with an automatic connection this starts runs that spend credits. |
| `datasets_listDatasetEntries` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `datasets_listDatasetSources` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `datasets_listDatasets` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `datasets_listWorkbookDatasets` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `datasets_listWorkflowDatasetConnectionRuns` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `datasets_replaceDatasetFieldCatalog` | false | true | **false** (now true) | Overwrites settings or metadata in the Workspace. |
| `datasets_rerunFailedWorkflowDatasetConnection` | false | true | true | Starts Workflow runs that spend credits and call data providers or user-chosen HTTP hosts; a spend cannot be undone. |
| `datasets_rotateDatasetWebhookSourceSecret` | false | true | **false** (now true) | Revokes the old webhook secret. |
| `datasets_runWorkflowDatasetConnectionEntries` | false | true | true | Starts Workflow runs that spend credits and call data providers or user-chosen HTTP hosts; a spend cannot be undone. |
| `datasets_triggerWorkflowDatasetConnection` | false | true | true | Starts Workflow runs that spend credits and call data providers or user-chosen HTTP hosts; a spend cannot be undone. |
| `datasets_updateDataset` | false | true | **false** (now true) | Overwrites settings or metadata in the Workspace. |
| `datasets_updateDatasetEntry` | false | true | true | Adds or changes rows; on a Dataset with an automatic connection this starts runs that spend credits. |
| `datasets_updateWorkflowDatasetConnectionRerunPolicy` | false | true | true | Starts Workflow runs that spend credits and call data providers or user-chosen HTTP hosts; a spend cannot be undone. |
| `datasets_updateWorkflowDatasetConnectionTriggerPolicy` | false | true | true | Starts Workflow runs that spend credits and call data providers or user-chosen HTTP hosts; a spend cannot be undone. |
| `datasets_waitForCsvImport` | false | true | true | Adds or changes rows; on a Dataset with an automatic connection this starts runs that spend credits. |
| `hubspotDatasetSources_create` | false | true | **false** (now true) | Imports from the user's own connected CRM into a Dataset; mirrored imports can remove rows. |
| `hubspotDatasetSources_deleteSchedule` | false | true | **false** (now true) | Deletes data or stops future work; cannot be undone. |
| `hubspotDatasetSources_fetchNextBatch` | false | true | **false** (now true) | Imports from the user's own connected CRM into a Dataset; mirrored imports can remove rows. |
| `hubspotDatasetSources_get` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `hubspotDatasetSources_pauseSchedule` | false | true | **false** (now true) | Deletes data or stops future work; cannot be undone. |
| `hubspotDatasetSources_resumeSchedule` | false | true | **false** (now true) | Imports from the user's own connected CRM into a Dataset; mirrored imports can remove rows. |
| `hubspotDatasetSources_setCheckpoint` | false | true | **false** (now true) | Imports from the user's own connected CRM into a Dataset; mirrored imports can remove rows. |
| `hubspotDatasetSources_setSchedule` | false | true | **false** (now true) | Imports from the user's own connected CRM into a Dataset; mirrored imports can remove rows. |
| `integrationCredentials_delete` | false | true | **false** (now true) | Deletes data or stops future work; cannot be undone. |
| `integrationCredentials_list` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `listBuilds_createAIArkCompanies` | false | **false** (now true) | true | Saves a List over public provider data; no import starts and no credits are spent until listBuilds_run. |
| `listBuilds_createAIArkPeople` | false | **false** (now true) | true | Saves a List over public provider data; no import starts and no credits are spent until listBuilds_run. |
| `listBuilds_createCompanies` | false | **false** (now true) | true | Saves a List over public provider data; no import starts and no credits are spent until listBuilds_run. |
| `listBuilds_createPeople` | false | **false** (now true) | true | Saves a List over public provider data; no import starts and no credits are spent until listBuilds_run. |
| `listBuilds_get` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `listBuilds_getAIArkFilters` | true | false | **false** (now true) | Returns fixed reference text or the node catalog; changes nothing. |
| `listBuilds_getFilterValues` | true | false | **false** (now true) | Returns fixed reference text or the node catalog; changes nothing. |
| `listBuilds_previewAIArkCompanies` | **true** (now false) | **false** (now true) | true | Previews a provider search over public company or people data; creates nothing and spends no credits (cost is only estimated). |
| `listBuilds_previewAIArkPeople` | **true** (now false) | **false** (now true) | true | Previews a provider search over public company or people data; creates nothing and spends no credits (cost is only estimated). |
| `listBuilds_previewCompanies` | **true** (now false) | **false** (now true) | true | Previews a provider search over public company or people data; creates nothing and spends no credits (cost is only estimated). |
| `listBuilds_previewPeople` | **true** (now false) | **false** (now true) | true | Previews a provider search over public company or people data; creates nothing and spends no credits (cost is only estimated). |
| `listBuilds_run` | false | true | true | Imports records from a public provider search; spends credits, which cannot be undone. |
| `salesforceDatasetSources_create` | false | true | **false** (now true) | Imports from the user's own connected CRM into a Dataset; mirrored imports can remove rows. |
| `salesforceDatasetSources_deleteSchedule` | false | true | **false** (now true) | Deletes data or stops future work; cannot be undone. |
| `salesforceDatasetSources_fetchNextBatch` | false | true | **false** (now true) | Imports from the user's own connected CRM into a Dataset; mirrored imports can remove rows. |
| `salesforceDatasetSources_fields` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `salesforceDatasetSources_get` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `salesforceDatasetSources_listViews` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `salesforceDatasetSources_objects` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `salesforceDatasetSources_previewSoql` | **true** (now false) | **false** (now true) | **false** (now true) | Previews up to 10 records from the user's own Salesforce; creates nothing. |
| `salesforceDatasetSources_setSchedule` | false | true | **false** (now true) | Imports from the user's own connected CRM into a Dataset; mirrored imports can remove rows. |
| `signals_createSignalProviderConfiguration` | false | true | true | Starts or resumes monitors of public company and people activity that charge credits per finding. |
| `signals_deleteSignalProviderConfiguration` | false | true | **false** (now true) | Deletes data or stops future work; cannot be undone. |
| `signals_getSignalProviderConfiguration` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `signals_listActiveSignalProviderConfigurations` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `signals_listSignalProviderConfigurationMonitorStatuses` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `signals_listSignalProviderConfigurations` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `signals_listSignalTypes` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `signals_pauseSignalProviderConfiguration` | false | true | **false** (now true) | Deletes data or stops future work; cannot be undone. |
| `signals_reactivateSignalProviderConfiguration` | false | true | true | Starts or resumes monitors of public company and people activity that charge credits per finding. |
| `signals_retrySignalProviderConfiguration` | false | true | true | Starts or resumes monitors of public company and people activity that charge credits per finding. |
| `workbooks_archiveWorkbook` | false | true | **false** (now true) | Archives an item, so it refuses imports and triggers (an archived Workbook also loses its Signals). |
| `workbooks_createWorkbook` | false | **false** (now true) | **false** (now true) | Creates a new item in the Workspace; removes or overwrites nothing and spends no credits. |
| `workbooks_getWorkbook` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workbooks_getWorkbookStats` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workbooks_listWorkbooks` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workbooks_subscribeToWorkbookRunCompletion` | false | **false** (now true) | **false** (now true) | Adds an email notification for the calling user; nothing else changes. |
| `workbooks_unarchiveWorkbook` | false | true | **false** (now true) | Restores an archived item, which can resume its automation. |
| `workbooks_unsubscribeFromWorkbookRunCompletion` | false | true | **false** (now true) | Deletes data or stops future work; cannot be undone. |
| `workbooks_updateWorkbook` | false | true | **false** (now true) | Overwrites settings or metadata in the Workspace. |
| `workflowDrafts_compileWorkflowDraft` | true | false | **false** (now true) | Compiles or checks a draft; saves and runs nothing. |
| `workflowDrafts_getDraftSyntax` | true | false | **false** (now true) | Returns fixed reference text or the node catalog; changes nothing. |
| `workflowDrafts_initDraft` | true | false | **false** (now true) | Returns fixed reference text or the node catalog; changes nothing. |
| `workflowNodes_getWorkflowNode` | true | false | **false** (now true) | Returns fixed reference text or the node catalog; changes nothing. |
| `workflowNodes_getWorkflowNodes` | true | false | **false** (now true) | Returns fixed reference text or the node catalog; changes nothing. |
| `workflowNodes_listWorkflowNodes` | true | false | **false** (now true) | Returns fixed reference text or the node catalog; changes nothing. |
| `workflowNodes_previewWorkflowNode` | true | false | **false** (now true) | Compiles or checks a draft; saves and runs nothing. |
| `workflowRuns_cancelAllWorkbookRuns` | false | true | **false** (now true) | Cancels queued work. |
| `workflowRuns_cancelAllWorkflowRuns` | false | true | **false** (now true) | Cancels queued work. |
| `workflowRuns_cancelWorkflowRuns` | false | true | **false** (now true) | Cancels queued work. |
| `workflowRuns_getWorkflowRunData` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflowRuns_getWorkflowRunStats` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflowRuns_getWorkflowRunView` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflowRuns_listWorkflowNodeRuns` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflowRuns_listWorkflowRunData` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflowRuns_listWorkflowRuns` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflowRuns_searchWorkflowRuns` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflowRuns_startWorkflowRun` | false | true | true | Starts Workflow runs that spend credits and call data providers or user-chosen HTTP hosts; a spend cannot be undone. |
| `workflowRuns_wait` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflows_archiveWorkflow` | false | true | **false** (now true) | Archives an item, so it refuses imports and triggers (an archived Workbook also loses its Signals). |
| `workflows_buildWorkflow` | false | true | true | Compiles, saves and connects a Workflow revision; with sampleRows it also runs rows that spend credits. |
| `workflows_createDraftUploadUrl` | false | true | true | Compiles, saves and connects a Workflow revision; with sampleRows it also runs rows that spend credits. |
| `workflows_createWorkflow` | false | **false** (now true) | **false** (now true) | Creates a new item in the Workspace; removes or overwrites nothing and spends no credits. |
| `workflows_getLatestWorkflowSchema` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflows_getWorkflow` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflows_getWorkflowRevision` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflows_getWorkflowRevisionSchema` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflows_listWorkflowNodes` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflows_listWorkflowRevisions` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflows_listWorkflows` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workflows_saveWorkflowRevision` | false | true | **false** (now true) | Saves a new latest revision, which changes what the Workflow's connections run. |
| `workflows_unarchiveWorkflow` | false | true | **false** (now true) | Restores an archived item, which can resume its automation. |
| `workflows_updateWorkflow` | false | true | **false** (now true) | Overwrites settings or metadata in the Workspace. |
| `workflows_updateWorkflowSettings` | false | true | **false** (now true) | Overwrites settings or metadata in the Workspace. |
| `workspace_context` | true | false | **false** (now true) | Reads data in the signed-in Workspace; changes nothing. |
| `workspace_select` | false | false | **false** (now true) | Changes only this MCP session's Workspace; no Workspace data changes. |
| `workspace_updateWorkspaceTimeZone` | false | true | **false** (now true) | Changes when every cron Rerun Policy in the Workspace fires. |
