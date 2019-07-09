--### Database
--requires op_dba.create_database wrapper function
SELECT op_dba.create_database(:V1,'development');

--uncomment for dev on local machines
--CREATE DATABASE file_router;
--CREATE ROLE file_router;

--### Extensions
--if the database uses any extensions they should be created here for production
--requires op_dba.create_extension wrapper function
--SELECT op_dba.create_extension('postgis','public');

--uncomment for dev on local machines
-- CREATE EXTENSION IF NOT EXISTS postgis;
