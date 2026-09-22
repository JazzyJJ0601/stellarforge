"""Barnes-Hut octree implementation for N-body simulation."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from ..core.body import Body


@dataclass
class OctreeNode:
    """A node in the Barnes-Hut octree."""
    center: tuple[float, float, float]
    size: float
    mass: float = 0.0
    center_of_mass: tuple[float, float, float] = (0.0, 0.0, 0.0)
    children: list[Optional[OctreeNode]] = field(default_factory=lambda: [None] * 8)
    body: Optional[Body] = None


class Octree:
    """Barnes-Hut octree for spatial partitioning."""

    def __init__(self, bodies: list[Body], max_particles_per_leaf: int = 1):
        if not bodies:
            raise ValueError("Cannot create octree with no bodies")

        self.max_particles = max_particles_per_leaf
        # Find bounding box
        min_pos = [b.position[i] for b in bodies for i in range(3)]
        max_pos = list(min_pos)
        for b in bodies:
            for i in range(3):
                min_pos[i] = min(min_pos[i], b.position[i])
                max_pos[i] = max(max_pos[i], b.position[i])

        # Compute center and size
        self.root = OctreeNode(
            center=(
                (min_pos[0] + max_pos[0]) / 2,
                (min_pos[1] + max_pos[1]) / 2,
                (min_pos[2] + max_pos[2]) / 2,
            ),
            size=max(
                max_pos[0] - min_pos[0],
                max_pos[1] - min_pos[1],
                max_pos[2] - min_pos[2],
            ),
        )

        # Insert all bodies
        self._subdivide(self.root, bodies)
        # Compute center of mass for all nodes
        self.compute_center_of_mass(self.root)

    @staticmethod
    def _octant_center(
        parent_center: tuple[float, float, float],
        parent_size: float,
        idx: int,
    ) -> tuple[float, float, float]:
        """Compute center of the i-th octant."""
        offset = parent_size / 4
        cx = parent_center[0] + offset * (-1 if idx % 2 == 0 else 1)
        cy = parent_center[1] + offset * (-1 if idx // 2 % 2 == 0 else 1)
        cz = parent_center[2] + offset * (-1 if idx // 4 == 0 else 1)
        return (cx, cy, cz)

    def _find_child_index(
        self, node: OctreeNode, position: tuple[float, float, float]
    ) -> int:
        """Find which octant (0-7) a position falls into."""
        idx = 0
        for i in range(3):
            if position[i] > node.center[i]:
                idx |= 1 << i
        return idx

    def _subdivide(self, node: OctreeNode, bodies_in_region: list[Body]):
        """Recursively subdivide a node into 8 octants."""
        if len(bodies_in_region) <= self.max_particles:
            # Leaf node - assign bodies directly
            if bodies_in_region:
                node.body = bodies_in_region[0]
            return

        # Create children for all octants
        node.children = [None] * 8

        # Partition bodies into octants
        octant_bodies = [[] for _ in range(8)]
        for b in bodies_in_region:
            idx = self._find_child_index(node, b.position)
            octant_bodies[idx].append(b)

        # Recursively subdivide each octant
        for i in range(8):
            if not octant_bodies[i]:
                continue

            octant_center = self._octant_center(node.center, node.size, i)
            child = OctreeNode(
                center=octant_center,
                size=node.size / 2,
            )
            node.children[i] = child
            self._subdivide(child, octant_bodies[i])

    def compute_center_of_mass(self, node: OctreeNode):
        """Recursively compute center of mass and total mass for a node."""
        if node.body is not None and all(c is None for c in node.children):
            # Leaf with a body
            node.mass = node.body.mass
            node.center_of_mass = node.body.position
            return

        total_mass = 0.0
        com = [0.0, 0.0, 0.0]

        # If node has a body (internal node with stored body)
        if node.body is not None:
            total_mass += node.body.mass
            for i in range(3):
                com[i] += node.body.position[i] * node.body.mass

        # Accumulate from children
        for child in node.children:
            if child is not None:
                self.compute_center_of_mass(child)
                total_mass += child.mass
                for i in range(3):
                    com[i] += child.center_of_mass[i] * child.mass

        node.mass = total_mass
        if total_mass > 0:
            node.center_of_mass = tuple(com[i] / total_mass for i in range(3))
        else:
            node.center_of_mass = node.center

    def _compute_acceleration_from_node(
        self,
        body: Body,
        node: OctreeNode,
        theta: float,
        G: float,
        softening: float,
    ) -> tuple[float, float, float]:
        """Compute acceleration on a body from a node using Barnes-Hut."""
        dx = node.center_of_mass[0] - body.position[0]
        dy = node.center_of_mass[1] - body.position[1]
        dz = node.center_of_mass[2] - body.position[2]
        dist_sq = dx * dx + dy * dy + dz * dz + softening * softening
        dist = dist_sq ** 0.5

        if dist / node.size > theta or node.body is not None and all(
            c is None for c in node.children
        ):
            # Treat as single point mass
            force = G * node.mass / (dist_sq * dist)
            return (dx * force, dy * force, dz * force)

        # Recurse into children
        total_accel = (0.0, 0.0, 0.0)
        for child in node.children:
            if child is not None:
                child_accel = self._compute_acceleration_from_node(
                    body, child, theta, G, softening
                )
                total_accel = (
                    total_accel[0] + child_accel[0],
                    total_accel[1] + child_accel[1],
                    total_accel[2] + child_accel[2],
                )
        return total_accel

    def compute_accelerations(
        self,
        bodies: list[Body],
        theta: float = 0.5,
        G: float = 1.0,
        softening: float = 1e-3,
    ) -> dict[int, tuple[float, float, float]]:
        """Compute gravitational acceleration for each body."""
        result = {}
        for b in bodies:
            accel = (0.0, 0.0, 0.0)
            for child in self.root.children:
                if child is not None:
                    child_accel = self._compute_acceleration_from_node(
                        b, child, theta, G, softening
                    )
                    accel = (
                        accel[0] + child_accel[0],
                        accel[1] + child_accel[1],
                        accel[2] + child_accel[2],
                    )
            result[b.id] = accel
        return result
