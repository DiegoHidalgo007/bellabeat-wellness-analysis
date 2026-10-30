# Bitácora Integral Paso a Paso: Caso de Estudio 2 - Bellabeat
**Certificado Profesional de Análisis de Datos de Google (Google Data Analytics Capstone)**  
**Autor:** Diego Hidalgo  
**Fecha:** Octubre 2026  
**Stack Tecnológico:** SQL (DuckDB + DBeaver) | R & RStudio (tidyverse, ggplot2) | Power BI Desktop | Tableau Desktop | Python

---

## Índice
1. [Fase 1: Preguntar (Ask) - El Problema de Negocio](#fase-1-preguntar-ask)
2. [Fase 2: Preparar (Prepare) - Datos y Limitaciones](#fase-2-preparar-prepare)
3. [Fase 3: Procesar (Process) - Limpieza y Modelado SQL](#fase-3-procesar-process)
4. [Fase 4: Analizar (Analyze) - Consultas Clave y Descubrimientos](#fase-4-analizar-analyze)
5. [Fase 5: Compartir (Share) - Visualizaciones Multiplataforma](#fase-5-compartir-share)
   - [5.1 Reporte Reproducible en R Markdown](#51-rstudio--ggplot2)
   - [5.2 Dashboard Ejecutivo en Power BI](#52-power-bi-desktop)
   - [5.3 Modelo de Dispersión en Tableau](#53-tableau-desktop)
6. [Fase 6: Actuar (Act) - Estrategia de Marketing para Bellabeat](#fase-6-actuar-act)
7. [Próximos Pasos: Publicación en GitHub y Kaggle](#próximos-pasos)

---

## Fase 1: Preguntar (Ask)

### Contexto de la Empresa
**Bellabeat** es una compañía tecnológica de bienestar orientada a mujeres, fundada por Urška Sršen y Sando Mur. Sus productos combinan diseño elegante y moda con monitoreo biométrico:
- **Bellabeat Leaf:** Rastreador de salud clásico que puede usarse como pulsera, collar o clip.
- **Bellabeat Time:** Reloj analógico con sensores inteligentes.
- **Bellabeat Spring:** Botella inteligente de hidratación.
- **Bellabeat App:** Plataforma móvil que integra datos de actividad, sueño, estrés y salud femenina.

### Preguntas Estratégicas del Caso
1. ¿Cuáles son las tendencias actuales en el uso de dispositivos inteligentes de salud (smart trackers no-Bellabeat)?
2. ¿Cómo se aplican estas tendencias a las clientas potenciales de Bellabeat?
3. ¿Cómo pueden orientar la estrategia de marketing y el posicionamiento de la marca?

---

## Fase 2: Preparar (Prepare)

### Fuente de Datos
- **Dataset:** *FitBit Fitness Tracker Data* (Kaggle / Möbius).
- **Contenido:** 18 tablas CSV con registros de 33 usuarios de Amazon Mechanical Turk entre el 12 de abril y el 12 de mayo de 2016.

### Evaluación Crítica de Limitaciones (Criterios ROCCC de Google):
- **Tamaño Muestral Reducido:** 33 usuarios en actividad física, 24 en sueño y solo 8 en registro de peso.
- **Falta de Datos Demográficos:** El dataset no especifica género, lo que representa un sesgo para una empresa enfocada exclusivamente en mujeres.
- **Antigüedad:** Datos recolectados en 2016 (requiere validar si los hábitos de uso se mantienen en el tiempo).

---

## Fase 3: Procesar (Process)

### Arquitectura de Datos Local
1. Se construyó una base de datos local en **DuckDB** (`bellabeat.duckdb`) conectada a **DBeaver** para ejecutar SQL de alto rendimiento sin depender de servidores en la nube.
2. Se cargaron las tablas principales:
   - `daily_activity` (actividad diaria, pasos, calorías, minutos sedentarios y activos).
   - `sleep_day` (registros diarios de sueño: minutos dormidos y tiempo total en cama).
   - `hourly_steps` (pasos desglosados hora por hora durante las 24 horas).

### Depuración y Reglas de Negocio
- Eliminación de registros con 0 pasos y 1.440 minutos sedentarios (días en que el usuario no usó el dispositivo).
- Normalización de formatos de fecha (`CAST(s.SleepDay AS DATE)` y `ActivityDate`).
- Resolución de discrepancias de redondeo y delimitadores regionales (coma vs punto).

---

## Fase 4: Analizar (Analyze)

A lo largo del proyecto escribiste y validaste las siguientes consultas analíticas esenciales en DBeaver:

### 1. El Abandono del Monitoreo del Sueño (Fricción en la Muñeca)
```sql
SELECT 
    COUNT(DISTINCT a.Id) AS total_usuarios_actividad,
    COUNT(DISTINCT s.Id) AS usuarios_con_datos_sueno,
    COUNT(DISTINCT a.Id) - COUNT(DISTINCT s.Id) AS usuarios_sin_registro_sueno
FROM daily_activity a
LEFT JOIN sleep_day s ON a.Id = s.Id;
```
* **Hallazgo:** De 33 usuarios, **9 jamás registraron sueño (27.3%)**. Los smartwatches tradicionales son incómodos para dormir, lo que deja el camino abierto al diseño discreto del Bellabeat Leaf.

### 2. Métrica de Desvelo Promedio en Cama
```sql
SELECT 
    ROUND(AVG(s.TotalMinutesAsleep) / 60.0, 1) AS horas_dormidas,
    ROUND(AVG(s.TotalTimeInBed) / 60.0, 1) AS horas_en_cama,
    ROUND(AVG(s.TotalTimeInBed - s.TotalMinutesAsleep), 1) AS minutos_desvelo_promedio
FROM daily_activity a
JOIN sleep_day s ON a.Id = s.Id AND a.ActivityDate = CAST(s.SleepDay AS DATE);
```
* **Hallazgo:** Las usuarias duermen en promedio **7.0 horas**, pero pasan **7.6 horas en cama**. La diferencia representa **39.2 minutos despiertas en cama** intentando conciliar el sueño o al despertar.

### 3. Patrón Semanal de Movimiento
```sql
SELECT 
    dayname(ActivityDate) AS dia_semana,
    ROUND(AVG(TotalSteps), 0) AS pasos_promedio,
    ROUND(AVG(Calories), 0) AS calorias_promedio
FROM daily_activity
WHERE TotalSteps > 0
GROUP BY dayname(ActivityDate), dayofweek(ActivityDate)
ORDER BY dayofweek(ActivityDate);
```
* **Hallazgo:** Martes (8.949) y Sábado (8.947) son los días de mayor actividad. El Domingo presenta la mayor caída (7.627 pasos).

### 4. Detección del "Bajón Laboral" Horario (Picos y Caídas)
```sql
SELECT 
    hour(ActivityHour) AS hora_del_dia,
    ROUND(AVG(StepTotal), 0) AS pasos_promedio
FROM hourly_steps
GROUP BY hour(ActivityHour)
ORDER BY pasos_promedio DESC
LIMIT 3;
```
* **Hallazgo:**
  - **Pico de movimiento:** 17:00 a 19:00 hrs (~580 - 599 pasos/hora), correspondiente a la salida laboral.
  - **Caída laboral pronunciada:** A las 15:00 hrs (3 PM) el movimiento se desploma a 406 pasos/hora.

### 5. Impacto del Sedentarismo Extremo en el Descanso
```sql
SELECT 
    CASE 
        WHEN a.SedentaryMinutes >= 960 THEN 'Alto Sedentarismo (>= 16 horas)'
        ELSE 'Sedentarismo Moderado (< 16 horas)'
    END AS nivel_sedentarismo_dia,
    COUNT(*) AS total_dias_analizados,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS porcentaje_dias,
    ROUND(AVG(a.TotalSteps), 0) AS pasos_promedio,
    ROUND(AVG(s.TotalMinutesAsleep) / 60.0, 1) AS horas_dormidas_promedio,
    ROUND(AVG(s.TotalTimeInBed - s.TotalMinutesAsleep), 1) AS minutos_desvelo_promedio
FROM daily_activity a
JOIN sleep_day s ON a.Id = s.Id AND a.ActivityDate = CAST(s.SleepDay AS DATE)
GROUP BY nivel_sedentarismo_dia;
```
* **Hallazgo:** El 94.2% de los días (389 días) presentan sedentarismo moderado con 7.3 horas de sueño. En cambio, el 5.8% (24 días) con más de 16 horas sedentarias presentan un colapso en el sueño registrado (2.7 horas promedio).

### 6. Segmentación Estratégica de Usuarias (CTE)
```sql
WITH promedio_por_usuario AS (
    SELECT 
        Id,
        ROUND(AVG(TotalSteps), 0) AS pasos_promedio_diarios
    FROM daily_activity
    GROUP BY Id
)
SELECT 
    CASE 
        WHEN pasos_promedio_diarios < 5000 THEN '1. Sedentario (< 5.000 pasos)'
        WHEN pasos_promedio_diarios BETWEEN 5000 AND 7499 THEN '2. Baja Actividad (5.000 - 7.499)'
        WHEN pasos_promedio_diarios BETWEEN 7500 AND 9999 THEN '3. Algo Activo (7.500 - 9.999)'
        ELSE '4. Muy Activo (>= 10.000 pasos)'
    END AS tipo_usuario,
    COUNT(*) AS cantidad_usuarios,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS porcentaje_usuarios,
    ROUND(AVG(pasos_promedio_diarios), 0) AS pasos_grupo
FROM promedio_por_usuario
GROUP BY tipo_usuario
ORDER BY tipo_usuario;
```
* **Hallazgo:**
  - 1. Sedentario: 8 usuarias (24.2%)
  - 2. Baja Actividad: 9 usuarias (27.3%)
  - 3. Algo Activo: 9 usuarias (27.3%)
  - 4. Muy Activo: 7 usuarias (21.2%)
  - **Conclusión:** El **51.5%** de la muestra camina menos de 7.500 pasos al día. Solo un 21.2% alcanza la meta de 10.000 pasos.

---

## Fase 5: Compartir (Share)

### 5.1 RStudio + ggplot2 (`analisis_bellabeat.Rmd`)
- Se implementó un documento en **R Markdown** con narrativa formal, carga del ecosistema `tidyverse` y 4 gráficos con `ggplot2`.
- Se compiló con **Knit** a un archivo HTML interactivo (`analisis_bellabeat.html`) con navegación flotante y botones para ocultar/mostrar código.

### 5.2 Power BI Desktop (`dashboard_bellabeat.pbix`)
- Se construyó un tablero ejecutivo en cuadrícula 2x2:
  1. **Gráfico de Anillo:** Segmentación de los 4 grupos de usuarias ordenados del 1 al 4.
  2. **Gráfico de Columnas:** Pasos promedio de Lunes a Domingo con línea de meta OMS (10 mil pasos).
  3. **Gráfico de Dispersión:** Horas sedentarias vs Horas de sueño con línea de regresión negativa y colores por grupo.
  4. **Tarjeta de varias filas (KPIs):** Pasos (8,54 mil), Sueño (7,00 hrs) y Desvelo (39,17 min).

### 5.3 Tableau Desktop (`analisis_bellabeat.twbx`)
- Conexión al archivo de 413 registros detallados.
- Desagregación de medidas en el menú superior para desplegar **413 marcas**.
- Círculos rellenos con opacidad y borde fino, diferenciados por `Grupo Sedentarismo`.
- Línea de tendencia global calculando automáticamente el modelo de regresión.

---

## Fase 6: Actuar (Act) - Recomendaciones para Bellabeat

### 1. Posicionamiento del Bellabeat Leaf frente a Smartwatches
- **Problema detectado:** El 27.3% de usuarias no duerme con relojes convencionales por incomodidad y peso.
- **Acción:** Campaña de marketing destacando el diseño del **Leaf** (clip para ropa de dormir o collar ligero, sin pantalla brillante ni batería que deba cargarse a diario).

### 2. Notificaciones Inteligentes a las 14:45 hrs
- **Problema detectado:** A las 15:00 hrs ocurre la caída de actividad más pronunciada de la jornada laboral.
- **Acción:** Programar alertas en la Bellabeat App a las 14:45 hrs invitando a una caminata de 5 minutos, estiramiento o hidratación mediante la botella inteligente **Spring**.

### 3. Programa de Metas Graduales para el 51.5%
- **Problema detectado:** Más de la mitad de las usuarias no llega a 7.500 pasos.
- **Acción:** No forzar una meta de 10.000 pasos desde el día uno; ofrecer retos progresivos (+500 pasos semanales) con gamificación y meditación guiada en la app para reducir los 39 minutos de desvelo nocturno.

---

## Próximos Pasos para tu Portafolio

1. **GitHub (`DiegoHidalgo007/bellabeat-wellness-analysis`):**
   - Subir el código, scripts SQL, Rmd, PDF y capturas de Power BI y Tableau.
2. **Kaggle:**
   - Crear un Notebook público con el análisis en R/Python para ganar visibilidad y medallas en la comunidad global.
3. **LinkedIn:**
   - Publicar un post ejecutivo mostrando el dashboard de Power BI y la gráfica de Tableau, enlazando a tu repositorio de GitHub.
