# ============================================
# Fred Baker's Automations
# opsguard_engine.py — OpsGuard RAG + Claude
# Nigerian Oil & Gas AI Knowledge Base
# ============================================

import chromadb
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# ---- CONFIGURATION ----
COLLECTION_NAME = "opsguard_nigeria_oilgas"
DB_PATH = "./chroma_db"

# ---- OIL & GAS DOCUMENTS ----
OIL_GAS_DOCS = [
    {
        "id": "pia_001",
        "title": "Petroleum Industry Act 2021 Operations Guide",
        "content": """
        The PIA 2021 governs all petroleum operations in Nigeria.
        Key operational requirements:
        1. Petroleum Prospecting License (PPL): Offshore 4 years, Onshore 3 years
        2. Petroleum Mining Lease (PML): 20 years, renewable
        3. Regulatory agencies: NUPRC (upstream), NMDPRA (midstream/downstream)
        Fiscal terms: Royalty 5-12.5% onshore, 5-8% offshore.
        Hydrocarbon tax 15-30%. Companies Income Tax 30%.
        Host Community: 3% of OPEX to Host Community Development Trust annually.
        """,
        "category": "Regulatory Framework",
        "source": "Petroleum Industry Act 2021"
    },
    {
        "id": "hse_001",
        "title": "HSE Management in Nigerian Oil & Gas Operations",
        "content": """
        HSE Management System Requirements:
        1. HSE Policy: Written, signed by CEO, reviewed annually
        2. Risk Assessment: HIRA, JSA for all tasks, PHA for facilities
        3. Permit to Work: Hot work, cold work, confined space, electrical permits
        4. Emergency Response Plan: Mandatory, quarterly drills minimum
        5. Incident Reporting: Near misses within 24hrs, LTI within 24hrs,
           Fatalities immediate notification to NUPRC
        Key KPIs: TRIR, LTIF, PSE, NMFR, DAFW
        Regulatory framework: NUPRC HSE Regulations, DPR Guidelines, NESREA
        """,
        "category": "HSE Management",
        "source": "NUPRC HSE Regulations"
    },
    {
        "id": "pipeline_001",
        "title": "Pipeline Operations and Integrity Management Nigeria",
        "content": """
        Pipeline Integrity Management Program (PIMP):
        1. Baseline Assessment: In-line inspection (smart pig) within 5 years
        2. Threat Identification: Corrosion, third-party damage (most common in Nigeria),
           manufacturing defects, equipment malfunction
        3. Monitoring: Daily aerial/ground patrols, SCADA, cathodic protection,
           leak detection systems
        4. Vandalism Prevention: Community engagement, host community employment,
           anonymous reporting hotlines, joint surveillance with security agencies
        5. Repair: Emergency procedures documented, regulatory notification within 2 hours
        Response times: Major spill response within 1 hour,
        notification within 2 hours, containment within 24 hours.
        """,
        "category": "Pipeline Operations",
        "source": "NUPRC Pipeline Regulations"
    },
    {
        "id": "environmental_001",
        "title": "Environmental Compliance in Nigerian Oil & Gas",
        "content": """
        Key environmental regulations: EIA Act, NESREA, NUPRC Guidelines, NOSDRA, PIA 2021.
        EIA: Mandatory for all new projects, public consultation required,
        Federal Ministry of Environment approval needed, annual audit required.
        Gas Flaring: Prohibited except safety reasons, fines $3.50 per 1,000 SCF,
        zero flaring target by 2030.
        Oil Spill Response: NOSDRA notified within 24 hours,
        Joint Investigation Visit (JIV) process within 72 hours.
        Penalties: Oil spill N1,000 per barrel, gas flaring $3.50/1,000 SCF,
        EIA violation up to N5 million.
        Environmental reporting: Monthly performance reports, annual audit (EAR),
        quarterly gas flaring reports.
        """,
        "category": "Environmental Compliance",
        "source": "NESREA Act, NOSDRA Act, PIA 2021"
    },
    {
        "id": "incident_001",
        "title": "Incident Reporting and Management in Oil & Gas Nigeria",
        "content": """
        Incident classification:
        Level 1 CATASTROPHIC: Fatalities, major environmental damage, >$1M asset damage.
        Immediate notification to NUPRC CEO, investigation within 24 hours.
        Level 2 CRITICAL: Serious injuries, significant spill >1 barrel.
        Notification within 2 hours, investigation within 48 hours.
        Level 3 MAJOR: Lost Time Injury, minor spill <1 barrel. Report within 24 hours.
        Level 4 MINOR: First aid cases, low potential near misses. Report within 72 hours.
        Investigation Process: Scene preservation, notify regulators, form investigation team,
        Root Cause Analysis (RCA), Corrective Action Plan (CAP), lessons learned.
        RCA methods: Fault Tree Analysis, Bow-Tie Analysis, 5-Why Analysis.
        OpsGuard automation: Digital reporting, automatic notifications,
        investigation workflow, corrective action tracking, predictive analytics.
        """,
        "category": "Incident Management",
        "source": "NUPRC Incident Reporting Guidelines"
    },
    {
        "id": "maintenance_001",
        "title": "Maintenance Management in Nigerian Oil & Gas Facilities",
        "content": """
        Types of maintenance programs:
        1. Preventive Maintenance (PM): Scheduled, equipment-specific intervals
        2. Predictive Maintenance (PdM): Condition monitoring, vibration analysis,
           thermography, AI/IoT sensors increasingly used
        3. Corrective Maintenance (CM): Repair after breakdown
        4. Shutdown/Turnaround: Major overhaul every 2-4 years, 6-12 months planning
        Key KPIs: Equipment Availability >95%, MTBF, MTTR <4 hours,
        Planned Maintenance Compliance >90%, Maintenance Cost <3% of asset value.
        Nigerian challenges: Spare parts availability, power supply,
        skilled technician shortage, corrosion from Niger Delta climate.
        Documentation: Equipment registers, maintenance history (5 years minimum),
        calibration certificates, pressure vessel certificates.
        """,
        "category": "Maintenance Management",
        "source": "NUPRC Operations Guidelines, ISO 55000"
    },
    {
        "id": "production_001",
        "title": "Oil Production Operations and Optimization Nigeria",
        "content": """
        Production monitoring requirements:
        Daily production reports to NUPRC, metering accuracy ±0.25%,
        meter calibration every 6 months minimum.
        Well management: Quarterly testing, annual integrity assessment,
        workover operations require regulatory approval.
        Production efficiency targets: Uptime >90%, water cut management,
        GOR monitoring, production deferment tracking.
        OpsGuard automation: Real-time monitoring dashboard,
        automated deferment logging, SCADA integration,
        predictive analytics, automated regulatory reports.
        Production sharing contracts: Government take through NNPC,
        cost oil recovery, profit oil split, royalty payments.
        """,
        "category": "Production Operations",
        "source": "NUPRC Production Guidelines, PIA 2021"
    },
    {
        "id": "community_001",
        "title": "Host Community Relations in Nigerian Oil & Gas",
        "content": """
        Legal framework: PIA 2021 3% OPEX to HCDT, NDDC Act, MOUs with communities.
        Host Community Development Trust (HCDT):
        Mandatory, board includes community representatives,
        funds for education, health, infrastructure, skills.
        Common grievances: Environmental pollution, lack of local employment,
        inadequate compensation, infrastructure deficit, health impacts from flaring.
        Best practices:
        1. Community Liaison Officers (CLOs) hired from host communities
        2. Employment: Local content requirements (NCDMB), skills training
        3. Grievance Management: Formal register, response within 30 days
        4. Environmental Remediation: Prompt response, community involvement
        Impact of poor relations: Pipeline vandalism, facility shutdowns,
        legal action, reputational damage, force majeure claims.
        """,
        "category": "Community Relations",
        "source": "PIA 2021, NDDC Act, NCDMB Guidelines"
    },
    {
        "id": "local_content_001",
        "title": "Nigerian Local Content Requirements Oil & Gas",
        "content": """
        NOGICD Act 2010 administered by NCDMB.
        Nigerian First Principle: Nigerian companies must be considered first.
        Minimum thresholds: Seismic acquisition 95%, Pipeline construction 45%,
        Engineering design 50%, Legal services 100% Nigerian law firms,
        Insurance 70% Nigerian insurers.
        Employment: Management 50% Nigerian (Year 1) increasing to 70% by Year 5,
        Senior staff 75%, Junior staff 95%.
        Nigerian Content Plan (NCP): Required for contracts >$1 million,
        submitted to NCDMB, monthly compliance reports, annual audit.
        Penalties: Fines up to 5% of contract value, contract cancellation,
        debarment from future contracts.
        OpsGuard tracking: Automated Nigerian staff percentage calculation,
        contract compliance monitoring, NCP submission preparation.
        """,
        "category": "Local Content",
        "source": "NOGICD Act 2010, NCDMB Guidelines"
    },
    {
        "id": "scada_001",
        "title": "SCADA and Digital Operations in Nigerian Oil & Gas",
        "content": """
        SCADA applications: Pipeline monitoring (pressure, flow, leak detection,
        remote valve operation, theft detection), Production monitoring
        (wellhead pressure, separator levels, gas flare), Facility management.
        Digital transformation: IoT sensors, AI predictive maintenance,
        digital twin technology, drone inspections, mobile workforce apps.
        Cybersecurity: OT/IT network segregation mandatory,
        NUPRC cybersecurity guidelines 2022, regular penetration testing.
        OpsGuard integration: SCADA data ingestion, AI anomaly detection,
        automated alerts, mobile incident reporting, regulatory auto-reports,
        predictive analytics, digital permit to work, real-time HSE dashboard.
        ROI: 15-25% reduction unplanned downtime, 10-20% maintenance cost reduction,
        30-40% faster incident response, 50-70% reduction in manual reporting.
        """,
        "category": "Digital Operations",
        "source": "NUPRC Digital Guidelines"
    }
]

