import tkinter as tk
from tkinter import messagebox, ttk
import clips


# ==========================================
# MOTOR EXPERTO CLIPS
# ==========================================

def crear_sistema_experto():

    env = clips.Environment()

    # REGLA 1
    env.build("""
    (defrule poco_ejercicio
        (ejercicio no)
        =>
        (assert (recomendacion "Realiza al menos 30 minutos de actividad fisica al dia."))
    )
    """)

    # REGLA 2
    env.build("""
    (defrule muchas_horas_sentado
        (horas_sentado muchas)
        =>
        (assert (recomendacion "Levantate y camina unos minutos cada hora."))
    )
    """)

    # REGLA 3
    env.build("""
    (defrule mucho_tiempo_pantalla
        (pantalla alta)
        =>
        (assert (recomendacion "Reduce el tiempo frente a pantallas y realiza pausas activas."))
    )
    """)

    # REGLA 4
    env.build("""
    (defrule no_caminar
        (camina no)
        =>
        (assert (recomendacion "Intenta caminar mas durante el dia, por ejemplo usando escaleras."))
    )
    """)

    # REGLA 5
    env.build("""
    (defrule no_pausas
        (pausas no)
        =>
        (assert (recomendacion "Realiza pausas activas durante el trabajo o estudio."))
    )
    """)

    # REGLA 6
    env.build("""
    (defrule riesgo_alto
        (ejercicio no)
        (horas_sentado muchas)
        (pausas no)
        =>
        (assert (recomendacion "Presentas un riesgo alto de sedentarismo. Es importante aumentar tu actividad fisica."))
    )
    """)

    # REGLA 7
    env.build("""
    (defrule buenos_habitos
        (ejercicio si)
        (horas_sentado pocas)
        (camina si)
        (pausas si)
        =>
        (assert (recomendacion "Tienes buenos habitos. Continua manteniendo una vida activa."))
    )
    """)

    return env


# ==========================================
# FUNCIÓN PARA EVALUAR AL USUARIO
# ==========================================

def evaluar():

    env = crear_sistema_experto()

    ejercicio = var_ejercicio.get()
    sentado = var_sentado.get()
    pantalla = var_pantalla.get()
    camina = var_camina.get()
    pausas = var_pausas.get()

    # Validar que todas las preguntas hayan sido respondidas
    if -1 in [ejercicio, sentado, pantalla, camina, pausas]:
        messagebox.showwarning(
            "Advertencia",
            "Por favor responde todas las preguntas."
        )
        return

    # Convertir las respuestas para CLIPS

    if ejercicio == 1:
        env.assert_string("(ejercicio si)")
    else:
        env.assert_string("(ejercicio no)")

    if sentado == 1:
        env.assert_string("(horas_sentado muchas)")
    else:
        env.assert_string("(horas_sentado pocas)")

    if pantalla == 1:
        env.assert_string("(pantalla alta)")
    else:
        env.assert_string("(pantalla baja)")

    if camina == 1:
        env.assert_string("(camina si)")
    else:
        env.assert_string("(camina no)")

    if pausas == 1:
        env.assert_string("(pausas si)")
    else:
        env.assert_string("(pausas no)")

    # Ejecutar las reglas de CLIPS
    env.run()

    recomendaciones = []

    for fact in env.facts():

        if fact.template.name == "recomendacion":
            recomendaciones.append(str(fact[0]))

    # Limpiar cuadro de resultado
    txt_resultado.delete("1.0", tk.END)

    if recomendaciones:

        txt_resultado.insert(
            tk.END,
            "RECOMENDACIONES DEL SISTEMA EXPERTO:\n\n"
        )

        for i, recomendacion in enumerate(recomendaciones, 1):
            txt_resultado.insert(
                tk.END,
                f"{i}. {recomendacion}\n\n"
            )

    else:
        txt_resultado.insert(
            tk.END,
            "No se encontraron recomendaciones."
        )


# ==========================================
# FUNCIÓN LIMPIAR
# ==========================================

