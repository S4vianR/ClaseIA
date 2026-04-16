import numpy as np
import pandas as pd
import matplotlib
import random

class Neurona:
    """
    Perceptrón simple basado en Rosenblatt (1957).
    Autor: Equipo 1
    Estudiantes:
        - Dalia Martinez
        - Marlene Martinez
        - Denisse Ramos
        - Reuben Rhienhart
    Materia: Inteligencia Artificial SCC-1012 ITCJ 2026
    """

    def __init__(self, n_entradas, tasa_aprendizaje=0.1):
        # Inicializar pesos con valores pequeños aleatorios
        # Inicializar bias (umbral θ negado)
        # Guardar la tasa de aprendizaje
        self.n_entradas = n_entradas
        self.tasa_aprendizaje = tasa_aprendizaje
        self.bias  = 0
        self.pesos = np.random.rand(n_entradas)

    def activacion(self, suma):
        # Función escalón de Heaviside:
        # Retorna 1 si suma >= 0, retorna 0 si suma < 0
        if suma>=0:
            return 1
        else:
            return 0

    def predecir(self, entradas):
        # Calcular: suma = Σ(w * x ) + biasᵢ ᵢ
        # Retornar activacion(suma)
        suma = np.dot(entradas, self.pesos) + self.bias
        return self.activacion(suma)

    def entrenar(self, X, y, epocas=100):
        historial_errores = []

        for epoca in range(epocas):
            errores_epoca = 0
            for xi,yi in zip(X,y):
                # Para cada época:
                # Para cada ejemplo (xi, yi):
                #   - prediccion = predecir(xi)
                prediccion = self.predecir(xi)
                #   - error = yi - prediccion
                error = yi - prediccion

                #   - w ← w + tasa * error * xi
                #   - bias ← bias + tasa * error
                if error != 0:
                    self.pesos += self.tasa_aprendizaje * error * xi
                    self.bias += self.tasa_aprendizaje * error
                    
                    errores_epoca += 1
            # Guardar el error total por época
            historial_errores.append(errores_epoca)

            if errores_epoca == 0:
                    print(f"¡Éxito! La neurona aprendió el patrón en la época {epoca + 1}")
                    break
            # Retornar historial de errores
            return historial_errores

if __name__ == "__main__":
    df = pd.read_csv("./dataset.csv")
    
    X = df[["asistencia","promedio"]].values
    y = df["clase"].values
    
    neurona = Neurona(2)

    print("Iniciando entrenamiento...")
    errores = neurona.entrenar(X, y)
    
    print("\nHistorial de errores por época:")
    print(errores)
    
    print("\nPesos finales aprendidos:", neurona.pesos)
    print("Bias final aprendido:", neurona.bias)

    nuevo_alumno = np.array([0.85, 0.90])
    prediccion_nuevo = neurona.predecir(nuevo_alumno)
    
    resultado = "Aprobado" if prediccion_nuevo == 1 else "Reprobado"
    print(f"\nPredicción para el nuevo alumno {nuevo_alumno}: {resultado}")
