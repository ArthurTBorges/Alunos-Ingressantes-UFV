import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv('alunos-ingressantes.csv', sep=';',encoding='latin-1')



df["Curso"]=df["Curso"].replace(["Física - Licenciatura", "Matemática - Licenciatura","Química - Licenciatura","Educação Física - Licenciatura","Ciências Biológicas - Licenciatura"],["Física", "Matemática","Química","Educação Física","Ciências Biológicas"])

f1=df.loc[df['Curso']!="Mobilidade Acadêmica - Graduação"]
f2=f1.loc[f1['Curso']!="Estudante Não VInculado"]
f3=f2.loc[f1['Curso']!="Tecnologia em Análise e Desenvolvimento de Sistemas"]

df2=f3[f3["NivelAgrupado"] == "Graduação"]
df3=df2[df2["Campus"] == "Florestal"]
df4=df2[df2["Campus"] == "Viçosa"]
df5=df2[df2["Campus"] == "Rio Paranaíba"]


cursosf = df3["Curso"].unique().tolist()

t = {
    'Cursos': cursosf,
    }

tt = pd.DataFrame(t)


st.table(tt)