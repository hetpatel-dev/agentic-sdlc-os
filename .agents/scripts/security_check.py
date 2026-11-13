#!/usr/bin/env python3
"""
Hook adapter delegating to root scripts/security_check.py
"""
import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

import scripts.security_check as sec

if __name__ == "__main__":
    sec.main()
