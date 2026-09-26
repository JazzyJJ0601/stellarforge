# StellarForge Demo

Two-body circular orbit simulation using the Leapfrog integrator.

## How to Run

```bash
cd /home/jasper/eirene-projects/04-forge && .venv/bin/python demo/orbit_demo.py
```

## What It Does

- Simulates two equal-mass bodies in a Keplerian circular orbit
- Runs for 500 steps with time step dt=0.01
- Writes CSV snapshots every 50 steps (10 total) to `demo/output/`

## Expected Output

- Energy drift < 2%
- Bodies remain bound throughout simulation
- 10 snapshot files created in `demo/output/`

## How to Inspect Results

```bash
cat demo/output/snap_*.csv | head -3
```

Each CSV contains columns: `id,mass,px,py,pz,vx,vy,vz`
