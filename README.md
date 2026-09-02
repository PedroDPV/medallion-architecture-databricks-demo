# Medallion Architecture on Databricks (Bronze, Silver, Gold)

This is a portfolio and demo project that reproduces, using synthetic data, a Bronze to Silver to Gold medallion lakehouse pipeline that I designed and implemented end to end natively inside Databricks, using Databricks notebooks, Jobs, and Delta Lake tables governed by Unity Catalog. This repository packages the same layered logic as a standalone PySpark and Delta Lake application so the code and design can be reviewed outside of a Databricks workspace.

**Disclaimer:** all data used in this project is synthetically generated, see `src/data_generator.py`. No real company, customer, or production data is used anywhere in this repository. This is a simplified sample meant to illustrate architecture and coding practices, not a production system.

## Architecture

In production, this pipeline runs entirely within Databricks: notebooks and Jobs orchestrate every layer, and each table is registered and governed through Unity Catalog. The layers are:

- **Bronze layer:** raw synthetic order events are ingested as-is and appended to a Delta table, preserving full history for auditability.
- **Silver layer:** Bronze data is cleaned, validated for schema, null checks, and valid status values, deduplicated, and enriched with a computed `total_amount` column.
- **Gold layer:** Silver data is aggregated into a business-ready table with daily revenue and order counts per marketplace, ready to be consumed by a BI tool.

## Project structure

- `src/config.py`: environment based configuration with no hardcoded secrets.
- `src/data_generator.py`: synthetic order data generator.
- `src/bronze_layer.py`: Bronze ingestion logic.
- `src/silver_layer.py`: Silver cleaning and validation logic.
- `src/gold_layer.py`: Gold aggregation logic.
- `src/pipeline.py`: orchestrates the full Bronze to Silver to Gold run.
- `tests`: unit tests for the synthetic data generator.
- `SECURITY.md`: security practices applied in this demo.

## Running locally

This standalone version reproduces the same layered logic outside of Databricks, for review purposes.

1. Create a virtual environment and install dependencies from `requirements.txt`.
2. Copy `.env.example` to `.env` and adjust values if needed.
3. Run the pipeline with `python -m src.pipeline`.

## Tech stack

Professionally, this architecture is built and orchestrated entirely within Databricks: notebooks, Jobs, Delta Lake, and Unity Catalog. In this standalone reproduction: Python, PySpark, Delta Lake, pytest, python-dotenv.

## About this repository

This project is part of my professional portfolio and demonstrates the medallion architecture that I designed and built entirely within Databricks, described in my LinkedIn profile and resume. It is a self-contained sample built specifically for this purpose using synthetic data, not an export of proprietary employer code.
