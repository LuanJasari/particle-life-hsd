import cProfile
import pstats
import numpy as np
import time
from particles import ParticleSystem
from interaction import Interaction
from simulation import Simulation


def profile_simulation():
    print("=== Performance Profiling (Milestone 4) ===")

    # 1. Setup: Wir testen mit einer hohen Last, um Bottlenecks deutlich zu sehen
    # 1000 Partikel ist das Ziel für Milestone 4
    N_PARTICLES = 1000
    N_TYPES = 4
    STEPS = 100  # Wir simulieren 100 Frames

    print(f"-> Setup: {N_PARTICLES} Partikel, {STEPS} Zeitschritte (Headless/Ohne Grafik)")

    # Initialisierung (wie in main.py, aber ohne Visualizer)
    particles = ParticleSystem(N_PARTICLES, N_TYPES)
    interactions = Interaction(N_TYPES)

    # Simulation Instanz
    sim = Simulation(0.02, 0.15, 0.1, particles, interactions)

    # 2. Der Profiler-Start
    print("-> Starte Profiling... (Bitte warten)")
    profiler = cProfile.Profile()
    profiler.enable()

    # --- Die kritische Schleife (Hot Path) ---
    start_time = time.time()

    for _ in range(STEPS):
        sim.update_accelerations()
        sim.update_velocities()
        sim.update_positions()

    end_time = time.time()
    # -----------------------------------------

    profiler.disable()

    # 3. Auswertung
    duration = end_time - start_time
    fps = STEPS / duration
    print(f"\n-> Fertig! Dauer: {duration:.4f}s | Simulierte FPS: {fps:.2f}")

    print("\n" + "=" * 60)
    print("TOP BOTTLENECKS (Nach kumulierter Zeit sortiert)")
    print("=" * 60)

    # Wir sortieren nach 'cumtime' (Cumulative Time = Zeit in der Funktion + Unterfunktionen)
    # Das zeigt uns, welcher High-Level-Aufruf am teuersten ist.
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(20)  # Zeige nur die Top 20 Zeilen

    print("\n" + "=" * 60)
    print("TOP BOTTLENECKS (Nach interner Zeit sortiert)")
    print("=" * 60)
    # 'tottime' = Zeit NUR in der Funktion selbst (ohne Unteraufrufe)
    # Das zeigt, wo die CPU wirklich rechnet (z.B. numpy Methoden)
    stats.sort_stats('tottime').print_stats(15)


if __name__ == "__main__":
    profile_simulation()