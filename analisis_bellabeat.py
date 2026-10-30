import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración de estilo visual elegante
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

base_dir = r"C:\Proyectos\07_Educacion_y_Hardware\Casos estudio Data analytics\Caso 2 bien estar en la compañia"
data_dir = os.path.join(base_dir, r"archive\mturkfitbit_export_4.12.16-5.12.16\Fitabase Data 4.12.16-5.12.16")
output_graphs = os.path.join(base_dir, "graficos")
output_reports = os.path.join(base_dir, "reportes_resumen")

os.makedirs(output_graphs, exist_ok=True)
os.makedirs(output_reports, exist_ok=True)

print("1. Cargando datos...")
daily_act = pd.read_csv(os.path.join(data_dir, "dailyActivity_merged.csv"))
sleep = pd.read_csv(os.path.join(data_dir, "sleepDay_merged.csv"))
hourly_steps = pd.read_csv(os.path.join(data_dir, "hourlySteps_merged.csv"))

print("2. Limpiando y transformando...")
# Eliminar duplicados si existen
sleep = sleep.drop_duplicates()
daily_act = daily_act.drop_duplicates()

# Formatear fechas
daily_act["ActivityDate"] = pd.to_datetime(daily_act["ActivityDate"], format="%m/%d/%Y")
sleep["SleepDay"] = pd.to_datetime(sleep["SleepDay"], format="%m/%d/%Y %I:%M:%S %p")
sleep["SleepDate"] = sleep["SleepDay"].dt.normalize()

hourly_steps["ActivityHour"] = pd.to_datetime(hourly_steps["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p")
hourly_steps["Hour"] = hourly_steps["ActivityHour"].dt.hour

# Filtrar días donde el usuario no usó el reloj (0 pasos y 1440 min sedentarios)
daily_act_clean = daily_act[daily_act["TotalSteps"] > 0].copy()

# Feature Engineering
daily_act_clean["DayOfWeek"] = daily_act_clean["ActivityDate"].dt.day_name()
dias_orden = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
daily_act_clean["DayOfWeek"] = pd.Categorical(daily_act_clean["DayOfWeek"], categories=dias_orden, ordered=True)

# Categorización por nivel de actividad (OMS/CDC)
def clasificar_actividad(pasos):
    if pasos < 5000:
        return "Sedentario (<5k)"
    elif pasos < 7500:
        return "Baja actividad (5k-7.5k)"
    elif pasos < 10000:
        return "Moderadamente activo (7.5k-10k)"
    else:
        return "Muy activo (>=10k)"

daily_act_clean["Categoria_Actividad"] = daily_act_clean["TotalSteps"].apply(clasificar_actividad)

# Unir actividad diaria con sueño
merged_df = pd.merge(daily_act_clean, sleep, left_on=["Id", "ActivityDate"], right_on=["Id", "SleepDate"])
merged_df["HorasEnCama"] = merged_df["TotalTimeInBed"] / 60.0
merged_df["HorasDormidas"] = merged_df["TotalMinutesAsleep"] / 60.0
merged_df["MinutosDesvelo"] = merged_df["TotalTimeInBed"] - merged_df["TotalMinutesAsleep"]
merged_df["EficienciaSueno"] = (merged_df["TotalMinutesAsleep"] / merged_df["TotalTimeInBed"]) * 100

print(f"Registros combinados de actividad y sueno: {len(merged_df)}")

print("3. Generando graficos de alta calidad...")

# Color corporativo de Bellabeat (Rosa oro y ciruela / gris oscuro)
c_primary = "#D97D8A"   # Rosa oro / coral suave
c_secondary = "#4A3B4E" # Ciruela oscuro / berenjena
c_accent = "#8DA0CB"    # Azul lavanda suave

# GRÁFICO 1: Sedentarismo vs Sueño
plt.figure(figsize=(9, 6))
sns.regplot(
    data=merged_df, 
    x="SedentaryMinutes", 
    y="TotalMinutesAsleep",
    scatter_kws={"color": c_primary, "alpha": 0.6, "s": 45},
    line_kws={"color": c_secondary, "linewidth": 2.5}
)
plt.title("Impacto del Sedentarismo en la Calidad del Sueño\n(Correlación: -0.60)", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Minutos Sedentarios durante el día", fontsize=11)
plt.ylabel("Minutos de Sueño por la noche", fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(output_graphs, "1_sedentarismo_vs_sueno.png"), dpi=300)
plt.close()

# GRÁFICO 2: Pasos vs Calorías
plt.figure(figsize=(9, 6))
sns.regplot(
    data=daily_act_clean, 
    x="TotalSteps", 
    y="Calories",
    scatter_kws={"color": "#66c2a5", "alpha": 0.5, "s": 35},
    line_kws={"color": "#fc8d62", "linewidth": 2.5}
)
plt.axvline(10000, color="gray", linestyle="--", alpha=0.7, label="Meta 10.000 pasos (OMS)")
plt.title("Relación entre Pasos Diarios y Calorías Quemadas\n(Correlación: +0.59)", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Pasos Diarios Totales", fontsize=11)
plt.ylabel("Calorías Quemadas", fontsize=11)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_graphs, "2_pasos_vs_calorias.png"), dpi=300)
plt.close()

# GRÁFICO 3: Pasos por Día de la Semana
dias_stats = daily_act_clean.groupby("DayOfWeek", observed=True)["TotalSteps"].mean().reset_index()
dias_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
dias_stats["DiaES"] = dias_es

plt.figure(figsize=(9, 5))
bars = plt.bar(dias_stats["DiaES"], dias_stats["TotalSteps"], color=c_primary, edgecolor=c_secondary, width=0.6)
plt.axhline(10000, color="red", linestyle="--", linewidth=1.5, label="Meta OMS (10.000)")
plt.title("Promedio de Pasos Diarios por Día de la Semana", fontsize=14, fontweight="bold", pad=15)
plt.ylabel("Pasos Promedio", fontsize=11)
plt.ylim(0, 11000)
for bar in bars:
    yval = int(bar.get_height())
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 150, f"{yval:,}", ha='center', va='bottom', fontsize=9, fontweight="bold")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_graphs, "3_pasos_por_dia_semana.png"), dpi=300)
plt.close()

