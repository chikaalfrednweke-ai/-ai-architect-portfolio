# ============================================
# Fred Baker's Automations
# report_agent.py — Sales Report Agent
# ============================================

import json
from datetime import datetime

# ---- LOAD DATA ----
def load_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []

# ---- REPORT GENERATOR ----
def generate_report(leads, sequences):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Stats
    total = len(leads)
    hot = len([l for l in leads if "HOT" in l["priority"]])
    warm = len([l for l in leads if "WARM" in l["priority"]])
    cold = len([l for l in leads if "COLD" in l["priority"]])
    
    lexai = len([l for l in leads if l["product"] == "LexAI"])
    estateiq = len([l for l in leads if l["product"] == "EstateIQ"])
    opsguard = len([l for l in leads if l["product"] == "OpsGuard"])

    report = []
    report.append("=" * 60)
    report.append("  FRED BAKER'S AUTOMATIONS")
    report.append("  AI Sales Intelligence Report")
    report.append(f"  Generated: {now}")
    report.append("=" * 60)

    report.append("\n  PIPELINE SUMMARY")
    report.append("-" * 60)
    report.append(f"  Total Leads      : {total}")
    report.append(f"  Hot Leads        : {hot} 🔥")
    report.append(f"  Warm Leads       : {warm} ⚡")
    report.append(f"  Cold Leads       : {cold} ❄️")

    report.append("\n  PRODUCT DISTRIBUTION")
    report.append("-" * 60)
    report.append(f"  LexAI            : {lexai} leads")
    report.append(f"  EstateIQ         : {estateiq} leads")
    report.append(f"  OpsGuard         : {opsguard} leads")

    report.append("\n  LEAD DETAILS")
    report.append("-" * 60)
    for i, lead in enumerate(leads, 1):
        report.append(f"\n  {i}. {lead['name']}")
        report.append(f"     Business  : {lead['business']}")
        report.append(f"     Product   : {lead['product']}")
        report.append(f"     Score     : {lead['score']}/10")
        report.append(f"     Priority  : {lead['priority']}")

    report.append("\n  WHATSAPP SEQUENCES STATUS")
    report.append("-" * 60)
    for seq in sequences:
        report.append(f"  {seq['first_name']} — 3 messages ready")

    report.append("\n  RECOMMENDED ACTIONS")
    report.append("-" * 60)
    hot_leads = [l for l in leads if "HOT" in l["priority"]]
    warm_leads = [l for l in leads if "WARM" in l["priority"]]
    cold_leads = [l for l in leads if "COLD" in l["priority"]]

    if hot_leads:
        report.append(f"\n  TODAY — Call these HOT leads immediately:")
        for l in hot_leads:
            report.append(f"    → {l['name']} | {l['product']}")

    if warm_leads:
        report.append(f"\n  THIS WEEK — Send WhatsApp to WARM leads:")
        for l in warm_leads:
            report.append(f"    → {l['name']} | {l['product']}")

    if cold_leads:
        report.append(f"\n  THIS MONTH — Nurture COLD leads:")
        for l in cold_leads:
            report.append(f"    → {l['name']} | {l['product']}")

    report.append("\n" + "=" * 60)
    report.append("  END OF REPORT")
    report.append("=" * 60)

    return "\n".join(report)

# ---- SAVE REPORT ----
def save_report(report_text):
    filename = f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\n  Report saved to: {filename}")
    return filename

# ---- MAIN PIPELINE ----
print("=" * 60)
print("  FRED BAKER'S AUTOMATIONS")
print("  Multi-Agent Pipeline Running...")
print("=" * 60)

print("\n  Step 1 — Loading lead data...")
leads = load_json("leads_processed.json")
print(f"  Loaded {len(leads)} leads")

print("\n  Step 2 — Loading WhatsApp sequences...")
sequences = load_json("whatsapp_sequences.json")
print(f"  Loaded {len(sequences)} sequences")

print("\n  Step 3 — Generating sales report...")
report = generate_report(leads, sequences)

print("\n  Step 4 — Saving report...")
filename = save_report(report)

print("\n  Step 5 — Printing report...")
print(report)