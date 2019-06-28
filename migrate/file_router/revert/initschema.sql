-- Revert file_router schema from pg

BEGIN;

DROP SCHEMA file_router CASCADE;

COMMIT;
