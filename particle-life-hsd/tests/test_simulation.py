import numpy as np
import pytes
from simulation import Simulation

# -------- vereinfachte Mock-Klassen ----------
"""Damit lässt sich die physikalische Berechnungslogik 
der Simulation-Klasse isoliert werden."""

class SimpleParticleMock:
  # Nur die absolut notwendigen Attribute und Methoden
  def __init__(self, pos, types)
    self.positions = pos
    self.types = types
    self.velocities = np.zeros(pos.shape)
    self.accelerations = np.zeros(pos.shape)

