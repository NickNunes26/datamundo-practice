# TechStore First Week Report

SQL analysis of a fictional Brazilian electronics retailer (**TechStore**), built around a first-week reporting scenario covering products, inventory, customers, orders, and sales targets.

This project started as an exercise from the DataMundo *SQL for Data Analysis* track and was refactored to run locally using DuckDB and pandas without external platform dependencies. All data is synthetic, and table/column names remain in Portuguese (`produtos`, `clientes`, `vendedores`, `pedidos`, `itens_pedido`) to match the original schema.

## Questions Covered

1. **Product catalog** — Full product list grouped by category and sorted by price.
2. **Low stock alert** — Products with fewer than 15 units remaining.
3. **Customer distribution** — Overview of the customer base ordered by state.
4. **Government accounts** — Customers in the `governo` segment.
5. **Top 10 orders** — Largest orders recorded by total value.
6. **Cancelled orders** — Cancelled orders sorted by value and payment method.
7. **Sales targets** — Sales reps with monthly targets above R$ 50,000.

## Dataset Overview

The database is loaded into an in-memory DuckDB instance from [`SQL/seed_techstore.sql`](SQL/seed_techstore.sql):

| Table | Rows | Description |
| ------- | ------ | ------------- |
| `produtos` | 23 | Product catalog, pricing, cost, and current stock |
| `clientes` | 47 | Customers across retail (`varejo`), corporate (`corporativo`), and government (`governo`) |
| `vendedores` | 7 | Sales team, region, hire date, and monthly target |
| `pedidos` | 165 | Orders from Dec 2023 to Mar 2024 (`entregue`, `em_transito`, `pendente`, `cancelado`) |
| `itens_pedido` | 182 | Line items linking orders to products |

## Key Findings

- **Inventory risk:** 3 products are below 15 units — `Monitor UltraWide 34"` (5), `Notebook Gamer Z5` (8), and `Workstation W3` (12). All three are high-ticket items (R$ 2,599 to R$ 7,899) and should be prioritized for restocking.
- **Cancellations:** 12 orders were cancelled, representing R$ 28,940.00 in lost revenue. Half of them (6 orders, R$ 15,280.00) used `cartao`, including the three largest cancellations (`#41`, `#136`, `#132`).
- **Pending high-value orders:** 2 of the top 10 orders (`#91` at R$ 8,799.00 and `#155` at R$ 6,480.00) are still `pendente` and worth following up before they turn into cancellations.
- **Regional concentration:** Most of the 47 customers sit in the Southeast (`SP`, `RJ`, `MG`), which also accounts for the only 2 sales reps with monthly targets above R$ 50,000 (`Ricardo Mendes` and `Carlos Eduardo`).
- **Government segment:** 7 public-sector accounts across 6 states (`AM`, `BA`, `MG`, `PE`, `RJ`, `SP`), separate from the 28 retail and 12 corporate accounts.

## Project Structure

```text
.
├── SQL/
│   └── seed_techstore.sql     # Schema and seed data
├── docs/                      # Charts and exported visuals (optional)
├── first_week_report.ipynb    # Main analysis notebook
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

## Next Steps

- Add `JOIN` and `GROUP BY` queries to compare actual delivered revenue against each rep's monthly target.
- Break down cancellation rate by payment method and month, and save a summary chart to `docs/`.
- Calculate gross margin per category using `preco` and `custo` from `produtos`.
