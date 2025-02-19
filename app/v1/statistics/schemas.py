from pydantic import BaseModel


class Stats(BaseModel):
    avg: float
    max: float
    min: float
    count: int

    model_config = {
        "json_schema_extra": {
            "examples": [{"avg": 100.0, "max": 200.0, "min": 50.0, "count": 10}]
        }
    }
