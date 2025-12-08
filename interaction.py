import numpy as np

class Interaction:
    """
    Verwaltet die physikalischen Regeln der Simulation (Das 'Gesetzbuch').
    
    Optimiert für NumPy: Statt einzelne Werte abzufragen, berechnet diese Klasse
    Matrizen für das gesamte System (Vektorisierung).
    """
    def __init__(self, num_types: int):
        """
        Initialisiert die Interaktions-Logik.

        Args:
            num_types (int): Anzahl der Partikel-Typen (Farben).

        """
        self.num_types = num_types


        # Die Interaktions-Matrix (N_types x N_types)
        # Wertebereich: -1.0 (Abstoßung) bis +1.0 (Anziehung)
        self.matrix = np.zeros((num_types, num_types))
        
        # Initialisiert die Standard-Regeln
        self._make_default_matrix()

        print(f"--> [Interaction] Initialisiert: {num_types} Typen")

    def set_rule(self, type_a: int, type_b: int, force: float):
        """Setzt eine spezifische Regel manuell."""
        self.matrix[type_a, type_b] = force

    def _make_default_matrix(self):
        """
        Füllt die Matrix mit Startwerten (Vektorisierte Initialisierung).
        Regel: Gleiche ziehen sich an (+1), Ungleiche stoßen sich ab (-1).
        """
        # Setze erst mal alles auf Abstoßung (-1.0)
        self.matrix.fill(-1.0)
        
        # Setze die Diagonale (Gleiche Farben) auf Anziehung (+1.0)
        np.fill_diagonal(self.matrix, 1.0)

        # Optional: Zufällige kleine Variationen für interessanteres Verhalten
        # self.matrix += np.random.uniform(-0.1, 0.1, size=self.matrix.shape)
        return self.matrix

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
