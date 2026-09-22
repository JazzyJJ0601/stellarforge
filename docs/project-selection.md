# Project Selection: stellarforge — Gravitational N-Body Simulation Engine

This document documents the rationale for selecting **stellarforge** as the project to build within Project Forge.

## Rationale

### Portfolio context

This project is selected for **Project 4 (Forge)** — the reputation engine in the 10-project portfolio. Per the portfolio definition, Forge's purpose is to build technical credibility through open engineering. stellarforge serves that role by demonstrating computational physics depth, algorithmic implementation from first principles, rigorous testing, and performance engineering.

### Why this project is technically impressive

The N-body problem — predicting the gravitational evolution of a system of N mutually-interacting particles — is a foundational challenge in computational physics, with direct applications in astrophysics (galaxy formation, dark-matter halo evolution, planetary dynamics), plasma physics, and molecular dynamics. A naive direct-sum approach scales as **O(n²)**, making it computationally intractable beyond a few thousand particles. stellarforge implements the **Barnes-Hut algorithm**, a tree-based spatial partitioning method that achieves **O(n log n)** complexity by grouping distant particles into multipole approximations. This is the same algorithmic innovation that enabled the first large-scale cosmological simulations.

### Existing code in the repository

The repository already contains working implementations:

- **Barnes-Hut octree** (`stellarforge/barneshut/octree.py`, 218 lines) — correct recursive subdivision, center-of-mass aggregation, theta-criterion tree walk with gravitational softening
- **Leapfrog integrator** (`stellarforge/core/integrator.py`, 67 lines) — symplectic kick-drift-kick integration
- **Brute-force O(n²) reference** for accuracy validation (`octree.py:brute_force_accelerations`)
- **Test suite** (`tests/`) — 8 tests covering octree structure, force symmetry, accuracy bounds (p90 error < 5% at θ=0.5, < 1% at θ=0.25, < 0.3% at θ=0.1), energy conservation (two-body < 2% drift, three-body < 0.5% drift)

### Depth of the Technical Challenge

| Challenge | Why It Matters |
|-----------|----------------|
| **Octree construction** | Dynamically partitioning a 3D point cloud into a hierarchical spatial tree requires careful subdivision logic and memory management. |
| **Multipole acceptance criterion** | The opening angle θ controls the accuracy-performance tradeoff — setting it too tight loses the O(n log n) advantage; too loose introduces unacceptable force error. |
| **Numerical integration** | Simple Euler integration is unstable for orbital motion. Symplectic integrators (Leapfrog, RK4) preserve energy over long timescales — a subtle but critical requirement. |
| **Accuracy validation** | Comparing tree-approximated forces against brute-force O(n²) computation and measuring energy drift over thousands of timesteps. |
| **Visualization pipeline** | Exporting particle positions as frame sequences for animation assembly — compressing >1M data points per frame into meaningful visuals. |

The project touches **algorithm design** (spatial trees), **numerical methods** (integration schemes), **physics** (gravitational dynamics, conservation laws), and **software engineering** (modular architecture, testing, CLI design).

## Measurable Completion Criteria (v1.0)

### Priority 0 — Ship-blocking
- [ ] P0.1 — Barnes-Hut octree correctly built from arbitrary 3D particle positions with configurable maximum particles-per-leaf (`max_particles=1` by default).
- [ ] P0.2 — Recursive force calculation via tree traversal with configurable opening angle θ, computing acceleration on every particle.
- [ ] P0.3 — Leapfrog (kick-drift-kick) integrator with fixed timestep, evolving positions and velocities.
- [ ] P0.4 — Brute-force O(n²) direct-sum force calculation as a reference implementation.
- [ ] P0.5 — Accuracy test: relative force error < 1% for a random N=1000 particle distribution at θ=0.5 when compared to direct sum.

### Priority 1 — Usability
- [ ] P1.1 — CLI interface accepting simulation parameters (N, timestep, integration method, output directory).
- [ ] P1.2 — Frame export: snapshots (positions + metadata) written to disk at configurable intervals.
- [ ] P1.3 — Plummer-model initial-condition generator (standard astrophysical test).

### Priority 2 — Correctness & Robustness
- [ ] P2.1 — Energy conservation: total energy drift < 1% over 1000 timesteps for a stable orbit (two-body Kepler problem).
- [ ] P2.2 — Softening parameter ε to prevent singularities at close encounters, configurable.
- [ ] P2.3 — Negative-energy bound systems remain bound over 10,000 timesteps.

### Priority 3 — Performance & Extensions
- [ ] P3.1 — Adaptive timestepping based on local acceleration magnitude.
- [ ] P3.2 — Multiprocessing parallelization of force calculation.
- [ ] P3.3 — Collision detection and merger handling.
- [ ] P3.4 — REST API for headless programmatic control (Flask/FastAPI).

## First Working Component — The Barnes-Hut Octree

The octree is the algorithmic core of the entire project — the data structure that enables O(n log n) performance. It is tested in isolation:

- **Tree construction**: subdivides 3D space into eight octants recursively until each leaf contains ≤1 particle.
- **Center-of-mass aggregation**: each internal node stores the total mass and center-of-mass of its subtree.
- **Serialization / traversal**: depth-first enumeration for verification.
- **Empty space handling**: nodes covering empty regions are not subdivided.

## Rejected Alternatives (from portfolio and beyond)

| Candidate | Rejected Because |
|-----------|-----------------|
| Exoplanet Hunter | Requires live astronomical data feeds; hard to test deterministically without real survey data |
| FaultLab | No existing seed code; fault-injection infrastructure is speculative without a target system |
| Space Game Engine | Broad scope, design-heavy; more game-design than computational depth |
| Elastic PC (Project 1) | Commercially important but infrastructure-heavy (streaming, provisioning, networking) — not a pure-code repo showcase |
| AI Inference Lab (Project 3) | Already has its own project; research-focused rather than build-focused |
| Project Prometheus (Project 5) | Research project with simulation tools as a by-product, not the main deliverable |
| Software 3D rasterizer | Impressive but mostly solved; less room for algorithmic novelty beyond the core pipeline |
| Real-time fluid simulation (SPH) | Requires GPU or compute-heavy visualization to be interesting — dependencies reduce portability |
| Minimal database engine | Well-trodden ground; hard to make visually compelling |
| Compiler for a hobby language | Large upfront grammar/lexer work before reaching the technically deep parts (register allocation, SSA) |
| Voxel terrain engine | Strong visual appeal but heavily graphics-API dependent; less portable and harder to test in CI |

stellarforge wins on **algorithmic depth + visual payoff + testability in isolation + portable pure-Python core + alignment with Forge's reputation mission**.

*Document authored: 22 September 2026*