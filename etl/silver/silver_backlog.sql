create or replace view silver_backlog as
select
    backlog_id,
    lower(team) as team,
    lower(item_type) as item_type,
    lower(priority) as priority,
    lower(status) as status,
    cast(created_date as date) as created_date,
    cast(completed_date as date) as completed_date,
    cast(story_points as int) as story_points
from bronze_backlog_items
where backlog_id is not null;
