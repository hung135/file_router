# Switchboard

Switchboard is part data cataloging and part data moving. Simply put, give Switchboard a directory and it will log your files current location and final location and any `logic` that may occur in-between. For now we only support GoCD kickoffs, however, we will be supporting AWS Lambdas in the future.

## Tables of Contents
- [Requirements](#requirements)
- [Deploying](#deploying)
- [Configuration](#configuration)
- [Usage](#usage)

# Requirements
PIP packages will need to install:
```bash
sqlalchemy==1.2.4
psycopg2-binary==2.7.4
pyyaml==5.1.1
requests==2.22.0
```

Have a postgres database setup and set the following environment variables:
- PGUSER
- PGPASSWORD
- PGHOST
- PGPORT

Once you are ready simply `git clone` this repository.

# Deploying
Wherever you are deploying this you may run into python versioning and/or packages issues where you may not be admin to overcome. Using `PyInstaller` we are able to package this up into an executable that you can move. 

To do this run:
`bash BuildMe.sh` this will output a a tar file with your exectuable

# Configuration
The entire project runs off a configured yaml file like the following:
```yaml
project1:
  logging: '<path-to-output-logger>'
  incoming: 
    path: '<path-to-data>'
    file_pattern: 
      - '*.csv'
      - '*.zip'
      ...
  outgoing: 
    path: '<path-to-output-data>'
    logic:
      rename_options:
        - lowercase
        - snakecase
        ...
      file_path_extract: <regex-of-important-information-to-extract>
    # Make sure GoCD username and pasword env var is in place. 
    # make sure we pass in the GoCD api pipeline;
    # https://ci.example.com/go/api
    # This expects: gocd-username and gocd-passwd to be set in
    #   environment variables 
    api: 
      uri: "uri"
      pipeline: "pipe"
```

You can configure this to have multiple projects, ie. project1,project2,project3,...which will run sequentially.

# Usage
If using the pyinstalled verison you can run `
```bash
usage: switchboard.py [-h] [-y YAML] [-s SKELETON] [-v] [-d] [--version]

Process a yaml file

optional arguments:
  -h, --help            show this help message and exit
  -s SKELETON, -skeleton SKELETON, --skeleton SKELETON
                        Generates a skeleton.yaml file to the directory
                        specified
  -v, -verbose          Enable verbose mode
  -d, --dry             Enable dry mode which will run the entire yaml file
                        with output only, nothing will be moved or saved
  --version             Version of executable

Required:
  -y YAML, -yaml YAML, --yaml YAML
                        Location of the yaml file
```