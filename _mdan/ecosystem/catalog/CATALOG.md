# Component Catalog — 1,053 Skills | 418 Agents | 340 Commands | 67 Hooks | 67 Settings | 69 MCPs

This catalog indexes ALL installed components. Use it to find the right tool for any task.

## How to use components

- **Skills**: `Skill(skill: "skill-name")` — specialized prompts activated via the Skill tool
- **Agents**: Read `~/.claude/agents/{category}/{name}.md` then use `Agent` tool with the agent's instructions
- **Commands**: Read `~/.claude/commands/{category}/{name}.md` then execute the described workflow
- **Hooks**: Copy JSON from `~/.claude/hooks/aitmpl/{category}/{name}.json` into settings.json hooks section
- **Settings**: Merge JSON from `~/.claude/settings-templates/{category}/{name}.json` into settings.json
- **MCPs**: Merge JSON from `~/.claude/mcp-templates/{category}/{name}.json` into settings.json mcpServers

---

## SKILLS (1,053) — Invoke via `Skill(skill: "name")`

### AI & ML (130+)
agents-autogpt, agents-crewai, agents-langchain, agents-llamaindex, ai-agent-builder, ai-agents-architect, ai-product, ai-workflow-orchestrator, ai-wrapper-product, anomaly-detection-builder, autonomous-agent-patterns, autonomous-agents, behavioral-modes, claude-api, claude-code-guide, claude-opus-4-5-migration, computer-use-agents, computer-vision-guide, context-window-management, conversation-memory, data-processing-nemo-curator, data-processing-ray-data, dataset-builder, deep-research-notebooklm, distributed-training-accelerate, distributed-training-deepspeed, distributed-training-megatron-core, distributed-training-pytorch-fsdp, distributed-training-pytorch-lightning, distributed-training-ray-train, emerging-techniques-knowledge-distillation, emerging-techniques-long-context, emerging-techniques-model-merging, emerging-techniques-model-pruning, emerging-techniques-moe-training, emerging-techniques-speculative-decoding, evaluation-bigcode-evaluation-harness, evaluation-lm-evaluation-harness, evaluation-nemo-evaluator, feature-engineering-guide, fine-tuning-axolotl, fine-tuning-llama-factory, fine-tuning-peft, fine-tuning-unsloth, inference-serving-llama-cpp, inference-serving-sglang, inference-serving-tensorrt-llm, inference-serving-vllm, langfuse, langgraph, llm-app-patterns, llm-integration-guide, mechanistic-interpretability-nnsight, mechanistic-interpretability-pyvene, mechanistic-interpretability-saelens, mechanistic-interpretability-transformer-lens, ml-experiment-tracker, ml-model-deployer, ml-paper-writing, mlops-mlflow, mlops-tensorboard, mlops-weights-and-biases, model-architecture-litgpt, model-architecture-mamba, model-architecture-nanogpt, model-architecture-rwkv, model-architecture-torchtitan, model-fine-tuner, model-optimization-guide, multimodal-audiocraft, multimodal-blip-2, multimodal-clip, multimodal-llava, multimodal-segment-anything, multimodal-stable-diffusion, multimodal-whisper, nlp-pipeline-designer, observability-langsmith, observability-phoenix, optimization-awq, optimization-bitsandbytes, optimization-flash-attention, optimization-gguf, optimization-gptq, optimization-hqq, parallel-agents, post-training-grpo-rl-training, post-training-miles, post-training-openrlhf, post-training-simpo, post-training-slime, post-training-torchforge, post-training-trl-fine-tuning, post-training-verl, prompt-caching, prompt-engineer, prompt-engineering, prompt-engineering-dspy, prompt-engineering-guidance, prompt-engineering-instructor, prompt-engineering-outlines, prompt-engineering-pro, prompt-library, prompt-master, prompt-optimizer, rag-chroma, rag-engineer, rag-faiss, rag-implementation, rag-pinecone, rag-pipeline-designer, rag-qdrant, rag-sentence-transformers, safety-alignment-constitutional-ai, safety-alignment-llamaguard, safety-alignment-nemo-guardrails, tokenization-huggingface-tokenizers, tokenization-sentencepiece, transformers

