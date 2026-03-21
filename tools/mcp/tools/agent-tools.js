import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { existsSync } from 'node:fs';

export function registerAgentTools(server, discovery, projectRoot) {
  // List agents tool
  server.tool(
    'mdan_list-agents',
    'List all installed MDAN agents with their capabilities',
    {},
    async () => ({
      content: [{
        type: 'text',
        text: JSON.stringify(discovery.agents.map(a => ({
          name: a.name,
          displayName: a.displayName,
          title: a.title,
          icon: a.icon,
          role: a.role,
          module: a.module,
        })), null, 2),
      }],
    })
  );

  // Register each agent as a tool
  for (const agent of discovery.agents) {
    server.tool(
      `mdan_agent_${agent.name}`,
      `Consult ${agent.displayName} (${agent.title}): ${agent.role}`,
      {
        question: { type: 'string', description: 'Question or topic to discuss with this agent' },
      },
      async ({ question }) => {
        const agentPath = join(projectRoot, agent.path);
        let agentContent = '';
        if (existsSync(agentPath)) {
          agentContent = await readFile(agentPath, 'utf-8');
        }

        // Check for customization
        const customPath = join(projectRoot, '_mdan/_config/agents', `${agent.module}-${agent.name}.customize.yaml`);
        let customContent = '';
        if (existsSync(customPath)) {
          customContent = await readFile(customPath, 'utf-8');
        }

        return {
          content: [{
            type: 'text',
            text: `# Agent: ${agent.icon} ${agent.displayName}\n` +
              `**Title:** ${agent.title}\n` +
              `**Role:** ${agent.role}\n` +
              `**Communication Style:** ${agent.communicationStyle}\n` +
              `**Principles:** ${agent.principles}\n\n` +
              `**Question:** ${question || '(ask the user)'}\n\n` +
              `---\n\n` +
              `Respond in character as ${agent.displayName}. ${agentContent}\n\n` +
              (customContent ? `## Customization:\n${customContent}` : ''),
          }],
        };
      }
    );
  }
}
