lint:
	autoflake --in-place --recursive --exclude="*/migrations/*,venv,local,media,templates" .
	isort .
	black --line-length 120 .
	flake8 .
