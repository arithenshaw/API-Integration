# Genderize Classifier API

FastAPI endpoint that classifies a name via the [Genderize.io](https://genderize.io) API.

## Endpoint

`GET /api/classify?name={name}`

**Success (200):**
```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-16T12:00:00Z"
  }
}
```

**Errors:** `{ "status": "error", "message": "..." }`

- `400` — name missing or empty
- `422` — name is not a string
- `404` — no prediction available
- `502` — upstream failure

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Deploy to Railway

1. Push to GitHub.
2. Railway → New Project → Deploy from GitHub repo.
3. Generate a domain under Settings → Networking.