### Agent Architecture (50+)
agent-conflict-resolver, agent-consensus-builder, agent-context-manager, agent-cost-optimizer, agent-deployment-guide, agent-development, agent-evaluation, agent-evaluation-framework, agent-handoff-designer, agent-hierarchy-designer, agent-load-balancer, agent-management, agent-manager-skill, agent-marketplace-creator, agent-md-refactor, agent-memory-designer, agent-memory-mcp, agent-memory-systems, agent-message-protocol, agent-messaging, agent-monitoring-setup, agent-observability, agent-pipeline-composer, agent-pool-manager, agent-prompt-tuner, agent-result-aggregator, agent-retry-strategist, agent-security-hardener, agent-spawner, agent-state-synchronizer, agent-supervisor-builder, agent-task-decomposer, agent-testing-framework, agent-tool-builder, autogen-guide, coding-agent-builder, crewai, crewai-expert, customer-support-agent, data-analyst-agent, human-in-the-loop-designer, langgraph-designer, multi-agent-orchestrator, openai-assistants-builder, research-agent-designer, sales-agent-builder, semantic-kernel-guide, subagent-delegator, tool-calling-architect, voice-agent-builder

### Web Development (80+)
angular-guide, api-patterns, astro (via skills), bun-development, clerk-auth, cloudflare-deploy, core-components, core-web-vitals, css-layout-solver, design-system-starter, design-to-code, django-guide, exa-search, express-guide, fastapi-guide, fastmcp-server, firebase, frontend-design, frontend-dev-guidelines, graphql, graphql-builder, hubspot-integration, i18n-localization, inngest, javascript-mastery, laravel-guide, mcp-builder, mcp-server-builder, micro-saas-launcher, mui, nestjs-guide, netlify-deploy, nextjs-best-practices, nextjs-guide, nextjs-supabase-auth, nginx-configurator, nodejs-best-practices, openapi-contract-first, openapi-to-typescript, plaid-fintech, playwright, playwright-browser-automation, playwright-e2e-builder, playwright-skill, prisma-expert, react-best-practices, react-component-builder, react-dev, react-native-guide, react-patterns, react-ui-patterns, react-useeffect, remotion, remotion-best-practices, render-deploy, responsive-design-helper, rest-api-designer, salesforce-development, scroll-experience, segment-cdp, seo, seo-audit, seo-fundamentals, seo-optimizer, shopify-apps, shopify-development, stripe-integration, svelte-guide, tailwind-expert, tailwind-patterns, tavily-web, trigger-dev, typescript-expert, typescript-mastery, upstash-qstash, vercel-deploy, vercel-deployment, vue-guide, web-performance-optimizer, web-quality-audit, websocket-designer

### Backend & Infrastructure (60+)
api-security-hardener, aws-architect, aws-serverless, azure-cloud-advisor, azure-functions, azure-functions-expert, backend-dev-guidelines, bullmq-specialist, caching-strategy, cicd-pipeline-builder, clean-architecture-guide, cloud-cost-optimizer, cloud-migration-planner, cloud-security-guide, database-design, database-design-advisor, database-migration-helper, database-query-optimizer, database-schema-designer, deployment-procedures, devops-iac-engineer, docker-composer, docker-expert, docker-swarm-guide, dotnet-aspire-guide, dotnet-csharp-advisor, event-driven-architect, gcp-cloud-run, gcp-guide, go-concurrency-guide, grpc-service-designer, hangfire-job-scheduler, health-check-monitor, helm-chart-builder, infrastructure-as-code, infrastructure-lambda-labs, infrastructure-modal, infrastructure-skypilot, java-spring-advisor, kafka-patterns, kong-api-gateway, kubernetes-helper, message-queue-architect, microservices-designer, monitoring-setup, neon-postgres, nosql-expert, oauth2-oidc-advisor, ocelot-gateway-guide, outbox-pattern-guide, postgres-best-practices, postgres-expert, prometheus-grafana-setup, rabbitmq-patterns-guide, rate-limiter-designer, redis-patterns, rust-guide, scalability-planner, server-management, serverless-designer, sqlite-guide, supabase-postgres-best-practices, terraform-guide, yarp-gateway-designer

### Database (20+)
cassandra-guide, dimensional-modeling, dynamodb-guide, elasticsearch-guide, mongodb-guide, mysql-tuner, neon-instagres, postgres-expert, redis-patterns, sql-advanced-analytics, sql-server-tuner, sqlite-guide, database-query-subagent

