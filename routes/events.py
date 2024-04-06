from fastapi import APIRouter, Response, HTTPException #, status
from datetime import datetime

from models.events import (
    EventBase, 
    PurchaseEvent, 
    EmailClickEvent, 
    EmailOpenEvent, 
    EmailUnsubscribeEvent,
    EventResponse
    )

from starlette.status import HTTP_204_NO_CONTENT
from typing import List
import json

output_path = "validated_events.jsonl"

events = APIRouter()



@events.post('/events',response_model=EventResponse, tags=["Events"])
async def receive_event(event_data: dict):
    
    timestamp_date = event_data['timestamp'].split("T")[0]
    timestamp_time = event_data['timestamp'].split("T")[1]
    
    # if year not first then swap year for day
    if len(timestamp_date.split("-")[0]) == 2:
        parts = timestamp_date.split("-")
        timestamp_date = parts[2] + "-" + parts[1] + "-" + parts[0]
        event_data['timestamp'] = timestamp_date + "T" + timestamp_time

    event_type = event_data.get("event_type")
    if event_type == "email_click":
        model = EmailClickEvent
    elif event_type == "purchase":
        model = PurchaseEvent
    elif event_type == "email_open":
        model = EmailOpenEvent
    elif event_type == "email_unsubscribe":
        model = EmailUnsubscribeEvent
    else:
        raise ValueError("Unknown event type")

    validated_event = model(**event_data)

    validated_event.timestamp = str(validated_event.timestamp)
    
    if isinstance(validated_event, EmailClickEvent):
        validated_event.clicked_link = str(validated_event.clicked_link)
    
    with open(output_path, "a") as f:
        f.write(json.dumps(dict(validated_event)) + "\n")
    return event_data 

