# 🔮 El Oráculo Visual

Un juego interactivo donde un oráculo misterioso te da pistas crípticas y poéticas sobre una imagen oculta. Tu misión: adivinar qué muestra la imagen antes de agotar tus 5 pistas.

## ✨ Características

- **Pistas poéticas generadas por IA** — Cada pista es metafórica y progresivamente más reveladora
- **Validación inteligente** — Acepta sinónimos, variaciones y traducciones
- **Interfaz de chat** — Experiencia conversacional con el oráculo
- **Fallback automático** — Si Bedrock (Claude) falla, usa NVIDIA (Gemma) como respaldo
- **Imágenes aleatorias** — Cada partida es diferente

## 🛠️ Stack tecnológico

| Componente | Tecnología |
|---|---|
| Frontend/Backend | [Streamlit](https://streamlit.io/) (Python) |
| IA Principal | Amazon Bedrock — Claude 3.5 Haiku (visión) |
| IA Respaldo | NVIDIA API — Gemma 3n |
| Imágenes | API Gateway + Lambda + S3 |
| Hosting | Docker + AWS ECS Fargate |

## 📁 Estructura del proyecto

```
oraculo/
├── app.py                  # Interfaz de usuario (Streamlit)
├── src/
│   ├── config.py           # Variables de entorno y constantes
│   ├── game.py             # Lógica del estado del juego
│   ├── clients/
│   │   ├── bedrock.py      # Cliente de Amazon Bedrock (Claude)
│   │   └── nvidia.py       # Cliente de NVIDIA API (Gemma)
│   └── services/
│       ├── hints.py        # Generación de pistas
│       ├── validation.py   # Validación de respuestas
│       └── images.py       # Obtención de imágenes
├── scripts/
│   └── check_models.py     # Script de diagnóstico
├── docs/
│   ├── ARCHITECTURE.md     # Arquitectura del sistema
│   └── DEPLOY.md           # Guía de despliegue en AWS
├── Dockerfile
├── requirements.txt
├── .env.example
└── .gitignore
```

## 🚀 Inicio rápido

### Prerrequisitos

- Python 3.11+
- Acceso a Amazon Bedrock con Claude 3.5 Haiku habilitado
- (Opcional) API key de NVIDIA para el modelo de respaldo

### Instalación local

```bash
# Clonar el repositorio
git clone <tu-repo-url>
cd oraculo

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

### Ejecutar

```bash
streamlit run app.py
```

La app estará disponible en `http://localhost:8501`.

### Con Docker

```bash
docker build -t oraculo-visual .
docker run -p 8501:8501 --env-file .env oraculo-visual
```

## ⚙️ Configuración

Copia `.env.example` a `.env` y configura las siguientes variables:

| Variable | Descripción | Requerida |
|---|---|---|
| `AWS_REGION` | Región de AWS | Sí |
| `AWS_ACCESS_KEY_ID` | Access key de AWS | Sí |
| `AWS_SECRET_ACCESS_KEY` | Secret key de AWS | Sí |
| `AWS_SESSION_TOKEN` | Token de sesión temporal | No |
| `IMAGE_API_URL` | URL del API de imágenes | Sí |
| `BEDROCK_MODEL_ID` | ID del modelo en Bedrock | Sí |
| `NVIDIA_API_KEY` | API key de NVIDIA | No (fallback) |
| `NVIDIA_MODEL_ID` | Modelo de NVIDIA | No (fallback) |

## 🎮 Cómo jugar

1. Al iniciar, el oráculo te da la primera pista sobre una imagen oculta.
2. Escribe tu respuesta en el chat para intentar adivinar.
3. Si no aciertas, pide más pistas (máximo 5).
4. Las pistas van de muy abstractas (1-2) a casi directas (5).
5. Si te rindes, el oráculo revela la imagen.

## 🔍 Diagnóstico

Para verificar que tus credenciales y modelos están configurados correctamente:

```bash
python scripts/check_models.py
```

## 📚 Documentación

- [Arquitectura del sistema](docs/ARCHITECTURE.md)
- [Guía de despliegue en AWS](docs/DEPLOY.md)

## 📄 Licencia

MIT
