# HTTP Load Tester

Test HTTP endpoints by load and measuring performance metrics.

## Usage

```sh
python tester.py <address> [-t DURATION] [-qps RATE_LIMIT]
```

## Arguments

- `<address>`: Address of the endpoint to test.
- `-t, --duration DURATION`: Duration of the test in seconds (default: 5).
- `-qps, --rate_limit RATE_LIMIT`: Rate limiting in queries per second (default: None for random relay).

## Examples

1. Test an endpoint for 10 seconds with default settings:

   ```sh
   python tester.py github.com -t 10
   ```

2. Test an endpoint for 5 seconds with a rate limit of 50 queries per second:

   ```sh
   python tester.py github.com -t 5 -qps 50
   ```
