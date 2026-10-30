import pandas as pd
import os

path = r"C:\Proyectos\07_Educacion_y_Hardware\Casos estudio Data analytics\Caso 2 bien estar en la compañia\archive\mturkfitbit_export_4.12.16-5.12.16\Fitabase Data 4.12.16-5.12.16"

daily_act = pd.read_csv(os.path.join(path, "dailyActivity_merged.csv"))
sleep = pd.read_csv(os.path.join(path, "sleepDay_merged.csv"))

daily_act["ActivityDate"] = pd.to_datetime(daily_act["ActivityDate"])
sleep["SleepDate"] = pd.to_datetime(sleep["SleepDay"]).dt.normalize()

merged = pd.merge(daily_act, sleep, left_on=["Id", "ActivityDate"], right_on=["Id", "SleepDate"])

# Correlaciones
corr = merged[["TotalSteps", "Calories", "SedentaryMinutes", "VeryActiveMinutes", "TotalMinutesAsleep", "TotalTimeInBed"]].corr()
print("=== MATRIZ DE CORRELACION ===")
print(corr.round(3))
