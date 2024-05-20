import pandas as pd
import streamlit as st
import plotly.express as px
import os

st.set_page_config(
                    layout="wide",
                    page_title="Análise de Dados",
                )
st.title("Análise de Dados - Ocorrência Aeuronáuticas Brasileiras (2007 - 2023)")

st.write("""
    A Aviação Civil desempenha um papel crucial na conectividade global e no transporte de passageiros e cargas em todo o mundo.
         No entanto, a segurança continua sendo uma prioridade primordial para a indústria da aviação.
         O registro e análise de ocorrências aeronáuticas são componentes essenciais para identificar tendências, áreas de melhoria e para aprimorar os padrõe
         de segurança.\n
         \nEste projeto propõe uma análise detalhada das ocorrências aeronáuticas na Aviação Civil Brasileira,
         o objetivo principal é extrair informações significativas dos dados disponíveis para entender melhor os padrões, causas e
         consequências dessas ocorrências.
""")

col1, col2, col3 = st.columns([1, 2, 1])  # Colunas com proporções de 1:2:1
with col2:
    st.image('airplane.png', width=800)

# Criação do Próximo dataframe
df = pd.read_csv(os.getcwd() + '/app/ocorrencia.csv', sep=';', encoding="ISO-8859-1")

# Inserção da tabela do dataframe
#st.subheader("Anpalise de Dados de Ocorrência Aeuronáuticas")

df['investigacao_status'] = df['investigacao_status'].fillna('ATIVA')

df4 = df[['ocorrencia_uf', 'total_aeronaves_envolvidas']].groupby('ocorrencia_uf').value_counts().reset_index()

df4 = df4.groupby('ocorrencia_uf')['count'].sum().reset_index()

st.subheader('Ilustração do conjunto de dados apresentando informações como data, hora, localização, tipo de ocorrência, status de investigação, quantidade de aeronaves envolvidas. ')
st.dataframe(df)

#df = df['ocorrencia_latitude'].dropna()

fig = px.scatter_geo(df, lat='ocorrencia_latitude', lon='ocorrencia_longitude', title="Relatório do local de acidente.")

fig2 = px.bar(df, x="ocorrencia_classificacao", y='ocorrencia_dia', title="Relatório de datas de cada tipo de ocorrência.")
fig2.update_layout(xaxis_title="Tipos das Ocorrências", yaxis_title="Data Ocorrências")

c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(fig)
    st.write("Procuramos ilustrar em um mapa a localização das ocorrências aéreas registradas baseadas em latitude e longitude, proporcionando uma representação visual clara da distribuição geográfica desses eventos, no entanto, é importante notar que algumas localizações podem não ser exibidas no mapa devido a possíveis incongruências nos dados. Essas inconsistências podem resultar em coordenadas geográficas inválidas ou ausentes, impedindo a exibição precisa no mapa.")
with c2:
    st.plotly_chart(fig2)
    st.write("""
             O gráfico acima destaca os tipos de ocorrências (acidentes, incidentes e incidentes graves) e as datas em que cada ocorrência ocorreu.
             Ao passar o mouse em cima do gráfico, é possível verificar a data de cada tipo de ocorrência.
             """)

df2 = df['ocorrencia_uf'].value_counts().to_frame('counts')

## Criação do gráfico de linhas quantidade de ocorrências por UF
fig = px.line(df2, title="Gráfico que ilustra a quantidade de ocorrências por UF")
fig.update_layout(xaxis_title="UF", yaxis_title="Quantidade")

#df.replace(to_replace=None, value='ATIVA', inplace=True)

st.plotly_chart(fig, use_container_width=True)
st.write("Este gráfico apresenta a distribuição geográfica da quantidade de ocorrências aeronáuticas por Unidade Federativa (UF) no Brasil. Esta visualização permite uma rápida comparação entre os diferentes Estados, destacando aqueles com maior e menor incidência de ocorrências aeronáuticas. Analisar essa distribuição pode ajudar na identificação de padrões regionais e na formulação de estratégias específicas para melhorar a segurança na aviação em áreas específicas do país.")

df2 = df['investigacao_status'].value_counts().to_frame('investigacao_status')

fig = px.pie(df2, names=['FINALIZADO', 'ATIVO'], values='investigacao_status', title="Relatório do status das investigações das ocorrências.")

total_envolvidas = df['total_aeronaves_envolvidas'].sum()

fig2 = px.scatter(df4, x='ocorrencia_uf', y='count', width=650, height=450, title="Quantidade de aviões envolvidos em cada Estado.<br>Total de Aeronaves: " + str(total_envolvidas))
fig2.update_layout(xaxis_title="UF", yaxis_title="Quantidade")
#df['data_igual'] = pd.to_datetime(df['ocorrencia_dia']) == pd.to_datetime('31/12/2023')
#print(df['data_igual'])

c1, c3, c2 = st.columns([2,.5,2])
with c1:
    st.plotly_chart(fig)
    st.write("O gráfico apresenta a distribuição percentual das investigações de ocorrências aeronáuticas, categorizadas em 'Finalizadas' e 'Ativas'. Cada categoria é representada por uma fatia do círculo, cujo tamanho reflete a proporção relativa do total de investigações. Essa visualização permite uma compreensão imediata da distribuição das investigações em termos de status, destacando a porcentagem de investigações que foram concluídas e aquelas que ainda estão em andamento. Analisar essa distribuição é crucial para avaliar a eficácia dos processos de investigação e para monitorar o progresso na resolução de ocorrências aeronáuticas, contribuindo assim para o aprimoramento contínuo da segurança na aviação.")
