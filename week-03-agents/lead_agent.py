# ============================================
# Fred Baker's Automations
# lead_agent.py — Lead Qualification Agent
# ============================================

import json
from datetime import datetime

# ---- LEAD DATABASE ----
leads = [
    {
        "name": "Barr. Emeka Obi",
        "first_name": "Emeka",
        "business": "Obi & Partners Legal",
        "industry": "law",
        "location": "Abuja",
        "employees": 35,
        "annual_revenue": 15000000,
        "pain_point": "Manual contract drafting takes too long",
        "contacted": False
    },
    {
        "name": "Alhaji Musa Dantata",
        "first_name": "Musa",
        "business": "Dantata Properties Ltd",
        "industry": "real estate",
        "location": "Abuja",
        "employees": 22,
        "annual_revenue": 25000000,
        "pain_point": "Difficulty tracking property listings and clients",
        "contacted": False
    },
    {
        "name": "Engr. Chukwudi Eze",
        "first_name": "Chukwudi",
        "business": "Eze Oil & Gas Ltd",
        "industry": "oil and gas",
        "location": "Abuja",
        "employees": 120,
        "annual_revenue": 80000000,
        "pain_point": "Pipeline maintenance scheduling is inefficient",
        "contacted": False
    },
    {
        "name": "Mrs. Aisha Bello",
        "first_name": "Aisha",
        "business": "Bello & Associates Law",
        "industry": "law",
        "location": "Abuja",
        "employees": 8,
        "annual_revenue": 3000000,
        "pain_point": "Court date management is chaotic",
        "contacted": False
    },
    {
        "name": "Mr. Tunde Fashola",
        "first_name": "Tunde",
        "business": "Fashola Homes",
        "industry": "real estate",
        "location": "Abuja",
        "employees": 5,
        "annual_revenue": 2000000,
        "pain_point": "No system to follow up with buyers",
        "contacted": False
    }
]

# ---- AGENT TOOLS ----
def score_lead(lead):
    score = 0
    if lead["annual_revenue"] >= 50000000: score += 5
    elif lead["annual_revenue"] >= 20000000: score += 4
    elif lead["annual_revenue"] >= 10000000: score += 3
    elif lead["annual_revenue"] >= 5000000: score += 2
    else: score += 1

    if lead["employees"] >= 100: score += 5
    elif lead["employees"] >= 50: score += 4
    elif lead["employees"] >= 20: score += 3
    elif lead["employees"] >= 10: score += 2
    else: score += 1

    return score

def get_priority(score):
    if score >= 8: return "🔥 HOT"
    elif score >= 5: return "⚡ WARM"
    else: return "❄️  COLD"

def recommend_product(industry):
    if "law" in industry or "legal" in industry:
        return "LexAI"
    elif "real estate" in industry or "property" in industry:
        return "EstateIQ"
    elif "oil" in industry or "gas" in industry or "energy" in industry:
        return "OpsGuard"
    else:
        return "Custom Solution"

def generate_outreach(lead, product, priority):
    return f"""
Hi {lead['first_name']},

I'm Chika Alfred from Fred Baker's Automations.

I noticed that {lead['business']} might be facing challenges with:
"{lead['pain_point']}"

We've built {product} specifically for {lead['industry']} businesses
in Abuja. It's already helping similar firms save 40% of their time.

Would you be open to a 15-minute WhatsApp call this week?

Best regards,
Chika Alfred
Fred Baker's Automations | Abuja
"""

# ---- MAIN AGENT ----
def run_lead_agent(leads):
    print("=" * 55)
    print("  FRED BAKER'S AUTOMATIONS")
    print("  Lead Qualification Agent — Running")
    print("=" * 55)

    results = []

    for lead in leads:
        score = score_lead(lead)
        priority = get_priority(score)
        product = recommend_product(lead["industry"])
        outreach = generate_outreach(lead, product, priority)

        result = {
            "name": lead["name"],
            "first_name": lead["first_name"],
            "business": lead["business"],
            "product": product,
            "score": score,
            "priority": priority,
            "outreach": outreach
        }
        results.append(result)

        print(f"\n  👤 {lead['first_name']} ({lead['name']})")
        print(f"  🏢 {lead['business']}")
        print(f"  📦 Product : {product}")
        print(f"  📊 Score   : {score}/10")
        print(f"  🎯 Priority: {priority}")
        print("-" * 55)

    results.sort(key=lambda x: x["score"], reverse=True)

    print("\n" + "=" * 55)
    print("  📋 PRIORITY OUTREACH ORDER:")
    print("=" * 55)
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r['priority']} | {r['first_name']} → {r['product']}")

    with open("leads_processed.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\n  💾 Results saved to leads_processed.json")

    top = results[0]
    print("\n" + "=" * 55)
    print(f"  📧 TOP LEAD OUTREACH MESSAGE:")
    print("=" * 55)
    print(top["outreach"])

    return results

# ---- RUN ----
run_lead_agent(leads)