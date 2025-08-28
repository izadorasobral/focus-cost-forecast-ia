import pandas as pd
import json

def validate_focus_format(df):
    """Valida se o DataFrame segue o padrão FOCUS v1.2"""

    # Lista de colunas obrigatórias presentes no seu CSV
    required_columns = [
        'ChargePeriodStart', 'ChargePeriodEnd', 'ProviderName', 
        'EffectiveCost', 'ServiceName'
    ]

    # Verificar colunas obrigatórias
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing_columns}")

    # Validar formato de datas
    try:
        pd.to_datetime(df['ChargePeriodStart'])
        pd.to_datetime(df['ChargePeriodEnd'])
    except:
        raise ValueError("Formato de data inválido. Use ISO 8601: YYYY-MM-DDTHH:mm:ssZ")

    # Validar formato de tags (se existirem)
    if 'Tags' in df.columns:
        for tag in df['Tags'].dropna():
            try:
                if tag and tag != '{}':
                    json.loads(tag.replace("'", '"'))
            except json.JSONDecodeError:
                raise ValueError(f"Formato de tags inválido: {tag}")

    # Validar códigos de moeda
    if 'BillingCurrency' in df.columns:
        valid_currencies = ['USD', 'EUR', 'BRL', 'GBP', 'JPY', 'CAD', 'AUD']
        invalid_currencies = df[~df['BillingCurrency'].isin(valid_currencies)]['BillingCurrency'].unique()
        if len(invalid_currencies) > 0:
            print(f"Aviso: Moedas não padrão encontradas: {invalid_currencies}")

    return True