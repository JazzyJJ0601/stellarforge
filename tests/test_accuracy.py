"""Tests for Barnes-Hut vs brute-force accuracy."""

import random
import math
import pytest
from stellarforge.core.body import Body
from stellarforge.barneshut.octree import Octree, brute_force_accelerations


def _random_bodies(n: int, seed: int = 42) -> list[Body]:
    """Generate n random bodies with reproducible seed."""
    rng = random.Random(seed)
    bodies = []
    for i in range(n):
        bodies.append(Body(
            id=i,
            mass=rng.uniform(0.1, 10.0),
            position=(rng.uniform(-50, 50), rng.uniform(-50, 50), rng.uniform(-50, 50)),
            velocity=(rng.uniform(-5, 5), rng.uniform(-5, 5), rng.uniform(-5, 5)),
        ))
    return bodies


def _relative_errors(bodies, tree, theta):
    """Return sorted relative force errors for all bodies."""
    bh = tree.compute_accelerations(bodies, theta=theta)
    bf = brute_force_accelerations(bodies)
    errors = []
    for b in bodies:
        a_bh = bh[b.id]
        a_bf = bf[b.id]
        norm_bf = math.sqrt(sum(v**2 for v in a_bf))
        if norm_bf > 1e-15:
            diff = math.sqrt(sum((a_bh[j] - a_bf[j])**2 for j in range(3)))
            errors.append(diff / norm_bf)
    errors.sort()
    return errors


class TestBHAccuracy:
    """Barnes-Hut accuracy relative to brute-force O(n²) reference."""

    def test_bh_theta_0_5_n100(self):
        """θ=0.5, N=100: 90th percentile error < 5%."""
        bodies = _random_bodies(100, seed=42)
        tree = Octree(bodies)
        errors = _relative_errors(bodies, tree, theta=0.5)

        assert len(errors) > 0, "No valid error measurements"
        p90 = errors[int(0.9 * len(errors))]
        assert p90 < 0.05, f"90th percentile error {p90*100:.2f}% >= 5%"

    def test_bh_theta_0_25_n100(self):
        """θ=0.25, N=100: 90th percentile error < 1%."""
        bodies = _random_bodies(100, seed=42)
        tree = Octree(bodies)
        errors = _relative_errors(bodies, tree, theta=0.25)

        assert len(errors) > 0, "No valid error measurements"
        p90 = errors[int(0.9 * len(errors))]
        assert p90 < 0.01, f"90th percentile error {p90*100:.2f}% >= 1%"

    def test_bh_theta_0_1_n100(self):
        """θ=0.1, N=100: 90th percentile error < 0.3% (almost direct sum)."""
        bodies = _random_bodies(100, seed=42)
        tree = Octree(bodies)
        errors = _relative_errors(bodies, tree, theta=0.1)

        assert len(errors) > 0, "No valid error measurements"
        p90 = errors[int(0.9 * len(errors))]
        assert p90 < 0.003, f"90th percentile error {p90*100:.4f}% >= 0.3%"

    def test_bh_theta_0_5_n1000(self):
        """θ=0.5, N=1000: 90th percentile error < 10% (P0.5 criterion: < 1% at tighter θ)."""
        bodies = _random_bodies(1000, seed=42)
        tree = Octree(bodies)
        errors = _relative_errors(bodies, tree, theta=0.5)

        assert len(errors) > 0, "No valid error measurements"
        p90 = errors[int(0.9 * len(errors))]
        max_err = errors[-1]
        print(f"θ=0.5 N=1000: p90_error={p90*100:.2f}% max_error={max_err*100:.2f}%")
        assert p90 < 0.10, f"90th percentile error {p90*100:.2f}% >= 10%"

    def test_bh_theta_0_25_n1000(self):
        """θ=0.25, N=1000: 90th percentile error < 1% (P0.5 criterion)."""
        bodies = _random_bodies(1000, seed=42)
        tree = Octree(bodies)
        errors = _relative_errors(bodies, tree, theta=0.25)

        assert len(errors) > 0, "No valid error measurements"
        p90 = errors[int(0.9 * len(errors))]
        max_err = errors[-1]
        print(f"θ=0.25 N=1000: p90_error={p90*100:.4f}% max_error={max_err*100:.2f}%")
        assert p90 < 0.01, f"90th percentile error {p90*100:.4f}% >= 1%"

    def test_tighter_theta_improves_accuracy(self):
        """θ=0.1 gives strictly better accuracy than θ=0.5."""
        bodies = _random_bodies(200, seed=42)
        tree = Octree(bodies)

        errors_loose = _relative_errors(bodies, tree, theta=0.5)
        errors_tight = _relative_errors(bodies, tree, theta=0.1)

        p90_loose = errors_loose[int(0.9 * len(errors_loose))]
        p90_tight = errors_tight[int(0.9 * len(errors_tight))]

        assert p90_tight < p90_loose, (
            f"Tighter θ should improve accuracy: "
            f"p90_loose={p90_loose*100:.4f}% p90_tight={p90_tight*100:.4f}%"
        )