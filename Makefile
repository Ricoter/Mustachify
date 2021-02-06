all: clean format sortimports lint

clean:
	@echo "Cleaning bytecode"
	find . -name '*.pyc' -delete
lint:
	poetry run flake8
format:
	poetry run black .
sortimports:
	poetry run isort

