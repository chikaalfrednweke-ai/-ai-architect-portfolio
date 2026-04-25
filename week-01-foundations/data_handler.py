 # ============================================
# Fred Baker's Automations
# data_handler.py — Reading & Writing JSON
# ============================================

import json
import os

# Our client data
clients = [
    {
        "name": "Emeka Obi",
        "business": "Obi & Partners Legal",
        "location": "Abuja",
        "product": "LexAI",
        "status": "prospect"
    },
    {
        "name": "Fatima Aliyu",
        "business": "Aliyu Real Estate",
        "location": "Abuja",
        "product": "EstateIQ",
        "status": "active"
    },
    {
        "name": "Chukwudi Eze",
        "business": "Eze Oil & Gas Ltd",
        "location": "Abuja",
        "product": "OpsGuard",
        "status": "cold"
    }
]

# ---- WRITE to a JSON file ----
def save_clients(data, filename="clients.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Saved {len(data)} clients to {filename}")

# ---- READ from a JSON file ----
def load_clients(filename="clients.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        print(f"📂 Loaded {len(data)} clients from {filename}")
        return data
    else:
        print("❌ No client file found!")
        return []

# ---- RUN IT ----
# Save clients to file
save_clients(clients)

# Load them back
loaded = load_clients()

# Print loaded data
print("\n  CLIENTS FROM FILE:")
print("=" * 45)
for client in loaded:
    print(f"  → {client['name']} | {client['product']} | {client['status'].upper()}")
print("=" * 45)