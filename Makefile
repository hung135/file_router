check_env:
	echo db:pg://$(value PGUSER):$(value PGPASSWORD)@$(PGHOST):$(PGPORT)/$(PGDATABASE)

check_connections:
	psql -d $(PGDATABASE) -aeE -c "SELECT pid, usename, application_name, waiting, state, query_start from pg_stat_activity where datname='$(PGDATABASE)'"

data_load:
	echo "Data Load not implemented!"

FORCE ?= false
health_checks:
	( \
		rhobot --loglevel info healthchecks schemas/switchboard/healthchecks/switchboard.sql.yml --report healthcheck.report.html \
	) || $(FORCE)

initialize_db:
	psql -d postgres -a -f migrate/initializeDB.sql \
	-v V1="'$(value PGDATABASE)'"
	psql -d $(PGDATABASE) -aeE -f migrate/initializeLinks.sql \
	-v V1='$(value PGLINKUSER)' -v V2='"$(value PGLINKPASSWORD)"' 

warden:
	psql -d $(PGDATABASE) -a -f migrate/initializeRoles.sql \
	-v V1="$(value PGDATABASE)"

schema_migrate: migration_pgcommon migration_project
	sqitch --engine pg --plan-file migrate/pg-common/migrations/sqitch.plan  status --project pg-common \
		db:pg://'$(value PGUSER)':'$(value PGPASSWORD)'@'$(value PGHOST)':$(PGPORT)/$(PGDATABASE);
	sqitch --engine pg --plan-file migrate/switchboard/sqitch.plan status --project switchboard \
		db:pg://'$(value PGUSER)':'$(value PGPASSWORD)'@'$(value PGHOST)':$(PGPORT)/$(PGDATABASE);

migration_project: initialize_db
	cd migrate/switchboard; \
	sqitch deploy \
		db:pg://'$(value PGUSER)':'$(value PGPASSWORD)'@'$(value PGHOST)':$(PGPORT)/$(PGDATABASE)

migration_pgcommon: initialize_db
	cd migrate/pg-common/migrations; \
	sqitch deploy \
		db:pg://'$(value PGUSER)':'$(value PGPASSWORD)'@'$(value PGHOST)':$(PGPORT)/$(PGDATABASE)

nuke_migrations:
	cd migrate/switchboard; \
	sqitch revert -y \
		db:pg://'$(value PGUSER)':'$(value PGPASSWORD)'@'$(value PGHOST)':$(PGPORT)/$(PGDATABASE)

gocd_init:
	rhobot pipeline push pipelines/deliver.prod.json DEV_DW

py_script:
	$(MAKE) sample_script -C scripts

publish:
	$(MAKE) publish -C publish

tar:
	perl tarup.pl -t switchboard.tar -d scripts/ -e __pycache__ incoming outgoing

#status page  https://static.data.cfpb.local/status/switchboard.html
status:
	rhobot healthchecks \
	schemas/switchboard/healthchecks/switchboard.sql.yml \
	--report status_page.html \
	--template schemas/switchboard/status/status_page.html
	cp status_page.html /home/dtwork/static/status/switchboard.html
	#chmod 766 /home/dtwork/static/status/switchboard.html
