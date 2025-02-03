from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hola! La teva API Flask funciona correctament!"

if __name__ == '__main__':
    import os

app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# La teva API Key de NewsAPI
API_KEY = os.getenv("NEWSAPI_KEY")
import requests
from flask import Flask, jsonify

app = Flask(__name__)


API_KEY = "ac4a581e87f749018d8fbc172cadcca6"

@app.route('/noticies')  # <- Aquesta línia ha d'existir exactament així
def obtenir_noticies():
    url = f"https://newsapi.org/v2/everything?q=forex OR economia OR mercats&language=es&sortBy=publishedAt&apiKey={API_KEY}"
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dades = resposta.json()
        articles = dades.get("articles", [])

        noticies_formatades = []
        for article in articles[:10]:  # Agafem només les 10 primeres notícies
            noticies_formatades.append({
                "títol": article["title"],
                "descripció": article["description"],
                "url": article["url"],
                "publicat": article["publishedAt"]
            })

        return jsonify(noticies_formatades)
    else:
        return jsonify({"error": "No s'han pogut obtenir notícies"}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

"

@app.route('/noticies')
def obtenir_noticies():
    url = f"https://newsapi.org/v2/everything?q=forex OR economia OR mercats&language=es&sortBy=publishedAt&apiKey={API_KEY}"
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dades = resposta.json()
        articles = dades.get("articles", [])

        noticies_formatades = []
        for article in articles[:10]:  # Limitem a 10 notícies per resposta
            noticies_formatades.append({
                "títol": article["title"],
                "descripció": article["



