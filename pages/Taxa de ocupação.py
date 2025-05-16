import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide")

# Carregar os dados
df = pd.read_csv('datasets\\alunos-ingressantes.csv', sep=';', encoding='latin-1')

# Sidebar com filtros
st.sidebar.header("Filtros")

# Filtro por campus
campus_options = df["Campus"].dropna().unique().tolist()
campus_options.sort()
selected_campus = st.sidebar.selectbox("Selecione o campus:", campus_options)

# Filtrar dados pelo campus selecionado
df = df[df["Campus"] == selected_campus]

if df.empty:
    st.warning(f"Nenhum dado encontrado para o campus {selected_campus}.")
    st.stop()

# Título da página
st.title(f"Taxa de Ocupação - Campus {selected_campus}")

# Filtro por nível de curso
nivel_options = df["NivelAgrupado"].unique().tolist()
selected_nivel = st.sidebar.multiselect("Selecione o nível:", nivel_options, default=nivel_options)

# Filtro por período
min_year = int(df["AnoAdmissao"].min())
max_year = int(df["AnoAdmissao"].max())
year_range = st.sidebar.slider("Selecione o período:", min_year, max_year, (min_year, max_year))

# Aplicar filtros
filtered_df = df[
    (df["NivelAgrupado"].isin(selected_nivel)) &
    (df["AnoAdmissao"].between(year_range[0], year_range[1]))
]

# Verificar se há dados após os filtros
if filtered_df.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# Dados de vagas por curso
vagas = {
    'Curso': ['Administração', 'Agronomia', 'Ciência da Computação',
              'Ciências Biológicas', 'Educação Física', 'Engenharia de Alimentos',
              'Física', 'Matemática', 'Química', 'Tecnologia em Gestão Ambiental'],
    'Nº de vagas': [60, 45, 50, 25, 50, 45, 25, 25, 25, 50]
}
vagas_df = pd.DataFrame(vagas)

# ----------- NOVO GRÁFICO GERAL POR CAMPUS --------------

st.subheader("Taxa de Ocupação Geral por Campus")

# Alunos que permaneceram
alunos_permanentes_total = filtered_df[~filtered_df['SituacaoAlunoAgrupada'].isin(['Evasão', 'Abandono', 'Desligamento'])]

# Agrupamento geral por ano
ocupacao_geral = alunos_permanentes_total.groupby(['AnoAdmissao']).size().reset_index(name='Alunos')

# Vagas totais por ano (soma das vagas definidas na lista)
vagas_totais_por_ano = vagas_df['Nº de vagas'].sum()
ocupacao_geral['Nº de vagas'] = vagas_totais_por_ano

# Calcular taxa
ocupacao_geral['Taxa Ocupação (%)'] = (ocupacao_geral['Alunos'] / ocupacao_geral['Nº de vagas']) * 100
ocupacao_geral['Taxa Ocupação (%)'] = ocupacao_geral['Taxa Ocupação (%)'].round(1)

# Gráfico geral
fig_geral = px.bar(
    ocupacao_geral,
    x='AnoAdmissao',
    y=['Alunos', 'Nº de vagas'],
    barmode='group',
    title='Taxa de Ocupação Geral por Ano',
    labels={'AnoAdmissao': 'Ano de Admissão', 'value': 'Quantidade'},
    text_auto=True
)

fig_geral.add_scatter(
    x=ocupacao_geral['AnoAdmissao'],
    y=ocupacao_geral['Taxa Ocupação (%)'],
    mode='lines+markers+text',
    name='Taxa Ocupação (%)',
    yaxis='y2',
    text=ocupacao_geral['Taxa Ocupação (%)'],
    textposition='top center'
)

fig_geral.update_layout(
    yaxis=dict(title='Quantidade de Alunos/Vagas'),
    yaxis2=dict(
        title='Taxa Ocupação (%)',
        overlaying='y',
        side='right',
        range=[0, 120]
    )
)

st.plotly_chart(fig_geral, use_container_width=True)

# ----------- ANÁLISE DETALHADA POR CURSO ----------------

# Alunos que permaneceram
alunos_permanentes = filtered_df[~filtered_df['SituacaoAlunoAgrupada'].isin(['Evasão', 'Abandono', 'Desligamento'])]

# Agrupar por curso e ano
ocupacao_por_curso = alunos_permanentes.groupby(['Curso', 'AnoAdmissao']).size().reset_index(name='Alunos')

# Juntar com dados de vagas
ocupacao_por_curso = pd.merge(ocupacao_por_curso, vagas_df, on='Curso', how='left')

# Calcular taxa de ocupação
ocupacao_por_curso['Taxa Ocupação (%)'] = (ocupacao_por_curso['Alunos'] / ocupacao_por_curso['Nº de vagas']) * 100
ocupacao_por_curso['Taxa Ocupação (%)'] = ocupacao_por_curso['Taxa Ocupação (%)'].round(1)

# Selecionar curso para análise detalhada
curso_options = ocupacao_por_curso['Curso'].unique().tolist()
selected_curso = st.selectbox("Selecione um curso para análise detalhada:", curso_options)

# Análise detalhada
st.subheader(f"Análise Detalhada: {selected_curso}")
curso_selecionado = ocupacao_por_curso[ocupacao_por_curso['Curso'] == selected_curso]

if not curso_selecionado.empty:
    # Gráfico de barras
    fig_curso = px.bar(
        curso_selecionado,
        x='AnoAdmissao',
        y=['Alunos', 'Nº de vagas'],
        barmode='group',
        title=f'Ocupação vs Vagas - {selected_curso}',
        labels={'AnoAdmissao': 'Ano de Admissão', 'value': 'Quantidade'},
        text_auto=True
    )

    # Linha com taxa de ocupação
    fig_curso.add_scatter(
        x=curso_selecionado['AnoAdmissao'],
        y=curso_selecionado['Taxa Ocupação (%)'],
        mode='lines+markers+text',
        name='Taxa Ocupação (%)',
        yaxis='y2',
        text=curso_selecionado['Taxa Ocupação (%)'],
        textposition='top center'
    )

    fig_curso.update_layout(
        yaxis=dict(title='Quantidade de Alunos/Vagas'),
        yaxis2=dict(
            title='Taxa Ocupação (%)',
            overlaying='y',
            side='right',
            range=[0, 120]
        )
    )

    st.plotly_chart(fig_curso, use_container_width=True)

    # Métricas do último ano
    ultimo_ano = curso_selecionado['AnoAdmissao'].max()
    dados_ultimo_ano = curso_selecionado[curso_selecionado['AnoAdmissao'] == ultimo_ano].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Número de Vagas", dados_ultimo_ano['Nº de vagas'])
    col2.metric("Alunos Permanentes", dados_ultimo_ano['Alunos'])
    col3.metric("Taxa de Ocupação", f"{dados_ultimo_ano['Taxa Ocupação (%)']}%")
else:
    st.warning(f"Não há dados de ocupação para o curso {selected_curso}")
