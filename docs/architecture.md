# Architecture

This document describes the architecture and design of the StellarForge N-body simulation engine.

## Module Structure

- **core/**: Core physics and simulation components
  - `body.py`: `Body` dataclass for particle representation
  - `integrator.py`: Leapfrog integrator implementation
- **barneshut/**: Barnes-Hut tree algorithm implementation
  - `octree.py`: Octree spatial partitioning and tree construction
  - `force.py`: Force computation using tree traversal
- **tests/**: Unit and integration tests
- **benchmarks/**: Performance benchmarks
- **demo/**: Example simulations and visualizations

## Data Flow

1. **Body Initialization**: Particle data is loaded into `Body` objects containing position, velocity, mass, and ID.
2. **Octree Construction**: Bodies are inserted into the Barnes-Hut octree, which recursively partitions space into octants.
3. **Force Computation**: For each body, forces are computed by traversing the octree. Nodes are accepted (approximated) if `θ = s/d < θ_threshold`, otherwise children are visited.
4. **Integration**: The leapfrog integrator updates positions and velocities using a kick-drift-kick scheme.
5. **Snapshots**: Simulation states can be serialized for reproducibility and analysis.

## Barnes-Hut Algorithm

The Barnes-Hut algorithm approximates long-range gravitational forces using a hierarchical tree structure:

1. **Octree Construction**: Space is recursively subdivided into octants until each cell contains at most one body. Internal nodes store the total mass and center of mass of their children.

2. **Force Approximation**: When computing force on a body:
   - Traverse the tree from the root.
   - For each node, calculate `θ = s/d` where `s` is the node width and `d` is the distance to the body.
   - If `θ < θ_threshold` (typically 0.5–1.0), approximate the node as a point mass at its center of mass.
   - Otherwise, recursively visit the node's children.

3. **Complexity**: Tree construction is O(N log N), and force computation is O(N log N) total, compared to O(N²) for brute force.

## Leapfrog Integrator

The leapfrog (kick-drift-kick) integrator is a symplectic time-stepping scheme that conserves energy over long simulations:

1. **Kick (half-step)**: Update velocities by half a timestep using current forces.
   `v(t + dt/2) = v(t) + a(t) * dt/2`

2. **Drift**: Update positions by a full timestep.
   `x(t + dt) = x(t) + v(t + dt/2) * dt`

3. **Kick (half-step)**: Update velocities by the remaining half-timestep using new forces.
   `v(t + dt) = v(t + dt/2) + a(t + dt) * dt/2`

This scheme is time-reversible, symplectic, and second-order accurate, making it ideal for long-term orbital dynamics.

## Accuracy Validation

StellarForge validates accuracy by comparing Barnes-Hut results against brute-force calculations on small systems:

1. **Ground Truth**: For N < 100 bodies, all pairwise forces are computed directly (O(N²)).
2. **Comparison**: Barnes-Hut forces and final positions are compared to brute-force results.
3. **Tolerance**: Relative errors must be below 1e-6 for forces and 1e-8 for positions (configurable via θ threshold).

This ensures the approximation error is controlled and predictable.
