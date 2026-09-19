# Railmind Benchmarks

This directory contains benchmark scripts and results for the Railmind platform, focusing on the GNN routing engine performance.

## Benchmark Methodology

The GNN routing engine was tested for pathfinding latency on a realistic graph topology representing a section of a railway network. 

### Environment
- **Platform**: Docker
- **CPU**: 4-core CPU
- **Memory**: 16GB RAM

### Workload
- **Graph Topology**: 150 track segments, 45 junction nodes
- **Queries**: 500 randomized routing queries between varied source and destination junctions.

## Results: GNN Routing Latency

The engine demonstrated consistent sub-50ms pathfinding latency for the vast majority of queries, well within the real-time operational requirements.

| Metric | Latency (ms) |
|--------|--------------|
| Min    | 12.4         |
| Median | 38.1         |
| Mean   | 39.5         |
| P90    | 44.2         |
| P95    | 46.8         |
| P99    | 49.3         |
| Max    | 54.1         |

*See `gnn_routing_latency.json` for raw metrics.*

## Reproducing the Benchmarks

Ensure the backend services are running via Docker Compose:

```bash
docker-compose up -d backend gnn-router
```

Run the benchmark script:

```bash
pip install httpx
python benchmarks/benchmark.py --url http://localhost:8000/api/v1/routing/path -n 500 -c 10
```
