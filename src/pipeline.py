"""
Pipeline orchestration entry point.

Runs the full Bronze -> Silver -> Gold flow using synthetic data. This
script is meant to be executed locally (for example via
`python -m src.pipeline`) as a self-contained demo; it does not connect to
any real cloud account or production system.
"""
from __future__ import annotations

import logging

from pyspark.sql import SparkSession

from src.bronze_layer import load_bronze
from src.config import settings
from src.data_generator import generate_fake_orders
from src.gold_layer import build_gold
from src.silver_layer import build_silver

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


def get_spark_session() -> SparkSession:
    """Build a local SparkSession configured with the Delta Lake extensions."""
    return (
        SparkSession.builder.appName("medallion-architecture-demo")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .getOrCreate()
    )


def run_pipeline(num_orders: int = 500) -> None:
    """Run the full Bronze -> Silver -> Gold pipeline end to end."""
    logger.info("Starting medallion pipeline demo (environment=%s)", settings.environment)

    spark = get_spark_session()
    try:
        raw_orders = generate_fake_orders(num_orders=num_orders)
        logger.info("Generated %d synthetic order events", len(raw_orders))

        load_bronze(spark, raw_orders, settings.data_lake_root)
        logger.info("Bronze layer written to %s/bronze/orders", settings.data_lake_root)

        build_silver(spark, settings.data_lake_root)
        logger.info("Silver layer written to %s/silver/orders", settings.data_lake_root)

        gold_df = build_gold(spark, settings.data_lake_root)
        logger.info(
            "Gold layer written to %s/gold/revenue_by_marketplace_day",
            settings.data_lake_root,
        )
        gold_df.show(20, truncate=False)
    finally:
        spark.stop()


if __name__ == "__main__":
    run_pipeline()
