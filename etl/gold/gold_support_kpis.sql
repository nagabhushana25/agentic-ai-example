create or replace view gold_support_kpis as
select
    cast(created_at as date) as ticket_date,
    count(*) as total_tickets,
    sum(case when status in ('resolved', 'closed') then 1 else 0 end) as resolved_tickets,
    sum(case when priority in ('high', 'critical') then 1 else 0 end) as high_priority_tickets,
    avg(first_response_minutes) as avg_first_response_minutes,
    avg(resolution_minutes) as avg_resolution_minutes,
    avg(sla_met) * 100 as sla_compliance_pct
from silver_support_tickets
group by cast(created_at as date);
