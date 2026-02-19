import numpy as np
import pytest
from src.particle_life_simulator.simulation import Simulation

class SimpleParticleMock:
    """Simuliert ein Partikel-System für den Test."""
    def __init__(self, pos, types):
        self.positions = np.array(pos, dtype=float)
        self.types = np.array(types, dtype=int)
        self.velocities = np.zeros_like(self.positions)
        self.accelerations = np.zeros_like(self.positions)

class SimpleInteractionMock:
    """Mock für die Interaktionsmatrix."""
    def __init__(self, rule_value):
        self.matrix = np.full((4, 4), rule_value, dtype=float)


@pytest.fixture
def basic_simulation():
    positions = np.array([[0.4, 0.5], [0.6, 0.5]])
    types = np.array([0, 0])

    dt = 0.1
    max_r = 0.5
    friction = 0.0 
    noise = 0.0    

    mock_particles = SimpleParticleMock(positions, types)
    mock_interaction = SimpleInteractionMock(rule_value=1.0)

    return Simulation(dt, max_r, friction, noise, mock_particles, mock_interaction)


def test_simulation_step_behavior(basic_simulation):
    """Prüft, ob ein step() die Positionen und Geschwindigkeiten verändert."""
    sim = basic_simulation
    old_pos = sim.particles.positions.copy()
    
    sim.step()
    
    assert not np.array_equal(sim.particles.positions, old_pos)
    assert sim.particles.velocities[0, 0] > 0 
    assert sim.particles.velocities[1, 0] < 0 

def test_no_interaction_outside_max_r_step(basic_simulation):
    """Prüft, ob Teilchen außerhalb von max_r ignoriert werden."""
    sim = basic_simulation
    sim.max_r = 0.05 
    
    sim.step()
    
    assert np.all(sim.particles.velocities == 0.0)
    assert np.all(sim.particles.positions[0] == [0.4, 0.5])
