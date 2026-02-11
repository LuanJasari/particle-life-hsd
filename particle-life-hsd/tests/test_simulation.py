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
        # Hinweis: 'accelerations' wird in der Numba-Version technisch nicht mehr gespeichert,
        # aber wir behalten es im Mock, falls alter Code darauf zugreift.
        self.accelerations = np.zeros_like(self.positions)

    # Für Numba-Kompatibilität: Properties, falls nötig
    def __len__(self):
        return len(self.positions)


class SimpleInteractionMock:
    """Gibt kontrollierte Regeln zurück."""

    def __init__(self, rule_value, n_types=2):
        self.rule_value = rule_value
        # FIX: Die Numba-Simulation greift DIREKT auf .matrix zu.
        # Wir müssen also eine NxN Matrix bereitstellen.
        self.matrix = np.full((n_types, n_types), self.rule_value, dtype=float)

    def get_rule_grid(self, types_array):
        # Legacy-Support, falls noch benötigt
        return np.full((len(types_array), len(types_array)), self.rule_value)


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

    # WICHTIG: Noise auf 0.0 setzen für deterministische Tests!
    noise = 0.0

    # Mocks initialisieren
    mock_particles = SimpleParticleMock(positions, types)
    # 1.0 = Maximale Anziehung
    mock_interaction = SimpleInteractionMock(rule_value=1.0, n_types=1)

    # Die echte Simulation-Klasse wird mit den Mocks gefüttert
    return Simulation(dt, max_r, friction, noise, mock_particles, mock_interaction)


# ------------ 3. Tests ----------------

def test_simulation_integration(basic_simulation):
    """
    Testet, ob die Integration (Bewegung) grundsätzlich funktioniert.
    Da wir Numba nutzen, können wir keine Zwischenschritte (Kräfte) mehr abfragen.
    Wir prüfen: Input -> Step -> Output (Bewegung).
    """
    sim = basic_simulation

    # 1. Status Quo prüfen (Ruhezustand)
    assert np.all(sim.particles.velocities == 0.0)
    start_pos_0 = sim.particles.positions[0, 0]
    start_pos_1 = sim.particles.positions[1, 0]

    # 2. Einen Schritt simulieren
    # Dies ruft intern den Numba-Kernel auf
    sim.update_positions()

    # 3. Prüfung: Haben sie sich bewegt?
    # Bei Anziehung (Rule 1.0) müssen sie sich aufeinander zu bewegen.

    # Partikel 0 (links) sollte nach rechts (+x) beschleunigt werden
    vel_0_x = sim.particles.velocities[0, 0]
    assert vel_0_x > 0.0, "Partikel 0 sollte sich nach rechts bewegen (Anziehung)"

    # Partikel 1 (rechts) sollte nach links (-x) beschleunigt werden
    vel_1_x = sim.particles.velocities[1, 0]
    assert vel_1_x < 0.0, "Partikel 1 sollte sich nach links bewegen (Anziehung)"

    # Positionen müssen sich verändert haben
    assert sim.particles.positions[0, 0] > start_pos_0
    assert sim.particles.positions[1, 0] < start_pos_1


def test_no_interaction_outside_max_r():
    """Testet den Randfall: Wenn Partikel zu weit weg sind, darf keine Kraft wirken."""
    # Setup
    positions = np.array([[0.0, 0.0], [0.4, 0.0]])  # Abstand 0.4
    types = np.array([0, 0])

    mock_particles = SimpleParticleMock(positions, types)
    mock_interaction = SimpleInteractionMock(rule_value=1.0, n_types=1)

    # Simulation mit sehr kleinem Radius (0.2)
    # Distanz (0.4) > max_r (0.2) -> Keine Kraft
    # Auch hier: noise=0.0 übergeben!
    sim = Simulation(0.1, 0.2, 0.0, 0.0, mock_particles, mock_interaction)

    # Schritt ausführen
    sim.update_positions()

    # Prüfung: Geschwindigkeiten müssen 0 bleiben, da keine Kraft wirkt
    # Wir nutzen eine kleine Toleranz für Floating Point Ungenauigkeiten
    assert np.allclose(sim.particles.velocities, 0.0), "Partikel sollten sich nicht bewegen (ausserhalb Reichweite)"