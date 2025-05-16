import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide")
st.title("Análise de Evasão de Alunos")

# Carregar os dados
df = pd.read_csv('datasets\\alunos-ingressantes.csv', sep=';', encoding='latin-1')

# Sidebar com filtros
st.sidebar.header("Filtros")

# Filtro por campus usando checkboxes
st.sidebar.subheader("Selecione o(s) campus:")
campus_options = ["Rio Paranaíba", "Viçosa", "Florestal"]

# Verificar quais campus existem nos dados
available_campuses = [campus for campus in campus_options if campus in df["Campus"].unique()]

# Criar checkboxes para cada campus disponível
selected_campus = []
for campus in available_campuses:
    if st.sidebar.checkbox(campus, value=True):
        selected_campus.append(campus)

# Se nenhum campus foi selecionado, usar todos disponíveis
if not selected_campus:
    selected_campus = available_campuses
    st.sidebar.warning("Nenhum campus selecionado. Mostrando todos por padrão.")

# Filtro por nível de curso
nivel_options = df["NivelAgrupado"].unique().tolist()
selected_nivel = st.sidebar.multiselect("Selecione o nível:", nivel_options, default=nivel_options)

# Filtro por período
min_year = int(df["AnoAdmissao"].min())
max_year = int(df["AnoAdmissao"].max())
year_range = st.sidebar.slider("Selecione o período:", min_year, max_year, (min_year, max_year))

# Aplicar filtros
filtered_df = df[
    (df["Campus"].isin(selected_campus)) & 
    (df["NivelAgrupado"].isin(selected_nivel)) &
    (df["AnoAdmissao"].between(year_range[0], year_range[1]))
]

# Verificar se há dados após filtrar
if filtered_df.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# Análise de evasão por ano
st.header("Evasão ao Longo dos Anos")

# Agrupar dados por ano e situação
evasao_por_ano = filtered_df.groupby(["AnoAdmissao", "SituacaoAlunoAgrupada"]).size().unstack().fillna(0)

# Calcular taxa de evasão
if "Evasão" not in evasao_por_ano.columns:
    st.warning("Não há dados de evasão para exibir.")
else:
    evasao_por_ano["Total"] = evasao_por_ano.sum(axis=1)
    evasao_por_ano["Taxa Evasão"] = (evasao_por_ano["Evasão"] / evasao_por_ano["Total"]) * 100

    # Gráfico de barras da taxa de evasão
    fig1 = px.bar(
        evasao_por_ano.reset_index(), 
        x="AnoAdmissao", 
        y="Taxa Evasão",
        title="Taxa de Evasão por Ano de Admissão",
        labels={"AnoAdmissao": "Ano de Admissão", "Taxa Evasão": "Taxa de Evasão (%)"},
        text_auto=".1f"
    )

    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico de linhas com todas as situações
    fig2 = px.line(
        evasao_por_ano.reset_index(), 
        x="AnoAdmissao", 
        y=[col for col in evasao_por_ano.columns if col not in ["Total", "Taxa Evasão"]],
        title="Distribuição de Situações dos Alunos por Ano",
        labels={"AnoAdmissao": "Ano de Admissão", "value": "Número de Alunos"}
    )

    st.plotly_chart(fig2, use_container_width=True)

# Análise por curso
st.header("Análise por Curso")

# Selecionar curso
curso_options = filtered_df["Curso"].unique().tolist()
selected_curso = st.selectbox("Selecione um curso:", curso_options)

# Filtrar por curso
curso_df = filtered_df[filtered_df["Curso"] == selected_curso]

# Agrupar dados do curso selecionado
evasao_curso = curso_df.groupby(["AnoAdmissao", "SituacaoAlunoAgrupada"]).size().unstack().fillna(0)

if not evasao_curso.empty and "Evasão" in evasao_curso.columns:
    evasao_curso["Total"] = evasao_curso.sum(axis=1)
    evasao_curso["Taxa Evasão"] = (evasao_curso["Evasão"] / evasao_curso["Total"]) * 100

    # Gráfico para o curso selecionado
    fig3 = px.bar(
        evasao_curso.reset_index(), 
        x="AnoAdmissao", 
        y="Taxa Evasão",
        title=f"Taxa de Evasão para o Curso de {selected_curso}",
        labels={"AnoAdmissao": "Ano de Admissão", "Taxa Evasão": "Taxa de Evasão (%)"},
        text_auto=".1f"
    )

    fig3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning(f"Não há dados de evasão para o curso {selected_curso}")