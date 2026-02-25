#!/bin/bash

# ============================================================
# MDAN CLI — Command Line Interface
# Multi-Agent Development Agentic Network
# ============================================================

VERSION="2.5.0"
MDAN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ============================================================
# BANNER
# ============================================================

banner() {
    echo -e "${CYAN}"
    echo "  ███╗   ███╗██████╗  █████╗ ███╗   ██╗"
    echo "  ████╗ ████║██╔══██╗██╔══██╗████╗  ██║"
    echo "  ██╔████╔██║██║  ██║███████║██╔██╗ ██║"
    echo "  ██║╚██╔╝██║██║  ██║██╔══██║██║╚██╗██║"
    echo "  ██║ ╚═╝ ██║██████╔╝██║  ██║██║ ╚████║"
    echo "  ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝"
    echo -e "${NC}"
    echo -e "  ${BOLD}Multi-Agent Development Agentic Network${NC} v${VERSION}"
    echo ""
}

# ============================================================
# HELP
# ============================================================

show_help() {
    banner
    echo -e "${BOLD}USAGE${NC}"
    echo "  mdan <command> [options]"
    echo ""
    echo -e "${BOLD}COMMANDS${NC}"
    echo "  init [project-name]       Create a new MDAN project"
    echo "  attach [--rebuild]        Add MDAN to existing project"
    echo "                            --rebuild: prepare for full rewrite"
    echo "  learn [--skill|--mcp|...] Learn & distribute knowledge"
    echo "  skills                    List available skills"
    echo "  skill add <source>        Install a new skill"
    echo "  phase [1-5]               Show phase guide"
    echo "  agent [name]              Show agent prompt"
    echo "  template [name]           Show or copy a template"
    echo "  prompt [llm]              Show setup instructions for an LLM"
    echo "  oc                        Copy orchestrator prompt to clipboard"

    echo "  status                    Show current project status"
    echo "  list                      List all agents and templates"
    echo "  version                   Show version"
    echo ""
    echo -e "${BOLD}EXAMPLES${NC}"
    echo "  mdan init my-saas                # Create new project"
    echo "  cd existing && mdan attach       # Add MDAN to existing project"
    echo "  cd existing && mdan attach --rebuild  # Prepare for full rewrite"
    echo "  mdan phase 1                     # Show DISCOVER guide"
    echo "  mdan skill add vercel-labs/skills --skill find-skills"
    echo ""
    echo -e "${BOLD}AGENTS${NC}"
    echo "  product, architect, ux, dev, test, security, devops, doc"
    echo ""
    echo -e "${BOLD}LLMS / TOOLS${NC}"
    echo "  claude, chatgpt, gemini, qwen, kimi, glm, minimax, opencode, cursor, windsurf, copilot"
}

# ============================================================
# LEARN
# ============================================================

cmd_learn() {
    SUBCOMMAND="${1}"
    shift

    case "${SUBCOMMAND}" in
        --skill|--rules|--url)
            SOURCE="${1}"
            echo -e "${CYAN}🧠 Learn Agent — Ingesting: ${BOLD}${SOURCE}${NC}"
            echo ""
            echo -e "Copy this activation prompt into your LLM:\n"
            echo "---"
            echo "[ACTIVATING: Learn Agent v2.0.0]"
            echo "Task: Learn and distribute the following source."
            echo "Source type: ${SUBCOMMAND/--/}"
            echo "Source: ${SOURCE}"
            echo "Distribute to: auto-detect"
            echo "---"
            ;;
        --mcp)
            MCP_NAME="${1}"
            echo -e "${CYAN}🔌 Learn Agent — MCP: ${BOLD}${MCP_NAME}${NC}"
            echo ""
            echo "Copy this activation prompt into your LLM:"
            echo "---"
            echo "[ACTIVATING: Learn Agent v2.0.0]"
            echo "Task: Learn the ${MCP_NAME} MCP server and distribute tools to relevant agents."
            echo "Source type: mcp"
            echo "Source: ${MCP_NAME}"
            echo "---"
            ;;
        --list)
            KNOWLEDGE_FILE="mdan/MDAN-KNOWLEDGE.md"
            if [[ -f "${KNOWLEDGE_FILE}" ]]; then
                cat "${KNOWLEDGE_FILE}"
            else
                echo -e "${YELLOW}No knowledge file found. Run: mdan learn --skill <file>${NC}"
            fi
            ;;
        --capsule)
            AGENT="${1}"
            echo -e "${CYAN}Capsule for agent: ${BOLD}${AGENT}${NC}"
            KNOWLEDGE_FILE="mdan/MDAN-KNOWLEDGE.md"
            if [[ -f "${KNOWLEDGE_FILE}" ]]; then
                grep -A 20 "### ${AGENT^} Agent" "${KNOWLEDGE_FILE}" | head -25
            else
                echo -e "${YELLOW}No knowledge file. Run mdan learn first.${NC}"
            fi
            ;;
        *)
            echo "Usage: mdan learn [--skill|--rules|--mcp|--url|--list|--capsule] [value]"
            echo ""
            echo "  mdan learn --skill ./docs/conventions.md"
            echo "  mdan learn --mcp github"
            echo "  mdan learn --rules .cursorrules"
            echo "  mdan learn --list"
            echo "  mdan learn --capsule dev"
            ;;
    esac
}

