import json
from datetime import datetime

def generate_engine_output():
    timestamp = datetime.now(datetime.UTC).isoformat()
    return {
        "timestamp": timestamp,
        "engine": "strategy_engine",
        "status": "ok"
    }

if __name__ == "__main__":
    print(json.dumps(generate_engine_output(), indent=2))
