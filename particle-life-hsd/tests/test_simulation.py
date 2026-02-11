import numpy as np
import pytest
from simulation import Simulation


# --------- 1. Mocks (Simulierte Objekte für Isolation) ----------

class SimpleParticleMock:
    """Simuliert ein Partikel-System mit minimalen Attributen für den Test."""

    def __init__(self, pos, types):
        self.positions = np.array(pos, dtype=float)
        self.types = np.array(types, dtype=int)
        # N x 2 Nullen für Geschwindigkeit und Beschleunigung initialisieren
        self.velocities = np.zeros_like(self.positions)
        self.accelerations = np.zeros_like(self.positions)


class SimpleInteractionMock:
    """Gibt kontrollierte Regeln zurück, ohne die echte Interaction-Klasse zu nutzen."""

    def __init__(self, rule_value):
        self.rule_value = rule_value

    def get_rule_grid(self, types_array):
        # Gibt eine 2x2 Matrix zurück, in der überall der rule_value steht.
        # Das simuliert, dass sich alle Partikel mit dieser Stärke beeinflussen.
        return np.full((2, 2), self.rule_value)


# ----------- 2. Fixture / Setup ----------

@pytest.fixture
def basic_simulation():
    # SETUP: Zwei Partikel
    # Partikel 0 bei (0,0), Partikel 1 bei (0.5, 0) -> Abstand ist 0.5
    positions = np.array([[0.0, 0.0], [0.5, 0.0]])
    types = np.array([0, 0])  # Beide haben Typ 0

    # Parameter der Simulation
    dt = 0.1
    max_r = 1.0
    friction = 0.5

    # Mocks initialisieren
    mock_particles = SimpleParticleMock(positions, types)
    mock_interaction = SimpleInteractionMock(rule_value=1.0)  # 1.0 = Maximale Anziehung

    # Die echte Simulation-Klasse wird mit den Mocks gefüttert
    return Simulation(dt, max_r, friction, mock_particles, mock_interaction)


# ------------ 3. Tests ----------------

def test_full_simulation_step(basic_simulation):
    """Testet einen kompletten Physik-Schritt: Distanz -> Kraft -> Bewegung."""
    sim = basic_simulation

    # 1. Distanz-Prüfung
    # Abstand zwischen (0,0) und (0.5,0) muss 0.5 sein
    distances = sim.compute_distances()
    assert np.isclose(distances[0, 1], 0.5)

    # 2. Kräfte-Prüfung
    # Formel: Kraft = Regel * (1 - Distanz/max_r)
    # Erwartet: 1.0 * (1 - 0.5/1.0) = 0.5
    total_forces = sim.compute_total_forces()

    # Wir prüfen den Betrag der Kraft auf Partikel 0 (x-Richtung)
    # Ob +0.5 oder -0.5 hängt von der Implementierung der Richtung ab,
    # aber die Stärke MUSS 0.5 sein.
    assert np.isclose(abs(total_forces[0, 0]), 0.5)
    assert np.isclose(total_forces[0, 1], 0.0)  # Keine Kraft in Y-Richtung

    # 3. Kinematik-Prüfung (Bewegung)
    sim.update_accelerations()
    sim.update_velocities()
    sim.update_positions()

    # Partikel müssen sich bewegt haben (Position nicht mehr 0.0)
    assert sim.particles.positions[0, 0] != 0.0

    # Reibungs-Check:
    # Ohne Reibung wäre v_neu = a * dt.
    # Mit Reibung muss v_neu etwas kleiner sein als a * dt.
    # a = 0.5, dt = 0.1 -> a*dt = 0.05
    pure_velocity_change = 0.5 * sim.dt
    assert abs(sim.particles.velocities[0, 0]) < pure_velocity_change


def test_no_interaction_outside_max_r():
    """Testet den Randfall: Wenn Partikel zu weit weg sind, darf keine Kraft wirken."""
    max_r_small = 0.5
    # Partikel sind 1.0 entfernt (also Distanz > max_r)
    positions = np.array([[0.0, 0.0], [1.0, 0.0]])
    types = np.array([0, 0])

    mock_particles = SimpleParticleMock(positions, types)
    mock_interaction = SimpleInteractionMock(rule_value=1.0)

    # Simulation mit kleinem Radius
    sim = Simulation(0.1, max_r_small, 0.0, mock_particles, mock_interaction)

    total_forces = sim.compute_total_forces()

    # Die Kraft muss exakt 0 sein
    assert np.allclose(total_forces, np.zeros((2, 2)))