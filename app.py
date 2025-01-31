from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hola! La teva API Flask funciona correctament!"

if __name__ == '__main__':
    import os

port = int(os.environ.get("PORT", 5000))
app.run(debug=False, host='

