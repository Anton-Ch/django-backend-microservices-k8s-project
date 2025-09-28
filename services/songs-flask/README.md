# Songs Service (Flask + MongoDB)

Flask microservice for songs and lyrics, backed by MongoDB.

---

## RESTful API Endpoints (planned schema)

| Action | Method  | Return code   | Body                          | URL Endpoint     |
|--------|---------|---------------|-------------------------------|------------------|
| Health | GET     | 200 OK        | `""`                          | `GET /health`    |
| Count  | GET     | 200 OK        | `""`                          | `GET /count`     |
| List   | GET     | 200 OK        | Array of songs `[{...}]`      | `GET /song`      |
| Create | POST    | 201 CREATED   | A song resource as JSON `{...}` | `POST /song`    |
| Read   | GET     | 200 OK / 404  | A song as JSON `{...}`        | `GET /song/{id}` |
| Update | PUT     | 200 OK / 404  | A song as JSON `{...}`        | `PUT /song/{id}` |
| Delete | DELETE  | 204 / 404     | `""`                          | `DELETE /song/{id}` |

---

## Local Development

### 1. Start MongoDB (via Docker Compose)
```bash
# from services/songs-flask
docker compose up -d mongodb
# optional UI
docker compose up -d mongo-express
```

- MongoDB will be available at `localhost:27017`.  
- Optional admin UI (Mongo Express) available at [http://localhost:8081](http://localhost:8081).  

Stop containers:
```bash
docker compose down
```

---

### 2. Run Flask app
```bash
cd services/songs-flask
pipenv install -r requirements.txt
pipenv shell
flask --app backend/routes.py run -p 8002
# http://localhost:8002/health
```

Run tests:
```bash
pytest -q
```

---

## Configuration (env)

Environment variables are stored in `.env` (not committed) and `.env.example` (committed).

### MongoDB (from `.env`)
- `MONGO_INITDB_ROOT_USERNAME` / `MONGO_INITDB_ROOT_PASSWORD` — root credentials for container bootstrap.  
- `MONGO_INITDB_DATABASE` — database to initialize (default: `app_db`).  
- `MONGO_APP_USERNAME` / `MONGO_APP_PASSWORD` — app-level user created by init script.  
- `MONGODB_PORT` — host port exposed for MongoDB (default: 27017).  
- `ME_UI_USER` / `ME_UI_PASS` — login for Mongo Express UI.

### Flask (from `services/songs-flask/.env`)
- `FLASK_ENV=development`  
- `MONGO_URI=mongodb://app_user:app_pass@localhost:27017/app_db?authSource=app_db`  
- `PORT_SONGS=8002`  

---

## Init Script

On first container start, the official `mongo:7` image executes all `.js` files from `/docker-entrypoint-initdb.d`.

We use:  
`infra/mongo/init/01-init.js` — creates the application user with `readWrite` role for `app_db`.

---

## Current Status
- MongoDB container working locally.  
- Flask service configured with Pipenv.  
- API endpoints are placeholders — to be implemented in upcoming steps.  