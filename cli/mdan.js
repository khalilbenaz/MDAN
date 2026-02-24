#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { intro, text, select, isCancel, cancel, outro, spinner } = require('@clack/prompts');
const pc = require('picocolors');

const VERSION = '2.4.1';
const MDAN_DIR = path.resolve(__dirname, '..');

// Colors
const colors = {
  red: '\x1b[0;31m',
  green: '\x1b[0;32m',
  yellow: '\x1b[1;33m',
  cyan: '\x1b[0;36m',
  magenta: '\x1b[0;35m',
  bold: '\x1b[1m',
  nc: '\x1b[0m'
};

function banner() {
  console.log(`${colors.cyan}
  ███╗   ███╗██████╗  █████╗ ███╗   ██╗
  ████╗ ████║██╔══██╗██╔══██╗████╗  ██║
  ██╔████╔██║██║  ██║███████║██╔██╗ ██║
  ██║╚██╔╝██║██║  ██║██╔══██║██║╚██╗██║
  ██║ ╚═╝ ██║██████╔╝██║  ██║██║ ╚████║
  ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
${colors.nc}
  ${colors.bold}Multi-Agent Development Agentic Network${colors.nc} v${VERSION}
`);
}

function showHelp() {
  banner();
  console.log(`${colors.bold}USAGE${colors.nc}
  mdan <command> [options]

 ${colors.bold}COMMANDS${colors.nc}
  init [name]              Create a new project
  attach [--rebuild]       Add MDAN to existing project
  status                   Show project status
  phase [1-5]              Show phase guide
  workflow [name]          Show granular workflow
  module add [name]        Install a domain module (e.g., agile-scrum)
  agent [name]             Show agent prompt
  oc                       Copy orchestrator prompt to clipboard
  skills                   List available skills
  mcp [action]             MCP config (init|validate|list)
  prompt [action]          Manage prompts (list|show <name>)
  version                  Show version

 ${colors.bold}EXAMPLES${colors.nc}
  mdan init my-app              # New project
  cd my-project && mdan attach  # Existing project
  mdan attach --rebuild         # Rebuild from scratch
  mdan mcp init                 # Generate .mcp.json
  mdan prompt list              # List versioned prompts

 ${colors.bold}AGENTS${colors.nc}
  product, architect, ux, dev, test, security, devops, doc
 `);
}

