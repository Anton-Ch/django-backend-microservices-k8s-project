# Songs Service (Flask + MongoDB)

Flask microservice for songs and lyrics, backed by MongoDB.  
Implements full CRUD on the `songs` collection and system endpoints for health and document count.

---

## RESTful API Endpoints (planned schema)

| Action | Method  | Return code        | Body                            | URL Endpoint        |
|-------:|---------|--------------------|---------------------------------|---------------------|
| Health | GET     | 200 OK             | `{"status":"OK"}`               | `GET /health`       |
| Count  | GET     | 200 OK             | `{"count": <int>}`              | `GET /count`        |
| List   | GET     | 200 OK             | Array of songs `[{...}]`        | `GET /song`         |
| Read   | GET     | 200 OK / 404       | A song as JSON `{...}`          | `GET /song/{id}`    |
| Create | POST    | 201 CREATED / 302  | Created song as JSON `{...}`    | `POST /song`        |
| Update | PUT     | 201 / 200 / 404    | Updated song as JSON `{...}`    | `PUT /song/{id}`    |
| Delete | DELETE  | 204 NO CONTENT/404 | `""`                            | `DELETE /song/{id}` |

**Notes**
- `302` on `POST` means a song with the given `id` already exists.
- `PUT` returns:
  - `201` if modified and returns the updated document;
  - `200` with `{"message":"song found, but nothing updated"}` if no changes;
  - `404` if target song not found.

---

## Local Development

### 1. Start MongoDB (via Docker Compose)
```bash
# from services/songs-flask
docker compose up -d mongodb
# optional UI
docker compose up -d mongo-express
```
Check:

```bash
docker compose ps
docker logs -f local-mongodb
```

- MongoDB will be available at `localhost:27017`.  
- Optional admin UI (Mongo Express) available at [http://localhost:8081](http://localhost:8081).  

Stop containers:
```bash
docker compose down
# or wipe data to re-bootstrap init scripts:
docker compose down -v
```

---

### 2. Run Flask app
```bash
cd services/songs-flask
pipenv install -r requirements.txt
# (optional) pin modern CLI support
pipenv install "Flask==2.3.3" "Werkzeug==2.3.8"
# run
pipenv run flask --app backend/routes.py run -p 8002 --reload
# http://localhost:8002/health
```

Run tests:
```bash
pytest -q
```

---

## Configuration (env)

Environment variables are stored in .env (not committed) and .env.example (committed).
python-dotenv used to load .env into the Flask process only (not system-wide).

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

### Build blocks for MONGO_URI
- MONGODB_HOST=localhost
- MONGO_DB=app_db
- MONGO_AUTH_SOURCE=${MONGO_DB}   # use "admin" if connecting as root

### Final connection string used by Flask (override or keep generated)
- MONGO_URI=mongodb://${MONGO_APP_USERNAME}:${MONGO_APP_PASSWORD}@${MONGODB_HOST}:${MONGODB_PORT}/${MONGO_DB}?authSource=${MONGO_AUTH_SOURCE}

---

## Init Script

On first container start, the official `mongo:7` image executes all `.js` files from `/docker-entrypoint-initdb.d`.

Used:  
`infra/mongo/init/01-init.js` — creates the application user with `readWrite` role for `app_db`.

---

## Example Requests

### Health & Count

```bash
curl.exe -s http://localhost:8002/health
# {"status":"OK"}

curl.exe -s http://localhost:8002/count
# {"count": 20}
```

### List & Read

```bash
curl.exe -s http://localhost:8002/song
curl.exe -s http://localhost:8002/song/1
```

### Create

```bash
curl.exe -s -X POST http://localhost:8002/song \
  -H "Content-Type: application/json" \
  -d '{"id":323,"title":"in faucibus orci luctus et ultrices","lyrics":"..."}'
# 201 on success; 302 if duplicate id
```

### Update

```bash
curl.exe -s -X PUT http://localhost:8002/song/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"yay song","lyrics":"yay hey yay yay"}'
# 201 updated doc / 200 no changes / 404 not found
```

### Delete

```bash
curl.exe -s -X DELETE http://localhost:8002/song/14
# 204 on success / 404 if not found
```

## Current Status

- ✅ MongoDB container works locally; app user is provisioned via init script.
- ✅ Flask service configured via Pipenv and python-dotenv.
- ✅ Implemented endpoints: /health, /count, GET /song, GET /song/<id>, POST /song, PUT /song/<id>, DELETE /song/<id>.
- ✅ README documents how to run, configure, and call the API.