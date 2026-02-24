# Contributing to MDAN

Thank you for your interest in contributing to MDAN!

## Quick Links

- **[Developer Guide (FR)](docs/fr/CONTRIBUTING-DEV.md)** — Guide complet pour développer sur MDAN
- **[Architecture](ARCHITECTURE.md)** — Documentation technique de l'architecture

## How to Contribute

### Improving Agent Prompts

Agent prompts are in `/agents/`. If you find that an agent produces better results with a modified prompt, open a PR with:
- The modified agent file
- An example showing the improvement (input → output comparison)
- Updated version number following [versioning rules](docs/fr/CONTRIBUTING-DEV.md#règles-de-versioning)

### Adding LLM Integrations

New LLM integration guides go in `/integrations/`. Follow the format of existing files.

### Improving Templates

Templates are in `/templates/`. Improvements that make templates more complete or easier to use are welcome.

### Adding Skills

Skills are optional, modular capabilities in `/skills/`. See [Creating a Skill](docs/fr/CONTRIBUTING-DEV.md#créer-un-skill) for the complete guide.

### Reporting Issues

If an agent produces consistently poor results on a specific type of task, open an issue with:
- Which agent
- What type of task
- Example input
- Actual output
- Expected output

## Development Setup

```bash
git clone https://github.com/khalilbenaz/MDAN.git
cd MDAN
npm link  # Install CLI globally for testing
mdan help
```

See [CONTRIBUTING-DEV.md](docs/fr/CONTRIBUTING-DEV.md) for detailed setup instructions.

## Guidelines

- Keep agent prompts focused — resist adding responsibilities to agents
- Document every change with a rationale
- Test with at least 2 different LLMs before submitting
- Keep the bilingual (EN/FR) principle — major changes should be reflected in both languages
- Follow the [versioning rules](docs/fr/CONTRIBUTING-DEV.md#règles-de-versioning)

## Code of Conduct

Be constructive. MDAN is a method, not a product — there are many valid ways to improve it.
