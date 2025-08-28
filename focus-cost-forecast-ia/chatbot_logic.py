import pandas as pd
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# Adicione a biblioteca que faz a previsão de custos aqui
# from src.cost_forecasting import get_forecast_plot

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def load_data():
    try:
        df_raw = pd.read_csv("data/raw/focus_simulated_dataset_focus_1.2.csv")
        df_monthly = pd.read_csv("data/processed/monthly_costs_by_provider.csv")
        
        df_raw['ChargePeriodStart'] = pd.to_datetime(df_raw['ChargePeriodStart'])
        df_monthly['ds'] = pd.to_datetime(df_monthly['ds'])
        
        return df_raw, df_monthly
    except FileNotFoundError:
        return None, None

def get_chatbot_response(prompt):
    df_raw, df_monthly = load_data()

    if df_raw is None or df_monthly is None:
        return "Desculpe, não consegui carregar os dados. Verifique se os arquivos CSV estão nos diretórios corretos."

    raw_data_context = df_raw.head().to_markdown() + "\n...\n" + df_raw.tail().to_markdown()
    monthly_data_context = df_monthly.head().to_markdown() + "\n...\n" + df_monthly.tail().to_markdown()

    # O prompt do sistema agora inclui informações sobre o que a IA pode fazer
    system_prompt = (
        "Você é um analista FinOps. Você pode responder perguntas sobre custos e também sobre previsões. "
        "Use o contexto dos dados fornecidos para responder. "
        "Se a pergunta for sobre previsão de custos, retorne a string 'FORECAST_REQUEST'. "
        "Para outras perguntas, responda com base nos dados. "
        f"Dados Brutos:\n{raw_data_context}\n\n"
        f"Dados Mensais:\n{monthly_data_context}"
    )

    try:
        response = model.generate_content(
            f"{system_prompt}\n\nPergunta do usuário: {prompt}"
        )

        # Checa se a IA identificou uma intenção de previsão
        if "FORECAST_REQUEST" in response.text:
            # Aqui você chamaria a função do seu novo arquivo de forecasting
            # forecast_plot = get_forecast_plot(df_monthly)
            # return "Aqui está a previsão de custos para os próximos meses."
            return "Desculpe, a funcionalidade de previsão ainda está em desenvolvimento. Mas eu sei que você perguntou sobre isso!"

        return response.text
    except Exception as e:
        return f"Desculpe, algo deu errado com a IA. Erro: {e}"