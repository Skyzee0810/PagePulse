from fastapi import FastAPI

app = FastAPI(title="Page Pulse")


@app.get("/")
def health_check():
    return {"message": "Page Pulse is running"}