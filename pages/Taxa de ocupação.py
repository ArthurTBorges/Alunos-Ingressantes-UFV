import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide")
st.title("Taxa de Ocupação - Campus Florestal")

# Dados de vagas por curso
vagas = {
    'Curso': ['Administração', 'Agronomia', 'Ciência da Computação',
              'Ciências Biológicas', 'Educação Física', 'Engenharia de Alimentos',
              'Física', 'Matemática', 'Química', 'Tecnologia em Gestão Ambiental'],
    'Nº de vagas': [60, 45, 50, 25, 50, 45, 25, 25, 25, 50]
}
vagas_df = pd.DataFrame(vagas)

# Mostrar tabela de vagas
st.subheader("Vagas por Curso no Campus Florestal")
st.table(vagas_df)

# Carregar os dados
df = pd.read_csv('alunos-ingressantes.csv', sep=';', encoding='latin-1')

# Filtrar apenas para o campus Florestal
df_florestal = df[df['Campus'] == 'Florestal']

# Verificar se há dados
if df_florestal.empty:
    st.warning("Nenhum dado encontrado para o campus Florestal.")
    st.stop()

# Sidebar com filtros
st.sidebar.header("Filtros")

# Filtro por nível de curso
nivel_options = df_florestal["NivelAgrupado"].unique().tolist()
selected_nivel = st.sidebar.multiselect("Selecione o nível:", nivel_options, default=nivel_options)

# Filtro por período
min_year = int(df_florestal["AnoAdmissao"].min())
max_year = int(df_florestal["AnoAdmissao"].max())
year_range = st.sidebar.slider("Selecione o período:", min_year, max_year, (min_year, max_year))

# Aplicar filtros
filtered_df = df_florestal[
    (df_florestal["NivelAgrupado"].isin(selected_nivel)) &
    (df_florestal["AnoAdmissao"].between(year_range[0], year_range[1]))
]

# Verificar se há dados após filtrar
if filtered_df.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# Análise de ocupação por curso e ano
st.header("Taxa de Ocupação por Curso")

# Calcular alunos que permaneceram (não evadiram)
alunos_permanentes = filtered_df[~filtered_df['SituacaoAlunoAgrupada'].isin(['Evasão', 'Abandono', 'Desligamento'])]

# Agrupar por curso e ano
ocupacao_por_curso = alunos_permanentes.groupby(['Curso', 'AnoAdmissao']).size().reset_index(name='Alunos')

# Juntar com os dados de vagas
ocupacao_por_curso = pd.merge(ocupacao_por_curso, vagas_df, on='Curso', how='left')

# Calcular taxa de ocupação
ocupacao_por_curso['Taxa Ocupação (%)'] = (ocupacao_por_curso['Alunos'] / ocupacao_por_curso['Nº de vagas']) * 100
ocupacao_por_curso['Taxa Ocupação (%)'] = ocupacao_por_curso['Taxa Ocupação (%)'].round(1)

# Selecionar curso para análise detalhada
curso_options = ocupacao_por_curso['Curso'].unique().tolist()
selected_curso = st.selectbox("Selecione um curso para análise detalhada:", curso_options)

# Gráfico de linha para taxa de ocupação geral
st.subheader("Evolução da Taxa de Ocupação")
fig_geral = px.line(
    ocupacao_por_curso,
    x='AnoAdmissao',
    y='Taxa Ocupação (%)',
    color='Curso',
    title='Taxa de Ocupação por Curso ao Longo dos Anos',
    labels={'AnoAdmissao': 'Ano de Admissão', 'Taxa Ocupação (%)': 'Taxa de Ocupação (%)'}
)
st.plotly_chart(fig_geral, use_container_width=True)

# Análise detalhada por curso selecionado
st.subheader(f"Análise Detalhada: {selected_curso}")

# Filtrar dados para o curso selecionado
curso_selecionado = ocupacao_por_curso[ocupacao_por_curso['Curso'] == selected_curso]

# Verificar se há dados
if not curso_selecionado.empty:
    # Gráfico de barras para o curso selecionado
    fig_curso = px.bar(
        curso_selecionado,
        x='AnoAdmissao',
        y=['Alunos', 'Nº de vagas'],
        barmode='group',
        title=f'Ocupação vs Vagas - {selected_curso}',
        labels={'AnoAdmissao': 'Ano de Admissão', 'value': 'Quantidade'},
        text_auto=True
    )
    
    # Adicionar linha da taxa de ocupação
    fig_curso.add_scatter(
        x=curso_selecionado['AnoAdmissao'],
        y=curso_selecionado['Taxa Ocupação (%)'],
        mode='lines+markers+text',
        name='Taxa Ocupação (%)',
        yaxis='y2',
        text=curso_selecionado['Taxa Ocupação (%)'],
        textposition='top center'
    )
    
    # Configurar eixo secundário
    fig_curso.update_layout(
        yaxis=dict(title='Quantidade de Alunos/Vagas'),
        yaxis2=dict(
            title='Taxa Ocupação (%)',
            overlaying='y',
            side='right',
            range=[0, 120]  # Fixar escala até 120% para visualização
        )
    )
    
    st.plotly_chart(fig_curso, use_container_width=True)
    
    # Mostrar métricas recentes
    ultimo_ano = curso_selecionado['AnoAdmissao'].max()
    dados_ultimo_ano = curso_selecionado[curso_selecionado['AnoAdmissao'] == ultimo_ano].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Número de Vagas", dados_ultimo_ano['Nº de vagas'])
    col2.metric("Alunos Permanentes", dados_ultimo_ano['Alunos'])
    col3.metric("Taxa de Ocupação", f"{dados_ultimo_ano['Taxa Ocupação (%)']}%")
else:
    st.warning(f"Não há dados de ocupação para o curso {selected_curso}")

# Mostrar dados completos
st.subheader("Dados Completos de Ocupação")
st.dataframe(ocupacao_por_curso.sort_values(['Curso', 'AnoAdmissao']))