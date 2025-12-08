import numpy as np
import sys

#from particles import ParticleSystem
#from interaction import Interaction

class Simulation:
    """
    Implementierung der Physik: Berechnung von Distanzen, Kräfte und Aktualisierung der Geschwindigkeiten sowie Positionen der Partikeln.
    Das Ganze mithilfe von Numpy Broadcasting. Vorteil: alle Berechnungen auf alle Partikeln auf einmal durchgeführt (für Aufwandsoptimierung).

    Attributes:
        dt (int) : stellt die Zeitänderung dar.
        friction (int) : repräsentiert die aus Reibung resultierende Verzögerung (Deceleration due to kinetic friction)
        max_r (int) : der maximale Abstand für Interaktion
        particles : ein Instanz von ParticleSystem
        interaction : ein Instanz von Interaction
    """
    def __init__(self, dt, max_r, friction, particles, interactions):
        self.dt = dt
        self.max_r = max_r
        self.friction = friction
        self.particles = particles
        self.interaction = interactions

    #Aufstellung einer Matrix, deren Einträge die Richtungsvektoren zwischen allen Partikelpaaren enthalten. Shape (N,N,2)
    def compute_distance_vector_matrix(self):
        distance_vector_matrix = self.particles.positions[:, np.newaxis, :] - self.particles.positions[np.newaxis, :, :]
        return distance_vector_matrix

    #Aufstellung einer Matrix, deren Einträge die Länge der Richtungsvektoren (Distanzen zwischen allen Partikelpaaren) enthalten. Shape (N,N)
    def compute_distances(self):
        distance_scalar_matrix= np.linalg.norm(self.compute_distance_vector_matrix(),axis=2)
        return distance_scalar_matrix

    #Aufstellung einer Matrix, deren Einträge die Einheitsvektoren der Richtungsvektoren enthalten. Shape (N,N,2)
    def compute_unit_vectors(self):
        #division durch null vermeiden
        distances= np.where(self.compute_distances()==0,sys.float_info.min,self.compute_distances()) #sys.float_info.min: der kleinste Wert in Python
        drx_vector_matrix= self.compute_distance_vector_matrix()/distances[:,:,np.newaxis]
        return drx_vector_matrix

    #Aufstellung einer Matrix, deren Einträge die Kräfte (als Scalar) zwischen allen Partikelpaaren enthalten. Shape (N,N)
    def compute_forces(self):
        force_variable_matrix=  1 - (self.compute_distances()/self.max_r)
        # if distance > max_r --> force_variable=0
        force_variable_matrix= np.clip(force_variable_matrix, 0.0, 1)
        force_scalar_matrix= self.interaction.get_rule_grid(self.particles.types) * force_variable_matrix
        return force_scalar_matrix

    #Aufstellung einer Matrix, deren Einträge die Kräfte (als Vektor) zwischen jeden Partikelpaaren enthalten. Shape: (N,N,2)
    def compute_force_vector(self):
        force_vektor_matrix= self.compute_forces()[:,:,np.newaxis] * self.compute_unit_vectors()
        return force_vektor_matrix

    #Berechnung des endgültigen Numpy-Arrays, nachdem alle Kräfte, die auf jedes Partikel agieren, summiert werden. Shape: (N,2)
    def compute_total_forces(self):
        return np.sum(self.compute_force_vector(), axis=1)

    #Berechnung neuer Beschleunigungen. Annahme: Jedes Partikel wiegt 1 kg, deswegen F=a
    def update_accelerations(self):
        self.particles.accelerations += self.compute_total_forces()

    #Berechnung neuer Geschwindigkeiten und Positionen: Aus den Formeln: dv/dt = a und ds/dt = v
    def update_velocities(self):
        self.particles.velocities += self.particles.accelerations * self.dt
        self.particles.velocities *= (1 - (self.friction * self.dt))

    def update_positions(self):
        self.particles.positions += self.particles.velocities * self.dt



#simulation= Simulation(0.1,0.1,0.1, ParticleSystem(16,4), Interaction(4))
#for i in range(100):
    #simulation.update_accelerations()
    #simulation.update_velocities()
    #simulation.update_positions()
    #print(simulation.particles.positions[:5])