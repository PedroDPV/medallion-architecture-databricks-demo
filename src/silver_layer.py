"""
Silver layer: cleaning, validation and standardization.

Reads from Bronze, applies data quality rules, deduplicates, and writes a
clean, conformed dataset used as the source of truth for downstream
aggregation (Gold layer).
"""
from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from src.bronze_layer import BRONZE_TABLE_PATH

SILVER_TABLE_PATH = "silver/orders"

_VALID_STATUSES = {"created", "paid", "shipped", "cancelled"}


def build_silver(spark: SparkSession, data_lake_root: str) -> DataFrame:
    """Transform Bronze orders into a clean Silver dataset.

    Applies the following data quality rules:
        - drops records with null or empty order_id or sku
        - drops records with non-positive quantity or unit_price
        - keeps only known, valid order statuses
        - deduplicates by order_id

    Args:
        spark: an active SparkSession.
        data_lake_root: root path of the local/demo data lake.

    Returns:
        The cleaned Silver DataFrame that was written to disk.
    """
    bronze_path = f"{data_lake_root}/{BRONZE_TABLE_PATH}"
    bronze_df = spark.read.format("delta").load(bronze_path)

    cleaned = (
        bronze_df.filter(F.col("order_id").isNotNull() & F.col("sku").isNotNull())
        .filter(F.col("quantity") > 0)
        .filter(F.col("unit_price") > 0)
        .filter(F.col("order_status").isin(list(_VALID_STATUSES)))
        .withColumn("created_at", F.to_timestamp("created_at"))
        .withColumn("total_amount", F.col("quantity") * F.col("unit_price"))
    )

    deduplicated = cleaned.dropDuplicates(["order_id"])

    output_path = f"{data_lake_root}/{SILVER_TABLE_PATH}"
    (
        deduplicated.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(output_path)
    )
    return deduplicated
