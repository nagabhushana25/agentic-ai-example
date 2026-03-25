create or replace view silver_orders as
select
    order_id,
    customer_id,
    product_id,
    cast(order_date as date) as order_date,
    cast(quantity as int) as quantity,
    cast(gross_amount as decimal(12,2)) as gross_amount,
    cast(discount_amount as decimal(12,2)) as discount_amount,
    cast(return_amount as decimal(12,2)) as return_amount,
    cast(gross_amount - discount_amount - return_amount as decimal(12,2)) as net_sales,
    lower(order_status) as order_status,
    lower(sales_channel) as sales_channel
from bronze_orders
where order_id is not null
  and customer_id is not null
  and product_id is not null;
