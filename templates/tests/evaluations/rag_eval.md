# RAG Evaluation Template

> Benchmark RAG (Retrieval-Augmented Generation) correctness and quality

## Metadata

| Field | Value |
|-------|-------|
| eval_name | rag_correctness |
| version | 1.0.0 |
| metrics | F1 Score, Precision, Recall, Context Relevance |

## Purpose

Evaluate how well the RAG pipeline retrieves relevant context and generates accurate answers.

## Dataset Format

```json
[
  {
    "query": "What is the refund policy?",
    "expected_chunks": [
      "refund_policy.md: paragraphs 1-3",
      "faq.md: refund section"
    ],
    "expected_answer_contains": ["30 days", "original payment", "processing time"]
  }
]
```

## Evaluation Metrics

### Retrieval Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Recall | ≥0.85 | % of relevant chunks retrieved |
| Precision | ≥0.90 | % of retrieved chunks that are relevant |
| F1 Score | ≥0.87 | Harmonic mean of precision/recall |

### Generation Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Context Relevance | ≥0.80 | LLM judge scores context usefulness |
| Answer Accuracy | ≥0.85 | Answer contains expected information |
| Hallucination Rate | ≤0.05 | Facts not in context |

## Evaluation Code

### Python (LangWatch)

```python
import langwatch

results = langwatch.evaluate(
    dataset="customer-support-rag",
    evaluator="rag_correctness",
    metrics=["f1_score", "precision", "recall", "context_relevance"]
)

print(f"F1 Score: {results.f1_score}")
print(f"Precision: {results.precision}")
print(f"Recall: {results.recall}")
print(f"Context Relevance: {results.context_relevance}")
```

### JavaScript/TypeScript

```typescript
import { evaluate } from "@langwatch/evaluators";

const results = await evaluate({
  dataset: "customer-support-rag",
  evaluator: "rag_correctness",
  metrics: ["f1_score", "precision", "recall", "context_relevance"],
});

console.log(`F1 Score: ${results.f1Score}`);
```

## Pass/Fail Criteria

| Metric | Threshold | Status |
|--------|-----------|--------|
| F1 Score | ≥0.87 | ✅ Pass |
| F1 Score | 0.70-0.86 | ⚠️ Warning |
| F1 Score | <0.70 | ❌ Fail |
| Hallucination | ≤0.05 | ✅ Pass |
| Hallucination | >0.15 | ❌ Fail |

## Troubleshooting

### Low Recall
- Check chunk size (try 512-1024)
- Add more overlapping chunks
- Improve embedding model

### Low Precision
- Reduce chunk size
- Add more specific metadata filters
- Filter out irrelevant sources

### High Hallucination
- Add source citations to prompt
- Reduce max_tokens
- Use better context ranking

## Integration with MDAN

During VERIFY phase, Test Agent should:
1. Create RAG evaluation dataset from PRD
2. Run retrieval + generation tests
3. Report metrics in quality gate
4. Fail if thresholds not met
