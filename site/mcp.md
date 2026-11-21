# Freckle MCP server

Use Freckle from Claude, Codex, Cursor, VS Code or any other AI agent that
speaks the Model Context Protocol. Build company and people lists, enrich and
score leads, author and run Workflows, import CRM records, watch Signals and
sync Ads audiences, all in plain language.

- **Server URL:** `https://next-api.freckle.io/mcp/full`
- **Transport:** Streamable HTTP
- **Auth:** OAuth. You sign in to Freckle in the browser and pick a Workspace.
- **Who can use it:** any member of a Freckle Workspace.

## Set up

### Claude Code

The plugin connects the server and adds Freckle's skills in one step:

```
/plugin marketplace add freckle-io/agent-plugins-mcp
/plugin install freckle@freckle-mcp-plugins
```

Then run `/mcp`, pick **freckle** and sign in. Server only, without the skills:

```bash
claude mcp add --transport http freckle https://next-api.freckle.io/mcp/full
```

### Claude (claude.ai and Claude Desktop)

1. Go to **Settings → Connectors → Add custom connector**.
2. Name it `Freckle`, paste `https://next-api.freckle.io/mcp/full`, then
   **Connect** and sign in to Freckle.
3. Optional: add the skills. Download
   [`freckle.zip`](https://github.com/freckle-io/agent-plugins-mcp/releases/download/skills-latest/freckle.zip)
   and [`freckle-plan.zip`](https://github.com/freckle-io/agent-plugins-mcp/releases/download/skills-latest/freckle-plan.zip)
   and upload each under **Settings → Capabilities → Skills**.

### Codex

```bash
codex plugin marketplace add freckle-io/agent-plugins-mcp
```

Run `/plugins`, install **Freckle** and sign in. Server only:

```bash
codex mcp add freckle --url https://next-api.freckle.io/mcp/full
```

### Cursor

[Add to Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=freckle&config=eyJ1cmwiOiJodHRwczovL25leHQtYXBpLmZyZWNrbGUuaW8vbWNwL2Z1bGwifQ==),
or add this to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "freckle": { "url": "https://next-api.freckle.io/mcp/full" }
  }
}
```

### VS Code

[Install in VS Code](https://vscode.dev/redirect/mcp/install?name=freckle&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A//next-api.freckle.io/mcp/full%22%7D),
or add this to `.vscode/mcp.json`:

```json
{
  "servers": {
    "freckle": { "type": "http", "url": "https://next-api.freckle.io/mcp/full" }
  }
}
```

### Other clients

Any client that supports remote (Streamable HTTP) MCP servers with OAuth can
connect to `https://next-api.freckle.io/mcp/full`. For clients that only run
local servers, bridge it with `npx -y mcp-remote https://next-api.freckle.io/mcp/full`.

## What you can ask

- "Which Workspace am I in and how many credits do I have?"
- "Preview VPs of Sales at US software companies with 50 to 500 employees. Don't build anything yet."
- "Make a Workbook from these 20 domains and fill in industry, headcount and HQ country."
- "Find work emails for everyone in my *Webinar attendees* Dataset. Run 10 rows first and show me."
- "Import my HubSpot contacts in the *Customers* list every morning and enrich new ones."
- "Watch these accounts for hiring and funding Signals."
- "Sync the *High intent* Dataset to a LinkedIn matched audience."

## Credits and safety

- **Approval before spend.** The server tells your agent to quote the maximum
  cost and get your yes before anything spends credits, to run a sample first
  when a job is over 100 rows, and to get your approval on a plan before it
  creates, imports, connects or builds anything.
- **Labelled tools.** Every tool carries MCP annotations (read-only,
  destructive, idempotent, open-world) so your client can auto-approve reads
  and ask before writes. The reference below shows which tools can spend credits.
- **Secrets stay out of chat.** API keys for integrations are entered in a
  Freckle browser form that `connections_setup` links to, never in tool arguments.
- **One Workspace per session.** The session uses the Workspace you picked at
  sign-in. Ask your agent to switch, and it changes only that session.

## Data and privacy

Freckle sees only what your agent sends to the tools and returns only data from
your Workspace and the providers your Workflows call. Customer data is never
used to train AI models. Freckle is SOC 2 Type II audited.
`snapshot_createUpload` shares the current session transcript with the Freckle
team for debugging or feedback. Its description tells agents to call it only
when you ask, and it works only in clients with a local shell (Claude Code, Codex).

