.PHONY: data clean test validate

data:
	python src/data/load.py

clean:
	rm -rf data/interim/* data/processed/*

test:
	python -m pytest tests/ -v

validate:
	python src/data/validate.py