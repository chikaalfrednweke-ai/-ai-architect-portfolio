# ============================================
# Fred Baker's Automations
# opsguard_engine.py — OpsGuard RAG Pipeline
# Nigerian Oil & Gas AI Knowledge Base
# ============================================

import chromadb
from datetime import datetime

# ---- CONFIGURATION ----
COLLECTION_NAME = "opsguard_nigeria_oilgas"
DB_PATH = "./chroma_db"

# ---- NIGERIAN OIL & GAS DOCUMENTS ----
OIL_GAS_DOCS = [
    {
        "id": "pia_001",
        "title": "Petroleum Industry Act 2021 — Operations Guide",
        "content": """
        The Petroleum Industry Act (PIA) 2021 governs all petroleum operations
        in Nigeria and established new regulatory frameworks.
        
        Key operational requirements under PIA 2021:
        
        1. Petroleum Prospecting License (PPL):
           - Replaces Oil Prospecting License (OPL)
           - Offshore: Maximum 4 years
           - Onshore: Maximum 3 years
           - Renewable once for same period
           - Work program obligations mandatory
           
        2. Petroleum Mining Lease (PML):
           - Replaces Oil Mining Lease (OML)
           - Duration: 20 years, renewable
           - Minimum production obligations
           - Annual rental payments required
           
        3. Midstream/Downstream License:
           - Required for transportation, processing, storage
           - Issued by NMDPRA (new agency)
           - Different tiers based on capacity
           
        Regulatory agencies under PIA 2021:
        - NUPRC: Upstream regulation and licensing
        - NMDPRA: Midstream and downstream regulation
        - NNPC Limited: Commercial entity (no longer regulator)
        
        Fiscal terms:
        - Royalty rates: 5-12.5% for onshore, 5-8% offshore
        - Hydrocarbon tax: 15-30% depending on field type
        - Companies Income Tax: 30% still applies
        - Petroleum Profits Tax (PPT): Being phased out
        
        Host Community obligations:
        - 3% of actual operating expenditure annually
        - Host Community Development Trust mandatory
        - Board includes community representatives
        - Funds for education, health, infrastructure
        """,
        "category": "Regulatory Framework",
        "source": "Petroleum Industry Act 2021"
    },
    {
        "id": "hse_001",
        "title": "HSE Management in Nigerian Oil & Gas Operations",
        "content": """
        Health, Safety and Environment (HSE) management is critical in Nigerian
        oil and gas operations, regulated by multiple agencies.
        
        HSE regulatory framework:
        1. NUPRC HSE Regulations
        2. Department of Petroleum Resources (DPR) guidelines
        3. National Environmental Standards and Regulations 
           Enforcement Agency (NESREA)
        4. Federal Ministry of Environment regulations
        
        HSE Management System Requirements:
        
        1. HSE Policy:
           - Written policy signed by CEO
           - Communicated to all employees
           - Reviewed annually
           
        2. Risk Assessment:
           - Hazard Identification and Risk Assessment (HIRA)
           - Job Safety Analysis (JSA) for all tasks
           - Process Hazard Analysis (PHA) for facilities
           
        3. Permit to Work System:
           - Hot work permits
           - Cold work permits  
           - Confined space entry permits
           - Electrical isolation permits
           
        4. Emergency Response:
           - Emergency Response Plan (ERP) mandatory
           - Drill exercises: Minimum quarterly
           - Muster points clearly marked
           - Emergency contact numbers posted
           
        5. Incident Reporting:
           - Near misses must be reported within 24 hours
           - Lost Time Injuries (LTI): Report within 24 hours
           - Fatalities: Immediate notification to NUPRC
           - Monthly HSE statistics to regulators
           
        Key performance indicators:
        - Total Recordable Incident Rate (TRIR)
        - Lost Time Injury Frequency (LTIF)
        - Process Safety Events (PSE)
        - Near Miss Frequency Rate (NMFR)
        - Days Away from Work (DAFW)
        """,
        "category": "HSE Management",
        "source": "NUPRC HSE Regulations, DPR Guidelines"
    },
    {
        "id": "pipeline_001",
        "title": "Pipeline Operations and Integrity Management Nigeria",
        "content": """
        Pipeline integrity management is critical for safe oil and gas
        transportation in Nigeria, where pipeline vandalism is a major challenge.
        
        Pipeline regulatory requirements:
        - NUPRC Pipeline Regulations
        - Nigerian Pipeline Code
        - API 1160 (Managing System Integrity for Hazardous Liquid Pipelines)
        - ASME B31.4 and B31.8 standards adopted in Nigeria
        
        Pipeline Integrity Management Program (PIMP):
        
        1. Baseline Assessment:
           - In-line inspection (smart pig) within 5 years of operation
           - Direct Assessment where ILI not possible
           - Hydrostatic testing for new pipelines
           
        2. Threat Identification:
           - Corrosion (internal and external)
           - Third-party damage (most common in Nigeria)
           - Manufacturing defects
           - Equipment malfunction
           - Incorrect operations
           
        3. Monitoring and Surveillance:
           - Daily aerial/ground patrols in high-risk areas
           - SCADA (Supervisory Control and Data Acquisition)
           - Cathodic protection monitoring
           - Leak detection systems
           - Community surveillance programs
           
        4. Pipeline Vandalism Prevention (Nigeria-specific):
           - Community engagement programs
           - Host community employment
           - Alternative livelihood programs
           - Joint surveillance with security agencies
           - Anonymous reporting hotlines
           
        5. Repair and Maintenance:
           - Emergency repair procedures documented
           - Repair clamps and materials pre-positioned
           - Trained repair crews on standby
           - Regulatory notification within 2 hours of rupture
           
        Response times required:
        - Major spill: Response within 1 hour
        - Regulatory notification: Within 2 hours
        - Containment: Within 24 hours
        - Clean-up initiation: Within 48 hours
        """,
        "category": "Pipeline Operations",
        "source": "NUPRC Pipeline Regulations, Nigerian Pipeline Code"
    },
    {
        "id": "environmental_001",
        "title": "Environmental Compliance in Nigerian Oil & Gas",
        "content": """
        Environmental compliance is increasingly enforced in Nigeria's oil and gas
        sector, with significant penalties for violations.
        
        Key environmental regulations:
        1. Environmental Impact Assessment (EIA) Act
        2. National Environmental Standards (NESREA)
        3. NUPRC Environmental Guidelines
        4. National Oil Spill Detection and Response Agency (NOSDRA)
        5. Petroleum Industry Act 2021 environmental provisions
        
        Environmental Impact Assessment (EIA):
        - Mandatory for all new oil and gas projects
        - Must be completed before project commencement
        - Public consultation required
        - Federal Ministry of Environment approval needed
        - Annual Environmental Audit required post-approval
        
        Gas Flaring Regulations:
        - Gas flaring prohibited except for safety reasons
        - Fines for unauthorized flaring: $3.50 per 1,000 SCF
        - Zero flaring target by 2030 (government policy)
        - Associated gas utilization plans mandatory
        - Flare-out targets in all new licenses
        
        Oil Spill Response:
        - NOSDRA must be notified within 24 hours
        - Joint Investigation Visit (JIV) process:
          1. Operator notifies NOSDRA and NUPRC
          2. Joint team visits site within 72 hours
          3. Cause determination (sabotage vs operational)
          4. Remediation plan agreed
        - Polluter pays principle strictly enforced
        - Remediation must meet DPR standards
        
        Environmental penalties:
        - Oil spill fines: N1,000 per barrel spilled
        - Gas flaring: $3.50 per 1,000 SCF above allowance
        - EIA violation: Up to N5 million
        - Repeat offenders: License suspension/revocation
        
        Environmental reporting:
        - Monthly environmental performance reports
        - Annual Environmental Audit Report (EAR)
        - Quarterly gas flaring reports to NUPRC
        - Incident reports to NOSDRA within 24 hours
        """,
        "category": "Environmental Compliance",
        "source": "NESREA Act, NOSDRA Act, PIA 2021"
    },
    {
        "id": "incident_001",
        "title": "Incident Reporting and Management in Oil & Gas Nigeria",
        "content": """
        Effective incident management is critical in Nigerian oil and gas operations.
        All incidents must be properly reported, investigated, and prevented.
        
        Incident classification system:
        
        Severity Level 1 — CATASTROPHIC:
        - Fatalities or multiple serious injuries
        - Major environmental damage
        - Significant asset damage (>$1M)
        - Mandatory immediate notification to NUPRC CEO
        - Investigation team within 24 hours
        
        Severity Level 2 — CRITICAL:
        - Serious injuries requiring hospitalization
        - Significant spill (>1 barrel crude oil)
        - Major equipment failure
        - Notification within 2 hours
        - Investigation within 48 hours
        
        Severity Level 3 — MAJOR:
        - Lost Time Injury (LTI)
        - Minor spill (< 1 barrel)
        - Near miss with high potential
        - Report within 24 hours
        
        Severity Level 4 — MINOR:
        - First aid cases
        - Near misses with low potential
        - Report within 72 hours
        
        Incident Investigation Process:
        1. Scene preservation and immediate response
        2. Notify regulatory authorities (timeline above)
        3. Form investigation team (HSE + Operations + Management)
        4. Root cause analysis (RCA) using:
           - Fault Tree Analysis (FTA)
           - Bow-Tie Analysis
           - 5-Why Analysis
        5. Corrective Action Plan (CAP) development
        6. Implementation and verification
        7. Lessons learned distribution
        8. Close-out report to regulators
        
        OpsGuard automation opportunities:
        - Digital incident reporting (WhatsApp/mobile)
        - Automatic regulatory notification
        - Investigation workflow management
        - Corrective action tracking
        - Real-time HSE dashboard
        - Predictive analytics for incident prevention
        """,
        "category": "Incident Management",
        "source": "NUPRC Incident Reporting Guidelines"
    },
    {
        "id": "maintenance_001",
        "title": "Maintenance Management in Nigerian Oil & Gas Facilities",
        "content": """
        Effective maintenance management ensures operational continuity and safety
        in Nigerian oil and gas facilities.
        
        Types of maintenance programs:
        
        1. Preventive Maintenance (PM):
           - Scheduled maintenance based on time or usage
           - Equipment-specific intervals (manufacturer recommendations)
           - Nigerian regulations require documented PM schedules
           - Examples: Monthly pump inspections, annual pressure tests
           
        2. Predictive Maintenance (PdM):
           - Condition monitoring to predict failures
           - Vibration analysis, thermography, oil analysis
           - More cost-effective than pure preventive maintenance
           - AI/IoT sensors increasingly used in Nigeria
           
        3. Corrective Maintenance (CM):
           - Repair after breakdown
           - Emergency repairs classified by priority
           - Spare parts management critical
           - MTTR (Mean Time to Repair) tracked as KPI
           
        4. Shutdown/Turnaround Maintenance:
           - Major planned shutdowns for overhaul
           - Typically every 2-4 years
           - Requires detailed planning 6-12 months ahead
           - Critical path management essential
           
        Key Maintenance KPIs:
        - Equipment Availability: Target >95%
        - Mean Time Between Failures (MTBF)
        - Mean Time to Repair (MTTR): Target <4 hours
        - Planned Maintenance Compliance: Target >90%
        - Maintenance Cost as % of Asset Value: Target <3%
        
        Nigerian-specific challenges:
        - Spare parts availability (long lead times)
        - Power supply for maintenance equipment
        - Skilled technician shortage
        - Corrosion due to Niger Delta climate
        - Security during maintenance activities
        
        Maintenance documentation requirements:
        - Equipment registers and asset lists
        - Maintenance history records (5 years minimum)
        - Calibration certificates for instruments
        - Pressure vessel inspection certificates
        - Lifting equipment certificates
        """,
        "category": "Maintenance Management",
        "source": "NUPRC Operations Guidelines, ISO 55000"
    },
    {
        "id": "production_001",
        "title": "Oil Production Operations and Optimization Nigeria",
        "content": """
        Oil production optimization is critical for Nigerian operators to maximize
        recovery from existing fields while meeting regulatory requirements.
        
        Production monitoring requirements:
        - Daily production reports to NUPRC
        - Metering accuracy: ±0.25% for fiscal metering
        - Meter calibration: Every 6 months minimum
        - Production allocation for joint ventures
        - Lifting schedules coordinated with NNPC
        
        Well management:
        1. Well testing: Minimum quarterly for producing wells
        2. Well integrity: Annual well integrity assessment
        3. Workover operations: Require regulatory approval
        4. Well abandonment: NUPRC permit required
        5. Production enhancement: Approval for major interventions
        
        Reservoir management:
        - Field Development Plan (FDP) approved by NUPRC
        - Annual update of FDP required
        - Material Balance calculations
        - Production optimization studies
        - Enhanced Oil Recovery (EOR) planning
        
        Production efficiency targets:
        - Uptime target: >90% for mature fields
        - Water cut management to maximize oil production
        - Gas-Oil Ratio (GOR) monitoring
        - Production deferment tracking and reporting
        
        OpsGuard production automation:
        - Real-time production monitoring dashboard
        - Automated deferment logging and reporting
        - SCADA data integration
        - Predictive analytics for production optimization
        - Automated regulatory report generation
        - Production allocation calculations
        
        Production sharing contracts (PSCs):
        - Government take through NNPC
        - Cost oil recovery provisions
        - Profit oil split between NNPC and operator
        - Royalty payments based on production rate
        """,
        "category": "Production Operations",
        "source": "NUPRC Production Guidelines, PIA 2021"
    },
    {
        "id": "community_001",
        "title": "Host Community Relations in Nigerian Oil & Gas",
        "content": """
        Host community relations is one of the most critical aspects of Nigerian
        oil and gas operations, directly affecting operational continuity.
        
        Legal framework:
        - PIA 2021: 3% of OPEX to Host Community Development Trust
        - Niger Delta Development Commission (NDDC) Act
        - Memoranda of Understanding (MOUs) with communities
        - Corporate Social Responsibility (CSR) obligations
        
        Host Community Development Trust (HCDT) under PIA 2021:
        - Mandatory for all operators with licenses
        - Board composition: Operator + Community representatives
        - Funds for: Education, Health, Infrastructure, Skills
        - Annual report to NUPRC on fund utilization
        - Communities can sue for non-compliance
        
        Common community grievances in Niger Delta:
        1. Environmental pollution from spills
        2. Lack of employment for local people
        3. Inadequate compensation for land use
        4. Infrastructure deficit despite oil wealth
        5. Health impacts from gas flaring
        
        Best practices for community relations:
        1. Community Liaison Officers (CLOs):
           - Hire from host communities
           - Regular community meetings
           - Grievance mechanism established
           
        2. Employment:
           - Local content requirements (NCDMB)
           - Skills training programs
           - Preference for host community members
           
        3. Grievance Management:
           - Formal grievance register
           - Response within 30 days
           - Escalation procedures
           - Third-party mediation option
           
        4. Environmental Remediation:
           - Prompt response to spills
           - Community involvement in clean-up
           - Compensation for damages
           - Restoration of livelihoods
           
        Impact of poor community relations:
        - Pipeline vandalism and oil theft
        - Facility shutdowns and production loss
        - Legal action and regulatory sanctions
        - Reputational damage
        - Force majeure claims on contracts
        """,
        "category": "Community Relations",
        "source": "PIA 2021, NDDC Act, NCDMB Guidelines"
    },
    {
        "id": "local_content_001",
        "title": "Nigerian Local Content Requirements — Oil & Gas",
        "content": """
        The Nigerian Oil and Gas Industry Content Development Act 2010 (NOGICD Act)
        mandates local content in all oil and gas operations.
        
        Administered by: Nigerian Content Development and Monitoring Board (NCDMB)
        
        Key local content requirements:
        
        1. Nigerian First Principle:
           - Nigerian companies must be considered first
           - Must demonstrate Nigerian capacity is inadequate 
             before engaging foreign companies
             
        2. Minimum thresholds by category:
           - Seismic data acquisition: 95% Nigerian
           - Pipeline construction: 45% Nigerian
           - Engineering design: 50% Nigerian
           - Project management: 55% Nigerian
           - Legal services: 100% Nigerian law firms
           - Insurance: 70% Nigerian insurers
           
        3. Employment requirements:
           - Management positions: 50% Nigerian (Year 1)
             increasing to 70% by Year 5
           - Senior staff: 75% Nigerian
           - Junior staff: 95% Nigerian
           - Supervisory: 80% Nigerian
           
        4. Technology transfer:
           - Foreign companies must train Nigerians
           - Succession plans for expatriate positions
           - Technology licensing agreements
           
        5. Nigerian Content Plan (NCP):
           - Required for all contracts >$1 million
           - Submitted to NCDMB for approval
           - Monthly compliance reports
           - Annual audit by NCDMB
           
        Penalties for non-compliance:
        - Fines up to 5% of contract value
        - Contract cancellation
        - Debarment from future contracts
        - Blacklisting of company
        
        OpsGuard local content tracking:
        - Automated Nigerian staff percentage calculation
        - Contract compliance monitoring
        - NCP submission preparation
        - Vendor Nigerian status verification
        """,
        "category": "Local Content",
        "source": "NOGICD Act 2010, NCDMB Guidelines"
    },
    {
        "id": "scada_001",
        "title": "SCADA and Digital Operations in Nigerian Oil & Gas",
        "content": """
        Supervisory Control and Data Acquisition (SCADA) systems are increasingly
        critical for Nigerian oil and gas operations management.
        
        SCADA applications in Nigerian oil & gas:
        
        1. Pipeline monitoring:
           - Real-time pressure and flow monitoring
           - Leak detection algorithms
           - Remote valve operation
           - Theft detection (flow imbalances)
           
        2. Production monitoring:
           - Well head pressure and temperature
           - Separator levels and pressures
           - Gas flare monitoring
           - Water injection monitoring
           
        3. Facility management:
           - Tank level monitoring
           - Pump and compressor status
           - Power generation monitoring
           - Utility systems management
           
        Digital transformation in Nigerian oil & gas:
        1. IoT sensors for remote monitoring
        2. AI-powered predictive maintenance
        3. Digital twin technology for facilities
        4. Drone inspections replacing manual
        5. Mobile workforce management apps
        6. Cloud-based data management
        
        Cybersecurity requirements:
        - OT/IT network segregation mandatory
        - NUPRC cybersecurity guidelines (2022)
        - Incident response plan for cyber attacks
        - Regular penetration testing
        - Staff cybersecurity training
        
        OpsGuard digital integration:
        - SCADA data ingestion and analysis
        - AI anomaly detection for early warning
        - Automated alert generation and escalation
        - Mobile incident reporting integration
        - Regulatory report auto-generation from SCADA data
        - Predictive analytics for equipment failure
        - Digital permit to work system
        - Real-time HSE dashboard for management
        
        ROI of digital operations in Nigeria:
        - 15-25% reduction in unplanned downtime
        - 10-20% reduction in maintenance costs
        - 30-40% faster incident response
        - 50-70% reduction in manual reporting time
        - Improved regulatory compliance
        """,
        "category": "Digital Operations",
        "source": "NUPRC Digital Guidelines, Industry Best Practices"
    }
]

