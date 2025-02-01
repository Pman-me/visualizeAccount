from fastapi import FastAPI
from src.app.routes import address_activities

app = FastAPI()

app.include_router(prefix='/address', router=address_activities.router)