### Security & Pentesting (40+)
active-directory-attacks, api-fuzzing-bug-bounty, api-security-best-practices, aws-penetration-testing, broken-authentication, burp-suite-testing, cloud-penetration-testing, compliance-checker, dependency-audit, ethical-hacking-methodology, file-path-traversal, fintech-compliance-checker, gdpr-checklist, html-injection-testing, idor-testing, incident-response-plan, linux-privilege-escalation, metasploit-framework, network-101, owasp-checker, pentest-assistant, pentest-checklist, pentest-commands, privilege-escalation-methods, red-team-tactics, red-team-tools, scanning-tools, secrets-scanner, security-audit-automation, security-auditor, security-best-practices, security-compliance, security-ownership-map, security-threat-model, shodan-reconnaissance, smart-contract-auditor, smtp-penetration-testing, sql-injection-testing, sqlmap-database-pentesting, ssh-penetration-testing, supply-chain-guard, threat-modeling, top-web-vulnerabilities, vulnerability-analyzer, vulnerability-scanner, windows-privilege-escalation, wordpress-penetration-testing, wireshark-analysis, xss-html-injection

### Scientific & Bioinformatics (126)
alphafold-database, anndata, arboreto, astropy, benchling-integration, biomni, biopython, biorxiv-database, bioservices, brenda-database, cellxgene-census, chembl-database, cirq, citation-management, clinical-decision-support, clinical-reports, clinicaltrials-database, clinpgx-database, clinvar-database, cobrapy, cosmic-database, datacommons-client, datamol, dask, deepchem, deeptools, diffdock, dnanexus-integration, drugbank-database, ena-database, ensembl-database, esm, etetoolkit, fda-database, flowio, fluidsim, gene-database, geo-database, geopandas, gget, gtars, gwas-database, histolab, hmdb-database, hypogenic, hypothesis-generation, kegg-database, labarchive-integration, lamindb, latchbio-integration, latex-posters, literature-review, matchms, matplotlib, medchem, metabolomics-workbench-database, neurokit2, neuropixels-analysis, networkx, omero-integration, openalex-database, opentargets-database, opentrons-integration, pathml, pdb-database, peer-review, pennylane, polars, protocolsio-integration, pubchem-database, pubmed-database, pufferlib, pydeseq2, pydicom, pyhealth, pylabrobot, pymatgen, pymc, pymoo, pyopenms, pysam, pytdc, qiskit, qutip, rdkit, reactome-database, research-engineer, research-grants, scanpy, scikit-bio, scikit-learn, scikit-survival, scientific-brainstorming, scientific-critical-thinking, scientific-schematics, scientific-slides, scientific-visualization, scientific-writing, scvi-tools, seaborn, shap, simpy, stable-baselines3, statistical-analysis, statsmodels, string-database, sympy, torch_geometric, torchdrug, transformers, umap-learn, uniprot-database, uspto-database, vaex, venue-templates, zarr-python, zinc-database

### Document Processing (15+)
doc, docx, docx-official, excel-analysis, json-canvas, markitdown, obsidian-bases, obsidian-clipper-template-creator, obsidian-markdown, pdf, pdf-anthropic, pdf-official, pdf-processing, pdf-processing-pro, pptx, pptx-official, pptx-posters, spreadsheet, xlsx, xlsx-official

### DevOps & CI/CD (30+)
ansible-playbook-builder, argocd-guide, azure-devops-pipeline-advisor, cicd-pipeline-builder, cloudflare-deploy, docker-composer, docker-expert, docker-swarm-guide, github-actions-expert, github-workflow-automation, gitlab-ci-guide, helm-chart-builder, kubernetes-helper, monitoring-setup, nginx-configurator, prometheus-grafana-setup, terraform-guide

### Design UI/UX (15+)
accessibility-checker, css-layout-solver, design-critique, design-mirror, design-system-starter, design-to-code, excalidraw, figma, figma-implement-design, mermaid-diagrams, pencil, pencil-ui-designer, pixel-art-advisor, responsive-design-helper, ui-design-system-builder, ui-ux-pro-max, user-flow-designer, ux-research-guide, web-design-guidelines, wireframe-advisor

