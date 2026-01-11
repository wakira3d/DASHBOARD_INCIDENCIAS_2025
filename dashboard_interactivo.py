import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Prevención 2025", layout="wide")

st.title("📊 Gestión Operativa: Agentes de Prevención del Delito")
st.markdown("Análisis interactivo de incidencias - Ciudad Autónoma de Buenos Aires")

# Cargar datos creados en el Paso 1
@st.cache_data
def load_data():
    return pd.read_csv('consolidado_prevencion.csv')

try:
    df = load_data()
    
    # Sidebar - Filtros
    st.sidebar.header("Filtros del Tablero")
    meses_sel = st.sidebar.multiselect("Meses", options=df['Mes'].unique(), default=df['Mes'].unique())
    cat_sel = st.sidebar.multiselect("Categoría", options=df['Categoria'].unique(), default=df['Categoria'].unique())
    
    df_filtrado = df[(df['Mes'].isin(meses_sel)) & (df['Categoria'].isin(cat_sel))]

    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Intervenciones", f"{len(df_filtrado):,}")
    c2.metric("Eventos de Seguridad", len(df_filtrado[df_filtrado['Categoria']=='Seguridad/Emergencia']))
    c3.metric("Comunas Cubiertas", df_filtrado['Distrital'].nunique())

    # Gráficos
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.subheader("Evolución por Mes")
        fig_mes = px.bar(df_filtrado['Mes'].value_counts().reindex(df['Mes'].unique()).dropna(), 
                         color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig_mes, use_container_width=True)

    with col_der:
        st.subheader("Distribución por Comuna")
        fig_com = px.pie(df_filtrado, names='Distrital', hole=0.4)
        st.plotly_chart(fig_com, use_container_width=True)

    st.subheader("Top 15 Motivos de Despacho")
    top_motivos = df_filtrado['Tipo y Subtipo'].value_counts().head(15).reset_index()
    fig_top = px.bar(top_motivos, x='count', y='Tipo y Subtipo', orientation='h', color='count')
    st.plotly_chart(fig_top, use_container_width=True)

except Exception as e:
    st.warning("Asegúrate de haber ejecutado el Paso 1 para generar el archivo 'consolidado_prevencion.csv'")