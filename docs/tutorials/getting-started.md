---
title: "Getting Started"
description: Install MDAN and build your first project
---

Build software faster using AI-powered workflows with specialized agents that guide you through planning, architecture, and implementation.

## What You'll Learn

- Install and initialize MDAN for a new project
- Use **MDAN-Help** — your intelligent guide that knows what to do next
- Choose the right planning track for your project size
- Progress through phases from requirements to working code
- Use agents and workflows effectively

:::note[Prerequisites]
- **Node.js 20+** — Required for the installer
- **Git** — Recommended for version control
- **AI-powered IDE** — Claude Code, Cursor, or similar
- **A project idea** — Even a simple one works for learning
:::

:::tip[The Easiest Path]
**Install** → `npx mdan install`
**Ask** → `/mdan-help what should I do first?`
**Build** → Let MDAN-Help guide you workflow by workflow
:::

## Meet MDAN-Help: Your Intelligent Guide

**MDAN-Help is the fastest way to get started with MDAN.** You don't need to memorize workflows or phases — just ask, and MDAN-Help will:

- **Inspect your project** to see what's already been done
- **Show your options** based on which modules you have installed
- **Recommend what's next** — including the first required task
- **Answer questions** like "I have a SaaS idea, where do I start?"

### How to Use MDAN-Help

Run it in your AI IDE with just the slash command:

```
/mdan-help
```

Or combine it with a question for context-aware guidance:

```
/mdan-help I have an idea for a SaaS product, I already know all the features I want. where do I get started?
```

MDAN-Help will respond with:
- What's recommended for your situation
- What the first required task is
- What the rest of the process looks like

### It Powers Workflows Too

MDAN-Help doesn't just answer questions — **it automatically runs at the end of every workflow** to tell you exactly what to do next. No guessing, no searching docs — just clear guidance on the next required workflow.

:::tip[Start Here]
After installing MDAN, run `/mdan-help` immediately. It will detect what modules you have installed and guide you to the right starting point for your project.
:::

## Understanding MDAN

MDAN helps you build software through guided workflows with specialized AI agents. The process follows four phases:

| Phase | Name           | What Happens                                        |
| ----- | -------------- | --------------------------------------------------- |
| 1     | Analysis       | Brainstorming, research, product brief *(optional)* |
| 2     | Planning       | Create requirements (PRD or tech-spec)              |
| 3     | Solutioning    | Design architecture *(MDAN Method/Enterprise only)* |
| 4     | Implementation | Build epic by epic, story by story                  |

**[Open the Workflow Map](../reference/workflow-map.md)** to explore phases, workflows, and context management.

Based on your project's complexity, MDAN offers three planning tracks:

| Track           | Best For                                               | Documents Created                      |
| --------------- | ------------------------------------------------------ | -------------------------------------- |
| **Quick Flow**  | Bug fixes, simple features, clear scope (1-15 stories) | Tech-spec only                         |
| **MDAN Method** | Products, platforms, complex features (10-50+ stories) | PRD + Architecture + UX                |
| **Enterprise**  | Compliance, multi-tenant systems (30+ stories)         | PRD + Architecture + Security + DevOps |

:::note
Story counts are guidance, not definitions. Choose your track based on planning needs, not story math.
:::

## Installation

### Install from npm (Recommended)

Open a terminal in your project directory and run:

```bash
npx mdan install
```

### Install from GitHub

Alternatively, clone the repository and install:

```bash
git clone https://github.com/khalilbenaz/MDANV2.git
cd MDANV2
npm install
npm link
```

When prompted to select modules, choose **MDAN Method**.

The installer creates two folders:
- `_.mdan/` — agents, workflows, tasks, and configuration
- `_mdan-output/` — empty for now, but this is where your artifacts will be saved

:::tip[Your Next Step]
Open your AI IDE in the project folder and run:

```
/mdan-help
```

