import numpy as np
from particles import ParticleSystem

def test_initialization_shapes():
    n_particles = 100
    n_types = 4
    system = ParticleSystem(n_particles, n_types)
    assert system.n_particles == n_particles
    assert system.n_types == n_types
    assert system.positions.shape == (n_particles, 2)
    assert system.velocities.shape == (n_particles, 2)
    assert system.accelerations.shape == (n_particles, 2)
    assert system.types.shape == (n_particles,)

def test_value_ranges():
    n_particles = 50
    n_types = 3
    system = ParticleSystem(n_particles, n_types)
    assert np.all(system.positions >= 0.0)
    assert np.all(system.positions <= 1.0)
    assert np.all(system.types >= 0)
    assert np.all(system.types < n_types)
    assert np.issubdtype(system.types.dtype, np.integer)

def test_initial_physics_state():
    system = ParticleSystem(10, 2)
    assert np.all(system.velocities == 0.0)
    assert np.all(system.accelerations == 0.0)

def test_getters():
    system = ParticleSystem(10, 2)
    assert np.array_equal(system.get_positions(), system.positions)
    assert np.array_equal(system.get_types(), system.types)
