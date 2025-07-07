import json

def main():
    with open("config.json") as f:
        config = json.load(f)

    print("✅ Loaded Config:")
    for k, v in config.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
