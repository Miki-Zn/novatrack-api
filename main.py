from fastapi import FastAPI

app = FastAPI(
    title="NovaTrack API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}