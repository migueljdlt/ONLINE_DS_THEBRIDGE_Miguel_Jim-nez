import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Configuramos la página
st.set_page_config(page_title="Movie Revenue Predictor", layout="wide")

# Título
st.title("Movie Revenue Predictor")
st.write("Predice el éxito de taquilla de una película usando Machine Learning")

# Cargamos los modelos
@st.cache_resource
def load_models():
    with open('models/modelo_clasificacion.pkl', 'rb') as f:
        clf = pickle.load(f)
    with open('models/modelo_regresion.pkl', 'rb') as f:
        reg = pickle.load(f)
    with open('models/modelo_clustering.pkl', 'rb') as f:
        cluster = pickle.load(f)
    return clf, reg, cluster

clf, reg, cluster_model = load_models()

# Sidebar con inputs
st.sidebar.header("Características de la Película")

# Datos Financieros y Técnicos
st.sidebar.subheader("Datos Principales")
budget = st.sidebar.number_input("Presupuesto (USD)", min_value=0, value=50000000, step=1000000)
runtime = st.sidebar.slider("Duración (minutos)", 60, 240, 120, 5)
vote_average = st.sidebar.slider("Calificación Promedio", 0.0, 10.0, 7.0, 0.1)
vote_count = st.sidebar.number_input("Número de Votos", min_value=0, value=5000, step=100)
release_year = st.sidebar.number_input("Año de Estreno", min_value=2024, max_value=2030, value=2025)

# Nuevos inputs
release_month = st.sidebar.selectbox(
    "Mes de Estreno",
    options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    index=5,  # Junio por defecto
    format_func=lambda x: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                           "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][x-1]
)

language = st.sidebar.selectbox(
    "Idioma Principal",
    options=["en", "es", "fr", "de", "it", "ja", "ko", "zh"],
    index=0,
    format_func=lambda x: {"en": "Inglés", "es": "Español", "fr": "Francés", 
                           "de": "Alemán", "it": "Italiano", "ja": "Japonés", 
                           "ko": "Coreano", "zh": "Chino"}[x]
)

num_famous_actors = st.sidebar.slider("Número de Actores Famosos", 0, 10, 2, 1)

log_popularity = st.sidebar.slider("Popularidad (escala logarítmica)", 0.0, 5.0, 3.0, 0.1)

# Características de Producción
st.sidebar.subheader("Características de Producción")
is_franchise = st.sidebar.checkbox("Es una franquicia")
has_major_studio = st.sidebar.checkbox("Estudio major")
is_usa_production = st.sidebar.checkbox("Producción USA", value=True)
has_famous_actor = st.sidebar.checkbox("Tiene actor famoso", value=False)

# Géneros - Ampliados
st.sidebar.subheader("Géneros")
st.sidebar.caption("Selecciona todos los que apliquen:")

col1, col2 = st.sidebar.columns(2)
with col1:
    genre_action = st.checkbox("Acción")
    genre_adventure = st.checkbox("Aventura")
    genre_comedy = st.checkbox("Comedia")
    genre_drama = st.checkbox("Drama")
    genre_horror = st.checkbox("Horror")
with col2:
    genre_animation = st.checkbox("Animación")
    genre_family = st.checkbox("Familiar")
    genre_fantasy = st.checkbox("Fantasía")
    genre_scifi = st.checkbox("Ciencia Ficción")
    genre_thriller = st.checkbox("Thriller")

# Botón de predicción
if st.button("PREDECIR", type="primary"):
    
    # Calculamos número total de géneros
    num_genres = sum([
        genre_action, genre_adventure, genre_comedy, genre_drama, genre_horror,
        genre_animation, genre_family, genre_fantasy, genre_scifi, genre_thriller
    ])
    
    # Preparamos las features
    features = pd.DataFrame([{
        'budget': budget,
        'runtime': runtime,
        'vote_average': vote_average,
        'vote_count': vote_count,
        'is_franchise': int(is_franchise),
        'log_popularity': log_popularity,
        'language_category': language,
        'release_year': release_year,
        'release_month': release_month,
        'num_genres': num_genres,
        'genre_action': int(genre_action),
        'genre_adventure': int(genre_adventure),
        'genre_animation': int(genre_animation),
        'genre_comedy': int(genre_comedy),
        'genre_horror': int(genre_horror),
        'genre_drama': int(genre_drama),
        'genre_family': int(genre_family),
        'genre_fantasy': int(genre_fantasy),
        'genre_science_fiction': int(genre_scifi),
        'genre_thriller': int(genre_thriller),
        'has_famous_actor': int(has_famous_actor),
        'num_famous_actors': num_famous_actors,
        'is_usa_production': int(is_usa_production),
        'has_major_studio': int(has_major_studio)
    }])
    
    # Clasificación
    va_a_cines = clf.predict(features)[0]
    probabilidad = clf.predict_proba(features)[0][1]
    
    # Clustering - Determinar segmento de mercado
    features_scaled = cluster_model['preprocessor'].transform(features)
    cluster_id = cluster_model['kmeans'].predict(features_scaled)[0]
    segmento = cluster_model['nombres'][cluster_id]
    
    # Mostramos resultados
    st.subheader("Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Estreno en Cines", "SÍ" if va_a_cines else "NO")
    
    with col2:
        st.metric("Probabilidad", f"{probabilidad*100:.1f}%")
    
    with col3:
        st.metric("Segmento de Mercado", segmento)
    
    # Regresión solo si va a cines
    if va_a_cines:
        pred_rf = reg['rf'].predict(features)[0]
        pred_xgb = reg['xgb'].predict(features)[0]
        revenue = np.exp(0.6 * pred_rf + 0.4 * pred_xgb)
        
        st.metric("Revenue Estimado", f"${revenue/1e6:.1f}M")
        
        roi = (revenue / budget - 1) * 100
        st.info(f"""
        **Análisis Financiero:**
        - Presupuesto: ${budget:,.0f}
        - Revenue estimado: ${revenue:,.0f}
        - ROI estimado: {roi:.1f}%
        - Segmento: {segmento}
        """)
        
        # Contexto según el segmento
        if "Blockbuster" in segmento or "comercial" in segmento.lower():
            st.success("Esta película tiene características de gran éxito comercial.")
        elif "Indie" in segmento:
            st.info("Película con perfil independiente pero potencial comercial.")
        else:
            st.info(f"Película clasificada como: {segmento}")
            
    else:
        st.warning("""
        **Esta película probablemente irá directamente a streaming.**
        
        Posibles razones:
        - Presupuesto bajo
        - Géneros poco comerciales
        - Falta de elementos atractivos para cines
        """)
        
        st.info(f"**Segmento identificado:** {segmento}")