MDAN-Help will detect what you've completed and recommend exactly what to do next. You can also ask it questions like "What are my options?" or "I have a SaaS idea, where should I start?"
:::

:::note[How to Load Agents and Run Workflows]
Each workflow has a **slash command** you run in your IDE (e.g., `/mdan-bmm-create-prd`). Running a workflow command automatically loads the appropriate agent — you don't need to load agents separately. You can also load an agent directly for general conversation (e.g., `/mdan-agent-bmm-pm` for the PM agent).
:::

:::caution[Fresh Chats]
Always start a fresh chat for each workflow. This prevents context limitations from causing issues.
:::

## Step 1: Create Your Plan

Work through phases 1-3. **Use fresh chats for each workflow.**

:::tip[Project Context (Optional)]
Before starting, consider creating `project-context.md` to document your technical preferences and implementation rules. This ensures all AI agents follow your conventions throughout the project.

Create it manually at `_mdan-output/project-context.md` or generate it after architecture using `/mdan-bmm-generate-project-context`. [Learn more](../explanation/project-context.md).
:::

### Phase 1: Analysis (Optional)

All workflows in this phase are optional:
- **brainstorming** (`/mdan-brainstorming`) — Guided ideation
- **research** (`/mdan-bmm-research`) — Market and technical research
- **create-product-brief** (`/mdan-bmm-create-product-brief`) — Recommended foundation document

### Phase 2: Planning (Required)

**For MDAN Method and Enterprise tracks:**
1. Load the **PM agent** (`/mdan-agent-bmm-pm`) in a new chat
2. Run the `prd` workflow (`/mdan-bmm-create-prd`)
3. Output: `PRD.md`

**For Quick Flow track:**
- Use the `quick-spec` workflow (`/mdan-bmm-quick-spec`) instead of PRD, then skip to implementation

:::note[UX Design (Optional)]
If your project has a user interface, load the **UX-Designer agent** (`/mdan-agent-bmm-ux-designer`) and run the UX design workflow (`/mdan-bmm-create-ux-design`) after creating your PRD.
:::

### Phase 3: Solutioning (MDAN Method/Enterprise)

**Create Architecture**
1. Load the **Architect agent** (`/mdan-agent-bmm-architect`) in a new chat
2. Run `create-architecture` (`/mdan-bmm-create-architecture`)
3. Output: Architecture document with technical decisions

**Create Epics and Stories**

:::tip[V6 Improvement]
Epics and stories are now created *after* architecture. This produces better quality stories because architecture decisions (database, API patterns, tech stack) directly affect how work should be broken down.
:::

1. Load the **PM agent** (`/mdan-agent-bmm-pm`) in a new chat
2. Run `create-epics-and-stories` (`/mdan-bmm-create-epics-and-stories`)
3. The workflow uses both PRD and Architecture to create technically-informed stories

**Implementation Readiness Check** *(Highly Recommended)*
1. Load the **Architect agent** (`/mdan-agent-bmm-architect`) in a new chat
2. Run `check-implementation-readiness` (`/mdan-bmm-check-implementation-readiness`)
3. Validates cohesion across all planning documents

## Step 2: Build Your Project

Once planning is complete, move to implementation. **Each workflow should run in a fresh chat.**

### Initialize Sprint Planning

Load the **SM agent** (`/mdan-agent-bmm-sm`) and run `sprint-planning` (`/mdan-bmm-sprint-planning`). This creates `sprint-status.yaml` to track all epics and stories.

### The Build Cycle

For each story, repeat this cycle with fresh chats:

| Step | Agent | Workflow       | Command                    | Purpose                            |
| ---- | ----- | -------------- | -------------------------- | ---------------------------------- |
| 1    | SM    | `create-story` | `/mdan-bmm-create-story`  | Create story file from epic        |
| 2    | DEV   | `dev-story`    | `/mdan-bmm-dev-story`     | Implement the story                |
| 3    | DEV   | `code-review`  | `/mdan-bmm-code-review`   | Quality validation *(recommended)* |

