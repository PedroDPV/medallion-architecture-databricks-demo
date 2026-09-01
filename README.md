# Medallion Architecture Demo, Bronze, Silver, Gold

This is a portfolio and demo project that implements a Bronze to Silver to Gold, medallion, lakehouse pipeline using PySpark and Delta Lake, inspired by patterns I use professionally with Databricks.

Disclaimer: all data used in this project is synthetically generated, see src/data_generator.py. No real company, customer, or production data is used anywhere in this repository. This is a simplified sample meant to illustrate architecture and coding practices, not a production system.

## Architecture

Bronze layer: raw synthetic order events are ingested as is and appended to a Delta table, preserving full history for auditability.

Silver layer: Bronze data is cleaned, validated for schema, null checks, and valid status values, deduplicated, and enriched with a computed total_amount column.

Gold layer: Silver data is aggregated into a business-ready table with daily revenue and order counts per marketplace, ready to be consumed by a BI tool.

## Project structure

`src/config.py`: environment based configuration with no hardcoded secrets.

`src/data_generator.py`: synthetic order data generator.

`src/bronze_layer.py`: Bronze ingestion logic.

`src/silver_layer.py`: Silver cleaning and validation logic.

`src/gold_layer.py`: Gold aggregation logic.

`src/pipeline.py`: orchestrates the full Bronze to Silver to Gold run.

tests: unit tests for the synthetic data generator.

`SECURITY.md`: security practices applied in this demo.

## Running locally

Create a virtual environment and install dependencies from requirements.txt.

Copy .env.example to .env and adjust values if needed.

Run the pipeline with: python -m src.pipeline

## Tech stack

Python, PySpark, Delta Lake, pytest, python-dotenv.

## About this repository

This project is part of my professional portfolio and demonstrates the kind of medallion architecture, data quality, and cost-aware pipeline design work described in my LinkedIn profile and resume. It is a self-contained sample built specifically for this purpose using synthetic data, not an export of proprietary employer code.
