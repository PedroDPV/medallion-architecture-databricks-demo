# Security Notes

This repository is a portfolio and demo project built entirely with synthetic, fake data. It does not connect to any real production system, and it is not meant to be deployed as is.

Practices demonstrated here that also apply to my professional work:

No credentials, tokens, or connection strings are hardcoded anywhere in the codebase. All configuration is loaded from environment variables, see .env.example, via src/config.py.

Local .env files are excluded from version control via .gitignore. Only .env.example, which contains no real values, is committed.

Data quality and validation checks are applied before promoting data between layers, see src/silver_layer.py.

Dependencies are pinned in requirements.txt to keep builds reproducible and auditable.

No personal, customer, or employer data is used or reproduced anywhere in this repository.

If you find a security concern in this demo repository, feel free to open an issue.
