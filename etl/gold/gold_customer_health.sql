create or replace view gold_customer_health as
select
    c.customer_id,
    c.customer_name,
    c.region,
    max(o.order_date) as last_order_date,
    count(case when o.order_status = 'completed' then 1 end) as completed_order_count,
    sum(case when o.order_status = 'completed' then o.net_sales else 0 end) as lifetime_net_sales,
    case
        when max(o.order_date) >= current_date - interval '90' day then 'active'
        else 'inactive'
    end as customer_health_status
from silver_customers c
left join silver_orders o
    on c.customer_id = o.customer_id
group by c.customer_id, c.customer_name, c.region;
