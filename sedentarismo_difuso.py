import tkinter as tk
from tkinter import messagebox
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ==========================================
# SISTEMA DE RAZONAMIENTO DIFUSO
# ==========================================

def crear_sistema_difuso():

    # ======================================
    # 1. VARIABLES DE ENTRADA Y SALIDA
    # ======================================

    # Minutos de ejercicio al día: 0 a 120
    ejercicio = ctrl.Antecedent(
        np.arange(0, 121, 1),
        'ejercicio'
    )

    # Horas sentado al día: 0 a 24
    sentado = ctrl.Antecedent(
        np.arange(0, 25, 1),
        'sentado'
    )

    # Horas frente a pantallas al día: 0 a 24
    pantalla = ctrl.Antecedent(
        np.arange(0, 25, 1),
        'pantalla'
    )

    # Riesgo de sedentarismo: 0 a 100
    riesgo = ctrl.Consequent(
        np.arange(0, 101, 1),
        'riesgo'
    )


    # ======================================
    # 2. CONJUNTOS DIFUSOS
    # ======================================

    # --------------------------------------
    # EJERCICIO
    # --------------------------------------

    ejercicio['bajo'] = fuzz.trimf(
        ejercicio.universe,
        [0, 0, 40]
    )

    ejercicio['medio'] = fuzz.trimf(
        ejercicio.universe,
        [20, 50, 80]
    )

    ejercicio['alto'] = fuzz.trimf(
        ejercicio.universe,
        [60, 120, 120]
    )


    # --------------------------------------
    # HORAS SENTADO
    # --------------------------------------

    sentado['pocas'] = fuzz.trimf(
        sentado.universe,
        [0, 0, 6]
    )

    sentado['moderadas'] = fuzz.trimf(
        sentado.universe,
        [4, 8, 12]
    )

    sentado['muchas'] = fuzz.trimf(
        sentado.universe,
        [10, 24, 24]
    )


    # --------------------------------------
    # HORAS FRENTE A PANTALLAS
    # --------------------------------------

    pantalla['bajas'] = fuzz.trimf(
        pantalla.universe,
        [0, 0, 4]
    )

    pantalla['moderadas'] = fuzz.trimf(
        pantalla.universe,
        [2, 6, 10]
    )

    pantalla['altas'] = fuzz.trimf(
        pantalla.universe,
        [8, 24, 24]
    )


    # --------------------------------------
    # RIESGO DE SEDENTARISMO
    # --------------------------------------

    riesgo['bajo'] = fuzz.trimf(
        riesgo.universe,
        [0, 0, 40]
    )

    riesgo['medio'] = fuzz.trimf(
        riesgo.universe,
        [25, 50, 75]
    )

    riesgo['alto'] = fuzz.trimf(
        riesgo.universe,
        [60, 100, 100]
    )


    # ======================================
    # 3. REGLAS DIFUSAS
    # ======================================

    # REGLA 1
    # Si el ejercicio es bajo Y pasa muchas
    # horas sentado -> riesgo alto
    regla1 = ctrl.Rule(
        ejercicio['bajo'] & sentado['muchas'],
        riesgo['alto']
    )


    # REGLA 2
    # Si el ejercicio es bajo Y pasa muchas
    # horas frente a pantallas -> riesgo alto
    regla2 = ctrl.Rule(
        ejercicio['bajo'] & pantalla['altas'],
        riesgo['alto']
    )


    # REGLA 3
    # Si el ejercicio es medio Y las horas
    # sentado son moderadas -> riesgo medio
    regla3 = ctrl.Rule(
        ejercicio['medio'] & sentado['moderadas'],
        riesgo['medio']
    )


    # REGLA 4
    # Si el ejercicio es alto Y pasa pocas
    # horas sentado -> riesgo bajo
    regla4 = ctrl.Rule(
        ejercicio['alto'] & sentado['pocas'],
        riesgo['bajo']
    )


    # REGLA 5
    # Si el ejercicio es alto Y pasa pocas
    # horas frente a pantallas -> riesgo bajo
    regla5 = ctrl.Rule(
        ejercicio['alto'] & pantalla['bajas'],
        riesgo['bajo']
    )


    # REGLA 6
    # Si pasa muchas horas sentado Y muchas
    # horas frente a pantallas -> riesgo alto
    regla6 = ctrl.Rule(
        sentado['muchas'] & pantalla['altas'],
        riesgo['alto']
    )


    # REGLA 7
    # Si hace ejercicio medio PERO pasa
    # muchas horas sentado -> riesgo alto
    regla7 = ctrl.Rule(
        ejercicio['medio'] & sentado['muchas'],
        riesgo['alto']
    )


    # REGLA 8
    # Si hace ejercicio medio Y pasa muchas
    # horas frente a pantallas -> riesgo medio
    regla8 = ctrl.Rule(
        ejercicio['medio'] & pantalla['altas'],
        riesgo['medio']
    )


    # REGLA 9
    # Si hace ejercicio alto PERO pasa horas
    # moderadas sentado -> riesgo medio
    regla9 = ctrl.Rule(
        ejercicio['alto'] & sentado['moderadas'],
        riesgo['medio']
    )


    # ======================================
    # 4. CREAR SISTEMA DE CONTROL
    # ======================================

    sistema = ctrl.ControlSystem([
        regla1,
        regla2,
        regla3,
        regla4,
        regla5,
        regla6,
        regla7,
        regla8,
        regla9
    ])

    return sistema


