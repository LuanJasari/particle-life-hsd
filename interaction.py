import numpy as np
import random

class Interaction:
    def __init__(self, num_types):
        self.num_types = num_types
        # Erstelle eine Matrix voller Nullen (4x4)
        self.matrix = np.zeros((num_types, num_types))
        
        # Füllt die Matrix direkt beim Start mit Zufallszahlen
        self.randomize_matrix()

    def randomize_matrix(self):
        # Wir laufen durch jede Zeile und Spalte
        for i in range(self.num_types):
            for j in range(self.num_types):
                # Zufallswert zwischen -1 (Abstoßung) und 1 (Anziehung)
                random_value = random.uniform(-1.0, 1.0)
                self.matrix[i][j] = random_value

    def force_function(self, i, d, max_dist):
        """
        Berechnet die Kraft basierend auf dem Wert i aus der Matrix.
        i: Interaktions-Wert (z.B. 0.5)
        d: Distanz zwischen den Partikeln
        max_dist: Maximale Reichweite
        """
        # Wenn die Partikel zu weit weg sind, gibt es keine Kraft
        if d >= max_dist:
            return 0.0
        
        # Das ist eine einfache Formel:
        # Je näher sie sich sind (kleines d), desto stärker wirkt die Kraft i.
        factor = 1.0 - (d / max_dist)
        return i * factor

    def force_vector_function(self):
        # Hier kommt später die Vektorberechnung rein.
        # Das machen wir, wenn wir die Positionen (x,y) haben.
        pass