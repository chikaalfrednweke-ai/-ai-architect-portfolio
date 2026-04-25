# ============================================
# Fred Baker's Automations
# setup.py — Week 2 Environment Setup
# ============================================

# First install the Anthropic library
# Run this in terminal: pip install anthropic

try:
    import anthropic
    print("✅ Anthropic library is installed and ready!")
except ImportError:
    print("❌ Anthropic library not found!")
    print("👉 Run: pip install anthropic")

# Check python version
import sys
print(f"✅ Python version: {sys.version}")
print("🚀 Ready for Claude API — just need the API key!")