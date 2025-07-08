
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Dashboard Tono y Tacho", layout="wide")
st.title("📊 Dashboard de Evaluación de Tono y Tacho")

# Cargar datos
df = pd.read_csv("data.csv")

# Corregir porcentajes si están entre 0 y 1 (multiplica por 100 si es necesario)
for col in ["% Aprobado", "% Concesionado", "% Rechazado"]:
    if df[col].max() <= 1.0:
        df[col] = df[col] * 100

# Filtros
semanas = st.multiselect("Selecciona semana(s):", options=df["Semana"].unique(), default=df["Semana"].unique())
tipos = st.multiselect("Selecciona tipo(s):", options=["Aprobado", "Concesionado", "Rechazado"], default=["Aprobado", "Concesionado", "Rechazado"])

df_filtrado = df[df["Semana"].isin(semanas)]

# Indicadores
st.subheader("Indicadores Clave")
cols = st.columns(len(tipos))
for i, tipo in enumerate(tipos):
    total = df_filtrado[tipo].sum()
    promedio = df_filtrado[f"% {tipo}"].mean()
    cols[i].metric(label=f"{tipo}", value=f"{total} partidas", delta=f"{promedio:.1f}% promedio")

# Gráfico de tendencia del % Rechazo
st.subheader("📉 Tendencia de % Rechazo por Semana")
fig_rechazo = px.line(df_filtrado, x="Semana", y="% Rechazado", markers=True)
fig_rechazo.update_layout(yaxis_title="% Rechazado", yaxis_range=[0, 100])
st.plotly_chart(fig_rechazo, use_container_width=True)

# Gráfico de barras apiladas con totales encima
st.subheader("📦 Partidas Evaluadas por Semana")
df_filtrado["Total Partidas"] = df_filtrado[["Aprobado", "Concesionado", "Rechazado"]].sum(axis=1)
fig_barras = px.bar(df_filtrado, x="Semana", y=["Aprobado", "Concesionado", "Rechazado"], barmode="stack", text_auto=False)
for i, semana in enumerate(df_filtrado["Semana"]):
    total = df_filtrado.iloc[i]["Total Partidas"]
    fig_barras.add_annotation(x=semana, y=total + 2, text=str(int(total)), showarrow=False)
fig_barras.update_layout(yaxis_title="Cantidad de Partidas")
st.plotly_chart(fig_barras, use_container_width=True)

# Gráfico de pastel
st.subheader("📊 Distribución Total de Partidas")
suma_totales = df_filtrado[["Aprobado", "Concesionado", "Rechazado"]].sum()
fig_pie = px.pie(names=suma_totales.index, values=suma_totales.values, hole=0.3)
st.plotly_chart(fig_pie, use_container_width=True)
