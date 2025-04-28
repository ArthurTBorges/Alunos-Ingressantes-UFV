#!/usr/bin/env python
# coding: utf-8

# In[5]:


pip install jupyterlab


# In[6]:


import pandas as pd
 
import csv
import numpy as np 
import matplotlib.pyplot as plt 
from decimal import Decimal
import plotly.express as px
df = pd.read_csv('alunos-ingressantes.csv', sep=';',encoding='latin-1')

df["Curso"]=df["Curso"].replace(["Física - Licenciatura", "Matemática - Licenciatura","Química - Licenciatura","Educação Física - Licenciatura","Ciências Biológicas - Licenciatura"],["Física", "Matemática","Química","Educação Física","Ciências Biológicas"])
display(df)


# In[7]:


df2=df[df["NivelAgrupado"] == "Graduação"]
df3=df2[df2["Campus"] == "Florestal"]
df4=df2[df2["Campus"] == "Viçosa"]
df5=df2[df2["Campus"] == "Rio Paranaíba"]
df3


# In[8]:


df_group1 = df3.groupby("AnoAdmissao").count().reset_index()
df_group1[['AnoAdmissao','Campus']]
dg1=df_group1[['AnoAdmissao','Campus']].rename(columns={
    "AnoAdmissao": "AnoAdmissao",
    "Campus": "Florestal"})
dg1


# In[9]:


df_group2 = df4.groupby("AnoAdmissao").count().reset_index()
df_group2[['AnoAdmissao','Campus']]

dg2=df_group2[['AnoAdmissao','Campus']].rename(columns={
    "AnoAdmissao": "AnoAdmissao",
    "Campus": "Viçosa"})
dg2


# In[10]:


data_df = df3.groupby(['AnoAdmissao', 'Curso']).agg(avg_age=('AnoAdmissao', 'mean'), count=('AnoAdmissao', 'count'))
  
data_df = data_df.reset_index() 
print(data_df.head()) 
data_df.shape 


# In[11]:


t=df3.groupby(['AnoAdmissao', 'Curso']).agg(avg_age=('AnoAdmissao', 'mean'), count=('AnoAdmissao', 'count'))


# In[12]:


t


# In[13]:


# replace column values with collection


# In[14]:


fig = px.bar(data_df, x="AnoAdmissao", y="count", color="Curso", barmode="group")
fig


# In[46]:


df_group3 = df5.groupby("AnoAdmissao").count().reset_index()
df_group3[['AnoAdmissao','Campus']]

dg3=df_group3[['AnoAdmissao','Campus']].rename(columns={
    "AnoAdmissao": "AnoAdmissao",
    "Campus": "Rio Paranaíba"})
dg3


# In[47]:


m = pd.merge(dg1, dg2, on = "AnoAdmissao")
m


# In[48]:


m1 = pd.merge(m, dg3, on = "AnoAdmissao")
m1


# In[49]:


m1.plot(x="AnoAdmissao", y=["Florestal","Rio Paranaíba","Viçosa"], kind="bar", figsize=(9, 7))


# In[50]:


dh3=df3[df3["SituacaoAluno"] == "Conclusão"]
dh4=df4[df4["SituacaoAluno"] == "Conclusão"]
dh5=df5[df5["SituacaoAluno"] == "Conclusão"]
dh3


# In[51]:


data_dh = dh3.groupby(['AnoAdmissao', 'Curso']).agg(avg_age=('AnoAdmissao', 'mean'), count=('AnoAdmissao', 'count'))
  
data_dh = data_dh.reset_index() 
print(data_dh.head()) 
data_dh.shape 


# In[52]:


df_group3 = dh3.groupby("AnoAdmissao").count().reset_index()
df_group3[['AnoAdmissao','Campus']]

dt=df_group3[['AnoAdmissao','Campus']].rename(columns={
    "AnoAdmissao": "AnoAdmissao",
    "Campus": "Florestal"})
dt


# In[53]:


fig2 = px.line(data_dh, x="AnoAdmissao", y="count", color="Curso")
fig2


# In[54]:


pd.set_option('display.max_rows', None)
df_group4 = df3.groupby("Naturalidade").count().reset_index()
df_group4[['Naturalidade','Campus']]

dl=df_group4[['Naturalidade','Campus']].rename(columns={
    "Naturalidade": "Naturalidade",
    "Campus": "Florestal"})

dl.sort_values(by='Florestal', ascending=False)

 


# In[55]:


pd.set_option('display.max_rows', None)
df_group5 = df4.groupby("Naturalidade").count().reset_index()
df_group5[['Naturalidade','Campus']]

dk=df_group5[['Naturalidade','Campus']].rename(columns={
    "Naturalidade": "Naturalidade",
    "Campus": "Viçosa"})

