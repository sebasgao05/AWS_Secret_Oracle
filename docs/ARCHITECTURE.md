# 🏗️ Arquitectura - El Oráculo Visual

## Diagrama

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUARIO                                  │
│                    (Navegador Web)                                │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP :8501
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  AWS ECS (Fargate - Express Mode)                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Streamlit App (app.py)                   │  │
│  │                                                            │  │
│  │  ┌──────────┐  ┌──────────────┐  ┌────────────────────┐  │  │
│  │  │  UI Chat │  │ Game Logic   │  │  AI Clients        │  │  │
│  │  │          │  │              │  │                    │  │  │
│  │  │ - Pistas │  │ - Estado     │  │ - Bedrock (Claude) │  │  │
│  │  │ - Input  │  │ - Validación │  │ - NVIDIA (Gemma)   │  │  │
│  │  │ - Imagen │  │ - Flujo      │  │ - Visión (imagen)  │  │  │
│  │  └──────────┘  └──────────────┘  └─────────┬──────────┘  │  │
│  └─────────────────────────────────────────────┼─────────────┘  │
└────────────────────────────────────────────────┼────────────────┘
                                                 │
                    ┌────────────────────────────┼────────────┐
                    │                            │            │
                    ▼                            ▼            │
┌──────────────────────────────┐  ┌─────────────────────┐    │
│   API Gateway + Lambda       │  │  Amazon Bedrock     │    │
│   (Random Image API)         │  │                     │    │
│                              │  │  Claude 3.5 Haiku   │    │
│  GET /prod/random-image      │  │  (Visión + Texto)   │    │
│  → { url, key, size, ... }   │  │                     │    │
└──────────────┬───────────────┘  └─────────────────────┘    │
               │                                              │
               ▼                                              │
┌──────────────────────────────┐  ┌─────────────────────┐    │
│        Amazon S3             │  │    NVIDIA API        │    │
│  (oracle-random-images)      │  │                     │    │
│                              │  │  Gemma 3n (respaldo)│    │
│  Imágenes con presigned URL  │  │  (Visión + Texto)   │    │
└──────────────────────────────┘  └─────────────────────┘    │
```

## Estructura del proyecto

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
│   ├── ARCHITECTURE.md     # Este archivo
│   └── DEPLOY.md           # Guía de despliegue
├── Dockerfile
├── requirements.txt
├── .env.example
└── .gitignore
```

## Componentes

| Componente | Tecnología | Función |
|---|---|---|
| Frontend/Backend | Streamlit (Python) | UI de chat, lógica del juego, estado de sesión |
| Contenedor | Docker + ECS Fargate | Hosting serverless del contenedor |
| IA Principal | Amazon Bedrock - Claude 3.5 Haiku | Genera pistas y valida respuestas con visión |
| IA Respaldo | NVIDIA API - Gemma 3n | Fallback cuando Bedrock no está disponible |
| Imágenes | API Gateway → Lambda → S3 | Provee imágenes aleatorias con URLs firmadas |

## Flujo del juego

1. **Inicio**: La app llama al API (`/prod/random-image`) y obtiene una imagen aleatoria.
2. **Descarga**: Descarga la imagen desde la URL firmada de S3 y la convierte a base64.
3. **Pista**: Cuando el usuario pide pista, envía la imagen a Bedrock con un prompt que pide una descripción críptica/poética.
4. **Respuesta**: Cuando el usuario escribe una respuesta, envía la imagen + respuesta a Bedrock para validar si es correcta (acepta sinónimos).
5. **Fallback**: Si Bedrock falla, automáticamente usa Gemma a través de NVIDIA API.
6. **Fin**: Si acierta o se rinde, muestra la imagen y permite reiniciar.

## Estado de sesión (Streamlit)

```python
st.session_state = {
    "image_url": str,        # URL firmada de S3
    "image_base64": str,     # Imagen en base64 para los modelos
    "media_type": str,       # MIME type de la imagen
    "hints": list,           # Lista de pistas generadas
    "messages": list,        # Historial del chat
    "game_over": bool,       # Si el juego terminó
    "won": bool,             # Si el usuario ganó
    "actual_name": str,      # Nombre real de la imagen
    "hint_count": int,       # Contador de pistas usadas
}
```

## Variables de entorno

| Variable | Descripción |
|---|---|
| `AWS_REGION` | Región de AWS (us-east-1) |
| `AWS_ACCESS_KEY_ID` | Access key para Bedrock |
| `AWS_SECRET_ACCESS_KEY` | Secret key para Bedrock |
| `AWS_SESSION_TOKEN` | Token de sesión (opcional) |
| `IMAGE_API_URL` | URL del API de imágenes aleatorias |
| `BEDROCK_MODEL_ID` | ID del modelo de Bedrock |
| `NVIDIA_API_KEY` | API key de NVIDIA |
| `NVIDIA_MODEL_ID` | ID del modelo de NVIDIA |

## Seguridad (Producción)

- Usar **IAM Task Role** en ECS en lugar de access keys hardcodeadas.
- El Task Role necesita: `bedrock:InvokeModel` sobre el modelo específico.
- Las URLs de S3 son presigned y expiran en 500 segundos.
