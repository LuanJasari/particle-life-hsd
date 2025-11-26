from particles import ParticleSystem


def main():
    """
    Haupt-Einstiegspunkt.
    Aktuell: Testet die Initialisierung der Datenstrukturen für Milestone 2.
    """
    print("=== Particle Life Simulator ===")

    # Konfiguration
    NUMBER_OF_PARTICLES = 2000
    NUMBER_OF_TYPES = 4

    # Initialisierung des Systems (Deine Aufgabe aus Issue #1)
    system = ParticleSystem(NUMBER_OF_PARTICLES, NUMBER_OF_TYPES)

    # Kurzer Check der Daten (Proof of Concept)
    print("\nDaten-Check (Erste 3 Partikel):")
    print(f"Pos 1: {system.positions[0]}")
    print(f"Pos 2: {system.positions[1]}")
    print(f"Typ 1: {system.types[0]}")

    print("\nSystem läuft. Bereit für Physik-Implementierung.")


if __name__ == "__main__":
    main()