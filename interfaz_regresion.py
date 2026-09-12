import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


# Variable donde guardaremos el dataset
df = None
datos_numericos = None


def cargar_dataset():
    global df, datos_numericos

    # Abrir ventana para seleccionar archivo
    ruta = filedialog.askopenfilename(
        title="Seleccionar dataset",
        filetypes=[("Archivos CSV", "*.csv")]
    )

    # Si el usuario cancela, no hacemos nada
    if not ruta:
        return

    try:
        # Cargar TODO el dataset
        df = pd.read_csv(ruta)

        # Seleccionar automáticamente las columnas numéricas
        datos_numericos = df.select_dtypes(include="number")

        # Excluir Person_ID porque es un identificador
        if "Person_ID" in datos_numericos.columns:
            datos_numericos = datos_numericos.drop(columns=["Person_ID"])

        # Obtener nombres de las variables numéricas
        columnas_numericas = datos_numericos.columns.tolist()

        # Cargar las variables en los selectores
        combo_x["values"] = columnas_numericas
        combo_y["values"] = columnas_numericas

        # Actualizar información en la interfaz
        etiqueta_archivo.config(
            text=f"Dataset cargado correctamente\n"
                 f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}"
        )

        messagebox.showinfo(
            "Dataset cargado",
            "El dataset se cargó correctamente."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No fue posible cargar el dataset.\n\n{error}"
        )


# -----------------------------------------
# VENTANA PRINCIPAL
# -----------------------------------------

def mostrar_matriz():
    if datos_numericos is None:
        messagebox.showwarning(
            "Advertencia",
            "Primero debes cargar un dataset."
        )
        return

    # Calcular matriz de correlación
    matriz_correlacion = datos_numericos.corr()

    # Crear mapa de calor
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

def realizar_regresion():
    if datos_numericos is None:
        messagebox.showwarning(
            "Advertencia",
            "Primero debes cargar un dataset."
        )
        return

    # Obtener variables seleccionadas
    variable_x = combo_x.get()
    variable_y = combo_y.get()

    # Validar que se hayan seleccionado ambas variables
    if variable_x == "" or variable_y == "":
        messagebox.showwarning(
            "Advertencia",
            "Debes seleccionar las variables X e Y."
        )
        return

    # Evitar seleccionar la misma variable
    if variable_x == variable_y:
        messagebox.showwarning(
            "Advertencia",
            "Las variables X e Y deben ser diferentes."
        )
        return

    # Seleccionar las dos variables y eliminar valores faltantes
    datos_regresion = datos_numericos[
        [variable_x, variable_y]
    ].dropna()

    # Variable independiente y dependiente
    X = datos_regresion[[variable_x]]
    y = datos_regresion[variable_y]

    # Crear y entrenar modelo
    modelo = LinearRegression()
    modelo.fit(X, y)

    # Obtener resultados
    pendiente = modelo.coef_[0]
    intercepto = modelo.intercept_
    r2 = modelo.score(X, y)
    correlacion = datos_regresion[variable_x].corr(
        datos_regresion[variable_y]
    )

    # Mostrar resultados en la interfaz
    texto_resultados.config(
        text=(
            f"Registros utilizados: {len(datos_regresion)}\n"
            f"Correlación: {correlacion:.4f}\n"
            f"Pendiente: {pendiente:.4f}\n"
            f"Intercepto: {intercepto:.4f}\n"
            f"R²: {r2:.4f}\n\n"
            f"Ecuación:\n"
            f"{variable_y} = {intercepto:.4f} + "
            f"({pendiente:.4f} × {variable_x})"
        )
    )

    # Realizar predicciones
    y_pred = modelo.predict(X)

    # Crear gráfica
    plt.figure(figsize=(10, 6))

    plt.scatter(
        X[variable_x],
        y,
        alpha=0.3,
        label="Datos reales"
    )

    plt.plot(
        X[variable_x],
        y_pred,
        linewidth=2,
        label="Regresión lineal"
    )

    plt.xlabel(variable_x)
    plt.ylabel(variable_y)
    plt.title(
        f"Regresión lineal: {variable_x} vs {variable_y}"
    )

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

ventana = tk.Tk()

ventana.title("Análisis de Regresión Lineal")
ventana.geometry("750x650")


# Título
titulo = tk.Label(
    ventana,
    text="Análisis de Regresión Lineal",
    font=("Arial", 20, "bold")
)
titulo.pack(pady=30)


# Botón para cargar dataset
boton_cargar = tk.Button(
    ventana,
    text="Cargar dataset",
    font=("Arial", 12),
    command=cargar_dataset
)
boton_cargar.pack(pady=15)


# Información del dataset
etiqueta_archivo = tk.Label(
    ventana,
    text="No se ha cargado ningún dataset",
    font=("Arial", 11)
)
etiqueta_archivo.pack(pady=20)

# -----------------------------------------
# SELECCIÓN DE VARIABLES
# -----------------------------------------

frame_variables = tk.Frame(ventana)
frame_variables.pack(pady=20)

# Variable independiente X
tk.Label(
    frame_variables,
    text="Variable independiente (X):",
    font=("Arial", 11)
).grid(row=0, column=0, padx=10, pady=10)

combo_x = ttk.Combobox(
    frame_variables,
    state="readonly",
    width=25
)
combo_x.grid(row=0, column=1, padx=10, pady=10)


# Variable dependiente Y
tk.Label(
    frame_variables,
    text="Variable dependiente (Y):",
    font=("Arial", 11)
).grid(row=1, column=0, padx=10, pady=10)

combo_y = ttk.Combobox(
    frame_variables,
    state="readonly",
    width=25
)
combo_y.grid(row=1, column=1, padx=10, pady=10)

boton_matriz = tk.Button(
    ventana,
    text="Ver matriz de correlación",
    font=("Arial", 11),
    command=mostrar_matriz
)

boton_matriz.pack(pady=15)

boton_regresion = tk.Button(
    ventana,
    text="Realizar regresión",
    font=("Arial", 11),
    command=realizar_regresion
)

boton_regresion.pack(pady=10)

texto_resultados = tk.Label(
    ventana,
    text="",
    font=("Arial", 11),
    justify="left"
)

texto_resultados.pack(pady=10)

# Mantener abierta la ventana
ventana.mainloop()