with c2:
    st.plotly_chart(fig2)
    st.write("Este gráfico apresenta a distribuição geográfica da quantidade de ocorrências aeronáuticas por Unidade Federativa (UF) no Brasil. Esta visualização permite uma rápida comparação entre os diferentes Estados, destacando aqueles com maior e menor incidência de ocorrências aeronáuticas. Analisar essa distribuição pode ajudar na identificação de padrões regionais e na formulação de estratégias específicas para melhorar a segurança na aviação em áreas específicas do país.")

df = pd.read_csv(os.getcwd() + '/app/fator_contribuinte.csv', sep=";", encoding="ISO-8859-1")

st.subheader('Análise Fator Contribuinte das Ocorrências')

st.dataframe(df, use_container_width=True)

q= 'FATOR OPERACIONAL'
n= 'INDISCIPLINA DE VOO'

df = df.query('fator_area == @q')
#df = df.query('fator_area == @q and fator_nome == @n')
qnt = df['fator_nome'].value_counts()

df['qnt_fator_nome'] = df['fator_nome'].map(qnt)

fig = px.bar(df, x='fator_nome', y='qnt_fator_nome',title="Comparação da quantidade de cada fator contribuinte.", text_auto='.2s')
fig.update_layout(xaxis_title="Nome do Fator Contribuinte", yaxis_title="Quantidade Fator Contribuinte")
st.plotly_chart(fig, use_container_width=True)
#df['fator_area'].value_counts().to_frame('fator_area')

#st.plotly_chart(fig)




df = pd.read_csv(os.getcwd() + '/app/recomendacao.csv', sep=';', encoding="ISO-8859-1")

#st.dataframe(df)

df.replace(to_replace='***', value="AGUARDANDO RESPOSTA", regex=False, inplace=True)



#count = df[['recomendacao_status', 'recomendacao_destinatario_sigla']].where(df['recomendacao_status'] == 'ADOTADA').groupby(df['recomendacao_destinatario_sigla']).value_counts().to_frame('count')

#print(count)

st.subheader("Recomendações, status e suas quantidades que foram ou não, adotadas pelas empresas.")

filter = ['ADOTADA', 'NÃO ADOTADA', 'AGUARDANDO RESPOSTA']
filter_select = st.selectbox("Selecione um Filtro", filter)

df_filter = df[['recomendacao_status']].where(df['recomendacao_status'] == filter_select).groupby(df['recomendacao_destinatario_sigla']).value_counts().reset_index()


st.dataframe(df_filter, use_container_width=True)

#print('================================')
#print(df_filter)

if(filter_select == 'AGUARDANDO RESPOSTA'):
    fig = px.line(df_filter, y='count', x='recomendacao_destinatario_sigla', title="Relatório de recomendações que estão AGUARDANDO RESPOSTA pelas empresas informadas no gráfico.")

elif(filter_select == 'NÃO ADOTADA'):
    fig = px.pie(df_filter, names='recomendacao_destinatario_sigla', values='count', title="Relatório de recomendações NÃO ADOTADAS pelas empresas informadas no gráfico.")
else:
    fig = px.bar(df_filter, y='count', x='recomendacao_destinatario_sigla', text_auto='2s', title="Relatório de recomendações que FORAM ADOTADAS pelas empresas informadas no gráfico.")
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(xaxis_title="Destinatários (Sigla)", yaxis_title="Qnt Recomendações (Adotadas)")

st.plotly_chart(fig, use_container_width=True)

st.header("CONCLUSÃO")
st.write("""
    Ao concluir este projeto de análise das ocorrências na aviação civil brasileira, fica evidente a importância de uma abordagem abrangente e proativa para aprimorar 
    a segurança operacional. A análise dos dados revelou padrões preocupantes e identificou diversos fatores contribuintes para as ocorrências,
    incluindo *erro humano, falhas de comunicação, condições meteorológicas adversas e deficiências de treinamento*. No entanto, com base nessas descobertas,
    podemos propor uma solução de melhoria para reduzir essas ocorrências e promover uma cultura de segurança robusta:\n\n
         
        ➢ Implementação de programas de treinamento contínuo: Investir em treinamento e capacitação contínuos para pilotos, tripulação e equipes de manutenção 
        é essencial para aprimorar habilidades técnicas e comportamentais, além de garantir a conformidade com os procedimentos operacionais padrão. 
         
        ➢ Melhoria na comunicação e coordenação: Reforçar a comunicação eficaz e a coordenação entre todos os responsáveis  envolvidos na aviação, incluindo pilotos, 
        controladores de tráfego aéreo, equipes de manutenção e autoridades regulatórias, é crucial para mitigar o risco de mal-entendidos e erros de comunicação que 
        possam contribuir para ocorrências.
         
    Em resumo, a redução das ocorrências na aviação civil brasileira exige uma abordagem multifacetada que englobe treinamento aprimorado, monitoramento eficaz, comunicação
    transparente e investimentos em tecnologias de segurança. Ao implementar essas soluções de melhoria de forma colaborativa e sustentada, podemos promover uma cultura de
    segurança robusta e garantir operações aéreas mais seguras e confiáveis para todos os envolvidos.
""")