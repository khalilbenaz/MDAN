import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { z } from 'zod';
import { safeJoin } from '../../lib/paths.js';
import { safe, text, nameSchema } from '../util.js';

async function renderAgent(projectRoot, agent, question) {
  const agentPath = safeJoin(projectRoot, agent.path);
  const agentContent = existsSync(agentPath) ? await readFile(agentPath, 'utf-8') : '';
  const customPath = safeJoin(projectRoot, '_mdan/_config/agents', `${agent.module}-${agent.name}.customize.yaml`);
  const customContent = existsSync(customPath) ? await readFile(customPath, 'utf-8') : '';

  return [
    `# Agent: ${agent.icon} ${agent.displayName}`,
    `**Title:** ${agent.title}`,
    `**Role:** ${agent.role}`,
    `**Communication Style:** ${agent.communicationStyle}`,
    `**Principles:** ${agent.principles}`,
    '',
    `**Question:** ${question || '(ask the user)'}`,
    `**Project root:** \`${projectRoot}\``,
    '',
    '---',
    '',
    `Respond in character as ${agent.displayName}.`,
    '',
    agentContent,
    customContent ? `\n## Customization\n\n${customContent}` : '',
  ].join('\n');
}

export function registerAgentTools(server, discovery, projectRoot) {
  const byName = new Map(discovery.agents.map(a => [a.name, a]));

  server.registerTool('mdan_list_agents', {
    description: 'List all installed MDAN agents with their roles',
    annotations: { readOnlyHint: true },
  }, safe(async () => text(JSON.stringify(discovery.agents.map(({ name, displayName, title, icon, role, module }) =>
    ({ name, displayName, title, icon, role, module })), null, 2))));

  server.registerTool('mdan_consult_agent', {
    description: 'Load an MDAN agent persona (with project customization) to answer in character',
    inputSchema: {
      name: nameSchema([...byName.keys()], 'Agent name (see mdan_list_agents)'),
      question: z.string().optional().describe('Question or topic to discuss with this agent'),
    },
    annotations: { readOnlyHint: true },
  }, safe(async ({ name, question }) => {
    const agent = byName.get(name);
    if (!agent) throw new Error(`Unknown agent '${name}'. Available: ${[...byName.keys()].join(', ')}`);
    return text(await renderAgent(projectRoot, agent, question));
  }));

  for (const agent of discovery.agents) {
    server.registerPrompt(`agent-${agent.name}`, {
      title: `${agent.icon} ${agent.displayName} — ${agent.title}`,
      description: agent.role || agent.title,
      argsSchema: { question: z.string().optional().describe('Question or topic for this agent') },
    }, async ({ question }) => ({
      messages: [{ role: 'user', content: { type: 'text', text: await renderAgent(projectRoot, agent, question) } }],
    }));
  }
}
