import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { z } from 'zod';
import { safeJoin } from '../../lib/paths.js';
import { safe, text, nameSchema } from '../util.js';
import { memoryBriefing } from '../../lib/memory.js';
import { resolveCustomization, renderCustomization, customize } from '../../lib/customize.js';

async function renderAgent(contentRoot, agent, question, projectRoot = contentRoot) {
  const agentPath = safeJoin(contentRoot, agent.path);
  const agentContent = existsSync(agentPath) ? await readFile(agentPath, 'utf-8') : '';
  const customization = renderCustomization(resolveCustomization(contentRoot, projectRoot, agent.name, agent.module));

  return [
    `# Agent: ${agent.icon} ${agent.displayName}`,
    `**Title:** ${agent.title}`,
    `**Role:** ${agent.role}`,
    `**Communication Style:** ${agent.communicationStyle}`,
    `**Principles:** ${agent.principles}`,
    '',
    `**Question:** ${question || '(ask the user)'}`,
    `**Project root:** \`${contentRoot}\``,
    '',
    memoryBriefing(projectRoot, agent.name),
    '',
    `Store anything worth remembering for next time with mdan_memory_remember { agent: "${agent.name}" }.`,
    '',
    '---',
    '',
    `Respond in character as ${agent.displayName}.`,
    '',
    agentContent,
    customization ? `\n${customization}` : '',
  ].join('\n');
}

export function registerAgentTools(server, discovery, contentRoot, projectRoot = contentRoot) {
  const byName = new Map(discovery.agents.map(a => [a.name, a]));

  server.registerTool('mdan_list_agents', {
    description: 'List all installed MDAN agents with their roles',
    annotations: { readOnlyHint: true },
  }, safe(async () => text(JSON.stringify(discovery.agents.map(({ name, displayName, title, icon, role, module }) =>
    ({ name, displayName, title, icon, role, module })), null, 2))));

  server.registerTool('mdan_consult_agent', {
    description: 'Load an MDAN agent persona (with layered customization and its memories) to answer in character',
    inputSchema: {
      name: nameSchema([...byName.keys()], 'Agent name (see mdan_list_agents)'),
      question: z.string().optional().describe('Question or topic to discuss with this agent'),
    },
    annotations: { readOnlyHint: true },
  }, safe(async ({ name, question }) => {
    const agent = byName.get(name);
    if (!agent) throw new Error(`Unknown agent '${name}'. Available: ${[...byName.keys()].join(', ')}`);
    return text(await renderAgent(contentRoot, agent, question, projectRoot));
  }));

  server.registerTool('mdan_customize_agent', {
    description: 'Customize an agent without editing its file: team layer (_mdan/custom/<agent>.yaml, versioned) or personal layer (<agent>.user.yaml, git-ignored). Values are merged into the layer',
    inputSchema: {
      agent: nameSchema([...byName.keys()], 'Agent name'),
      layer: z.enum(['team', 'user']).default('team'),
      displayName: z.string().optional().describe('Override the persona name'),
      communication_style: z.string().optional(),
      principles: z.array(z.string()).optional().describe('Principles appended to the persona'),
      critical_actions: z.array(z.string()).optional().describe('Actions run right after activation'),
      memories: z.array(z.string()).optional().describe('Permanent facts the agent must know'),
      menu: z.array(z.object({
        trigger: z.string(),
        description: z.string(),
        exec: z.string().optional(),
        workflow: z.string().optional(),
      })).optional(),
    },
  }, safe(async ({ agent, layer, displayName, communication_style, principles, critical_actions, memories, menu }) => {
    if (!byName.has(agent)) throw new Error(`Unknown agent '${agent}'`);
    const patch = JSON.parse(JSON.stringify({
      agent: displayName ? { metadata: { name: displayName } } : undefined,
      persona: { communication_style, principles },
      critical_actions,
      memories,
      menu,
    }));
    const { file } = customize(projectRoot, agent, layer, patch);
    return text(`Saved ${layer} customization for ${agent} in ${file}. It applies the next time the agent is loaded.`);
  }));

  for (const agent of discovery.agents) {
    server.registerPrompt(`agent-${agent.name}`, {
      title: `${agent.icon} ${agent.displayName} — ${agent.title}`,
      description: agent.role || agent.title,
      argsSchema: { question: z.string().optional().describe('Question or topic for this agent') },
    }, async ({ question }) => ({
      messages: [{ role: 'user', content: { type: 'text', text: await renderAgent(contentRoot, agent, question, projectRoot) } }],
    }));
  }
}
