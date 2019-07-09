-- Deploy switchboard schema to pg

BEGIN;

CREATE SCHEMA stg AUTHORIZATION operational_dba;

COMMIT;
