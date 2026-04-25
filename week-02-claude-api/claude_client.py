# ============================================
# Fred Baker's Automations
# claude_client.py — Claude API Integration
# ============================================

import anthropic

# ---- CONFIGURATION ----
API_KEY = "your-api-key-here"

client = anthropic.Anthropic(api_key=API_KEY)

def ask_claude(system_prompt, user_message):
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    return message.content[0].text

def lexai_query(client_name, issue):
    system = """You are LexAI, an AI legal assistant for Nigerian law firms.
You provide professional legal guidance relevant to Nigerian law.
Be concise, professional and practical."""
    return ask_claude(system, f"Client: {client_name}\nIssue: {issue}")

def estateiq_query(property_type, location, budget):
    system = """You are EstateIQ, an AI real estate assistant for the Nigerian property market.
You provide investment recommendations based on current Nigerian market conditions.
Be concise and data-driven."""
    return ask_claude(system, f"Property: {property_type}\nLocation: {location}\nBudget: {budget}")

def opsguard_query(company, operation, issue):
    system = """You are OpsGuard, an AI operations assistant for Nigerian oil and gas companies.
You provide operational risk assessments and recommendations.
Be precise and safety-focused."""
    return ask_claude(system, f"Company: {company}\nOperation: {operation}\nIssue: {issue}")

print("=" * 55)
print("  FRED BAKER'S AUTOMATIONS — Claude API Live Test")
print("=" * 55)

print("\n📜 LEXAI RESPONSE:")
print("-" * 55)
print(lexai_query(
    client_name="Obi & Partners Legal",
    issue="Contract dispute with vendor over delivery timelines"
))

print("\n🏢 ESTATEIQ RESPONSE:")
print("-" * 55)
print(estateiq_query(
    property_type="Commercial Office Space",
    location="Maitama, Abuja",
    budget="₦50,000,000"
))

print("\n⚙️ OPSGUARD RESPONSE:")
print("-" * 55)
print(opsguard_query(
    company="Eze Oil & Gas Ltd",
    operation="Pipeline inspection",
    issue="Delayed maintenance schedule due to weather"
))

print("\n" + "=" * 55)
print("  ✅ All three products powered by Claude API!")
print("=" * 55)