See the [privacy policy](https://freckle.io/privacy-policy) and
[terms of service](https://freckle.io/terms-of-service). Data requests:
privacy@freckle.io. Security: security@freckle.io.

## Tools

<!-- tools:start -->
143 tools, generated from the server's tool annotations.

### Workspace and connections

| Tool | What it does | Effect |
| --- | --- | --- |
| `integrationCredentials_list` | List Connections | Read only |
| `integrationCredentials_delete` | Delete Connection | Free write |
| `connections_setup` | Set Up Connection | Read only |
| `workspace_context` | Get Workspace Context | Read only |
| `workspace_select` | Switch Workspace | Free write |
| `workspace_updateWorkspaceTimeZone` | Set Workspace Time Zone | Free write |
| `snapshot_createUpload` | Share Session Transcript With Freckle | Free write |

### Credits

| Tool | What it does | Effect |
| --- | --- | --- |
| `creditUsage_getCurrentCredits` | Get Credit Balance | Read only |
| `creditUsage_getUsageByDay` | Get Credit Usage by Day | Read only |
| `creditUsage_getUsageByWorkbook` | Get Credit Usage by Workbook | Read only |
| `creditUsage_getUsageByWorkflow` | Get Credit Usage by Workflow | Read only |
| `creditUsage_getUsageByNodeInWorkbook` | Get Workbook Credit Usage by Node | Read only |
| `creditUsage_getUsageByNodeInWorkflow` | Get Workflow Credit Usage by Node | Read only |

### Workbooks

| Tool | What it does | Effect |
| --- | --- | --- |
| `workbooks_createWorkbook` | Create Workbook | Free write |
| `workbooks_listWorkbooks` | List Workbooks | Read only |
| `workbooks_getWorkbook` | Get Workbook | Read only |
| `workbooks_getWorkbookStats` | Get Workbook Stats | Read only |
| `workbooks_subscribeToWorkbookRunCompletion` | Email When Workbook Runs Finish | Free write |
| `workbooks_unsubscribeFromWorkbookRunCompletion` | Cancel Workbook Run Email | Free write |
| `workbooks_updateWorkbook` | Update Workbook | Free write |
| `workbooks_archiveWorkbook` | Archive Workbook | Free write |
| `workbooks_unarchiveWorkbook` | Unarchive Workbook | May spend credits |

### Datasets

| Tool | What it does | Effect |
| --- | --- | --- |
| `datasets_createWorkbookDataset` | Create Dataset | Free write |
| `datasets_listWorkbookDatasets` | List Workbook Datasets | Read only |
| `datasets_listDatasets` | List Datasets | Read only |
| `datasets_getDataset` | Get Dataset | Read only |
| `datasets_updateDataset` | Update Dataset | Free write |
| `datasets_archiveDataset` | Archive Dataset | Free write |
| `datasets_deleteDataset` | Delete Dataset | Free write |
| `datasets_createDatasetEntry` | Add Dataset Entry | May spend credits |
| `datasets_importDatasetCsv` | Import CSV Rows | May spend credits |
| `datasets_createDatasetCsvImport` | Create CSV Import | Enables later spend |
| `datasets_completeDatasetCsvImport` | Queue CSV Import | May spend credits |
| `datasets_createDatasetWebhookSource` | Create Webhook Source | Enables later spend |
| `datasets_rotateDatasetWebhookSourceSecret` | Rotate Webhook Secret | Free write |
| `datasets_getDatasetSource` | Get Dataset Source | Read only |
| `datasets_listDatasetSources` | List Dataset Sources | Read only |
| `datasets_listDatasetEntries` | List Dataset Entries | Read only |
| `datasets_getDatasetEntryGridWindow` | Get Dataset Grid Rows | Read only |
| `datasets_getDatasetEntryCount` | Count Dataset Entries | Read only |
| `datasets_updateDatasetEntry` | Update Dataset Entry | May spend credits |
| `datasets_deleteDatasetEntries` | Delete Dataset Entries | Free write |
| `datasets_replaceDatasetFieldCatalog` | Replace Dataset Fields | Free write |
| `datasets_createWorkflowDatasetConnection` | Connect Workflow to Dataset | Enables later spend |
| `datasets_getWorkflowDatasetConnection` | Get Connection | Read only |
| `datasets_triggerWorkflowDatasetConnection` | Run Pending Entries | May spend credits |
| `datasets_rerunFailedWorkflowDatasetConnection` | Rerun Failed Entries | May spend credits |
| `datasets_runWorkflowDatasetConnectionEntries` | Run Selected Entries | May spend credits |
| `datasets_updateWorkflowDatasetConnectionTriggerPolicy` | Set Connection Trigger Policy | Enables later spend |
| `datasets_updateWorkflowDatasetConnectionRerunPolicy` | Set Connection Rerun Policy | Enables later spend |
| `datasets_archiveWorkflowDatasetConnection` | Archive Connection | Free write |
| `datasets_listWorkflowDatasetConnectionRuns` | List Connection Runs | Read only |
| `datasets_createCsvUploadUrl` | Create CSV Upload URL | Enables later spend |
| `datasets_waitForCsvImport` | Import Uploaded CSV and Wait | May spend credits |
| `datasets_addCatalogFields` | Add Dataset Fields | Free write |

### List building

| Tool | What it does | Effect |
| --- | --- | --- |
| `listBuilds_createAIArkCompanies` | Create AI Ark Company List | May spend credits |
| `listBuilds_createAIArkPeople` | Create AI Ark People List | May spend credits |
| `listBuilds_createCompanies` | Create Apollo Company List | May spend credits |
| `listBuilds_createPeople` | Create Apollo People List | May spend credits |
| `listBuilds_run` | Run List Import | May spend credits |
| `listBuilds_get` | Get List Progress | Read only |
| `listBuilds_getFilterValues` | List Filter Values | Read only |
| `listBuilds_getAIArkFilters` | Get AI Ark Filter Fields | Read only |

### Workflows and enrichment

| Tool | What it does | Effect |
| --- | --- | --- |
| `workflowDrafts_compileWorkflowDraft` | Validate Workflow Draft | Read only |
| `workflowDrafts_getDraftSyntax` | Get Draft Syntax | Read only |
| `workflowDrafts_initDraft` | Start Workflow Draft | Read only |
| `workflowNodes_listWorkflowNodes` | List Workflow Nodes | Read only |
| `workflowNodes_getWorkflowNode` | Get Workflow Node | Read only |
| `workflowNodes_getWorkflowNodes` | Get Workflow Nodes | Read only |
| `workflowNodes_previewWorkflowNode` | Preview Workflow Node | Read only |
| `workflows_createWorkflow` | Create Workflow | Free write |
| `workflows_listWorkflows` | List Workflows | Read only |
| `workflows_listWorkflowNodes` | List Nodes in Workflow | Read only |
| `workflows_archiveWorkflow` | Archive Workflow | Free write |
| `workflows_unarchiveWorkflow` | Unarchive Workflow | Enables later spend |
| `workflows_getWorkflow` | Get Workflow | Read only |
| `workflows_updateWorkflow` | Update Workflow | Free write |
| `workflows_updateWorkflowSettings` | Update Workflow Settings | Enables later spend |
| `workflows_saveWorkflowRevision` | Save Workflow Revision | Enables later spend |
| `workflows_listWorkflowRevisions` | List Workflow Revisions | Read only |
| `workflows_getWorkflowRevision` | Get Workflow Revision | Read only |
| `workflows_getPinnedWorkflowRevision` | Get Pinned Workflow Revision | Read only |
| `workflows_getLatestWorkflowSchema` | Get Workflow Schema | Read only |
| `workflows_getWorkflowRevisionSchema` | Get Revision Schema | Read only |
| `workflows_listAcrossWorkspaces` | List Workflows in All Workspaces | Read only |
| `workflows_buildWorkflow` | Build Workflow | May spend credits |
| `workflows_createDraftUploadUrl` | Create Draft Upload URL | May spend credits |

### Workflow runs

| Tool | What it does | Effect |
| --- | --- | --- |
| `workflowRuns_listWorkflowRuns` | List Workflow Runs | Read only |
| `workflowRuns_listWorkflowRunData` | List Workflow Run Data | Read only |
| `workflowRuns_getWorkflowRunStats` | Get Workflow Run Stats | Read only |
| `workflowRuns_searchWorkflowRuns` | Search Workflow Runs | Read only |
| `workflowRuns_startWorkflowRun` | Start Workflow Run | May spend credits |
| `workflowRuns_getWorkflowRunData` | Get Workflow Run Data | Read only |
| `workflowRuns_listWorkflowNodeRuns` | List Node Runs | Read only |
| `workflowRuns_getWorkflowRunView` | Get Workflow Run | Read only |
| `workflowRuns_getWorkflowRunParent` | Get Parent Workflow Run | Read only |
| `workflowRuns_cancelWorkflowRuns` | Cancel Workflow Runs | Free write |
| `workflowRuns_cancelAllWorkflowRuns` | Cancel All Workflow Runs | Free write |
| `workflowRuns_cancelAllWorkbookRuns` | Cancel All Workbook Runs | Free write |
| `workflowRuns_wait` | Wait for Runs | Read only |

### CRM and warehouse imports

| Tool | What it does | Effect |
| --- | --- | --- |
| `hubspotDatasetSources_create` | Import from HubSpot | Starts work, free |
| `hubspotDatasetSources_setSchedule` | Set HubSpot Import Schedule | Enables later spend |
| `hubspotDatasetSources_deleteSchedule` | Delete HubSpot Import Schedule | Free write |
| `hubspotDatasetSources_pauseSchedule` | Pause HubSpot Import Schedule | Free write |
| `hubspotDatasetSources_resumeSchedule` | Resume HubSpot Import Schedule | May spend credits |
| `hubspotDatasetSources_setCheckpoint` | Set HubSpot Import Checkpoint | Enables later spend |
| `hubspotDatasetSources_get` | Get HubSpot Source | Read only |
| `hubspotDatasetSources_fetchNextBatch` | Import Next HubSpot Batch | May spend credits |
| `salesforceDatasetSources_previewSoql` | Preview Salesforce SOQL | Read only |
| `salesforceDatasetSources_create` | Import from Salesforce | Starts work, free |
| `salesforceDatasetSources_get` | Get Salesforce Source | Read only |
| `salesforceDatasetSources_fetchNextBatch` | Import Next Salesforce Batch | May spend credits |
| `salesforceDatasetSources_setSchedule` | Set Salesforce Import Schedule | Enables later spend |
| `salesforceDatasetSources_deleteSchedule` | Delete Salesforce Import Schedule | Free write |
| `salesforceDatasetSources_objects` | List Salesforce Objects | Read only |
| `salesforceDatasetSources_fields` | List Salesforce Fields | Read only |
| `salesforceDatasetSources_listViews` | List Salesforce List Views | Read only |
| `attioDatasetSources_create` | Import from Attio | Starts work, free |
| `attioDatasetSources_get` | Get Attio Source | Read only |
| `attioDatasetSources_sync` | Sync Attio Source | May spend credits |
| `attioDatasetSources_setSchedule` | Set Attio Import Schedule | Enables later spend |
| `attioDatasetSources_deleteSchedule` | Delete Attio Import Schedule | Free write |
| `attioDatasetSources_objects` | List Attio Objects | Read only |
| `attioDatasetSources_attributes` | List Attio Attributes | Read only |
| `snowflakeDatasetSources_previewQuery` | Preview Snowflake Query | Read only |
| `snowflakeDatasetSources_createImport` | Import from Snowflake | May spend credits |

### Signals

| Tool | What it does | Effect |
| --- | --- | --- |
| `signals_listSignalTypes` | List Signal Types | Read only |
| `signals_createSignalProviderConfiguration` | Create Signal | May spend credits |
| `signals_listSignalProviderConfigurationMonitorStatuses` | List Signal Monitor Statuses | Read only |
| `signals_listSignalProviderConfigurations` | List Dataset Signals | Read only |
| `signals_listActiveSignalProviderConfigurations` | List Active Signals | Read only |
| `signals_getSignalProviderConfiguration` | Get Signal | Read only |
| `signals_pauseSignalProviderConfiguration` | Pause Signal | Free write |
| `signals_reactivateSignalProviderConfiguration` | Reactivate Signal | May spend credits |
| `signals_retrySignalProviderConfiguration` | Retry Signal Monitors | May spend credits |
| `signals_deleteSignalProviderConfiguration` | Delete Signal | Free write |
| `signals_listByWorkbook` | List Workbook Signals | Read only |

### Ads audiences

| Tool | What it does | Effect |
| --- | --- | --- |
| `adAudienceSyncs_createAdAudienceSync` | Create Ad Audience Sync | Starts work, free |
| `adAudienceSyncs_listAdAudienceSyncs` | List Ad Audience Syncs | Read only |
| `adAudienceSyncs_getAdAudienceSync` | Get Ad Audience Sync | Read only |
| `adAudienceSyncs_updateAdAudienceSync` | Update Ad Audience Sync | Free write |
| `adAudienceSyncs_runAdAudienceSync` | Run Ad Audience Sync | Starts work, free |
| `adAudienceSyncs_deleteAdAudienceSync` | Delete Ad Audience Sync | Free write |
<!-- tools:end -->

## Troubleshooting

**Sign-in loops or the server shows as disconnected.** Remove the connection
and add it again, or run `/mcp` in Claude Code and pick **Re-authenticate**.

**My agent is in the wrong Workspace.** Ask it to "switch Freckle Workspace";
it lists the Workspaces you belong to and switches this session.

**Tools are missing.** Check that the URL ends in `/mcp/full`. Some clients cap
the number of tools; turn off tool groups you don't need.

**A run spent more than I expected.** Ask your agent for "my Freckle credit
usage today" to see it itemised in chat, or check usage in the Freckle app.

## Support

Email support@freckle.io or open an issue at
[freckle-io/agent-plugins-mcp](https://github.com/freckle-io/agent-plugins-mcp/issues).
