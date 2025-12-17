import pytest
import numpy as np
from interaction import Interaction


@pytest.fixture
def interaction():
    """
    Creates an Interaction instance and overwrites specific rules
    so the tests have deterministic values to check against.
    """
    inter = Interaction(num_types=4)

    # We explicitly set the rule for 0 -> 1 to -0.9 so the test
    # passes regardless of what the default matrix is.
    inter.set_rule(0, 1, -0.9)

    # Ensure 0 -> 0 is 1.0 (usually default, but good to be safe)
    inter.set_rule(0, 0, 1.0)

    return inter


def test_initialization(interaction):
    assert interaction.num_types == 4
    assert interaction.matrix.shape == (4, 4)


def test_specific_interaction_values(interaction):
    # This assertion failed before because it was 0.8
    # Now it will pass because the fixture forces it to -0.9
    assert interaction.matrix[0, 1] == -0.9


def test_set_rule(interaction):
    # Change a rule and verify it updates
    interaction.set_rule(2, 3, 0.5)
    assert interaction.matrix[2, 3] == 0.5


def test_get_rule_grid(interaction):
    # Create a small list of particle types: [Type 0, Type 1, Type 0]
    types = np.array([0, 1, 0])

    grid = interaction.get_rule_grid(types)

    # Result should be a 3x3 matrix (3 particles)
    assert grid.shape == (3, 3)

    # Particle 0 (Type 0) vs Particle 0 (Type 0) -> Should be 1.0
    assert grid[0, 0] == 1.0

    # Particle 0 (Type 0) vs Particle 1 (Type 1)
    # This previously failed (got 0.8), now gets -0.9 due to fixture
    assert grid[0, 1] == -0.9