"""Unit tests for the synthetic data generator."""
from src.data_generator import generate_fake_orders

_REQUIRED_FIELDS = {
    "order_id",
    "marketplace",
    "sku",
    "product_name",
    "unit_price",
    "quantity",
    "order_status",
    "created_at",
}


def test_generate_fake_orders_count():
    orders = generate_fake_orders(num_orders=10, seed=1)
    assert len(orders) == 10


def test_generate_fake_orders_fields():
    orders = generate_fake_orders(num_orders=5, seed=1)
    for order in orders:
        assert _REQUIRED_FIELDS.issubset(order.keys())
        assert order["quantity"] >= 1
        assert order["unit_price"] > 0


def test_generate_fake_orders_reproducible():
    orders_a = generate_fake_orders(num_orders=20, seed=7)
    orders_b = generate_fake_orders(num_orders=20, seed=7)
    assert orders_a == orders_b


def test_generate_fake_orders_zero():
    orders = generate_fake_orders(num_orders=0, seed=1)
    assert orders == []
