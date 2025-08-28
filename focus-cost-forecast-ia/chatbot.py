# chatbot.py

# Importar as bibliotecas necessárias
import os
import streamlit as st
import pandas as pd
import openai

# Configurar a chave da API do OpenAI
# SUBSTITUA "SUA_CHAVE_AQUI" PELA SUA CHAVE DE API REAL
openai.api_key = "SUA_CHAVE_AQUI" 

# Carregar o dataset
# O caminho do arquivo precisa ser ajustado para onde o arquivo está salvo.
# Exemplo: df = pd.read_csv('data/focus_simulated_dataset_focus_1.2.csv')
file_path = "focus_simulated_dataset_focus_1.2.csv"
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"Erro: O arquivo '{file_path}' não foi encontrado.")
    st.stop()

# Título da aplicação
st.title("🤖 Chatbot FinOps")
st.write("Pergunte-me sobre os custos da nuvem. Por exemplo: 'Qual foi o custo total no mês passado?'")

# Inicializa o histórico do chat no estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens do histórico do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Processa a entrada do usuário
if prompt := st.chat_input("Pergunte-me sobre os custos..."):
    # Adiciona a mensagem do usuário ao histórico do chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown("Pensando...")

        # Formata os dados do DataFrame para o prompt
        data_info = f"Dados de custo:\n{df.to_string()}\n"
        
        # Cria o prompt completo para a IA
        full_prompt = (
            "Você é um chatbot de FinOps, capaz de responder perguntas sobre os dados de custo de nuvem fornecidos.\n"
            "Responda apenas com base nos dados fornecidos e em suas instruções. Não invente informações.\n"
            "Se a pergunta não puder ser respondida com os dados fornecidos, responda que você só pode analisar os dados de custo de nuvem.\n"
            f"Pergunta: {prompt}\n\n{data_info}\nResposta:"
        )

        try:
            # Chama a API da OpenAI
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um chatbot de FinOps."},
                    {"role": "user", "content": full_prompt}
                ]
            )
            # Extrai e exibe a resposta da IA
            assistant_response = response.choices[0].message.content
            st.markdown(assistant_response)
            
            # Adiciona a resposta da IA ao histórico do chat
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
        except Exception as e:
            st.error(f"Desculpe, houve um erro ao processar sua solicitação: {e}")