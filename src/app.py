import pandas as pd
import json
import time
from dotenv import load_dotenv, find_dotenv
from groq import Groq
import streamlit as st
import os

load_dotenv(find_dotenv())

client = Groq(
    #Chama a api_key do arquivo .env
    api_key=os.environ.get('GROQ_API')#
)

print(type(Groq))

#1. Carregando os dados
historico = pd.read_csv('data/historico_atendimento.csv')
transacoes = pd.read_csv('data/transacoes.csv')
with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
    perfil = json.load(f)
with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
    produtos = json.load(f)


#2. Montando Contexto
CONTEXTO = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO R$: {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

#3. SYSTEM PROMPT
PROMPT = """
Você é um agente financeiro especializado em investimentos de baixo e médio risco.

OBJETIVO: Ensinar economia e indicar investimentos conforme dados fornecidos.

Regras:
NUNCA inventar informações.
Responder apenas sobre finanças, mercado financeiro e investimentos.
Usar somente dados fornecidos pelo usuário.
Se não souber, admitir e sugerir alternativas financeiras.
Sempre dar dicas práticas após explicações.
Indicar investimentos apenas com base nos dados do usuário.
Responder em até 3 parágrafos, de forma clara e direta.
Fora do escopo → informar que só trata de finanças.
Pedidos sensíveis (senhas, dados pessoais) → recusar.
Recomendações sem contexto → pedir perfil do investidor antes.
"""
#4. Inicilizar o histórico na sessão
if 'chat_history' not in st.session_state:
     st.session_state.chat_history = []
    
#5. Interface Streamlit
st.title('Agente financeiro Inteligente 💹')

#6. Mostrar histórico

for msg in st.session_state.chat_history:
    if msg['role'] == 'user':
          st.markdown(f'**Você:** {msg["content"]}')
    else:
     st.markdown(f'**Agente:** {msg["content"]}')

#6. Campo de entrada
USER_QUESTION = st.text_input('Digite sua pergunta:')
if USER_QUESTION:
    start_time = time.time()
    st.session_state.chat_history.append({'role':'user', 'content': USER_QUESTION})

     #Montar mensagens (prompt+contexto+histórico+nova_pergunta)
    messages = [{'role':'system', 'content':PROMPT},
                 {'role':'user', 'content': CONTEXTO}] + st.session_state.chat_history
     
     #Chamada ao Groq
    chat_completion = client.chat.completions.create(
          model='openai/gpt-oss-120b',
          messages=messages,
          temperature=0.2
     )
    latencia = time.time() - start_time
    resposta = chat_completion.choices[0].message.content

    #Adicionar resposta ao histórico
    st.session_state.chat_history.append({'role':'assistant', 'content': resposta})

    #Mostrar resposta
    st.subheader('Resposta do Agente:')
    st.write(resposta)

    #Métricas
    st.markdown('### Métricas da chamada')
    st.write(f'⏱ Latência: {latencia:.2f} segundos')
    st.write(f'Tokens prompt: {chat_completion.usage.prompt_tokens}')
    st.write(f'Tokens resposta: {chat_completion.usage.completion_tokens}')
    st.write(f'Token totais: {chat_completion.usage.total_tokens}')
