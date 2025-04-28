import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")


dfAM = pd.read_csv('Alunos Matriculados.csv', sep=';',encoding='latin-1')
dfAM['Áreas/Cursos'] = dfAM['Áreas/Cursos'].str.strip()

data_dfAD = dfAM.groupby(['Ano', 'Áreas/Cursos']).agg(avg_age=('Ano', 'mean'), count1=('Dip. Sem. 1 Total', 'sum'),
                                                      count2=('Dip. Sem. 2 Total', 'sum'))
data_dfAD = data_dfAD.reset_index()

data_dgAD = data_dfAD.groupby(['Ano']).agg(avg_age=('Ano', 'mean'), Semestre_1=('count1', 'sum'),
                                           Semestre_2=('count2', 'sum'))
data_dgAD = data_dgAD.reset_index()
f = data_dgAD.eval('Formandos =Semestre_1+ Semestre_2')
fc = data_dfAD.eval('Formandos =count1+ count2')

st.title("Diplomados")

fig1 = px.bar(fc, x="Ano", y="Formandos", barmode="group",title="Concluintes por curso")

a3=px.bar(f,x="Ano", y="Formandos",barmode="group",width=1050, height=600, text_auto='', title="Alunos diplomados no campus UFV-Florestal")
a3.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

st.plotly_chart(a3, use_container_width=True)

cursos = fc["Áreas/Cursos"].unique().tolist()

## Criar a caixa de seleção
opcao_selecionada = st.selectbox('Escolha uma opção:', cursos)
## Exibir a opção selecionada
st.write('Você selecionou:', opcao_selecionada)
filtered_df = fc[fc['Áreas/Cursos'] == opcao_selecionada]


fig1 = px.bar(filtered_df, x="Ano", y="Formandos", barmode="group",title="Matriculados por curso")
st.plotly_chart(fig1, use_container_width=True)