import base64
from io import BytesIO
import numpy as np
from matplotlib import pyplot as plt

from PSO.PSO import PSO


class ChartGenerator:

    def rosenbrock_function(self, x):
        # Implementacja funkcji Rosenbrocka
        a = 1
        b = 100
        return (a - x[0]) ** 2 + b * (x[1] - x[0] ** 2) ** 2

    def drop_wave_function(self, x):
        # Implementacja funkcji Drop-Wave
        numerator = 1 + np.cos(12 * np.sqrt(x[0] ** 2 + x[1] ** 2))
        denominator = 0.5 * (x[0] ** 2 + x[1] ** 2) + 2
        return -numerator / denominator

    def generuj_wykres(self, num_particles, maxiter, cost_function):
        bounds = [(-10, 10), (-10, 10)]  # Przykładowe granice dla przestrzeni poszukiwań
        pso = PSO(cost_function, bounds, num_particles, maxiter)
        best_position, best_value, best_values = pso.run()

        plt.figure()
        plt.plot(best_values)  # Tworzy wykres z najlepszymi wartościami
        plt.title(f"Postęp optymalizacji PSO - Najlepsza wartość: {best_value}")
        plt.xlabel("Iteracja")
        plt.ylabel("Najlepsza znaleziona wartość")

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        # Zamknięcie figury po zapisaniu do bufora
        plt.close()

        buf.close()

        return image_base64

