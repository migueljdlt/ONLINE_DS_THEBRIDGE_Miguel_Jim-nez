#  EDA: Impacto de los Free-to-Play en la Industria del Videojuego

Análisis exploratorio de datos sobre el impacto del modelo Free-to-Play en el mercado de videojuegos, utilizando datos de **Steam** y **SteamSpy**.

---

##  Estructura del Proyecto

```
proyecto_eda/
│
├── src/
│   ├── data/                              # Archivos de datos
│   │   ├── steam_games_final.csv         # Dataset final de Steam (2,446 juegos)
│   │   ├── steamspy_cleaned_final.csv    # Dataset limpio de SteamSpy
│   │   ├── steamspy_enriched.csv         # Dataset enriquecido
│   │   └── steamspy_transformed.csv      # Datos transformados
│   │
│   ├── notebooks/                         # Notebooks de análisis
│   │   ├── requests_steam_api.ipynb       # Extracción desde Steam API
│   │   └── requests_steamspy.ipynb        # Extracción desde SteamSpy API
│   │
│   ├── utils/                            
│   │
│   └── memoria.ipynb                      # Memoria completa del proyecto
│
├── Presentacion.pptx                      # Presentación de resultados
├── EDA_Memoria.docx                       # Documento de memoria
├── README.md                              # Este archivo
└── requirements.txt                       # Dependencias del proyecto
```

---

## Descripción del Proyecto

Este proyecto investiga cómo los juegos Free-to-Play han transformado la industria del videojuego, analizando:

- **Evolución temporal** del mercado F2P vs juegos de pago
- **Alcance y popularidad** comparativa
- **Calidad percibida** por los consumidores
- **Influencia en precios**
- **Retención del consumidor**

### Hipótesis Principal

> **"Los juegos Free-to-Play han revolucionado el mercado del videojuego"**

---

##  Dataset

### Fuentes de Datos

1. **Steam Web API**: Datos oficiales de juegos
   - URL: https://developer.valvesoftware.com/wiki/Steam_Web_API
   - Muestra: 9,060 juegos válidos

2. **SteamSpy API**: Métricas de jugadores y engagement
   - URL: http://steamspy.com/api.php
   - Muestra: 6,089 juegos F2P

### Dataset Final

- **Tamaño**: 2,446 juegos × 25 variables
- **Período**: 2004-2025
- **Ubicación**: `src/data/steam_games_final.csv`

### Variables Principales

**Numéricas (17):**
- `positive`, `negative`: Reviews de usuarios
- `owners_median`: Propietarios del juego
- `average_forever`, `average_2weeks`: Tiempo de juego
- `ccu`: Jugadores concurrentes
- `price`, `initialprice`, `discount`: Datos económicos
- `metacritic_score`, `dlc_count`, `release_year`

**Categóricas (8):**
- `appid`, `name`, `developer`, `publisher`
- `is_free`: F2P vs PAID (variable clave)
- `genres`, `release_date`, `owners`

---

## Instalación y Uso

### Requisitos

- Python 3.8+
- Jupyter Notebook

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/eda-free-to-play-steam.git
cd eda-free-to-play-steam

# Instalar dependencias
pip install -r requirements.txt

# Iniciar Jupyter
jupyter notebook
```

### Notebooks

1. **`src/memoria.ipynb`**: Memoria completa del proyecto con todos los pasos
2. **`src/notebooks/01_extraccion_steam_api.ipynb`**: Extracción de datos de Steam
3. **`src/notebooks/02_extraccion_steamspy.ipynb`**: Extracción de datos de SteamSpy

---

##  Principales Hallazgos

### 1. Evolución del Mercado
- Los F2P pasaron de **0% a 42%** del mercado en 20 años
- Representan el **55.7%** de los juegos totales
- Boom entre 2010-2015, seguido de estabilización

### 2. Patrón Winner-Takes-All
- **F2P**: Pocos megahits concentran el éxito
- **PAID**: Distribución más equitativa
- Alcance típico: **PAID gana 2.3×**

### 3. Calidad Percibida
- **Opinión promedio**: Empate técnico
- **Consistencia**: PAID más consistente
- **F2P**: Mayor polarización (excelentes vs mediocres)

### 4. Impacto en Precios
- Presión a la baja durante boom F2P (2010-2015)
- Recuperación posterior
- Rango óptimo: **$15-$20**

### 5. Retención del Consumidor

| Métrica | F2P | PAID | Winner |
|---------|-----|------|--------|
| Tiempo total jugado | 3.0h | 6.9h |  PAID (2.3×) |
| Actividad reciente (%) | 15% | 8% |  F2P (1.9×) |
| Correlación CCU-Engagement | r=0.185 | r=0.411 |  PAID |

**Interpretación:**
- **PAID**: Picos intensos + abandono predecible
- **F2P**: Engagement moderado + retención sostenida

---

##  Metodología

### Pipeline de Trabajo

1. **Extracción**: APIs de Steam y SteamSpy
2. **Limpieza**: Filtrado y transformación de datos
3. **Enriquecimiento**: Cruce de datasets y variables derivadas
4. **Análisis**: Estadísticas descriptivas e inferenciales
5. **Visualización**: Gráficos y dashboards

### Análisis Estadísticos

- **Mann-Whitney U-test**: Comparación de distribuciones
- **Coeficiente de Gini**: Medida de desigualdad
- **Correlación de Pearson**: Relaciones entre variables
- **Regresión lineal**: Tendencias temporales
- **KDE**: Distribuciones de probabilidad

---

##  Visualizaciones

Las visualizaciones principales incluyen:

- Evolución temporal del mercado F2P
- Comparativa de alcance (F2P vs PAID)
- Distribución de calidad percibida
- Análisis de precios a lo largo del tiempo
- Métricas de retención y engagement

*(Ver `Presentacion.pptx` para visualizaciones completas)*

---

##  Conclusiones

### Validación de Hipótesis

**CONFIRMADA con matices**

Los F2P han transformado la industria al crear un nuevo segmento de mercado, influir en estrategias de monetización y forzar adaptaciones competitivas.

Sin embargo, **coexisten** con juegos tradicionales en un ecosistema segmentado donde cada modelo atiende diferentes perfiles de jugador.

### Implicaciones

**Para Desarrolladores F2P:**
- Estrategias de retención robustas son críticas
- Diferenciación clara para evitar abandono

**Para Desarrolladores PAID:**
- Calidad consistente sigue siendo competitiva
- Rango $15-$20 maximiza rentabilidad

**Para la Industria:**
- Coexistencia enriquece el ecosistema
- Innovación en modelos híbridos


##  Archivos del Proyecto

- **`src/memoria.ipynb`**: Memoria completa con análisis paso a paso
- **`Presentacion.pptx`**: Presentación de resultados
- **`EDA_Memoria.docx`**: Documento de memoria en Word
- **`README.md`**: Este archivo

---

**Proyecto desarrollado para Bootcamp de Data Science**

*Noviembre 2025*

---

## Licencia

Este proyecto está bajo la licencia MIT.

---

<div align="center">

**⭐ Si este proyecto te resultó útil, considera darle una estrella ⭐**

</div>
