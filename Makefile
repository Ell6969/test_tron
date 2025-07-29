test:
	pytest -v
formatter:
	isort --profile black src
	black --line-length=120 src