-- Revert file_router schema from pg

BEGIN;

DROP SCHEMA stg CASCADE;

COMMIT;
