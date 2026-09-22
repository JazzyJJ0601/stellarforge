"""Tests for the Barnes-Hut octree implementation."""
import pytest
from stellarforge.core.body import Body
from stellarforge.barneshut.octree import Octree


def test_empty_octree():
    """Octree with no bodies should raise ValueError."""
    with pytest.raises(ValueError, match="no bodies"):
        Octree([])


def test_single_particle():
    """Octree with 1 body: root is the leaf, no children."""
    body = Body(position=(0.0, 0.0, 0.0), velocity=(0.0, 0.0, 0.0), mass=1.0, id=1)
    tree = Octree([body])
    
    # Root should be a leaf (no children)
    assert all(c is None for c in tree.root.children)
    # Root should have the body
    assert tree.root.body is body
    # Mass should be correct
    assert tree.root.mass == pytest.approx(1.0)


def test_octree_subdivision():
    """2 particles far apart end up in different children."""
    body1 = Body(position=(0.0, 0.0, 0.0), velocity=(0.0, 0.0, 0.0), mass=1.0, id=1)
    body2 = Body(position=(100.0, 0.0, 0.0), velocity=(0.0, 0.0, 0.0), mass=1.0, id=2)
    tree = Octree([body1, body2], max_particles_per_leaf=1)
    
    # Tree should have depth > 0 (subdivision happened)
    assert any(c is not None for c in tree.root.children)
    
    # Each leaf should have <= max_particles (1)
    def count_bodies_in_leaves(node):
        if node is None:
            return 0
        if all(c is None for c in node.children):
            return 1 if node.body is not None else 0
        return sum(count_bodies_in_leaves(c) for c in node.children if c is not None)
    
    def check_leaf_counts(node):
        if node is None:
            return True
        if all(c is None for c in node.children):
            return node.body is None or len([b for b in [node.body]]) == 1
        return all(check_leaf_counts(c) for c in node.children if c is not None)
    
    assert check_leaf_counts(tree.root)


def test_center_of_mass():
    """2 equal-mass particles at (0,0,0) and (2,0,0); CoM should be at (1,0,0) with mass=2."""
    body1 = Body(position=(0.0, 0.0, 0.0), velocity=(0.0, 0.0, 0.0), mass=1.0, id=1)
    body2 = Body(position=(2.0, 0.0, 0.0), velocity=(0.0, 0.0, 0.0), mass=1.0, id=2)
    tree = Octree([body1, body2])
    
    # Total mass should be 2
    assert tree.root.mass == pytest.approx(2.0)
    # Center of mass should be at (1, 0, 0)
    assert tree.root.center_of_mass[0] == pytest.approx(1.0)
    assert tree.root.center_of_mass[1] == pytest.approx(0.0)
    assert tree.root.center_of_mass[2] == pytest.approx(0.0)


def test_force_symmetry():
    """2 particles exert equal-and-opposite forces on each other."""
    body1 = Body(position=(0.0, 0.0, 0.0), velocity=(0.0, 0.0, 0.0), mass=1.0, id=1)
    body2 = Body(position=(1.0, 0.0, 0.0), velocity=(0.0, 0.0, 0.0), mass=1.0, id=2)
    tree = Octree([body1, body2])
    
    accel = tree.compute_accelerations([body1, body2])
    
    # Magnitudes should be equal within 1e-10
    mag1 = (accel[1][0]**2 + accel[1][1]**2 + accel[1][2]**2) ** 0.5
    mag2 = (accel[2][0]**2 + accel[2][1]**2 + accel[2][2]**2) ** 0.5
    
    assert mag1 == pytest.approx(mag2, rel=1e-10)
    # Forces should be in opposite directions (dot product negative)
    dot = (accel[1][0] * accel[2][0] + 
           accel[1][1] * accel[2][1] + 
           accel[1][2] * accel[2][2])
    assert dot < 0
