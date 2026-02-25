# Context Save Format Specification

> MDAN-AUTO v1.0 Context Persistence Format

## Overview

Context saves are JSON files that capture the complete state of an MDAN-AUTO execution, enabling resumption after token limits or interruptions.

## File Location

```
/tmp/mdan-save-[timestamp].json
```

Example: `/tmp/mdan-save-1705310400.json`

## JSON Structure

```json
{
  "version": "1.0",
  "mode": "auto",
  "timestamp": "2024-01-15T10:23:45Z",
  "project": {
    "name": "MyProject",
    "description": "Project description",
    "tech_stack": {
      "language": "csharp",
      "framework": "dotnet",
      "ui": "blazor",
      "database": "sqlserver",
      "cloud": "azure"
    }
  },
  "phases": {
    "current": "IMPLEMENT",
    "completed": ["LOAD", "DISCOVER", "PLAN", "ARCHITECT"],
    "status": {
      "LOAD": "complete",
      "DISCOVER": "complete",
      "PLAN": "complete",
      "ARCHITECT": "complete",
      "IMPLEMENT": "in_progress",
      "TEST": "pending",
      "DEPLOY": "pending",
      "DOC": "pending"
    }
  },
  "context": {
    "token_usage": {
      "total": 102400,
      "limit": 128000,
      "percentage": 0.8
    },
    "conversation_history": [
      {
        "role": "system",
        "content": "System message",
        "timestamp": "2024-01-15T10:00:00Z"
      },
      {
        "role": "user",
        "content": "User message",
        "timestamp": "2024-01-15T10:00:01Z"
      },
      {
        "role": "assistant",
        "content": "Assistant response",
        "timestamp": "2024-01-15T10:00:05Z"
      }
    ],
    "artifacts": {
      "discover": {
        "file": "docs/discover.md",
        "content": "# Discover Phase\n\n..."
      },
      "plan": {
        "file": "docs/plan.md",
        "content": "# Plan\n\n#PHASE1\n..."
      },
      "architecture": {
        "file": "docs/architecture.md",
        "content": "# Architecture\n\n..."
      }
    },
    "decisions": [
      {
        "id": "decision-001",
        "topic": "Database Choice",
        "winner": "SQL Server",
        "rationale": "Azure integration and enterprise features",
        "timestamp": "2024-01-15T10:05:00Z"
      }
    ]
  },
  "debates": [
    {
      "id": "debate-001",
      "topic": "Architecture Pattern",
      "question": "Should we use monolith or microservices?",
      "participants": ["architect", "dev", "devops"],
      "arguments": {
        "architect": "Microservices for scalability",
        "dev": "Monolith for simplicity",
        "devops": "Microservices for deployment flexibility"
      },
      "winner": "architect",
      "rationale": "Project requires scalability",
      "timestamp": "2024-01-15T10:10:00Z"
    }
  ],
  "errors": [],
  "quality_gates": {
    "LOAD": true,
    "DISCOVER": true,
    "PLAN": true,
    "ARCHITECT": true,
    "IMPLEMENT": false,
    "TEST": false,
    "DEPLOY": false,
    "DOC": false
  },
  "configuration": {
    "token_limit": 128000,
    "save_threshold": 0.8,
    "output_dir": "./mdan-auto-output",
    "log_level": "INFO",
    "fail_fast": true,
    "debate_enabled": true
  },
  "metadata": {
    "created_at": "2024-01-15T10:00:00Z",
    "updated_at": "2024-01-15T10:23:45Z",
    "save_count": 1,
    "resume_count": 0
  }
}
```

## Field Descriptions

### Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Format version (always "1.0") |
| `mode` | string | Execution mode (always "auto") |
| `timestamp` | string | ISO 8601 timestamp of save |
| `project` | object | Project information |
| `phases` | object | Phase execution state |
| `context` | object | Execution context |
| `debates` | array | Debate history |
| `errors` | array | Error log |
| `quality_gates` | object | Quality gate status |
| `configuration` | object | Runtime configuration |
| `metadata` | object | Save metadata |

