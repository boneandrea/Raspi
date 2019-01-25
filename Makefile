all:
	echo "ALL"
	echo "Run test, type:\n	python -m unittest tests/**.py"
	echo "make test"
test:
	python -m unittest discover -s tests
