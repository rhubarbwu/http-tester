import asyncio
from random import uniform
from statistics import mean, stdev
from time import time

import aiohttp
from aiohttp.client import ClientSession, ClientTimeout


class Tester:
    """HTTP Load Testing Class -- reports error counts and latency statistics."""

    def __init__(
        self,
        address: str,
        duration: int,
        http_method: str = "GET",
        timeout: int = None,
        rate_limit: int = None,
        logging: bool = True,
    ):
        self.address = address
        self.http_method = http_method
        self.duration = duration
        self.timeout = timeout
        self.rate_limit = rate_limit
        self.latencies = []
        self.n_requests, self.n_errors = 0, 0
        self.logging = logging

    async def send_request(self, session: ClientSession):
        """Send an HTTP request from client <session> of method setting."""
        try:
            start = time()

            match self.http_method:
                case "HEAD":
                    session_func = session.head
                case "OPT" | "OPTIONS":
                    session_func = session.options
                case "GET" | _:
                    session_func = session.get

            async with session_func(self.address) as response:
                latency = time() - start
                self.latencies.append(latency)
                if response.status not in [200, 204]:
                    self.n_errors += 1
        except Exception:
            self.n_errors += 1
        finally:
            self.n_requests += 1

    async def run(self):
        """Run the load test by sending HTTP requests in a loop with either
        random delay or pre-set duration (set in __init__).
        """
        timeout = ClientTimeout(self.timeout if self.timeout else self.duration + 1)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = []
            send = lambda s: tasks.append(asyncio.create_task(self.send_request(s)))

            start = time()
            while time() - start < self.duration:
                if not self.rate_limit:  # random delay
                    send(session)
                    await asyncio.sleep(uniform(0, 1))
                    continue

                for _ in range(self.rate_limit):
                    send(session)
                await asyncio.sleep(1)

            await asyncio.gather(*tasks)

    def report(self):
        """Output a report of load test settings, error counts, and latency
        statistics."""
        if not self.logging:
            return

        print("**Summary**")
        print(f"    Address: {self.address}")
        print(f"HTTP Method: {self.http_method}")
        print(f"   Duration: {self.duration}s")
        if self.timeout:
            print(f"    Timeout: {self.timeout}s")
        if self.rate_limit:
            print(f"  QPS Limit: {self.rate_limit}")

        print("\n**Results**")
        n_successes = self.n_requests - self.n_errors
        n_digits = len(str(self.n_requests))
        print(f" Success: {n_successes:>{n_digits}}/{self.n_requests}")
        print(f" Failure: {self.n_errors:>{n_digits}}/{self.n_requests}")
        # rate percentage can be computed trivially; counts are more flexible

        print("\n**Latencies**")
        try:
            print(" Min:", min(self.latencies))
            print(" Max:", max(self.latencies))
            print(" Avg:", mean(self.latencies))
            print(" StD:", stdev(self.latencies))
        except Exception:
            print("None recorded. Maybe timed out?")

    def write_to_json(self, output_file: str = None):
        """Write results to file at path <output_file>.
        Outputs warnings only if logging is enabled.
        """
        import json

        if output_file is None:
            output_file = f"./results-{time()}.json"

        results = {
            "address": self.address,
            "http_method": self.http_method,
            "duration": self.duration,
            "rate_limit": self.rate_limit,
            "timeout": self.timeout,
            "n_requests": self.n_requests,
            "n_failure": self.n_errors,
            "n_success": self.n_requests - self.n_errors,
        }
        try:
            results["min_latency"] = min(self.latencies)
            results["max_latency"] = max(self.latencies)
            results["avg_latency"] = mean(self.latencies)
            results["std_latency"] = stdev(self.latencies)
        except Exception:
            pass

        if not output_file.endswith(".json"):
            if self.logging:
                print(f"\nWriting -- adding extension: {output_file}(.json)")
            output_file += ".json"

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
        except Exception:
            if self.logging:
                print(f"\nCan't write: file {output_file} may not exist.")


from argparse import ArgumentParser


def main():
    parser = ArgumentParser(description="HTTP Load Tester")
    parser.add_argument("address", type=str, help="Address to test.")
    parser.add_argument(
        "-x",
        "--http_method",
        type=str,
        choices=["GET", "HEAD", "OPTIONS"],
        default="GET",
        help="Which HTTP request method to send. Default: GET.",
    )
    parser.add_argument(
        "-t", "--duration", type=int, default=5, help="Duration of the test (seconds)."
    )
    parser.add_argument(
        "-to",
        "--timeout",
        type=int,
        default=None,
        help="Timeout per request (seconds). Default: None (total duration).",
    )
    parser.add_argument(
        "-qps",
        "--rate_limit",
        type=int,
        default=None,
        help="Rate limiting (queries per second). Default: None (random relay).",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Whether to suppress output (e.g. only save to file).",
    )

    parser.add_argument(
        "-o",
        "--save_results",
        action="store_true",
        help="Whether to store out. Default:  (don't save).",
    )
    parser.add_argument(
        "-f",
        "--output_file",
        type=str,
        default=None,
        help="Path to JSON file to store results. Default: None (generate on completion time).",
    )

    args = parser.parse_args()

    tester = Tester(
        args.address,
        args.duration,
        args.http_method,
        args.timeout,
        args.rate_limit,
        not args.quiet,
    )
    asyncio.run(tester.run())  # may be better way?
    if not args.quiet:
        print("=" * 64)
        tester.report()
    if args.save_results or args.output_file:
        tester.write_to_json(args.output_file)
    if not args.quiet:
        print("=" * 64)
        print()


if __name__ == "__main__":
    main()
