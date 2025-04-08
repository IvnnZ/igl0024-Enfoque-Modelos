import pandas as pd
import spacy
import string
import unidecode
import es_core_news_sm
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Cargar el idioma español de spaCy
nlp = spacy.load("es_core_news_sm")
nlp = es_core_news_sm.load()

# Leer CSV
data = pd.read_csv("data/faqs.csv")

# Preprocesamiento
def preprocesar(texto):
    texto = texto.lower()  # minúsculas
    texto = unidecode.unidecode(texto)  # quitar tildes
    texto = texto.translate(str.maketrans('', '', string.punctuation))  # quitar puntuación

    doc = nlp(texto)
    tokens = [token.text.lower() for token in doc if token.text not in string.punctuation and not token.is_stop]

    return " ".join(tokens)

data['pregunta_procesada'] = data['pregunta'].apply(preprocesar)

# Vectorizar (TF-IDF)
vectorizador = CountVectorizer()
X = vectorizador.fit_transform(data['pregunta_procesada'])
y = data['categoria']

# Dividir los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# 4. Entrenar el clasificador Random Forest
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Evaluar el modelo
accuracy = modelo.predict(X_test)
print('Classification Report:')
print(classification_report(y_test, accuracy))

# 5. Guardar modelo y vectorizador para usar en la API
joblib.dump(modelo, 'models/modelo.pkl')
joblib.dump(vectorizador, 'models/vectorizador.pkl')

print("✅ Modelo y vectorizador entrenados y guardados correctamente.")