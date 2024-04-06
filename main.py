from fastapi import FastAPI
from routes.events import events


app = FastAPI()

# Include routes
app.include_router(events)