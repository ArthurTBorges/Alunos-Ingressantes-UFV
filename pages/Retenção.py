import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide")
st.title("Análise de Retenção de Alunos")

# Carregar os dados
df = pd.read_csv('alunos-ingressantes.csv', sep=';', encoding='latin-1')

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

# Análise de retenção por ano
st.header("Retenção ao Longo dos Anos")

# Agrupar dados por ano e situação
retencao_por_ano = filtered_df.groupby(["AnoAdmissao", "SituacaoAlunoAgrupada"]).size().unstack().fillna(0)

# Calcular taxa de retenção
if "Retenção" not in retencao_por_ano.columns:
    st.warning("Não há dados de retenção para exibir.")
else:
    retencao_por_ano["Total"] = retencao_por_ano.sum(axis=1)
    retencao_por_ano["Taxa Retenção"] = (retencao_por_ano["Retenção"] / retencao_por_ano["Total"]) * 100

    # Gráfico de barras da taxa de retenção
    fig1 = px.bar(
        retencao_por_ano.reset_index(), 
        x="AnoAdmissao", 
        y="Taxa Retenção",
        title="Taxa de Retenção por Ano de Admissão",
        labels={"AnoAdmissao": "Ano de Admissão", "Taxa Retenção": "Taxa de Retenção (%)"},
        text_auto=".1f",
        color_discrete_sequence=["#2ca02c"]  # Cor verde para retenção
    )

    fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico de linhas com todas as situações
    fig2 = px.line(
        retencao_por_ano.reset_index(), 
        x="AnoAdmissao", 
        y=[col for col in retencao_por_ano.columns if col not in ["Total", "Taxa Retenção"]],
        title="Distribuição de Situações dos Alunos por Ano",
        labels={"AnoAdmissao": "Ano de Admissão", "value": "Número de Alunos"}
    )
    
    # Destacar a linha de Retenção
    fig2.update_traces(line=dict(width=4), selector={"name":"Retenção"})
    st.plotly_chart(fig2, use_container_width=True)

# Análise por curso
st.header("Análise por Curso")

# Selecionar curso
curso_options = filtered_df["Curso"].unique().tolist()
selected_curso = st.selectbox("Selecione um curso:", curso_options)

# Filtrar por curso
curso_df = filtered_df[filtered_df["Curso"] == selected_curso]

# Agrupar dados do curso selecionado
retencao_curso = curso_df.groupby(["AnoAdmissao", "SituacaoAlunoAgrupada"]).size().unstack().fillna(0)

if not retencao_curso.empty and "Retenção" in retencao_curso.columns:
    retencao_curso["Total"] = retencao_curso.sum(axis=1)
    retencao_curso["Taxa Retenção"] = (retencao_curso["Retenção"] / retencao_curso["Total"]) * 100

    # Gráfico para o curso selecionado
    fig3 = px.bar(
        retencao_curso.reset_index(), 
        x="AnoAdmissao", 
        y="Taxa Retenção",
        title=f"Taxa de Retenção para o Curso de {selected_curso}",
        labels={"AnoAdmissao": "Ano de Admissão", "Taxa Retenção": "Taxa de Retenção (%)"},
        text_auto=".1f",
        color_discrete_sequence=["#2ca02c"]  # Cor verde para retenção
    )

    fig3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning(f"Não há dados de retenção para o curso {selected_curso}")

# Mostrar estatísticas adicionais
st.header("Estatísticas de Retenção")

# Calcular métricas gerais
total_alunos = len(filtered_df)
total_retencao = len(filtered_df[filtered_df["SituacaoAlunoAgrupada"] == "Retenção"])
taxa_geral_retencao = (total_retencao / total_alunos) * 100 if total_alunos > 0 else 0

# Exibir métricas em colunas
col1, col2, col3 = st.columns(3)
col1.metric("Total de Alunos", total_alunos)
col2.metric("Alunos em Retenção", total_retencao)
col3.metric("Taxa Geral de Retenção", f"{taxa_geral_retencao:.1f}%")

# Mostrar dados brutos
st.header("Dados Detalhados")
st.dataframe(filtered_df)