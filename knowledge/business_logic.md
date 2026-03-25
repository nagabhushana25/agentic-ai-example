# Business Logic Rules

This document defines the business logic used in reporting and analytics.

Customer rules:
- active customer means a customer with at least one completed purchase in the last 90 days
- inactive customer means no completed purchase in the last 90 days
- new customer means first purchase date is within the current calendar month

Sales rules:
- gross sales means total order value before discounts and returns
- net sales means gross sales minus discounts and returns
- completed order means order_status is completed
- cancelled orders must not be included in revenue reporting
- backlog-linked orders can be analyzed for delayed fulfillment risk but do not change revenue logic

Support rules:
- high priority ticket means severity is critical or impact is marked high
- resolved ticket means status is resolved or closed
- reopened ticket means a resolved ticket was reopened within 7 days
- SLA breach means resolution time exceeded target threshold of 240 minutes

ETL rules:
- records missing primary business keys must be rejected
- duplicate order records should be flagged and removed before loading curated tables
- any negative revenue value must be validated against returns or refund transactions
- backlog items without owning team must be marked for data quality review

Dashboard rules:
- executive dashboard uses only curated reporting tables
- KPI values must come from the latest successful ETL load
- stale data warning should appear if data refresh is older than expected SLA
