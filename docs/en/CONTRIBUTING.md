# Contributing to MDAN

Thank you for your interest in contributing to MDAN!

## How to Contribute

### Improving Agent Prompts

Agent prompts are in `/agents/`. If you find that an agent produces better results with a modified prompt, open a PR with:
- The modified agent file
- An example showing the improvement (input → output comparison)

### Adding LLM Integrations

New LLM integration guides go in `/integrations/`. Follow the format of existing files.

### Improving Templates

Templates are in `/templates/`. Improvements that make templates more complete or easier to use are welcome.

### Reporting Issues

If an agent produces consistently poor results on a specific type of task, open an issue with:
- Which agent
- What type of task
- Example input
- Actual output
- Expected output

## Guidelines

- Keep agent prompts focused — resist adding responsibilities to agents
- Document every change with a rationale
- Test with at least 2 different LLMs before submitting
- Keep the bilingual (EN/FR) principle — major changes should be reflected in both languages

## Code of Conduct

Be constructive. MDAN is a method, not a product — there are many valid ways to improve it.
