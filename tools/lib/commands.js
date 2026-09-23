// Renders IDE slash commands from the manifests. Each command is { slug, name, description, module, body }.
const yamlQuote = s => `'${String(s).replace(/'/g, "''")}'`;

export function agentSlug(agent) {
  return agent.module === 'core' ? `agent-${agent.name}` : `agent-${agent.module}-${agent.name}`;
}

function workflowBody(wf) {
  if (wf.kind !== 'yaml') {
    return `IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND: LOAD the FULL @{project-root}/${wf.path}, READ its entire contents and follow its directions exactly!`;
  }
  return [
    'IT IS CRITICAL THAT YOU FOLLOW THESE STEPS - while staying in character as the current agent persona you may have loaded:',
    '',
    '<steps CRITICAL="TRUE">',
    '1. Always LOAD the FULL @{project-root}/_mdan/core/tasks/workflow.xml',
    `2. READ its entire contents - this is the CORE OS for EXECUTING the specific workflow-config @{project-root}/${wf.path}`,
    `3. Pass the yaml path @{project-root}/${wf.path} as 'workflow-config' parameter to the workflow.xml instructions`,
    '4. Follow workflow.xml instructions EXACTLY as written to process and follow the specific workflow config and its instructions',
    '5. Save outputs after EACH section when generating any documents from templates',
    '</steps>',
  ].join('\n');
}

function agentBody(agent) {
  return [
    "You must fully embody this agent's persona and follow all activation instructions exactly as specified. NEVER break character until given an exit command.",
    '',
    '<agent-activation CRITICAL="TRUE">',
    `1. LOAD the FULL agent file from {project-root}/${agent.path}`,
    '2. READ its entire contents - this contains the complete agent persona, menu, and instructions',
    '3. FOLLOW every step in the <activation> section precisely',
    '4. DISPLAY the welcome/greeting as instructed',
    '5. PRESENT the numbered menu',
    '6. WAIT for user input before proceeding',
    '</agent-activation>',
  ].join('\n');
}

export function buildCommands({ agents, workflows, tasks }) {
  const commands = [];
  for (const wf of workflows) {
    commands.push({ slug: wf.name, name: wf.name, description: wf.description, module: wf.module, body: workflowBody(wf) });
  }
  for (const task of tasks) {
    commands.push({
      slug: task.name,
      name: task.name,
      description: task.description,
      module: task.module,
      body: `# ${task.name}\n\nRead the entire task file at: {project-root}/${task.path}\n\nFollow all instructions in the task file exactly as written.`,
    });
  }
  for (const agent of agents) {
    commands.push({
      slug: agentSlug(agent),
      name: agent.name,
      description: agent.title || agent.capabilities,
      module: agent.module,
      body: agentBody(agent),
    });
  }
  return commands.sort((a, b) => a.slug.localeCompare(b.slug));
}

// Gemini CLI / Qwen Code: TOML with a literal multi-line prompt; @{path} injects a file.
function tomlCommand(c) {
  const body = c.body
    .replace(/@\{project-root\}\/(\S+?)([,\s]|$)/g, '@{$1}$2')
    .replace(/\{project-root\}\//g, '');
  return `description = ${JSON.stringify(c.description)}\nprompt = """\n${body.replace(/"""/g, '\\"\\"\\"')}\n"""\n`;
}

// IDE targets: command directory (relative to the project), file name and renderer.
export const IDE_TARGETS = {
  'claude-code': {
    dir: '.claude/commands',
    file: c => `mdan-${c.slug}.md`,
    render: c => `---\nname: ${yamlQuote(c.name)}\ndescription: ${yamlQuote(c.description)}\n---\n\n${c.body}\n`,
  },
  cursor: {
    dir: '.cursor/commands',
    file: c => `mdan-${c.slug}.md`,
    render: c => `# ${c.description}\n\n${c.body}\n`,
  },
  opencode: {
    dir: '.opencode/command',
    file: c => `mdan-${c.slug}.md`,
    render: c => `---\ndescription: ${yamlQuote(c.description)}\n---\n\n${c.body}\n`,
  },
  gemini: {
    dir: '.gemini/commands',
    file: c => `mdan-${c.slug}.toml`,
    render: tomlCommand,
  },
  qwen: {
    dir: '.qwen/commands',
    file: c => `mdan-${c.slug}.toml`,
    render: tomlCommand,
  },
};
