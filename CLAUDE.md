# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Advanced RAG experimentation repository focused on comparing Late Interaction (ColBERT) vs Dense Retrieval methods using restaurant reviews data. Built for AI Tinkerers demonstration with modular Jupyter notebooks.

## Development Commands

### Environment Setup
```bash
# Install dependencies (Python 3.8+)
uv pip install -e .

# Install with optional dependencies
uv pip install -e .[dev]        # Development tools (pytest, black, ruff)
uv pip install -e .[gpu]        # GPU support (faiss-gpu, torch[cuda])
uv pip install -e .[demo]       # Demo tools (gradio, streamlit)
```

### Code Quality
```bash
# Format code
black .

# Lint code
ruff check .

# Run tests
pytest
```

### Demo Applications
```bash
# Run Streamlit annotation app
streamlit run annotation/streamlit_app.py

# Extract PDF text (research papers)
python scripts/extract_pdf_text.py
```

## Architecture

### Core Setup System
- **setup.py**: Main environment configuration loader imported by all notebooks
- Handles .env loading, device detection (MPS/CUDA/CPU), and common imports
- Sets PROJECT_ROOT, DATA_DIR and other paths automatically

### Notebook Structure (`/notebooks/`)

**ColBERT Pipeline** (main demo):
1. `0-Exploratory Data Analysis.ipynb` - Dataset exploration
2. `1-Setup-And-Configuration.ipynb` - Environment and dependency verification
3. `2-Dense-Embeddings.ipynb` - Traditional dense retrieval baseline
4. `3-ColBERT-Embeddings.ipynb` - Token-level ColBERT embeddings
5. `4-Search-Comparison.ipynb` - Side-by-side comparison
6. `5-Token-Visualization.ipynb` - ColBERT MaxSim visualization
7. `6-Demo-Summary.ipynb` - Final insights and takeaways

**Reasoning Retrievers** (experimental):
- Promptriever and Rank1 reasoning approaches

### Data Management
- **data/**: CSV files with restaurant reviews and test queries
- **vector_store/**: LanceDB vector database (created during notebook runs)
- **research/**: PDF papers and extracted text for reference

### Key Technologies
- **PyTorch**: Core ML framework with MPS (Apple Silicon) support
- **PyLate**: ColBERT implementation for late interaction
- **LanceDB**: Vector database with multi-vector support
- **SentenceTransformers**: Dense embedding baseline
- **Streamlit**: Data annotation and viewing interface

## Notebook Usage

All notebooks should start with:
```python
import sys
sys.path.append('../..')  # For ColBERT/ subfolder
from setup import *       # Loads environment and common imports
```

This provides access to:
- Environment variables (PROJECT_ROOT, DATA_DIR, model names)
- Device detection via `get_device()`
- Pre-configured plotting and pandas setup

## Model Configuration

Dense models load on CPU for M1/M2 compatibility:
```python
device_for_dense = 'cpu' if get_device() == 'mps' else get_device()
```

ColBERT models work better on CPU for Apple Silicon.

## Key Demo Queries

Test these to show ColBERT advantages:
- Multi-constraint: "Italian budget-friendly outdoor seating"
- Contradictory: "expensive but worth it fine dining"
- Specific needs: "laptop work wifi quiet productive"
- Complex preferences: "vegetarian sushi late night"