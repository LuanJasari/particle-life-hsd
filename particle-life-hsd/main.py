from particles import ParticleSystem
from interaction import Interaction
from simulation import Simulation
from visualisation import Visualizer


def main():
    print("=== Particle Life Simulator (Milestone 3 Build) ===")

    # 1. Konfiguration
    NUMBER_OF_PARTICLES = 2000  # Startwert für flüssige 60 FPS
    NUMBER_OF_TYPES = 4

    # Physik-Parameter (Experimentiere hiermit für cooles Verhalten!)
    DT = 0.001  # Zeitschritt
    MAX_R = 0.15  # Radius der Wahrnehmung
    FRICTION = 0.1  # Reibung (0.0 = keine, 1.0 = Klebstoff)

    # 2. Initialisierung Backend
    print("-> Initialisiere Partikel...")
    particles = ParticleSystem(NUMBER_OF_PARTICLES, NUMBER_OF_TYPES)

    print("-> Initialisiere Regeln...")
    interactions = Interaction(NUMBER_OF_TYPES)


    #interactions.matrix = np.random.uniform(-0.5, 1.0, size=(NUMBER_OF_TYPES, NUMBER_OF_TYPES))

    print("-> Starte Physik-Engine...")
    sim = Simulation(DT, MAX_R, FRICTION, particles, interactions)

    # 3. Start Frontend
    print("-> Öffne Fenster (Vispy)...")
    viz = Visualizer(sim)
    viz.run()


if __name__ == "__main__":
    main()
