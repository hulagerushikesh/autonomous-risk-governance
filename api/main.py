from fastapi import FastAPI

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

db_url = os.getenv("DATABASE_URL")
api_key = os.getenv("API_KEY")
debug_mode = os.getenv("DEBUG")


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Autonomous Risk Governance API is running!"}
