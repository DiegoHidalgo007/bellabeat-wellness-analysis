# Caso de Estudio: Bellabeat — Cómo una Empresa de Bienestar Juega de Forma Inteligente
## Análisis de Datos de Dispositivos Inteligentes para Impulsar el Ecosistema Leaf y Bellabeat App
**Google Data Analytics Professional Certificate — Capstone Project (Caso 2)**  
*Autor: Diego H. | Fecha: Octubre 2026*  
*Herramientas: Python (Pandas, Matplotlib, Seaborn), SQL, Git/GitHub*

---

## 1. Resumen Ejecutivo (Executive Summary)

Bellabeat es una empresa pionera de tecnología enfocada en la salud y el bienestar femenino, cofundada por **Urška Sršen** y **Sando Mur**. Su catálogo incluye productos de diseño elegante como el monitor inteligente **Leaf** (usable como pulsera, collar o broche) y la **Bellabeat App**.

Para identificar oportunidades de crecimiento frente a competidores gigantes como Fitbit o Apple, este estudio analizó datos de actividad física, sueño y frecuencia horaria de usuarios de monitores inteligentes (*FitBit Fitness Tracker Data*).

### Los 4 Hallazgos Clave de Negocio:
1. **El Rechazo al Monitor de Muñeca Nocturno:** Mientras que el 100% de los usuarios registra su actividad diurna, el **27,3% abandona el seguimiento del sueño** (solo 24 de 33 usuarios lo utilizan). Los relojes inteligentes voluminosos con pantallas brillantes incomodan al dormir. **Oportunidad para Leaf:** al carecer de pantalla y ser liviano como broche de pijama, ofrece una experiencia de descanso sin interrupciones.
2. **Impacto Negativo del Sedentarismo en el Sueño:** Se descubrió una **fuerte correlación negativa (-0,60)** entre minutos sedentarios diurnos y minutos de sueño nocturno. El sedentarismo prolongado sabotea el descanso de las usuarias.
3. **El "Desvelo Oculto" de 39 Minutos:** En promedio, las personas pasan **458 minutos en la cama pero solo duermen 419 minutos**. Pasan casi 40 minutos despiertas tratando de conciliar el sueño.
4. **Horarios de Mayor Movimiento:** La actividad física no es homogénea: se concentra en dos picos específicos: **12:00 PM - 2:00 PM** (pausa de almuerzo) y **5:00 PM - 7:00 PM** (salida laboral). Los domingos y viernes son los días con menor actividad.

---

## 2. Fase 1: Preguntar (Ask)

### Tarea de Negocio (Business Task)
Analizar las tendencias de uso de dispositivos inteligentes de salud de la competencia para comprender los hábitos diarios de las consumidoras, y aplicar estos hallazgos en una **estrategia de marketing integral que posicione el rastreador Leaf y la Bellabeat App**.

### Preguntas Guía:
1. ¿Cuáles son las principales tendencias de uso en dispositivos de bienestar?
2. ¿Cómo se aplican estas tendencias a las clientas actuales y potenciales de Bellabeat?
3. ¿Cómo pueden estos hallazgos influir en el mensaje y los canales de marketing de Bellabeat?

### Partes Interesadas (Stakeholders)
* **Urška Sršen:** Cofundadora y Directora Creativa de Bellabeat.
* **Sando Mur:** Matemático y Cofundador de Bellabeat.
* **Equipo de Marketing Analytics de Bellabeat.**

---

## 3. Fase 2: Preparar (Prepare)

### Fuente de Datos
* **Dataset:** *FitBit Fitness Tracker Data* (dominio público CC0, compartido por Mobius en Kaggle).
* **Contenido:** 18 archivos CSV que registran actividad diaria, pasos por hora, calorías, minutos de intensidad y registros de sueño.
* **Muestra:** 33 usuarios únicos durante un período de 31 días (12 de abril a 12 de mayo de 2016).

