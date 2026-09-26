# Design Decisions

This document records key design decisions made in the stellarforge N-body simulation engine.

## Barnes-Hut Theta Opening Angle Criterion

The Barnes-Hut algorithm uses the criterion `s/d < theta` to decide whether to approximate a group of bodies as a single mass:
- `s` = size of the octree node
- `d` = distance from target body to the node's center of mass
- `theta` = opening angle parameter (default 0.5)

**Trade-off:** Smaller theta values increase accuracy but reduce performance. Empirical results:
- θ=0.5: ~5% P90 error at N=100
- θ=0.25: ~1% P90 error at N=100
- θ=0.1: <0.3% P90 error (nearly direct sum accuracy)

## Symplectic Leapfrog Integrator (Kick-Drift-Kick)

We use a second-order symplectic kick-drift-kick scheme:
1. **Kick**: Update velocities by half a timestep
2. **Drift**: Update positions using new velocities
3. **Kick**: Update velocities by remaining half timestep

**Why this choice:**
- Symplectic: Preserves phase-space volume and energy over long simulations
- Time-reversible: Reduces numerical drift
- Second-order accurate with O(N) cost per step

**Alternatives considered:**
- Verlet (equivalent to leapfrog but less intuitive)
- Runge-Kutta (higher accuracy but not symplectic, much more expensive)

## Gravitational Softening

We add a softening parameter `epsilon` to the force law: `F ∝ 1/(r² + ε²)^(3/2)`.

**Purpose:** Prevents singularities when bodies approach each other closely (r → 0).

**Default value:** ε = 10⁻³, chosen as a balance between numerical stability and physical realism.

## Octree Data Structure vs Grid-Based Approaches

We use an adaptive octree where each node can contain 0-1 bodies before subdivision:

**Why octree:**
- Handles non-uniform particle distributions efficiently
- Automatic refinement where needed (high-density regions)
- O(N log N) complexity vs O(N²) for direct summation

**Why not grid-based:**
- Fixed grids waste memory in empty regions
- Less flexible for widely varying densities

## Package Layout: `src/` Directory Structure

We use a `src/stellarforge/` layout rather than top-level package:

**Benefits:**
- Prevents accidental imports from the development directory
- Cleaner test isolation (tests import installed package, not local files)
- Follows modern Python packaging best practices

## Pure Python Implementation (No NumPy in Core)

The core simulation code uses only Python builtins (tuples, lists, dataclasses).

**Trade-offs:**
- ✓ Accessibility: Easier to read, modify, and install
- ✓ Educational: Clear algorithm implementation
- ✗ Performance: ~10-100× slower than vectorized NumPy/C/Cython equivalents

NumPy remains available for benchmarks and analysis scripts via optional dependencies.

## Build System: setuptools

We use setuptools with `pyproject.toml` as the build backend.

**Why:**
- Mature and widely adopted
- No additional dependencies required
- Compatible with standard Python packaging tooling

## Issues Fixed

No critical bugs were found during review. All 14 tests pass. Minor code review observations:
- Bounding box computation in `octree.py` works correctly through cumulative min/max comparisons (code is correct but could be clearer)
- Self-force exclusion properly implemented in `_compute_acceleration_from_node()`
- Empty body list handled in `Integrator.step()`
