# Enfoque Modelos

Este proyecto utiliza el modelo Ranfom Forest para clasificar preguntas y predecir una respuesta.

## 🚀 Instalación en Local

### 1️⃣ Requisitos Previos

Asegúrate de tener instalado:

- Python 3.12<=
- pip

### 2️⃣ Instalación de Dependencias

Clona el repositorio y accede a la carpeta:

```bash
git clone https://github.com/IvnnZ/igl0024-Enfoque-Modelos.git
```

### 3️⃣ Configuración del Entorno

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

### 4️⃣ Ejecución de la API

Para ejecutar el servidor FastAPI:

```bash
uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000/docs`.

---
