# Pictures Service (Flask)

Minimal Flask microservice that exposes:
- GET /health — liveness probe
- GET /api/v1/pictures[?date=YYYY-MM-DD] — returns past-event picture URLs (backed by cloud object storage in the course context)

Local Dev
```bash
pip install -r requirements.txt
pytest -q
FLASK_APP=app/main.py flask run -p 5000
# http://localhost:5000/health 
```

---

## RESTful API Endpoints

| Action | Method | Return code | Body                          | URL Endpoint        |
|--------|--------|-------------|-------------------------------|---------------------|
| Health | GET    | 200 OK      | `{"status": "OK"}`            | `/health`           |
| Count  | GET    | 200 OK      | `{"length": <int>}`           | `/count`            |
| List   | GET    | 200 OK      | Array of pictures `[{...}]`   | `/picture`          |
| Read   | GET    | 200 OK      | A picture as JSON `{...}`     | `/picture/<id>`     |
| Create | POST   | 201 CREATED | Created picture as JSON `{...}` | `/picture`        |
|        |        | 302 FOUND   | `{"Message": "... already present"}` | `/picture`  |
| Update | PUT    | 200 OK      | Updated picture as JSON `{...}` | `/picture/<id>`   |
|        |        | 404 NOT FOUND | `{"Message": "picture not"}` | `/picture/<id>`   |
| Delete | DELETE | 204 NO CONTENT | `""`                       | `/picture/<id>`     |
|        |        | 404 NOT FOUND | `{"Message": "picture not"}` | `/picture/<id>`     |


---


## Example Requests

### Health check
```bash
curl -s http://localhost:5000/health
# {"status": "OK"}
```

### Count
```bash
curl -s http://localhost:5000/count
# {"length": 10}
```

### List all pictures
```bash
curl -s http://localhost:5000/picture
```

### Get picture by ID
```bash
curl -s http://localhost:5000/picture/1
```

### Create picture

```bash
curl -X POST http://localhost:5000/picture \
  -H "Content-Type: application/json" \
  -d '{"id":200,"pic_url":"http://dummyimage.com/230x100.png/dddddd/000000","event_country":"United States","event_state":"California","event_city":"Fremont","event_date":"11/2/2030"}'
```

### Update picture
```bash
curl -X PUT http://localhost:5000/picture/200 \
  -H "Content-Type: application/json" \
  -d '{"id":200,"pic_url":"http://dummyimage.com/300x200.png/ff4444/ffffff","event_country":"United States","event_state":"California","event_city":"Fremont","event_date":"12/12/2031"}'
```

### Delete picture

```bash
curl -X DELETE http://localhost:5000/picture/200 -i
```


## Local Development
```bash
# From service folder
cd services/pictures-flask

# Install dependencies (using pipenv)
pipenv --python 3.9
pipenv install -r requirements.txt
pipenv install pytest

# Run tests
pipenv run pytest -q

# Run service
FLASK_APP=backend/routes.py pipenv run flask run -p 5000
# Visit http://localhost:5000/health
```


## Tests

All endpoints are covered by unit tests.

Run all tests:
```bash
pipenv run pytest -q
```

Expected passing tests:
- test_health
- test_count
- test_data_contains_10_pictures
- test_get_picture
- test_get_pictures_check_content_type_equals_json
- test_get_picture_by_id
- test_pictures_json_is_not_empty
- test_post_picture
- test_post_picture_duplicate
- test_update_picture_by_id
- test_delete_picture_by_id