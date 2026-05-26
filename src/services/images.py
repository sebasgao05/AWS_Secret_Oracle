"""Servicio de obtención y procesamiento de imágenes."""

import base64

import requests

from src.config import IMAGE_API_URL


def fetch_random_image() -> dict:
    """Obtiene metadata de una imagen aleatoria del API.

    Returns:
        Dict con la información de la imagen (url, key, size, etc.).
    """
    response = requests.get(IMAGE_API_URL, timeout=10)
    response.raise_for_status()
    return response.json()


def download_image_as_base64(url: str) -> tuple[str, str]:
    """Descarga una imagen y la convierte a base64.

    Args:
        url: URL de la imagen a descargar.

    Returns:
        Tupla (imagen_base64, content_type).
    """
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "image/jpeg")
    image_b64 = base64.standard_b64encode(response.content).decode("utf-8")
    return image_b64, content_type
