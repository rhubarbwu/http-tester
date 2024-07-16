# HTTP Load Tester

Test HTTP endpoints by load and measuring performance metrics.

## Usage

```sh
python tester.py <address> [-t DURATION] [-to TIMEOUT] [-qps RATE_LIMIT] [-q]
```

## Arguments

- `<address>`: Address of the endpoint to test.
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
