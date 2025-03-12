import os
import requests
import json
import pandas as pd
import sqlite3
from flask import Flask, Response, jsonify, request
from tipus_canvi import obtenir_dades_tipus_canvi, obtenir_tipus_canvi
from model import preparar_dades, entrenar_model, predir_tipus_canvi
from datetime import datetime
import joblib
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# API Key de NewsAPI desde variables de entorno
API_KEY = os.getenv('NEWS_API_KEY')

def crear_base_de_dades():
    conn = sqlite3.connect('prediccions.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediccions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            noticia TEXT,
            tipus_canvi_prediccio REAL
        )
    ''')
    conn.commit()
    conn.close()

crear_base_de_dades()

def connect_db():
    return sqlite3.connect('database.db')

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

@app.route('/tipus-canvi/<data>/<moneda_origen>/<moneda_destino>', methods=['GET'])
def tipus_canvi(data, moneda_origen, moneda_destino):
    dades = obtenir_dades_tipus_canvi(data)

    if isinstance(dades, dict):
        tipus_canvi_resultat = obtenir_tipus_canvi(dades, moneda_origen, moneda_destino)
        return jsonify({'tipus_canvi': tipus_canvi_resultat})
    else:
        return jsonify({'error': dades})

@app.route('/entrenar_model', methods=['GET'])
def entrenar():
    noticies_df = pd.DataFrame({
        'data': ['2025-02-01', '2025-02-02'],
        'títol': ['Notícia 1', 'Notícia 2'],
        'descripció': ['Descripció de la notícia 1', 'Descripció de la notícia 2']
    })

    tipus_canvi_df = pd.DataFrame({
        'data': ['2025-02-01', '2025-02-02'],
        'tipus_canvi': [1.2, 1.25]
    })

    df_final = preparar_dades(noticies_df, tipus_canvi_df)
    model, vectorizer = entrenar_model(df_final)

    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')

    return jsonify({'message': 'Model entrenat correctament!'})

@app.route('/prediccio', methods=['GET'])
def prediccio():
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')

    nova_noticia = "Nova notícia sobre els mercats financers..."
    tipus_canvi_prediccio = predir_tipus_canvi(model, vectorizer, nova_noticia)

    conn = sqlite3.connect('prediccions.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO prediccions (data, noticia, tipus_canvi_prediccio)
        VALUES (?, ?, ?)
    ''', (datetime.now(), nova_noticia, tipus_canvi_prediccio.tolist()[0]))
    conn.commit()
    conn.close()

    return jsonify({'tipus_canvi_prediccio': tipus_canvi_prediccio.tolist()})

@app.route('/predict', methods=['POST'])
def predict():
    nova_noticia = request.json['noticia']
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')

    X_nova_noticia = vectorizer.transform([nova_noticia])
    tipus_canvi_prediccio = model.predict(X_nova_noticia)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO prediccions (data, noticia, tipus_canvi_prediccio)
        VALUES (?, ?, ?)
    ''', (datetime.now(), nova_noticia, tipus_canvi_prediccio.tolist()[0]))
    conn.commit()
    conn.close()

    return jsonify({'tipus_canvi_prediccio': tipus_canvi_prediccio.tolist()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    