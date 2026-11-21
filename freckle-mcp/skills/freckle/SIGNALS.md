# Signal monitors

- For a native Signal, `signals_listSignalTypes` gives supported types and per-finding cost. Settle the records, type, filters, destination and per-finding cost first; the input and output Datasets are distinct and in the same Workbook.
- Fill missing required inputs first, so the Signal watches every row (`contact_job_changes` needs a LinkedIn URL and a company domain on each row).
- A job-change Signal's first scan covers the whole Dataset and charges each change found; for company types, settle whether to include the last 24 hours.
- New monitors can take up to 3 hours to go live, and Freckle emails when they do; report the status `signals_getSignalProviderConfiguration` shows.
- Change only the Signal the user names.

## Approved funding webhook alternative

When the user allows a funding webhook and account-membership gate, a missing funding type or price in the Signal catalog does not block that construction. Use the webhook route without inventing a hidden Signal type or requiring a Signal per-finding price; inspect and disclose the downstream enrichment nodes' own costs separately. Build-only approval permits saving the receiver and graph, not spending enrichment credits.

- Create a dedicated event Dataset in the target Workbook with `datasets_createWorkbookDataset`, then `datasets_createDatasetWebhookSource` with an event-id `keyPath` when available. Catalog the company-domain and funding-event fields with `datasets_replaceDatasetFieldCatalog` so the Workflow connection can map them.
- Inspect the gate and company-enrichment nodes through [BUILD.md](BUILD.md). Gate every enrichment path on exact membership in the approved account domains; an outsider or missing domain reaches no enrichment. An allowlist copied from the account Dataset is a snapshot: say so rather than claiming live membership updates. Supplied fixture domains remain valid strings for a saved gate; live matching is unverified.
- Save the Workflow, bind the domain and funding-event inputs, and bind funding findings, membership result and enrichment to the output Dataset. Use `datasets_createWorkflowDatasetConnection` with the approved automatic webhook trigger, preserving any no-run instruction: do not send test events or trigger enrichment.
- Report the saved receiver, gate and output separately from upstream delivery. A generic receiver does not register TAMradar or verify incoming funding events; state that upstream registration and delivery are unverified unless tool evidence establishes them. Keep its credential-bearing webhook URL private under the shared secret rules.
