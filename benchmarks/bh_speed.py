#!/usr/bin/env python3
"""Benchmark Barnes-Hut vs brute-force force computation for stellarforge."""

import random
import time

# Add src to path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stellarforge.core.body import Body
from stellarforge.barneshut.octree import Octree, brute_force_accelerations


def generate_random_bodies(n: int, seed: int = 42) -> list[Body]:
    """Generate random N-body configuration."""
    random.seed(seed)
    bodies = []
    for i in range(n):
        pos = (random.uniform(-1000, 1000),
               random.uniform(-1000, 1000),
               random.uniform(-1000, 1000))
        vel = (random.uniform(-10, 10),
               random.uniform(-10, 10),
               random.uniform(-10, 10))
        mass = random.uniform(1e-3, 1e2)
        bodies.append(Body(position=pos, velocity=vel, mass=mass, id=i))
    return bodies


def benchmark_force_computation(n: int) -> tuple[float, float]:
    """Run Barnes-Hut and brute-force benchmarks at given N."""
    bodies = generate_random_bodies(n)
    
    # Benchmark Barnes-Hut
    start = time.perf_counter()
    tree = Octree(bodies)
    _ = tree.compute_accelerations(bodies)
    bh_time = time.perf_counter() - start
    
    # Benchmark brute-force
    start = time.perf_counter()
    _ = brute_force_accelerations(bodies)
    direct_time = time.perf_counter() - start
    
    return bh_time, direct_time


def main():
    """Run benchmarks at multiple N values."""
    n_values = [128, 256, 512, 1024]
    
    print("=" * 70)
    print("Barnes-Hut vs Brute-Force Acceleration Benchmark")
    print("=" * 70)
    print(f"{'N':<8} {'BH Time (s)':<15} {'Direct Time (s)':<18} {'Speedup':<10}")
    print("-" * 70)
    
    for n in n_values:
        bh_time, direct_time = benchmark_force_computation(n)
        speedup = direct_time / bh_time if bh_time > 0 else float("inf")
        print(f"{n:<8} {bh_time:<15.6f} {direct_time:<18.6f} {speedup:<10.2f}")
    
    print("=" * 70)
    print("Benchmark complete.")


if __name__ == "__main__":
    main()
