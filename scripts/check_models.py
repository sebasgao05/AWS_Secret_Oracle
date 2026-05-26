"""Script para validar credenciales y modelos disponibles en Bedrock."""
import os
import boto3
import json
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

print(f"Region: {AWS_REGION}")
print(f"Access Key: {AWS_ACCESS_KEY_ID[:8]}...")
print(f"Session Token: {'SI' if AWS_SESSION_TOKEN else 'NO'}")
print()

kwargs = {
    "region_name": AWS_REGION,
    "aws_access_key_id": AWS_ACCESS_KEY_ID,
    "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
}
if AWS_SESSION_TOKEN:
    kwargs["aws_session_token"] = AWS_SESSION_TOKEN

# Test 1: Verificar identidad
print("=== Test 1: Verificando identidad AWS ===")
try:
    sts = boto3.client("sts", **kwargs)
    identity = sts.get_caller_identity()
    print(f"Account: {identity['Account']}")
    print(f"ARN: {identity['Arn']}")
    print("OK - Credenciales validas")
except Exception as e:
    print(f"ERROR: {e}")

print()

# Test 2: Listar modelos disponibles en Bedrock
print("=== Test 2: Modelos disponibles en Bedrock ===")
try:
    bedrock = boto3.client("bedrock", **kwargs)
    response = bedrock.list_foundation_models(byProvider="Anthropic")
    models = response.get("modelSummaries", [])
    print(f"Modelos Anthropic encontrados: {len(models)}")
    for m in models:
        print(f"  - {m['modelId']} ({m.get('modelLifecycle', {}).get('status', 'unknown')})")
except Exception as e:
    print(f"ERROR listando modelos: {e}")

print()

# Test 3: Probar invocacion con el modelo configurado
print(f"=== Test 3: Probando modelo '{os.getenv('BEDROCK_MODEL_ID')}' ===")
try:
    runtime = boto3.client("bedrock-runtime", **kwargs)
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 10,
        "messages": [{"role": "user", "content": "Hola"}],
    })
    response = runtime.invoke_model(
        modelId=os.getenv("BEDROCK_MODEL_ID"),
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    result = json.loads(response["body"].read())
    print(f"OK - Respuesta: {result['content'][0]['text']}")
except Exception as e:
    print(f"ERROR: {e}")