async function cmdInit(initialName) {
  intro(pc.bgCyan(pc.black(' MDAN v' + VERSION + ' - Initialization Wizard ')));

  let name = initialName;
  
  if (!name) {
    const namePrompt = await text({
      message: 'What is your project name?',
      initialValue: 'my-project',
      validate(value) {
        if (value.length === 0) return 'Name is required!';
      }
    });

    if (isCancel(namePrompt)) {
      cancel('Operation cancelled.');
      return process.exit(0);
    }
    name = namePrompt;
  }
  
  const setupType = await select({
    message: 'What kind of project are you building?',
    options: [
      { value: 'standard', label: 'Standard Web/Mobile App', hint: 'Default 5-phase workflow' },
      { value: 'micro', label: 'Micro Project', hint: 'Solo dev, single feature, simple' },
      { value: 'api', label: 'API / SDK', hint: 'No UI, dev-focused' },
      { value: 'product', label: 'Scale-up Product', hint: 'Multi-month, stakeholders' }
    ]
  });

  if (isCancel(setupType)) {
    cancel('Operation cancelled.');
    return process.exit(0);
  }

  const s = spinner();
  s.start(`Creating ${name} project structure...`);
  
  const dirs = [
    `${name}/mdan/agents`,
    `${name}/mdan/skills`,
    `${name}/mdan_output`,
    `${name}/.claude/skills`,
    `${name}/.github`,
    `${name}/tests/scenarios`,
    `${name}/tests/evaluations`,
    `${name}/templates/prompts`
  ];
  
  dirs.forEach(dir => fs.mkdirSync(dir, { recursive: true }));
  
  fs.copyFileSync(`${MDAN_DIR}/core/orchestrator.md`, `${name}/mdan/orchestrator.md`);
  fs.copyFileSync(`${MDAN_DIR}/core/universal-envelope.md`, `${name}/mdan/universal-envelope.md`);
  
  fs.readdirSync(`${MDAN_DIR}/agents`).filter(f => f.endsWith('.md')).forEach(f => {
    fs.copyFileSync(`${MDAN_DIR}/agents/${f}`, `${name}/mdan/agents/${f}`);
  });
  
  fs.readdirSync(`${MDAN_DIR}/templates`).filter(f => f.endsWith('.md')).forEach(f => {
    fs.copyFileSync(`${MDAN_DIR}/templates/${f}`, `${name}/mdan_output/${f}`);
  });
  
  // Copy skills
  const skillsDir = `${MDAN_DIR}/skills`;
  if (fs.existsSync(skillsDir)) {
    fs.readdirSync(skillsDir).forEach(skill => {
      const src = `${skillsDir}/${skill}`;
      const dest1 = `${name}/mdan/skills/${skill}`;
      const dest2 = `${name}/.claude/skills/${skill}`;
      if (fs.statSync(src).isDirectory()) {
        fs.cpSync(src, dest1, { recursive: true });
        fs.cpSync(src, dest2, { recursive: true });
      }
    });
  }
  
  // Create .cursorrules
  let cursorrules = fs.readFileSync(`${MDAN_DIR}/core/orchestrator.md`, 'utf8');
  cursorrules += '\n\n## CURSOR INSTRUCTIONS\nAgent files are in mdan/agents/\nSkills are in mdan/skills/';
  fs.writeFileSync(`${name}/.cursorrules`, cursorrules);
  fs.copyFileSync(`${name}/.cursorrules`, `${name}/.windsurfrules`);
  fs.copyFileSync(`${MDAN_DIR}/core/orchestrator.md`, `${name}/.github/copilot-instructions.md`);
  
  fs.writeFileSync(`${name}/README.md`, `# ${name}\n\n> Built with MDAN (${setupType} profile)\n`);
  
  // Copy AGENTS.md and generate .mcp.json
  if (fs.existsSync(`${MDAN_DIR}/AGENTS.md`)) {
    fs.copyFileSync(`${MDAN_DIR}/AGENTS.md`, `${name}/AGENTS.md`);
  }
  
  const mcpConfig = {
    mcpServers: { "mdan-memory": { command: "node", args: ["-e", "console.log('MDAN MCP')"] } },
    metadata: { version: VERSION, framework: "mdan", generated: new Date().toISOString().split('T')[0] },
    capabilities: {
      scenarios: { enabled: true, test_paths: ["tests/scenarios/", "templates/tests/scenarios/"] },
      evaluations: { enabled: true, eval_paths: ["tests/evaluations/", "templates/tests/evaluations/"] },
      prompts: { enabled: true, prompt_paths: ["templates/prompts/"], registry: "templates/prompts.json" }
    },
    quality_gates: { min_test_coverage: 80, require_evaluations: true, require_scenarios: false }
  };
  fs.writeFileSync(`${name}/.mcp.json`, JSON.stringify(mcpConfig, null, 2));
  
  s.stop(pc.green(`Project ${name} initialized successfully!`));
  
  outro(
    pc.bold('Next steps:\n') +
    `1. ${pc.cyan(`cd ${name}`)}\n` +
    `2. Open the folder in your IDE (Cursor, Windsurf, etc.)\n` +
    `3. Or run ${pc.cyan('mdan oc')} and paste into your favorite LLM chat.`
  );
}

