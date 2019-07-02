BEGIN;
select 1/count(*) from information_schema.tables where table_schema='file_router' and table_name='file_router_history';
ROLLBACK;
