#!/usr/bin/env python3
"""
Set up environment variables for development.
"""

import os

# Set required environment variables for development
os.environ["SECRET_KEY"] = "dev-secret-key-for-testing-only"
os.environ["API_KEY"] = "dev-api-key-for-testing-only"
os.environ["POSTGRES_PASSWORD"] = "dev-password"
os.environ["NIM_API_KEY"] = "dev-nim-key"
os.environ["LOG_LEVEL"] = "INFO"

print("✅ Environment variables set for development")
