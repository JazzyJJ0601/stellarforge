# Publication Request: stellarforge

## Project Summary

**stellarforge** is a gravitational N-body simulation engine implementing the Barnes-Hut O(n log n) tree algorithm — the same algorithmic approach that enabled the first large-scale cosmological simulations. It is written in pure Python (no external runtime dependencies) and is the flagship reputation project within Project Forge (the user's technical credibility portfolio).

## What exists

- **Algorithm**: Correct Barnes-Hut octree with configurable theta opening angle, gravitational softening, and center-of-mass aggregation
- **Integration**: Symplectic leapfrog kick-drift-kick integrator with verified long-term energy stability
- **Validation**: Brute-force O(n²) reference implementation — BH accuracy measured to <5% P90 error at θ=0.5, <1% at θ=0.25
- **Tests**: 14 passing tests covering octree structure, force Newton-pair symmetry (1e-10), accuracy bounds, and energy conservation (two-body <2% drift over 200 steps, three-body <0.5% over 1000 steps)
- **Benchmarks**: BH vs direct-sum speed comparison at N=128–1024, showing ~1.8× speedup at N=1024 in pure Python
- **Demo**: Two-body circular orbit simulation with CSV snapshot output and verified 1.24% energy drift over 500 steps
- **Docs**: README, architecture.md, design-decisions.md, completion-criteria.md, CHANGELOG, MIT License

## Repository

**URL**: https://github.com/JazzyJJ0601/stellarforge (currently private)
**Branch**: master
**Tag**: v1.0.0
**Commits**: 11 clean, descriptive commits

## Quality evidence

- Clean setup verified (clone → venv → install → all tests pass → benchmarks run → demo runs)
- All 14 tests pass deterministically (seeded random)
- Code reviewed — no bugs found
- Design decisions documented with trade-offs explicitly stated
- No external API calls, no dependencies beyond Python stdlib (pytest and numpy optional for dev)

## Request

I am asking for your explicit approval to make this repository **public** on GitHub. I will not publish it without your say-so.

**Once approved**, the action is: `gh repo edit JazzyJJ0601/stellarforge --visibility public`

---

**Published**: 26 September 2026, by Jasper's approval. Repository is now public at https://github.com/JazzyJJ0601/stellarforge.