# ============================================================
# SKILLS
# ============================================================

cmd_skills() {
    SKILLS_DIR="${MDAN_DIR}/skills"
    
    if [[ -d "${SKILLS_DIR}" ]]; then
        echo -e "${CYAN}${BOLD}Available Skills{NC}"
        echo ""
        for skill_dir in "${SKILLS_DIR}"/*/; do
            if [[ -d "${skill_dir}" ]]; then
                skill_name=$(basename "${skill_dir}")
                skill_file="${skill_dir}skill.md"
                if [[ -f "${skill_file}" ]]; then
                    description=$(grep -A1 "^description:" "${skill_file}" 2>/dev/null | tail -1 | sed 's/^description: //')
                    echo -e "  ${GREEN}●${NC} ${BOLD}${skill_name}${NC}"
                    echo "    ${description}"
                    echo ""
                else
                    echo -e "  ${GREEN}●${NC} ${BOLD}${skill_name}${NC}"
                    echo ""
                fi
            fi
        done
    else
        echo -e "${YELLOW}No skills installed.${NC}"
    fi
}

cmd_skill_add() {
    SOURCE="${1}"
    shift
    
    echo -e "${CYAN}📦 Installing skill from: ${BOLD}${SOURCE}${NC}"
    echo ""
    
    npx skills add "${SOURCE}" "$@" --yes
}

# ============================================================
# ATTACH (Add MDAN to existing project)
# ============================================================

cmd_attach() {
    REBUILD_MODE=false
    
    # Check for --rebuild flag
    if [[ "${1}" == "--rebuild" ]]; then
        REBUILD_MODE=true
    fi
    
    # Check if we're in a project directory
    if [[ ! -f "package.json" && ! -f "requirements.txt" && ! -f "go.mod" && ! -f "Cargo.toml" && ! -f "pom.xml" && ! -f "build.gradle" && ! -f "composer.json" && ! -d ".git" ]]; then
        echo -e "${YELLOW}⚠️  Warning: This doesn't look like a project directory.${NC}"
        echo "   No package.json, requirements.txt, or other project files found."
        echo ""
        read -p "   Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    PROJECT_NAME=$(basename "$PWD")
    
    if [[ "$REBUILD_MODE" == true ]]; then
        echo -e "${MAGENTA}🔄 Attaching MDAN with REBUILD mode: ${BOLD}${PROJECT_NAME}${NC}"
        echo ""
        echo -e "${YELLOW}This will prepare MDAN to rewrite the entire project from scratch.${NC}"
        echo ""
    else
        echo -e "${CYAN}🔗 Attaching MDAN to: ${BOLD}${PROJECT_NAME}${NC}"
        echo ""
    fi
    
    # Check if mdan already exists
    if [[ -d "mdan" ]]; then
        echo -e "${YELLOW}⚠️  mdan folder already exists.${NC}"
        read -p "   Overwrite? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "   Keeping existing mdan folder."
        else
            rm -rf mdan
        fi
    fi
    
    # Create mdan directory structure
    mkdir -p mdan/agents
    mkdir -p mdan/artifacts
    mkdir -p mdan/skills
    
    # Copy core files
    cp "${MDAN_DIR}/core/orchestrator.md" mdan/orchestrator.md
    cp "${MDAN_DIR}/core/universal-envelope.md" mdan/universal-envelope.md
    
    # Copy all agents
    cp "${MDAN_DIR}/agents/"*.md mdan/agents/
    
    # Copy skills if available
    if [[ -d "${MDAN_DIR}/skills" ]]; then
        cp -r "${MDAN_DIR}/skills/"* mdan/skills/ 2>/dev/null
    fi
    
    # Create .cursorrules
    cat "${MDAN_DIR}/core/orchestrator.md" > .cursorrules
    echo "" >> .cursorrules
    echo "## CURSOR INSTRUCTIONS" >> .cursorrules
    echo "Agent files are in mdan/agents/. Reference them with @file when activating agents." >> .cursorrules
    echo "Skills are in mdan/skills/. Reference them for extended capabilities." >> .cursorrules
    echo "" >> .cursorrules
    
    if [[ "$REBUILD_MODE" == true ]]; then
        echo "## PROJECT CONTEXT" >> .cursorrules
        echo "This is an existing project that will be REWRITTEN FROM SCRATCH." >> .cursorrules
        echo "MDAN must first analyze all features, then rebuild everything." >> .cursorrules
        echo "" >> .cursorrules
        echo "## REBUILD MODE ACTIVE" >> .cursorrules
        echo "1. DISCOVER: Analyze ALL features of existing codebase" >> .cursorrules
        echo "2. DESIGN: Propose NEW modern architecture" >> .cursorrules
        echo "3. BUILD: Rewrite everything from scratch" >> .cursorrules
        echo "4. VERIFY: Full test coverage" >> .cursorrules
        echo "5. SHIP: Complete documentation" >> .cursorrules
    else
        echo "## PROJECT CONTEXT" >> .cursorrules
        echo "This is an existing project. MDAN should analyze the codebase before making changes." >> .cursorrules
    fi
    
    # Create .windsurfrules
    cp .cursorrules .windsurfrules
    
    # Create .claude/skills for Claude Code
    mkdir -p .claude/skills
    if [[ -d "${MDAN_DIR}/skills" ]]; then
        cp -r "${MDAN_DIR}/skills/"* .claude/skills/ 2>/dev/null
    fi
    
    # Create GitHub Copilot instructions
    mkdir -p .github
    cp "${MDAN_DIR}/core/orchestrator.md" .github/copilot-instructions.md
    
    # Create MDAN-STATE.json
    if [[ "$REBUILD_MODE" == true ]]; then
        cat > mdan/MDAN-STATE.json << EOF
{
  "user": {
    "name": null
  },
  "project": {
    "name": "${PROJECT_NAME}",
    "type": "existing",
    "mode": "REBUILD",
    "profile": "STANDARD",
    "started": "$(date +%Y-%m-%d)",
    "last_updated": "$(date +%Y-%m-%dT%H:%M:%S)"
  },
  "phase": {
    "current": "DISCOVER",
    "status": "analyzing_for_rebuild"
  },
  "features": [],
  "artifacts": {
    "prd": null,
    "architecture": null,
    "ux_spec": null,
    "test_plan": null,
    "security_review": null
  },
  "agents_used": {},
  "notes": "REBUILD MODE: MDAN will analyze existing codebase and rewrite from scratch."
}
EOF
    else
        cat > mdan/MDAN-STATE.json << EOF
{
  "user": {
    "name": null
  },
  "project": {
    "name": "${PROJECT_NAME}",
    "type": "existing",
    "profile": "STANDARD",
    "started": "$(date +%Y-%m-%d)",
    "last_updated": "$(date +%Y-%m-%dT%H:%M:%S)"
  },
  "phase": {
    "current": "DISCOVER",
    "status": "analyzing_existing_codebase"
  },
  "features": [],
  "artifacts": {
    "prd": null,
    "architecture": null,
    "ux_spec": null,
    "test_plan": null,
    "security_review": null
  },
  "agents_used": {},
  "notes": "MDAN attached to existing project. Start with DISCOVER phase to analyze the codebase."
}
EOF
    fi
    
    # Create STATUS.md
    if [[ "$REBUILD_MODE" == true ]]; then
        cat > mdan/STATUS.md << EOF
# MDAN Project Status — REBUILD MODE

**Project:** ${PROJECT_NAME}
**Started:** $(date +%Y-%m-%d)
**Mode:** 🔄 REBUILD FROM SCRATCH
**Current Phase:** 1 — DISCOVER (Analyzing existing codebase)

## 🎯 Objective
Rewrite the entire project from scratch with a modern architecture.

## Phase Progress
- [ ] Phase 1: DISCOVER — Analyze ALL features of existing codebase
- [ ] Phase 2: DESIGN — New modern architecture validated
- [ ] Phase 3: BUILD — Rewrite everything from scratch
- [ ] Phase 4: VERIFY — 100% test coverage
- [ ] Phase 5: SHIP — Complete documentation

## What MDAN Will Do
1. **DISCOVER**: Deep analysis of existing code to understand ALL features
2. **DESIGN**: Propose a completely new, modern architecture
3. **BUILD**: Implement everything fresh (no code reuse)
4. **VERIFY**: Write comprehensive tests
5. **SHIP**: Generate full documentation

## Commands to Start
1. Open this folder in Cursor/Windsurf
2. Start with: "MDAN REBUILD: Begin DISCOVER phase. Analyze this entire codebase."
EOF
    else
        cat > mdan/STATUS.md << EOF
# MDAN Project Status

**Project:** ${PROJECT_NAME} (existing)
**Started:** $(date +%Y-%m-%d)
**Current Phase:** 1 — DISCOVER (Analyzing existing codebase)

## Phase Progress
- [ ] Phase 1: DISCOVER — Analyze existing codebase & define improvements
- [ ] Phase 2: DESIGN — Architecture changes validated
- [ ] Phase 3: BUILD — Features implemented
- [ ] Phase 4: VERIFY — Tests passing, security reviewed
- [ ] Phase 5: SHIP — Deployed and documented

## Existing Project Notes
- MDAN attached on $(date +%Y-%m-%d)
- Start by analyzing the current codebase structure
- Identify what needs to be built/improved

## Commands to Start
1. Open Claude/Cursor with this project
2. Paste mdan/orchestrator.md as system prompt
3. Start with: "MDAN: Analyze this existing project and help me [goal]"
EOF
    fi
    
    echo -e "${GREEN}✅ MDAN attached to ${PROJECT_NAME}!${NC}"
    echo ""
    echo -e "  ${BOLD}MDAN files:${NC} mdan/"
    echo -e "  ${BOLD}Agents:${NC} mdan/agents/"
    echo -e "  ${BOLD}Skills:${NC} mdan/skills/"
    echo -e "  ${BOLD}State:${NC} mdan/MDAN-STATE.json"
    echo ""
    
    if [[ "$REBUILD_MODE" == true ]]; then
        echo -e "${MAGENTA}${BOLD}🔄 REBUILD MODE ACTIVATED${NC}"
        echo ""
        echo -e "${YELLOW}MDAN will rewrite the entire project from scratch.${NC}"
        echo ""
        echo "  ${BOLD}Next steps:${NC}"
        echo ""
        echo "  1. Open this folder in Cursor/Windsurf"
        echo "  2. Start with this prompt:"
        echo ""
        echo -e "  ${CYAN}MDAN REBUILD: Begin DISCOVER phase."
        echo "  Analyze this entire codebase and document ALL features."
        echo "  Then propose a modern architecture to rebuild from scratch.${NC}"
    else
        echo -e "${YELLOW}Next steps:${NC}"
        echo ""
        echo "  ${BOLD}Option 1 — Cursor/Windsurf:${NC}"
        echo "    Just open this folder in your IDE and start chatting."
        echo ""
        echo "  ${BOLD}Option 2 — Claude (Web) / ChatGPT:${NC}"
        echo "    1. Run ${CYAN}mdan oc${NC} to copy the orchestrator prompt to clipboard"
        echo "    2. Paste as system prompt (or first message)"
        echo "    3. Start with: 'MDAN: Analyze this existing project...'"
    fi
}

# ============================================================
# INIT
# ============================================================

cmd_init() {
    PROJECT_NAME="${1:-my-project}"
    
    echo -e "${CYAN}🚀 Initializing MDAN project: ${BOLD}${PROJECT_NAME}${NC}"
    echo ""
    
    # Create mdan directory structure
    mkdir -p "${PROJECT_NAME}/mdan/agents"
    mkdir -p "${PROJECT_NAME}/mdan/artifacts"
    mkdir -p "${PROJECT_NAME}/mdan/skills"
    mkdir -p "${PROJECT_NAME}/mdan_output"
    
    # Copy core files
    cp "${MDAN_DIR}/core/orchestrator.md" "${PROJECT_NAME}/mdan/orchestrator.md"
    cp "${MDAN_DIR}/core/universal-envelope.md" "${PROJECT_NAME}/mdan/universal-envelope.md"
    
    # Copy all agents
    cp "${MDAN_DIR}/agents/"*.md "${PROJECT_NAME}/mdan/agents/"
    
    # Copy templates
    cp "${MDAN_DIR}/templates/"*.md "${PROJECT_NAME}/mdan_output/"
    
    # Copy skills if available
    if [[ -d "${MDAN_DIR}/skills" ]]; then
        cp -r "${MDAN_DIR}/skills/"* "${PROJECT_NAME}/mdan/skills/" 2>/dev/null
    fi
    
    # Create .cursorrules
    cat "${MDAN_DIR}/core/orchestrator.md" > "${PROJECT_NAME}/.cursorrules"
    echo "" >> "${PROJECT_NAME}/.cursorrules"
    echo "## CURSOR INSTRUCTIONS" >> "${PROJECT_NAME}/.cursorrules"
    echo "Agent files are in mdan/agents/. Reference them with @file when activating agents." >> "${PROJECT_NAME}/.cursorrules"
    echo "Skills are in mdan/skills/. Reference them for extended capabilities." >> "${PROJECT_NAME}/.cursorrules"
    
    # Create .windsurfrules
    cp "${PROJECT_NAME}/.cursorrules" "${PROJECT_NAME}/.windsurfrules"
    
    # Create .claude/skills for Claude Code
    mkdir -p "${PROJECT_NAME}/.claude/skills"
    if [[ -d "${MDAN_DIR}/skills" ]]; then
        cp -r "${MDAN_DIR}/skills/"* "${PROJECT_NAME}/.claude/skills/" 2>/dev/null
    fi
    
    # Create GitHub Copilot instructions
    mkdir -p "${PROJECT_NAME}/.github"
    cp "${MDAN_DIR}/core/orchestrator.md" "${PROJECT_NAME}/.github/copilot-instructions.md"
    
    # Create STATUS.md
    cat > "${PROJECT_NAME}/mdan/STATUS.md" << EOF
# MDAN Project Status

**Project:** ${PROJECT_NAME}
**Started:** $(date +%Y-%m-%d)
**Current Phase:** 1 — DISCOVER

## Phase Progress
- [ ] Phase 1: DISCOVER — PRD validated
- [ ] Phase 2: DESIGN — Architecture + UX validated
- [ ] Phase 3: BUILD — All MVP features implemented
- [ ] Phase 4: VERIFY — All tests passing, security reviewed
- [ ] Phase 5: SHIP — Deployed and documented

## Notes
EOF
    
    # Create README
    cat > "${PROJECT_NAME}/README.md" << EOF
# ${PROJECT_NAME}

> *Project initialized with [MDAN](https://github.com/khalilbenaz/MDAN)*

## Status
Phase 1: DISCOVER — In progress

## Getting Started
See \`mdan_output/\` for project documentation and artifacts as they evolve.
EOF
    
    echo -e "${GREEN}✅ MDAN project initialized successfully!${NC}"
    echo ""
    echo -e "  ${BOLD}Project:${NC} ${PROJECT_NAME}/"
    echo -e "  ${BOLD}MDAN files:${NC} ${PROJECT_NAME}/mdan/"
    echo -e "  ${BOLD}Templates:${NC} ${PROJECT_NAME}/mdan_output/"
    echo -e "  ${BOLD}Skills:${NC} ${PROJECT_NAME}/mdan/skills/"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Open your chosen LLM"
    echo "  2. Paste mdan/orchestrator.md as your system prompt"
    echo "  3. Start with: 'MDAN: I want to build ${PROJECT_NAME}'"
    echo ""
    echo -e "  Or for Cursor/Windsurf: open the ${PROJECT_NAME}/ folder — .cursorrules is ready"
}

# ============================================================
# PHASE
# ============================================================

cmd_phase() {
    PHASE="${1}"
    ACTION="${2}"
    
    FILE=""
    NAME=""
    case "${PHASE}" in
        1|discover) 
            FILE="01-discover.md"
            NAME="DISCOVER"
            ;;
        2|design) 
            FILE="02-design.md"
            NAME="DESIGN"
            ;;
        3|build) 
            FILE="03-build.md"
            NAME="BUILD"
            ;;
        4|verify) 
            FILE="04-verify.md"
            NAME="VERIFY"
            ;;
        5|ship) 
            FILE="05-ship.md"
            NAME="SHIP"
            ;;
        *)
            echo -e "${RED}Unknown phase: ${PHASE}${NC}"
            echo "Available phases: 1 (discover), 2 (design), 3 (build), 4 (verify), 5 (ship)"
            return 1
            ;;
    esac

    if [[ -f "${MDAN_DIR}/phases/${FILE}" ]]; then
        if [[ "${ACTION}" == "copy" || "${ACTION}" == "-c" ]]; then
            CONTENT=$(cat "${MDAN_DIR}/phases/${FILE}")
            if command -v pbcopy &> /dev/null; then
                echo "$CONTENT" | pbcopy
                echo -e "${GREEN}✅ Phase ${NAME} prompt copied to clipboard!${NC}"
                echo "   Paste it into your LLM to start the phase."
            elif command -v xclip &> /dev/null; then
                echo "$CONTENT" | xclip -selection clipboard
                echo -e "${GREEN}✅ Phase ${NAME} prompt copied to clipboard!${NC}"
                echo "   Paste it into your LLM to start the phase."
            elif command -v wl-copy &> /dev/null; then
                echo "$CONTENT" | wl-copy
                echo -e "${GREEN}✅ Phase ${NAME} prompt copied to clipboard!${NC}"
                echo "   Paste it into your LLM to start the phase."
            else
                cat "${MDAN_DIR}/phases/${FILE}"
                echo -e "\n${YELLOW}⚠️  Could not copy automatically. Please copy the text above.${NC}"
            fi
        else
            echo -e "${CYAN}${BOLD}Phase ${NAME}${NC}"
            cat "${MDAN_DIR}/phases/${FILE}"
            echo ""
            echo -e "${YELLOW}Tip: Run '${CYAN}mdan phase ${PHASE} copy${YELLOW}' to copy this content to clipboard.${NC}"
        fi
    else
        echo -e "${RED}Phase file not found: ${FILE}${NC}"
    fi
}

# ============================================================
# AGENT
# ============================================================

cmd_agent() {
    AGENT="${1}"
    AGENT_FILE="${MDAN_DIR}/agents/${AGENT}.md"
    
    if [[ -f "${AGENT_FILE}" ]]; then
        cat "${AGENT_FILE}"
    else
        echo -e "${RED}Unknown agent: ${AGENT}${NC}"
        echo "Available agents: product, architect, ux, dev, test, security, devops, doc"
    fi
}

# ============================================================
# TEMPLATE
# ============================================================

cmd_template() {
    TEMPLATE="${1}"
    TEMPLATE_FILE="${MDAN_DIR}/templates/${TEMPLATE}.md"
    
    if [[ -f "${TEMPLATE_FILE}" ]]; then
        cat "${TEMPLATE_FILE}"
    else
        echo -e "${RED}Template not found: ${TEMPLATE}${NC}"
        echo "Available templates:"
        ls "${MDAN_DIR}/templates/" | sed 's/.md//'
    fi
}

# ============================================================
# PROMPT (LLM setup)
# ============================================================

cmd_prompt() {
    LLM="${1}"
    INTEGRATION_FILE="${MDAN_DIR}/integrations/${LLM}.md"
    
    if [[ -f "${INTEGRATION_FILE}" ]]; then
        cat "${INTEGRATION_FILE}"
    else
        echo -e "${RED}Integration not found: ${LLM}${NC}"
        echo "Available integrations:"
        ls "${MDAN_DIR}/integrations/" | sed 's/.md//'
    fi
}

# ============================================================
# STATUS
# ============================================================

# ============================================================n# OC (Orchestrator)n# ============================================================nncmd_oc() {n    ORCH_FILE="mdan/orchestrator.md"n    if [[ ! -f "$ORCH_FILE" ]]; thenn        ORCH_FILE="${MDAN_DIR}/core/orchestrator.md"n    fin    n    if [[ -f "$ORCH_FILE" ]]; thenn        if command -v pbcopy &> /dev/null; thenn            cat "$ORCH_FILE" | pbcopyn            echo -e "${GREEN}✅ Orchestrator prompt copied to clipboard!${NC}"n            echo "   Paste it into Claude, ChatGPT, or your favorite LLM."n        elif command -v xclip &> /dev/null; thenn            cat "$ORCH_FILE" | xclip -selection clipboardn            echo -e "${GREEN}✅ Orchestrator prompt copied to clipboard!${NC}"n            echo "   Paste it into Claude, ChatGPT, or your favorite LLM."n        elif command -v wl-copy &> /dev/null; thenn            cat "$ORCH_FILE" | wl-copyn            echo -e "${GREEN}✅ Orchestrator prompt copied to clipboard!${NC}"n            echo "   Paste it into Claude, ChatGPT, or your favorite LLM."n        elsen            cat "$ORCH_FILE"n            echo -e "\n${YELLOW}⚠️  Could not copy to clipboard automatically. Please copy the text above.${NC}"n        fin    elsen        echo -e "${RED}Orchestrator file not found.${NC}"n    fin}nn
cmd_status() {
    STATUS_FILE="mdan/STATUS.md"
    if [[ -f "${STATUS_FILE}" ]]; then
        cat "${STATUS_FILE}"
    else
        echo -e "${YELLOW}No MDAN project found in current directory.${NC}"
        echo ""
        echo "  To create a new project: mdan init [project-name]"
        echo "  To add MDAN to existing project: mdan attach"
        echo "  To rebuild existing project: mdan attach --rebuild"
    fi
}

# ============================================================
# LIST
# ============================================================

cmd_list() {
    echo -e "${BOLD}MDAN v${VERSION}${NC}"
    echo ""
    echo -e "${CYAN}Phases:${NC}"
    ls "${MDAN_DIR}/phases/" | sed 's/.md//' | sed 's/^/  /'
    echo ""
    echo -e "${CYAN}Agents:${NC}"
    ls "${MDAN_DIR}/agents/" | grep -v "REGISTRY" | sed 's/.md//' | sed 's/^/  /'
    echo ""
    echo -e "${CYAN}Templates:${NC}"
    ls "${MDAN_DIR}/templates/" | sed 's/.md//' | sed 's/^/  /'
    echo ""
    echo -e "${CYAN}Integrations:${NC}"
    ls "${MDAN_DIR}/integrations/" | sed 's/.md//' | sed 's/^/  /'
    echo ""
    if [[ -d "${MDAN_DIR}/skills" ]]; then
        echo -e "${CYAN}Skills:${NC}"
        ls "${MDAN_DIR}/skills/" | sed 's/^/  /'
    fi
}

# ============================================================
# MAIN
# ============================================================

COMMAND="${1}"
shift

case "${COMMAND}" in
    learn)      cmd_learn "$@" ;;
    skills)     cmd_skills ;;
    skill)      cmd_skill_add "$@" ;;
    attach)     cmd_attach "$@" ;;
    init)       cmd_init "$@" ;;
    phase)      cmd_phase "$@" ;;
    agent)      cmd_agent "$@" ;;
    template)   cmd_template "$@" ;;
    prompt)     cmd_prompt "$@" ;;
    oc)         cmd_oc ;;

    status)     cmd_status ;;
    list)       cmd_list ;;
    version)    echo "MDAN v${VERSION}" ;;
    help|--help|-h|"") show_help ;;
    *)
        echo -e "${RED}Unknown command: ${COMMAND}${NC}"
        echo "Run 'mdan help' for usage"
        exit 1
        ;;
esac
