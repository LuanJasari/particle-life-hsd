import numpy as np
from numba import jit


class Simulation:
    """
    High-Performance Implementierung der Physik mit Numba JIT.
    Statt speicherintensiver Matrizen nutzen wir kompilierte Schleifen.
    """

    def __init__(self, dt, max_r, friction, noise, particles, interactions):
        """
        Initialisiert die Simulation mit den physikalischen Parametern.
        Der Parameter 'noise' steuert die zusätzliche Zufallsbewegung.
        """
        self.dt = dt
        self.max_r = max_r
        self.friction = friction
        self.noise = noise  # 
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
        # Die Signatur entspricht nun der Erwartung in profiling.py
        update_physics_numba(
            positions,
            velocities,
            types,
            rules,
            self.max_r,
            self.dt,
            self.friction,
            self.noise
        )

        # 3. Wrapping (Randbedingung: Partikel bleiben im Bereich 0.0-1.0)
        self.particles.positions %= 1.0

    # Wrapper-Methoden für Kompatibilität mit Visualizer/Tests
    def update_accelerations(self): 
        pass  # Die Beschleunigung wird nun direkt im Numba-Kernel verarbeitet

    def update_velocities(self): 
        pass  # Die Geschwindigkeit wird nun direkt im Numba-Kernel verarbeitet

    def update_positions(self):  
        self.step()

# --- Der Numba JIT Kernel ---

@jit(nopython=True, fastmath=True)
def update_physics_numba(positions, velocities, types, rules, max_r, dt, friction, noise):
    """
    Kompilierter Kernel zur Berechnung der Partikelinteraktionen.
    Implementiert Anziehung, Abstoßung, Reibung und Zufallsbewegung[cite: 31, 39].
    """
    n_particles = len(positions)

    # Nested Loop: Jeder gegen Jeden (O(N^2))
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

            if dist_sq > 0 and dist_sq < (max_r * max_r):
                dist = np.sqrt(dist_sq)

                # 4. Kraft berechnen (F = rule * (1 - dist/max_r)) [cite: 33, 34]
                force_val = rules[type_i, types[j]] * (1.0 - (dist / max_r))

                # Vektor normalisieren und Kraft anwenden
                total_force_x += (dx / dist) * force_val
                total_force_y += (dy / dist) * force_val

        # 5. Integration (Euler)
        # Reibung anwenden
        velocities[i, 0] *= (1.0 - friction * dt)
        velocities[i, 1] *= (1.0 - friction * dt)

        # Kräfte auf Geschwindigkeit anwenden
        velocities[i, 0] += total_force_x * dt
        velocities[i, 1] += total_force_y * dt
        
        # Zusätzliche Zufallsbewegung (Noise) hinzufügen 
        # Erzeugt einen Wert zwischen -noise und +noise
        velocities[i, 0] += (np.random.random() * 2.0 - 1.0) * noise * dt
        velocities[i, 1] += (np.random.random() * 2.0 - 1.0) * noise * dt

    # 6. Geschwindigkeit auf Position anwenden
    for i in range(n_particles):
        positions[i, 0] += velocities[i, 0] * dt
        positions[i, 1] += velocities[i, 1] * dt
