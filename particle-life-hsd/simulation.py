import numpy as np
from numba import jit

class Simulation:
    def __init__(self, dt, max_r, friction, noise, particles, interactions):
        self.dt = dt
        self.max_r = max_r
        self.friction = friction
        self.noise = noise
        self.particles = particles
        self.interaction = interactions

    def step(self):
        # Vorbereitung der Daten für den Numba-Kernel
        positions = self.particles.positions
        velocities = self.particles.velocities
        types = self.particles.types
        rules = self.interaction.matrix

        update_physics_numba(
            positions, velocities, types, rules,
            self.max_r, self.dt, self.friction, self.noise
        )

        # Torus-Welt: Partikel bleiben im Bereich 0.0-1.0
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
            if i == j: continue

            dx = positions[j, 0] - pos_x_i
            dy = positions[j, 1] - pos_y_i

            # Wrap-Around (Torus)
            if dx > 0.5: dx -= 1.0
            elif dx < -0.5: dx += 1.0
            if dy > 0.5: dy -= 1.0
            elif dy < -0.5: dy += 1.0

            dist_sq = dx * dx + dy * dy

            if dist_sq > 0 and dist_sq < (max_r * max_r):
                dist = np.sqrt(dist_sq)
                # Kraftberechnung [cite: 31, 33]
                force_val = rules[type_i, types[j]] * (1.0 - (dist / max_r))
                total_force_x += (dx / dist) * force_val
                total_force_y += (dy / dist) * force_val

        # Euler-Integration inkl. Reibung und Noise [cite: 125, 39]
        velocities[i, 0] *= (1.0 - friction * dt)
        velocities[i, 1] *= (1.0 - friction * dt)
        velocities[i, 0] += (total_force_x + (np.random.random() * 2 - 1) * noise) * dt
        velocities[i, 1] += (total_force_y + (np.random.random() * 2 - 1) * noise) * dt

    for i in range(n_particles):
        positions[i, 0] += velocities[i, 0] * dt
        positions[i, 1] += velocities[i, 1] * dt
