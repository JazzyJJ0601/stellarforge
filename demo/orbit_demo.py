#!/usr/bin/env python3
"""Two-body circular orbit simulation using stellarforge."""

import csv
import math
import os
import sys

# Add project root to path for importing stellarforge
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stellarforge import Body, LeapfrogIntegrator


def compute_energy(bodies: list[Body], G: float = 1.0) -> float:
    """Compute total energy (kinetic + potential) of the system."""
    kinetic = 0.0
    for b in bodies:
        v2 = b.velocity[0]**2 + b.velocity[1]**2 + b.velocity[2]**2
        kinetic += 0.5 * b.mass * v2
    
    potential = 0.0
    n = len(bodies)
    for i in range(n):
        for j in range(i + 1, n):
            dx = bodies[i].position[0] - bodies[j].position[0]
            dy = bodies[i].position[1] - bodies[j].position[1]
            dz = bodies[i].position[2] - bodies[j].position[2]
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            potential -= G * bodies[i].mass * bodies[j].mass / dist
    
    return kinetic + potential


def compute_separation(bodies: list[Body]) -> float:
    """Compute distance between two bodies."""
    if len(bodies) != 2:
        return 0.0
    dx = bodies[0].position[0] - bodies[1].position[0]
    dy = bodies[0].position[1] - bodies[1].position[1]
    dz = bodies[0].position[2] - bodies[1].position[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)


def are_bodies_bound(bodies: list[Body], G: float = 1.0) -> bool:
    """Check if the two-body system is gravitationally bound (total energy < 0)."""
    return compute_energy(bodies, G) < 0


def write_snapshot(bodies: list[Body], filepath: str) -> None:
    """Write body states to a CSV file."""
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'mass', 'px', 'py', 'pz', 'vx', 'vy', 'vz'])
        for b in bodies:
            writer.writerow([
                b.id, b.mass,
                b.position[0], b.position[1], b.position[2],
                b.velocity[0], b.velocity[1], b.velocity[2]
            ])


def main():
    # Parameters
    G = 1.0
    mass = 1.0
    separation = 2.0  # Distance between bodies
    radius = separation / 2.0  # Distance from center of mass
    dt = 0.01
    total_steps = 500
    snapshot_interval = 50
    
    # For a two-body circular orbit with equal masses:
    # Each body orbits at distance radius from COM
    # Gravitational force = G*m*m / separation^2
    # Centripetal force needed = m*v^2 / radius
    # Setting equal: G*m^2 / separation^2 = m*v^2 / radius
    # v = sqrt(G*m*radius / separation^2) = sqrt(G*m / (4*radius))
    # With G=1, m=1, radius=1: v = sqrt(0.25) = 0.5
    v_mag = math.sqrt(G * mass / (4.0 * radius))
    
    # Initial positions: symmetric about origin on x-axis
    body0 = Body(
        position=(-radius, 0.0, 0.0),
        velocity=(0.0, v_mag, 0.0),
        mass=mass,
        id=0
    )
    body1 = Body(
        position=(radius, 0.0, 0.0),
        velocity=(0.0, -v_mag, 0.0),
        mass=mass,
        id=1
    )
    bodies = [body0, body1]
    
    # Initial energy
    initial_energy = compute_energy(bodies, G)
    
    # Run simulation
    integrator = LeapfrogIntegrator()
    snapshot_count = 0
    
    for step in range(total_steps):
        # Take a step
        bodies = integrator.step(bodies, dt, G=G)
        
        # Write snapshot every snapshot_interval steps
        if (step + 1) % snapshot_interval == 0:
            snapshot_path = os.path.join(
                os.path.dirname(__file__),
                'output',
                f'snap_{snapshot_count:06d}.csv'
            )
            write_snapshot(bodies, snapshot_path)
            snapshot_count += 1
    
    # Compute final metrics
    final_energy = compute_energy(bodies, G)
    energy_drift_pct = abs(final_energy - initial_energy) / abs(initial_energy) * 100 if initial_energy != 0 else 0.0
    final_sep = compute_separation(bodies)
    bound = are_bodies_bound(bodies, G)
    
    # Print summary
    print("=== Simulation Summary ===")
    print(f"Total steps: {total_steps}")
    print(f"Energy drift: {energy_drift_pct:.4f}%")
    print(f"Final separation: {final_sep:.6f}")
    print(f"Bodies remain bound: {bound}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
