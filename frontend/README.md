# Frontend Vue.js

Frontend pentru API-ul de evenimente, implementat cu:

- Vue 3
- Vue Router
- Pinia
- Axios

## Setup

```sh
npm install
```

## Config

Copiezi fisierul de env:

```sh
cp .env.example .env
```

`VITE_API_BASE_URL` trebuie sa pointeze catre backend (implicit: `http://127.0.0.1:8000/api/v1`).
`VITE_GOOGLE_CLIENT_ID` trebuie setat cu OAuth Client ID din Google Cloud.

## Autentificare Google pentru studenti

- Frontend trimite `id_token` la endpoint-ul backend `POST /auth/google`.
- Backend accepta doar emailuri din subdomeniul `@student.usv.ro`.
- Acest login este folosit pentru functionalitati critice student (ex: trimiterea feedback-ului).

## Ruleaza in dezvoltare

```sh
npm run dev
```

## Build productie

```sh
npm run build
```
