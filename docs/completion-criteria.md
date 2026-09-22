# stellarforge — Completion Criteria

This file defines specific, measurable, and automatically verifiable completion criteria for the stellarforge gravitational N-body simulation engine. Each criterion includes a shell command that an automated agent can run to verify it. All criteria are ordered by phase; earlier phases must hold before later ones are meaningful.

## Verification convention

- `run_tests.sh` returns exit 0 = all tests pass, non-zero = failure.
- `benchmarks/run.sh` returns exit 0 = all benchmarks complete, outputs scores to stdout.
- `demo/run.sh` returns exit 0 = demo produces expected output without error.
- All paths are relative to the repository root.

---

## Phase 0 — Infrastructure

| # | Criterion | Verify command |
|---|-----------|----------------|
| 0.1 | Repository has a `pyproject.toml` defining the `stellarforge` package with build metadata | `test -f pyproject.toml && grep -q 'name = "stellarforge"' pyproject.toml` |
| 0.2 | Package installs from source (editable or regular) | `pip install -e . 2>&1 && python -c "import stellarforge; print(stellarforge.__version__)"` |
| 0.3 | A `run_tests.sh` script exists and is executable, runs the full test suite, and returns exit 0 | `test -x run_tests.sh && bash run_tests.sh` |
| 0.4 | All existing tests pass with exit code 0 | `python -m pytest tests/ -v --tb=short 2>&1` — must show all passed |
| 0.5 | Poetry / pip xdev dependencies (pytest, numpy) are declared | `grep -q 'pytest' pyproject.toml && grep -q 'numpy' pyproject.toml` |
| 0.6 | `.gitignore` ignores `__pycache__/`, `*.pyc`, `.venv/`, `*.egg-info/` | `grep -q '__pycache__' .gitignore && grep -q '*.egg-info' .gitignore` |

---

## Phase 1 — Algorithm correctness (Barnes-Hut octree)

| # | Criterion | Verify command |
|---|-----------|----------------|
| 1.1 | Octree constructed from 1 particle: root is a leaf with no children, body assigned, mass equals particle mass | `python -c "from stellarforge import Body, Octree; b=Body(id=0,mass=5.0,position=(0,0,0),velocity=(0,0,0)); t=Octree([b]); assert all(c is None for c in t.root.children); assert t.root.body is b; assert abs(t.root.mass - 5.0) < 1e-15"` |
| 1.2 | Octree rejects empty body list with ValueError | `python -c "from stellarforge import Octree; Octree([])" 2>&1 | grep -q 'no bodies'` |
| 1.3 | Octree subdivides: 2 particles far apart end up in different child octants | `python -c "from stellarforge import Body, Octree; b1=Body(id=0,mass=1,position=(0,0,0),velocity=(0,0,0)); b2=Body(id=1,mass=1,position=(100,0,0),velocity=(0,0,0)); t=Octree([b1,b2],max_particles_per_leaf=1); assert any(c is not None for c in t.root.children), 'no subdivision'"` |
| 1.4 | Center-of-mass computed correctly: 2 equal-mass bodies at (0,0,0) and (2,0,0) give CoM at (1,0,0) with total mass 2.0 | `python -c "from stellarforge import Body, Octree; b1=Body(id=0,mass=1,position=(0,0,0),velocity=(0,0,0)); b2=Body(id=1,mass=1,position=(2,0,0),velocity=(0,0,0)); t=Octree([b1,b2]); assert abs(t.root.mass - 2.0) < 1e-15; assert abs(t.root.center_of_mass[0] - 1.0) < 1e-15; assert abs(t.root.center_of_mass[1]) < 1e-15; assert abs(t.root.center_of_mass[2]) < 1e-15; print('CoM OK')"` |
| 1.5 | Brute-force direct-sum acceleration produces equal-and-opposite forces for 2 particles within 1e-10 relative | `python -c "from stellarforge import Body; from stellarforge.barneshut.octree import brute_force_accelerations; b1=Body(id=0,mass=1,position=(0,0,0),velocity=(0,0,0)); b2=Body(id=1,mass=1,position=(1,0,0),velocity=(0,0,0)); a=brute_force_accelerations([b1,b2]); m0=sum(v**2 for v in a[0])**0.5; m1=sum(v**2 for v in a[1])**0.5; assert abs(m0-m1)/m0 < 1e-10; assert a[0][0]*a[1][0] < 0; print('Force symmetry OK')"` |

---

## Phase 2 — Accuracy and physics validation

