env: env/bin/activate

env/bin/activate: requirements.txt
	test -d env || /usr/local/bin/virtualenv env -p python3
	env/bin/python -m pip install -Ur requirements.txt
	touch env/bin/activate

sample_script: env
	env/bin/python -u sample_script.py