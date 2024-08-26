.PHONY: setup install add freeze run test clean

setup:
	poetry init -n

install:
	poetry install

add:
	poetry add $(package)

freeze:
	poetry export -f requirements.txt --output requirements.txt

run:
	poetry run python main.py

test:
	poetry run pytest

clean:
	poetry env remove --all
	find . -type d -name __pycache__ -exec rm -rf {} +