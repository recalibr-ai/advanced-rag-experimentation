# 📓 Notebook Structure Guide

## Overview
This project demonstrates advanced RAG techniques for the AI Tinkerers talk, focusing on **Late Interaction (ColBERT)** vs **Dense Retrieval** using restaurant reviews data.

## Current Notebooks

### 📁 `/notebooks/ColBERT/`

| Notebook | Status | Description |
|----------|--------|-------------|
| `0-Exploratory Data Analysis.ipynb` | ✅ In Progress | Dataset exploration and understanding |
| `1-Creating Vector DB.ipynb` | ✅ Created | Vector database setup with LanceDB |
| `colbert_demo.ipynb` | ✅ Working | Monolithic demo (to be broken down) |

## Recommended Modular Structure

Breaking down the monolithic demo into focused, manageable notebooks:

### 0️⃣ **Exploratory Data Analysis** 
- Load and explore the restaurant reviews dataset
- Basic statistics and visualizations
- Data quality checks
- Sample reviews analysis
- Understanding the data for RAG demo

### 1️⃣ **Setup and Configuration**
- Import shared config and setup
- Test device configuration (MPS/CUDA/CPU)
- Install and verify all dependencies
- LanceDB connection testing
- Model loading verification

### 2️⃣ **Dense Embeddings**
- Load SentenceTransformer model
- Create dense embeddings for all reviews
- Store in LanceDB dense table
- Basic dense search examples
- Visualize embedding space (optional)

### 3️⃣ **ColBERT Embeddings**
- Load PyLate ColBERT model
- Create token-level embeddings
- Store in LanceDB ColBERT table
- Understand multi-vector structure
- Token analysis and visualization

### 4️⃣ **Search Comparison**
- Implement both search functions
- Side-by-side comparisons on test queries
- Multi-constraint query testing ("Italian budget-friendly outdoor")
- Contradictory concepts testing ("expensive but worth it")
- Performance analysis

### 5️⃣ **Token Visualization**
- Deep dive into ColBERT token matching
- Visualize MaxSim operations
- Show why ColBERT wins specific cases
- Interactive token analysis
- Visual comparison of matching patterns

### 6️⃣ **Demo Summary**
- Final comparison and insights
- Storage vs quality trade-offs
- Key takeaways for AI Tinkerers talk
- Next steps and advanced techniques

## Setup Instructions

### Using the Setup System

All notebooks should start with:

```python
# For notebooks in ColBERT/ subfolder:
import sys
sys.path.append('../..')  # Add project root to path
from setup import *

# This automatically:
# - Loads .env configuration
# - Sets working directory to project root
# - Imports common libraries (pandas, numpy, matplotlib)
# - Configures plotting and warnings
```

### Environment Variables Available

After importing `setup`, you have access to:

```python
# Paths
os.getenv('PROJECT_ROOT')           # Project root directory
os.getenv('DATA_DIR')               # Data folder path
os.getenv('RESTAURANT_REVIEWS_CSV') # Restaurant reviews file

# Model Configuration
os.getenv('DENSE_MODEL_NAME')       # all-MiniLM-L6-v2
os.getenv('COLBERT_MODEL_NAME')     # sentence-transformers/all-MiniLM-L6-v2

# Vector Storage
os.getenv('LANCEDB_PATH')          # ./restaurant_reviews_vectors

# Helper Functions
get_device()                        # Returns optimal device (mps/cuda/cpu)
```

## Benefits of Modular Structure

### ✅ **Development Benefits**
- **Isolated debugging** - Issues confined to specific notebooks
- **Faster iteration** - Don't re-run everything when testing one part
- **Clear progression** - Logical flow from data to insights
- **Reusable components** - Import functions between notebooks

### ✅ **Presentation Benefits**
- **Easy to follow** - Audience can focus on one concept at a time
- **Skip sections** - Can jump to specific topics as needed
- **Live coding friendly** - Can run individual notebooks during talk
- **Clear narrative** - Story flows from problem to solution

### ✅ **Maintenance Benefits**
- **Version control** - Smaller, focused changes
- **Collaboration** - Multiple people can work on different notebooks
- **Documentation** - Each notebook self-documents its purpose
- **Testing** - Can validate each component independently

## Demo Flow for AI Tinkerers Talk

1. **Start with EDA** - Show the restaurant data everyone can relate to
2. **Explain the problem** - Why dense retrieval fails on complex queries
3. **Show dense baseline** - Traditional RAG approach and limitations
4. **Introduce ColBERT** - Token-level matching concept
5. **Live comparison** - Side-by-side results on test queries
6. **Visualize tokens** - Show exactly HOW ColBERT finds better matches
7. **Conclude with insights** - Trade-offs and when to use each approach

## Key Queries for Demo

Test these queries to show ColBERT's advantages:

1. **Multi-constraint**: "Italian budget-friendly outdoor seating"
2. **Contradictory**: "expensive but worth it fine dining"  
3. **Specific needs**: "laptop work wifi quiet productive"
4. **Complex preferences**: "vegetarian sushi late night"

## Next Steps

- [ ] Complete notebook 0 (EDA)
- [ ] Break down monolithic demo into notebooks 2-6
- [ ] Add interactive widgets for live demo
- [ ] Create presentation slides that reference notebooks
- [ ] Test full flow end-to-end