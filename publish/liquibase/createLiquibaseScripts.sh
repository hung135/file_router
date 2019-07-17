#!/bin/bash
set -x #echo on
mkdir publish -p

PGconnection="
--url=jdbc:postgresql://${PGHOST_EXTERNAL}:${PGPORT_EXTERNAL}/${PGDATABASE_EXTERNAL} \
--username=${PGUSER_EXTERNAL} \
--password=${PGPASSWORD_EXTERNAL} \
--referenceUrl=jdbc:postgresql://${PGHOST_INTERNAL}:${PGPORT_INTERNAL}/${PGDATABASE_INTERNAL} \
--referenceUsername=${PGUSER_INTERNAL} \
--referencePassword=${PGPASSWORD_INTERNAL}"

echo "Looping through schemas"
while read schema; do

  printf '%80s\n' | tr ' ' -
  echo "Processing Schema: $schema"

  PGPASSWORD=${PGPASSWORD_EXTERNAL} psql \
  -U ${PGUSER_EXTERNAL} -h ${PGHOST_EXTERNAL} -p ${PGPORT_EXTERNAL} -d ${PGDATABASE_EXTERNAL} \
  -c "CREATE SCHEMA IF NOT EXISTS $schema"

  #schema
  ./liquibase \
  ${PGconnection} \
  --changeLogFile="publish/${schema}_schema_changelog.xml" \
  --defaultSchemaName="${schema}" \
  --referenceDefaultSchemaName="${schema}" \
  --diffTypes="" \
  --logFile="publish/${schema}_schema_diff.log" \
  diffChangeLog

  ./liquibase \
  ${PGconnection} \
  --changeLogFile="publish/${schema}_schema_changelog.xml" \
  --defaultSchemaName="${schema}" --referenceDefaultSchemaName="${schema}" \
  --logFile="publish/${schema}_schema_update.log" \
  updateSQL > publish/${schema}_schema_changes.sql

  printf '%80s\n' | tr ' ' -
  echo "Processing Schema Changes for: $schema"
  PGPASSWORD=${PGPASSWORD_EXTERNAL}  psql \
  -U ${PGUSER_EXTERNAL} -h ${PGHOST_EXTERNAL} -p ${PGPORT_EXTERNAL} -d ${PGDATABASE_EXTERNAL} \
  -a -f publish/${schema}_schema_changes.sql

  #data
  ./liquibase \
  ${PGconnection} \
  --changeLogFile="publish/${schema}_data_changelog.xml" \
  --defaultSchemaName="${schema}" --referenceDefaultSchemaName="${schema}" \
  --diffTypes="data" \
  --logFile="publish/${schema}_data_diff.log" \
  diffChangeLog

  ./liquibase \
  ${PGconnection} \
  --changeLogFile="publish/${schema}_data_changelog.xml" \
  --defaultSchemaName="${schema}" --referenceDefaultSchemaName="${schema}" \
  --logFile="publish/${schema}_data_update.log" \
  updateSQL > publish/${schema}_data_changes.sql

  printf '%80s\n' | tr ' '
  echo "Processing Data Changes for: $schema"
  PGPASSWORD=${PGPASSWORD_EXTERNAL}  psql \
  -U ${PGUSER_EXTERNAL} -h ${PGHOST_EXTERNAL} -p ${PGPORT_EXTERNAL} -d ${PGDATABASE_EXTERNAL} \
  -a -f publish/${schema}_data_changes.sql

  # psql < publish/${schema}_schema_changes.sql
  # psql < publish/${schema}_data_changes.sql

done < ../schemas.txt
