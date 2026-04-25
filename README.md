# Pulse App

Simple pulse calculator app with:
- `backend`: FastAPI service with PostgreSQL persistence.
- `frontend`: static page served by Nginx.
- `k8s-helm`: Helm chart to deploy app and database.

## Local run (without Docker)

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Environment variables:
- `DB_HOST` (default: `localhost`)
- `DB_NAME` (default: `postgres`)
- `DB_USER` (default: `postgres`)
- `DB_PASSWORD` (default: `password`)
- `SKIP_DB_INIT` (set `true` for local smoke tests without DB)

### 2) Frontend

Open `frontend/index.html` in browser or run through any static server.

## Tests

Run backend smoke tests:

```bash
SKIP_DB_INIT=true PYTHONPATH=backend pytest backend/tests -q
```

## Kubernetes / Helm

Before installing chart, create DB password secret:

```bash
kubectl create secret generic pulse-db-secret \
  --from-literal=password='<your-db-password>'
```

Create Grafana admin password secret:

```bash
kubectl create secret generic grafana-admin-secret \
  --from-literal=password='<your-grafana-admin-password>'
```

Then deploy chart from `k8s-helm`.

HPA modes:
- `autoscaling.mode: custom` (default): scales by RPS via Prometheus Adapter (installed by chart).
- `autoscaling.mode: resource`: scales by CPU/Memory, requires `metrics-server` in cluster.

## CI

Pipeline in `.github/workflows/ci.yml` includes:
- lint (`ruff`)
- backend smoke tests (`pytest`)
- secrets scan (`gitleaks`)
- dependency scan (`snyk`)
- Docker build/push on `push` to `main`
- image scan (`trivy`) on pushed images
