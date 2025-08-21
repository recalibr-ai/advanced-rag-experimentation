"""
Simple notebook setup using .env configuration.
Import this at the top of any notebook for consistent environment setup.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (same directory as this file)
project_root = Path(__file__).parent
env_path = project_root / ".env"

if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded environment from: {env_path}")
else:
    print(f"⚠️  No .env file found at: {env_path}")

# Add project root to Python path for imports
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Change working directory to project root
os.chdir(project_root)

# Common imports for notebooks
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Configure warnings and plotting
warnings.filterwarnings('ignore')
try:
    plt.style.use('seaborn-v0_8')
except OSError:
    plt.style.use('default')
    
try:
    sns.set_palette("husl")
except:
    pass

# Device configuration helper
def get_device():
    """Get optimal device based on .env DEVICE setting or auto-detect"""
    device_setting = os.getenv('DEVICE', 'auto').lower()
    
    if device_setting != 'auto':
        return device_setting
        
    # Auto-detect
    try:
        import torch
        if torch.backends.mps.is_available():
            return "mps"
        elif torch.cuda.is_available():
            return "cuda"
        else:
            return "cpu"
    except ImportError:
        return "cpu"

# Print setup info
print(f"📂 Working directory: {os.getcwd()}")
print(f"🎯 Project root: {os.getenv('PROJECT_ROOT', 'Not set')}")
print(f"📊 Data directory: {os.getenv('DATA_DIR', 'Not set')}")
print(f"🔧 Device: {get_device()}")
print(f"📁 Environment variables loaded: {len([k for k in os.environ.keys() if not k.startswith('_')])}")