import pandas as pd
import streamlit as st
import plotly.express as px
import os

st.set_page_config(layout="wide")
st.write("Análise de Dados")

# Exportação dos arquivos csv
df = pd.read_csv("F:/Programacao/faculdade/Analise_Dados/app/77-c277-4174-b3d7-dbf2a2eec47d.csv", sep=",", encoding="utf-8")
df2 = pd.read_csv("F:/Programacao/faculdade/Analise_Dados/app/Atendimento_Usuarios_TRE-PI.csv", sep=';', encoding="utf-8")

# Formatação das STRINGS do primeiro dataframe
df.replace(to_replace=r'[-]', value=0, regex=True, inplace=True)

# Renderização de tabelas
st.dataframe(df)
st.dataframe(df2)

# Criação do gráfico em Barras do primeiro dataframe
contact_options = "VALOR EXEC"

inform = f"Filtrando dados por {contact_options} no gráfico de Barras:"
fig = px.bar(df, x="NUM EMP", y=contact_options, title=inform)
st.plotly_chart(fig, use_container_width=True)

# Criação do gráfico em pixa dinâmica do segundo dataframe
filter = ["Atribuído - Técnico", "Status", "Tipo"]

df2.dropna()
filter_selected = st.selectbox("Selecione um capo para mostrar no gráfico", filter)
fig2 = px.pie(df2, names=filter_selected)
st.plotly_chart(fig2, use_container_width=True)

# Criação do Gráfico de correlação de datas
fig = px.scatter(df2, x='Requerente - Requerente', y='Última atualização', width=500, height=500, title="Taxa de Atualização de cada requerente")
st.plotly_chart(fig, use_container_width=True)

# Criação do Próximo dataframe
df = pd.read_csv(os.getcwd() + '/app/ocorrencia.csv', sep=';', encoding="ISO-8859-1")

# Inserção da tabela do dataframe
st.title("Anpalise de Dados de Ocorrência Aeuronáuticas")

df['investigacao_status'] = df['investigacao_status'].fillna('ATIVA')

st.dataframe(df)

fig = px.scatter_geo(df, lat='ocorrencia_latitude', lon='ocorrencia_longitude')
#st.plotly_chart(fig, use_container_width=True)
fig2 = px.bar(df, x="ocorrencia_classificacao", y='ocorrencia_dia')
#st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    st.write('Relatório de localização de local de acidente.')
    st.plotly_chart(fig)
with c2:
    st.write('Relatório de datas de cada tipo de ocorrência.')
    st.plotly_chart(fig2)

df2 = df['ocorrencia_uf'].value_counts().to_frame('counts')

st.write('Gráfico que ilustra a quantidade de ocorrências por UF')
## Criação do gráfico de linhas quantidade de ocorrências por UF
fig = px.line(df2)

#df.replace(to_replace=None, value='ATIVA', inplace=True)

#fig = px.line(df, x='ocorrencia_uf' , y='counts' )
st.plotly_chart(fig, use_container_width=True)

df2 = df['investigacao_status'].value_counts().to_frame('investigacao_status')

fig = px.pie(df2, names=['FINALIZADO', 'ATIVO'], values='investigacao_status')

fig2 = px.scatter(df, y='ocorrencia_uf', x='total_aeronaves_envolvidas', width=650, height=650, title="Taxa de Atualização de cada requerente")

c1, c2 = st.columns(2)
with c1:
    st.write('Relatório de localização de local de acidente.')
    st.plotly_chart(fig)
with c2:
    st.write('Relatório de datas de cada tipo de ocorrência.')
    st.plotly_chart(fig2)