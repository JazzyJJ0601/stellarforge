# StellarForge

StellarForge is an N-body gravitational simulation engine implementing the Barnes-Hut algorithm (O(n log n) force calculation via octree spatial partitioning) for efficient computation of gravitational forces in large N-body systems.

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLI / Examples                           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Core Module                              │
│                  ┌──────────────┐   ┌──────────────┐            │
│                  │    Body      │   │  Integrator  │            │
│                  │ (dataclass)  │   │ (Leapfrog)   │            │
│                  └──────────────┘   └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Barnes-Hut Module                           │
│                  ┌──────────────────┐                           │
│                  │     Octree       │                           │
│                  │ (spatial index)  │                           │
│                  └──────────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Visualization                            │
└─────────────────────────────────────────────────────────────────┘
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed documentation on:
- Module structure (core/, barneshut/, tests/, benchmarks/, demo/)
- Data flow: Body → Octree construction → Force computation → Integration → Snapshots
- Barnes-Hut algorithm details
- Leapfrog integrator implementation
- Accuracy validation (BH vs brute-force comparison)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
3. Install in editable mode:
   ```bash
   .venv/bin/pip install -e .
   ```
   
   For quick setup instructions, see the sections below.

## Running Tests

```bash
bash run_tests.sh
```

All tests pass deterministically using a fixed random seed for reproducibility.

## Running Benchmarks

```bash
python benchmarks/bh_speed.py
```

This benchmarks the Barnes-Hut algorithm performance against brute-force computation.

## Running Demo

```bash
.venv/bin/python demo/orbit_demo.py
```

Runs a sample orbital simulation to demonstrate the engine.

## Features

- Barnes-Hut octree spatial partitioning (O(n log n) force computation)
- Body dataclass for particle representation (position, velocity, mass, id)
- Leapfrog integrator with kick-drift-kick scheme
- Extensible integrator protocol for future algorithms
- Well-tested core components

## Limitations

- Pure Python implementation
- Not suitable for systems with >10k particles
- No GPU acceleration support

## Roadmap

The project roadmap includes the following planned enhancements:

- [ ] CLI interface for configuration and execution
- [ ] Adaptive timestepping
- [ ] Collision detection
- [ ] Visualization tools
- [ ] GPU acceleration
