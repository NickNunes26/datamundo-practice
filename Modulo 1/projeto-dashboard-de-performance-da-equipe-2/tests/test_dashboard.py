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
    raw_count = con.execute(f"SELECT COUNT(*) FROM {raw_table}").fetchall()[0][0]
    view_count = con.execute(f"SELECT COUNT(*) FROM {view_name}").fetchall()[0][0]
    assert raw_count > 0
    assert view_count == raw_count


def test_all_sales_reps_appear_in_ranking(con):
    rows = con.execute(
        """
        SELECT
            RANK() OVER (ORDER BY COALESCE(SUM(o.total_amount), 0) DESC) AS rank,
            r.name AS sales_rep,
            COALESCE(SUM(o.total_amount), 0) AS revenue
        FROM sales_reps r
        LEFT JOIN orders o
            ON o.sales_rep_id = r.id
            AND o.status = 'Delivered'
        GROUP BY r.id, r.name
        ORDER BY revenue DESC
        """
    ).fetchall()
    assert len(rows) == 7
    assert rows[0][1] == "Ricardo Mendes"
    revenues = [row[2] for row in rows]
    assert revenues == sorted(revenues, reverse=True)


def test_top3_products_per_region_capped_at_three(con):
    rows = con.execute(
        """
        WITH ranked AS (
            SELECT
                r.region,
                p.name AS product,
                SUM(oi.quantity * oi.unit_price) AS revenue,
                ROW_NUMBER() OVER (
                    PARTITION BY r.region
                    ORDER BY SUM(oi.quantity * oi.unit_price) DESC
                ) AS rn
            FROM order_items oi
            JOIN orders o ON o.id = oi.order_id
            JOIN products p ON p.id = oi.product_id
            JOIN sales_reps r ON r.id = o.sales_rep_id
            WHERE o.status = 'Delivered'
            GROUP BY r.region, p.id, p.name
        )
        SELECT region, COUNT(*) AS product_count
        FROM ranked
        WHERE rn <= 3
        GROUP BY region
        """
    ).fetchall()
    assert len(rows) == 5
    assert all(count <= 3 for _, count in rows)


def test_cancellation_red_zone_alert(con):
    rows = con.execute(
        """
        SELECT
            r.name AS sales_rep,
            ROUND(
                100.0 * SUM(CASE WHEN o.status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(o.id),
                1
            ) AS cancellation_rate_pct
        FROM sales_reps r
        JOIN orders o ON o.sales_rep_id = r.id
        GROUP BY r.id, r.name
        HAVING ROUND(
            100.0 * SUM(CASE WHEN o.status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(o.id),
            1
        ) > 10
        """
    ).fetchall()
    assert {row[0] for row in rows} == {"Bruno Alves", "Carlos Eduardo"}


def test_below_80_pct_target_alert(con):
    rows = con.execute(
        """
        SELECT
            r.name AS sales_rep,
            ROUND(100.0 * COALESCE(SUM(o.total_amount), 0) / r.monthly_target, 1) AS pct_of_target
        FROM sales_reps r
        LEFT JOIN orders o
            ON o.sales_rep_id = r.id
            AND o.status = 'Delivered'
        GROUP BY r.id, r.name, r.monthly_target
        HAVING ROUND(100.0 * COALESCE(SUM(o.total_amount), 0) / r.monthly_target, 1) < 80
        """
    ).fetchall()
    assert {row[0] for row in rows} == {"Bruno Alves", "Amanda Torres"}
