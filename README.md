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

## Quickstart

```bash
pip install -e .
pytest tests/ -v
```

## Features

- Barnes-Hut octree spatial partitioning (O(n log n) force computation)
- Body dataclass for particle representation (position, velocity, mass, id)
- Leapfrog integrator with kick-drift-kick scheme
- Extensible integrator protocol for future algorithms
- Well-tested core components
