-- Deploy switchboard schema to pg

BEGIN;

CREATE SCHEMA switchboard authorization operational_dba;

COMMIT;
