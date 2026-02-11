from particles import ParticleSystem
from interaction import Interaction
from simulation import Simulation
from visualisation import Visualizer


def main():
    print("=== Particle Life Simulator (Milestone 3+ Feature Complete) ===")

    # 1. Konfiguration
    # Tipp: Reduziere die Partikelzahl für Tests, erhöhe sie für das finale Video
    NUMBER_OF_PARTICLES = 1500
    NUMBER_OF_TYPES = 4

    # Physik-Parameter
    # Gute Werte für "Zellen": dt=0.02, max_r=0.1, friction=0.1, noise=0.05
    DT = 0.02  # Zeitschritt (kleiner = genauer, aber langsamer)
    MAX_R = 0.1  # Radius der Wahrnehmung
    FRICTION = 0.1  # Reibung (Verhindert Explosion der Geschwindigkeiten)
    NOISE = 0.05  # NEU: Zufallsbewegung (Macht das System "organischer")

    # 2. Initialisierung Backend
    print(f"-> Setup: {NUMBER_OF_PARTICLES} Partikel, 4 Typen")
    particles = ParticleSystem(NUMBER_OF_PARTICLES, NUMBER_OF_TYPES)

    # Interaktions-Regeln (Zufällig für spannende Ergebnisse)
    interactions = Interaction(NUMBER_OF_TYPES)
    # Optional: Setze eine feste Matrix für reproduzierbare Ergebnisse
    # interactions.set_rule(0, 0, 1.0) ...

    print("-> Starte Physik-Engine (Numba JIT)...")
    # Hier übergeben wir den neuen NOISE Parameter
    sim = Simulation(DT, MAX_R, FRICTION, NOISE, particles, interactions)

    # 3. Start Frontend
    print("-> Öffne Fenster (Vispy)...")
    viz = Visualizer(sim)
    viz.run()


if __name__ == "__main__":
    main()