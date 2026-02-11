from particles import ParticleSystem
from interaction import Interaction
from simulation import Simulation
from visualisation import Visualizer


def main():
    print("=== Particle Life Simulator (Milestone 4 Build) ===")

    # 1. Konfiguration
    NUMBER_OF_PARTICLES = 2000  # Startwert für die Simulation
    [cite_start]NUMBER_OF_TYPES = 4         # Mindestens 4 Typen gefordert [cite: 36]

    # Physik-Parameter
    DT = 0.001       # Zeitschritt
    MAX_R = 0.15     # Radius der Wahrnehmung
    FRICTION = 0.1   # Reibung
    [cite_start]NOISE = 0.02     # Zusätzliche Zufallsbewegung für emergentes Verhalten [cite: 39]

    # 2. Initialisierung Backend
    print("-> Initialisiere Partikel...")
    particles = ParticleSystem(NUMBER_OF_PARTICLES, NUMBER_OF_TYPES)

    print("-> Initialisiere Regeln...")
    interactions = Interaction(NUMBER_OF_TYPES)

    print("-> Starte Physik-Engine...")
    # Übergabe der Parameter inklusive Noise an die Simulation
    sim = Simulation(DT, MAX_R, FRICTION, NOISE, particles, interactions)

    # 3. Start Frontend
    print("-> Öffne Fenster (Vispy)...")
    viz = Visualizer(sim)
    viz.run()


if __name__ == "__main__":
    main()
