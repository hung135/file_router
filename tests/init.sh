#!/bin/bash

psql -c"create role operational_dba"
mkdir -p "/home/dtdata/transfer/connect_direct/frb/download/"