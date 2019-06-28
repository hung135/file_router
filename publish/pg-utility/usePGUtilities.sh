#!/bin/bash
# set -x #echo on
mkdir dumps -p

echo "Looping through schemas"
while read schema; do

  if [ "$DROPSCHEMA" == true ]; then
    # DROP External Schema
    printf '%80s\n' | tr ' ' - && echo "DROP External Schema $schema"

    PGPASSWORD=${PGPASSWORD_EXTERNAL} psql \
    -U ${PGUSER_EXTERNAL} -h ${PGHOST_EXTERNAL} -p ${PGPORT_EXTERNAL} -d ${PGDATABASE_EXTERNAL} \
    -c "DROP SCHEMA IF EXISTS $schema CASCADE"
  fi

  # Create Schema on External DB
  printf '%80s\n' | tr ' ' \# && echo "Processing Schema: $schema"

  PGPASSWORD=${PGPASSWORD_EXTERNAL} psql \
  -U ${PGUSER_EXTERNAL} -h ${PGHOST_EXTERNAL} -p ${PGPORT_EXTERNAL} -d ${PGDATABASE_EXTERNAL} \
  -c "CREATE SCHEMA IF NOT EXISTS $schema"

  # DUMP Internal Schema
  printf '%80s\n' | tr ' ' - && echo "DUMP Schema $schema"

  PGPASSWORD=${PGPASSWORD_INTERNAL}  pg_dump -s -n ${schema} -Fc \
  -U ${PGUSER_INTERNAL} -h ${PGHOST_INTERNAL} -p ${PGPORT_INTERNAL} -d ${PGDATABASE_INTERNAL} \
  > dumps/${schema}_schema_changes.db

  # RESTORE External Schema
  printf '%80s\n' | tr ' ' - && echo "RESTORE Schema $schema"

  PGPASSWORD=${PGPASSWORD_EXTERNAL}  pg_restore -n ${schema} \
  -U ${PGUSER_EXTERNAL} -h ${PGHOST_EXTERNAL} -p ${PGPORT_EXTERNAL} -d ${PGDATABASE_EXTERNAL} \
  dumps/${schema}_schema_changes.db

  # DUMP Internal Data
  printf '%80s\n' | tr ' ' - && echo "DUMP DATA $schema"

  PGPASSWORD=${PGPASSWORD_INTERNAL}  pg_dump -a -n ${schema} -Fc \
  -U ${PGUSER_INTERNAL} -h ${PGHOST_INTERNAL} -p ${PGPORT_INTERNAL} -d ${PGDATABASE_INTERNAL} \
  > dumps/${schema}_data_changes.db

  # RESTORE External Data
  printf '%80s\n' | tr ' ' - && echo "RESTORE DATA $schema"

  PGPASSWORD=${PGPASSWORD_EXTERNAL}  pg_restore -n ${schema} \
  -U ${PGUSER_EXTERNAL} -h ${PGHOST_EXTERNAL} -p ${PGPORT_EXTERNAL} -d ${PGDATABASE_EXTERNAL} \
  dumps/${schema}_data_changes.db

  if [ "$CLEANSQL" == true ]; then
    # CLEAN DUMP files
    printf '%80s\n' | tr ' ' - && echo "Clean DUMPS $schema"

    rm dumps/${schema}_schema_changes.db
    rm dumps/${schema}_data_changes.db
  fi

done < ../schemas.txt
printf '%80s\n' | tr ' ' \#
