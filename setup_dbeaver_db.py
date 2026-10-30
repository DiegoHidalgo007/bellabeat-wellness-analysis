import duckdb
import os

base_dir = r"C:\Proyectos\07_Educacion_y_Hardware\Casos estudio Data analytics\Caso 2 bien estar en la compañia"
data_dir = os.path.join(base_dir, r"archive\mturkfitbit_export_4.12.16-5.12.16\Fitabase Data 4.12.16-5.12.16")
db_path = os.path.join(base_dir, "bellabeat.duckdb")

con = duckdb.connect(db_path)

print("Creando tablas base en bellabeat.duckdb...")

# 1. Tabla de actividad diaria
act_csv = os.path.join(data_dir, "dailyActivity_merged.csv")
con.execute(f"""
CREATE OR REPLACE TABLE daily_activity AS 
SELECT * FROM read_csv_auto('{act_csv}', dateformat='%m/%d/%Y');
""")

# 2. Tabla de sueño
sleep_csv = os.path.join(data_dir, "sleepDay_merged.csv")
con.execute(f"""
CREATE OR REPLACE TABLE sleep_day AS 
SELECT * FROM read_csv_auto('{sleep_csv}');
""")

# 3. Tabla de pasos por hora
steps_csv = os.path.join(data_dir, "hourlySteps_merged.csv")
con.execute(f"""
CREATE OR REPLACE TABLE hourly_steps AS 
SELECT * FROM read_csv_auto('{steps_csv}');
""")

con.close()
print("¡Base de datos bellabeat.duckdb lista con las 3 tablas crudas cargadas!")
