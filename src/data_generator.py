"""
Synthetic data generator.

Generates fully fake e-commerce order data used only to demonstrate the
medallion architecture pipeline. No real customer, order, or company data
is used anywhere in this project.
"""
from __future__ import annotations

import random
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List

_FAKE_PRODUCTS = [
    ("SKU-1001", "Wireless Mouse", 29.90),
    ("SKU-1002", "Mechanical Keyboard", 149.90),
    ("SKU-1003", "USB-C Hub", 79.50),
    ("SKU-1004", "Noise Cancelling Headphones", 399.00),
    ("SKU-1005", "27-inch Monitor", 899.00),
]

_FAKE_MARKETPLACES = ["marketplace_a", "marketplace_b", "marketplace_c"]

_VALID_STATUSES = ["created", "paid", "shipped", "cancelled"]


def generate_fake_orders(num_orders: int = 500, seed: int = 42) -> List[Dict[str, Any]]:
    """Generate a list of fake, randomized order records.

    Args:
        num_orders: number of synthetic orders to generate.
        seed: random seed for reproducibility.

    Returns:
        A list of dictionaries representing raw (Bronze-layer) order events.
    """
    rng = random.Random(seed)
    orders: List[Dict[str, Any]] = []
    base_time = datetime(2026, 1, 1)

    for _ in range(num_orders):
        sku, name, price = rng.choice(_FAKE_PRODUCTS)
        quantity = rng.randint(1, 5)
        order = {
            "order_id": str(uuid.uuid4()),
            "marketplace": rng.choice(_FAKE_MARKETPLACES),
            "sku": sku,
            "product_name": name,
            "unit_price": price,
            "quantity": quantity,
            "order_status": rng.choice(_VALID_STATUSES),
            "created_at": (base_time + timedelta(minutes=rng.randint(0, 60 * 24 * 90))).isoformat(),
        }
        orders.append(order)

    return orders
