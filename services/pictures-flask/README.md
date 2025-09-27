# Pictures Service (Flask)

Minimal Flask microservice that exposes:
- GET /health — liveness probe
- GET /api/v1/pictures[?date=YYYY-MM-DD] — returns past-event picture URLs (backed by cloud object storage in the course context)

Local Dev
```bash
pip install -r requirements.txt
pytest -q
FLASK_APP=app/main.py flask run -p 8001
# http://localhost:8001/health ```

## Configuration (env)

- `EXTERNAL_PICTURES_API_BASE` — optional upstream API/base    
- `PORT_PICTURES` — default 8001    
- `ENV` — dev/prod
  
## Tests
- `pytest` under `tests/` covers health and basic endpoint behavior.