BEGIN;
select 1/count(*) from information_schema.tables where table_schema='switchboard' and table_name='switchboard_history';
ROLLBACK;