# ---- OPSGUARD RAG ENGINE ----
class OpsGuardRAGEngine:
    def __init__(self):
        print("  Initializing OpsGuard RAG Engine...")
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Nigerian Oil & Gas Knowledge Base for OpsGuard"}
        )
        print(f"  Collection: {COLLECTION_NAME}")
        print(f"  Documents in DB: {self.collection.count()}")

    def load_documents(self, documents):
        print(f"\n  Loading {len(documents)} documents into ChromaDB...")
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
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def answer(self, question):
        print(f"\n  Question: {question}")
        results = self.search(question)
        print("  Context retrieved:")
        for i, meta in enumerate(results["metadatas"][0]):
            print(f"    {i+1}. {meta['title']} ({meta['category']})")
        return results

# ---- MAIN ----
print("=" * 55)
print("  FRED BAKER'S AUTOMATIONS")
print("  OpsGuard RAG Pipeline — Nigerian Oil & Gas AI")
print("=" * 55)

engine = OpsGuardRAGEngine()
engine.load_documents(OIL_GAS_DOCS)

# Test queries
test_questions = [
    "What are the HSE requirements for oil operations?",
    "How do I report an oil spill in Nigeria?",
    "What is the PIA 2021 about?",
    "How do I manage pipeline integrity?",
    "What are local content requirements?",
    "How does SCADA help in oil operations?",
    "What are host community obligations?",
    "How do I handle a major incident?"
]

print("\n" + "=" * 55)
print("  TESTING OPSGUARD SEARCH")
print("=" * 55)

for question in test_questions:
    results = engine.answer(question)
    print(f"  Top match: {results['metadatas'][0][0]['title']}")
    print()

print("=" * 55)
print("  OpsGuard RAG Engine ready!")
print("  10 Nigerian Oil & Gas documents loaded")
print("  Next: Build OpsGuard operations dashboard")
print("=" * 55)