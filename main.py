from datetime import datetime, timezone

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])


def error(status: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"status": "error", "message": message})


@app.get("/api/classify")
async def classify(request: Request):
    if "name" not in request.query_params:
        return error(400, "Missing 'name' query parameter")

    name = request.query_params["name"]

    if name.strip().lstrip("-").isdigit():
        return error(422, "'name' must be a string")

    if not name.strip():
        return error(400, "'name' cannot be empty")

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://api.genderize.io", params={"name": name.strip()})
    except httpx.RequestError:
        return error(502, "Failed to reach upstream API")

    if r.status_code >= 400:
        return error(502, f"Upstream API returned status {r.status_code}")

    data = r.json()
    gender = data.get("gender")
    sample_size = data.get("count")

    if gender is None or not sample_size:
        return error(404, "No prediction available for the provided name")

    probability = float(data.get("probability", 0))

    return {
        "status": "success",
        "data": {
            "name": data.get("name", name),
            "gender": gender,
            "probability": probability,
            "sample_size": sample_size,
            "is_confident": probability >= 0.7 and sample_size >= 100,
            "processed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
    }