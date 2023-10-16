
dev:
	pip install -e .[dev]

tests:
	pytest src

black:
	black -l 88 src --exclude "/(__pythran__|doc/_build|\.ipynb_checkpoints/*)/"

clean:
	rm -f tmp_* cases_test/tmp_*