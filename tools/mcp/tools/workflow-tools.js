import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { z } from 'zod';
import { safeJoin } from '../../lib/paths.js';
import { loadState } from '../../lib/state.js';
import { safe, text, nameSchema } from '../util.js';

const RULES = '_mdan/core/rules.md';

async function readContentFile(root, rel) {
  const full = safeJoin(root, rel);
  if (!existsSync(full)) throw new Error(`File not found: ${rel}`);
  return readFile(full, 'utf-8');
}

function progressSection(wf, projectRoot) {
  const state = loadState(projectRoot);
  const current = state.current_workflow?.name === wf.name ? state.current_workflow : null;
  const done = state.workflows_completed.find(w => w.name === wf.name);
  const lines = ['', '## Progress tracking', ''];
  if (current?.step) {
    lines.push(`⏯️ **Resume:** this workflow was interrupted at step \`${current.step}\`${current.step_file ? ` (\`${current.step_file}\`)` : ''}. ` +
      'Offer the user to resume there (load that step file) or restart from the beginning.', '');
  } else if (done) {
    lines.push(`ℹ️ This workflow was already completed on ${done.completed_at}. Ask whether to update the existing artifact or start over.`, '');
  }
  if (state.artifacts.length) {
    lines.push('Existing project artifacts (use them as inputs):', ...state.artifacts.map(a => `- \`${a.id}\` → ${a.path}`), '');
  }
  lines.push(
    `- At the start: \`mdan_state_update { action: "start", workflow: "${wf.name}" }\``,
    `- On each new step: \`mdan_state_update { action: "step", workflow: "${wf.name}", step, stepFile }\``,
    `- At the end: \`mdan_state_update { action: "complete", workflow: "${wf.name}", artifacts: [{ id, path, inputs }], summary }\` ` +
      '— this registers the artifacts in the context graph and returns the next recommended workflow.',
    '- Without MCP tools, update `_mdan/state/MDAN-STATE.json` directly (current_workflow, workflows_completed, artifacts).',
  );
  return lines.join('\n');
}

export async function renderWorkflow(contentRoot, wf, topic, projectRoot = contentRoot) {
  const parts = [
    `# Execute Workflow: ${wf.name}`,
    '',
    `**Topic:** ${topic || '(ask the user)'}`,
    `**Project root:** \`${contentRoot}\` — resolve every \`{project-root}\` in the files below against it.`,
  ];
  if (existsSync(safeJoin(contentRoot, RULES))) {
    parts.push('', '## Mandatory rules', '', await readContentFile(contentRoot, RULES));
  }
  parts.push(progressSection(wf, projectRoot));
  if (wf.kind === 'yaml') {
    parts.push('', '## Workflow engine (_mdan/core/tasks/workflow.xml)', '',
      await readContentFile(contentRoot, '_mdan/core/tasks/workflow.xml'),
      '', `## Workflow config (${wf.path}) — pass it as 'workflow-config'`, '', await readContentFile(contentRoot, wf.path));
  } else {
    parts.push('', `## Wizard (${wf.path})`, '', 'Read and execute the wizard below step by step.', '',
      await readContentFile(contentRoot, wf.path));
  }
  return parts.join('\n');
}

export function registerWorkflowTools(server, discovery, contentRoot, projectRoot = contentRoot) {
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
    description: 'Load an MDAN workflow (wizard) with its rules and progress (resume point, existing artifacts) and return the instructions to execute step by step',
    inputSchema: {
      name: nameSchema([...byName.keys()], 'Workflow name (see mdan_list_workflows)'),
      topic: z.string().optional().describe('Topic or subject for the workflow'),
    },
    annotations: { readOnlyHint: true },
  }, safe(async ({ name, topic }) => text(await renderWorkflow(contentRoot, find(name), topic, projectRoot))));

  // Same workflows exposed as MCP prompts, so clients can offer them as slash commands.
  for (const wf of discovery.workflows) {
    server.registerPrompt(wf.name, {
      title: wf.name,
      description: wf.description || `MDAN workflow ${wf.name}`,
      argsSchema: { topic: z.string().optional().describe('Topic or subject for the workflow') },
    }, async ({ topic }) => ({
      messages: [{ role: 'user', content: { type: 'text', text: await renderWorkflow(contentRoot, wf, topic, projectRoot) } }],
    }));
  }
}
