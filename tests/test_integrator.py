import pytest
import math
from stellarforge.core.body import Body
from stellarforge.core.integrator import LeapfrogIntegrator


def test_single_body_at_rest():
    """A single body with zero velocity stays at rest after one step."""
    body = Body(id=0, mass=1.0, position=(0.0, 0.0, 0.0), velocity=(0.0, 0.0, 0.0))
    initial_pos = body.position
    initial_vel = body.velocity
    
    integrator = LeapfrogIntegrator()
    result = integrator.step([body], dt=0.01)
    
    # Single body has no forces, should stay exactly the same
    assert result[0].position == initial_pos
    assert result[0].velocity == initial_vel


def two_two_body_circular_orbit_energy():
    """Two equal-mass bodies in circular orbit stay bound with minimal energy drift."""
    G = 1.0
    M = 1.0
    R = 2.0  # separation
    v = math.sqrt(G * M / (2 * R))  # circular orbit velocity = 0.5
    
    body1 = Body(
        id=0,
        mass=M,
        position=(-R/2, 0.0, 0.0),
        velocity=(0.0, v, 0.0)
    )
    body2 = Body(
        id=1,
        mass=M,
        position=(R/2, 0.0, 0.0),
        velocity=(0.0, -v, 0.0)
    )
    
    initial_separation = math.sqrt(
        (body2.position[0] - body1.position[0])**2 +
        (body2.position[1] - body1.position[1])**2 +
        (body2.position[2] - body1.position[2])**2
    )
    
    def compute_energy(bodies):
        # Kinetic energy
        KE = 0.5 * sum(b.mass * sum(v**2 for v in b.velocity) for b in bodies)
        # Potential energy
        PE = 0.0
        for i in range(len(bodies)):
            for j in range(i+1, len(bodies)):
                dx = bodies[i].position[0] - bodies[j].position[0]
                dy = bodies[i].position[1] - bodies[j].position[1]
                dz = bodies[i].position[2] - bodies[j].position[2]
                dist = math.sqrt(dx**2 + dy**2 + dz**2)
                PE -= G * bodies[i].mass * bodies[j].mass / dist
        return KE + PE
    
    integrator = LeapfrogIntegrator()
    bodies = [body1, body2]
    initial_energy = compute_energy(bodies)
    
    dt = 0.01
    for _ in range(500):
        integrator.step(bodies, dt=dt)
    
    final_energy = compute_energy(bodies)
    energy_drift = abs(final_energy - initial_energy) / abs(initial_energy)
    
    final_separation = math.sqrt(
        (bodies[1].position[0] - bodies[0].position[0])**2 +
        (bodies[1].position[1] - bodies[0].position[1])**2 +
        (bodies[1].position[2] - bodies[0].position[2])**2
    )
    
    # Energy drift should be < 1%
    assert energy_drift < 0.01, f"Energy drift {energy_drift:.4f} >= 1%"
    # Bodies should remain bound (separation < 2x initial)
    assert final_separation < 2 * initial_separation, f"Separation {final_separation:.4f} >= 2x initial"


def test_energy_conservation_three_body():
    """Three-body system conserves energy within 0.5% over 1000 steps."""
    import random
    random.seed(123)
    
    G = 1.0
    bodies = []
    for i in range(3):
        pos = (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10))
        vel = (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        bodies.append(Body(id=i, mass=random.uniform(0.5, 2.0), position=pos, velocity=vel))
    
    def compute_energy(bodies):
        KE = 0.5 * sum(b.mass * sum(v**2 for v in b.velocity) for b in bodies)
        PE = 0.0
        for i in range(len(bodies)):
            for j in range(i+1, len(bodies)):
                dx = bodies[i].position[0] - bodies[j].position[0]
                dy = bodies[i].position[1] - bodies[j].position[1]
                dz = bodies[i].position[2] - bodies[j].position[2]
                dist = math.sqrt(dx**2 + dy**2 + dz**2)
                PE -= G * bodies[i].mass * bodies[j].mass / dist
        return KE + PE
    
    integrator = LeapfrogIntegrator()
    initial_energy = compute_energy(bodies)
    
    dt = 0.001
    for _ in range(1000):
        integrator.step(bodies, dt=dt)
    
    final_energy = compute_energy(bodies)
    energy_drift = abs(final_energy - initial_energy) / abs(initial_energy)
    
    assert energy_drift < 0.005, f"Energy drift {energy_drift:.4f} >= 0.5%"
