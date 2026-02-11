import cProfile
import pstats
import time
from particles import ParticleSystem
from interaction import Interaction
from simulation import Simulation

def profile_simulation():
    print("=== Performance Profiling (Milestone 4) ===")
    N_PARTICLES = 1500
    N_TYPES = 4
    STEPS = 200

    print(f"-> Setup: {N_PARTICLES} Partikel, {STEPS} Zeitschritte (Headless)")

    particles = ParticleSystem(N_PARTICLES, N_TYPES)
    interactions = Interaction(N_TYPES)
    sim = Simulation(0.02, 0.15, 0.1, 0.0, particles, interactions)

    print("-> JIT-Warmup...")
    sim.step()

    print("-> Starte Profiling...")
    profiler = cProfile.Profile()
    profiler.enable()

    start_time = time.time()
    for _ in range(STEPS):
        sim.step()

    end_time = time.time()
    profiler.disable()

    duration = end_time - start_time
    fps = STEPS / duration
    print(f"\n-> Fertig! Dauer: {duration:.4f}s | Simulierte FPS: {fps:.2f}")

    print("\n" + "=" * 60)
    print("TOP BOTTLENECKS")
    print("=" * 60)
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(15)

if __name__ == "__main__":
    profile_simulation()
