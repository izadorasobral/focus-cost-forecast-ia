import pandas as pd
import json
from datetime import datetime, timedelta

def convert_to_focus_format(forecast_df, original_df):
    """Converte resultados de previsão para formato FOCUS"""

    # Criar DataFrame no formato FOCUS para previsões
    focus_forecast = pd.DataFrame({
        'Charge Period Start': forecast_df['ds'],
        'Charge Period End': forecast_df['ds'] + pd.DateOffset(months=1) - pd.DateOffset(seconds=1),
        'Provider': forecast_df['Provider'],
        'Service Category': 'Forecast',
        'Service Name': 'CostForecast',
        'Charge Category': 'Prediction',
        'Effective Cost': forecast_df['yhat'],
        'Billed Cost': forecast_df['yhat'],
        'Pricing Category': 'Forecast',
        'Region Name': 'Global',
        'Forecast Upper Bound': forecast_df['yhat_upper'],
        'Forecast Lower Bound': forecast_df['yhat_lower'],
        'Confidence Interval': forecast_df['yhat_upper'] - forecast_df['yhat_lower'],
        'Generated Timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    })

    # Formatar datas no padrão ISO 8601
    focus_forecast['Charge Period Start'] = focus_forecast['Charge Period Start'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    focus_forecast['Charge Period End'] = focus_forecast['Charge Period End'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    return focus_forecast

def save_focus_compliant_csv(df, filepath):
    """Salva DataFrame em formato CSV compatível com FOCUS"""

    # Ordenar colunas de acordo com o padrão FOCUS
    focus_columns = [
        'Charge Period Start', 'Charge Period End', 'Provider', 'Service Category',
        'Service Name', 'Charge Category', 'Effective Cost', 'Billed Cost',
        'Pricing Category', 'Region Name'
    ]

    # Manter apenas colunas presentes no DataFrame
    available_columns = [col for col in focus_columns if col in df.columns]
    additional_columns = [col for col in df.columns if col not in focus_columns]

    # Reordenar colunas
    df = df[available_columns + additional_columns]

    # Salvar CSV
    df.to_csv(filepath, index=False, date_format='%Y-%m-%dT%H:%M:%SZ')