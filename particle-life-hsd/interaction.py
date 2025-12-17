import numpy as np
from astropy.utils.metadata.utils import dtype


class Interaction:
    """
    Verwaltet die physikalischen Regeln der Simulation (Das 'Gesetzbuch').

    Optimiert für NumPy: Statt einzelne Werte abzufragen, berechnet diese Klasse
    Matrizen für das gesamte System (Vektorisierung).
    """

    def __init__(self, num_types: int):
        """
        Initialisiert die Interaktions-Logik.
        """
        self.num_types = num_types

        # Die Interaktions-Matrix (N_types x N_types)
        # Wertebereich: -1.0 (Abstoßung) bis +1.0 (Anziehung)
        self.matrix = self._make_default_matrix()

        print(f"--> [Interaction] Initialisiert: {num_types} Typen")

    def set_rule(self, type_a: int, type_b: int, force: float):
        """Setzt eine spezifische Regel manuell."""
        self.matrix[type_a, type_b] = force

    def _make_default_matrix(self):
        """
        Interaktionsmatrix für echtes 'Particle Life' (Asymmetrisch).
        """
        # Wir definieren 4 Typen: 0=Rot, 1=Grün, 2=Blau, 3=Weiß
        # Zeile i = Wie reagiert Typ i auf andere?
        # Spalte j = Auf wen wird reagiert?

        matrix = np.array([
            #           Rot   Grün  Blau  Weiß  (Gegenüber)
            # Typ 0 (Rot)
            [1.0, 0.8, -0.5, -0.5],  # Rot mag sich und Grün, hasst Blau

            # Typ 1 (Grün)
            [-0.8, 1.0, 0.5, 0.0],  # Grün flieht vor Rot (!), mag sich

            # Typ 2 (Blau)
            [0.5, -0.5, 1.0, 0.5],  # Blau jagt Rot (!), hasst Grün

            # Typ 3 (Weiß)
            [0.0, 0.5, -0.2, 1.0]  # Weiß mag Grün, ignoriert Rest
        ], dtype=float)

        return matrix

    def get_rule_grid(self, types_array: np.ndarray) -> np.ndarray:
        """
        DER PERFORMANCE-BOOSTER (Advanced Indexing).

        Erstellt basierend auf dem Typen-Array aller Partikel sofort
        die korrekte (N, N) Kraft-Matrix für jeden gegen jeden.

        Args:
            types_array (np.ndarray): Array der Form (N,) mit den Typen aller Partikel.

        Returns:
            np.ndarray: Eine (N, N) Matrix, wobei entry [i, j] den Faktor definiert,
                        wie Partikel i auf Partikel j reagiert.
        """
        # NumPy Magic: Wir nutzen die Typen-Arrays als Indizes für die Matrix.
        # Broadcasting sorgt dafür, dass wir eine N x N Matrix erhalten.
        # Zeile i, Spalte j = self.matrix[type_i, type_j]
        return self.matrix[types_array[:, np.newaxis], types_array[np.newaxis, :]]

i=Interaction(4)
print(i.matrix)