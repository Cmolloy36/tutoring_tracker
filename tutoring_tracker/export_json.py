import json
import sqlalchemy as sa
from sqlalchemy.ext.declarative import DeclarativeMeta

def serialize_model(model):
    return {
        key: value
        for key, value in model.__dict__.items()
        if not key.startswith('_')  # Exclude SQLAlchemy internals
    }