# ============================================
# Fred Baker's Automations
# clients.py — Functions & Dictionaries
# ============================================

# Dictionary — like a client record
client = {
    "name": "Adaeze Okonkwo",
    "business": "Okonkwo & Associates Law Firm",
    "location": "Abuja, Nigeria",
    "product": "LexAI",
    "status": "prospect"
}

# Function — reusable block of code
def print_client_profile(client):
    print("=" * 45)
    print(f"  CLIENT PROFILE")
    print("=" * 45)
    print(f"  Name     : {client['name']}")
    print(f"  Business : {client['business']}")
    print(f"  Location : {client['location']}")
    print(f"  Product  : {client['product']}")
    print(f"  Status   : {client['status'].upper()}")
    print("=" * 45)

def qualify_lead(client):
    if client["status"] == "prospect":
        print(f"  🎯 {client['name']} is a hot lead for {client['product']}!")
    elif client["status"] == "active":
        print(f"  ✅ {client['name']} is an active client!")
    else:
        print(f"  ❄️  {client['name']} needs follow up.")

# Run the functions
print_client_profile(client)
qualify_lead(client)

# Multiple clients — list of dictionaries
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

# Loop through all clients
print("\n  ALL CLIENTS REPORT")
print("=" * 45)
for c in clients:
    print_client_profile(c)
    qualify_lead(c)
    print()