### Evaluación ROCCC de los Datos
* **Reliable (Confiable):** Nivel medio. Son datos directos de sensores de Fitbit, pero recolectados mediante Amazon Mechanical Turk con consentimiento de los participantes.
* **Original:** Datos de segunda fuente (usuarios voluntarios de Fitbit exportados mediante Fitabase).
* **Comprehensive (Exhaustivo):** Registros a nivel de día, hora y minuto. Sin embargo, tiene una **limitación crítica**: no incluye variables demográficas de género (aunque Bellabeat apunta a mujeres, la muestra es general) y el tamaño muestral (33 personas) es pequeño.
* **Current (Actual):** Datos de 2016 (útiles para patrones de comportamiento humano universales como el sueño y el sedentarismo, pero se recomienda complementar con métricas propias de la app Bellabeat en producción).
* **Cited (Citado):** Licencia abierta CC0 acreditada.

---

## 4. Fase 3: Procesar y Limpiar (Process)

### Limpieza y Tratamiento de Datos (Python Script `analisis_bellabeat.py`)
1. **Eliminación de duplicados:** Se identificaron y eliminaron registros duplicados en el conjunto de sueño (`sleepDay`).
2. **Conversión de Fechas:** Las fechas en texto se estandarizaron al formato nativo `datetime` de Pandas.
3. **Filtrado de Registros Inactivos:** Se descartaron días donde `TotalSteps == 0`, ya que corresponden a días en que el usuario no portó el dispositivo (olvido o carga de batería).
4. **Fusión de Datasets:** Se unieron `dailyActivity` y `sleepDay` mediante `Id` y fecha (`ActivityDate`), resultando en **410 jornadas completas con actividad y sueño simultáneos**.

### Variables Calculadas (Feature Engineering)
* `HorasEnCama`: `TotalTimeInBed / 60`
* `HorasDormidas`: `TotalMinutesAsleep / 60`
* `MinutosDesvelo`: `TotalTimeInBed - TotalMinutesAsleep`
* `EficienciaSueno`: `(TotalMinutesAsleep / TotalTimeInBed) * 100`
* `Categoria_Actividad`: Sedentario (<5.000 pasos), Baja actividad (5.000 - 7.499), Moderado (7.500 - 9.999), Muy activo (>=10.000 pasos).

---

## 5. Fase 4: Analizar (Analyze)

### 5.1. Estadísticas Generales de Salud

| Métrica | Promedio Obtenido | Meta Recomendada (OMS / CDC) | Brecha / Hallazgo |
| :--- | :---: | :---: | :--- |
| **Pasos Diarios** | **8.319 pasos** | 10.000 pasos | Por debajo de la meta de salud óptima |
| **Tiempo Sedentario** | **15,9 horas / día** | < 8 - 10 horas | Nivel crítico de sedentarismo |
| **Actividad Intensa** | **23 minutos / día** | 30 minutos / día | Brecha de 7 minutos diarios |
| **Horas de Sueño** | **7,0 horas** | 7 - 9 horas | Cumplimiento justo en el límite inferior |
| **Tiempo en Cama** | **7,6 horas** | - | **39,3 minutos despiertos en cama** |
| **Eficiencia de Sueño** | **91,6%** | > 85% | Rango saludable, pero con fricción para conciliar |

---

### 5.2. Segmentación de Usuarios por Pasos Diarios

* **Muy Activos (>= 10.000 pasos):** 33,2% de los días registrados.
* **Moderadamente Activos (7.500 - 9.999 pasos):** 28,5% de los días.
* **Baja Actividad (5.000 - 7.499 pasos):** 21,8% de los días.
* **Sedentarios (< 5.000 pasos):** 16,5% de los días.

> **Conclusión:** Casi el **38% de los días registrados** caen en niveles de baja actividad o sedentarismo puro, lo que demuestra la necesidad de "empujones" (*nudges*) de motivación.

---

### 5.3. Actividad por Día de la Semana

