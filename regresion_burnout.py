import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Cargar el dataset completo
df = pd.read_csv("mental_health_burnout_prediction_dataset.csv")

# Seleccionar únicamente las columnas numéricas
datos_numericos = df.select_dtypes(include="number")

# Eliminar Person_ID porque es un identificador
datos_numericos = datos_numericos.drop(columns=["Person_ID"])

print("\nColumnas que se utilizarán en el análisis:")
print(datos_numericos.columns.tolist())

print("\nCantidad de variables para el análisis:")
print(datos_numericos.shape[1])

# -----------------------------------------
# MATRIZ DE CORRELACIÓN
# -----------------------------------------

matriz_correlacion = datos_numericos.corr()

print("\nMatriz de correlación:")
print(matriz_correlacion)

# Mostrar correlaciones con Burnout_Score
correlaciones_burnout = matriz_correlacion["Burnout_Score"].sort_values(
    ascending=False
)

print("\nCorrelaciones con Burnout Score:")
print(correlaciones_burnout)

# -----------------------------------------
# GRÁFICA DE LA MATRIZ DE CORRELACIÓN
# -----------------------------------------

plt.figure(figsize=(14, 10))

sns.heatmap(
    matriz_correlacion,
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)

plt.title("Matriz de correlación")
plt.tight_layout()
plt.show()

# -----------------------------------------
# REGRESIÓN LINEAL
# -----------------------------------------

# Seleccionar las variables de la regresión
datos_regresion = datos_numericos[
    ["Anxiety_Score", "Burnout_Score"]
].dropna()

print("\nRegistros disponibles para la regresión:")
print(datos_regresion.shape[0])

# Variable independiente
X = datos_regresion[["Anxiety_Score"]]

# Variable dependiente
y = datos_regresion["Burnout_Score"]

# Crear y entrenar el modelo
modelo = LinearRegression()
modelo.fit(X, y)

# Realizar predicciones
y_pred = modelo.predict(X)

# Calcular error de la regresión
mse = mean_squared_error(y, y_pred)
rmse = mse ** 0.5

# Mostrar resultados de la regresión
print("\nResultados de la regresión lineal:")
print("Pendiente:", modelo.coef_[0])
print("Intercepto:", modelo.intercept_)
print("R²:", modelo.score(X, y))
print("Error cuadrático medio (MSE):", mse)
print("Raíz del error cuadrático medio (RMSE):", rmse)

# -----------------------------------------
# GRÁFICA DE REGRESIÓN LINEAL
# -----------------------------------------

# Crear gráfica
plt.figure(figsize=(10, 6))

# Datos reales
plt.scatter(
    X["Anxiety_Score"],
    y,
    alpha=0.3,
    label="Datos reales"
)

# Recta de regresión
plt.plot(
    X["Anxiety_Score"],
    y_pred,
    linewidth=2,
    label="Regresión lineal"
)

plt.xlabel("Puntaje de ansiedad")
plt.ylabel("Puntaje de burnout")
plt.title("Regresión lineal: Ansiedad vs Burnout")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()