| # | Criterion | Verify command |
|---|-----------|----------------|
| 2.1 | BH accuracy: θ=0.5, N=100 — 90th percentile relative force error < 5% | `python -m pytest tests/test_accuracy.py::TestBHAccuracy::test_bh_theta_0_5_n100 -x --tb=short 2>&1` — must show PASSED |
| 2.2 | BH accuracy: θ=0.25, N=100 — 90th percentile relative force error < 1% | `python -m pytest tests/test_accuracy.py::TestBHAccuracy::test_bh_theta_0_25_n100 -x --tb=short 2>&1` — PASSED |
| 2.3 | BH accuracy: θ=0.1, N=100 — 90th percentile relative force error < 0.3% | `python -m pytest tests/test_accuracy.py::TestBHAccuracy::test_bh_theta_0_1_n100 -x --tb=short 2>&1` — PASSED |
| 2.4 | BH accuracy: θ=0.5, N=1000 — 90th percentile error < 10% | `python -m pytest tests/test_accuracy.py::TestBHAccuracy::test_bh_theta_0_5_n1000 -x --tb=short 2>&1` — PASSED |
| 2.5 | BH accuracy: θ=0.25, N=1000 — 90th percentile error < 1% | `python -m pytest tests/test_accuracy.py::TestBHAccuracy::test_bh_theta_0_25_n1000 -x --tb=short 2>&1` — PASSED |
| 2.6 | Tighter θ (0.1) yields strictly better accuracy than looser θ (0.5) | `python -m pytest tests/test_accuracy.py::TestBHAccuracy::test_tighter_theta_improves_accuracy -x --tb=short 2>&1` — PASSED |
| 2.7 | Single-body: body at rest stays at rest after one integrator step | `python -m pytest tests/test_integrator.py::test_single_body_at_rest -x --tb=short 2>&1` — PASSED |
| 2.8 | Two-body circular orbit: energy drift < 2% over 200 steps, bodies remain bound | `python -m pytest tests/test_integrator.py::test_two_body_circular_orbit_energy -x --tb=short 2>&1` — PASSED |
| 2.9 | Three-body system: energy drift < 0.5% over 1000 steps | `python -m pytest tests/test_integrator.py::test_energy_conservation_three_body -x --tb=short 2>&1` — PASSED |

---

## Phase 3 — CLI and usability

| # | Criterion | Verify command |
|---|-----------|----------------|
| 3.1 | CLI entry point `stellarforge` is installed and invocable | `which stellarforge && stellarforge --help 2>&1 | grep -q 'usage'` |
| 3.2 | CLI accepts `--n-bodies N`, `--dt TIMESTEP`, `--steps STEPS` parameters | `stellarforge --help 2>&1 | grep -q '--n-bodies' && stellarforge --help 2>&1 | grep -q '--dt' && stellarforge --help 2>&1 | grep -q '--steps'` |
| 3.3 | CLI produces snapshot output files at configurable intervals (`--output-dir`, `--snap-interval`) | `stellarforge --help 2>&1 | grep -q '--output-dir' && stellarforge --help 2>&1 | grep -q '--snap-interval'` |
| 3.4 | A short CLI simulation (N=16, dt=0.01, steps=100) runs without error and produces output files | `stellarforge --n-bodies 16 --dt 0.01 --steps 100 --output-dir /tmp/stf-test-1 --snap-interval 10 2>&1 && ls /tmp/stf-test-1/snap*.csv 2>/dev/null | grep -q . && rm -rf /tmp/stf-test-1` |
| 3.5 | CLI accepts `--theta` opening-angle parameter | `stellarforge --help 2>&1 | grep -q '\--theta'` |
| 3.6 | CLI accepts `--seed` for reproducible random initial conditions | `stellarforge --help 2>&1 | grep -q '\--seed'` |
| 3.7 | CLI shows energy diagnostics (total KE, PE, ETot) on stdout per step or at end | `stellarforge --n-bodies 8 --dt 0.01 --steps 10 --seed 42 2>&1 | grep -qi 'energy'` |

---

## Phase 4 — Benchmarks

| # | Criterion | Verify command |
|---|-----------|----------------|
| 4.1 | `benchmarks/` directory exists with a `README.md` and at least one runnable benchmark script | `test -d benchmarks && test -f benchmarks/README.md && ls benchmarks/*.py benchmarks/*.sh 2>/dev/null | grep -q .` |
| 4.2 | Benchmark script runs without error and prints timing/speed results | `bash benchmarks/run.sh 2>&1 | head -20` — must show timing data |
| 4.3 | BH vs direct-sum speed comparison benchmark exists (measures ratio of wall-clock times) | `grep -qi 'direct' benchmarks/run.sh || grep -qi 'bh_bench' benchmarks/*.py 2>/dev/null` |
| 4.4 | Benchmark records: BH 1024-body force calc is at least 5× faster than direct O(n²) at θ=0.5 | `bash benchmarks/run.sh 2>&1 | grep -qi 'speedup'` or quantitative output showing ratio ≥ 5 |
| 4.5 | N=4096 benchmark completes within timeout (no runaway) | `timeout 120 bash benchmarks/run.sh 2>&1` — exit 0 |

