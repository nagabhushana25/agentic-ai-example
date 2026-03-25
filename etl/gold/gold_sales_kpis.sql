create or replace view gold_sales_kpis as
select
    order_date,
    count(case when order_status = 'completed' then 1 end) as completed_orders,
    sum(case when order_status = 'completed' then gross_amount else 0 end) as gross_sales,
    sum(case when order_status = 'completed' then discount_amount else 0 end) as total_discounts,
    sum(case when order_status = 'completed' then return_amount else 0 end) as total_returns,
    sum(case when order_status = 'completed' then net_sales else 0 end) as net_sales,
    avg(case when order_status = 'completed' then net_sales end) as avg_order_value
from silver_orders
group by order_date;