### Productivity & Business (40+)
agile-product-owner, brainstorming, budget-tracker, career-transition-planner, ceo-advisor, content-creator, content-repurposer, copywriting-assistant, cto-advisor, cv-builder, daily-meeting-update, deadline-prep, decision-matrix, email-drafter, email-sequence, email-systems, expense-analyzer, feature-design-assistant, file-organizer, habit-tracker, interview-prep, investment-journal, invoice-organizer, kaizen, learning-roadmap, linkedin-optimizer, meeting-insights-analyzer, meeting-summarizer, networking-script, notion-knowledge-capture, notion-meeting-intelligence, notion-research-documentation, notion-spec-to-implementation, product-manager-toolkit, product-strategist, project-estimation-helper, project-kickstart, salary-negotiation, savings-goal-planner, session-handoff, weekly-planner

### Marketing & Growth (25+)
ab-test-setup, analytics-tracking, app-store-optimization, competitive-ads-extractor, competitor-alternatives, content-research-writer, email-marketing-designer, executing-marketing-campaigns, form-cro, free-tool-strategy, geo-fundamentals, growth-hacking-strategist, launch-strategy, lead-research-assistant, marketing-demand-acquisition, marketing-ideas, marketing-psychology, marketing-strategy-pmm, onboarding-cro, page-cro, paid-ads, popup-cro, programmatic-seo, referral-program, schema-markup, seo-optimizer, signup-flow-cro, social-media-strategist, x-twitter-scraper

### Health & Wellness (20+)
allergy-reaction-log, blood-pressure-log, breathing-exercise-guide, chronic-illness-dashboard, diet-trigger-journal, doctor-visit-prep, emotional-checkin, health-question-builder, lab-explainer, med-side-effect-mood-log, medical-history-summary, medical-research-safe, medication-schedule, pain-journal, post-surgery-tracker, red-flag-checker, sleep-journal, supplement-checker, symptom-tracker

### Psychology (10+)
addiction-awareness-log, anxiety-debrief, boundary-setter, burnout-assessment, cbt-thought-record, crisis-escalation, grief-support, psychiatry-visit-prep, psychology-visit-prep, therapy-journal

### Game Development (15+)
2d-games, 3d-games, game-art, game-audio, game-design, game-design-patterns, game-development, mobile-games, multiplayer, pc-games, pixel-art-advisor, unity-game-helper, vr-ar, web-games

### Communication & Bots (15+)
discord-bot-architect, email-agent-builder, internal-comms, professional-communication, slack-bot-builder, slack-gif-creator, telegram-bot-builder, telegram-mini-app, voice-agent-builder, voice-agents, voice-ai-development

### Compliance & Regulatory (15+)
capa-officer, compliance-checker, data-privacy-compliance, fda-consultant-specialist, fintech-compliance-checker, gdpr-checklist, gdpr-dsgvo-expert, information-security-manager-iso27001, isms-audit-expert, mdr-745-specialist, quality-documentation-manager, quality-manager-qmr, quality-manager-qms-iso13485, regulatory-affairs-head, risk-management-specialist

---

## AGENTS (418) — Read from `~/.claude/agents/{category}/{name}.md`