---

## Phase 5 — Demo

| # | Criterion | Verify command |
|---|-----------|----------------|
| 5.1 | `demo/` directory exists with `README.md` and at least one runnable demo script | `test -d demo && test -f demo/README.md && ls demo/*.py demo/*.sh 2>/dev/null | grep -q .` |
| 5.2 | Demo script runs without error | `bash demo/run.sh 2>&1` — exit 0 |
| 5.3 | Demo produces visual output (PNG/MP4/HTML frames) or CSV snapshot files | `ls demo/output/*.csv demo/output/*.png demo/output/*.mp4 2>/dev/null | grep -q .` |
| 5.4 | Demo README describes setup, invocation, and expected output in ≤5 steps | `grep -q 'setup' demo/README.md && grep -q 'invocation\|run\|usage' demo/README.md && grep -q 'expected\|example\|sample' demo/README.md` |

---

## Phase 6 — Documentation

| # | Criterion | Verify command |
|---|-----------|----------------|
| 6.1 | `README.md` exists at repo root with project overview, setup, usage, and roadmap sections | `test -f README.md && grep -q 'setup\|install' README.md && grep -q 'usage\|example\|demo' README.md && grep -q 'roadmap\|todo\|planned' README.md` |
| 6.2 | `docs/architecture.md` describes the module structure and data flow | `test -f docs/architecture.md && grep -q 'octree\|barneshut\|integrator\|body' docs/architecture.md` |
| 6.3 | `docs/design-decisions.md` documents key choices and trade-offs | `test -f docs/design-decisions.md && grep -q 'choice\|trade-off\|decision' docs/design-decisions.md` |
| 6.4 | `LICENSE` file exists (MIT or Apache 2.0) | `test -f LICENSE && (head -1 LICENSE | grep -qi 'MIT' || head -1 LICENSE | grep -qi 'Apache')` |
| 6.5 | `docs/verification.md` documents clean-install verification steps and results | `test -f docs/verification.md && grep -q 'clean\|fresh\|pip install' docs/verification.md` |
| 6.6 | `CHANGELOG.md` exists with at least one version entry | `test -f CHANGELOG.md && grep -q 'v\|## \[0\.' CHANGELOG.md` |

---

## Phase 7 — Clean-install verification

| # | Criterion | Verify command |
|---|-----------|----------------|
| 7.1 | Package installs cleanly in a fresh virtual environment | `cd /tmp && python3 -m venv stf-verify && source stf-verify/bin/activate && pip install -e /home/jasper/eirene-projects/04-forge 2>&1 && python -c 'import stellarforge; print(\"OK\")' && deactivate && rm -rf stf-verify` — prints "OK" |
| 7.2 | All tests pass from a clean install | (same venv setup) `python -m pytest /home/jasper/eirene-projects/04-forge/tests/ -v --tb=short 2>&1` — all passed |
| 7.3 | Demo runs from a clean install | (same venv setup) `bash /home/jasper/eirene-projects/04-forge/demo/run.sh 2>&1` — exit 0 |

---

## Phase 8 — Release readiness

| # | Criterion | Verify command |
|---|-----------|----------------|
| 8.1 | Git commit history is clean: no merge commits, no WIP messages | `git log --oneline --no-merges | head -10` — messages are descriptive, not "wip", "fix", "temp" |
| 8.2 | A version tag exists (e.g., `v1.0.0`) | `git tag | grep -q 'v'` |
| 8.3 | `CHANGELOG.md` is accurate against `git log` (no fabricated entries) | `grep -q '^## \[' CHANGELOG.md && grep -q 'Added\|Fixed\|Changed' CHANGELOG.md` |
| 8.4 | Publication request `docs/publication-request.md` exists and asks Jasper for approval | `test -f docs/publication-request.md && grep -q 'approval\|publish' docs/publication-request.md` |

---

## Master verification script

The single command `bash verify-all.sh` (or equivalently `bash run_tests.sh && bash benchmarks/run.sh && bash demo/run.sh`) must return exit 0, confirming all Phase 0–3 criteria are met. Phase 4–8 are verified per-phase with the individual commands above.

When every criterion above reports PASS, the project is ready for Jasper's publication review.