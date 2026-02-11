import numpy as np
from numba import jit

class Simulation:
    """
    High-Performance Implementierung der Physik mit Numba JIT.
    """

    def __init__(self, dt, max_r, friction, noise, particles, interactions):
        # Die Signatur folgt nun dem im Profiling-Skript erwarteten Format
        self.dt = dt
        self.max_r = max_r
        self.friction = friction
        self.noise = noise  # Neuer Parameter für Zufallsbewegung
        self.particles = particles
        self.interaction = interactions

    def step(self):
        positions = self.particles.positions
        velocities = self.particles.velocities
        types = self.particles.types
        rules = self.interaction.matrix

        update_physics_numba(
            positions,
            velocities,
            types,
            rules,
            self.max_r,
            self.dt,
            self.friction,
            self.noise  # Übergabe an den Kernel
        )

        self.particles.positions %= 1.0

    def update_accelerations(self): pass
    def update_velocities(self): pass
    def update_positions(self):
        self.step()

@jit(nopython=True, fastmath=True)
def update_physics_numba(positions, velocities, types, rules, max_r, dt, friction, noise):
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

            # Torus-Welt Wrap-Around
            if dx > 0.5: dx -= 1.0
            elif dx < -0.5: dx += 1.0
            if dy > 0.5: dy -= 1.0
            elif dy < -0.5: dy += 1.0

            dist_sq = dx * dx + dy * dy

            if dist_sq > 0 and dist_sq < (max_r * max_r):
                dist = np.sqrt(dist_sq)
                force_val = rules[type_i, types[j]] * (1.0 - (dist / max_r))

                total_force_x += (dx / dist) * force_val
                total_force_y += (dy / dist) * force_val

        # Integration (Euler)
        # 1. Reibung anwenden
        velocities[i, 0] *= (1.0 - friction * dt)
        velocities[i, 1] *= (1.0 - friction * dt)

        # 2. Kräfte addieren
        velocities[i, 0] += total_force_x * dt
        velocities[i, 1] += total_force_y * dt

        # 3. Zufallsbewegung (Noise) hinzufügen
        # Wir nutzen np.random.uniform für den JIT-Kernel
        velocities[i, 0] += (np.random.random() * 2.0 - 1.0) * noise * dt
        velocities[i, 1] += (np.random.random() * 2.0 - 1.0) * noise * dt

    # Positionen aktualisieren
    for i in range(n_particles):
        positions[i, 0] += velocities[i, 0] * dt
        positions[i, 1] += velocities[i, 1] * dt
