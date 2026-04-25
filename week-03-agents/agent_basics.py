# ============================================
# Fred Baker's Automations
# agent_basics.py — AI Agent Foundations
# ============================================

# An agent has 3 core components:
# 1. MEMORY   — what it knows
# 2. TOOLS    — what it can do
# 3. PLANNING — how it decides

import json
from datetime import datetime

# ---- MEMORY ----
class AgentMemory:
    def __init__(self):
        self.conversations = []
        self.client_data = {}
    
    def remember(self, role, message):
        self.conversations.append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def recall(self):
        return self.conversations
    
    def store_client(self, name, data):
        self.client_data[name] = data
        print(f"  💾 Stored client: {name}")
    
    def get_client(self, name):
        return self.client_data.get(name, None)

# ---- TOOLS ----
class AgentTools:
    def search_client(self, memory, name):
        client = memory.get_client(name)
        if client:
            return f"✅ Found: {client}"
        return f"❌ Client {name} not found"
    
    def qualify_lead(self, revenue, employees):
        score = 0
        if revenue > 10000000: score += 3
        elif revenue > 5000000: score += 2
        else: score += 1
        
        if employees > 50: score += 3
        elif employees > 20: score += 2
        else: score += 1
        
        if score >= 5:
            return "🔥 HOT LEAD — Priority outreach"
        elif score >= 3:
            return "⚡ WARM LEAD — Schedule follow up"
        else:
            return "❄️  COLD LEAD — Nurture campaign"
    
    def recommend_product(self, industry):
        mapping = {
            "law": "LexAI",
            "legal": "LexAI",
            "real estate": "EstateIQ",
            "property": "EstateIQ",
            "oil": "OpsGuard",
            "gas": "OpsGuard",
            "energy": "OpsGuard"
        }
        for key in mapping:
            if key in industry.lower():
                return f"✅ Recommended: {mapping[key]}"
        return "⚠️ Custom solution needed"

# ---- AGENT ----
class FredBakersAgent:
    def __init__(self):
        self.memory = AgentMemory()
        self.tools = AgentTools()
        self.name = "Fred Baker's AI Agent"
    
    def process(self, task, **kwargs):
        print(f"\n  🤖 Agent processing: {task}")
        print("-" * 50)
        
        if task == "qualify_lead":
            result = self.tools.qualify_lead(
                kwargs["revenue"],
                kwargs["employees"]
            )
            self.memory.remember("agent", result)
            print(f"  {result}")
        
        elif task == "recommend_product":
            result = self.tools.recommend_product(kwargs["industry"])
            self.memory.remember("agent", result)
            print(f"  {result}")
        
        elif task == "store_client":
            self.memory.store_client(kwargs["name"], kwargs["data"])
        
        elif task == "search_client":
            result = self.tools.search_client(
                self.memory, kwargs["name"]
            )
            print(f"  {result}")

# ---- RUN THE AGENT ----
print("=" * 50)
print("  FRED BAKER'S AUTOMATIONS")
print("  AI Agent — Basic Demo")
print("=" * 50)

# Initialize agent
agent = FredBakersAgent()

# Store some clients
agent.process("store_client",
    name="Obi & Partners",
    data={"industry": "law", "revenue": 15000000, "employees": 35}
)

agent.process("store_client",
    name="Aliyu Real Estate",
    data={"industry": "real estate", "revenue": 8000000, "employees": 12}
)

# Qualify leads
agent.process("qualify_lead", revenue=15000000, employees=35)
agent.process("qualify_lead", revenue=8000000, employees=12)
agent.process("qualify_lead", revenue=2000000, employees=5)

# Recommend products
agent.process("recommend_product", industry="law firm")
agent.process("recommend_product", industry="oil and gas")
agent.process("recommend_product", industry="real estate")

# Search clients
agent.process("search_client", name="Obi & Partners")
agent.process("search_client", name="Unknown Company")

print("\n" + "=" * 50)
print("  ✅ Agent demo complete!")
print("  🚀 Week 3 — AI Agents foundations done!")
print("=" * 50)