async function cmdAttach(rebuildMode) {
  intro(pc.bgMagenta(pc.black(' MDAN v' + VERSION + ' - Attach Wizard ')));

  const projectName = path.basename(process.cwd());
  let isRebuild = rebuildMode === '--rebuild';

  if (!rebuildMode) {
    const action = await select({
      message: `How do you want to attach MDAN to ${pc.bold(projectName)}?`,
      options: [
        { value: 'attach', label: 'Attach normally', hint: 'Analyze existing codebase and add features' },
        { value: 'rebuild', label: 'Rebuild Mode', hint: 'Analyze then rewrite EVERYTHING from scratch' }
      ]
    });

    if (isCancel(action)) {
      cancel('Operation cancelled.');
      return process.exit(0);
    }
    
    isRebuild = action === 'rebuild';
  }
  
  const s = spinner();
  s.start(isRebuild 
    ? `Preparing REBUILD environment for ${projectName}...` 
    : `Attaching MDAN to ${projectName}...`);
  
  fs.mkdirSync('mdan/agents', { recursive: true });
  fs.mkdirSync('mdan/skills', { recursive: true });
  fs.mkdirSync('.claude/skills', { recursive: true });
  fs.mkdirSync('.github', { recursive: true });
  fs.mkdirSync('tests/scenarios', { recursive: true });
  fs.mkdirSync('tests/evaluations', { recursive: true });
  fs.mkdirSync('templates/prompts', { recursive: true });
  
  fs.copyFileSync(`${MDAN_DIR}/core/orchestrator.md`, 'mdan/orchestrator.md');
  fs.copyFileSync(`${MDAN_DIR}/core/universal-envelope.md`, 'mdan/universal-envelope.md');
  
  fs.readdirSync(`${MDAN_DIR}/agents`).filter(f => f.endsWith('.md')).forEach(f => {
    fs.copyFileSync(`${MDAN_DIR}/agents/${f}`, `mdan/agents/${f}`);
  });
  
  // Copy skills
  const skillsDir = `${MDAN_DIR}/skills`;
  if (fs.existsSync(skillsDir)) {
    fs.readdirSync(skillsDir).forEach(skill => {
      const src = `${skillsDir}/${skill}`;
      if (fs.statSync(src).isDirectory()) {
        fs.cpSync(src, `mdan/skills/${skill}`, { recursive: true });
        fs.cpSync(src, `.claude/skills/${skill}`, { recursive: true });
      }
    });
  }
  
  // Create .cursorrules
  let cursorrules = fs.readFileSync(`${MDAN_DIR}/core/orchestrator.md`, 'utf8');
  if (isRebuild) {
    cursorrules += '\n\n## REBUILD MODE\nAnalyze existing code then rewrite from scratch.';
  } else {
    cursorrules += '\n\n## EXISTING PROJECT\nAnalyze codebase before making changes.';
  }
  fs.writeFileSync('.cursorrules', cursorrules);
  fs.copyFileSync('.cursorrules', '.windsurfrules');
  fs.copyFileSync(`${MDAN_DIR}/core/orchestrator.md`, '.github/copilot-instructions.md');
  
  // Copy AGENTS.md and generate .mcp.json
  if (fs.existsSync(`${MDAN_DIR}/AGENTS.md`)) {
    fs.copyFileSync(`${MDAN_DIR}/AGENTS.md`, 'AGENTS.md');
  }
  
  const mcpConfig = {
    mcpServers: { "mdan-memory": { command: "node", args: ["-e", "console.log('MDAN MCP')"] } },
    metadata: { version: VERSION, framework: "mdan", generated: new Date().toISOString().split('T')[0] },
    capabilities: {
      scenarios: { enabled: true, test_paths: ["tests/scenarios/", "templates/tests/scenarios/"] },
      evaluations: { enabled: true, eval_paths: ["tests/evaluations/", "templates/tests/evaluations/"] },
      prompts: { enabled: true, prompt_paths: ["templates/prompts/"], registry: "templates/prompts.json" }
    },
    quality_gates: { min_test_coverage: 80, require_evaluations: true, require_scenarios: false }
  };
  fs.writeFileSync('.mcp.json', JSON.stringify(mcpConfig, null, 2));
  
  s.stop(pc.green(`MDAN attached successfully!`));
  
  outro(
    pc.bold('Next steps:\n') +
    `1. Open this folder in your IDE (Cursor, Windsurf, etc.)\n` +
    `2. Or run ${pc.cyan('mdan oc')} and paste the prompt into Claude/ChatGPT\n\n` +
    (isRebuild 
      ? pc.magenta(`Start prompt: "MDAN REBUILD: Analyze and rewrite this project"`)
      : pc.cyan(`Start prompt: "MDAN: Analyze this project and help me [your goal]"`))
  );
}

