# Classification Evaluation Template

> Benchmark routing accuracy and categorization correctness

## Metadata

| Field | Value |
|-------|-------|
| eval_name | classification_accuracy |
| version | 1.0.0 |
| metrics | Accuracy, Precision, Recall, F1 Score |

## Purpose

Evaluate how well the agent correctly routes requests, categorizes inputs, or makes routing decisions.

## Use Cases

- Intent classification (chatbot routing)
- Content moderation
- Priority/ticket categorization
- Language detection
- Sentiment analysis

## Dataset Format

```json
[
  {
    "input": "I want to get a refund",
    "expected_category": "refund_request",
    "expected_confidence": 0.90
  },
  {
    "input": "How do I change my password?",
    "expected_category": "account_settings",
    "expected_confidence": 0.85
  }
]
```

## Evaluation Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Accuracy | ≥0.95 | % of correct classifications |
| Macro F1 | ≥0.90 | F1 averaged across all categories |
| Precision (per class) | ≥0.85 | True positives / predicted positives |
| Recall (per class) | ≥0.85 | True positives / actual positives |
| Confidence Calibration | ≤0.10 | Mean absolute error between confidence and accuracy |

## Evaluation Code

### Python (LangWatch)

```python
import langwatch

results = langwatch.evaluate(
    dataset="intent-classification",
    evaluator="classification_accuracy",
    metrics=["accuracy", "precision", "recall", "f1_macro", "calibration"]
)

print(f"Accuracy: {results.accuracy}")
print(f"Macro F1: {results.f1_macro}")
print(f"Precision: {results.precision}")
print(f"Recall: {results.recall}")
```

### JavaScript/TypeScript

```typescript
import { evaluate } from "@langwatch/evaluators";

const results = await evaluate({
  dataset: "intent-classification",
  evaluator: "classification_accuracy",
  metrics: ["accuracy", "precision", "recall", "f1_macro"],
});

console.log(`Accuracy: ${results.accuracy}`);
```

## Pass/Fail Criteria

| Metric | Threshold | Status |
|--------|-----------|--------|
| Accuracy | ≥0.95 | ✅ Pass |
| Accuracy | 0.90-0.94 | ⚠️ Warning |
| Accuracy | <0.90 | ❌ Fail |
| Macro F1 | ≥0.90 | ✅ Pass |
| Macro F1 | <0.85 | ❌ Fail |
| Confidence Error | ≤0.10 | ✅ Pass |
| Confidence Error | >0.15 | ⚠️ Warning |

## Per-Class Analysis

Generate confusion matrix:

|  | Predicted A | Predicted B | Predicted C |
|--|-------------|-------------|-------------|
| Actual A | 45 | 3 | 2 |
| Actual B | 5 | 38 | 7 |
| Actual C | 1 | 4 | 40 |

Identify:
- **High-confusion pairs**: A↔B need better differentiation
- **Low-recall classes**: More training data needed
- **Low-precision classes**: Overlapping with other categories

## Common Issues

### Low Precision (many false positives)
- Add negative examples
- Make categories more distinct
- Add disambiguation prompts

### Low Recall (many false negatives)
- Add more training data
- Expand category definitions
- Check for data quality issues

### Poor Calibration
- Retrain with temperature scaling
- Add more diverse examples
- Use calibration-aware loss

## Integration with MDAN

During VERIFY phase, Test Agent should:
1. Identify all classification/routing points in the system
2. Create evaluation datasets from real user queries
3. Run classification evaluation
4. Report per-class performance
5. Fail if overall accuracy < 90%
