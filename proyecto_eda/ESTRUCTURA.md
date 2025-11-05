#  Estructura del Proyecto - Resumen

##  Proyecto Organizado según Enunciado

```
proyecto_eda/
│
├──  README.md                           # Descripción del proyecto
├──  requirements.txt                    # Dependencias Python
├──  .gitignore                          # Archivos a ignorar en Git
│
├──  Presentacion.pptx                   # Presentación de resultados (15 slides)
├──  EDA_Memoria.docx                    # Memoria en Word
│
└── src/                                   # Código fuente
    │
    ├── memoria.ipynb                   # Memoria principal (TODO EL ANÁLISIS)
    │
    ├── data/                              # Archivos de datos (NO subir a GitHub si son pesados)
    │   ├── steam_games_final.csv          # Dataset final (2,446 juegos × 25 vars)
    │   ├── steamspy_cleaned_final.csv     # SteamSpy limpio
    │   ├── steamspy_enriched.csv          # SteamSpy enriquecido
    │   └── steamspy_transformed.csv       # Transformaciones aplicadas
    │
    ├── notebooks/                     
    │   ├── requests_steam_api.ipynb  # Extracción desde Steam
    │   └── requests_steamspy.ipynb   # Extracción desde SteamSpy
    │
    └── utils/                            
        └── .gitkeep                       # Para mantener carpeta en Git
```



##  Contenido de los Archivos Principales

###  `src/memoria.ipynb`
**Secciones:**
1. Introducción
2. Objetivos
3. Fuentes de Datos
4. Metodología
5. Exploración de Datos
6. Análisis y Resultados
   - 6.1. Evolución del Mercado F2P
   - 6.2. Alcance y Popularidad
   - 6.3. Calidad Percibida
   - 6.4. Influencia en Precios
   - 6.5. Retención del Consumidor
   - 6.6. Análisis Estadísticos
7. Conclusiones
8. Referencias

###  `Presentacion.pptx`
**15 Diapositivas:**
0. Portada
1. Índice
2. Contexto e Hipótesis
3-5. Evolución del Mercado
6-7. Alcance y Popularidad
8-9. Calidad Percibida
10-11. Influencia en Precios
12-13. Retención 
14. Conclusiones

###  `EDA_Memoria.docx`
**Documento Word profesional con:**
- Formato gaming/tech
- Estructura completa del análisis
- Explicaciones detalladas
- Listo para entregar


