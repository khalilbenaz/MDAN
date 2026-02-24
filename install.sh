#!/bin/bash

# ============================================================
# MDAN Installer
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

INSTALL_DIR="$HOME/.mdan"
BIN_DIR="$HOME/.local/bin"

echo -e "${CYAN}"
echo "  ███╗   ███╗██████╗  █████╗ ███╗   ██╗"
echo "  ████╗ ████║██╔══██╗██╔══██╗████╗  ██║"
echo "  ██╔████╔██║██║  ██║███████║██╔██╗ ██║"
echo "  ██║╚██╔╝██║██║  ██║██╔══██║██║╚██╗██║"
echo "  ██║ ╚═╝ ██║██████╔╝██║  ██║██║ ╚████║"
echo "  ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝"
echo -e "${NC}"
echo -e "  ${BOLD}MDAN Installer${NC}"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${YELLOW}Installing MDAN...${NC}"
echo ""

# Create installation directory
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Copy MDAN files
echo "  📁 Copying files to $INSTALL_DIR..."
cp -r "$SCRIPT_DIR/core" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/agents" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/phases" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/templates" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/integrations" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/memory" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/skills" "$INSTALL_DIR/" 2>/dev/null || mkdir -p "$INSTALL_DIR/skills"
cp "$SCRIPT_DIR/MDAN.md" "$INSTALL_DIR/" 2>/dev/null || true
cp "$SCRIPT_DIR/MDAN.fr.md" "$INSTALL_DIR/" 2>/dev/null || true

# Create the mdan command
echo "  🔧 Creating mdan command..."
cat > "$BIN_DIR/mdan" << 'MDAN_SCRIPT'
#!/bin/bash

VERSION="2.2.0"
MDAN_DIR="$HOME/.mdan"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

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

show_help() {
    banner
    echo -e "${BOLD}USAGE${NC}"
    echo "  mdan <command> [options]"
    echo ""
    echo -e "${BOLD}COMMANDS${NC}"
    echo "  init [name]              Create a new project"
    echo "  attach [--rebuild]       Add MDAN to existing project"
    echo "  status                   Show project status"
    echo "  phase [1-5]              Show phase guide"
    echo "  agent [name]             Show agent prompt"
    echo "  skills                   List available skills"
    echo "  version                  Show version"
    echo ""
    echo -e "${BOLD}EXAMPLES${NC}"
    echo "  mdan init my-app              # New project"
    echo "  cd my-project && mdan attach  # Existing project"
    echo "  mdan attach --rebuild         # Rebuild from scratch"
    echo ""
    echo -e "${BOLD}AGENTS${NC}"
    echo "  product, architect, ux, dev, test, security, devops, doc"
}

cmd_init() {
    PROJECT_NAME="${1:-my-project}"
    echo -e "${CYAN}🚀 Creating: ${BOLD}${PROJECT_NAME}${NC}"
    
    mkdir -p "${PROJECT_NAME}/.mdan/agents"
    mkdir -p "${PROJECT_NAME}/.mdan/skills"
    mkdir -p "${PROJECT_NAME}/docs"
    mkdir -p "${PROJECT_NAME}/.claude/skills"
    mkdir -p "${PROJECT_NAME}/.github"
    
    cp "${MDAN_DIR}/core/orchestrator.md" "${PROJECT_NAME}/.mdan/"
    cp "${MDAN_DIR}/core/universal-envelope.md" "${PROJECT_NAME}/.mdan/"
    cp "${MDAN_DIR}/agents/"*.md "${PROJECT_NAME}/.mdan/agents/"
    cp "${MDAN_DIR}/templates/"*.md "${PROJECT_NAME}/mdan_output/"
    cp -r "${MDAN_DIR}/skills/"* "${PROJECT_NAME}/.mdan/skills/" 2>/dev/null || true
    cp -r "${MDAN_DIR}/skills/"* "${PROJECT_NAME}/.claude/skills/" 2>/dev/null || true
    
    cat "${MDAN_DIR}/core/orchestrator.md" > "${PROJECT_NAME}/.cursorrules"
    echo -e "\n## CURSOR INSTRUCTIONS\nAgent files in .mdan/agents/\nSkills in .mdan/skills/" >> "${PROJECT_NAME}/.cursorrules"
    cp "${PROJECT_NAME}/.cursorrules" "${PROJECT_NAME}/.windsurfrules"
    cp "${MDAN_DIR}/core/orchestrator.md" "${PROJECT_NAME}/.github/copilot-instructions.md"
    
    echo "# ${PROJECT_NAME}\n\n> Built with MDAN" > "${PROJECT_NAME}/README.md"
    
    echo -e "${GREEN}✅ Created ${PROJECT_NAME}/${NC}"
    echo ""
    echo "  ${BOLD}Next:${NC} cursor ${PROJECT_NAME}"
}