### Project Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Project name |
| `description` | string | Project description |
| `tech_stack` | object | Technology stack |

### Phases Object

| Field | Type | Description |
|-------|------|-------------|
| `current` | string | Currently executing phase |
| `completed` | array | List of completed phases |
| `status` | object | Status of each phase (pending/in_progress/complete/failed) |

### Context Object

| Field | Type | Description |
|-------|------|-------------|
| `token_usage` | object | Token usage statistics |
| `conversation_history` | array | LLM conversation history |
| `artifacts` | object | Generated artifacts |
| `decisions` | array | Decision history |

### Token Usage Object

| Field | Type | Description |
|-------|------|-------------|
| `total` | number | Total tokens used |
| `limit` | number | Token limit |
| `percentage` | number | Usage as decimal (0.0-1.0) |

### Conversation History Item

| Field | Type | Description |
|-------|------|-------------|
| `role` | string | Message role (system/user/assistant) |
| `content` | string | Message content |
| `timestamp` | string | ISO 8601 timestamp |

### Artifacts Object

| Field | Type | Description |
|-------|------|-------------|
| `[phase]` | object | Phase-specific artifacts |
| `file` | string | Artifact file path |
| `content` | string | Artifact content |

### Debate Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique debate ID |
| `topic` | string | Debate topic |
| `question` | string | Debate question |
| `participants` | array | Participating agents |
| `arguments` | object | Agent arguments |
| `winner` | string | Winning agent |
| `rationale` | string | Decision rationale |
| `timestamp` | string | ISO 8601 timestamp |

### Error Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique error ID |
| `phase` | string | Phase where error occurred |
| `message` | string | Error message |
| `stack_trace` | string | Stack trace (if available) |
| `timestamp` | string | ISO 8601 timestamp |
| `critical` | boolean | Whether error is critical |

### Quality Gates Object

| Field | Type | Description |
|-------|------|-------------|
| `[phase]` | boolean | Whether quality gate passed |

### Configuration Object

| Field | Type | Description |
|-------|------|-------------|
| `token_limit` | number | Token limit |
| `save_threshold` | number | Save threshold (0.0-1.0) |
| `output_dir` | string | Output directory |
| `log_level` | string | Log level |
| `fail_fast` | boolean | Fail-fast enabled |
| `debate_enabled` | boolean | Debate enabled |

### Metadata Object

| Field | Type | Description |
|-------|------|-------------|
| `created_at` | string | Creation timestamp |
| `updated_at` | string | Last update timestamp |
| `save_count` | number | Number of saves |
| `resume_count` | number | Number of resumes |

## Save Triggers

Context is saved when:

1. Token usage ≥ 80% of limit
2. Before critical operations
3. On phase completion
4. On error (before abort)
5. Manual save command

## Resume Process

When resuming from save:

1. Load save file
2. Validate version compatibility
3. Restore conversation history
4. Restore artifacts
5. Resume from `phases.current`
6. Increment `metadata.resume_count`

## Validation

Save files must be valid JSON with all required fields. Missing or invalid fields should trigger a warning and use defaults.

## Compression

For large saves (>1MB), consider using gzip compression:

```
/tmp/mdan-save-[timestamp].json.gz
```

## Security

- Never save sensitive data (API keys, passwords, tokens)
- Sanitize conversation history before saving
- Use secure file permissions (0600)
- Delete old saves after successful completion

## Version Compatibility

| Version | Changes |
|---------|---------|
| 1.0 | Initial version |

## Example Usage

```python
import json
from datetime import datetime

def save_context(state):
    timestamp = int(datetime.now().timestamp())
    filename = f"/tmp/mdan-save-{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(state, f, indent=2)

    print(f"CONTEXT SAVE {filename}")

def load_context(filename):
    with open(filename, 'r') as f:
        state = json.load(f)

    state['metadata']['resume_count'] += 1
    return state
```

## Version

MDAN-AUTO Context Save Format v1.0