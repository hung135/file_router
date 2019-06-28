
--requires op_dba.create_role wrapper function
SELECT op_dba.create_role ('file_router_readonly');

--uncomment for dev on local machines
--CREATE ROLE file_router_readonly;

--Permission Granting shall be replaced by warden
GRANT :V1 TO file_router_readonly;

GRANT USAGE on SCHEMA file_router to file_router_readonly;

GRANT SELECT ON ALL TABLES IN SCHEMA file_router TO file_router_readonly;

ALTER DEFAULT PRIVILEGES IN SCHEMA file_router GRANT SELECT ON TABLES TO file_router_readonly;
