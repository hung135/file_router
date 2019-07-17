
--requires op_dba.create_role wrapper function
SELECT op_dba.create_role ('switchboard_readonly');

--uncomment for dev on local machines
--CREATE ROLE switchboard_readonly;

--Permission Granting shall be replaced by warden
GRANT :V1 TO switchboard_readonly;

GRANT USAGE on SCHEMA switchboard to switchboard_readonly;

GRANT SELECT ON ALL TABLES IN SCHEMA switchboard TO switchboard_readonly;

ALTER DEFAULT PRIVILEGES IN SCHEMA switchboard GRANT SELECT ON TABLES TO switchboard_readonly;
