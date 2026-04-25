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
        print("❌ No leads file found! Run lead_agent.py first.")
        return []

# ---- MESSAGE TEMPLATES ----
def whatsapp_intro(lead):
    return f"""👋 Hello {lead['name'].split()[0]}!

I'm Chika from *Fred Baker's Automations* 🤖

I help {get_industry_label(lead['product'])} businesses in Abuja automate their operations using AI.

I believe *{lead['business']}* could benefit from our *{lead['product']}* solution.

Can I share a quick 60-second overview? 🙏"""

def whatsapp_followup(lead):
    return f"""Hello {lead['name'].split()[0]} 👋

Just following up on my previous message about *{lead['product']}*.

We're currently onboarding 3 pilot clients in Abuja at a *special founding rate* — and I immediately thought of *{lead['business']}*.

Would you have 15 minutes this week for a quick call? 📞

I can show you exactly how we've helped similar businesses save 40% of their operational time. 💡"""

def whatsapp_closing(lead):
    return f"""Hi {lead['name'].split()[0]},

Quick update — we only have *2 pilot spots* remaining for {lead['product']} this month.

Here's what you get as a founding client:
✅ 3 months free setup support
✅ Custom configuration for {lead['business']}
✅ Direct WhatsApp access to our team
✅ Special founding client pricing

Are you ready to move forward? 🚀

Just reply *YES* and I'll send over the details right away!"""

def get_industry_label(product):
    mapping = {
        "LexAI": "law firm",
        "EstateIQ": "real estate",
        "OpsGuard": "oil & gas"
    }
    return mapping.get(product, "business")

# ---- SEQUENCE GENERATOR ----
def generate_sequence(lead):
    print(f"\n{'=' * 55}")
    print(f"  📱 WHATSAPP SEQUENCE: {lead['name']}")
    print(f"  🎯 Priority: {lead['priority']}")
    print(f"  📦 Product : {lead['product']}")
    print(f"{'=' * 55}")
    
    print(f"\n  📤 MESSAGE 1 — Day 1 (Intro):")
    print(f"  {'-' * 50}")
    print(whatsapp_intro(lead))
    
    print(f"\n  📤 MESSAGE 2 — Day 3 (Follow Up):")
    print(f"  {'-' * 50}")
    print(whatsapp_followup(lead))
    
    print(f"\n  📤 MESSAGE 3 — Day 7 (Closing):")
    print(f"  {'-' * 50}")
    print(whatsapp_closing(lead))

# ---- SAVE SEQUENCES ----
def save_sequences(leads):
    sequences = []
    for lead in leads:
        sequences.append({
            "name": lead["name"],
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
    print(f"\n  💾 Saved {len(sequences)} WhatsApp sequences!")

# ---- MAIN ----
print("=" * 55)
print("  FRED BAKER'S AUTOMATIONS")
print("  WhatsApp Message Agent")
print("=" * 55)

leads = load_leads()

if leads:
    # Show sequence for TOP lead only
    top_lead = leads[0]
    generate_sequence(top_lead)
    
    # Save all sequences
    save_sequences(leads)
    
    print(f"\n{'=' * 55}")
    print(f"  ✅ WhatsApp sequences ready for all {len(leads)} leads!")
    print(f"  📁 Check whatsapp_sequences.json for full output")
    print(f"  🚀 Next: Connect to ManyChat for auto-sending!")
    print(f"{'=' * 55}")