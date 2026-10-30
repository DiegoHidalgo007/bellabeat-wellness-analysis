import pandas as pd
import os

path = r"C:\Proyectos\07_Educacion_y_Hardware\Casos estudio Data analytics\Caso 2 bien estar en la compañia\archive\mturkfitbit_export_4.12.16-5.12.16\Fitabase Data 4.12.16-5.12.16"

daily_act = pd.read_csv(os.path.join(path, "dailyActivity_merged.csv"))
sleep = pd.read_csv(os.path.join(path, "sleepDay_merged.csv"))
weight = pd.read_csv(os.path.join(path, "weightLogInfo_merged.csv"))
hourly_steps = pd.read_csv(os.path.join(path, "hourlySteps_merged.csv"))

print("=== RESUMEN DE LOS DATASETS ===")
print("dailyActivity :", len(daily_act), "filas |", daily_act["Id"].nunique(), "usuarios unicos")
print("sleepDay      :", len(sleep), "filas |", sleep["Id"].nunique(), "usuarios unicos")
print("weightLogInfo :", len(weight), "filas |", weight["Id"].nunique(), "usuarios unicos")
print("hourlySteps   :", len(hourly_steps), "filas |", hourly_steps["Id"].nunique(), "usuarios unicos")

print("\n--- Estadisticas de dailyActivity ---")
print(daily_act[["TotalSteps", "TotalDistance", "SedentaryMinutes", "VeryActiveMinutes", "Calories"]].describe().round(2))

print("\n--- Estadisticas de sleepDay ---")
print(sleep[["TotalMinutesAsleep", "TotalTimeInBed"]].describe().round(2))
