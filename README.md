# JWT Implementation using Python (FastAPI)

Este repositorio incluye una aplicación Web API en Python/FastAPI dentro de la carpeta `backend` que implementa autenticación JWT.

## Estructura

```text
.
├── backend
│   ├── app
│   │   └── main.py
│   ├── Dockerfile
│   └── pyproject.toml
└── docker-compose.yml
```

## Requisitos funcionales implementados

- Endpoint `POST /token` para autenticación con:
  - `username`: `admin`
  - `password`: `admin123`
- Generación de token JWT con expiración de **300 segundos**.
- Endpoint `POST /token/refresh` para refrescar el token usando un `refresh_token`.

## Endpoints

### 1) Obtener token

`POST /token`

Body:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Respuesta esperada:

```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

### 2) Refrescar token

`POST /token/refresh`

Body:

```json
{
  "refresh_token": "<jwt>"
}
```

Respuesta esperada:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

## Gestión de dependencias con Poetry

El backend usa Poetry (`backend/pyproject.toml`) para gestionar dependencias:

- fastapi
- uvicorn
- pyjwt

## Variables de entorno requeridas

- `APP_ADMIN_USERNAME` (ejemplo: `admin`)
- `APP_ADMIN_PASSWORD` (ejemplo: `admin123`)
- `JWT_SECRET_KEY` (clave secreta para firmar/validar JWT)

> Si falta cualquiera de estas variables, la aplicación falla al iniciar.

Puedes usar `.env.example` como base:

```bash
cp .env.example .env
```

## Ejecución con Docker Compose

Desde la raíz del proyecto:

```bash
cp .env.example .env
docker compose up --build
```

La API quedará disponible en:

`http://localhost:8000`

Documentación automática:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`