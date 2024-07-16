build: Dockerfile tester.py
	docker build -t tester .

test-docker: Dockerfile tester.py
	docker run --rm tester http://microsoft.com -t 5 -qps 50

test: tester.py
	python tester.py http://microsoft.com -t 1 -qps 100
