# StellarForge Benchmarks

## Running the Benchmarks

To run the Barnes-Hut speed benchmark:

```bash
python benchmarks/bh_speed.py
```

Or with the virtual environment Python:

```bash
.venv/bin/python benchmarks/bh_speed.py
```

## What Each Benchmark Measures

This benchmark suite compares two approaches to computing gravitational forces in N-body simulations:

1. **Barnes-Hut (BH)**: Uses an octree spatial data structure to approximate forces. Bodies far away are grouped together and treated as single point masses, reducing complexity from O(n²) to approximately O(n log n).

2. **Brute-Force (Direct)**: Computes the gravitational force between every pair of bodies explicitly. This is O(n²) but provides exact results.

The benchmark measures the time required to compute accelerations for all bodies at increasing N values (128, 256, 512, 1024).

## Expected Behavior

- **N=128**: Direct computation may be competitive or faster due to overhead in the octree construction
- **N≥256**: Barnes-Hut should become faster than direct computation
- **Speedup grows with N**: As N increases, the O(n log n) BH algorithm gains increasing advantage over O(n²) direct

For reference, at N=1024 in pure Python, expect roughly 2–3× speedup with the current implementation. Pure Python overhead in the octree traversal means the crossover point is around N=512; above that, the O(n log n) advantage gains ground progressively.

## Benchmark Output Format

```
======================================================================
Barnes-Hut vs Brute-Force Acceleration Benchmark
======================================================================
N        BH Time (s)     Direct Time (s)      Speedup     
----------------------------------------------------------------------
128      0.012345      0.023456             1.90      
256      0.024567      0.089012             3.62      
512      0.048901      0.356789             7.29      
1024     0.098765      1.423456             14.41     
======================================================================
Benchmark complete.
```

## Requirements

- Python 3.10+
- stellarforge package installed in the current environment
- No external dependencies required
