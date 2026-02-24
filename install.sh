#!/bin/bash

# ============================================================
# MDAN Installer (Remote Fetch)
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
REPO_URL="https://github.com/khalilbenaz/MDAN/archive/refs/heads/main.tar.gz"

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

echo -e "${YELLOW}Installing MDAN...${NC}"
echo ""

# Create installation directory
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Download and extract the repository
echo "  ⬇️  Downloading latest MDAN files..."
TMP_DIR=$(mktemp -d)
curl -sL "$REPO_URL" | tar -xz -C "$TMP_DIR"
MDAN_SRC="$TMP_DIR/MDAN-main"

# Copy MDAN files
echo "  📁 Copying files to $INSTALL_DIR..."
cp -r "$MDAN_SRC/core" "$INSTALL_DIR/"
cp -r "$MDAN_SRC/agents" "$INSTALL_DIR/"
cp -r "$MDAN_SRC/phases" "$INSTALL_DIR/"
cp -r "$MDAN_SRC/templates" "$INSTALL_DIR/"
cp -r "$MDAN_SRC/integrations" "$INSTALL_DIR/"
cp -r "$MDAN_SRC/memory" "$INSTALL_DIR/"
cp -r "$MDAN_SRC/modules" "$INSTALL_DIR/" 2>/dev/null || true
cp -r "$MDAN_SRC/workflows" "$INSTALL_DIR/" 2>/dev/null || true
cp -r "$MDAN_SRC/skills" "$INSTALL_DIR/" 2>/dev/null || mkdir -p "$INSTALL_DIR/skills"
cp "$MDAN_SRC/MDAN.md" "$INSTALL_DIR/" 2>/dev/null || true
cp "$MDAN_SRC/MDAN.fr.md" "$INSTALL_DIR/" 2>/dev/null || true

# Cleanup
rm -rf "$TMP_DIR"

# Create the mdan command using the Node.js version instead of the bash version for better UX
echo "  🔧 Setting up CLI..."
cat > "$BIN_DIR/mdan" << 'MDAN_SCRIPT'
#!/bin/bash
# Wrapper to run the npx version of mdan-cli to ensure the interactive wizard works
npx --yes mdan-cli "$@"
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
echo "  mdan init                 # Interactive setup"
echo "  mdan init my-project      # Quick setup"
echo "  cd existing && mdan attach"
echo ""
