
--requires op_dba.create_role wrapper function
SELECT op_dba.create_role ('switchboard_readonly');
SELECT op_dba.create_role ('switchboard_readwrite');

--uncomment for dev on local machines
--CREATE ROLE switchboard_readonly;
--CREATE ROLE switchboard_readwrite;

--Permission Granting shall be replaced by warden
GRANT :V1 TO switchboard_readonly;
GRANT :V1 TO switchboard_readwrite;

GRANT USAGE on SCHEMA switchboard to switchboard_readonly;
GRANT USAGE on SCHEMA switchboard to switchboard_readwrite;
GRANT USAGE on SCHEMA stg to switchboard_readonly;
GRANT USAGE on SCHEMA stg to switchboard_readwrite;

GRANT SELECT ON ALL TABLES IN SCHEMA switchboard TO switchboard_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA switchboard TO switchboard_readwrite;
GRANT SELECT ON ALL TABLES IN SCHEMA stg TO switchboard_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA stg TO switchboard_readwrite;

ALTER DEFAULT PRIVILEGES IN SCHEMA switchboard GRANT SELECT ON TABLES TO switchboard_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA switchboard GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO switchboard_readwrite;
ALTER DEFAULT PRIVILEGES IN SCHEMA stg GRANT SELECT ON TABLES TO switchboard_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA stg GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO switchboard_readwrite;
