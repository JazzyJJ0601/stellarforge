# Changelog

## [1.0.0] — 2026-09-26

### Added
- Barnes-Hut octree spatial partitioning for O(n log n) gravitational force computation
- Leapfrog kick-drift-kick symplectic integrator with configurable timestep
- Body dataclass (position, velocity, mass, id) for particle representation
- Brute-force O(n²) direct-summation reference for accuracy validation
- Gravitational softening parameter to prevent singularities at close encounters
- Configurable theta opening angle controlling accuracy–performance trade-off

### Testing & Validation
- 14 automated tests covering octree structure, force symmetry, BH accuracy (θ=0.5/0.25/0.1 at N=100/1000), energy conservation (two-body <2% drift, three-body <0.5% drift), and edge cases
- BH accuracy validated against brute-force reference: P90 error <5% at θ=0.5, <1% at θ=0.25, <0.3% at θ=0.1

### Benchmarks
- BH vs direct-sum speed comparison at N=128, 256, 512, 1024
- BH speedup of ~1.8× at N=1024 (pure Python, θ=0.5)
- Crossover at N≈512 where BH begins to outperform direct sum

### Demo
- Two-body circular orbit simulation (500 steps, dt=0.01)
- CSV snapshot output every 50 steps for post-processing
- Verified energy drift of 1.24% over 500 steps

### Documentation
- README with overview, setup, architecture, tests, benchmarks, demo, limitations, and roadmap
- Architecture document (docs/architecture.md) describing module structure and data flow
- Design decisions document (docs/design-decisions.md) covering key trade-offs
- Completion criteria (docs/completion-criteria.md) with 45 verifiable milestones
- Clean-setup verification report (docs/verification.md)

### Infrastructure
- MIT License
- src/ layout following modern Python packaging conventions
- setuptools build backend with pyproject.toml
- run_tests.sh single-command test runner
- Private GitHub repository at https://github.com/JazzyJJ0601/stellarforge