import requests
import json

def pull_model(model_name):
    url = "http://localhost:11434/api/pull"
    payload = {"name": model_name}
    
    print(f"Pulling model {model_name} via API...")
    try:
        response = requests.post(url, json=payload, stream=True)
        for line in response.iter_lines():
            if line:
                status = json.loads(line)
                if 'status' in status:
                    print(f"Status: {status['status']}", end='\r')
                if 'completed' in status and 'total' in status:
                    pct = (status['completed'] / status['total']) * 100
                    print(f"Status: {status['status']} ({pct:.2f}%)", end='\r')
        print(f"\nSuccessfully pulled {model_name}")
    except Exception as e:
        print(f"\nError pulling model: {e}")

if __name__ == "__main__":
    pull_model("llama3.2:1b")
