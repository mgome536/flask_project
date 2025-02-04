import requests

def obtenir_dades_tipus_canvi(data):
    api_key = '7f85e30815e6442eb962f51ed2bc738a'  # Substitueix per la teva API Key
    url = f'https://openexchangerates.org/api/historical/{data}.json?app_id={api_key}'
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dades = resposta.json()
        return dades
    else:
        return f'Error {resposta.status_code}: No s\'han pogut obtenir les dades.'
  
def obtenir_tipus_canvi(dades, moneda_origen, moneda_destino):
    try:
        tipus_canvi = dades['rates'][moneda_destino] / dades['rates'][moneda_origen]
        return tipus_canvi
    except KeyError:
        return f'Error: Moneda no trobada en les dades.'

