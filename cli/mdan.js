#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { intro, text, select, isCancel, cancel, outro, spinner } = require('@clack/prompts');
const pc = require('picocolors');

const VERSION = '2.5.1';
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
  console.log(`${colors.bold}UTILISATION${colors.nc}
  mdan <command> [options]

 ${colors.bold}COMMANDES${colors.nc}
  init [nom]              Creer un nouveau projet
  attach [--rebuild]       Ajouter MDAN a un projet existant
  status                   Afficher le statut du projet
  phase [1-5]              Afficher le guide d'une phase
  workflow [nom]           Afficher un workflow detaille
  module add [nom]        Installer un module (ex: agile-scrum)
  agent [nom]             Afficher le prompt d'un agent
  oc                       Copier le prompt de l'orchestrateur
  skills                   Lister les skills disponibles
  mcp [action]            Config MCP (init|validate|list)
  prompt [action]         Gerer les prompts (list|show <nom>)
  version                  Afficher la version

 ${colors.bold}EXEMPLES${colors.nc}
  mdan init mon-projet           # Nouveau projet
  cd mon-projet && mdan attach   # Projet existant
  mdan attach --rebuild          # Rebuild complet
  mdan mcp init                  # Generer .mcp.json
  mdan prompt list               # Lister les prompts

 ${colors.bold}AGENTS${colors.nc}
  product, architect, ux, dev, test, security, devops, doc
 `);
}

async function cmdInit(initialName) {
  intro(pc.bgCyan(pc.black(' MDAN v' + VERSION + ' - Assistant de creation ')));

  let name = initialName;
  
  if (!name) {
    const namePrompt = await text({
      message: 'Quel est le nom de votre projet ?',
      initialValue: 'mon-projet',
      validate(value) {
        if (value.length === 0) return 'Le nom est requis !';
      }
    });

    if (isCancel(namePrompt)) {
      cancel('Operation annulee.');
      return process.exit(0);
    }
    name = namePrompt;
  }
  
  const setupType = await select({
    message: 'Quel type de projet construisez-vous ?',
    options: [
      { value: 'standard', label: 'Application Web/Mobile standard', hint: 'Workflow 5 phases par defaut' },
      { value: 'micro', label: 'Micro projet', hint: 'Dev solo, une seule feature' },
      { value: 'api', label: 'API / SDK', hint: 'Pas de UI, oriente dev' },
      { value: 'product', label: 'Produit Scale-up', hint: 'Multi-mois, stakeholders' }
    ]
  });

  if (isCancel(setupType)) {
    cancel('Operation annulee.');
    return process.exit(0);
  }

  const s = spinner();
  s.start(`Creation de la structure du projet ${name}...`);
  
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
  
  s.stop(pc.green(`Projet ${name} initialise avec succes !`));
  
  outro(
    pc.bold('Prochaines etapes:\n') +
    `1. ${pc.cyan(`cd ${name}`)}\n` +
    `2. Ouvrez le dossier dans votre IDE (Cursor, Windsurf, etc.)\n` +
    `3. Ou executez ${pc.cyan('mdan oc')} et collez dans votre LLM prefere.`
  );
}

async function cmdAttach(rebuildMode) {
  intro(pc.bgMagenta(pc.black(' MDAN v' + VERSION + ' - Assistant d\'attachement ')));

  const projectName = path.basename(process.cwd());
  let isRebuild = rebuildMode === '--rebuild';

  if (!rebuildMode) {
    const action = await select({
      message: `Comment voulez-vous attacher MDAN a ${pc.bold(projectName)} ?`,
      options: [
        { value: 'attach', label: 'Attacher normalement', hint: 'Analyser le code existant et ajouter des features' },
        { value: 'rebuild', label: 'Mode Rebuild', hint: 'Analyser et tout reecrire from scratch' }
      ]
    });

    if (isCancel(action)) {
      cancel('Operation annulee.');
      return process.exit(0);
    }
    
    isRebuild = action === 'rebuild';
  }
  
  const s = spinner();
  s.start(isRebuild 
    ? `Preparation de l'environnement REBUILD pour ${projectName}...` 
    : `Attachement de MDAN a ${projectName}...`);
  
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
  
  s.stop(pc.green(`MDAN attache avec succes !`));
  
  outro(
    pc.bold('Prochaines etapes:\n') +
    `1. Ouvrez ce dossier dans votre IDE (Cursor, Windsurf, etc.)\n` +
    `2. Ou executez ${pc.cyan('mdan oc')} et collez le prompt dans Claude/ChatGPT\n\n` +
    (isRebuild 
      ? pc.magenta(`Prompt de demarrage: "MDAN REBUILD: Analyze and rewrite this project"`)
      : pc.cyan(`Prompt de demarrage: "MDAN: Analyze this project and help me [votre objectif]"`))
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
      console.log(`${colors.green}✅ Prompt de l'orchestrateur copie dans le presse-papier !${colors.nc}`);
      console.log('   Collez-le dans Claude, ChatGPT, ou votre LLM prefere.');
    } catch (e) {
      console.log(content);
      console.log(`\n${colors.yellow}⚠️  Impossible de copier automatiquement. Veuillez copier le texte ci-dessus.${colors.nc}`);
    }
  } else {
    console.log(`${colors.red}Fichier orchestrateur introuvable.${colors.nc}`);
  }
}

