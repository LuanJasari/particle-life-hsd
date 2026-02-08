import numpy as np
from numba import jit


class Simulation:
    """
    High-Performance Implementierung der Physik mit Numba JIT.
    Statt speicherintensiver Matrizen nutzen wir kompilierte Schleifen.
    """

    def __init__(self, dt, max_r, friction, particles, interactions):
        self.dt = dt
        self.max_r = max_r
        self.friction = friction
        self.particles = particles
        self.interaction = interactions

    def step(self):
        """Führt einen kompletten Simulationsschritt durch (Kräfte + Bewegung)."""

        # 1. Daten für Numba vorbereiten (NumPy Arrays extrahieren)
        positions = self.particles.positions
        velocities = self.particles.velocities
        types = self.particles.types
        rules = self.interaction.matrix

        # 2. Die schwere Arbeit an Numba delegieren
        # Wir übergeben Arrays und erhalten neue Geschwindigkeiten/Positionen zurück
        update_physics_numba(
            positions,
            velocities,
            types,
            rules,
            self.max_r,
            self.dt,
            self.friction
        )

        # 3. Wrapping (Randbedingung: Partikel bleiben im Bereich 0.0-1.0)
        # Das geht in NumPy sehr schnell
        self.particles.positions %= 1.0

    # Wrapper-Methoden für Kompatibilität mit Visualizer/Tests
    def update_accelerations(self): pass  # In Numba integriert

    def update_velocities(self): pass  # In Numba integriert

    def update_positions(self):  # In Numba integriert
        self.step()

    # --- Der Numba JIT Kernel (Das Herzstück) ---


# @jit(nopython=True) kompiliert diesen Python-Code in extrem schnellen Maschinencode.
# parallel=True könnte man noch nutzen, aber für den Anfang reicht nopython.

@jit(nopython=True, fastmath=True)
def update_physics_numba(positions, velocities, types, rules, max_r, dt, friction):
    n_particles = len(positions)

    # Nested Loop: Jeder gegen Jeden (O(N^2))
    # Aber: Da es kompiliert ist, läuft es 100x schneller als Python.
    for i in range(n_particles):
        total_force_x = 0.0
        total_force_y = 0.0

        pos_x_i = positions[i, 0]
        pos_y_i = positions[i, 1]
        type_i = types[i]

        for j in range(n_particles):
            if i == j:
                continue

            # 1. Vektor berechnen
            dx = positions[j, 0] - pos_x_i
            dy = positions[j, 1] - pos_y_i

            # 2. Wrap-Around (Torus-Welt) berücksichtigen
            # Wenn dx > 0.5 ist, ist der Weg über den Rand kürzer -> dx -= 1.0
            if dx > 0.5:
                dx -= 1.0
            elif dx < -0.5:
                dx += 1.0
            if dy > 0.5:
                dy -= 1.0
            elif dy < -0.5:
                dy += 1.0

            # 3. Distanz
            dist_sq = dx * dx + dy * dy

            # Performance: Wurzelziehen ist teuer, daher erst prüfen ob wir im Radius sind
            if dist_sq > 0 and dist_sq < (max_r * max_r):
                dist = np.sqrt(dist_sq)

                # 4. Kraft berechnen (Normale Physik)
                # F = rule * (1 - dist/max_r)
                # rule holen wir direkt aus der Matrix: rules[type_i, type_j]
                force_val = rules[type_i, types[j]] * (1.0 - (dist / max_r))

                # Vektor normalisieren und Kraft anwenden
                total_force_x += (dx / dist) * force_val
                total_force_y += (dy / dist) * force_val

        # 5. Integration (Euler) direkt hier anwenden
        # Reibung
        velocities[i, 0] *= (1.0 - friction * dt)
        velocities[i, 1] *= (1.0 - friction * dt)

        # Beschleunigung -> Geschwindigkeit
        velocities[i, 0] += total_force_x * dt
        velocities[i, 1] += total_force_y * dt

    # 6. Geschwindigkeit -> Position (außerhalb der i-Schleife anwenden)
    for i in range(n_particles):
        positions[i, 0] += velocities[i, 0] * dt
        positions[i, 1] += velocities[i, 1] * dt