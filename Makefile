.PHONY: install lint format type-check check-all clean

install:
	pip install -r requirements.txt

lint:
	flake8 .

format:
	black .
	isort .

type-check:
	mypy .

check-all: format lint type-check

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 