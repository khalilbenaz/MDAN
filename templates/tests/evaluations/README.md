# Test Evaluations Index

> Structured benchmarking for agent components

## Overview

Evaluations provide quantitative testing for specific components of your agent pipeline. Unlike scenarios (end-to-end), evaluations test isolated components.

## Available Evaluations

| Evaluation | Description | Metrics |
|------------|-------------|---------|
| [rag_eval.md](rag_eval.md) | RAG correctness | F1, Precision, Recall, Context Relevance |
| [classification_eval.md](classification_eval.md) | Routing/categorization | Accuracy, F1, Precision, Recall |

## Adding New Evaluations

1. Copy an existing template:
   ```bash
   cp rag_eval.md my_eval.md
   ```

2. Customize:
   - Update dataset format
   - Set target thresholds
   - Add domain-specific checks

3. Run:
   ```python
   import langwatch
   results = langwatch.evaluate(
       dataset="my-dataset",
       evaluator="my_eval",
       metrics=["accuracy", "f1"]
   )
   ```

## Built-in Evaluators

LangWatch provides extensive evaluators:

| Evaluator | Description |
|-----------|-------------|
| `rag_correctness` | Retrieval and generation quality |
| `classification_accuracy` | Routing and categorization |
| `answer_correctness` | Factual accuracy |
| `safety_check` | Jailbreak, PII, toxicity |
| `format_validation` | JSON, XML, markdown structure |
| `tool_calling` | Correct tool selection and args |
| `latency` | Response time benchmarking |

## Running Evaluations

```bash
# Python
pytest tests/evaluations/ -v

# JavaScript
npm test -- tests/evaluations/

# With LangWatch
langwatch evaluate --dataset my-project
```

## Integration with MDAN

During VERIFY phase:
1. Test Agent identifies components needing evaluation
2. Creates evaluation datasets from PRD/user stories
3. Runs relevant evaluations
4. Reports metrics in quality gate
5. Fails if thresholds not met

## Best Practices

- Create evaluation datasets from real user queries
- Include edge cases and negative examples
- Set realistic thresholds (not 100%)
- Track metrics over time (regression detection)
- Run evaluations in CI/CD pipeline
