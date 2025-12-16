import numpy as np
import pytest
from interaction import Interaction


@pytest.fixture
def interaction():
    return Interaction(num_types=4)


def test_initialization(interaction):
    assert interaction.num_types == 4
    assert interaction.matrix.shape == (4, 4)


def test_diagonal_is_attraction(interaction):
    assert np.all(np.diag(interaction.matrix) == 1.0)


def test_off_diagonal_is_repulsion(interaction):
    assert interaction.matrix[0, 1] == -1.0


def test_set_rule(interaction):
    interaction.set_rule(0, 1, 0.5)
    assert interaction.matrix[0, 1] == 0.5


def test_get_rule_grid(interaction):
    types = np.array([0, 1, 0])
    grid = interaction.get_rule_grid(types)

    assert grid.shape == (3, 3)
    assert grid[0, 0] == 1.0
    assert grid[0, 1] == -1.0
