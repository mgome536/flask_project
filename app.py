import os
import requests
import json
import pandas as pd
from flask import Flask, Response, jsonify
from tipus_canvi import obtenir_dades_tipus_canvi, obtenir_tipus_canvi  # Importa les funcions
from model import preparar_dades, entrenar_model, predir_tipus_canvi  # Importa les funcions del model

app = Flask(__name__)

# API Key de NewsAPI
API_KEY = "ac4a581e87f749018d8fbc172cadcca6"

# Ruta per obtenir notícies
@app.route('/noticies', methods=['GET'])
def obtenir_noticies():
    url_1 = f"https://newsapi.org/v2/everything?q=forex OR economia OR mercats&language=es&sortBy=publishedAt&apiKey={API_KEY}&pageSize=50&page=1"
    resposta_1 = requests.get(url_1)
    
    if resposta_1.status_code != 200:
        return {"error": "Error en obtenir les primeres notícies"}, 500

    dades_1 = resposta_1.json()
    articles_1 = dades_1.get("articles", [])

    url_2 = f"https://newsapi.org/v2/everything?q=forex OR economia OR mercats&language=es&sortBy=publishedAt&apiKey={API_KEY}&pageSize=50&page=2"
    resposta_2 = requests.get(url_2)
    
    if resposta_2.status_code != 200:
        return {"error": f"Error en obtenir les segones notícies. Detalls: {resposta_2.text}"}, 500

    dades_2 = resposta_2.json()
    articles_2 = dades_2.get("articles", [])

    articles = articles_1 + articles_2

    noticies_formatades = []
    for article in articles[:100]:
        noticies_formatades.append({
            "títol": article["title"],
            "descripció": article["description"],
            "url": article["url"],
            "publicat": article["publishedAt"]
        })

    return Response(json.dumps(noticies_formatades, ensure_ascii=False), mimetype='application/json')

# Ruta per obtenir el tipus de canvi
@app.route('/tipus-canvi/<data>/<moneda_origen>/<moneda_destino>', methods=['GET'])
def tipus_canvi(data, moneda_origen, moneda_destino):
    dades = obtenir_dades_tipus_canvi(data)
    
    if isinstance(dades, dict):  # Si les dades s'han obtingut correctament
        tipus_canvi_resultat = obtenir_tipus_canvi(dades, moneda_origen, moneda_destino)
        return jsonify({'tipus_canvi': tipus_canvi_resultat})
    else:
        return jsonify({'error': dades})

# Ruta per entrenar el model
@app.route('/entrenar_model', methods=['GET'])
def entrenar():
    # Carregar les dades de notícies i tipus de canvi (exemple)
    noticies_df = pd.DataFrame({
        'data': ['2025-02-01', '2025-02-02'],
        'títol': ['Notícia 1', 'Notícia 2'],
        'descripció': ['Descripció de la notícia 1', 'Descripció de la notícia 2']
    })

    tipus_canvi_df = pd.DataFrame({
        'data': ['2025-02-01', '2025-02-02'],
        'tipus_canvi': [1.2, 1.25]  # Exemple de tipus de canvi USD/EUR
    })

    # Preparar les dades per al model
    df_final = preparar_dades(noticies_df, tipus_canvi_df)

    # Entrenar el model
    model, vectorizer = entrenar_model(df_final)

    # Retornar una resposta de confirmació
    return jsonify({'message': 'Model entrenat correctament!'})

# Ruta per fer una predicció
@app.route('/prediccio', methods=['GET'])
def prediccio():
    # Carregar les dades de notícies i tipus de canvi (exemple)
    noticies_df = pd.DataFrame({
        'data': ['2025-02-01', '2025-02-02'],
        'títol': ['Notícia 1', 'Notícia 2'],
        'descripció': ['Descripció de la notícia 1', 'Descripció de la notícia 2']
    })

    tipus_canvi_df = pd.DataFrame({
        'data': ['2025-02-01', '2025-02-02'],
        'tipus_canvi': [1.2, 1.25]
    })

    # Preparar les dades
    df_final = preparar_dades(noticies_df, tipus_canvi_df)

    # Entrenar el model (o carregar-lo si és necessari)
    model, vectorizer = entrenar_model(df_final)

    # Fer una predicció per a la nova notícia
    nova_noticia = "Nova notícia sobre els mercats financers..."
    tipus_canvi_prediccio = predir_tipus_canvi(model, vectorizer, nova_noticia)

    return jsonify({'tipus_canvi_prediccio': tipus_canvi_prediccio.tolist()})

# Executar l'aplicació
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))  # Utilitzar el port dinàmic assignat per Railway