# ---- OPSGUARD RAG ENGINE ----
class OpsGuardRAGEngine:
    def __init__(self):
        print("  Initializing OpsGuard RAG Engine...")
        self.client_db = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client_db.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Nigerian Oil & Gas Knowledge Base"}
        )
        self.claude = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        print(f"  Documents in DB: {self.collection.count()}")

    def load_documents(self, documents):
        print(f"\n  Loading {len(documents)} documents...")
        ids = []
        texts = []
        metadatas = []

        for doc in documents:
            ids.append(doc["id"])
            texts.append(f"{doc['title']}\n\n{doc['content']}")
            metadatas.append({
                "title": doc["title"],
                "category": doc["category"],
                "source": doc["source"]
            })

        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        print(f"  Loaded {len(documents)} documents!")
        print(f"  Total in DB: {self.collection.count()}")

    def search(self, query, n_results=3):
        return self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

    def answer(self, question):
        print(f"\n  ❓ {question}")
        results = self.search(question)

        context = ""
        for i, (doc, meta) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0]
        )):
            context += f"\n--- Source {i+1}: {meta['title']} ---\n"
            context += f"Category: {meta['category']}\n"
            context += f"Source: {meta['source']}\n"
            context += f"Content: {doc[:600]}\n"

        print("  Sources found:")
        for i, meta in enumerate(results["metadatas"][0]):
            print(f"    {i+1}. {meta['title']}")

        prompt = f"""You are OpsGuard, an AI operations assistant specializing
in Nigerian oil and gas operations. Use the following knowledge base to answer accurately.

OIL & GAS KNOWLEDGE BASE:
{context}

QUESTION: {question}

Provide a clear, safety-focused answer about Nigerian oil & gas operations.
Reference specific regulations and standards. Be precise and actionable."""

        message = self.claude.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

# ---- MAIN ----
print("=" * 55)
print("  FRED BAKER'S AUTOMATIONS")
print("  OpsGuard — RAG + Claude API = FULL POWER!")
print("=" * 55)

engine = OpsGuardRAGEngine()
engine.load_documents(OIL_GAS_DOCS)

test_questions = [
    "What are the HSE requirements for oil operations?",
    "How do I report an oil spill in Nigeria?",
    "What are local content requirements?",
]

print("\n" + "=" * 55)
print("  OPSGUARD REAL AI RESPONSES")
print("=" * 55)

for question in test_questions:
    answer = engine.answer(question)
    print("\n" + "-" * 55)
    print(answer)
    print()

print("=" * 55)
print("  OpsGuard RAG + Claude = FULLY OPERATIONAL!")
print("=" * 55)