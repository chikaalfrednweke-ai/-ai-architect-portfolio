# ============================================
# Fred Baker's Automations
# whatsapp_agent.py — WhatsApp Message Agent
# ============================================

import json
from datetime import datetime

# ---- LOAD PROCESSED LEADS ----
def load_leads(filename="leads_processed.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("No leads file found! Run lead_agent.py first.")
        return []

# ---- HELPER ----
def get_first_name(lead):
    return lead.get("first_name", lead["name"].split()[-1])

def get_industry_label(product):
    mapping = {
        "LexAI": "law firm",
        "EstateIQ": "real estate",
        "OpsGuard": "oil & gas"
    }
    return mapping.get(product, "business")

# ---- MESSAGE TEMPLATES ----
def whatsapp_intro(lead):
    name = get_first_name(lead)
    product = lead["product"]
    business = lead["business"]
    industry = get_industry_label(product)
    return (
        f"Hi {name},\n\n"
        f"I'm Chika from *Fred Baker's Automations*\n\n"
        f"I help {industry} businesses in Abuja automate their operations using AI.\n\n"
        f"I believe *{business}* could benefit from our *{product}* solution.\n\n"
        f"Can I share a quick 60-second overview?"
    )

def whatsapp_followup(lead):
    name = get_first_name(lead)
    product = lead["product"]
    business = lead["business"]
    return (
        f"Hello {name},\n\n"
        f"Just following up on my previous message about *{product}*.\n\n"
        f"We're currently onboarding 3 pilot clients in Abuja at a "
        f"*special founding rate* and I immediately thought of *{business}*.\n\n"
        f"Would you have 15 minutes this week for a quick call?\n\n"
        f"I can show you exactly how we've helped similar businesses "
        f"save 40% of their operational time."
    )

def whatsapp_closing(lead):
    name = get_first_name(lead)
    product = lead["product"]
    business = lead["business"]
    return (
        f"Hi {name},\n\n"
        f"Quick update — we only have *2 pilot spots* remaining "
        f"for {product} this month.\n\n"
        f"Here's what you get as a founding client:\n"
        f"- 3 months free setup support\n"
        f"- Custom configuration for {business}\n"
        f"- Direct WhatsApp access to our team\n"
        f"- Special founding client pricing\n\n"
        f"Are you ready to move forward?\n\n"
        f"Just reply *YES* and I'll send the details right away."
    )

# ---- SEQUENCE GENERATOR ----
def generate_sequence(lead):
    name = get_first_name(lead)
    print(f"\n{'=' * 55}")
    print(f"  WHATSAPP SEQUENCE: {name}")
    print(f"  Priority : {lead['priority']}")
    print(f"  Product  : {lead['product']}")
    print(f"{'=' * 55}")

    print(f"\n  MESSAGE 1 — Day 1 (Intro):")
    print(f"  {'-' * 50}")
    print(whatsapp_intro(lead))

    print(f"\n  MESSAGE 2 — Day 3 (Follow Up):")
    print(f"  {'-' * 50}")
    print(whatsapp_followup(lead))

    print(f"\n  MESSAGE 3 — Day 7 (Closing):")
    print(f"  {'-' * 50}")
    print(whatsapp_closing(lead))

# ---- SAVE SEQUENCES ----
def save_sequences(leads):
    sequences = []
    for lead in leads:
        sequences.append({
            "name": lead["name"],
            "first_name": get_first_name(lead),
            "business": lead["business"],
            "product": lead["product"],
            "priority": lead["priority"],
            "messages": {
                "day_1": whatsapp_intro(lead),
                "day_3": whatsapp_followup(lead),
                "day_7": whatsapp_closing(lead)
            },
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    with open("whatsapp_sequences.json", "w") as f:
        json.dump(sequences, f, indent=4)
    print(f"\n  Saved {len(sequences)} WhatsApp sequences!")

# ---- MAIN ----
print("=" * 55)
print("  FRED BAKER'S AUTOMATIONS")
print("  WhatsApp Message Agent")
print("=" * 55)

leads = load_leads()

if leads:
    top_lead = leads[0]
    generate_sequence(top_lead)
    save_sequences(leads)

    print(f"\n{'=' * 55}")
    print(f"  WhatsApp sequences ready for all {len(leads)} leads!")
    print(f"  Check whatsapp_sequences.json for full output")
    print(f"  Next: Connect to ManyChat for auto-sending!")
    print(f"{'=' * 55}")