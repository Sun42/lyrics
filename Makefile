init:
	pip3 install -r requirements.txt

test:
	python3 ./tests/lyrics_tests.py

.PHONY: init test
