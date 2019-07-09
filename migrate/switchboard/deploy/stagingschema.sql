-- Deploy switchboard schema to pg

BEGIN;

CREATE SCHEMA stg authorization operational_dba;

COMMIT;
