# TechStore First Week Report

SQL analysis of a fictional Brazilian electronics retailer (**TechStore**), built around a first-week reporting scenario covering products, inventory, customers, orders, sales targets, and category margins.

This project started as an exercise from the DataMundo *SQL for Data Analysis* track and was refactored to run locally using DuckDB, pandas, and matplotlib without external platform dependencies. All data is synthetic, and table/column names remain in Portuguese (`produtos`, `clientes`, `vendedores`, `pedidos`, `itens_pedido`) to match the original schema.

## Questions Covered

**Initial report (filtering & sorting)**
1. **Product catalog** — Full product list grouped by category and sorted by price.
2. **Low stock alert** — Products with fewer than 15 units remaining.
3. **Customer distribution** — Overview of the customer base ordered by state.
4. **Government accounts** — Customers in the `governo` segment.
5. **Top 10 orders** — Largest orders recorded by total value.
6. **Cancelled orders** — Cancelled orders sorted by value and payment method.
7. **Sales targets** — Sales reps with monthly targets above R$ 50,000.

**Deeper analysis (`JOIN`s & aggregations)**
8. **Delivered revenue by sales rep** — Total and monthly average delivered revenue vs. `meta_mensal`.
9. **Cancellation rate by payment method** — Order volume vs. lost revenue across `cartao`, `boleto`, and `pix`.
10. **Gross margin by category** — Average margin and retail inventory value per category.
11. **Zero-sale products** — Catalog items with no recorded line items in `itens_pedido`.

## Key Findings

- **Inventory risk:** 3 products are below 15 units — `Monitor UltraWide 34"` (5), `Notebook Gamer Z5` (8), and `Workstation W3` (12). All three are high-ticket items (R$ 2,599 to R$ 7,899) and should be prioritized for restocking.
- **Cancellations:** 12 orders were cancelled, totaling R$ 28,940.00. `cartao` accounts for the highest lost value (5 orders, R$ 18,476.00), while `boleto` has the highest cancellation rate at **16.7%** (4 of 24 orders) — roughly 3x the rate of `cartao` (5.9%) and `pix` (5.3%).
- **Pending high-value orders:** 2 of the top 10 orders (`#91` at R$ 8,799.00 and `#155` at R$ 6,480.00) are still `pendente` and worth following up before they expire or cancel.
- **Sales rep performance:** `Ricardo Mendes` (R$ 69,300.30), `Fernanda Lima` (R$ 61,382.60), and `Juliana Rocha` (R$ 59,480.00) lead total delivered revenue across the 4-month window. Monthly averages sit below 40% of `meta_mensal` for all 7 reps.
- **Margins & dead stock:** `Acessorios` has the highest average gross margin (56.4%) vs. `Notebooks` (34.6%). 5 catalog items have zero recorded sales, led by `Notebook Essencial E2` (R$ 112,495.50 in stock) and `Tablet Essencial 8"` (R$ 47,960.00).

### Visuals

![Delivered Revenue by Sales Rep](docs/revenue_by_rep.png)

![Cancellations by Payment Method](docs/cancellations_by_payment.png)

## Dataset Overview

The database is loaded into an in-memory DuckDB instance from [`SQL/seed_techstore.sql`](SQL/seed_techstore.sql):

| Table | Rows | Description |
|-------|------|-------------|
| `produtos` | 23 | Product catalog, pricing, cost, and current stock |
| `clientes` | 47 | Customers across retail (`varejo`), corporate (`corporativo`), and government (`governo`) |
| `vendedores` | 7 | Sales team, region, hire date, and monthly target |
| `pedidos` | 165 | Orders from Dec 2023 to Mar 2024 (`entregue`, `em_transito`, `pendente`, `cancelado`) |
| `itens_pedido` | 182 | Line items linking orders to products |

## Project Structure

```text
.
├── SQL/
│   └── seed_techstore.sql            # Schema and seed data
├── docs/
│   ├── revenue_by_rep.png            # Chart: delivered revenue by rep
│   └── cancellations_by_payment.png  # Chart: cancellation rate and value
├── first_week_report.ipynb           # Main analysis notebook
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook first_week_report.ipynb
```

Run all cells from top to bottom. The first cell loads `SQL/seed_techstore.sql` into an in-memory DuckDB database and defines a small `sql()` helper that returns pandas DataFrames.