function cmdStatus() {
  if (fs.existsSync('mdan/orchestrator.md')) {
    console.log(`${colors.green}✅ MDAN est actif dans ce projet${colors.nc}`);
    if (fs.existsSync('mdan/STATUS.md')) {
      console.log(fs.readFileSync('mdan/STATUS.md', 'utf8'));
    }
  } else {
    console.log(`${colors.yellow}Pas de projet MDAN ici.${colors.nc}`);
    console.log('  Executer: mdan init [nom]  ou  mdan attach');
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
    console.log('Utilisation: mdan phase [1-5|nom] [copy]');
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
        console.log(`${colors.green}✅ Prompt de la phase ${name} copie dans le presse-papier !${colors.nc}`);
        console.log('   Collez-le dans votre LLM pour demarrer la phase.');
      } catch (e) {
        console.log(content);
        console.log(`\n${colors.yellow}⚠️  Impossible de copier automatiquement. Veuillez copier le texte ci-dessus.${colors.nc}`);
      }
    } else {
      console.log(`${colors.cyan}${colors.bold}Phase ${name}${colors.nc}`);
      console.log(content);
      console.log(`\n${colors.yellow}Astuce: Executez '${colors.cyan}mdan phase ${num} copy${colors.yellow}' pour copier ce contenu.${colors.nc}`);
    }
  } else {
    console.log(`${colors.red}Fichier de phase introuvable: ${file}${colors.nc}`);
  }
}

function cmdModule(action, name) {
  if (action !== 'add' || !name) {
    console.log('Utilisation: mdan module add [nom]');
    console.log('Modules disponibles:');
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
    console.log(`${colors.red}Module introuvable: ${name}${colors.nc}`);
    return;
  }

  console.log(`${colors.cyan}📦 Installation du module: ${colors.bold}${name}${colors.nc}`);
  
  if (!fs.existsSync('mdan')) {
    console.log(`${colors.yellow}⚠️  Pas de dossier mdan trouve. Etes-vous dans un projet MDAN ?${colors.nc}`);
    return;
  }

  // Copy agents
  if (fs.existsSync(`${moduleDir}/agents`)) {
    fs.readdirSync(`${moduleDir}/agents`).forEach(f => {
      fs.copyFileSync(`${moduleDir}/agents/${f}`, `mdan/agents/${f}`);
      console.log(`${colors.green}  Agent ajoute:${colors.nc} ${f}`);
    });
  }

  console.log(`\n${colors.green}✅ Module ${name} installe !${colors.nc}`);
}

function cmdWorkflow(name, action) {
  if (!name) {
    console.log('Utilisation: mdan workflow [nom] [copy]');
    console.log('Workflows disponibles:');
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
        console.log(`${colors.green}✅ Prompt du workflow ${name} copie dans le presse-papier !${colors.nc}`);
      } catch (e) {
        console.log(content);
        console.log(`\n${colors.yellow}⚠️  Impossible de copier automatiquement. Veuillez copier le texte ci-dessus.${colors.nc}`);
      }
    } else {
      console.log(`${colors.cyan}${colors.bold}Workflow: ${name}${colors.nc}`);
      console.log(content);
      console.log(`\n${colors.yellow}Astuce: Executez '${colors.cyan}mdan workflow ${name} copy${colors.yellow}' pour copier ce contenu.${colors.nc}`);
    }
  } else {
    console.log(`${colors.red}Workflow introuvable: ${name}${colors.nc}`);
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
    console.log('  Aucun skill installe');
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
    console.log(`${colors.green}✅ .mcp.json cree !${colors.nc}`);
    console.log('  Configurez votre IDE pour utiliser MCP avec ce fichier.');
  } else if (action === 'validate') {
    if (fs.existsSync('.mcp.json')) {
      try {
        JSON.parse(fs.readFileSync('.mcp.json', 'utf8'));
        console.log(`${colors.green}✅ .mcp.json est valide${colors.nc}`);
      } catch (e) {
        console.log(`${colors.red}❌ JSON invalide: ${e.message}${colors.nc}`);
      }
    } else {
      console.log(`${colors.yellow}⚠️  Pas de .mcp.json trouve${colors.nc}`);
    }
  } else if (action === 'list') {
    console.log(`${colors.cyan}Outils MCP:${colors.nc}`);
    console.log('  - mdan-state: Lire/ecrire l\'etat du projet');
    console.log('  - mdan-agents: Lister les agents MDAN');
    console.log('  - mdan-phases: Obtenir les informations des phases');
  } else {
    console.log('Utilisation: mdan mcp [init|validate|list]');
  }
}

function cmdPrompt(action, name) {
  const promptsDir = `${MDAN_DIR}/templates/prompts`;
  if (!fs.existsSync(promptsDir)) {
    console.log(`${colors.yellow}Pas de dossier de prompts trouve${colors.nc}`);
    return;
  }
  
  if (!action || action === 'list') {
    console.log(`${colors.cyan}Prompts disponibles:${colors.nc}`);
    fs.readdirSync(promptsDir).filter(f => f.endsWith('.yaml')).forEach(f => {
      console.log(`  ${f.replace('.yaml', '')}`);
    });
  } else if (action === 'show' && name) {
    const file = `${promptsDir}/${name}.yaml`;
    if (fs.existsSync(file)) {
      console.log(fs.readFileSync(file, 'utf8'));
    } else {
      console.log(`${colors.red}Prompt introuvable: ${name}${colors.nc}`);
    }
  } else {
    console.log('Utilisation: mdan prompt [list|show <nom>]');
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
        message: 'Que souhaitez-vous faire ?',
        options: [
          { value: 'init', label: 'Creer un nouveau projet', hint: 'Commencer a zero' },
          { value: 'attach', label: 'Attacher a un projet existant', hint: 'Ajouter MDAN a ce dossier' },
          { value: 'help', label: 'Afficher l\'aide', hint: 'Voir toutes les commandes' }
        ]
      });

      if (isCancel(action)) {
        cancel('Operation annulee.');
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
