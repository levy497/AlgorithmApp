import numpy as np

class Particle:
    def __init__(self, bounds):
        self.position = np.array([np.random.uniform(low, high) for low, high in bounds])
        self.velocity = np.random.rand(len(bounds))
        self.best_position = np.copy(self.position)
        self.best_value = float('inf')

class PSO:
    def __init__(self, cost_function, bounds, num_particles, maxiter):
        self.cost_function = cost_function
        self.bounds = bounds
        self.num_particles = num_particles
        self.maxiter = maxiter
        self.gbest_value = float('inf')
        self.gbest_position = np.array([np.random.uniform(low, high) for low, high in bounds])

        self.particles = [Particle(bounds) for _ in range(num_particles)]

    def run(self):
        best_values = []  # Lista do przechowywania najlepszych wartości

        for t in range(self.maxiter):
            for particle in self.particles:
                fitness_candidate = self.cost_function(particle.position)
                if particle.best_value > fitness_candidate:
                    particle.best_value = fitness_candidate
                    particle.best_position = particle.position

                if self.gbest_value > fitness_candidate:
                    self.gbest_value = fitness_candidate
                    self.gbest_position = particle.position

            best_values.append(self.gbest_value)

            for particle in self.particles:
                new_velocity = (np.random.rand(len(particle.velocity)) * particle.velocity +
                                2 * np.random.rand(len(particle.velocity)) * (particle.best_position - particle.position) +
                                2 * np.random.rand(len(particle.velocity)) * (self.gbest_position - particle.position))
                particle.velocity = new_velocity
                particle.position = particle.position + new_velocity

        return self.gbest_position, self.gbest_value, best_values

# Przykładowa implementacja cost_function
def cost_function(x):
    return np.sum(np.square(x))  # Sferyczna funkcja testowa
