import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Funció per preparar les dades de les notícies i el tipus de canvi
def preparar_dades(noticies_df, tipus_canvi_df):
    # Unir les dades de notícies i tipus de canvi per la data
    df_final = pd.merge(noticies_df, tipus_canvi_df, on='data')
    return df_final

# Funció per entrenar el model predictiu
def entrenar_model(df_final):
    # Preprocessament de les dades
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df_final['descripció'])
    y = df_final['tipus_canvi']

    # Dividir les dades en conjunt d'entrenament i test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear i entrenar el model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Avaluar el model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'Error quadràtic mitjà: {mse}')

    # Guardar el model i el vectoritzador
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')

    return model, vectorizer

# Funció per fer prediccions amb el model
def predir_tipus_canvi(model, vectorizer, nova_noticia):
    # Preprocessament de la nova notícia
    X_nova_noticia = vectorizer.transform([nova_noticia])
    tipus_canvi_prediccio = model.predict(X_nova_noticia)
    return tipus_canvi_prediccio
