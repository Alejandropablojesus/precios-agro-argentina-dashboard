import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from prophet import Prophet
from utils.fetch_data import actualizar_datos
import os

st.set_page_config(page_title="Precios Agro Argentina 2025", layout="wide")
st.title("🌾 Precios Agro Argentina + Forecasting 2025")
st.markdown("Datos oficiales del Ministerio de Agricultura + INDEC | Actualizado automáticamente")

# ---- 1. Auto-descarga de datos la primera vez ----
if not os.path.exists("data/precios_agro.parquet"):
    with st.spinner("Descargando 5+ años de datos oficiales..."):
        actualizar_datos()

# ---- 2. Cargar con DuckDB (rápido hasta con 10M de filas) ----
con = duckdb.connect(database=':memory:')
con.execute("INSTALL httpfs; LOAD httpfs;")
df = con.execute("SELECT * FROM 'data/precios_agro.parquet'").df()

# Filtros
col1, col2, col3 = st.columns(3)
productos = df['producto'].unique()
provincias = df['provincia'].unique()

producto = col1.selectbox("Producto", options=["Todos"] + list(productos))
provincia = col2.selectbox("Provincia", options=["Todos"] + list(provincias))
fecha_min, fecha_max = col3.date_input("Rango de fechas", 
                                       [df['fecha'].min(), df['fecha'].max()], 
                                       min_value=df['fecha'].min(), 
                                       max_value=df['fecha'].max())

# Aplicar filtros
query = "SELECT * FROM df WHERE fecha BETWEEN ? AND ?"
params = [pd.to_datetime(fecha_min), pd.to_datetime(fecha_max)]

if producto != "Todos":
    query += " AND producto = ?"
    params.append(producto)
if provincia != "Todos":
    query += " AND provincia = ?"
    params.append(provincia)

df_filtrado = con.execute(query, params).df()

# ---- 3. Gráficos ----
st.subheader("Precio promedio por día")
df_graf = df_filtrado.groupby(['fecha', 'producto'])['precio_promedio'].mean().reset_index()
fig = px.line(df_graf, x='fecha', y='precio_promedio', color='producto', 
              title="Evolución de precios", height=500)
st.plotly_chart(fig, use_container_width=True)

# ---- 4. Forecasting con Prophet (solo soja por ahora) ----
if st.checkbox("Ver predicción 90 días (Soja)", value=True):
    with st.spinner("Entrenando modelo Prophet..."):
        df_soja = df[df['producto'] == 'Soja'].groupby('fecha')['precio_promedio'].mean().reset_index()
        df_soja = df_soja.rename(columns={'fecha': 'ds', 'precio_promedio': 'y'})
        
        m = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
        m.add_country_holidays(country_name='AR')
        m.fit(df_soja)
        
        future = m.make_future_dataframe(periods=90)
        forecast = m.predict(future)
        
        fig2 = m.plot(forecast)
        st.pyplot(fig2)
        
        ultimo_precio = forecast.iloc[-1]['yhat']
        precio_actual = df_soja.iloc[-1]['y']
        variacion = ((ultimo_precio - precio_actual) / precio_actual) * 100
        
        st.success(f"Predicción 90 días: ${ultimo_precio:,.0f} | Variación estimada: {variacion:+.1f}%")

# ---- 5. Tabla descargable ----
st.download_button("Descargar datos filtrados (CSV)", 
                   df_filtrado.to_csv(index=False).encode(), 
                   "precios_agro_filtrado.csv")

st.caption("Fuente: datos.gob.ar | Hecho con DuckDB + Prophet + Streamlit | 100% gratis y open-source")