# ==========================================
# CREAR EL SISTEMA DIFUSO
# ==========================================

sistema_difuso = crear_sistema_difuso()


# ==========================================
# FUNCIÓN EVALUAR
# ==========================================

def evaluar():

    try:

        # Obtener los datos ingresados
        minutos_ejercicio = float(
            entrada_ejercicio.get()
        )

        horas_sentado = float(
            entrada_sentado.get()
        )

        horas_pantalla = float(
            entrada_pantalla.get()
        )


        # ==================================
        # VALIDAR LOS DATOS
        # ==================================

        if minutos_ejercicio < 0 or minutos_ejercicio > 120:

            messagebox.showwarning(
                "Dato incorrecto",
                "Los minutos de ejercicio deben estar "
                "entre 0 y 120."
            )

            return


        if horas_sentado < 0 or horas_sentado > 24:

            messagebox.showwarning(
                "Dato incorrecto",
                "Las horas sentado deben estar "
                "entre 0 y 24."
            )

            return


        if horas_pantalla < 0 or horas_pantalla > 24:

            messagebox.showwarning(
                "Dato incorrecto",
                "Las horas frente a pantallas deben estar "
                "entre 0 y 24."
            )

            return


        # ==================================
        # CREAR SIMULACIÓN
        # ==================================

        simulador = ctrl.ControlSystemSimulation(
            sistema_difuso
        )


        # ==================================
        # ENVIAR VALORES AL SISTEMA
        # ==================================

        simulador.input['ejercicio'] = minutos_ejercicio

        simulador.input['sentado'] = horas_sentado

        simulador.input['pantalla'] = horas_pantalla


        # ==================================
        # EJECUTAR RAZONAMIENTO DIFUSO
        # ==================================

        simulador.compute()


        # ==================================
        # OBTENER RESULTADO
        # ==================================

        resultado = simulador.output['riesgo']


        # ==================================
        # CLASIFICAR EL RESULTADO
        # ==================================

        if resultado < 35:

            nivel = "BAJO"

            recomendacion = (
                "Mantienes buenos hábitos. "
                "Continúa realizando actividad física "
                "y evitando periodos prolongados sentado."
            )


        elif resultado < 65:

            nivel = "MEDIO"

            recomendacion = (
                "Procura realizar más actividad física, "
                "hacer pausas activas y disminuir los "
                "periodos prolongados sentado."
            )


        else:

            nivel = "ALTO"

            recomendacion = (
                "Se recomienda aumentar la actividad física, "
                "realizar pausas activas y reducir el tiempo "
                "sentado y frente a pantallas."
            )


        # ==================================
        # MOSTRAR RESULTADO
        # ==================================

        txt_resultado.delete(
            "1.0",
            tk.END
        )

        txt_resultado.insert(
            tk.END,
            "RESULTADO DEL SISTEMA DIFUSO\n\n"
        )

        txt_resultado.insert(
            tk.END,
            f"Riesgo de sedentarismo: "
            f"{resultado:.2f}/100\n\n"
        )

        txt_resultado.insert(
            tk.END,
            f"Nivel de riesgo: {nivel}\n\n"
        )

        txt_resultado.insert(
            tk.END,
            "Recomendación:\n"
        )

        txt_resultado.insert(
            tk.END,
            recomendacion
        )


    # ======================================
    # ERROR SI NO INGRESA NÚMEROS
    # ======================================

    except ValueError:

        messagebox.showwarning(
            "Advertencia",
            "Por favor ingresa valores numéricos "
            "en todos los campos."
        )


    # ======================================
    # OTRO ERROR
    # ======================================

    except Exception as error:

        messagebox.showwarning(
            "Advertencia",
            "No fue posible calcular el resultado.\n\n"
            f"Detalle: {error}"
        )