def limpiar():

    var_ejercicio.set(-1)
    var_sentado.set(-1)
    var_pantalla.set(-1)
    var_camina.set(-1)
    var_pausas.set(-1)

    txt_resultado.delete("1.0", tk.END)


# ==========================================
# INTERFAZ GRÁFICA
# ==========================================

ventana = tk.Tk()

ventana.title("Sistema Experto - Prevención del Sedentarismo")
ventana.geometry("800x850")
ventana.resizable(True, True)

# Título
titulo = tk.Label(
    ventana,
    text="SISTEMA EXPERTO",
    font=("Arial", 22, "bold")
)

titulo.pack(pady=(20, 5))

subtitulo = tk.Label(
    ventana,
    text="Prevención del Sedentarismo",
    font=("Arial", 16)
)

subtitulo.pack(pady=(0, 20))


# ==========================================
# VARIABLES
# ==========================================

var_ejercicio = tk.IntVar(value=-1)
var_sentado = tk.IntVar(value=-1)
var_pantalla = tk.IntVar(value=-1)
var_camina = tk.IntVar(value=-1)
var_pausas = tk.IntVar(value=-1)


# ==========================================
# PREGUNTA 1
# ==========================================

tk.Label(
    ventana,
    text="1. ¿Realizas ejercicio regularmente?",
    font=("Arial", 11, "bold")
).pack()

tk.Radiobutton(
    ventana,
    text="Sí",
    variable=var_ejercicio,
    value=1
).pack()

tk.Radiobutton(
    ventana,
    text="No",
    variable=var_ejercicio,
    value=0
).pack()


# ==========================================
# PREGUNTA 2
# ==========================================

tk.Label(
    ventana,
    text="2. ¿Pasas muchas horas sentado durante el día?",
    font=("Arial", 11, "bold")
).pack(pady=(10, 0))

tk.Radiobutton(
    ventana,
    text="Sí",
    variable=var_sentado,
    value=1
).pack()

tk.Radiobutton(
    ventana,
    text="No",
    variable=var_sentado,
    value=0
).pack()


# ==========================================
# PREGUNTA 3
# ==========================================

tk.Label(
    ventana,
    text="3. ¿Pasas más de 4 horas al día frente a una pantalla?",
    font=("Arial", 11, "bold")
).pack(pady=(10, 0))

tk.Radiobutton(
    ventana,
    text="Sí",
    variable=var_pantalla,
    value=1
).pack()

tk.Radiobutton(
    ventana,
    text="No",
    variable=var_pantalla,
    value=0
).pack()


# ==========================================
# PREGUNTA 4
# ==========================================

tk.Label(
    ventana,
    text="4. ¿Caminas frecuentemente durante el día?",
    font=("Arial", 11, "bold")
).pack(pady=(10, 0))

tk.Radiobutton(
    ventana,
    text="Sí",
    variable=var_camina,
    value=1
).pack()

tk.Radiobutton(
    ventana,
    text="No",
    variable=var_camina,
    value=0
).pack()


# ==========================================
# PREGUNTA 5
# ==========================================

tk.Label(
    ventana,
    text="5. ¿Realizas pausas activas mientras estudias o trabajas?",
    font=("Arial", 11, "bold")
).pack(pady=(10, 0))

tk.Radiobutton(
    ventana,
    text="Sí",
    variable=var_pausas,
    value=1
).pack()

tk.Radiobutton(
    ventana,
    text="No",
    variable=var_pausas,
    value=0
).pack()


# ==========================================
# BOTONES
# ==========================================

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=20)

btn_evaluar = tk.Button(
    frame_botones,
    text="Evaluar",
    command=evaluar,
    width=15,
    font=("Arial", 11, "bold")
)

btn_evaluar.grid(row=0, column=0, padx=10)

btn_limpiar = tk.Button(
    frame_botones,
    text="Limpiar",
    command=limpiar,
    width=15
)

btn_limpiar.grid(row=0, column=1, padx=10)


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
    width=80,
    height=14,
    wrap="word",
    font=("Arial", 11)
)

txt_resultado.pack(pady=10)


# ==========================================
# EJECUTAR PROGRAMA
# ==========================================

ventana.mainloop()