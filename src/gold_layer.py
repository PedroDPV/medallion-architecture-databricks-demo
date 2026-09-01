"""
Gold layer: business-level aggregates.

Builds analytics-ready tables on top of the Silver layer, such as revenue
per marketplace and per day, ready to be consumed by a BI tool.
"""
from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from src.silver_layer import SILVER_TABLE_PATH

GOLD_TABLE_PATH = "gold/revenue_by_marketplace_day"


def build_gold(spark: SparkSession, data_lake_root: str) -> DataFrame:
    """Aggregate Silver orders into a daily revenue-by-marketplace Gold table.

    Args:
        spark: an active SparkSession.
        data_lake_root: root path of the local/demo data lake.

    Returns:
        The aggregated Gold DataFrame that was written to disk.
    """
    silver_path = f"{data_lake_root}/{SILVER_TABLE_PATH}"
    silver_df = spark.read.format("delta").load(silver_path)

    gold_df = (
        silver_df.filter(F.col("order_status") != "cancelled")
        .withColumn("order_date", F.to_date("created_at"))
        .groupBy("marketplace", "order_date")
        .agg(
            F.sum("total_amount").alias("total_revenue"),
            F.count("order_id").alias("total_orders"),
        )
        .orderBy("order_date", "marketplace")
    )

    output_path = f"{data_lake_root}/{GOLD_TABLE_PATH}"
    (
        gold_df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(output_path)
    )
    return gold_df
