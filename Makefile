
pylint:
	pylint app.py

run:
	python app.py

test:
	coverage run -m pytest
	coverage report app.py
