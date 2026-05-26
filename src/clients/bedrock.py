"""Cliente de Amazon Bedrock (Claude) para generación de texto con visión."""

import json

import boto3

from src.config import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN,
    BEDROCK_MODEL_ID,
)


def get_client():
    """Crea y retorna un cliente de Bedrock Runtime."""
    kwargs = {
        "region_name": AWS_REGION,
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
    }
    if AWS_SESSION_TOKEN:
        kwargs["aws_session_token"] = AWS_SESSION_TOKEN
    return boto3.client("bedrock-runtime", **kwargs)


def invoke_with_image(image_base64: str, media_type: str, prompt: str, max_tokens: int = 150) -> str:
    """Invoca Claude con una imagen y un prompt de texto.

    Args:
        image_base64: Imagen codificada en base64.
        media_type: Tipo MIME de la imagen (e.g. image/jpeg).
        prompt: Texto del prompt.
        max_tokens: Máximo de tokens en la respuesta.

    Returns:
        Texto de la respuesta del modelo.
    """
    client = get_client()

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
    })

    response = client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"].strip()
