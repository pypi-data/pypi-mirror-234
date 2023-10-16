


MODULE:

	https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/
	
	#
	#	RETRIEVE PIP
	#
	python -m pip install --upgrade pip
	
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	sudo python get-pip.py
	
	#
	#	VIRTUAL ENVIRONMENTS
	#
	python3 -m venv VENV
	source VENV/bin/activate
	python3 -m pip install --upgrade pip-tools	
	
	#
	#	https://pip.pypa.io/en/stable/installation/
	#
	python3 -m pip install --upgrade build
	python3 -m pip install --upgrade twine
	
	
	
	(rm -rf dist && python3 -m build --sdist && twine upload dist/*)
	
	
	[build-system]
	requires = ["setuptools ~= 58.0", "cython ~= 0.29.0"]
	
	
	PUBLISHERS:
		https://stackoverflow.com/questions/64150719/how-to-write-a-minimally-working-pyproject-toml-file-that-can-install-packages
		
		
		SETUPTOOLS:
			(rm -rf dist && python3 -m build --sdist && twine upload dist/*)
		
		FLIT:
			python3 -m pip install flit
			
			
		HATCH:
			pip install hatch
	
	LINTING:
		https://flake8.pycqa.org/en/latest/