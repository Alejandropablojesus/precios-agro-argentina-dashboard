# Precios Agro Argentina + Forecasting 2025

**Dashboard interactivo de precios de soja, maíz, trigo y girasol (2023–2025) con predicción a 90 días usando Prophet (Meta AI)**

Live demo: https://precios-agro-argentina-dashboard-alejandropablo.streamlit.app

![Dashboard Preview](https://github.com/Alejandropablojesus/precios-agro-argentina-dashboard/blob/main/preview.png?raw=true)

### Características
- Datos realistas mensuales 2023–2025 (provincia de Buenos Aires)
- Filtros interactivos por producto, provincia y rango de fechas
- Gráficos con Plotly (zoom, hover, responsive)
- Forecasting automático con Prophet + festivos argentinos
- Predicción a 90 días con variación porcentual
- Descarga de datos filtrados en CSV

### Tecnologías usadas (2025 stack)
- Python + Streamlit
- DuckDB → base de datos analítica ultra-rápida
- Prophet → forecasting de Meta
- Plotly → gráficos interactivos
- Pandas + PyArrow

### Cómo correr localmente
```bash
git clone https://github.com/Alejandropablojesus/precios-agro-argentina-dashboard.git
cd precios-agro-argentina-dashboard
pip install -r requirements.txt
streamlit run app.py
