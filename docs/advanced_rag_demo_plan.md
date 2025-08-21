# Advanced RAG Demo Plan - AI Tinkerers Talk
## 80/20 Concepts for Maximum Impact

---

## 🎯 Core Message
**"Stop squeezing everything into one vector - use smarter retrieval"**

---

## 📋 Demo Flow (30 minutes)

### Part 1: The Problem (5 min)
#### **Demo: Why Single Vectors Fail**
```python
# Live failure case
query = "Find papers about transformers that use metaphors in titles"
# Show traditional RAG missing nuanced requirements
```

**Visual**: Side-by-side comparison
- ❌ Dense retrieval: Returns any transformer paper
- ✅ Advanced RAG: Returns "Attention is All You Need" (metaphor!)

**Key Insight**: Information bottleneck - pooling loses critical details

---

### Part 2: Late Interaction - Token-Level Magic (10 min)
#### **Demo: ColBERT with PyLate**

```python
from pylate import models
import torch

# Load pre-trained model
model = models.ColBERT.from_pretrained("lightonai/colbertv2.0")

# Show token-level matching
query_tokens = model.encode_queries(["machine learning breakthrough"])
doc_tokens = model.encode_documents(["Deep learning achieves new milestone"])

# Visualize MaxSim scores
similarity_matrix = compute_maxsim(query_tokens, doc_tokens)
# Show heatmap - which tokens actually match!
```

**Key Points**:
- 150M parameter model beats 7B models on reasoning
- **Live visualization**: Token similarity heatmap
- **Interpretability win**: See exactly why documents match

**Practical Insight**: "It's like having keyword search with semantic understanding"

---

### Part 3: Multiple Representations (10 min)
#### **Demo: One Document, Many Maps**

```python
# Same financial document, 3 representations
document = load_financial_report()

representations = {
    "summary": generate_summary(document),      # For high-level queries
    "tables": extract_tables(document),         # For data queries  
    "entities": extract_entities(document),     # For specific names/numbers
}

# Smart routing based on query type
def route_query(query):
    if "data" in query or "numbers" in query:
        return search(representations["tables"])
    elif "company" in query or "CEO" in query:
        return search(representations["entities"])
    else:
        return search(representations["summary"])
```

**Visual Demo**:
1. Query: "What was the Q3 revenue?" → Routes to tables
2. Query: "Who is the CEO?" → Routes to entities
3. Query: "Overall company strategy?" → Routes to summary

**Key Metaphor**: "The map is not the territory - make multiple maps!"

---

### Part 4: Instruction-Following Retrieval (5 min)
#### **Quick Promptriever Concept Demo**

```python
# Same query, different instructions
base_query = "machine learning papers"

# Instruction 1: Academic focus
results_1 = retriever.search(
    query=base_query,
    instruction="Find seminal, highly-cited foundational papers"
)

# Instruction 2: Practical focus  
results_2 = retriever.search(
    query=base_query,
    instruction="Find recent implementation tutorials with code"
)

# Show completely different results!
```

**Impact**: Zero-shot hyperparameter tuning via natural language

---

## 🛠️ Practical Implementation Recipe (5 min)

### The 80/20 Stack for Production

```python
# 1. Start with hybrid search (immediate win)
from rank_bm25 import BM25Okapi
results = combine_results(
    bm25_search(query),     # Catches exact matches
    dense_search(query)      # Catches semantic matches
)

# 2. Add late interaction for complex queries
from pylate import models
colbert = models.ColBERT.from_pretrained("lightonai/colbertv2.0")
# Use for queries with multiple constraints

# 3. Create 2-3 representations of critical docs
representations = {
    "technical": technical_description,
    "simple": eli5_explanation,
    "metadata": extract_metadata
}

# 4. Simple routing (no complex agents needed)
if query_is_technical():
    search(representations["technical"])
else:
    search(representations["simple"])
```

---

## 💡 One-Slide Takeaway

```
Traditional RAG:
Query → Single Vector → Results ❌

Advanced RAG:
Query → Router → Multiple Representations
           ↓
    Token-Level Matching (ColBERT)
           ↓
    Instruction-Aware Retrieval
           ↓
    Better Results ✅
```

---

## 🎬 Live Coding Focus

### Option A: ColBERT Demo (Recommended)
- **Setup**: pip install pylate
- **Dataset**: 10 research papers (mix of relevant/irrelevant)
- **Query**: Complex multi-constraint query
- **Wow moment**: Visualize token heatmap showing why it matched

### Option B: Multiple Representations
- **Setup**: Single document (e.g., research paper)
- **Create**: 3 different representations
- **Demo**: Show how different queries route to different representations
- **Wow moment**: Same doc, completely different retrieval based on query

---

## 🎤 Key Talking Points

1. **"Pooling is the enemy"** - Information loss from compression
2. **"BM25 still wins sometimes"** - Because it doesn't compress!
3. **"Make multiple maps"** - Different representations for different needs
4. **"Let models think"** - Reasoning during retrieval, not just after

---

## 📊 Metrics to Show

- ColBERT: **+37% performance** on reasoning tasks vs dense
- Storage tradeoff: **~10x more space** but **worth it for accuracy**
- Latency: ColBERT adds **~50ms** vs dense (acceptable for most use cases)

---

## 🔗 Resources for Attendees

```python
# Quick start code
pip install pylate ragatouille

# Models to try
"lightonai/colbertv2.0"
"colbert-ir/colbertv2.0"

# Benchmarks to test on
- BRIGHT (reasoning)
- LongEmbed (long context)
- FollowIR (instruction following)
```

---

## ⚡ Backup Plans

1. **If live coding fails**: Pre-recorded notebook with outputs
2. **If visualization breaks**: Static heatmap images ready
3. **If time runs short**: Skip instruction-following, focus on ColBERT

---

## 🎯 Success Metrics

Attendees should leave knowing:
1. Why single vectors fail for complex queries
2. How to implement ColBERT with PyLate/RAGatouille
3. When to create multiple representations
4. One concrete improvement they can make tomorrow

---

## 📝 Notes
- Keep energy high during demos
- Use real examples (not toy data)
- Show failures first, then solutions
- End with "you can do this today"