dk.sort_values(by='Viçosa', ascending=False)
dv=dk.sort_values(by='Viçosa', ascending=False)
dv
 


# In[56]:


pd.set_option('display.max_rows', None)
df_group6 = df5.groupby("Naturalidade").count().reset_index()
df_group6[['Naturalidade','Campus']]

dk1=df_group6[['Naturalidade','Campus']].rename(columns={
    "Naturalidade": "Naturalidade",
    "Campus": "Rio Paranaíba"})

dk1.sort_values(by='Rio Paranaíba', ascending=False)
drp=dk1.sort_values(by='Rio Paranaíba', ascending=False)
drp


# In[57]:


dm=dl.sort_values(by='Florestal', ascending=False)
dm


# In[58]:


dfAM = pd.read_csv('Alunos Matriculados.csv', sep=';',encoding='latin-1')

display(dfAM)


# In[59]:


data_dfAM = dfAM.groupby(['Ano', 'Áreas/Cursos']).agg(avg_age=('Ano', 'mean'), count1=('Mat. Sem. 1 Total', 'sum'), count2=('Mat. Sem. 2 Total', 'sum'))
  
data_dfAM = data_dfAM.reset_index() 
print(data_dfAM.head()) 
data_dfAM.shape


# In[60]:


data_dgAM = data_dfAM.groupby(['Ano']).agg(avg_age=('Ano', 'mean'), Semestre_1=('count1', 'sum'), Semestre_2=('count2', 'sum'))
  
data_dgAM = data_dgAM.reset_index() 
print(data_dgAM.head()) 
data_dgAM.shape


# In[61]:


data_dfAD = dfAM.groupby(['Ano', 'Áreas/Cursos']).agg(avg_age=('Ano', 'mean'), count1=('Dip. Sem. 1 Total', 'sum'), count2=('Dip. Sem. 2 Total', 'sum'))
  
data_dfAD = data_dfAD.reset_index() 
print(data_dfAD.head()) 
data_dfAD.shape


# In[62]:


data_dgAD = data_dfAD.groupby(['Ano']).agg(avg_age=('Ano', 'mean'), Semestre_1=('count1', 'sum'), Semestre_2=('count2', 'sum'))
  
data_dgAD = data_dgAD.reset_index() 
print(data_dgAD.head()) 
data_dgAD.shape


# In[63]:


f = data_dgAD.eval('Formandos =Semestre_1+ Semestre_2')
print(f)


# In[64]:


cid0=df3.loc[(df3["Naturalidade"] == 'Belo Horizonte') | (df3["Naturalidade"] == 'Betim')| (df3["Naturalidade"] == 'Pará de Minas')]
cid = cid0.groupby(['AnoAdmissao', 'Naturalidade']).agg(avg_age=('AnoAdmissao', 'mean'), count=('AnoAdmissao', 'count'))
cid = cid.reset_index()  
cid


# In[ ]:





# In[65]:


cidc=df3.loc[(df3["Naturalidade"] == 'Belo Horizonte') | (df3["Naturalidade"] == 'Betim')| (df3["Naturalidade"] == 'Pará de Minas')]
cidcc = cidc.groupby(['AnoAdmissao', 'Naturalidade','Curso']).agg(avg_age=('AnoAdmissao', 'mean'), count=('AnoAdmissao', 'count'))
cidcc = cidcc.reset_index()  
cidcc


# In[3]:


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv('alunos-ingressantes.csv', sep=';',encoding='latin-1')

df["Curso"]=df["Curso"].replace(["Física - Licenciatura", "Matemática - Licenciatura","Química - Licenciatura","Educação Física - Licenciatura","Ciências Biológicas - Licenciatura"],["Física", "Matemática","Química","Educação Física","Ciências Biológicas"])


df2=df[df["NivelAgrupado"] == "Graduação"]
df3=df2[df2["Campus"] == "Florestal"]
df4=df2[df2["Campus"] == "Viçosa"]
df5=df2[df2["Campus"] == "Rio Paranaíba"]
df_group1 = df3.groupby("AnoAdmissao").count().reset_index()
df_group1[['AnoAdmissao','Campus']]
dg1=df_group1[['AnoAdmissao','Campus']].rename(columns={
    "AnoAdmissao": "AnoAdmissao",
    "Campus": "Florestal"})
df_group2 = df4.groupby("AnoAdmissao").count().reset_index()
df_group2[['AnoAdmissao','Campus']]

dg2=df_group2[['AnoAdmissao','Campus']].rename(columns={
    "AnoAdmissao": "AnoAdmissao",
    "Campus": "Viçosa"})
data_df = df3.groupby(['AnoAdmissao', 'Curso']).agg(avg_age=('AnoAdmissao', 'mean'), count=('AnoAdmissao', 'count'))

data_df = data_df.reset_index()


# In[ ]:






# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