| Category | Agents |
|----------|--------|
| ai-specialists (8) | ai-ethics-advisor, hackathon-ai-strategist, llm-architect, llms-maintainer, model-evaluator, prompt-engineer, search-specialist, task-decomposition-expert |
| api-graphql (8) | Thinking-Beast-Mode, api-architect, api-designer, graphql-architect, graphql-performance-optimizer, graphql-security-specialist, octopus-deploy-release-notes-mcp, shopify-expert |
| blockchain-web3 (4) | blockchain-developer, smart-contract-auditor, smart-contract-specialist, web3-integration-specialist |
| business-marketing (22) | business-analyst, communication-excellence-coach, competitive-analyst, content-marketer, customer-success-manager, customer-support, legal-advisor, market-researcher, marketing-attribution-analyst, payment-integration, product-manager, product-strategist, project-manager, risk-manager, sales-automator, sales-engineer, salesforce-expert, scrum-master, seo-specialist, trend-analyst, ux-researcher |
| data-ai (40) | adr-generator, ai-engineer, blueprint-mode, computer-vision-engineer, data-analyst, data-engineer, data-scientist, machine-learning-engineer, ml-engineer, mlops-engineer, nlp-engineer, postgresql-dba, prompt-builder, prompt-engineer, quant-analyst, semantic-kernel-dotnet, tdd-green, tdd-red... |
| database (11) | database-admin, database-architect, database-optimization, neon-auth-specialist, neon-database-architect, neon-expert, nosql-specialist, postgres-pro, supabase-schema-architect |
| deep-research-team (16) | academic-researcher, competitive-intelligence-analyst, data-analyst, fact-checker, research-coordinator, research-orchestrator, research-synthesizer, technical-researcher... |
| development-team (17) | backend-architect, backend-developer, code-architect, code-explorer, devops-engineer, frontend-developer, fullstack-developer, ios-developer, mobile-developer, test-generator, test-runner, ui-designer... |
| development-tools (34) | accessibility-tester, architect-reviewer, build-engineer, chaos-engineer, cli-developer, code-reviewer, codebase-explorer, debugger, dependency-manager, dx-optimizer, mcp-expert, performance-engineer, playwright-tester, qa-expert, refactoring-specialist, test-automator, test-engineer... |
| devops-infrastructure (39) | azure-infra-engineer, azure-principal-architect, bicep-implement, cloud-architect, deployment-engineer, devops-engineer, devops-expert, incident-responder, kubernetes-specialist, microservices-architect, monitoring-specialist, network-engineer, platform-engineer, sre-engineer, terraform-engineer, terraform-specialist, terragrunt-expert, vercel-deployment-specialist... |
| documentation (11) | api-documenter, changelog-generator, diagram-architect, documentation-engineer, docusaurus-expert, technical-writer... |
| expert-advisors (52) | 4.1-Beast, agent-expert, agent-organizer, architect-review, critical-thinking, custom-agent-foundry, declarative-agents-architect, expert-dotnet-software-engineer, implementation-plan, it-ops-orchestrator, knowledge-synthesizer, mentor, meta-agentic-project-scaffold, multi-agent-coordinator, principal-software-engineer, workflow-orchestrator... |
| ffmpeg-clip-team (8) | audio-mixer, podcast-content-analyzer, podcast-transcriber, social-media-clip-creator, video-editor... |
| finance (5) | fintech-engineer, payment-integration, quant-analyst, risk-manager |
| game-development (5) | 3d-artist, game-designer, game-developer, unity-game-developer, unreal-engine-developer |
| git (3) | commit-guardian, git-flow-manager, git-workflow-manager |
| mcp-dev-team (8) | mcp-deployment-orchestrator, mcp-developer, mcp-integration-engineer, mcp-protocol-specialist, mcp-security-auditor, mcp-server-architect, mcp-testing-engineer |
| modernization (3) | architecture-modernizer, cloud-migration-specialist, legacy-modernizer |
| obsidian-ops-team (7) | connection-agent, content-curator, metadata-agent, moc-agent, review-agent, tag-agent, vault-optimizer |
| ocr-extraction-team (7) | document-structure-analyzer, ocr-grammar-fixer, ocr-preprocessing-optimizer, ocr-quality-assurance, visual-analysis-ocr... |
| performance-testing (5) | load-testing-specialist, performance-engineer, react-performance-optimization, web-vitals-optimizer |
| podcast-creator-team (11) | episode-orchestrator, guest-outreach-coordinator, podcast-editor, podcast-trend-scout, seo-podcast-optimizer, social-media-copywriter... |
| programming-languages (50) | angular-architect, c-pro, cpp-pro, csharp-developer, django-developer, dotnet-core-expert, elixir-expert, flutter-expert, golang-pro, java-architect, javascript-pro, kotlin-specialist, laravel-specialist, nextjs-developer, php-pro, python-pro, rails-expert, react-specialist, rust-engineer, rust-pro, shell-scripting-pro, spring-boot-engineer, sql-pro, swift-expert, typescript-pro, vue-expert... |
| realtime (2) | supabase-realtime-optimizer, websocket-engineer |
| security (21) | api-security-audit, compliance-auditor, compliance-specialist, github-actions-expert, incident-responder, penetration-tester, security-auditor, security-engineer, supply-chain-security... |
| ui-analysis (5) | screenshot-business-analyzer, screenshot-interaction-analyzer, screenshot-reviewer, screenshot-synthesizer, screenshot-ui-analyzer |
| web-tools (16) | accessibility, expert-nextjs-developer, expert-react-frontend-engineer, nextjs-architecture-expert, react-performance-optimizer, seo-analyzer, web-accessibility-checker, wordpress-master... |

---

## COMMANDS (340) — Read from `~/.claude/commands/{category}/{name}.md`

