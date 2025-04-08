import spacy
import string
import unidecode
import joblib
import pandas as pd
import es_core_news_sm
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Cargar spaCy para español
nlp = spacy.load("es_core_news_sm")
nlp = es_core_news_sm.load()

# Cargar modelo y vectorizador entrenados
modelo = joblib.load("models/modelo.pkl")
vectorizador = joblib.load("models/vectorizador.pkl")

# Crear la aplicación FastAPI
app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")

# Definir un modelo de datos para la entrada (la pregunta)
class Pregunta(BaseModel):
    texto: str

# Diccionario de respuestas por categoría

df_respuestas = pd.read_csv("data/responses.csv")
respuestas = dict(zip(df_respuestas['categoria'], df_respuestas['respuesta']))

# Ruta para servir el index.html
@app.get("/")
def home():
    return FileResponse("./static/index.html", status_code=200)

# Endpoint para predecir la respuesta a una pregunta
@app.post("/consulta")
async def predecirRespuesta(pregunta: Pregunta):
    pregunta_procesada = preprocesar(pregunta.texto)
    X = vectorizador.transform([pregunta_procesada])
    
    # Predecir categoría
    categoria = modelo.predict(X)[0]
    precision = max(modelo.predict_proba(X)[0])

    if precision > 0.31:
        respuesta = respuestas.get(categoria)
    else:
        respuesta = "No entendí la consulta. ¿Podrías reformularla?"
        categoria = "Desconocido"
    
    return {
        "categoria": categoria,
        "respuesta": respuesta,
        "precision": precision
    }

def preprocesar(texto):
    texto = texto.lower()
    texto = unidecode.unidecode(texto)
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    doc = nlp(texto)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    
    return " ".join(tokens)