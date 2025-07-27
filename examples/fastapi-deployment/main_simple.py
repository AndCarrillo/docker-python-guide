from fastapi import FastAPI

app = FastAPI(title="FastAPI Docker Example")

users = []


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI in Docker!", "users_count": len(users)}