function cmdOc() {
  let orchFile = 'mdan/orchestrator.md';
  if (!fs.existsSync(orchFile)) {
    orchFile = `${MDAN_DIR}/core/orchestrator.md`;
  }
  
  if (fs.existsSync(orchFile)) {
    const content = fs.readFileSync(orchFile, 'utf8');
    try {
      if (process.platform === 'darwin') {
        execSync('pbcopy', { input: content });
      } else if (process.platform === 'win32') {
        execSync('clip', { input: content });
      } else if (process.platform === 'linux') {
        try {
          execSync('xclip -selection clipboard', { input: content });
        } catch (e) {
          execSync('wl-copy', { input: content });
        }
      } else {
        throw new Error('Unsupported platform');
      }
      console.log(`${colors.green}✅ Orchestrator prompt copied to clipboard!${colors.nc}`);
      console.log('   Paste it into Claude, ChatGPT, or your favorite LLM.');
    } catch (e) {
      console.log(content);
      console.log(`\n${colors.yellow}⚠️  Could not copy to clipboard automatically. Please copy the text above.${colors.nc}`);
    }
  } else {
    console.log(`${colors.red}Orchestrator file not found.${colors.nc}`);
  }
}

function cmdStatus() {
  if (fs.existsSync('mdan/orchestrator.md')) {
    console.log(`${colors.green}✅ MDAN is active in this project${colors.nc}`);
    if (fs.existsSync('mdan/STATUS.md')) {
      console.log(fs.readFileSync('mdan/STATUS.md', 'utf8'));
    }
  } else {
    console.log(`${colors.yellow}No MDAN project here.${colors.nc}`);
    console.log('  Run: mdan init [name]  or  mdan attach');
  }
}

function cmdPhase(num, action) {
  const phases = {
    '1': ['01-discover.md', 'DISCOVER'],
    'discover': ['01-discover.md', 'DISCOVER'],
    '2': ['02-design.md', 'DESIGN'],
    'design': ['02-design.md', 'DESIGN'],
    '3': ['03-build.md', 'BUILD'],
    'build': ['03-build.md', 'BUILD'],
    '4': ['04-verify.md', 'VERIFY'],
    'verify': ['04-verify.md', 'VERIFY'],
    '5': ['05-ship.md', 'SHIP'],
    'ship': ['05-ship.md', 'SHIP']
  };
  
  if (!phases[num]) {
    console.log('Usage: mdan phase [1-5|name] [copy]');
    return;
  }
  
  const [file, name] = phases[num];
  const phaseFile = `${MDAN_DIR}/phases/${file}`;
  
  if (fs.existsSync(phaseFile)) {
    const content = fs.readFileSync(phaseFile, 'utf8');
    
    if (action === 'copy' || action === '-c') {
      try {
        if (process.platform === 'darwin') {
          execSync('pbcopy', { input: content });
        } else if (process.platform === 'win32') {
          execSync('clip', { input: content });
        } else if (process.platform === 'linux') {
          try {
            execSync('xclip -selection clipboard', { input: content });
          } catch (e) {
            execSync('wl-copy', { input: content });
          }
        } else {
          throw new Error('Unsupported platform');
        }
        console.log(`${colors.green}✅ Phase ${name} prompt copied to clipboard!${colors.nc}`);
        console.log('   Paste it into your LLM to start the phase.');
      } catch (e) {
        console.log(content);
        console.log(`\n${colors.yellow}⚠️  Could not copy automatically. Please copy the text above.${colors.nc}`);
      }
    } else {
      console.log(`${colors.cyan}${colors.bold}Phase ${name}${colors.nc}`);
      console.log(content);
      console.log(`\n${colors.yellow}Tip: Run '${colors.cyan}mdan phase ${num} copy${colors.yellow}' to copy this content to clipboard.${colors.nc}`);
    }
  } else {
    console.log(`${colors.red}Phase file not found: ${file}${colors.nc}`);
  }
}