| Category | Commands |
|----------|----------|
| analysis (1) | supply-chain-audit |
| automation (4) | act, ci-pipeline, husky, workflow-orchestrator |
| azure (2) | appinsights-instrumentation, azure-role-selector |
| database (9) | snowflake-semanticview, supabase-backup-manager, supabase-data-explorer, supabase-migration-assistant, supabase-performance-optimizer, supabase-realtime-monitor, supabase-schema-sync, supabase-security-audit, supabase-type-generator |
| deployment (11) | add-changelog, blue-green-deployment, ci-setup, containerize-application, deployment-monitoring, hotfix-deploy, prepare-release, rollback-deploy, setup-automated-releases, setup-kubernetes-deployment |
| design (1) | web-design-reviewer |
| documentation (10) | create-architecture-documentation, create-onboarding-guide, doc-api, docs-maintenance, generate-api-documentation, interactive-documentation, load-llms-txt, migration-guide, troubleshooting-guide, update-docs |
| game-development (5) | game-analytics-integration, game-asset-pipeline, game-performance-profiler, game-testing-framework, unity-project-setup |
| git (5) | feature, finish, flow-status, hotfix, release |
| git-workflow (14) | branch-cleanup, commit, create-pr, create-pull-request, create-worktrees, fix-github-issue, gemini-review, git-bisect-helper, pr-review, update-branch-name, worktree-check, worktree-cleanup, worktree-deliver, worktree-init |
| google-workspace (47) | gws-admin, gws-calendar, gws-chat, gws-docs, gws-drive, gws-forms, gws-gmail, gws-keep, gws-meet, gws-sheets, gws-slides, gws-tasks, gws-vault, gws-workflow... |
| marketing (5) | publisher-all, publisher-devto, publisher-linkedin, publisher-medium, publisher-x |
| nextjs-vercel (10) | nextjs-api-tester, nextjs-bundle-analyzer, nextjs-component-generator, nextjs-middleware-creator, nextjs-migration-helper, nextjs-performance-audit, nextjs-scaffold, vercel-deploy-optimize, vercel-edge-function, vercel-env-sync |
| orchestration (15) | archive, commit, feature-analyzer, feature-dev, feature-pipeline, find, log, move, optimize, remove, report, resume, start, status, sync |
| performance (10) | add-performance-monitoring, implement-caching-strategy, optimize-api-performance, optimize-build, optimize-bundle-size, optimize-database-performance, optimize-memory-usage, performance-audit, setup-cdn-optimization, system-behavior-simulator |
| personas (10) | persona-content-creator, persona-customer-support, persona-event-coordinator, persona-exec-assistant, persona-hr-coordinator, persona-it-admin, persona-project-manager, persona-researcher, persona-sales-ops, persona-team-lead |
| project-management (20) | add-package, create-feature, create-jtbd, create-prd, create-prp, github-issues, init-project, milestone-tracker, nuget-manager, pac-configure, pac-create-epic, pac-create-ticket, pac-validate, project-health-check, project-timeline-simulator, release, todo... |
| recipes (50) | Google Workspace automation recipes (email, calendar, drive, sheets, docs, tasks, forms...) |
| security (6) | add-authentication-system, dependency-audit, penetration-test, secrets-scanner, security-audit, security-hardening |
| setup (15) | create-database-migrations, design-database-schema, design-rest-api, implement-graphql-api, migrate-to-typescript, setup-ci-cd-pipeline, setup-development-environment, setup-docker-containers, setup-formatting, setup-linting, setup-monitoring-observability, setup-monorepo, setup-rate-limiting, update-dependencies, vercel-analytics |
| simulation (10) | business-scenario-explorer, constraint-modeler, decision-tree-explorer, digital-twin-creator, future-scenario-generator, market-response-modeler, monte-carlo-simulator, simulation-calibrator, system-dynamics-modeler, timeline-compressor |
| svelte (16) | svelte-a11y, svelte-component, svelte-debug, svelte-migrate, svelte-optimize, svelte-scaffold, svelte-storybook, svelte-test... |
| sync (14) | bidirectional-sync, bulk-import-issues, cross-reference-manager, issue-to-linear-task, sync-automation-setup, sync-conflict-resolver, sync-health-monitor, sync-issues-to-linear, sync-status... |
| team (14) | architecture-review, decision-quality-analyzer, dependency-mapper, estimate-assistant, issue-triage, memory-spring-cleaning, migration-assistant, retrospective-analyzer, sprint-planning, standup-report, team-knowledge-mapper, team-velocity-tracker, team-workload-balancer |
| testing (15) | add-mutation-testing, add-property-based-testing, e2e-setup, generate-test-cases, generate-tests, setup-comprehensive-testing, setup-load-testing, setup-visual-testing, test-automation-orchestrator, test-coverage, test-quality-analyzer, write-tests... |
| utilities (21) | all-tools, architecture-scenario-explorer, clean, cleanup-cache, code-review, code-to-task, context-prime, debug-error, directory-deep-dive, explain-code, fix-issue, git-status, prime, refactor-code, screenshot-analyzer, ultra-think... |

