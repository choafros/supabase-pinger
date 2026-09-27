# Supabase Keeper

This repository periodically sends lightweight REST queries to Supabase Free Tier projects so otherwise-idle development projects still receive external database activity. The checks run in GitHub Actions, so they do not depend on a laptop being awake.

## How it works

```text
GitHub Actions
    ↓
Every 6 hours
    ↓
Supabase REST API
    ↓
SELECT one column LIMIT 1
```

One scheduled workflow reads a JSON array from a GitHub repository secret and checks every configured project. It continues after individual failures, then reports a failed workflow if any project did not return a successful HTTP response.

## GitHub setup

After creating a GitHub repository and pushing this project, open:

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

Create a repository secret named `SUPABASE_PROJECTS`. Its value should be a JSON array:

```json
[
  {
    "name": "bn-club",
    "url": "https://YOUR_PROJECT_REF.supabase.co",
    "key": "YOUR_PUBLISHABLE_OR_ANON_KEY",
    "table": "profiles",
    "column": "id"
  },
  {
    "name": "freightzilla",
    "url": "https://ANOTHER_PROJECT_REF.supabase.co",
    "key": "ANOTHER_PUBLISHABLE_OR_ANON_KEY",
    "table": "profiles",
    "column": "id"
  }
]
```

Use a Supabase publishable or anon key that RLS permits to read the selected column. Do not commit the JSON containing real keys. The `column` property is optional and defaults to `id`.

A safe single-project template is also available in `supabase-projects.example.json`.

## Manual test

After the workflow is on GitHub, run it from:

```text
GitHub
→ Actions
→ Keep Supabase Projects Alive
→ Run workflow
```

Successful output looks like:

```text
✓ bn-club: OK (200)
✓ freightzilla: OK (200)

All Supabase projects responded successfully.
```

The workflow checks every project even if an earlier one fails, and exits non-zero after the checks if there were any failures.

## Adding another project

Edit the `SUPABASE_PROJECTS` repository secret and append another object to its JSON array. No workflow change or additional workflow file is required.

## Schedule

The workflow uses `17 */6 * * *`, which runs approximately four times per day in UTC, at minute 17 every six hours. GitHub Actions schedules can be delayed during periods of high load.

## Legacy local keeper

`pinger.py`, `requirements.txt`, and `setup.sh` are the legacy local keeper and remain as a fallback. Do not remove them until the first GitHub Actions run completes successfully. After that successful run, these three files—and the old local cron entry, if no longer wanted—can be removed.
