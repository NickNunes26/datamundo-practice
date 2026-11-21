from pathlib import Path
import duckdb
import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def con():
    db = duckdb.connect()
    db.execute((ROOT / "SQL/seed_techstore.sql").read_text(encoding="utf-8"))
    db.execute((ROOT / "SQL/views_en.sql").read_text(encoding="utf-8"))
    yield db
    db.close()


@pytest.mark.parametrize(
    "raw_table,view_name",
    [
        ("produtos", "products"),
        ("clientes", "customers"),
        ("vendedores", "sales_reps"),
        ("pedidos", "orders"),
        ("itens_pedido", "order_items"),
    ],
)
def test_view_row_counts_match_raw_tables(con, raw_table, view_name):
    raw_count = con.execute(f"SELECT COUNT(*) FROM {raw_table}").fetchone()[0]
    view_count = con.execute(f"SELECT COUNT(*) FROM {view_name}").fetchone()[0]
    assert raw_count > 0
    assert view_count == raw_count


@pytest.mark.parametrize(
    "view_name,column,expected_values",
    [
        ("products", "category", {"Laptops", "Smartphones", "Monitors", "Tablets", "Accessories"}),
        ("customers", "segment", {"Retail", "Corporate", "Government"}),
        ("sales_reps", "region", {"Southeast", "South", "Northeast", "North", "Center-West"}),
        ("orders", "status", {"Delivered", "In Transit", "Pending", "Cancelled"}),
        ("orders", "payment_method", {"Card", "Bank Slip", "Instant Transfer"}),
    ],
)
def test_i18n_views_map_all_categorical_values(con, view_name, column, expected_values):
    actual = {
        row[0]
        for row in con.execute(f"SELECT DISTINCT {column} FROM {view_name}").fetchall()
    }
    assert actual <= expected_values, f"Unmapped values in {view_name}.{column}: {actual - expected_values}"
    assert len(actual) > 0


def test_referential_integrity(con):
    orphan_customers = con.execute(
        "SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON c.id = o.customer_id WHERE c.id IS NULL"
    ).fetchone()[0]
    orphan_reps = con.execute(
        "SELECT COUNT(*) FROM orders o LEFT JOIN sales_reps r ON r.id = o.sales_rep_id WHERE r.id IS NULL"
    ).fetchone()[0]
    orphan_orders = con.execute(
        "SELECT COUNT(*) FROM order_items oi LEFT JOIN orders o ON o.id = oi.order_id WHERE o.id IS NULL"
    ).fetchone()[0]
    orphan_products = con.execute(
        "SELECT COUNT(*) FROM order_items oi LEFT JOIN products p ON p.id = oi.product_id WHERE p.id IS NULL"
    ).fetchone()[0]

    assert orphan_customers == 0
    assert orphan_reps == 0
    assert orphan_orders == 0
    assert orphan_products == 0


def test_domain_value_bounds(con):
    invalid_products = con.execute(
        "SELECT COUNT(*) FROM products WHERE price <= 0 OR cost <= 0 OR price <= cost OR stock < 0"
    ).fetchone()[0]
    invalid_orders = con.execute(
        "SELECT COUNT(*) FROM orders WHERE total_amount <= 0 OR discount_pct < 0 OR discount_pct > 100"
    ).fetchone()[0]
    invalid_items = con.execute(
        "SELECT COUNT(*) FROM order_items WHERE quantity <= 0 OR unit_price <= 0"
    ).fetchone()[0]

    assert invalid_products == 0
    assert invalid_orders == 0
    assert invalid_items == 0
