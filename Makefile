build: Dockerfile tester.py
	docker build -t tester .

test-docker: Dockerfile tester.py
	docker run --rm tester http://microsoft.com -t 5 -qps 20
	python tester.py http://cslab.cs.toronto.edu -t 5 -to 1 -qps 20

test: tester.py
	python tester.py http://microsoft.com -t 1 -qps 100
	python tester.py http://cslab.cs.toronto.edu -t 1 -to 1 -qps 100
