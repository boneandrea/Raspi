TESTEXEC=	python -m unittest discover -s tests
all:
	echo "ALL"
	echo "Run test, type:\n	python -m unittest tests/**.py"
	echo "make test"
test:
	$(TESTEXEC)
testv:
	$(TESTEXEC) -v

testone:
	python -m unittest tests.testSay.TestSay.test_dequeue -v