function cmdModule(action, name) {
  if (action !== 'add' || !name) {
    console.log('Usage: mdan module add [name]');
    console.log('Available modules:');
    if (fs.existsSync(`${MDAN_DIR}/modules`)) {
      fs.readdirSync(`${MDAN_DIR}/modules`).forEach(m => {
        const stat = fs.statSync(`${MDAN_DIR}/modules/${m}`);
        if (stat.isDirectory()) console.log(`  ${m}`);
      });
    }
    return;
  }

  const moduleDir = `${MDAN_DIR}/modules/${name}`;
  if (!fs.existsSync(moduleDir)) {
    console.log(`${colors.red}Module not found: ${name}${colors.nc}`);
    return;
  }

  console.log(`${colors.cyan}📦 Installing module: ${colors.bold}${name}${colors.nc}`);
  
  if (!fs.existsSync('mdan')) {
    console.log(`${colors.yellow}⚠️  No mdan folder found. Are you in an MDAN project?${colors.nc}`);
    return;
  }

  // Copy agents
  if (fs.existsSync(`${moduleDir}/agents`)) {
    fs.readdirSync(`${moduleDir}/agents`).forEach(f => {
      fs.copyFileSync(`${moduleDir}/agents/${f}`, `mdan/agents/${f}`);
      console.log(`${colors.green}  Added agent:${colors.nc} ${f}`);
    });
  }

  console.log(`\n${colors.green}✅ Module ${name} installed!${colors.nc}`);
}

function cmdWorkflow(name, action) {
  if (!name) {
    console.log('Usage: mdan workflow [name] [copy]');
    console.log('Available workflows:');
    if (fs.existsSync(`${MDAN_DIR}/workflows`)) {
      fs.readdirSync(`${MDAN_DIR}/workflows`).forEach(f => {
        if (f.endsWith('.md')) console.log(`  ${f.replace('.md', '')}`);
      });
    }
    return;
  }
  
  const workflowFile = `${MDAN_DIR}/workflows/${name}.md`;
  
  if (fs.existsSync(workflowFile)) {
    const content = fs.readFileSync(workflowFile, 'utf8');
    
    if (action === 'copy' || action === '-c') {
      try {
        if (process.platform === 'darwin') {
          execSync('pbcopy', { input: content });
        } else if (process.platform === 'win32') {
          execSync('clip', { input: content });
        } else if (process.platform === 'linux') {
          try {
            execSync('xclip -selection clipboard', { input: content });
          } catch (e) {
            execSync('wl-copy', { input: content });
          }
        }
        console.log(`${colors.green}✅ Workflow ${name} prompt copied to clipboard!${colors.nc}`);
      } catch (e) {
        console.log(content);
        console.log(`\n${colors.yellow}⚠️  Could not copy automatically. Please copy the text above.${colors.nc}`);
      }
    } else {
      console.log(`${colors.cyan}${colors.bold}Workflow: ${name}${colors.nc}`);
      console.log(content);
      console.log(`\n${colors.yellow}Tip: Run '${colors.cyan}mdan workflow ${name} copy${colors.yellow}' to copy this content to clipboard.${colors.nc}`);
    }
  } else {
    console.log(`${colors.red}Workflow not found: ${name}${colors.nc}`);
  }
}

function cmdAgent(name) {
  const file = `${MDAN_DIR}/agents/${name}.md`;
  if (fs.existsSync(file)) {
    console.log(fs.readFileSync(file, 'utf8'));
  } else {
    console.log('Agents: product, architect, ux, dev, test, security, devops, doc');
  }
}

function cmdSkills() {
  console.log(`${colors.cyan}Skills:${colors.nc}`);
  const skillsDir = `${MDAN_DIR}/skills`;
  if (fs.existsSync(skillsDir)) {
    fs.readdirSync(skillsDir).forEach(s => console.log(`  ${s}`));
  } else {
    console.log('  No skills installed');
  }
}

