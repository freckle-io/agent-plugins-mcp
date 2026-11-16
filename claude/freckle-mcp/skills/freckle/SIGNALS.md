# Signal monitors

- `signals_listSignalTypes` gives types and per-finding cost. Settle the records, type, filters, destination and per-finding cost first; the input and output Datasets are distinct and in the same Workbook.
- Fill missing required inputs first, so the Signal watches every row (`contact_job_changes` needs a LinkedIn URL and a company domain on each row).
- A job-change Signal's first scan covers the whole Dataset and charges each change found; for company types, settle whether to include the last 24 hours.
- New monitors can take up to 3 hours to go live, and Freckle emails when they do; report the status `signals_getSignalProviderConfiguration` shows.
- Change only the Signal the user names.
