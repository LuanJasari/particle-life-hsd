import cProfile
import pstats
import time
from particles import ParticleSystem
from interaction import Interaction
from simulation import Simulation

 
def profile_simulation():
    print("=== Performance Profiling (Milestone 4) ===")

    # 1. Setup: Hohe Last für deutliche Signale
    N_PARTICLES = 1500  # Angepasst an Numba-Leistungsfähigkeit
    N_TYPES = 4
    STEPS = 200         # Mehr Schritte für stabilere Daten

    print(f"-> Setup: {N_PARTICLES} Partikel, {STEPS} Zeitschritte (Headless)")

    particles = ParticleSystem(N_PARTICLES, N_TYPES)
    interactions = Interaction(N_TYPES)

    # FIX: Parameter an neue Signatur angepasst (noise=0.0 für faire Messung)
    # Simulation(dt, max_r, friction, noise, particles, interactions)
    sim = Simulation(0.02, 0.15, 0.1, 0.0, particles, interactions)

    # 2. Warmup (Wichtig bei JIT!)
    # Numba braucht einen Durchlauf zum Kompilieren. Den wollen wir NICHT messen.
    print("-> JIT-Warmup...")
    sim.step()

    # 3. Der Profiler-Start
    print("-> Starte Profiling...")
    profiler = cProfile.Profile()
    profiler.enable()

    start_time = time.time()

    # Hot Path Loop
    for _ in range(STEPS):
        sim.step()  # Wir nutzen jetzt direkt .step(), da die Wrapper leer sind

    end_time = time.time()

    profiler.disable()

    # 4. Auswertung
    duration = end_time - start_time
    fps = STEPS / duration
    print(f"\n-> Fertig! Dauer: {duration:.4f}s | Simulierte FPS: {fps:.2f}")

    print("\n" + "=" * 60)
    print("TOP BOTTLENECKS (Nach kumulierter Zeit)")
    print("=" * 60)
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(15)

    print("\n" + "=" * 60)
    print("TOP BOTTLENECKS (Nach interner Zeit - Numba check)")
    print("=" * 60)
    # Hier sollten wir sehen, dass fast alles in der kompilierten Funktion passiert
    stats.sort_stats('tottime').print_stats(10)


if __name__ == "__main__":
    profile_simulation()
