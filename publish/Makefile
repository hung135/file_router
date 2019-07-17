
publish:
	echo "Publish not implemented!"

liquibase_script: initialize_db
	cd liquibase; \
	./createLiquibaseScripts.sh

pg_dump_restore: initialize_db
	cd pg-utility; \
	./usePGUtilities.sh

initialize_db:
	PGPASSWORD='$(value PGPASSWORD_EXTERNAL)' psql \
	-U ${PGUSER_EXTERNAL} -h ${PGHOST_EXTERNAL} -p ${PGPORT_EXTERNAL} -d postgres \
	-aeE -f initializeDB.sql \
	-v V1="'$(value PGDATABASE_EXTERNAL)'"
	PGPASSWORD='$(value PGPASSWORD_EXTERNAL)' psql \
	-U ${PGUSER_EXTERNAL} -h ${PGHOST_EXTERNAL} -p ${PGPORT_EXTERNAL} -d $(PGDATABASE_EXTERNAL) \
	-aeE -f initializeLinks.sql \
	-v V1='$(value PGLINKUSER)' -v V2='"$(value PGLINKPASSWORD)"'

warden:
	PGPASSWORD='$(value PGPASSWORD_EXTERNAL)' psql \
	-U ${PGUSER_EXTERNAL} -h ${PGHOST_EXTERNAL} -p ${PGPORT_EXTERNAL} -d $(PGDATABASE_EXTERNAL) \
	-aeE -f initializeRoles.sql \
	-v V1="$(value PGDATABASE_EXTERNAL)"
