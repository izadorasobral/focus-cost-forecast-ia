import streamlit as st
import pandas as pd
import os
import sys

# Adiciona o diretório-pai (raiz do projeto) ao caminho do Python para
# que o chatbot possa encontrar a pasta 'src'.
# O caminho pode variar dependendo de onde o notebook está.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Importa a lógica do chatbot
sys.path.append(os.path.join(project_root, 'src'))
from chatbot_logic import get_chatbot_response

# Define o título da aplicação com o ícone do robô
st.title("🤖 Chatbot FinOps")

# Inicializa o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens do histórico do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Obtém a entrada do usuário
if prompt := st.chat_input("Pergunte-me algo sobre os custos..."):
    # Adiciona a mensagem do usuário ao histórico do chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Exibe a mensagem do usuário na tela
    with st.chat_message("user"):
        st.markdown(prompt)

    # Obtém a resposta do chatbot (a lógica real da IA está em 'src/chatbot_logic.py')
    response = get_chatbot_response(prompt)
    
    # Adiciona a resposta do assistente ao histórico do chat
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