# ==========================================
# FUNCIÓN LIMPIAR
# ==========================================

def limpiar():

    entrada_ejercicio.delete(
        0,
        tk.END
    )

    entrada_sentado.delete(
        0,
        tk.END
    )

    entrada_pantalla.delete(
        0,
        tk.END
    )

    txt_resultado.delete(
        "1.0",
        tk.END
    )


# ==========================================
# INTERFAZ GRÁFICA
# ==========================================

ventana = tk.Tk()


ventana.title(
    "Sistema Difuso - Prevención del Sedentarismo"
)


ventana.geometry(
    "750x680"
)


ventana.resizable(
    False,
    False
)


# ==========================================
# TÍTULO
# ==========================================

titulo = tk.Label(
    ventana,
    text="SISTEMA DE RAZONAMIENTO DIFUSO",
    font=("Arial", 20, "bold")
)

titulo.pack(
    pady=(30, 5)
)


subtitulo = tk.Label(
    ventana,
    text="Evaluación del Riesgo de Sedentarismo",
    font=("Arial", 15)
)

subtitulo.pack(
    pady=(0, 30)
)


# ==========================================
# ENTRADA 1: EJERCICIO
# ==========================================

tk.Label(
    ventana,
    text="Minutos de ejercicio al día (0 - 120):",
    font=("Arial", 11, "bold")
).pack(
    pady=(10, 5)
)


entrada_ejercicio = tk.Entry(
    ventana,
    width=20,
    font=("Arial", 12),
    justify="center"
)

entrada_ejercicio.pack()


# ==========================================
# ENTRADA 2: HORAS SENTADO
# ==========================================

tk.Label(
    ventana,
    text="Horas sentado al día (0 - 24):",
    font=("Arial", 11, "bold")
).pack(
    pady=(20, 5)
)


entrada_sentado = tk.Entry(
    ventana,
    width=20,
    font=("Arial", 12),
    justify="center"
)

entrada_sentado.pack()


# ==========================================
# ENTRADA 3: PANTALLA
# ==========================================

tk.Label(
    ventana,
    text="Horas frente a pantallas al día (0 - 24):",
    font=("Arial", 11, "bold")
).pack(
    pady=(20, 5)
)


entrada_pantalla = tk.Entry(
    ventana,
    width=20,
    font=("Arial", 12),
    justify="center"
)

entrada_pantalla.pack()


# ==========================================
# BOTONES
# ==========================================

frame_botones = tk.Frame(
    ventana
)

frame_botones.pack(
    pady=30
)


btn_evaluar = tk.Button(
    frame_botones,
    text="Evaluar",
    command=evaluar,
    width=15,
    font=("Arial", 11, "bold")
)

btn_evaluar.grid(
    row=0,
    column=0,
    padx=10
)


btn_limpiar = tk.Button(
    frame_botones,
    text="Limpiar",
    command=limpiar,
    width=15,
    font=("Arial", 11)
)

btn_limpiar.grid(
    row=0,
    column=1,
    padx=10
)


# ==========================================
# RESULTADOS
# ==========================================

tk.Label(
    ventana,
    text="Resultado:",
    font=("Arial", 12, "bold")
).pack()


txt_resultado = tk.Text(
    ventana,
    width=70,
    height=9,
    font=("Arial", 11),
    wrap="word"
)

txt_resultado.pack(
    pady=10
)


# ==========================================
# EJECUTAR PROGRAMA
# ==========================================

ventana.mainloop()