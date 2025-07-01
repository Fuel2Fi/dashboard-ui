import json
from datetime import datetime

def generate_consensus():
    timestamp = datetime.now(datetime.UTC).isoformat()
    consensus = {
        "timestamp": timestamp,
        "strategy": "consensus",
        "signals": []
    }
    return consensus

if __name__ == "__main__":
    print(json.dumps(generate_consensus(), indent=2))
