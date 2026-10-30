# Lists and CRM imports

## Company and people lists
- Apollo or AI Ark: preview, then create and `listBuilds_run`. When the user names no provider, explain the difference that matters and recommend one.
- Keep the import cap, preview size, qualified-result target and filter values separate. Pass the cap as `resultLimit` on every preview, with the filters the import will use.
- A preview authorizes nothing. Show the candidates, the scope searched, the estimated cost and which criteria stay unverified; provider matches are not verified customers.
- For new people, drop anyone already in the CRM or Dataset before counting; ask what "new" means when unclear. Pick the cheapest mode with the fields the deliverable needs.
- On continuation keep criteria, exclusions and destination, and exclude already delivered entities by a stable id, not by name.
- After an import, read every row and report the count saved; flag any mismatch with the import's own count.

## CRM imports
- `hubspotDatasetSources_create` or `salesforceDatasetSources_create`. In the first question round, unless the ask settles them, ask both: a list, all records or a filter; and, as its own question, whether a list should be mirrored (members who leave the list leave the Dataset) or only add and update, recommending mirror when the Dataset should match the list.
- Downstream work waits for the import to complete; report a failed or partial import and ask before processing it.
