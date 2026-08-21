# Frontend — Aplicación React

Aplicación web construida con **React + Vite** que implementa autenticación contra el backend FastAPI mediante JWT.

## Estructura

```text
frontend/
├── src/
│   ├── pages/
│   │   ├── LoginPage.jsx        # Página de inicio de sesión
│   │   ├── LoginPage.module.css
│   │   ├── WelcomePage.jsx      # Página de bienvenida (protegida)
│   │   └── WelcomePage.module.css
│   ├── App.jsx                  # Lógica de enrutado (sin router externo)
│   ├── index.css                # Variables de diseño (PlayStation Design System)
│   └── main.jsx                 # Punto de entrada React
├── index.html
├── vite.config.js
├── .env.example
└── README.md
```

## Requisitos previos

- Node.js ≥ 18
- Backend corriendo en `http://localhost:8000` (ver `../backend/`)

## Instalación

```bash
cd frontend
npm install
```

## Configuración

Copia el archivo de ejemplo y ajusta la URL del backend si es necesario:

```bash
cp .env.example .env
```

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `VITE_API_BASE_URL` | URL base del backend | `http://localhost:8000` |

## Ejecución en desarrollo

```bash
npm run dev
```

La aplicación estará disponible en: **http://localhost:5173**

## Build de producción

```bash
npm run build
# Los archivos quedan en dist/
```

## Uso

### Inicio de sesión

1. Abre **http://localhost:5173** en el navegador.
2. Ingresa las credenciales del backend (por defecto `admin` / `admin123`).
3. Al autenticarse correctamente, el token JWT se guarda en `sessionStorage` y eres redirigido a la página de bienvenida.

### Página de bienvenida

- Sólo es accesible si hay un token activo en `sessionStorage`.
- Si navegas directamente sin sesión activa, serás redirigido a la página de login.
- Usa el botón **Cerrar sesión** para eliminar el token y volver a la pantalla de login.

## Diseño

La interfaz sigue el **PlayStation Design System** definido en `DESIGN 1` (raíz del proyecto):

- Paleta de colores: fondo oscuro (`#000000`), acento primario azul PlayStation (`#0070d1`).
- Tipografía: weight 300 para headings, 400/500 para body y botones.
- Botón CTA: píldora completamente redondeada (`border-radius: 9999px`).
- Cards con `border-radius: 8px`.
