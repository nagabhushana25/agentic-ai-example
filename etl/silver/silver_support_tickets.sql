create or replace view silver_support_tickets as
select
    ticket_id,
    customer_id,
    cast(created_at as timestamp) as created_at,
    cast(resolved_at as timestamp) as resolved_at,
    lower(priority) as priority,
    lower(category) as category,
    lower(status) as status,
    cast(first_response_minutes as int) as first_response_minutes,
    cast(resolution_minutes as int) as resolution_minutes,
    lower(channel) as channel,
    case
        when resolution_minutes is not null and resolution_minutes <= 240 then 1
        else 0
    end as sla_met
from bronze_support_tickets
where ticket_id is not null
  and customer_id is not null;
