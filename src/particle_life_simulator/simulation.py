import numpy as np
from numba import jit

class Simulation:
    """
    High-Performance Implementierung der Physik mit Numba JIT.
    Statt speicherintensiver Matrizen nutzen wir kompilierte Schleifen.
    """

    def __init__(self, dt, max_r, friction, noise_strength, particles, interactions):
        """
        Args:
            dt: Der Zeitschritt
            max_r: Maximale Raum für eine Interaktion
            friction: Die Reibung, die die Geschwindigkeit verringern soll
            noise_strength: Stärke der stochastischen Zufallsbewegung
            particles: Das Partikelsystem
            interactions: Die Interaktionsmatrix
        """
        self.dt = dt
        self.max_r = max_r
        self.friction = friction
        self.noise_strength = noise_strength
        self.particles = particles
        self.interaction = interactions

    def step(self):
        """Führt einen kompletten Simulationsschritt durch."""

        # 1. Daten für Numba vorbereiten (NumPy Arrays extrahieren)
        positions = self.particles.positions
        velocities = self.particles.velocities
        types = self.particles.types
        rules = self.interaction.matrix

        # 2. Die physikalischen Berechnungen an Numba delegieren
        update_physics_numba(
            positions,
            velocities,
            types,
            rules,
            self.max_r,
            self.dt,
            self.friction,
            self.noise_strength,
        )

        # 3. Wrapping (Randbedingung: Partikel bleiben im Bereich 0.0-1.0)
        self.particles.positions %= 1.0

    # Wrapper-Methoden für Kompatibilität mit dem Visualizer
    def update_accelerations(self):
        pass

    def update_velocities(self):
        pass

    def update_positions(self):
        self.step()


@jit(nopython=True, fastmath=True)
def update_physics_numba(positions, velocities, types, rules, max_r, dt, friction, noise_strength):
    """
    Numba JIT Kernel zur Berechnung der Interaktionen inkl. Zufallsbewegung.
    """
    n_particles = len(positions)

    for i in range(n_particles):
        total_force_x = 0.0
        total_force_y = 0.0

        pos_x_i = positions[i, 0]
        pos_y_i = positions[i, 1]
        type_i = types[i]

        for j in range(n_particles):
            if i == j:
                continue

            dx = positions[j, 0] - pos_x_i
            dy = positions[j, 1] - pos_y_i

            if dx > 0.5:
                dx -= 1.0
            elif dx < -0.5:
                dx += 1.0

            if dy > 0.5:
                dy -= 1.0
            elif dy < -0.5:
                dy += 1.0

            dist_sq = dx * dx + dy * dy

            if dist_sq > 0 and dist_sq < (max_r * max_r):
                dist = np.sqrt(dist_sq)
                force_val = rules[type_i, types[j]] * (1.0 - (dist / max_r))
                total_force_x += (dx / dist) * force_val
                total_force_y += (dy / dist) * force_val

        # 5. Integration (Euler) inkl. Reibung und Zufallsbewegung
        velocities[i, 0] *= (1.0 - friction * dt)
        velocities[i, 1] *= (1.0 - friction * dt)

        # Deterministische Kraft
        velocities[i, 0] += total_force_x * dt
        velocities[i, 1] += total_force_y * dt
        
        # Stochastische Kraft (Noise)
        if noise_strength > 0.0:
            velocities[i, 0] += (np.random.rand() - 0.5) * noise_strength * dt
            velocities[i, 1] += (np.random.rand() - 0.5) * noise_strength * dt

    # 6. Geschwindigkeit auf Position anwenden
    for i in range(n_particles):
        positions[i, 0] += velocities[i, 0] * dt
        positions[i, 1] += velocities[i, 1] * dt
