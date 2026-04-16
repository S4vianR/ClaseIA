import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

    def graficar_resultados(self, X, y, historial_errores):
        """
        Genera y guarda una figura con la frontera de decisión y la curva de aprendizaje.
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Resultados del Entrenamiento del Perceptrón', fontsize=16)

        # --- Subgráfica 1: Frontera de decisión ---
        X_riesgo = X[y == 1]
        X_sin_riesgo = X[y == 0]

        # Graficar los puntos
        ax1.scatter(X_riesgo[:, 0], X_riesgo[:, 1], color='red', label='Riesgo (1)', marker='o')
        ax1.scatter(X_sin_riesgo[:, 0], X_sin_riesgo[:, 1], color='green', label='Sin riesgo (0)', marker='x')

        # Calcular la línea de frontera: w0*x1 + w1*x2 + bias = 0
        w_asistencia = self.pesos[0]
        w_promedio = self.pesos[1]

        # Tomar el valor mínimo y máximo de la asistencia para trazar la línea de orilla a orilla
        x_min, x_max = X[:, 0].min(), X[:, 0].max()
        x_frontera = np.array([x_min, x_max])

        if w_promedio != 0:
            y_frontera = -(w_asistencia * x_frontera + self.bias) / w_promedio
            ax1.plot(x_frontera, y_frontera, color='blue', linestyle='--', label='Frontera de decisión')

        # Configurar Subgráfica 1
        ax1.set_xlabel('Asistencia', fontsize=12)
        ax1.set_ylabel('Promedio', fontsize=12)
        ax1.set_title('Subgráfica 1 - Frontera de Decisión', fontsize=14)
        ax1.legend(loc='best')

        # --- Subgráfica 2: Curva de aprendizaje ---
        epocas = range(1, len(historial_errores) + 1)
        ax2.plot(epocas, historial_errores, color='purple', linestyle='-', marker='o')

        # Configurar Subgráfica 2
        ax2.set_xlabel('Época', fontsize=12)
        ax2.set_ylabel('Error Total (Clasificaciones incorrectas)', fontsize=12)
        ax2.set_title('Subgráfica 2 - Curva de Aprendizaje', fontsize=14)
        ax2.grid(True, linestyle='--', alpha=0.7)

        # --- Guardar la figura ---
        plt.tight_layout() # Ajusta los espacios para que no se empalme el texto
        nombre_archivo = 'visualizacion_entrenamiento.png'
        plt.savefig(nombre_archivo, dpi=300)
        print(f"¡Gráfica generada y guardada exitosamente como '{nombre_archivo}'!")

        # plt.show()


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

    neurona.graficar_resultados(X, y, errores)

    nuevo_alumno = np.array([0.85, 0.90])
    prediccion_nuevo = neurona.predecir(nuevo_alumno)
    
    resultado = "Aprobado" if prediccion_nuevo == 1 else "Reprobado"
    print(f"\nPredicción para el nuevo alumno {nuevo_alumno}: {resultado}")
