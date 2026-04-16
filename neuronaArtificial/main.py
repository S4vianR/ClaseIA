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
        self.w = np.random.rand(n_entradas)

    def activacion(self, suma):
        # Función escalón de Heaviside:
        # Retorna 1 si suma >= 0, retorna 0 si suma < 0
        if suma>=0:
            return 1
        else:
            return 0

    def predecir(self, entradas):
        for x in range(entradas):
            x+=1
            print(x)
        # Calcular: suma = Σ(w * x ) + biasᵢ ᵢ
        # Retornar activacion(suma)

    def entrenar(self, X, y, epocas=100):
        # Para cada época:
        # Para cada ejemplo (xi, yi):
        #   - prediccion = predecir(xi)
        #   - error = yi - prediccion
        #   - w ← w + tasa * error * xi
        #   - bias ← bias + tasa * error
        # Guardar el error total por época
        # Retornar historial de errores
        pass


if __name__ == "__main__":
    df = pd.read_csv("./dataset.csv")
    
    X = df[["asistencia","promedio"]].values
    y = df["clase"].values
    
    neurona = Neurona(2)
    # neurona.entrenar(X,y)
    neurona.predecir(neurona.n_entradas)
