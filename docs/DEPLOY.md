# 🚀 Despliegue - El Oráculo Visual (ECS Express Mode)

## Prerrequisitos

- Cuenta AWS con permisos para ECS, ECR y Bedrock
- AWS CLI configurado (`aws configure`)
- Docker instalado y corriendo
- Acceso habilitado al modelo `anthropic.claude-3-5-haiku-20241022-v1:0` en Amazon Bedrock (región us-east-1)

---

## Paso 1: Configurar variables de entorno

Copia el archivo de ejemplo y llena tus credenciales:

```bash
cp .env.example .env
```

Edita `.env` con tus valores reales:

```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
IMAGE_API_URL=https://qqgfg03g58.execute-api.us-east-1.amazonaws.com/prod/random-image
BEDROCK_MODEL_ID=anthropic.claude-3-5-haiku-20241022-v1:0
NVIDIA_API_KEY=nvapi-...
NVIDIA_MODEL_ID=google/gemma-3n-e4b-it
```

---

## Paso 2: Probar localmente con Docker

```bash
docker build -t oraculo-visual .
docker run -p 8501:8501 --env-file .env oraculo-visual
```

Abre `http://localhost:8501` para verificar que funciona.

---

## Paso 3: Crear repositorio en ECR

```bash
aws ecr create-repository --repository-name oraculo-visual --region us-east-1
```

---

## Paso 4: Push de la imagen a ECR

```bash
# Login en ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <TU_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Tag y push
docker tag oraculo-visual:latest <TU_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/oraculo-visual:latest
docker push <TU_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/oraculo-visual:latest
```

> Reemplaza `<TU_ACCOUNT_ID>` con tu ID de cuenta AWS (12 dígitos).

---

## Paso 5: Desplegar con ECS Express Mode (Consola AWS)

ECS Express Mode simplifica el despliegue sin necesidad de configurar clusters, task definitions ni load balancers manualmente.

### Desde la consola AWS:

1. Ve a **Amazon ECS** en la consola de AWS.
2. Haz clic en **"Get Started"** o **"Deploy"** (Express Mode).
3. Selecciona **"Deploy from ECR image"**.
4. Ingresa la URI de tu imagen:
   ```
   <TU_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/oraculo-visual:latest
   ```
5. Configura:
   - **Puerto**: `8501`
   - **CPU**: 0.5 vCPU
   - **Memoria**: 1 GB
   - **Variables de entorno**: Agrega cada variable de tu `.env`
6. Haz clic en **"Deploy"**.

ECS Express Mode creará automáticamente:
- Un cluster de Fargate
- Una task definition
- Un servicio con IP pública

### Obtener la URL:

Una vez desplegado, ve a la sección **"Tasks"** del servicio, haz clic en la tarea activa y copia la **Public IP**. Tu app estará en:

```
http://<PUBLIC_IP>:8501
```

---

## Paso alternativo: Deploy con AWS CLI (Copilot)

Si prefieres CLI, puedes usar AWS Copilot:

```bash
# Instalar Copilot CLI
curl -Lo copilot https://github.com/aws/copilot-cli/releases/latest/download/copilot-linux && chmod +x copilot && sudo mv copilot /usr/local/bin/

# Inicializar
copilot init --app oraculo --name web --type "Request-Driven Web Service" --dockerfile ./Dockerfile --port 8501 --deploy

# Agregar variables de entorno
copilot secret init --name AWS_ACCESS_KEY_ID
copilot secret init --name AWS_SECRET_ACCESS_KEY
```

---

## Notas importantes

- **Bedrock Access**: Asegúrate de habilitar el modelo Claude 3.5 Haiku en la consola de Bedrock (Model Access → Request Access).
- **Seguridad**: En producción, usa IAM Roles en lugar de access keys. Asigna un Task Role con permisos `bedrock:InvokeModel`.
- **Costos**: ECS Fargate cobra por vCPU y memoria por segundo de uso. Con 0.5 vCPU y 1GB es económico.
