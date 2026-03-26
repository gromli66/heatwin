.PHONY: data clean test

data:
	python src/data/load.py

clean:
	rm -rf data/interim/* data/processed/*

test:
	python -m pytest tests/ -v