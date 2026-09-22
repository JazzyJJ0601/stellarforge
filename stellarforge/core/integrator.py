from abc import ABC, abstractmethod
from typing import Protocol
from .body import Body


class Integrator(Protocol):
    """Protocol for time integration of N-body systems."""

    def step(self, bodies: list[Body], dt: float) -> list[Body]:
        """Advance the system by dt."""
        ...


class LeapfrogIntegrator:
    """Leapfrog integrator using kick-drift-kick scheme."""

    def step(self, bodies: list[Body], dt: float) -> list[Body]:
        """Advance the system by dt using kick-drift-kick."""
        n = len(bodies)
        if n == 0:
            return bodies

        # Compute accelerations using direct sum O(n²)
        accel = [(0.0, 0.0, 0.0) for _ in range(n)]
        G = 1.0

        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dx = bodies[j].position[0] - bodies[i].position[0]
                dy = bodies[j].position[1] - bodies[i].position[1]
                dz = bodies[j].position[2] - bodies[i].position[2]
                dist_sq = dx * dx + dy * dy + dz * dz
                force = G * bodies[j].mass / (dist_sq ** 1.5)
                accel[i] = (
                    accel[i][0] + dx * force,
                    accel[i][1] + dy * force,
                    accel[i][2] + dz * force,
                )

        # Kick-drift-kick
        dt2 = dt / 2
        for i, b in enumerate(bodies):
            # Kick 1
            vx = b.velocity[0] + accel[i][0] * dt2
            vy = b.velocity[1] + accel[i][1] * dt2
            vz = b.velocity[2] + accel[i][2] * dt2
            # Drift
            px = b.position[0] + vx * dt
            py = b.position[1] + vy * dt
            pz = b.position[2] + vz * dt
            # Kick 2
            b.velocity = (
                vx + accel[i][0] * dt2,
                vy + accel[i][1] * dt2,
                vz + accel[i][2] * dt2,
            )
            b.position = (px, py, pz)

        return bodies
