import asyncio
from random import uniform
from statistics import mean
from time import time

import aiohttp
from aiohttp.client import ClientSession, ClientTimeout


class Tester:
    def __init__(
        self,
        address: str,
        duration: int,
        timeout: int = None,
        rate_limit: int = None,
    ):
        self.address = address
        self.duration = duration
        self.timeout = timeout
        self.rate_limit = rate_limit
        self.latencies = []
        self.n_requests, self.n_errors = 0, 0

    async def send_request(self, session: ClientSession):
        try:
            start = time()
            async with session.get(self.address) as response:
                latency = time() - start
                self.latencies.append(latency)
                if response.status != 200:
                    self.n_errors += 1
        except Exception:
            self.n_errors += 1
        finally:
            self.n_requests += 1

    async def run(self):
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

        print("\n**Summary**")
        print(f"   Address: {self.address}")
        print(f"  Duration: {self.duration}s")
        if self.timeout:
            print(f"   Timeout: {self.timeout}s")
        if self.rate_limit:
            print(f" QPS Limit: {self.rate_limit}")

        print("\n**Results**")
        n_successes = self.n_requests - self.n_errors
        n_digits = len(str(self.n_requests))
        print(f" Success: {n_successes:>{n_digits}}/{self.n_requests}")
        print(f" Failure: {self.n_errors:>{n_digits}}/{self.n_requests}")

        print("\n**Latencies**")
        try:
            print(" Min:", min(self.latencies))
            print(" Max:", max(self.latencies))
            print(" Avg:", mean(self.latencies))
        except Exception:
            print("None recorded. Maybe timed out?")

        print()


from argparse import ArgumentParser


def main():
    parser = ArgumentParser(description="HTTP Load Tester")
    parser.add_argument("address", type=str, help="Address to test.")
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
    args = parser.parse_args()

    tester = Tester(args.address, args.duration, args.timeout, args.rate_limit)
    asyncio.run(tester.run())  # may be better way?
    if not args.quiet:
        tester.report()


if __name__ == "__main__":
    main()
