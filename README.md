# Incoming File Router

> **Database Name:** switchboard  
> **Point of Contact:** Hung Nguyen [hung.nguyen@cfpb.gov](mailto:hung.nguyen@cfpb.gov)  
> **Database Type:** development  
> **Data Catalog URL:** Insert URL Here  

## Table of Contents

- [Overview](#overview)
- [Data Dictionary](#data_dictionary)
- [Permissions and Roles](#permissions)
- [Backup and Retention](#backup)
- [Migrations](#migrations)
- [GoCD Pipeline](#pipeline)
- [Health Checks](#health_checks)

<a name="overview"></a>
## Overview

**TODO:** Fill in this section with a thorough description of the database, it's business purpose, and any important high-level details.

<a name="data_dictionary"></a>
## Data Dictionary

### table_name
| Fields   | Data type | Constraints | Description |
| -------- | --------- | ----------- | ----------- |
| id       | integer   | unique      | Primary key |
| ...      | ...       | ...         | ...         |

<a name="permissions"></a>
## Permissions and Access Roles

**TODO:** List out all Active Directory groups and corresponding Postgres roles that have access to this database, e.g.:

| AD Group                     | PSQL Role                    | Description                    |
| ---------------------------- | ---------------------------- | ------------------------------ |
| switchboard_readonly | switchboard_readonly | Read only access to all tables |

<a name="backup"></a>
## Backup and Retention Requirements

**TODO:** *Please provide a description of how often this database needs to be backed up, and how long backed up data needs to be retained, i.e. weekly snapshots, full point-in-time recovery going back 5 years, etc.*

<a name="migrations"></a>
## Migrations

**TODO:** Please provide any instructions or context for the Sqitch migrations of this project, or delete this section if it is not needed.

<a name="pipeline"></a>
## Pipeline

**TODO:** Please provide any instructions or context for the GoCD pipeline for this project, or delete this section if it is not needed.

<a name="health_checks"></a>
## Health Checks

**TODO:** Please provide any instructions or context for the health checks used for this project, or delete this section if it is not needed.