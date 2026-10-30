import markdown
import os
import base64

base_dir = r"C:\Proyectos\07_Educacion_y_Hardware\Casos estudio Data analytics\Caso 2 bien estar en la compañia"
md_path = os.path.join(base_dir, "INFORME_FINAL_BELLABEAT.md")
html_path = os.path.join(base_dir, "INFORME_FINAL_BELLABEAT.html")
graphs_dir = os.path.join(base_dir, "graficos")

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

# Convertir gráficos a Base64 para que el HTML sea 100% autónomo (los gráficos se ven siempre incluso si se mueve el archivo)
def img_to_base64(img_name):
    p = os.path.join(graphs_dir, img_name)
    if os.path.exists(p):
        with open(p, "rb") as img_f:
            return "data:image/png;base64," + base64.b64encode(img_f.read()).decode("utf-8")
    return ""

img1 = img_to_base64("1_sedentarismo_vs_sueno.png")
img2 = img_to_base64("2_pasos_vs_calorias.png")
img3 = img_to_base64("3_pasos_por_dia_semana.png")
img4 = img_to_base64("4_pasos_por_hora.png")
img5 = img_to_base64("5_segmentacion_usuarios.png")

body_html = markdown.markdown(text, extensions=['tables', 'fenced_code'])

# Inyectar las imágenes debajo de la sección 6
galeria_html = f"""
<div class="gallery-section">
    <div class="chart-card">
        <h4>1. Correlación Negativa entre Sedentarismo y Sueño</h4>
        <img src="{img1}" alt="Sedentarismo vs Sueño">
        <p class="chart-desc">A mayor cantidad de minutos sedentarios en el día, menor es el tiempo de sueño nocturno (r = -0.60).</p>
    </div>
    <div class="chart-card">
        <h4>2. Pasos Diarios vs Calorías Quemadas</h4>
        <img src="{img2}" alt="Pasos vs Calorías">
        <p class="chart-desc">Relación lineal positiva entre pasos y gasto calórico con meta de 10.000 pasos de la OMS.</p>
    </div>
    <div class="chart-card">
        <h4>3. Pasos por Día de la Semana</h4>
        <img src="{img3}" alt="Pasos por Día">
        <p class="chart-desc">Los martes y sábados alcanzan el pico máximo; domingos y viernes registran la menor actividad.</p>
    </div>
    <div class="chart-card">
        <h4>4. Distribución de Pasos por Hora</h4>
        <img src="{img4}" alt="Pasos por Hora">
        <p class="chart-desc">Picos pronunciados de actividad a las 12:00 PM (almuerzo) y 5:00 - 7:00 PM (salida laboral).</p>
    </div>
    <div class="chart-card">
        <h4>5. Segmentación de Usuarios por Nivel de Actividad</h4>
        <img src="{img5}" alt="Segmentación">
        <p class="chart-desc">El 38.3% de las jornadas registradas caen en baja actividad o sedentarismo.</p>
    </div>
</div>
"""

body_html = body_html.replace("Fase 5: Compartir (Share) — Galería de Gráficos</h2>", "Fase 5: Compartir (Share) — Galería de Gráficos</h2>" + galeria_html)

full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe Final - Bellabeat Wellness Case Study</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        
        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.65;
            color: #2e2633;
            background-color: #fdfafb;
            margin: 0;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 920px;
            margin: 0 auto;
            background: #ffffff;
            padding: 60px 75px;
            border-radius: 16px;
            box-shadow: 0 4px 25px rgba(217, 125, 138, 0.08);
            border: 1px solid #f2e6ea;
        }}
        h1 {{
            color: #3b2c3d;
            font-size: 2.1rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
            border-bottom: 2px solid #ecd4dc;
            padding-bottom: 12px;
        }}
        h2 {{
            color: #b0536c;
            font-size: 1.45rem;
            font-weight: 600;
            margin-top: 2.2rem;
            margin-bottom: 0.8rem;
            border-bottom: 1px solid #fcedf1;
            padding-bottom: 6px;
        }}
        h3 {{
            color: #4a3b4e;
            font-size: 1.15rem;
            font-weight: 600;
            margin-top: 1.5rem;
        }}
        p, li {{
            font-size: 1rem;
            color: #3e3342;
        }}
        ul, ol {{
            padding-left: 24px;
        }}
        li {{
            margin-bottom: 6px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0;
            font-size: 0.95rem;
            background: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid #f2e6ea;
        }}
        th {{
            background-color: #faf0f3;
            color: #593542;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 0.05em;
        }}
        tr:hover {{
            background-color: #fff8fa;
        }}
        blockquote {{
            margin: 20px 0;
            padding: 16px 20px;
            background-color: #fdf2f5;
            border-left: 4px solid #d97d8a;
            color: #8c3b4f;
            border-radius: 0 8px 8px 0;
            font-style: italic;
        }}
        hr {{
            border: 0;
            height: 1px;
            background: #f2e6ea;
            margin: 40px 0;
        }}
        .gallery-section {{
            display: flex;
            flex-direction: column;
            gap: 30px;
            margin: 30px 0;
        }}
        .chart-card {{
            background: #fffbfe;
            border: 1px solid #f2e6ea;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        .chart-card h4 {{
            margin-top: 0;
            color: #4a3b4e;
            font-size: 1.1rem;
        }}
        .chart-card img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        .chart-desc {{
            font-size: 0.9rem;
            color: #6b5c6f;
            margin-top: 10px;
            font-style: italic;
        }}
        .print-btn {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #b0536c;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 30px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(176, 83, 108, 0.35);
            transition: all 0.2s;
        }}
        .print-btn:hover {{
            background: #8f3b52;
            transform: translateY(-2px);
        }}
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                border: none;
                padding: 0;
                max-width: 100%;
            }}
            .print-btn {{
                display: none;
            }}
            .chart-card {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">📥 Guardar como PDF</button>
    <div class="container">
        {body_html}
    </div>
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("HTML de Bellabeat generado exitosamente con graficos embebidos en:", html_path)
