-- Revert switchboard schema from pg

BEGIN;

DROP SCHEMA switchboard CASCADE;

COMMIT;