| Día de la Semana | Pasos Diarios Promedio | Minutos Sedentarios Promedio |
| :--- | :---: | :---: |
| **Lunes** | 8.488 | 988 min |
| **Martes** | **8.949 (Pico máx)** | 996 min |
| **Miércoles** | 8.158 | 989 min |
| **Jueves** | 8.185 | 962 min |
| **Viernes** | 7.821 | 1.004 min |
| **Sábado** | **8.947 (Pico máx)** | 968 min |
| **Domingo** | **7.627 (Pico mín)** | 990 min |

> **Hallazgo:** El domingo es el día más sedentario y con menos pasos de la semana. Los martes y sábados las usuarias se sienten más motivadas para ejercitarse.

---

### 5.4. Análisis de Correlación Clave

* **Minutos Sedentarios vs Minutos de Sueño: -0,60 (Correlación Negativa Fuerte):** Demuestra empíricamente que pasar el día inmóvil frente a una pantalla reduce las horas y la profundidad del sueño.
* **Pasos Diarios vs Calorías Quemadas: +0,59 (Correlación Positiva Moderada-Alta):** Confirma la eficacia del movimiento continuo para el gasto calórico basal.

---

## 6. Fase 5: Compartir (Share) — Galería de Gráficos

Los siguientes gráficos fueron generados y almacenados en alta resolución en la carpeta `graficos/`:

1. **`1_sedentarismo_vs_sueno.png`:** Diagrama de dispersión con línea de regresión descendente que ilustra la penalización del sueño a medida que suben los minutos sedentarios.
2. **`2_pasos_vs_calorias.png`:** Curva de quema calórica con la línea de referencia de los 10.000 pasos de la OMS.
3. **`3_pasos_por_dia_semana.png`:** Gráfico de barras comparativo de lunes a domingo.
4. **`4_pasos_por_hora.png`:** Curva horaria que resalta los picos de las 12 PM y 5-7 PM.
5. **`5_segmentacion_usuarios.png`:** Gráfico circular de distribución de actividad.

---

## 7. Fase 6: Actuar (Act) — Recomendaciones de Marketing para Bellabeat

Basado en la evidencia cuantitativa, se presentan **3 recomendaciones estratégicas para Urška Sršen y el equipo directivo**:

### Recomendación 1: Campaña "Descansa sin Pantallas" (Posicionamiento del Leaf)
* **El Problema en los Datos:** El 27% de las usuarias no registra su sueño con relojes inteligentes convencionales debido al peso y la luz de pantalla.
* **La Propuesta de Marketing:** Lanzar una campaña centrada en el descanso nocturno destacando el diseño del **Bellabeat Leaf**:
  * *"Tu descanso no necesita otra pantalla brillante. Conoce Leaf: el rastreador joya que se prende a tu pijama y cuida tu sueño sin molestarte"*.
  * Destacar que la batería dura hasta 6 meses (sin tener que cargarlo todos los días antes de dormir).

### Recomendación 2: Alertas Predictivas en la Bellabeat App ("El Vínculo Sedentarismo-Sueño")
* **El Problema en los Datos:** Correlación de -0,60 entre sedentarismo y pérdida de sueño.
* **La Función en la App:** Crear notificaciones inteligentes basadas en la ciencia del descanso:
  * Si la app detecta más de 90 minutos de inmovilidad continua entre las 2:00 PM y las 6:00 PM: *"Llevas un buen rato sentada. Una caminata de 10 minutos ahora te ayudará a dormir profundamente esta noche"*.
  * Conectar el movimiento diurno con el beneficio directo del descanso nocturno.

### Recomendación 3: Rutinas de Meditación para el "Desvelo de 39 Minutos"
* **El Problema en los Datos:** Las usuarias pasan casi 40 minutos despiertas en cama antes de dormir.
* **Estrategia de Suscripción (Membresía Bellabeat):**
  * Incluir en la Bellabeat App una función de **"Sleep Wind-Down"**: cuando el sensor Leaf detecta que la usuaria se recuesta en la cama, la app sugiere audios relajantes de 15 minutos, sonidos de la naturaleza y ejercicios de respiración para conciliar el sueño más rápido.
  * Ofrecer 30 días gratuitos de la membresía con este programa de sueño.

---
*Fin del Informe Ejecutivo — Bellabeat Case Study 2*
