import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { existsSync } from 'node:fs';

export function registerWorkflowTools(server, discovery, projectRoot) {
  // List workflows tool
  server.tool(
    'mdan_list-workflows',
    'List all available MDAN workflows with their descriptions',
    {},
    async () => ({
      content: [{
        type: 'text',
        text: JSON.stringify(discovery.workflows.map(w => ({
          name: w.name,
          description: w.description,
          module: w.module,
          path: w.path,
        })), null, 2),
      }],
    })
  );

  // Register each workflow as a tool
  for (const wf of discovery.workflows) {
    server.tool(
      `mdan_workflow_${wf.name}`,
      wf.description || `Execute the ${wf.name} workflow`,
      {
        topic: { type: 'string', description: 'Topic or subject for the workflow' },
      },
      async ({ topic }) => {
        const wizardPath = join(projectRoot, wf.path);
        if (!existsSync(wizardPath)) {
          return { content: [{ type: 'text', text: `Workflow file not found: ${wf.path}` }], isError: true };
        }

        const wizardContent = await readFile(wizardPath, 'utf-8');
        return {
          content: [{
            type: 'text',
            text: `# Execute Workflow: ${wf.name}\n\n` +
              `**Instructions:** Read and execute the workflow wizard below.\n` +
              `**Topic:** ${topic || '(ask the user)'}\n\n` +
              `---\n\n${wizardContent}`,
          }],
        };
      }
    );
  }
}