function cmdMcp(action) {
  if (!action || action === 'init') {
    const mcpConfig = {
      mcpServers: {
        "mdan-memory": {
          command: "node",
          args: ["-e", "console.log(JSON.stringify({tools: []}))"]
        }
      },
      metadata: {
        version: VERSION,
        framework: "mdan",
        generated: new Date().toISOString().split('T')[0]
      },
      capabilities: {
        scenarios: { enabled: true, test_paths: ["tests/scenarios/", "templates/tests/scenarios/"] },
        evaluations: { enabled: true, eval_paths: ["tests/evaluations/", "templates/tests/evaluations/"] },
        prompts: { enabled: true, prompt_paths: ["templates/prompts/"], registry: "templates/prompts.json" }
      },
      quality_gates: {
        min_test_coverage: 80,
        require_evaluations: true,
        require_scenarios: false
      }
    };
    fs.writeFileSync('.mcp.json', JSON.stringify(mcpConfig, null, 2));
    console.log(`${colors.green}✅ .mcp.json created!${colors.nc}`);
    console.log('  Configure your IDE to use MCP with this file.');
  } else if (action === 'validate') {
    if (fs.existsSync('.mcp.json')) {
      try {
        JSON.parse(fs.readFileSync('.mcp.json', 'utf8'));
        console.log(`${colors.green}✅ .mcp.json is valid${colors.nc}`);
      } catch (e) {
        console.log(`${colors.red}❌ Invalid JSON: ${e.message}${colors.nc}`);
      }
    } else {
      console.log(`${colors.yellow}⚠️  No .mcp.json found${colors.nc}`);
    }
  } else if (action === 'list') {
    console.log(`${colors.cyan}MCP Tools:${colors.nc}`);
    console.log('  - mdan-state: Read/write project state');
    console.log('  - mdan-agents: List MDAN agents');
    console.log('  - mdan-phases: Get phase information');
  } else {
    console.log('Usage: mdan mcp [init|validate|list]');
  }
}

function cmdPrompt(action, name) {
  const promptsDir = `${MDAN_DIR}/templates/prompts`;
  if (!fs.existsSync(promptsDir)) {
    console.log(`${colors.yellow}No prompts directory found${colors.nc}`);
    return;
  }
  
  if (!action || action === 'list') {
    console.log(`${colors.cyan}Available Prompts:${colors.nc}`);
    fs.readdirSync(promptsDir).filter(f => f.endsWith('.yaml')).forEach(f => {
      console.log(`  ${f.replace('.yaml', '')}`);
    });
  } else if (action === 'show' && name) {
    const file = `${promptsDir}/${name}.yaml`;
    if (fs.existsSync(file)) {
      console.log(fs.readFileSync(file, 'utf8'));
    } else {
      console.log(`${colors.red}Prompt not found: ${name}${colors.nc}`);
    }
  } else {
    console.log('Usage: mdan prompt [list|show <name>]');
  }
}

// Main
const [,, cmd, ...args] = process.argv;

async function main() {
  if (!cmd || cmd === 'help' || cmd === '--help' || cmd === '-h') {
    if (!cmd) {
      // Interactive Wizard Default
      intro(pc.bgCyan(pc.black(' MDAN v' + VERSION + ' ')));
      const action = await select({
        message: 'What would you like to do?',
        options: [
          { value: 'init', label: 'Create a new project', hint: 'Start fresh' },
          { value: 'attach', label: 'Attach to existing project', hint: 'Add MDAN to this folder' },
          { value: 'help', label: 'Show Help', hint: 'See all commands' }
        ]
      });

      if (isCancel(action)) {
        cancel('Operation cancelled.');
        return process.exit(0);
      }

      if (action === 'init') {
        return cmdInit();
      } else if (action === 'attach') {
        return cmdAttach();
      } else if (action === 'help') {
        showHelp();
        return;
      }
    } else {
      showHelp();
    }
    return;
  }

  switch (cmd) {
    case 'init':
      await cmdInit(args[0]);
      break;
    case 'attach':
      await cmdAttach(args[0]);
      break;
    case 'oc':
      cmdOc();
      break;
    case 'status':
      cmdStatus();
      break;
    case 'phase':
      cmdPhase(args[0], args[1]);
      break;
    case 'module':
      cmdModule(args[0], args[1]);
      break;
    case 'workflow':
      cmdWorkflow(args[0], args[1]);
      break;
    case 'agent':
      cmdAgent(args[0]);
      break;
    case 'skills':
      cmdSkills();
      break;
    case 'mcp':
      cmdMcp(args[0]);
      break;
    case 'prompt':
      cmdPrompt(args[0], args[1]);
      break;
    case 'version':
    case '-v':
      console.log(`MDAN v${VERSION}`);
      break;
    default:
      console.log(`Unknown: ${cmd}. Run: mdan help`);
  }
}
main().catch(console.error);
