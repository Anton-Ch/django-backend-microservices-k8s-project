# Pictures Service (Flask)

Minimal Flask microservice that exposes:
- GET /health — liveness probe
- GET /api/v1/pictures[?date=YYYY-MM-DD] — returns past-event picture URLs (backed by cloud object storage in the course context)

Local Dev
```bash
pip install -r requirements.txt
pytest -q
FLASK_APP=app/main.py flask run -p 8001
# http://localhost:8001/health 
```

---

## RESTful API Endpoints (planned schema)

| Action | Method | Return code | Body                        | URL Endpoint     |
|--------|--------|-------------|-----------------------------|------------------|
| List   | GET    | 200 OK      | Array of picture URLs `[{...}]` | `GET /picture`     |
| Create | POST   | 201 CREATED | A picture resource as JSON `{...}` | `POST /picture`    |
| Read   | GET    | 200 OK      | A picture as JSON `{...}`   | `GET /picture/{id}` |
| Update | PUT    | 200 OK      | A picture as JSON `{...}`   | `PUT /picture/{id}` |
| Delete | DELETE | 204 NO CONTENT | `""`                      | `DELETE /picture/{id}` |

---


## Existing Endpoints (already implemented)

| Action | Method | Return code | Body | URL Endpoint |
|--------|--------|-------------|------|--------------|
| Health | GET    | 200 OK      | `""` | `GET /health` |
| Count  | GET    | 200 OK      | `""` | `GET /count`  |

---


## Configuration (env)

- `EXTERNAL_PICTURES_API_BASE` — optional upstream API/base    
- `PORT_PICTURES` — default 8001    
- `ENV` — dev/prod
  
## Tests

The previous developer wrote tests for the service. At the moment:
- Only `/health` and `/count` tests pass.
- Other tests fail until the CRUD endpoints are implemented.

Run only passing tests:
```bash
pytest -k 'test_health or test_count'
```

Run all tests (expected failures for unimplemented endpoints):
```bash
pytest
```