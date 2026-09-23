import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { z } from 'zod';
import { safeJoin } from '../../lib/paths.js';
import { safe, text, nameSchema } from '../util.js';

const RULES = '_mdan/core/rules.md';

async function readProjectFile(projectRoot, rel) {
  const full = safeJoin(projectRoot, rel);
  if (!existsSync(full)) throw new Error(`File not found: ${rel}`);
  return readFile(full, 'utf-8');
}

export async function renderWorkflow(projectRoot, wf, topic) {
  const parts = [
    `# Execute Workflow: ${wf.name}`,
    '',
    `**Topic:** ${topic || '(ask the user)'}`,
    `**Project root:** \`${projectRoot}\` — resolve every \`{project-root}\` in the files below against it.`,
  ];
  if (existsSync(safeJoin(projectRoot, RULES))) {
    parts.push('', '## Mandatory rules', '', await readProjectFile(projectRoot, RULES));
  }
  if (wf.kind === 'yaml') {
    parts.push('', '## Workflow engine (_mdan/core/tasks/workflow.xml)', '',
      await readProjectFile(projectRoot, '_mdan/core/tasks/workflow.xml'),
      '', `## Workflow config (${wf.path}) — pass it as 'workflow-config'`, '', await readProjectFile(projectRoot, wf.path));
  } else {
    parts.push('', `## Wizard (${wf.path})`, '', 'Read and execute the wizard below step by step.', '',
      await readProjectFile(projectRoot, wf.path));
  }
  parts.push('', '## When the final artifact is written',
    '', 'Register it with `mdan_graph_add_node` (id, path, workflow) and link its inputs with `mdan_graph_add_edge` (relation `input_to`).');
  return parts.join('\n');
}

export function registerWorkflowTools(server, discovery, projectRoot) {
  const byName = new Map(discovery.workflows.map(w => [w.name, w]));
  const find = name => {
    const wf = byName.get(name);
    if (!wf) throw new Error(`Unknown workflow '${name}'. Available: ${[...byName.keys()].join(', ')}`);
    return wf;
  };

  server.registerTool('mdan_list_workflows', {
    description: 'List all installed MDAN workflows with their descriptions',
    annotations: { readOnlyHint: true },
  }, safe(async () => text(JSON.stringify(discovery.workflows.map(({ name, description, module, path }) =>
    ({ name, description, module, path })), null, 2))));

  server.registerTool('mdan_run_workflow', {
    description: 'Load an MDAN workflow (wizard) and return its full instructions to execute step by step',
    inputSchema: {
      name: nameSchema([...byName.keys()], 'Workflow name (see mdan_list_workflows)'),
      topic: z.string().optional().describe('Topic or subject for the workflow'),
    },
    annotations: { readOnlyHint: true },
  }, safe(async ({ name, topic }) => text(await renderWorkflow(projectRoot, find(name), topic))));

  // Same workflows exposed as MCP prompts, so clients can offer them as slash commands.
  for (const wf of discovery.workflows) {
    server.registerPrompt(wf.name, {
      title: wf.name,
      description: wf.description || `MDAN workflow ${wf.name}`,
      argsSchema: { topic: z.string().optional().describe('Topic or subject for the workflow') },
    }, async ({ topic }) => ({
      messages: [{ role: 'user', content: { type: 'text', text: await renderWorkflow(projectRoot, wf, topic) } }],
    }));
  }
}
