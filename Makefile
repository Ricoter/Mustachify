all: clean format sortimports lint

clean:
	@echo "Cleaning bytecode"
	find . -name '*.pyc' -delete
lint:
	poetry run flake8
format:
	poetry run black --force-exclude deps .
sortimports:
	poetry run isort
runserver:
	DEBUG=1 uvicorn main:app --reload