import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")


dfAM = pd.read_csv('Alunos Matriculados.csv', sep=';',encoding='latin-1')
dfAM['Áreas/Cursos'] = dfAM['Áreas/Cursos'].str.strip()


data_dfAM = dfAM.groupby(['Ano', 'Áreas/Cursos']).agg(avg_age=('Ano', 'mean'), Semestre_1=('Mat. Sem. 1 Total', 'sum'),
                                                      Semestre_2=('Mat. Sem. 2 Total', 'sum'))

data_dfAM = data_dfAM.reset_index()
data_dgAM = data_dfAM.groupby(['Ano']).agg(avg_age=('Ano', 'mean'), Semestre_1=('Semestre_1', 'sum'),
                                           Semestre_2=('Semestre_2', 'sum'))

data_dgAM = data_dgAM.reset_index()

# Using "with" notation


st.title("Matriculados por ano")




a3=px.bar(data_dgAM,x="Ano", y=["Semestre_1","Semestre_2"],barmode="group",width=1050, height=600, text_auto='', title="Alunos Matriculados no campus UFV-Florestal")
a3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

fig1 = px.bar(data_dfAM, x="Ano", y="Semestre_1", color="Áreas/Cursos", barmode="group",title="Matrículas anuais por curso")


st.plotly_chart(a3, use_container_width=True)

cursos = data_dfAM["Áreas/Cursos"].unique().tolist()

## Criar a caixa de seleção
opcao_selecionada = st.selectbox('Escolha uma opção:', cursos)
## Exibir a opção selecionada
st.write('Você selecionou:', opcao_selecionada)
filtered_df = data_dfAM[data_dfAM['Áreas/Cursos'] == opcao_selecionada]


fig1 = px.bar(filtered_df, x="Ano", y=["Semestre_1","Semestre_2"], barmode="group",title="Matriculados por curso")
st.plotly_chart(fig1, use_container_width=True)

