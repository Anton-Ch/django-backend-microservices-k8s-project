# Songs Service (Flask + MongoDB)

Flask microservice for songs and lyrics, backed by MongoDB.

## Endpoints (planned)
- `GET /health`    
- CRUD for `song` resource (TBD)    
- Query popular lyrics (TBD)

## Local Dev
```bash
# ensure MongoDB is running (docker-compose or local)
pip install -r requirements.txt
pytest -q
FLASK_APP=app/main.py flask run -p 8002
# http://localhost:8002/health ```

## Configuration (env)

- `MONGO_URL` — e.g., `mongodb://localhost:27017`    
- `MONGO_DB` — e.g., `songsdb`    
- `PORT_SONGS` — default 8002