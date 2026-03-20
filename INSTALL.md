# MDAN Installation Guide

This guide will help you install and set up MDAN on your system.

## 📋 Prerequisites

Before installing MDAN, ensure you have the following:

- **Node.js** v20.0.0 or higher
- **npm** v9.0.0 or higher
- **Git** (for cloning the repository)
- **Python** v3.8 or higher (for running agents)
- An AI IDE (Claude Code, Cursor, or similar)

### Checking Prerequisites

```bash
# Check Node.js version
node --version  # Should be v20.0.0 or higher

# Check npm version
npm --version   # Should be v9.0.0 or higher

# Check Python version
python --version  # Should be v3.8 or higher

# Check Git version
git --version
```

## 🚀 Installation Methods

### Method 1: NPM Installation (Recommended)

This is the easiest way to install MDAN globally on your system.

```bash
# Install MDAN globally
npm install -g mdan-ai

# Verify installation
mdan-ai --version
```

**Package URL:** https://www.npmjs.com/package/mdan-ai

### Method 2: Local Installation

Install MDAN locally in your project directory.

```bash
# Create a new project directory
mkdir my-mdan-project
cd my-mdan-project

# Initialize MDAN
npx mdan-ai install
```

### Method 3: Clone from GitHub

Clone the repository and install dependencies manually.

```bash
# Clone the repository
git clone https://github.com/khalilbenaz/MDANV2.git
cd MDANV2

# Install dependencies
npm install

# Link globally
npm link

# Verify installation
mdan --version
```

**Repository URL:** https://github.com/khalilbenaz/MDANV2

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in your project root:

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your configuration
nano .env
```

Required environment variables:

```env
# AI Model Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# MCP Server Configuration (Optional)
BRAVE_API_KEY=your_brave_api_key_here
GITHUB_TOKEN=your_github_token_here

# MDAN Configuration
MDAN_LOG_LEVEL=info
MDAN_MAX_CONCURRENT_AGENTS=5
```

### MCP Server Configuration

MDAN uses the Model Context Protocol (MCP) for tool access. The configuration is in `.mcp.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/your/project"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git", "--repository", "/path/to/your/project"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

**Note:** Update the file paths to match your project directory.

### AI IDE Configuration

#### Claude Code

1. Open Claude Code
2. Open your project directory
3. The `CLAUDE.md` file will be automatically loaded
4. MDAN agents will be available in the agent selector

#### Cursor

1. Open Cursor
2. Open your project directory
3. The `.cursor/mcp.json` symlink will be automatically detected
4. MDAN agents will be available in the agent selector

## 🧪 Verification

After installation, verify that everything is working correctly:

```bash
# Run the test suite
npm test

# Run scenario tests
npm run test:scenarios

# Run evaluations
npm run test:evaluations
```

All tests should pass successfully.

## 📦 Module Installation

MDAN supports modular installation. You can install only the modules you need:

```bash
# Install only the FinTech pack
npx mdan-ai install --modules fintech

# Install multiple modules
npx mdan-ai install --modules fintech devops-azure db-optimization

# Install all modules
npx mdan-ai install --modules all
```

Available modules:
- `core` - Core MDAN framework
- `mmm` - Business Model & Management
- `mmb` - Module Builder
- `cis` - Creative Innovation Strategy
- `tea` - Test Engineering & Architecture
- `fintech` - FinTech Pack
- `devops-azure` - DevOps/Azure Pack
- `db-optimization` - Database Optimization Pack

## 🔧 Troubleshooting

### Common Issues

#### Issue: "node: command not found"

**Solution:** Install Node.js from [nodejs.org](https://nodejs.org)

#### Issue: "npm: command not found"

**Solution:** npm is included with Node.js. Reinstall Node.js.

#### Issue: "python: command not found"

**Solution:** Install Python from [python.org](https://python.org)

#### Issue: Tests fail with import errors

**Solution:** Ensure all dependencies are installed:
```bash
npm install
pip install -r requirements.txt
```

#### Issue: MCP servers not connecting

**Solution:** Check that the file paths in `.mcp.json` are correct and that you have the necessary API keys in `.env`.

### Getting Help

If you encounter any issues not covered here:

1. Check the [Documentation](./README.md)
2. Search [GitHub Issues](https://github.com/khalilbenaz/MDANV2/issues)
3. Create a new issue with detailed information about your problem

## 🚀 Next Steps

After successful installation:

1. Read the [Usage Guide](./USAGE.md) to learn how to use MDAN
2. Explore the [Agent List](./AGENTS_LIST.md) to see available agents
3. Check the [Architecture Documentation](./ARCHITECTURE.md) to understand the system
4. Start building with MDAN!

---

**Last Updated:** 28 February 2026
**Version:** 2.6.0