---

## HOOKS (67) — Templates at `~/.claude/hooks/aitmpl/{category}/`

| Category | Hooks |
|----------|-------|
| automation (20) | agents-md-loader, build-on-change, change-logger, dependency-checker, deployment-health-monitor, discord-notifications (3 variants), simple-notifications, slack-notifications (3 variants), telegram-notifications (3 variants), telegram-pr-webhook, vercel-auto-deploy, vercel-environment-sync |
| development-tools (11) | change-tracker, command-logger, debug-window, edit-audit-log, file-backup, lint-on-save, nextjs-code-quality-enforcer, smart-formatting, worktree-ghostty |
| git (6) | conventional-commits, prevent-direct-push, validate-branch-name |
| git-workflow (2) | auto-git-add, smart-commit |
| monitoring (3) | desktop-notification-on-stop, langsmith-tracing |
| performance (2) | performance-budget-guard, performance-monitor |
| post-tool (4) | format-javascript-files, format-python-files, git-add-changes, run-tests-after-changes |
| pre-tool (4) | backup-before-edit, console-log-cleaner, notify-before-bash, update-search-year |
| quality-gates (6) | plan-gate, scope-guard, tdd-gate |
| security (8) | dangerous-command-blocker, env-file-protection, file-protection, force-push-blocker, secret-scanner, security-scanner |
| testing (1) | test-runner |

---

## SETTINGS TEMPLATES (67) — At `~/.claude/settings-templates/{category}/`

| Category | Templates |
|----------|-----------|
| api (4) | bedrock-configuration, corporate-proxy, custom-headers, vertex-configuration |
| authentication (3) | api-key-helper, force-claudeai-login, force-console-login |
| cleanup (2) | retention-7-days, retention-90-days |
| environment (5) | bash-timeouts, development-utils, friday-deploy-warning, performance-optimization, privacy-focused |
| git (1) | git-flow-settings |
| global (5) | aws-credentials, company-announcements, custom-model, git-commit-settings, spinner-tips-override |
| mcp (4) | disable-risky-servers, enable-all-project-servers, enable-specific-servers, mcp-timeouts |
| model (2) | use-haiku, use-sonnet |
| permissions (6) | additional-directories, allow-git-operations, allow-npm-commands, deny-sensitive-files, development-mode, read-only-mode |
| statusline (30) | colorful, minimal, git-branch, git-flow-status, project-info, rpg-status-bar, vercel-deployment-monitor, neon-database-context... |
| telemetry (4) | custom-telemetry, disable-telemetry, enable-telemetry, langsmith-tracing |

---

## MCP TEMPLATES (69) — At `~/.claude/mcp-templates/{category}/`

| Category | Servers |
|----------|---------|
| audio (1) | elevenlabs |
| browser_automation (6) | browser-use-mcp-server, browsermcp, mcp-server-browserbase, mcp-server-playwright, playwright-mcp-server, playwright-mcp |
| database (5) | mysql-integration, neon, postgresql-documentation, postgresql-integration, supabase |
| deepgraph (4) | deepgraph-nextjs, deepgraph-react, deepgraph-typescript, deepgraph-vue |
| deepresearch (1) | mcp-server-nia |
| devtools (37) | azure-kubernetes-service, chrome-devtools, circleci, codacy, context7, dynatrace, elasticsearch, figma-dev-mode, firecrawl, grafana, huggingface, jfrog, launchdarkly, logfire, markitdown, mongodb, postman, pulumi, railway, sentry, serena, stripe, terraform, webflow... |
| filesystem (1) | filesystem-access |
| integration (3) | footballbin-predictions, github-integration, memory-integration |
| marketing (2) | facebook-ads-mcp-server, google-ads-mcp-server |
| productivity (2) | monday, notion |
| web-data (2) | brightdata, browseract |
| web (5) | tinyfish, web-fetch, web-reader, web-search-prime, zread |
