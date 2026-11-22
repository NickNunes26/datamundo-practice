# DataMundo Practice

[![Data Quality Tests](https://github.com/NickNunes26/datamundo-practice/actions/workflows/ci.yml/badge.svg)](https://github.com/NickNunes26/datamundo-practice/actions/workflows/ci.yml)

Repository of hands-on SQL and data analysis projects developed during the DataMundo track, organized by module.

## Structure

### Modulo 1

| # | Project | Description | Status |
|---|---------|-------------|--------|
| 1 | [TechStore First Week Report](Modulo%201/projeto-relatorio-da-primeira-semana-1/README.md) | SQL reporting & analysis (filtering, JOINs, CTEs, window functions) with DuckDB, pandas, matplotlib, and pytest data quality checks | Completed |
| 2 | [Sales Team Performance Dashboard](Modulo%201/projeto-dashboard-de-performance-da-equipe-2/README.md) | Executive sales team dashboard (ranking, category mix, customer concentration, cancellation alerts, regional champions, Q1 trends) with DuckDB, matplotlib, and pytest | Completed |

## Running Tests

From the repository root:

```bash
pytest -v
```

GitHub Actions automatically runs the test suite on pushes and pull requests to `main`.
