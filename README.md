# Ecommerce Database Engineering

Monorepo containing three subcontexts:

- `subcontext-a-modeling` — schema and DBML modeling files
- `subcontext-b-optimization` — performance reports and query tooling
- `subcontext-c-lakehouse` — lakehouse notebooks and data

To deploy this repo to GitHub (automated):

1. Ensure the `gh` CLI is installed and authenticated: `gh auth login`.
2. From the repository root run: `gh repo create ecommerce-database-engineering --public --source=. --remote=origin --push --confirm`.
