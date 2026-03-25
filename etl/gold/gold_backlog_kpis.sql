create or replace view gold_backlog_kpis as
select
    team,
    count(*) as total_items,
    sum(case when status in ('todo', 'in_progress') then 1 else 0 end) as open_items,
    sum(case when status = 'done' then 1 else 0 end) as completed_items,
    sum(case when status in ('todo', 'in_progress') then story_points else 0 end) as open_story_points,
    sum(case when priority = 'critical' and status in ('todo', 'in_progress') then 1 else 0 end) as critical_open_items
from silver_backlog
group by team;
