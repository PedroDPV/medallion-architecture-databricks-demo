"""
Bronze layer: raw ingestion.

Writes the synthetic source events as-is (append-only) into the Bronze
Delta table, preserving the original shape of the data for auditability.
"""
from __future__ import annotations

from typing import Any, Dict, List

from pyspark.sql import DataFrame, SparkSession

BRONZE_TABLE_PATH = "bronze/orders"


def load_bronze(
    spark: SparkSession,
    raw_records: List[Dict[str, Any]],
    data_lake_root: str,
) -> DataFrame:
    """Persist raw records into the Bronze Delta table.

    Args:
        spark: an active SparkSession.
        raw_records: synthetic raw order events.
        data_lake_root: root path of the local/demo data lake.

    Returns:
        The DataFrame that was written to the Bronze layer.
    """
    if not raw_records:
        raise ValueError("raw_records must not be empty")

    df = spark.createDataFrame(raw_records)
    output_path = f"{data_lake_root}/{BRONZE_TABLE_PATH}"

    (
        df.write.format("delta")
        .mode("append")
        .option("mergeSchema", "true")
        .save(output_path)
    )
    return df
