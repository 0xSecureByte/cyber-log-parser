import asyncio
import httpx
import time
import random
import datetime
import string
import sys
from tqdm import tqdm

class Benchmark:
    def __init__(self, url, num_requests, batch_size):
        self.url = url
        self.num_requests = num_requests
        self.batch_size = batch_size
        self.results = []

    async def send_request(self, client, data):
        try:
            response = await client.post(self.url, json=data)
            return response.status_code, response.json()
        except Exception as e:
            return 500, {"error": str(e)}

    async def batch_requests(self, client, batch_size):
        tasks = []
        for _ in range(batch_size):
            random_timestamp = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(-3600, 3600))
            random_log_level = random.choice(["DEBUG", "INFO", "WARNING", "ERROR"])
            random_message = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
            data = {
                "timestamp": random_timestamp.isoformat() + "Z",
                "log_level": random_log_level,
                "message": random_message
            }
            tasks.append(self.send_request(client, data))
        return await asyncio.gather(*tasks)

    async def run(self):
        async with httpx.AsyncClient(timeout=60.0) as client:
            start_time = time.time()
            with tqdm(total=self.num_requests, desc="Processing Requests", unit="req", dynamic_ncols=True, colour="cyan") as pbar:
                for i in range(0, self.num_requests, self.batch_size):
                    current_batch_size = min(self.batch_size, self.num_requests - i)
                    batch_results = await self.batch_requests(client, current_batch_size)
                    self.results.extend(batch_results)
                    pbar.update(current_batch_size)
            end_time = time.time()

        self.report_results(end_time - start_time)

    def report_results(self, total_time):
        failed_requests = [result for result in self.results if result[0] >= 400]
        print(f"\nTotal time taken for processing {self.num_requests} requests: {total_time:.2f} seconds")
        print(f"Final Results: {len(self.results) - len(failed_requests)} requests were successfully processed.")
        print(f"Failed Requests: {len(failed_requests)} requests failed.")
        print(f"Average time taken per request: {total_time / self.num_requests:.4f} seconds")
        print(f"Total time elapsed: {total_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python benchmark.py <number_of_requests> <batch_size>")
        sys.exit(1)
    num_requests = int(sys.argv[1])
    batch_size = int(sys.argv[2])
    benchmark = Benchmark("http://127.0.0.1:8000/logs/", num_requests, batch_size)
    asyncio.run(benchmark.run())