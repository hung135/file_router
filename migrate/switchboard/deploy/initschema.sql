-- Deploy switchboard schema to pg

BEGIN;

CREATE SCHEMA switchboard AUTHORIZATION operational_dba;

COMMIT;
