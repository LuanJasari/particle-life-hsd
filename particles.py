import numpy as np

class ParticleSystem:
    """
    Zentrale Klasse zur Verwaltung aller Partikel.
    Nutzt NumPy Arrays für performante Berechnungen (Vektorisierung),
    statt einzelner Python-Objekte pro Partikel.
    """
    def __init__(self, n_particles: int, n_types: int):
        """
        Initialisiert das System mit N Partikeln und T Typen.

        Args:
            n_particles (int): Anzahl der zu simulierenden Partikel (z.B. 2000).
            n_types (int): Anzahl der verschiedenen Partikel-Typen/Farben.
        """
        self.n_particles = n_particles
        self.n_types = n_types

        # 1. Positionen (x, y)
        # Ein Array der Form (N, 2). Werte zwischen 0.0 und 1.0.
        # Zeile = Partikel, Spalte 0 = x, Spalte 1 = y
        self.positions = np.random.rand(n_particles, 2)

        # 2. Geschwindigkeiten (vx, vy)
        # ein Array der Form (N, 2). Initialisiert mit 0.
        self.velocities = np.zeros((n_particles, 2))

        # 3. Beschleunigungen (ax, ay)
        self.accelerations= np.zeros((n_particles, 2))

        # 4. Typen (Farben)
        # ein Array der Form (N,). Werte sind Integer von 0 bis n_types-1.
        # Z.B. [0, 3, 1, 0, 2, ...]
        self.types = np.random.randint(0, n_types, size=n_particles)

        print(f"--> ParticleSystem initialisiert: {n_particles} Partikel, {n_types} Typen.")
        print(f"    Memory Layout: Positions={self.positions.shape}, Types={self.types.shape}")

    def get_positions(self):
        """Gibt die rohen Positionsdaten zurück."""
        return self.positions

    def get_types(self):
        """Gibt die Typen-Daten zurück."""
        return self.types

#p=ParticleSystem(2000,4)
#print(p.positions)
