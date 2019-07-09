-- Revert switchboard schema from pg

BEGIN;

DROP SCHEMA stg CASCADE;

COMMIT;