After completing all stories in an epic, load the **SM agent** (`/mdan-agent-bmm-sm`) and run `retrospective` (`/mdan-bmm-retrospective`).

## What You've Accomplished

You've learned the foundation of building with MDAN:

- Installed MDAN and configured it for your IDE
- Initialized a project with your chosen planning track
- Created planning documents (PRD, Architecture, Epics & Stories)
- Understood the build cycle for implementation

Your project now has:

```text
your-project/
├── _.mdan/                                   # MDAN configuration
├── _mdan-output/
│   ├── planning-artifacts/
│   │   ├── PRD.md                           # Your requirements document
│   │   ├── architecture.md                  # Technical decisions
│   │   └── epics/                           # Epic and story files
│   ├── implementation-artifacts/
│   │   └── sprint-status.yaml               # Sprint tracking
│   └── project-context.md                   # Implementation rules (optional)
└── ...
```

## Quick Reference

| Workflow                              | Command                                    | Agent     | Purpose                                         |
| ------------------------------------- | ------------------------------------------ | --------- | ----------------------------------------------- |
| **`help`** ⭐                         | `/mdan-help`                               | Any       | **Your intelligent guide — ask anything!**      |
| `prd`                                 | `/mdan-bmm-create-prd`                     | PM        | Create Product Requirements Document            |
| `create-architecture`                 | `/mdan-bmm-create-architecture`            | Architect | Create architecture document                     |
| `generate-project-context`            | `/mdan-bmm-generate-project-context`       | Analyst   | Create project context file                     |
| `create-epics-and-stories`       | `/mdan-bmm-create-epics-and-stories`       | PM        | Break down PRD into epics            |
| `check-implementation-readiness` | `/mdan-bmm-check-implementation-readiness` | Architect | Validate planning cohesion           |
| `sprint-planning`                | `/mdan-bmm-sprint-planning`                | SM        | Initialize sprint tracking           |
| `create-story`                   | `/mdan-bmm-create-story`                   | SM        | Create a story file                  |
| `dev-story`                      | `/mdan-bmm-dev-story`                      | DEV       | Implement a story                    |
| `code-review`                    | `/mdan-bmm-code-review`                    | DEV       | Review implemented code              |

## Common Questions

**Do I always need architecture?**
Only for MDAN Method and Enterprise tracks. Quick Flow skips from tech-spec to implementation.

**Can I change my plan later?**
Yes. The SM agent has a `correct-course` workflow (`/mdan-bmm-correct-course`) for handling scope changes.

**What if I want to brainstorm first?**
Load the Analyst agent (`/mdan-agent-bmm-analyst`) and run `brainstorming` (`/mdan-brainstorming`) before starting your PRD.

**Do I need to follow a strict order?**
Not strictly. Once you learn the flow, you can run workflows directly using the Quick Reference above.

## Getting Help

:::tip[First Stop: MDAN-Help]
**Run `/mdan-help` anytime** — it's the fastest way to get unstuck. Ask it anything:
- "What should I do after installing?"
- "I'm stuck on workflow X"
- "What are my options for Y?"
- "Show me what's been done so far"

MDAN-Help inspects your project, detects what you've completed, and tells you exactly what to do next.
:::

- **During workflows** — Agents guide you with questions and explanations
- **Community** — [Discord](https://discord.gg/gk8jAdXWmj) (#mdan-help, #report-bugs-and-issues)

## Key Takeaways

:::tip[Remember These]
- **Start with `/mdan-help`** — Your intelligent guide that knows your project and options
- **Always use fresh chats** — Start a new chat for each workflow
- **Track matters** — Quick Flow uses quick-spec; Method/Enterprise need PRD and architecture
- **MDAN-Help runs automatically** — Every workflow ends with guidance on what's next
:::

Ready to start? Install MDAN, run `/mdan-help`, and let your intelligent guide lead the way.
