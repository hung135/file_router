--### Database
--requires op_dba.create_database wrapper function
SELECT op_dba.create_database(:V1,'development');

--uncomment for dev on local machines
--CREATE DATABASE switchboard;
--CREATE ROLE switchboard;

--### Extensions
--if the database uses any extensions they should be created here for production
--requires op_dba.create_extension wrapper function
--SELECT op_dba.create_extension('postgis','public');

--uncomment for dev on local machines
-- CREATE EXTENSION IF NOT EXISTS postgis;
