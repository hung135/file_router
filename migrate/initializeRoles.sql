
--requires op_dba.create_role wrapper function
SELECT op_dba.create_role ('file_router_readonly');
SELECT op_dba.create_role ('file_router_readwrite');

--uncomment for dev on local machines
--CREATE ROLE file_router_readonly;
--CREATE ROLE file_router_readwrite;

--Permission Granting shall be replaced by warden
GRANT :V1 TO file_router_readonly;
GRANT :V1 TO file_router_readwrite;

GRANT USAGE on SCHEMA file_router to file_router_readonly;
GRANT USAGE on SCHEMA file_router to file_router_readwrite;
GRANT USAGE on SCHEMA stg to file_router_readonly;
GRANT USAGE on SCHEMA stg to file_router_readwrite;

GRANT SELECT ON ALL TABLES IN SCHEMA file_router TO file_router_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA file_router TO file_router_readwrite;
GRANT SELECT ON ALL TABLES IN SCHEMA stg TO file_router_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA stg TO file_router_readwrite;

ALTER DEFAULT PRIVILEGES IN SCHEMA file_router GRANT SELECT ON TABLES TO file_router_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA file_router GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO file_router_readwrite;
ALTER DEFAULT PRIVILEGES IN SCHEMA stg GRANT SELECT ON TABLES TO file_router_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA stg GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO file_router_readwrite;
