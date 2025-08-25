# Advanced RAG Experimentation

A comprehensive comparison of Late Interaction (ColBERT) vs Dense Retrieval methods using restaurant reviews data. This repository demonstrates the advantages of token-level retrieval over traditional dense embeddings.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Step 1: Create Virtual Environment

```bash
# Create a new virtual environment using uv
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
# Install the package with all dependencies
uv pip install -e .

# Optional: Install with development tools
uv pip install -e .[dev]

# Optional: Install with GPU support (if you have CUDA)
uv pip install -e .[gpu]

# Optional: Install demo tools (for Streamlit app)
uv pip install -e .[demo]
```

### Step 3: Configure Environment

```bash
# Copy the environment template
cp .env.copy .env

# Edit .env file and set your project root path
# Open .env in your editor and replace:
# PROJECT_ROOT=YOUR_ROOT_FOLDER
# with your actual project directory path, for example:
# PROJECT_ROOT=/Users/username/Documents/repos/advanced-rag-experimentation
```

### Step 4: View the Data (Optional)

Explore the synthetic restaurant reviews dataset using the Streamlit viewer:

```bash
# Run the Streamlit annotation viewer
streamlit run annotation/streamlit_app.py
```

This will open a browser window where you can:
- Browse restaurant reviews
- View sentiment scores
- Explore different cuisine types
- See the synthetic data used for RAG experiments

### Step 5: Run the Notebooks

Execute the ColBERT comparison notebooks in order:

```bash
# Navigate to the ColBERT notebooks directory
cd notebooks/ColBERT

# Run notebooks in this sequence:
# 1. Start Jupyter
jupyter notebook

# 2. Execute notebooks in order:
#    0-Exploratory Data Analysis.ipynb     - Explore the dataset
#    1-Setup-And-Configuration.ipynb       - Verify environment setup
#    2-Dense-Embeddings.ipynb              - Traditional dense retrieval baseline
#    3-ColBERT-Embeddings.ipynb            - Token-level ColBERT embeddings and comparison with Dense.
```

## 📁 Project Structure

```
advanced-rag-experimentation/
├── data/                    # Restaurant reviews dataset
│   ├── restaurant_reviews.csv
│   ├── simple_questions.json
│   └── complex_questions.json
├── notebooks/
│   └── ColBERT/            # Main comparison notebooks
├── annotation/             # Data viewer application
│   └── streamlit_app.py
├── research/               # Research papers and references
├── vector_store/           # LanceDB vector databases (created on run)
├── setup.py               # Core setup module for notebooks
├── .env.copy             # Environment template
└── pyproject.toml        # Project dependencies
```

## 🔑 Key Features

- **ColBERT vs Dense Retrieval**: Side-by-side comparison showing how token-level matching outperforms sentence-level embeddings
- **Real-world Queries**: Test with multi-constraint searches like "Italian budget-friendly outdoor seating"
- **Apple Silicon Support**: Optimized for M1/M2 Macs with MPS device detection

## 🎯 Example Queries to Try

After running notebooks 0-3, test these queries to see ColBERT's advantages:

- **Multi-constraint**: "Italian budget-friendly outdoor seating"
- **Contradictory**: "expensive but worth it fine dining"
- **Specific needs**: "laptop work wifi quiet productive"

- **Complex preferences**: "vegetarian sushi late night"

## 🛠️ Troubleshooting

### Environment Issues
- Make sure `.env` file exists and contains correct `PROJECT_ROOT` path
- Verify virtual environment is activated before installing packages
- Use `uv pip list` to check installed packages

### Notebook Issues
- Always run notebooks from 0 to 3 in sequence
- Each notebook builds on the previous one
- If you encounter device errors on Apple Silicon, models will automatically fall back to CPU

### Data Issues
- The synthetic data is already included in `data/` folder
- Use the Streamlit viewer to explore the dataset structure
- Vector store will be created automatically in `vector_store/` during notebook execution

## 📚 Technologies Used

- **PyLate**: ColBERT implementation for late interaction
- **LanceDB**: Vector database with multi-vector support
- **SentenceTransformers**: Dense embedding baseline
- **Streamlit**: Interactive data viewer
- **PyTorch**: Core ML framework with MPS/CUDA support

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This is an experimental repository for AI Tinkerers demonstrations. Feel free to explore and adapt for your own RAG experiments!