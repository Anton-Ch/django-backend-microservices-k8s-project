# Django + Flask Microservices + K8s 
## IBM Capstone Project
This showcase monorepo hosts a production backend stack:
1. **Django** main application (auth, pages, orchestration)    
2. **Flask** microservices:    
    - **Pictures** service (past-event pictures, health)        
    - **Songs** service (MongoDB-backed lyrics & songs)        
3. **Datastores**: SQLite (Django) + MongoDB (Songs)    
4. **Infrastructure**: Docker & docker-compose for local dev, Kubernetes manifests (infra/k8s) for cluster deployment    

> Built as the wrap up capstone project of the **IBM Back-End Development Professional Certificate** and extended for real-world portfolio needs.

## Architecture (high-level)
 ```mermaid
flowchart LR
    U["User (Browser)"] -->|HTTP| DJ["Django Main App"]
    DJ -->|REST| PICS["Flask Pictures Service"]
    PICS --> COS["Cloud Object Storage"]

    DJ -->|REST| SONGS["Flask Songs Service"]
    SONGS --> MDB[("MongoDB")]
```

## Planned Repository Folders Structure
```bash
django-backend-microservices-k8s-project/
├─ services/
│  ├─ pictures-flask/   # Flask 'Get Pictures' microservice
│  │  ├─ app/           # Flask app code
│  │  ├─ tests/
│  │  ├─ Dockerfile
│  │  └─ requirements.txt
│  ├─ songs-flask/     # Flask 'Get Songs' microservice (MongoDB)
│  │  ├─ app/
│  │  ├─ tests/
│  │  ├─ Dockerfile
│  │  └─ requirements.txt
│  └─ web-django/      # Django main application
│     ├─ app/
│     ├─ tests/
│     ├─ Dockerfile
│     └─ requirements.txt
├─ infra/
│  ├─ docker-compose.yml
│  ├─ k8s/          # Kubernetes manifests (deployments, services, ingress, etc.)
│  │  ├─ namespace.yaml
│  │  ├─ pictures-{deployment,service,ingress}.yaml
│  │  ├─ songs-{deployment,service,ingress}.yaml
│  │  ├─ web-{deployment,service,ingress}.yaml
│  │  ├─ secrets.yaml.example
│  │  └─ configmap.yaml
├─ scripts/
│  ├─ dev_bootstrap.ps1
│  ├─ dev_bootstrap.sh
│  └─ seed_songs.py
├─ .github/
│  ├─ workflows/ci.yml
│  └─ ISSUE_TEMPLATE.md
├─ Makefile
├─ README.md
└─ LICENSE 
```

## Local Development (quickstart)

### Prereqs

- Python 3.11+    
- Docker & docker-compose    
- Git    

### Start via docker-compose
```bash
# from repo root
docker compose -f infra/docker-compose.yml up -d --build

# expected endpoints (dev):
# Pictures: http://localhost:8001/health
# Songs:    http://localhost:8002/health
# Django:   http://localhost:8000/ 
```

### Running tests locally (example)
```bash
# pictures service
cd services/pictures-flask
pip install -r requirements.txt
pytest -q 
```

## Deployment
- **Containers:** each service has its own Dockerfile.    
- **Kubernetes:** manifests live in `infra/k8s/`.    
- Cloud targets (per capstone): IBM Code Engine (Pictures), OpenShift (Songs + MongoDB), IBM Kubernetes Service (Main App).    
- For non-IBM clusters (e.g., Linode/K8s), adapt Ingress, Secrets, and registry references.

## Branching & PR Workflow

- Feature branches per service/task (`feat/pictures-bootstrap`, `feat/songs-mongo`, `feat/web-django`, `docs/readme`, `ci/pytest`).    
- Open PRs early (Draft), keep diffs small, add screenshots/test evidence.    
- Conventional Commits for both commit messages and PR titles.    

## Conventional Commits (excerpt)

- `feat(scope): summary` — new feature    
- `fix(scope): summary` — bug fix    
- `refactor(scope): summary` — non-behavior code change    
- `docs(scope): summary` — docs only    
- `test(scope): summary` — add/update tests    
- `ci(scope): summary` — CI/CD changes    
- `build(scope): summary` — build/deps    
- `chore(scope): summary` — repo chores

## Roadmap (initial)
-  Pictures service: implement `/api/v1/pictures` and pass pytest    
-  Songs service: MongoDB CRUD + indices + tests    
-  Django: models, views, templates, integration to services    
-  CI: pytest + lint    
-  K8s manifests & cloud deployment docs

## License
MIT (see `LICENSE`).