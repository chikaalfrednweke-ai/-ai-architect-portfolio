# ============================================
# Fred Baker's Automations
# prompt_builder.py — AI Prompt Builder
# ============================================

# This is the bridge to Week 2 — Claude API

def build_lexai_prompt(client_name, issue):
    prompt = f"""You are LexAI, an AI legal assistant for Nigerian law firms.

Client: {client_name}
Issue: {issue}

Provide a brief, professional legal guidance note relevant to Nigerian law.
Keep it under 100 words."""
    return prompt

def build_estateiq_prompt(property_type, location, budget):
    prompt = f"""You are EstateIQ, an AI real estate assistant for the Nigerian market.

Property Type: {property_type}
Location: {location}
Budget: {budget}

Provide a brief property investment recommendation for this client.
Keep it under 100 words."""
    return prompt

def build_opsguard_prompt(company, operation, issue):
    prompt = f"""You are OpsGuard, an AI operations assistant for Nigerian oil and gas companies.

Company: {company}
Operation: {operation}
Issue: {issue}

Provide a brief operational risk assessment and recommendation.
Keep it under 100 words."""
    return prompt

# ---- TEST THE PROMPT BUILDER ----
print("=" * 50)
print("  FRED BAKER'S AUTOMATIONS")
print("  AI Prompt Builder — Week 1")
print("=" * 50)

# LexAI prompt
lexai = build_lexai_prompt(
    client_name="Obi & Partners Legal",
    issue="Contract dispute with a vendor over delivery timelines"
)
print("\n📜 LEXAI PROMPT:")
print("-" * 50)
print(lexai)

# EstateIQ prompt
estateiq = build_estateiq_prompt(
    property_type="Commercial Office Space",
    location="Maitama, Abuja",
    budget="₦50,000,000"
)
print("\n🏢 ESTATEIQ PROMPT:")
print("-" * 50)
print(estateiq)

# OpsGuard prompt
opsguard = build_opsguard_prompt(
    company="Eze Oil & Gas Ltd",
    operation="Pipeline inspection",
    issue="Delayed maintenance schedule due to weather"
)
print("\n⚙️ OPSGUARD PROMPT:")
print("-" * 50)
print(opsguard)

print("\n" + "=" * 50)
print("  ✅ Prompts ready — Week 2 we send these to Claude API!")
print("=" * 50)