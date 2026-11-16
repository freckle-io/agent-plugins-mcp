# Ad audiences

- `adAudienceSyncs_createAdAudienceSync` pushes a Dataset to a LinkedIn, Meta or Google Ads audience every 24 hours, for free. Meta and Google only add people; LinkedIn replaces its list each run.
- A sync sends only rows with a usable email and finds none itself; never hash in code. Even when the Dataset has emails, first build an enrichment workflow whose email result is a hashed-email waterfall (two or more hashed-email providers, Aviato last) for every row, and sync that hashed result from its output Dataset, never the raw import. Warn when fewer than about 300 people will likely match.
- Enrich what the user asks for (such as work emails) in the workflow that feeds the sync, and sync that enriched result (or its hash), never the original email column; beyond that, an audience gets only match keys (hashed or personal email, plus phone for Meta), never provider or status columns. Outreach data goes in its own Dataset.
- Offer only authorized connections with an ad account; with none, send the `connections_setup` form and build nothing for the audience until it is connected.
- Map every field the platform accepts: email (required); first and last name and country for Meta and LinkedIn; phone, city and state for Meta; company name and title for LinkedIn. Settle the connection, audience name, schedule and mapping in one round, then create.
- To feed an audience from results that already exist, create a sync on the enrichment's output Dataset and turn the old sync off; do not rebuild the enrichment. A sync's Dataset cannot be changed.
- Relay sync status and match counts as reported. A company left out for most rows usually means an address is mapped as the company. Deleting a sync leaves the audience in the platform.
