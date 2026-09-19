import argparse
import time
import json
import statistics
import httpx
import asyncio

async def benchmark_endpoint(url, num_requests, concurrency):
    latencies = []
    
    async def make_request(client):
        start = time.perf_counter()
        try:
            # Example payload for routing
            payload = {"source_node": "J1", "target_node": "J45"}
            response = await client.post(url, json=payload)
            response.raise_for_status()
            latencies.append((time.perf_counter() - start) * 1000)
        except Exception as e:
            print(f"Request failed: {e}")
            
    async def worker(client, queue):
        while True:
            try:
                _ = queue.get_nowait()
                await make_request(client)
                queue.task_done()
            except asyncio.QueueEmpty:
                break

    queue = asyncio.Queue()
    for _ in range(num_requests):
        queue.put_nowait(None)

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = []
        for _ in range(concurrency):
            task = asyncio.create_task(worker(client, queue))
            tasks.append(task)
        await asyncio.gather(*tasks)

    if not latencies:
        print("All requests failed.")
        return

    results = {
        "min": min(latencies),
        "median": statistics.median(latencies),
        "mean": statistics.mean(latencies),
        "p90": statistics.quantiles(latencies, n=100)[89] if len(latencies) >= 100 else max(latencies),
        "p95": statistics.quantiles(latencies, n=100)[94] if len(latencies) >= 100 else max(latencies),
        "p99": statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else max(latencies),
        "max": max(latencies),
        "total_requests": len(latencies)
    }
    
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark routing API endpoint")
    parser.add_argument("--url", default="http://localhost:8000/api/v1/routing/path", help="Endpoint URL")
    parser.add_argument("-n", "--requests", type=int, default=500, help="Number of requests")
    parser.add_argument("-c", "--concurrency", type=int, default=10, help="Concurrency level")
    args = parser.parse_args()
    
    asyncio.run(benchmark_endpoint(args.url, args.requests, args.concurrency))
