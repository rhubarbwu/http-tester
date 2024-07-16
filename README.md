# HTTP Load Tester

Test HTTP endpoints by load and measuring performance metrics. Currently only supports `GET`, `HEAD`, `OPTIONS` requests.

## Usage

```sh
python tester.py <address> [-x HTTP_METHOD] [-t DURATION] [-to TIMEOUT] [-qps RATE_LIMIT] [-q]
```

## Arguments

- `<address>`: Address of the endpoint to test.
- `-x, request_method HTTP_METHOD`: Which HTTP request method to send. (default: `GET`).
- `-t, --duration DURATION`: Duration of the test in seconds (default: 5).
- `-to, --timeout TIMEOUT`: Timeout per request in seconds (default: -1 for total duration).
- `-qps, --rate_limit RATE_LIMIT`: Rate limiting in queries per second (default: None for random relay).
- `-q, --quiet`: Suppress output to console (e.g., only save to file).

## Examples

1. Test an endpoint for 10 seconds with default settings:

   ```sh
   python tester.py github.com -t 10
   ```

2. Test an endpoint for 5 seconds with a rate limit of 50 queries per second:

   ```sh
   python tester.py github.com -t 5 -qps 50
   ```

3. Test an endpoint for 1 minute with a timeout of 2 seconds per request and suppress output:

   ```sh
   python http_load_tester.py github.com -t 60 -to 2 -q
   ```

### Outputs from Makefile Tests

```sh
python tester.py http://www.microsoft.com -t 1 -qps 100 -o -f results-ms

**Summary**
    Address: http://www.microsoft.com
HTTP Method: GET
   Duration: 1s
  QPS Limit: 100

**Results**
 Success:  98/100
 Failure:   2/100

**Latencies**
 Min: 0.40906381607055664
 Max: 1.9798245429992676
 Avg: 1.1469733106846711
 StD: 0.32635958637489465

Warning -- adding extension: results-ms(.json)
python tester.py http://www.google.com -t 1 -qps 100 -o -f results-g -x HEAD

**Summary**
    Address: http://www.google.com
HTTP Method: HEAD
   Duration: 1s
  QPS Limit: 100

**Results**
 Success: 100/100
 Failure:   0/100

**Latencies**
 Min: 0.13163399696350098
 Max: 0.17531871795654297
 Avg: 0.16290982246398925
 StD: 0.010312770109600166

Warning -- adding extension: results-g(.json)
python tester.py http://cslab.cs.toronto.edu -t 1 -to 1 -qps 100 -o

**Summary**
    Address: http://cslab.cs.toronto.edu
HTTP Method: GET
   Duration: 1s
    Timeout: 1s
  QPS Limit: 100

**Results**
 Success:   0/100
 Failure: 100/100

**Latencies**
None recorded. Maybe timed out?
```