cmd_attach() {
    REBUILD="${1}"
    PROJECT_NAME=$(basename "$PWD")
    
    if [[ "$REBUILD" == "--rebuild" ]]; then
        echo -e "${MAGENTA}🔄 REBUILD MODE: ${BOLD}${PROJECT_NAME}${NC}"
    else
        echo -e "${CYAN}🔗 Attaching to: ${BOLD}${PROJECT_NAME}${NC}"
    fi
    
    mkdir -p .mdan/agents .mdan/skills .claude/skills .github
    
    cp "${MDAN_DIR}/core/orchestrator.md" .mdan/
    cp "${MDAN_DIR}/core/universal-envelope.md" .mdan/
    cp "${MDAN_DIR}/agents/"*.md .mdan/agents/
    cp -r "${MDAN_DIR}/skills/"* .mdan/skills/ 2>/dev/null || true
    cp -r "${MDAN_DIR}/skills/"* .claude/skills/ 2>/dev/null || true
    
    cat "${MDAN_DIR}/core/orchestrator.md" > .cursorrules
    if [[ "$REBUILD" == "--rebuild" ]]; then
        echo -e "\n## REBUILD MODE\nAnalyze existing code then rewrite from scratch." >> .cursorrules
    else
        echo -e "\n## EXISTING PROJECT\nAnalyze codebase before making changes." >> .cursorrules
    fi
    cp .cursorrules .windsurfrules
    cp "${MDAN_DIR}/core/orchestrator.md" .github/copilot-instructions.md
    
    echo -e "${GREEN}✅ MDAN ready!${NC}"
    echo ""
    if [[ "$REBUILD" == "--rebuild" ]]; then
        echo "  Start: ${CYAN}MDAN REBUILD: Analyze and rewrite this project${NC}"
    else
        echo "  Start: ${CYAN}MDAN: Analyze this project${NC}"
    fi
}

cmd_status() {
    if [[ -f ".mdan/orchestrator.md" ]]; then
        echo -e "${GREEN}✅ MDAN is active in this project${NC}"
        [[ -f ".mdan/STATUS.md" ]] && cat .mdan/STATUS.md
    else
        echo -e "${YELLOW}No MDAN project here.${NC}"
        echo "  Run: mdan init [name]  or  mdan attach"
    fi
}

cmd_phase() {
    [[ -f "${MDAN_DIR}/phases/0${1}-"*.md ]] && cat "${MDAN_DIR}/phases/0${1}-"*.md || echo "Phase 1-5"
}

cmd_agent() {
    [[ -f "${MDAN_DIR}/agents/${1}.md" ]] && cat "${MDAN_DIR}/agents/${1}.md" || echo "Agents: product, architect, ux, dev, test, security, devops, doc"
}

cmd_skills() {
    echo -e "${CYAN}Skills:${NC}"
    ls "${MDAN_DIR}/skills/" 2>/dev/null || echo "  No skills installed"
}

# Main
case "${1}" in
    init)       cmd_init "$2" ;;
    attach)     cmd_attach "$2" ;;
    status)     cmd_status ;;
    phase)      cmd_phase "$2" ;;
    agent)      cmd_agent "$2" ;;
    skills)     cmd_skills ;;
    version|-v) echo "MDAN v${VERSION}" ;;
    help|--help|-h|"") show_help ;;
    *)          echo "Unknown: $1. Run: mdan help" ;;
esac
MDAN_SCRIPT

chmod +x "$BIN_DIR/mdan"

# Check if bin dir is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo -e "${YELLOW}⚠️  Add MDAN to your PATH:${NC}"
    echo ""
    echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    echo ""
    echo "  Or for zsh:"
    echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
    echo "  source ~/.zshrc"
fi

echo ""
echo -e "${GREEN}✅ MDAN installed successfully!${NC}"
echo ""
echo -e "  ${BOLD}Usage:${NC}"
echo "  mdan init my-project        # Create new project"
echo "  cd existing && mdan attach  # Add to existing project"
echo ""
