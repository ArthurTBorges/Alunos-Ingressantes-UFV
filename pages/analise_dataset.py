import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard de Matrículas")

# Carregando os dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv('datasets\alunos-ingressantes.csv', sep=';', encoding='latin-1')
    df["Curso"] = df["Curso"].replace([
        "Física - Licenciatura", 
        "Matemática - Licenciatura",
        "Química - Licenciatura",
        "Educação Física - Licenciatura",
        "Ciências Biológicas - Licenciatura"
    ], [
        "Física", 
        "Matemática",
        "Química",
        "Educação Física",
        "Ciências Biológicas"
    ])
    return df

def salvar_colunas_e_valores_unicos(df, caminho_arquivo="valores_unicos_dataset.txt"):
    colunas_ignoradas = {"CodigoEstudante", "Naturalidade", "UF", "Pais"}
    
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write("Colunas e seus valores únicos no dataset:\n\n")
        for coluna in df.columns:
            if coluna in colunas_ignoradas:
                continue  # Ignora as colunas especificadas
            f.write(f"Coluna: {coluna}\n")
            unicos = df[coluna].dropna().unique()
            for valor in unicos:
                f.write(f"  - {valor}\n")
            f.write("\n")
    print(f"Arquivo '{caminho_arquivo}' gerado com sucesso.")



df = carregar_dados()
salvar_colunas_e_valores_unicos(df)


# Título principal
st.title("Dashboard de Matrículas Anuais")
st.write("Análise de alunos ingressantes por campus e curso")

# Seção de informações sobre o dataset
with st.expander("🔍 Informações sobre o Dataset", expanded=True):
    st.subheader("Dados Brutos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Colunas disponíveis:**")
        st.write(list(df.columns))
        
        st.write("**Total de registros:**", len(df))
        
        st.write("**Amostra dos dados:**")
        st.dataframe(df.head(3))
    
    with col2:
        st.write("**Estatísticas descritivas:**")
        st.write(df.describe(include='all'))
        
        st.write("**Contagem por Campus:**")
        st.write(df['Campus'].value_counts())

# Filtros
st.sidebar.header("Filtros")
campus_options = df['Campus'].unique()
selected_campus = st.sidebar.multiselect(
    "Selecione o(s) campus:", 
    options=campus_options, 
    default=campus_options
)

curso_options = df['Curso'].unique()
selected_curso = st.sidebar.multiselect(
    "Selecione o(s) curso(s):", 
    options=curso_options, 
    default=curso_options
)

# Aplicando filtros
df_filtered = df[
    (df['Campus'].isin(selected_campus)) & 
    (df['Curso'].isin(selected_curso))
]

# Processamento dos dados filtrados
df_graduacao = df_filtered[df_filtered["NivelAgrupado"] == "Graduação"]

# Criando DataFrames para cada campus
dfs = {
    campus: df_graduacao[df_graduacao["Campus"] == campus]
    for campus in selected_campus
}

# Agregações
data_dfs = {}
for campus in selected_campus:
    data_dfs[campus] = df_graduacao[df_graduacao["Campus"] == campus]\
        .groupby(['AnoAdmissao', 'Curso'])\
        .agg(count=('AnoAdmissao', 'count'))\
        .reset_index()

# Preparando dados para gráficos comparativos
comparison_data = []
for campus in selected_campus:
    temp_df = dfs[campus].groupby("AnoAdmissao").count().reset_index()
    temp_df = temp_df[['AnoAdmissao', 'Campus']].rename(columns={'Campus': campus})
    comparison_data.append(temp_df)

# Combinando dados para comparação
if len(comparison_data) > 0:
    merged_df = comparison_data[0]
    for df_temp in comparison_data[1:]:
        merged_df = pd.merge(merged_df, df_temp, on="AnoAdmissao", how="outer")

# Visualizações
if not df_filtered.empty:
    st.header("Visualizações")
    
    # Gráfico de barras por curso
    if len(selected_campus) == 1:
        fig_cursos = px.bar(
            data_dfs[selected_campus[0]], 
            x="AnoAdmissao", 
            y="count", 
            color="Curso", 
            barmode="group",
            title=f"Matrículas anuais por curso - Campus {selected_campus[0]}"
        )
        st.plotly_chart(fig_cursos, use_container_width=True)
    
    # Gráficos comparativos entre campus
    if len(selected_campus) > 1 and 'merged_df' in locals():
        col1, col2 = st.columns(2)
        
        with col1:
            fig_barras = px.bar(
                merged_df,
                x="AnoAdmissao", 
                y=selected_campus,
                barmode="group",
                title="Matrículas anuais - Comparação entre campus (Barras)"
            )
            st.plotly_chart(fig_barras, use_container_width=True)
        
        with col2:
            fig_linhas = px.line(
                merged_df,
                x="AnoAdmissao", 
                y=selected_campus,
                title="Matrículas anuais - Comparação entre campus (Linhas)"
            )
            st.plotly_chart(fig_linhas, use_container_width=True)
else:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")



# Mostrar dados filtrados
with st.expander("📊 Visualizar Dados Filtrados"):
    st.dataframe(df_filtered)