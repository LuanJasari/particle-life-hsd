import pytest
import numpy as np
from particles import ParticleSystem


def test_initialization_shapes():
    """Prüft, ob alle Arrays mit der richtigen Form (Shape) erstellt werden."""
    n_particles = 100
    n_types = 4
    system = ParticleSystem(n_particles, n_types)

    # 1. Attribute prüfen
    assert system.n_particles == n_particles
    assert system.n_types == n_types

    # 2. Array Shapes prüfen (N x 2 für Vektoren, N für Typen)
    assert system.positions.shape == (n_particles, 2)
    assert system.velocities.shape == (n_particles, 2)
    assert system.accelerations.shape == (n_particles, 2)
    assert system.types.shape == (n_particles,)


def test_value_ranges():
    """Prüft, ob die Startwerte physikalisch sinnvoll sind."""
    n_particles = 50
    n_types = 3
    system = ParticleSystem(n_particles, n_types)

    # Positionen müssen zwischen 0.0 und 1.0 liegen
    assert np.all(system.positions >= 0.0)
    assert np.all(system.positions <= 1.0)

    # Typen müssen Integers zwischen 0 und n_types-1 sein
    assert np.all(system.types >= 0)
    assert np.all(system.types < n_types)

    # Datentyp-Check: Typen müssen Integers sein
    assert np.issubdtype(system.types.dtype, np.integer)


def test_initial_physics_state():
    """Prüft, ob Partikel im Stillstand starten."""
    system = ParticleSystem(10, 2)

    # Geschwindigkeit und Beschleunigung müssen am Anfang 0 sein
    assert np.all(system.velocities == 0.0)
    assert np.all(system.accelerations == 0.0)


def test_getters():
    """Prüft, ob die Getter-Methoden die korrekten Referenzen zurückgeben."""
    system = ParticleSystem(10, 2)

    assert np.array_equal(system.get_positions(), system.positions)
    assert np.array_equal(system.get_types(), system.types)