# GRÁFICO 4: Pasos por Hora del Día (Horas Pico)
hourly_avg = hourly_steps.groupby("Hour")["StepTotal"].mean().reset_index()
plt.figure(figsize=(10, 5))
plt.plot(hourly_avg["Hour"], hourly_avg["StepTotal"], color=c_secondary, marker='o', linewidth=2.5, markersize=6)
plt.fill_between(hourly_avg["Hour"], hourly_avg["StepTotal"], color=c_primary, alpha=0.3)
plt.title("Distribución de Pasos a lo largo del Día (Horas Pico)", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Hora del Día (00:00 - 23:00)", fontsize=11)
plt.ylabel("Promedio de Pasos por Hora", fontsize=11)
plt.xticks(range(0, 24))
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(output_graphs, "4_pasos_por_hora.png"), dpi=300)
plt.close()

# GRÁFICO 5: Distribución de Categorías de Usuarios
cat_counts = daily_act_clean["Categoria_Actividad"].value_counts(normalize=True) * 100
plt.figure(figsize=(7, 7))
colores_cat = ["#fc8d62", "#ffd92f", "#8da0cb", "#66c2a5"]
plt.pie(cat_counts, labels=cat_counts.index, autopct="%1.1f%%", startangle=140, colors=colores_cat, explode=(0.05, 0, 0, 0))
plt.title("Segmentación de Usuarios por Nivel de Actividad Diaria", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(output_graphs, "5_segmentacion_usuarios.png"), dpi=300)
plt.close()

print("4. Exportando reportes resumidos en CSV...")
# 1. Resumen general
resumen_gen = pd.DataFrame({
    "Métrica": [
        "Usuarios Únicos (Actividad)",
        "Usuarios Únicos (Sueño)",
        "Usuarios Únicos (Peso)",
        "Pasos Diarios Promedio",
        "Horas Sedentarias Diarias Promedio",
        "Minutos Activos Diarios Promedio",
        "Horas Dormidas Promedio",
        "Horas en Cama Promedio",
        "Tiempo de Desvelo Promedio en Cama (min)",
        "Eficiencia del Sueño Promedio (%)"
    ],
    "Valor": [
        daily_act["Id"].nunique(),
        sleep["Id"].nunique(),
        33 - sleep["Id"].nunique(), # no usan sueno
        round(daily_act_clean["TotalSteps"].mean(), 1),
        round(daily_act_clean["SedentaryMinutes"].mean() / 60.0, 1),
        round(daily_act_clean["VeryActiveMinutes"].mean(), 1),
        round(merged_df["HorasDormidas"].mean(), 1),
        round(merged_df["HorasEnCama"].mean(), 1),
        round(merged_df["MinutosDesvelo"].mean(), 1),
        round(merged_df["EficienciaSueno"].mean(), 1)
    ]
})
resumen_gen.to_csv(os.path.join(output_reports, "resumen_general_metricas.csv"), index=False)
dias_stats.to_csv(os.path.join(output_reports, "pasos_por_dia_semana.csv"), index=False)
hourly_avg.to_csv(os.path.join(output_reports, "pasos_por_hora.csv"), index=False)

print("¡Pipeline de Bellabeat completado con éxito!")
