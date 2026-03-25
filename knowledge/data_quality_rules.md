# Data Quality Rules

Data quality checks are required before analytics datasets are published.

Rules:
- customer_id must not be null
- order_id must be unique in curated sales tables
- ticket_id must be unique in support ticket tables
- backlog_id must be unique in backlog tables
- order_date must be a valid date
- net_sales must not exceed gross_sales
- resolved tickets must have resolution timestamp
- stale ETL loads must be flagged
- backlog items must have valid team and priority values

Data quality issue examples:
- duplicate orders
- missing customer references
- incorrect revenue signs
- invalid ticket statuses
- delayed refresh causing outdated dashboards
- backlog records with missing owner team
