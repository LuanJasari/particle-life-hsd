from particles import ParticleSystem
from interaction import Interaction
import numpy as np

class Simulation:
    """
    dt: int : stellt die Zeitänderung dar.
    friction: int : repräsentiert die aus Reibung resultierende Verzögerung (Deceleration due to kinetic friction)
    rmax: int : der maximale Abstand für Interaktion
    ax, ay: die initialen Beschleunigung --> 0
    """

    def __init__(self,dt,friction,max_r):
        self.dt = dt
        self.friction = friction
        self.max_r = max_r
        self.interaction = Interaction(4)
        self.particles = ParticleSystem(2000,4)
        self.ax=0
        self.ay=0

    #Distanz zwischen 2 Partikeln berechnen
    """
    Da alle Partikelpositionen (x,y) in einem array gespeichert wurden, brauchen wir 2 Schleifen.
    Um für jedes Partikelpaar, p1 und p2, die x und y Koordinaten abzurufen, den Vektor zwischen den beiden zu berechnen und dann die Länge.

    """
    def calculate_distance(self):
        for idx,p1 in enumerate(self.particles.get_positions()):
            for i in range(idx+1,len(self.particles.get_positions())):
                p2= self.particles.get_positions()[i]
                vector_p1_p2= p2[0] - p1[0], p2[1] - p1[1]
                distance = (vector_p1_p2[0]**2 + vector_p1_p2[1]**2)**0.5
                return distance

    #Beschleunigung jedes einzelne Partikel updaten. Aus Physik: F=ma. m wird hier erstmal vernachlässigt.
    def update_acceleration(self,fx,fy):
        self.ax+=fx
        self.ay+=fy
        return self.ax,self.ay

    #neuer Beschleunigungsvektor-->neuer Geschwindigkeitsvektor. Aus Physik: a=dv/dt
    #Dazu betrachten wir auch die Reibung
    def update_velocity(self,ax,ay):
        for idx, velocities in enumerate(self.particles.velocities):
            vx=velocities[0]
            vy=velocities[1]
            vx+=ax*self.dt
            vy+=ay*self.dt

            vx-=self.friction*self.dt
            vy-=self.friction*self.dt

            self.particles.velocities[idx]=vx,vy

    # Positionen für die Partikel updaten.  Aus Physik: v= Positionsänderung/Zeitänderung
    def update_positions(self,vx,vy):
        for idx,position in self.particles.get_positions():
            position[0]+=vx*self.dt
            position[1]+=vy*self.dt

            self.particles.get_positions()[idx]=position[0],position[1]