create or replace view silver_customers as
select
    customer_id,
    customer_name,
    region,
    cast(signup_date as date) as signup_date,
    lower(status) as status
from bronze_customers
where customer_id is not null;
