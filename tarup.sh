#!/bin/bash
#tar -czvf switcboard.tar ./prod.yaml -C  ./scripts/ scripts/  -C $VIRTUAL_ENV . --exclude=sample_script.py --exclude=switchboard.yaml
tar -czvf switcboard.tar ./prod.yaml ./scripts/ -C $VIRTUAL_ENV . 
