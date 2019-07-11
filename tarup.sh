#!/bin/bash
#tar -czvf switcboard.tar ./prod.yaml -C  ./scripts/ scripts/  -C $VIRTUAL_ENV . --exclude=sample_script.py --exclude=switchboard.yaml
pyinstaller ./scripts/switchboard.py
tar -czvf switcboard.tar -C dist .
