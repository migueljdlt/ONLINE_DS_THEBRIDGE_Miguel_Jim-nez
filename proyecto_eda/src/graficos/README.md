# Scripts de Visualizaciones

Esta carpeta contiene los scripts de Python para generar todas las visualizaciones del análisis EDA.

---

## Estructura

```
graficos/
├── 1evolucion_mercado.py       # Evolución temporal F2P
├── 2alcance.py                 # Análisis de alcance F2P vs PAID
├── 3calidad_percibida.py       # Reviews y calidad percibida
├── 4impacto_precios.py         # Análisis de precios
├── 5retencion.py               # Retención
└── README.md                     # Este archivo
```

---

## Contenido de cada script

### `1evolucion_mercado.py`
**Gráficos generados:**
- Línea temporal de cuota de mercado F2P (%)
- Hitos clave del gaming (eventos importantes)
- Proporción de juegos F2P vs PAID (pie chart + bar chart)
- Número de juegos por año
- Volumen real de lanzamientos por año (stacked area)

**Variables principales:** `release_year`, `is_free`, `f2p_proporcion`

---

### `2alcance.py`
**Gráficos generados:**
- Alcance agregado (suma total de descargas F2P vs PAID)
- Mediana vs Media de owners por juego
- Test estadístico Mann-Whitney U
- Coeficiente de Gini (desigualdad en distribución)

**Variables principales:** `owners_median`, `is_free`

**Análisis estadísticos:**
- Mann-Whitney U-test
- Índice de Gini

---

### `3calidad_percibida.py`
**Gráficos generados:**
- Boxplot de calidad percibida (% reviews positivas)
- Distribución de calidad con KDE (Kernel Density Estimation)
- Zonas de valoración Steam (Muy Negativo, Regulares, Positivas, Muy Positivas)

**Variables principales:** `positive`, `negative`, `positive_ratio`, `is_free`

**Análisis estadísticos:**
- Mann-Whitney U-test
- Gaussian KDE

---

### `4impacto.py`
**Gráficos generados:**
- Evolución de precios medianos a lo largo del tiempo
- Zona del boom F2P (2012-2018)
- Regresión lineal de tendencia de precios
- Precio óptimo por rango
- Alcance + Mercado Total vs Competencia (3 barras comparativas)

**Variables principales:** `price_usd`, `release_year`, `owners_median`

**Análisis estadísticos:**
- Regresión lineal (scipy.stats.linregress)
- Normalización de valores

---

### `5retencion.py`
**Gráficos generados:**
- Tiempo total de juego (average_forever) F2P vs PAID
- Ratio de retención activa (boxplot)
- Comparación de engagement total vs actividad reciente

**Variables principales:** 
- `average_forever` (tiempo total jugado)
- `average_2weeks` (tiempo reciente)
- `retention_ratio` (% de actividad reciente)

**Análisis estadísticos:**
- T-test (scipy.stats.ttest_ind)
- Cálculo de ratios de retención

---

## Cómo ejecutar

### Requisitos
```bash
pip install pandas matplotlib seaborn numpy scipy
```

### Ejecución individual
```bash
cd src/graficos
python 01_evolucion_mercado.py
```

### Ejecución de todos
```bash
for script in 01_*.py 02_*.py 03_*.py 04_*.py 05_*.py; do
    python "$script"
done
```

---

##  Datos necesarios

Todos los scripts requieren el archivo:
```
../data/steamspy_enriched.csv
```

**Ruta relativa desde graficos:** `../data/steamspy_enriched.csv`

### Limpieza de datos

**Todos los scripts aplican la misma limpieza inicial para garantizar consistencia:**

**Resultado:**
- Dataset original: 9,061 juegos
- Dataset limpio: 2,416 juegos
- 

**Porcentajes consistentes en todos los gráficos:**
- F2P: 55.8% (1,347 juegos)
- PAID: 44.2% (1,069 juegos)

---

## Estilo visual

Todos los gráficos usan:
- **Tema gaming dark** (`dark_background`)
- **Colores principales:**
  - `COLOR_F2P = '#00ff41'` (verde neón)
  - `COLOR_PAID = '#ff0080'` (rosa neón)
  - `COLOR_TEXT = '#00ffff'` (cyan)
- **Efectos:** glow, bordes neón, tipografía monospace


**Última actualización:** Noviembre 2025
