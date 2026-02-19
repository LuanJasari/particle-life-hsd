import pytest
import numpy as np
from particle_life_simulator.interaction import Interaction

@pytest.fixture
def interaction():
    """
    Creates an Interaction instance and overwrites specific rules
    so the tests have deterministic values to check against.
    """
    inter = Interaction(num_types=4)
    
    inter.set_rule(0, 1, -0.9)

    inter.set_rule(0, 0, 1.0)

    return inter


def test_initialization(interaction):
    assert interaction.num_types == 4
    assert interaction.matrix.shape == (4, 4)


def test_specific_interaction_values(interaction):
    
    assert interaction.matrix[0, 1] == -0.9


def test_set_rule(interaction):
    interaction.set_rule(2, 3, 0.5)
    assert interaction.matrix[2, 3] == 0.5


def test_get_rule_grid(interaction):
    types = np.array([0, 1, 0])

    grid = interaction.get_rule_grid(types)

    assert grid.shape == (3, 3)

    assert grid[0, 0] == 1.0

    assert grid[0, 1] == -0.9
