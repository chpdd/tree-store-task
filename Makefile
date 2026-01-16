lint:
	poetry run ruff check .

lint-watch:
	poetry run ruff check . -w

test:
	poetry run pytest