from pydantic import BaseModel


class Ticks(BaseModel):
    instrument: str
    price: float
    timestamp: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"instrument": "IBM.N", "price": 143.82, "timestamp": 1478192204000}
            ]
        }
    }
