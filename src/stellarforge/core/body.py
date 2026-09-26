from dataclasses import dataclass


@dataclass
class Body:
    position: tuple[float, float, float]
    velocity: tuple[float, float, float]
    mass: float
    id: int

    def __repr__(self):
        return f"Body(id={self.id}, mass={self.mass}, position={self.position})"
